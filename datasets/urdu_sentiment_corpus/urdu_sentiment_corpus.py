"""Urdu Sentiment Corpus"""


import os

import datasets


_CITATION = """
@inproceedings{khan2020usc,
  title={Urdu Sentiment Corpus (v1.0): Linguistic Exploration and Visualization of Labeled Datasetfor Urdu Sentiment Analysis.},
  author={Khan, Muhammad Yaseen and Nizami, Muhammad Suffian},
  booktitle={2020 IEEE 2nd International Conference On Information Science & Communication Technology (ICISCT)},
  pages={},
  year={2020},
  organization={IEEE}
}
"""

_DESCRIPTION = """
“Urdu Sentiment Corpus” (USC) shares the dat of Urdu tweets for the sentiment analysis and polarity detection.
The dataset is consisting of tweets and overall, the dataset is comprising over 17, 185 tokens
with 52% records as positive, and 48 % records as negative.
"""

_URL = "https://github.com/MuhammadYaseenKhan/Urdu-Sentiment-Corpus/archive/master.zip"


class UrduSentimentCorpus(datasets.GeneratorBasedBuilder):
    VERSION = datasets.Version("1.0.0")

    labels_dic = {
        "P": 0,
        "N": 1,
        "O": 2,
    }

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "sentence": datasets.Value("string"),
                    "sentiment": datasets.ClassLabel(names=list(self.labels_dic.keys())),
                }
            ),
            homepage="https://github.com/MuhammadYaseenKhan/Urdu-Sentiment-Corpus",
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        dl_path = dl_manager.download_and_extract(_URL)
        dl_dir = os.path.join(dl_path, "Urdu-Sentiment-Corpus-master", "urdu-sentiment-corpus-v1.tsv")

        # This dataset has no train test split
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={"filepath": os.path.join(dl_dir)},
            ),
        ]

    def _generate_examples(self, filepath=None):
        """Yields examples."""
        with open(filepath, encoding="utf-8") as f:
            next(f)
            for id_, row in enumerate(f):
                row = row.strip().split("\t")
                if len(row) != 2:
                    continue
                row[1] = self.labels_dic[row[1]]

                yield id_, {"sentence": row[0][::-1], "sentiment": row[1]}
