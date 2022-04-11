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
"""Polish Summaries Corpus: the corpus of Polish news summaries"""


import glob
import xml.etree.ElementTree as ET

import datasets


# TODO: Add BibTeX citation
# Find for instance the citation on arxiv or on the dataset repo/website
_CITATION = """\
@inproceedings{
    ogro:kop:14:lrec,
    author = "Ogrodniczuk, Maciej and Kopeć, Mateusz",
    pdf = "http://nlp.ipipan.waw.pl/Bib/ogro:kop:14:lrec.pdf",
    title = "The {P}olish {S}ummaries {C}orpus",
    pages = "3712--3715",
    crossref = "lrec:14"
}
@proceedings{
    lrec:14,
    editor = "Calzolari, Nicoletta and Choukri, Khalid and Declerck, Thierry and Loftsson, Hrafn and Maegaard, Bente and Mariani, Joseph and Moreno, Asuncion and Odijk, Jan and Piperidis, Stelios",
    isbn = "978-2-9517408-8-4",
    title = "Proceedings of the Ninth International {C}onference on {L}anguage {R}esources and {E}valuation, {LREC}~2014",
    url = "http://www.lrec-conf.org/proceedings/lrec2014/index.html",
    booktitle = "Proceedings of the Ninth International {C}onference on {L}anguage {R}esources and {E}valuation, {LREC}~2014",
    address = "Reykjavík, Iceland",
    key = "LREC",
    year = "2014",
    organization = "European Language Resources Association (ELRA)"
}
"""

# TODO: Add description of the dataset here
# You can copy an official description
_DESCRIPTION = """\
Polish Summaries Corpus: the corpus of Polish news summaries.
"""

# TODO: Add a link to an official homepage for the dataset here
_HOMEPAGE = "http://zil.ipipan.waw.pl/PolishSummariesCorpus"

# TODO: Add the licence for the dataset here if you can find it
_LICENSE = "CC BY v.3"

# TODO: Add link to the official dataset URLs here
# The HuggingFace dataset library don't host the datasets but only point to the original files
# This can be an arbitrary nested dict/list of URLs (see below in `_split_generators` method)
_URL = "http://zil.ipipan.waw.pl/PolishSummariesCorpus?action=AttachFile&do=get&target=PSC_1.0.zip"


# TODO: Name of the dataset usually match the script name with CamelCase instead of snake_case
class Polsum(datasets.GeneratorBasedBuilder):
    """Polish Summaries Corpus: the corpus of Polish news summaries."""

    VERSION = datasets.Version("1.1.0")

    def _info(self):
        features = datasets.Features(
            {
                "id": datasets.Value("string"),
                "date": datasets.Value("string"),
                "title": datasets.Value("string"),
                "section": datasets.Value("string"),
                "authors": datasets.Value("string"),
                "body": datasets.Value("string"),
                "summaries": datasets.features.Sequence(
                    {
                        "ratio": datasets.Value("int32"),
                        "type": datasets.Value("string"),
                        "author": datasets.Value("string"),
                        "body": datasets.Value("string"),
                        "spans": datasets.features.Sequence(
                            {
                                "start": datasets.Value("int32"),
                                "end": datasets.Value("int32"),
                                "span_text": datasets.Value("string"),
                            }
                        ),
                    }
                ),
            }
        )
        return datasets.DatasetInfo(
            # This is the description that will appear on the datasets page.
            description=_DESCRIPTION,
            # This defines the different columns of the dataset and their types
            features=features,  # Here we define them above because they are different between the two configurations
            # If there's a common (input, target) tuple from the features,
            # specify them here. They'll be used if as_supervised=True in
            # builder.as_dataset.
            supervised_keys=None,
            # Homepage of the dataset for documentation
            homepage=_HOMEPAGE,
            # License for the dataset if available
            license=_LICENSE,
            # Citation for the dataset
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        # dl_manager is a datasets.download.DownloadManager that can be used to download and extract URLs
        # It can accept any type or nested list/dict and will give back the same structure with the url replaced with path to local files.
        # By default the archives will be extracted and a path to a cached folder where they are extracted is returned instead of the archive
        data_dir = dl_manager.download_and_extract(_URL)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "filepaths": glob.glob(data_dir + "/*/*/*.xml"),
                },
            ),
        ]

    def _generate_examples(self, filepaths):
        """Yields examples."""
        # TODO: This method will receive as arguments the `gen_kwargs` defined in the previous `_split_generators` method.
        # It is in charge of opening the given file and yielding (key, example) tuples from the dataset
        # The key is not important, it's more here for legacy reason (legacy from tfds)

        for i, xml_path in enumerate(sorted(filepaths)):
            root = ET.parse(xml_path).getroot()
            text_id = root.get("id")
            date_tag = root.find("date")
            date = date_tag.text.strip()
            title_tag = root.find("title")
            title = title_tag.text.strip()
            section_tag = root.find("section")
            section = section_tag.text.strip()
            authors_tag = root.find("authors")
            authors = authors_tag.text.strip()
            body_tag = root.find("body")
            body = body_tag.text.strip()
            summaries_tag = root.find("summaries")
            summaries = []
            for summary_tag in summaries_tag.iterfind("summary"):
                sratio = int(summary_tag.get("ratio"))
                stype = summary_tag.get("type")
                sauthor = summary_tag.get("author")
                sbody_tag = summary_tag.find("body")
                sbody = sbody_tag.text.strip()
                spans_tag = summary_tag.find("spans")
                spans = []
                if spans_tag:
                    for span_tag in spans_tag.iterfind("span"):
                        start = int(span_tag.get("start"))
                        end = int(span_tag.get("end"))
                        span_text = span_tag.text.strip()
                        spans.append(
                            {
                                "start": start,
                                "end": end,
                                "span_text": span_text,
                            }
                        )
                summaries.append(
                    {
                        "ratio": sratio,
                        "type": stype,
                        "author": sauthor,
                        "body": sbody,
                        "spans": spans,
                    }
                )

            yield i, {
                "id": text_id,
                "date": date,
                "title": title,
                "section": section,
                "authors": authors,
                "body": body,
                "summaries": summaries,
            }
