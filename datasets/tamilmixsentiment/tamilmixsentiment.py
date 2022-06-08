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
"""Code-Mixed Tamil-English Text for Sentiment Analysis"""


import csv

import datasets
from datasets.tasks import TextClassification


_CITATION = """\
@inproceedings{chakravarthi-etal-2020-corpus,
    title = "Corpus Creation for Sentiment Analysis in Code-Mixed {T}amil-{E}nglish Text",
    author = "Chakravarthi, Bharathi Raja  and
      Muralidaran, Vigneshwaran  and
      Priyadharshini, Ruba  and
      McCrae, John Philip",
    booktitle = "Proceedings of the 1st Joint Workshop on Spoken Language Technologies for Under-resourced languages (SLTU) and Collaboration and Computing for Under-Resourced Languages (CCURL)",
    month = may,
    year = "2020",
    address = "Marseille, France",
    publisher = "European Language Resources association",
    url = "https://www.aclweb.org/anthology/2020.sltu-1.28",
    pages = "202--210",
    abstract = "Understanding the sentiment of a comment from a video or an image is an essential task in many applications. Sentiment analysis of a text can be useful for various decision-making processes. One such application is to analyse the popular sentiments of videos on social media based on viewer comments. However, comments from social media do not follow strict rules of grammar, and they contain mixing of more than one language, often written in non-native scripts. Non-availability of annotated code-mixed data for a low-resourced language like Tamil also adds difficulty to this problem. To overcome this, we created a gold standard Tamil-English code-switched, sentiment-annotated corpus containing 15,744 comment posts from YouTube. In this paper, we describe the process of creating the corpus and assigning polarities. We present inter-annotator agreement and show the results of sentiment analysis trained on this corpus as a benchmark.",
    language = "English",
    ISBN = "979-10-95546-35-1",
}
"""

_DESCRIPTION = """\
The first gold standard Tamil-English code-switched, sentiment-annotated corpus containing 15,744 comment posts from YouTube. Train: 11,335 Validation: 1,260 and Test: 3,149.  This makes the largest general domain sentiment dataset for this relatively low-resource language with code-mixing phenomenon.  The dataset contains all the three types of code-mixed sentences - Inter-Sentential switch, Intra-Sentential switch and Tag switching. Most comments were written in Roman script with either Tamil grammar with English lexicon or English grammar with Tamil lexicon. Some comments were written in Tamil script with English expressions in between.
"""

_LICENSE = ""

_TRAIN_DOWNLOAD_URL = "https://drive.google.com/u/0/uc?id=1hDHeoFIfQzJec1NgZNXh3CTNbchiIvuG&export=download"
_VALIDATION_DOWNLOAD_URL = "https://drive.google.com/u/0/uc?id=1lyCxkDwZyvKLaF5NZhS3JE2ftMmHAKBT&export=download"
_TEST_DOWNLOAD_URL = (
    "https://docs.google.com/spreadsheets/d/1_6HJWkOuD76pQ6M_RVoP4FOsUK22zPl1IMpq1atLhl4/export?format=tsv"
)


class Tamilmixsentiment(datasets.GeneratorBasedBuilder):
    """Tamilmixsentiment sentiment analysis dataset."""

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "text": datasets.Value("string"),
                    "label": datasets.features.ClassLabel(
                        names=["Positive", "Negative", "Mixed_feelings", "unknown_state", "not-Tamil"]
                    ),
                }
            ),
            homepage="https://dravidian-codemix.github.io/2020/datasets.html",
            citation=_CITATION,
            task_templates=[TextClassification(text_column="text", label_column="label")],
        )

    def _split_generators(self, dl_manager):
        train_path = dl_manager.download_and_extract(_TRAIN_DOWNLOAD_URL)
        validation_path = dl_manager.download_and_extract(_VALIDATION_DOWNLOAD_URL)
        test_path = dl_manager.download_and_extract(_TEST_DOWNLOAD_URL)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={
                    "filepath": train_path,
                    "split": "train",
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                gen_kwargs={
                    "filepath": validation_path,
                    "split": "validation",
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                gen_kwargs={
                    "filepath": test_path,
                    "split": "test",
                },
            ),
        ]

    def _generate_examples(self, filepath, split):
        """Generate Tamilmixsentiment examples."""
        with open(filepath, encoding="utf-8") as csv_file:
            csv_reader = csv.reader(
                csv_file, quotechar='"', delimiter="\t", quoting=csv.QUOTE_ALL, skipinitialspace=True
            )
            # skip header
            next(csv_reader)

            for id_, row in enumerate(csv_reader):

                # test - has a first column indicating sentence number
                if split == "test":
                    idcol, text, label = row

                # train, validation
                else:
                    text, label = row

                yield id_, {"text": text, "label": label}
