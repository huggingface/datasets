# coding=utf-8
# Copyright 2020 The HuggingFace Datasets Authors and the current dataset script contributor.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Wikisource dataset."""


import bz2
import codecs
import json
import re
import xml.etree.ElementTree as etree

import datasets


logger = datasets.logging.get_logger(__name__)


_CITATION = """\
@ONLINE {wikidump,
    author = {Wikimedia Foundation},
    title  = {Wikimedia Downloads},
    url    = {https://dumps.wikimedia.org}
}
"""

_DESCRIPTION = """\
Wikisource dataset containing cleaned articles for all languages.
"""

_HOMEPAGE = "https://dumps.wikimedia.org"

_LICENSE = "Creative Commons Attribution-ShareAlike 3.0 Unported"

_BASE_URL_TMPL = "https://dumps.wikimedia.org/{lang}wikisource/{date}/"
_INFO_FILE = "dumpstatus.json"

# Source: https://meta.wikimedia.org/wiki/Wikisource#List_of_Wikisources (accessed 2022-02-07)
WIKISOURCE_LANGUAGES = [
    "ang",
    "ar",
    "as",
    "az",
    "ban",
    "be",
    "bg",
    "bn",
    "br",
    "bs",
    "ca",
    "cs",
    "cy",
    "da",
    "de",
    "el",
    "en",
    "eo",
    "es",
    "et",
    "eu",
    "fa",
    "fi",
    "fo",
    "fr",
    "gl",
    "gu",
    "he",
    "hi",
    "hr",
    "ht",
    "hu",
    "hy",
    "id",
    "is",
    "it",
    "ja",
    "jv",
    "kn",
    "ko",
    "la",
    "li",
    "lij",
    "lt",
    "mk",
    "ml",
    "mr",
    "mul",
    "nap",
    "nl",
    "no",
    "or",
    "pa",
    "pl",
    "pms",
    "pt",
    "ro",
    "ru",
    "sa",
    "sah",
    "sk",
    "sl",
    "sr",
    "sv",
    "ta",
    "te",
    "th",
    "tr",
    "uk",
    "vec",
    "vi",
    "wa",
    "yi",
    "zh",
]


class WikisourceConfig(datasets.BuilderConfig):
    """BuilderConfig for Wikisource."""

    VERSION = datasets.Version("1.0.0")

    def __init__(self, language=None, date=None, text_min_length=100, version=None, **kwargs):
        """BuilderConfig for Wikisource.

        Args:
            language (str): Language code for the Wikisource dump to use.
            date (str): Date of the Wikisource dump in YYYYMMDD format. A list of
                available dates can be found at https://dumps.wikimedia.org/enwiki/.
            text_min_length (int): Minimum text length. Note that many pages just have a small amount of metadata but
                not contain the transcribed text.
            **kwargs: Keyword arguments forwarded to super.
        """
        super().__init__(
            name=f"{date}.{language}",
            description=f"Wikisource dataset for {language}, parsed from {date} dump.",
            version=version or self.VERSION,
            **kwargs,
        )
        self.date = date
        self.language = language
        self.text_min_length = text_min_length


class Wikisource(datasets.GeneratorBasedBuilder):
    """Wikisource dataset."""

    BUILDER_CONFIG_CLASS = WikisourceConfig
    BUILDER_CONFIGS = [
        WikisourceConfig(
            language=lang,
            date="20220120",
        )
        for lang in WIKISOURCE_LANGUAGES
    ]
    # DEFAULT_CONFIG_NAME = ""

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features({"title": datasets.Value("string"), "text": datasets.Value("string")}),
            supervised_keys=None,
            homepage=_HOMEPAGE,
            license=_LICENSE,
            citation=_CITATION,
            task_templates=[datasets.tasks.LanguageModeling(text_column="text")],
        )

    def _split_generators(self, dl_manager, pipeline):
        def _base_url(lang):
            return _BASE_URL_TMPL.format(lang=lang.replace("-", "_"), date=self.config.date)

        lang = self.config.language

        info_url = _base_url(lang) + _INFO_FILE
        # Use dictionary since testing mock always returns the same result.
        downloaded_files = dl_manager.download_and_extract({"info": info_url})

        xml_urls = []
        total_bytes = 0
        with open(downloaded_files["info"], encoding="utf-8") as f:
            dump_info = json.load(f)
        multistream_dump_info = dump_info["jobs"]["articlesmultistreamdump"]
        assert (
            multistream_dump_info["status"] == "done"
        ), "Specified dump (%s) multistream status is not 'done': %s" % (
            _base_url(lang),
            multistream_dump_info["status"],
        )

        for fname, info in multistream_dump_info["files"].items():
            if ".xml" not in fname:
                continue
            total_bytes += info["size"]
            xml_urls.append(_base_url(lang) + fname)

        # Use dictionary since testing mock always returns the same result.
        downloaded_files = dl_manager.download({"xml": xml_urls})
        if not pipeline.is_local():
            downloaded_files = dl_manager.ship_files_with_pipeline(downloaded_files, pipeline)

        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN, gen_kwargs={"filepaths": downloaded_files["xml"], "language": lang}
            )
        ]

    def _build_pcollection(self, pipeline, filepaths, language):
        """Build PCollection of examples in the raw (text) form."""
        import apache_beam as beam
        import mwparserfromhell

        def _extract_content(filepath):
            """Extracts article content from a single WikiMedia XML file."""
            logger.info("generating examples from = %s", filepath)
            with beam.io.filesystems.FileSystems.open(filepath) as f:
                f = bz2.BZ2File(filename=f)
                # Workaround due to: https://github.com/tensorflow/tensorflow/issues/33563
                utf_f = codecs.getreader("utf-8")(f)
                context = etree.iterparse(utf_f, events=("end",))
                for unused_event, elem in context:
                    if not elem.tag.endswith("page"):
                        continue
                    namespace = elem.tag[:-4]
                    title = elem.find(f"./{namespace}title").text
                    ns = elem.find(f"./{namespace}ns").text
                    id_ = elem.find(f"./{namespace}id").text

                    # Filter pages that are not in the "main" namespace.
                    if ns != "0":
                        elem.clear()
                        continue

                    raw_content = elem.find(f"./{namespace}revision/{namespace}text").text
                    elem.clear()

                    # Filter redirects.
                    if raw_content is None or raw_content.lower().startswith("#redirect"):
                        beam.metrics.Metrics.counter(language, "filtered-redirects").inc()
                        continue

                    beam.metrics.Metrics.counter(language, "extracted-examples").inc()
                    yield id_, title, raw_content

        def _clean_content(inputs):
            """Cleans raw wikicode to extract text."""
            id_, title, raw_content = inputs
            try:
                text = _parse_and_clean_wikicode(raw_content, parser=mwparserfromhell)
            except mwparserfromhell.parser.ParserError as e:
                beam.metrics.Metrics.counter(language, "parser-error").inc()
                logger.error("mwparserfromhell ParseError: %s", e)
                return

            if not text or len(text) < self.config.text_min_length:
                beam.metrics.Metrics.counter(language, "empty-clean-examples").inc()
                return

            beam.metrics.Metrics.counter(language, "cleaned-examples").inc()

            yield id_, {"title": title, "text": text}

        return (
            pipeline
            | "Initialize" >> beam.Create(filepaths)
            | "Extract content" >> beam.FlatMap(_extract_content)
            | "Distribute" >> beam.transforms.Reshuffle()
            | "Clean content" >> beam.FlatMap(_clean_content)
        )


def _parse_and_clean_wikicode(raw_content, parser):
    """Strip formatting and unwanted sections from raw page content."""
    wikicode = parser.parse(raw_content)

    # Filters for references, tables, and file/image links.
    re_rm_wikilink = re.compile("^(?:File|Image|Media):", flags=re.IGNORECASE | re.UNICODE)

    def rm_wikilink(obj):
        return bool(re_rm_wikilink.match(str(obj.title)))

    def rm_tag(obj):
        return str(obj.tag) in {"ref", "table"}

    def rm_template(obj):
        return obj.name.lower() in {"reflist", "notelist", "notelist-ua", "notelist-lr", "notelist-ur", "notelist-lg"}

    def try_remove_obj(obj, section):
        try:
            section.remove(obj)
        except ValueError:
            # For unknown reasons, objects are sometimes not found.
            pass

    section_text = []
    # Filter individual sections to clean.
    for section in wikicode.get_sections(flat=True, include_lead=True, include_headings=True):
        for obj in section.ifilter_wikilinks(matches=rm_wikilink, recursive=True):
            try_remove_obj(obj, section)
        for obj in section.ifilter_templates(matches=rm_template, recursive=True):
            try_remove_obj(obj, section)
        for obj in section.ifilter_tags(matches=rm_tag, recursive=True):
            try_remove_obj(obj, section)

        section_text.append(section.strip_code().strip())
    return "\n\n".join(section_text)
