# coding=utf-8
# Copyright 2020 The TensorFlow Datasets Authors and the HuggingFace Datasets Authors.
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

# Lint as: python3
"""Wikipedia dataset containing cleaned articles of all languages."""

from __future__ import absolute_import, division, print_function

import codecs
import json
import logging
import re
import xml.etree.cElementTree as etree

import six

import datasets


if six.PY3:
    import bz2  # pylint:disable=g-import-not-at-top
else:
    # py2's built-in bz2 package does not support reading from file objects.
    import bz2file as bz2  # pylint:disable=g-import-not-at-top

_CITATION = """\
@ONLINE {wikidump,
    author = {Wikimedia Foundation},
    title  = {Wikimedia Downloads},
    url    = {https://dumps.wikimedia.org}
}
"""

_DESCRIPTION = """\
Wikipedia dataset containing cleaned articles of all languages.
The datasets are built from the Wikipedia dump
(https://dumps.wikimedia.org/) with one split per language. Each example
contains the content of one full Wikipedia article with cleaning to strip
markdown and unwanted sections (references, etc.).
"""

_LICENSE = (
    "This work is licensed under the Creative Commons Attribution-ShareAlike "
    "3.0 Unported License. To view a copy of this license, visit "
    "http://creativecommons.org/licenses/by-sa/3.0/ or send a letter to "
    "Creative Commons, PO Box 1866, Mountain View, CA 94042, USA."
)

# Source: https://en.wikipedia.org/wiki/List_of_Wikipedias (accessed 3/1/2019)
# Removed because no articles: hz.
WIKIPEDIA_LANGUAGES = [
    "aa",
    "ab",
    "ace",
    "ady",
    "af",
    "ak",
    "als",
    "am",
    "an",
    "ang",
    "ar",
    "arc",
    "arz",
    "as",
    "ast",
    "atj",
    "av",
    "ay",
    "az",
    "azb",
    "ba",
    "bar",
    "bat-smg",
    "bcl",
    "be",
    "be-x-old",
    "bg",
    "bh",
    "bi",
    "bjn",
    "bm",
    "bn",
    "bo",
    "bpy",
    "br",
    "bs",
    "bug",
    "bxr",
    "ca",
    "cbk-zam",
    "cdo",
    "ce",
    "ceb",
    "ch",
    "cho",
    "chr",
    "chy",
    "ckb",
    "co",
    "cr",
    "crh",
    "cs",
    "csb",
    "cu",
    "cv",
    "cy",
    "da",
    "de",
    "din",
    "diq",
    "dsb",
    "dty",
    "dv",
    "dz",
    "ee",
    "el",
    "eml",
    "en",
    "eo",
    "es",
    "et",
    "eu",
    "ext",
    "fa",
    "ff",
    "fi",
    "fiu-vro",
    "fj",
    "fo",
    "fr",
    "frp",
    "frr",
    "fur",
    "fy",
    "ga",
    "gag",
    "gan",
    "gd",
    "gl",
    "glk",
    "gn",
    "gom",
    "gor",
    "got",
    "gu",
    "gv",
    "ha",
    "hak",
    "haw",
    "he",
    "hi",
    "hif",
    "ho",
    "hr",
    "hsb",
    "ht",
    "hu",
    "hy",
    "ia",
    "id",
    "ie",
    "ig",
    "ii",
    "ik",
    "ilo",
    "inh",
    "io",
    "is",
    "it",
    "iu",
    "ja",
    "jam",
    "jbo",
    "jv",
    "ka",
    "kaa",
    "kab",
    "kbd",
    "kbp",
    "kg",
    "ki",
    "kj",
    "kk",
    "kl",
    "km",
    "kn",
    "ko",
    "koi",
    "krc",
    "ks",
    "ksh",
    "ku",
    "kv",
    "kw",
    "ky",
    "la",
    "lad",
    "lb",
    "lbe",
    "lez",
    "lfn",
    "lg",
    "li",
    "lij",
    "lmo",
    "ln",
    "lo",
    "lrc",
    "lt",
    "ltg",
    "lv",
    "mai",
    "map-bms",
    "mdf",
    "mg",
    "mh",
    "mhr",
    "mi",
    "min",
    "mk",
    "ml",
    "mn",
    "mr",
    "mrj",
    "ms",
    "mt",
    "mus",
    "mwl",
    "my",
    "myv",
    "mzn",
    "na",
    "nah",
    "nap",
    "nds",
    "nds-nl",
    "ne",
    "new",
    "ng",
    "nl",
    "nn",
    "no",
    "nov",
    "nrm",
    "nso",
    "nv",
    "ny",
    "oc",
    "olo",
    "om",
    "or",
    "os",
    "pa",
    "pag",
    "pam",
    "pap",
    "pcd",
    "pdc",
    "pfl",
    "pi",
    "pih",
    "pl",
    "pms",
    "pnb",
    "pnt",
    "ps",
    "pt",
    "qu",
    "rm",
    "rmy",
    "rn",
    "ro",
    "roa-rup",
    "roa-tara",
    "ru",
    "rue",
    "rw",
    "sa",
    "sah",
    "sat",
    "sc",
    "scn",
    "sco",
    "sd",
    "se",
    "sg",
    "sh",
    "si",
    "simple",
    "sk",
    "sl",
    "sm",
    "sn",
    "so",
    "sq",
    "sr",
    "srn",
    "ss",
    "st",
    "stq",
    "su",
    "sv",
    "sw",
    "szl",
    "ta",
    "tcy",
    "te",
    "tet",
    "tg",
    "th",
    "ti",
    "tk",
    "tl",
    "tn",
    "to",
    "tpi",
    "tr",
    "ts",
    "tt",
    "tum",
    "tw",
    "ty",
    "tyv",
    "udm",
    "ug",
    "uk",
    "ur",
    "uz",
    "ve",
    "vec",
    "vep",
    "vi",
    "vls",
    "vo",
    "wa",
    "war",
    "wo",
    "wuu",
    "xal",
    "xh",
    "xmf",
    "yi",
    "yo",
    "za",
    "zea",
    "zh",
    "zh-classical",
    "zh-min-nan",
    "zh-yue",
    "zu",
]

_BASE_URL_TMPL = "https://dumps.wikimedia.org/{lang}wiki/{date}/"
_INFO_FILE = "dumpstatus.json"


class WikipediaConfig(datasets.BuilderConfig):
    """BuilderConfig for Wikipedia."""

    def __init__(self, language=None, date=None, **kwargs):
        """BuilderConfig for Wikipedia.

        Args:
          language: string, the language code for the Wikipedia dump to use.
          date: string, date of the Wikipedia dump in YYYYMMDD format. A list of
            available dates can be found at https://dumps.wikimedia.org/enwiki/.
          **kwargs: keyword arguments forwarded to super.
        """
        super(WikipediaConfig, self).__init__(
            name="{0}.{1}".format(date, language),
            description="Wikipedia dataset for {0}, parsed from {1} dump.".format(language, date),
            **kwargs,
        )
        self.date = date
        self.language = language


_VERSION = datasets.Version("1.0.0", "")


class Wikipedia(datasets.BeamBasedBuilder):
    """Wikipedia dataset."""

    # Use mirror (your.org) to avoid download caps.
    BUILDER_CONFIG_CLASS = WikipediaConfig
    BUILDER_CONFIGS = [
        WikipediaConfig(
            version=_VERSION,
            language=lang,
            date="20200501",
        )  # pylint:disable=g-complex-comprehension
        for lang in WIKIPEDIA_LANGUAGES
    ]

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features({"title": datasets.Value("string"), "text": datasets.Value("string")}),
            # No default supervised_keys.
            supervised_keys=None,
            homepage="https://dumps.wikimedia.org",
            citation=_CITATION,
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
            datasets.SplitGenerator(  # pylint:disable=g-complex-comprehension
                name=datasets.Split.TRAIN, gen_kwargs={"filepaths": downloaded_files["xml"], "language": lang}
            )
        ]

    def _build_pcollection(self, pipeline, filepaths, language):
        """Build PCollection of examples in the raw (text) form."""
        import apache_beam as beam
        import mwparserfromhell

        def _extract_content(filepath):
            """Extracts article content from a single WikiMedia XML file."""
            logging.info("generating examples from = %s", filepath)
            with beam.io.filesystems.FileSystems.open(filepath) as f:
                f = bz2.BZ2File(filename=f)
                if six.PY3:
                    # Workaround due to:
                    # https://github.com/tensorflow/tensorflow/issues/33563
                    utf_f = codecs.getreader("utf-8")(f)
                else:
                    utf_f = f

                # To clear root, to free-up more memory than just `elem.clear()`.
                context = etree.iterparse(utf_f, events=("end",))
                context = iter(context)
                unused_event, root = next(context)
                for unused_event, elem in context:
                    if not elem.tag.endswith("page"):
                        continue
                    namespace = elem.tag[:-4]
                    title = elem.find("./{0}title".format(namespace)).text
                    ns = elem.find("./{0}ns".format(namespace)).text
                    id_ = elem.find("./{0}id".format(namespace)).text

                    # Filter pages that are not in the "main" namespace.
                    if ns != "0":
                        root.clear()
                        continue

                    raw_content = elem.find("./{0}revision/{0}text".format(namespace)).text
                    root.clear()

                    # Filter redirects.
                    if raw_content is None or raw_content.lower().startswith("#redirect"):
                        beam.metrics.Metrics.counter(language, "filtered-redirects").inc()
                        continue

                    beam.metrics.Metrics.counter(language, "extracted-examples").inc()
                    yield (id_, title, raw_content)

        def _clean_content(inputs):
            """Cleans raw wikicode to extract text."""
            id_, title, raw_content = inputs
            try:
                text = _parse_and_clean_wikicode(raw_content, parser=mwparserfromhell)
            except (mwparserfromhell.parser.ParserError) as e:
                beam.metrics.Metrics.counter(language, "parser-error").inc()
                logging.error("mwparserfromhell ParseError: %s", e)
                return

            if not text:
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
    """Strips formatting and unwanted sections from raw page content."""
    wikicode = parser.parse(raw_content)

    # Filters for references, tables, and file/image links.
    re_rm_wikilink = re.compile("^(?:File|Image|Media):", flags=re.IGNORECASE | re.UNICODE)

    def rm_wikilink(obj):
        return bool(re_rm_wikilink.match(six.text_type(obj.title)))

    def rm_tag(obj):
        return six.text_type(obj.tag) in {"ref", "table"}

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
