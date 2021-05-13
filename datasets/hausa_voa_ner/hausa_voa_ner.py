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

"""Introduction to the Yoruba GV NER dataset: A Yoruba Global Voices (News) Named Entity Recognition Dataset"""


import datasets


logger = datasets.logging.get_logger(__name__)


# TODO: Add BibTeX citation
# Find for instance the citation on arxiv or on the dataset repo/website
_CITATION = """\
@inproceedings{hedderich-etal-2020-transfer,
    title = "Transfer Learning and Distant Supervision for Multilingual Transformer Models: A Study on {A}frican Languages",
    author = "Hedderich, Michael A.  and
      Adelani, David  and
      Zhu, Dawei  and
      Alabi, Jesujoba  and
      Markus, Udia  and
      Klakow, Dietrich",
    booktitle = "Proceedings of the 2020 Conference on Empirical Methods in Natural Language Processing (EMNLP)",
    month = nov,
    year = "2020",
    address = "Online",
    publisher = "Association for Computational Linguistics",
    url = "https://www.aclweb.org/anthology/2020.emnlp-main.204",
    doi = "10.18653/v1/2020.emnlp-main.204",
    pages = "2580--2591",
}
"""

# TODO: Add description of the dataset here
# You can copy an official description
_DESCRIPTION = """\
The Hausa VOA NER dataset is a labeled dataset for named entity recognition in Hausa. The texts were obtained from
Hausa Voice of America News articles https://www.voahausa.com/ . We concentrate on
four types of named entities: persons [PER], locations [LOC], organizations [ORG], and dates & time [DATE].

The Hausa VOA NER data files contain 2 columns separated by a tab ('\t'). Each word has been put on a separate line and
there is an empty line after each sentences i.e the CoNLL format. The first item on each line is a word, the second
is the named entity tag. The named entity tags have the format I-TYPE which means that the word is inside a phrase
of type TYPE. For every multi-word expression like 'New York', the first word gets a tag B-TYPE and the subsequent words
have tags I-TYPE, a word with tag O is not part of a phrase. The dataset is in the BIO tagging scheme.

For more details, see https://www.aclweb.org/anthology/2020.emnlp-main.204/
"""

_URL = "https://github.com/uds-lsv/transfer-distant-transformer-african/raw/master/data/hausa_ner/"
_TRAINING_FILE = "train_clean.tsv"
_DEV_FILE = "dev.tsv"
_TEST_FILE = "test.tsv"


class HausaVoaNerConfig(datasets.BuilderConfig):
    """BuilderConfig for HausaVoaNer"""

    def __init__(self, **kwargs):
        """BuilderConfig for HausaVoaNer.
        Args:
          **kwargs: keyword arguments forwarded to super.
        """
        super(HausaVoaNerConfig, self).__init__(**kwargs)


class HausaVoaNer(datasets.GeneratorBasedBuilder):
    """Hausa VOA NER dataset."""

    BUILDER_CONFIGS = [
        HausaVoaNerConfig(
            name="hausa_voa_ner", version=datasets.Version("1.0.0"), description="Hausa VOA NER dataset"
        ),
    ]

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "id": datasets.Value("string"),
                    "tokens": datasets.Sequence(datasets.Value("string")),
                    "ner_tags": datasets.Sequence(
                        datasets.features.ClassLabel(
                            names=[
                                "O",
                                "B-PER",
                                "I-PER",
                                "B-ORG",
                                "I-ORG",
                                "B-LOC",
                                "I-LOC",
                                "B-DATE",
                                "I-DATE",
                            ]
                        )
                    ),
                }
            ),
            supervised_keys=None,
            homepage="https://www.aclweb.org/anthology/2020.emnlp-main.204/",
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        urls_to_download = {
            "train": f"{_URL}{_TRAINING_FILE}",
            "dev": f"{_URL}{_DEV_FILE}",
            "test": f"{_URL}{_TEST_FILE}",
        }
        downloaded_files = dl_manager.download_and_extract(urls_to_download)

        return [
            datasets.SplitGenerator(name=datasets.Split.TRAIN, gen_kwargs={"filepath": downloaded_files["train"]}),
            datasets.SplitGenerator(name=datasets.Split.VALIDATION, gen_kwargs={"filepath": downloaded_files["dev"]}),
            datasets.SplitGenerator(name=datasets.Split.TEST, gen_kwargs={"filepath": downloaded_files["test"]}),
        ]

    def _generate_examples(self, filepath):
        logger.info("⏳ Generating examples from = %s", filepath)
        with open(filepath, encoding="utf-8") as f:
            guid = 0
            tokens = []
            ner_tags = []
            for line in f:
                line = line.strip()
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
                    # yoruba_gv_ner tokens are tab separated
                    splits = line.strip().split("\t")
                    tokens.append(splits[0])
                    ner_tags.append(splits[1].rstrip())
            # last example
            yield guid, {
                "id": str(guid),
                "tokens": tokens,
                "ner_tags": ner_tags,
            }
