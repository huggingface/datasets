# coding=utf-8
# Copyright 2020 HuggingFace Datasets Authors.
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
"""Named Entity Recognition corpora for Dutch, French, German from Europeana Newspapers."""

import logging

import datasets


_CITATION = """\
@InProceedings{NEUDECKER16.110,
  author = {Clemens Neudecker},
  title = {An Open Corpus for Named Entity Recognition in Historic Newspapers},
  booktitle = {Proceedings of the Tenth International Conference on Language Resources and Evaluation (LREC 2016)},
  year = {2016},
  month = {may},
  date = {23-28},
  location = {Portorož, Slovenia},
  editor = {Nicoletta Calzolari (Conference Chair) and Khalid Choukri and Thierry Declerck and Sara Goggi and Marko Grobelnik and Bente Maegaard and Joseph Mariani and Helene Mazo and Asuncion Moreno and Jan Odijk and Stelios Piperidis},
  publisher = {European Language Resources Association (ELRA)},
  address = {Paris, France},
  isbn = {978-2-9517408-9-1},
  language = {english}
 }
"""

_DESCRIPTION = """\
The corpora comprise of files per data provider that are encoded in the IOB format (Ramshaw & Marcus, 1995). The IOB format is a simple text chunking format that divides texts into single tokens per line, and, separated by a whitespace, tags to mark named entities. The most commonly used categories for tags are PER (person), LOC (location) and ORG (organization). To mark named entities that span multiple tokens, the tags have a prefix of either B- (beginning of named entity) or I- (inside of named entity). O (outside of named entity) tags are used to mark tokens that are not a named entity.
"""

_URL = "https://raw.githubusercontent.com/EuropeanaNewspapers/ner-corpora/master/"
_FR_BNF = "enp_FR.bnf.bio/enp_FR.bnf.bio"
_NL_KB = "enp_NL.kb.bio/enp_NL.kb.bio"
_DE_SBB = "enp_DE.sbb.bio/enp_DE.sbb.bio"
_DE_ONB = "enp_DE.onb.bio/enp_DE.onb.bio"
_DE_LFT = "enp_DE.lft.bio/enp_DE.lft.bio"

_TAGS = [
    "O",
    "B-PER",
    "I-PER",
    "B-ORG",
    "I-ORG",
    "B-LOC",
    "I-LOC",
]


class EuroNewsConfig(datasets.BuilderConfig):
    """BuilderConfig for Europana Newspaper"""

    def __init__(self, **kwargs):
        """BuilderConfig for Europana Newspaper.

        Args:
          **kwargs: keyword arguments forwarded to super.
        """
        super(EuroNewsConfig, self).__init__(**kwargs)


class Euronews(datasets.GeneratorBasedBuilder):
    """Europana Newspaper dataset."""

    BUILDER_CONFIGS = [
        EuroNewsConfig(
            name="fr-bnf", version=datasets.Version("1.0.0"), description="National Library of France Dataset"
        ),
        EuroNewsConfig(
            name="nl-kb", version=datasets.Version("1.0.0"), description="National Library of the Netherlands Dataset"
        ),
        EuroNewsConfig(name="de-sbb", version=datasets.Version("1.0.0"), description="Berlin State Library Dataset"),
        EuroNewsConfig(
            name="de-onb", version=datasets.Version("1.0.0"), description="Austrian National Library Dataset"
        ),
        EuroNewsConfig(
            name="de-lft", version=datasets.Version("1.0.0"), description="Dr Friedrich Teßmann Library Dataset"
        ),
    ]

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "id": datasets.Value("string"),
                    "tokens": datasets.Sequence(datasets.Value("string")),
                    "ner_tags": datasets.Sequence(datasets.features.ClassLabel(names=_TAGS)),
                }
            ),
            supervised_keys=None,
            homepage="https://github.com/EuropeanaNewspapers/ner-corpora",
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        if self.config.name == "fr-bnf":
            url_to_download = _URL + _FR_BNF
        elif self.config.name == "nl-kb":
            url_to_download = _URL + _NL_KB
        elif self.config.name == "de-sbb":
            url_to_download = _URL + _DE_SBB
        elif self.config.name == "de-onb":
            url_to_download = _URL + _DE_ONB
        elif self.config.name == "de-lft":
            url_to_download = _URL + _DE_LFT

        downloaded_files = dl_manager.download_and_extract(url_to_download)

        return [
            datasets.SplitGenerator(name=datasets.Split.TRAIN, gen_kwargs={"filepath": downloaded_files}),
        ]

    def _generate_examples(self, filepath):
        logging.info("⏳ Generating examples from = %s", filepath)
        with open(filepath, encoding="utf-8") as f:
            guid = 0
            tokens = []
            ner_tags = []
            for line in f:
                splits = line.split()
                if len(splits) != 2:
                    continue
                if line == "" or line == "\n":
                    if tokens:
                        yield guid, {
                            "id": str(guid),
                            "tokens": tokens,
                            "ner_tags": ner_tags,
                        }
                        guid += 1
                        tokens = []
                        ner_tags = []
                else:
                    # Europana Newspaper tokens are space separated
                    tag = splits[1].rstrip().upper()
                    if tag not in _TAGS:
                        continue
                    tokens.append(splits[0])
                    ner_tags.append(tag)
            # last example
            yield guid, {
                "id": str(guid),
                "tokens": tokens,
                "ner_tags": ner_tags,
            }
