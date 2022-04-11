"""IMDB Urdu movie reviews dataset."""


import csv
import os

import datasets
from datasets.tasks import TextClassification


_CITATION = """
@InProceedings{maas-EtAl:2011:ACL-HLT2011,
  author    = {Maas, Andrew L. and Daly,nRaymond E. and Pham, Peter T. and Huang, Dan and Ng, Andrew Y...},
  title     = {Learning Word Vectors for Sentiment Analysis},
  month     = {June},
  year      = {2011},
  address   = {Portland, Oregon, USA},
  publisher = {Association for Computational Linguistics},
  pages     = {142--150},
  url       = {http://www.aclweb.org/anthology/P11-1015}
}
"""

_DESCRIPTION = """
Large Movie translated Urdu Reviews Dataset.
This is a dataset for binary sentiment classification containing substantially more data than previous
benchmark datasets. We provide a set of 40,000 highly polar movie reviews for training, and 10,000 for testing.
To increase the availability of sentiment analysis dataset for a low recourse language like Urdu,
we opted to use the already available IMDB Dataset. we have translated this dataset using google translator.
This is a binary classification dataset having two classes as positive and negative.
The reason behind using this dataset is high polarity for each class.
It contains 50k samples equally divided in two classes.
"""

_URL = "https://github.com/mirfan899/Urdu/blob/master/sentiment/imdb_urdu_reviews.csv.tar.gz?raw=true"

_HOMEPAGE = "https://github.com/mirfan899/Urdu"


class ImdbUrduReviews(datasets.GeneratorBasedBuilder):
    VERSION = datasets.Version("1.0.0")

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "sentence": datasets.Value("string"),
                    "sentiment": datasets.ClassLabel(names=["positive", "negative"]),
                }
            ),
            citation=_CITATION,
            homepage=_HOMEPAGE,
            task_templates=[TextClassification(text_column="sentence", label_column="sentiment")],
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        dl_path = dl_manager.download_and_extract(_URL)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN, gen_kwargs={"filepath": os.path.join(dl_path, "imdb_urdu_reviews.csv")}
            ),
        ]

    def _generate_examples(self, filepath):
        """Yields examples."""
        with open(filepath, encoding="utf-8") as f:
            reader = csv.reader(f, delimiter=",")
            for id_, row in enumerate(reader):
                if id_ == 0:
                    continue
                yield id_, {"sentiment": row[1], "sentence": row[0]}
