from __future__ import absolute_import, division, print_function

import csv
import os

import nlp


_CITATION = """\
@article{go2009twitter,
  title={Twitter sentiment classification using distant supervision},
  author={Go, Alec and Bhayani, Richa and Huang, Lei},
  journal={CS224N project report, Stanford},
  volume={1},
  number={12},
  pages={2009},
  year={2009}
}
"""

_DESCRIPTION = """\
Sentiment140 consists of Twitter messages with emoticons, which are used as noisy labels for
sentiment classification. For more detailed information please refer to the paper.
"""
_URL = "http://help.sentiment140.com/home"
_DATA_URL = "http://cs.stanford.edu/people/alecmgo/trainingandtestdata.zip"

_TEST_FILE_NAME = "testdata.manual.2009.06.14.csv"
_TRAIN_FILE_NAME = "training.1600000.processed.noemoticon.csv"


class Sentiment140Config(nlp.BuilderConfig):

    """BuilderConfig for Break"""

    def __init__(self, data_url, **kwargs):
        """BuilderConfig for BlogAuthorship

        Args:
          data_url: `string`, url to the dataset (word or raw level)
          **kwargs: keyword arguments forwarded to super.
        """
        super(Sentiment140Config, self).__init__(
            version=nlp.Version("1.0.0", "New split API (https://tensorflow.org/datasets/splits)"), **kwargs
        )
        self.data_url = data_url


class Sentiment140(nlp.GeneratorBasedBuilder):

    VERSION = nlp.Version("0.1.0")
    BUILDER_CONFIGS = [
        Sentiment140Config(
            name="sentiment140",
            data_url=_DATA_URL,
            description="sentiment classification dataset. Twitter messages are classified as either 'positive'=0, 'neutral'=1 or 'negative'=2.",
        )
    ]

    def _info(self):
        return nlp.DatasetInfo(
            # This is the description that will appear on the datasets page.
            description=_DESCRIPTION,
            # nlp.features.FeatureConnectors
            features=nlp.Features(
                {
                    "text": nlp.Value("string"),
                    "date": nlp.Value("string"),
                    "user": nlp.Value("string"),
                    "sentiment": nlp.Value("int32"),
                    "query": nlp.Value("string"),
                }
            ),
            # If there's a common (input, target) tuple from the features,
            # specify them here. They'll be used if as_supervised=True in
            # builder.as_dataset.
            supervised_keys=None,
            # Homepage of the dataset for documentation
            homepage=_URL,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        data_dir = dl_manager.download_and_extract(_DATA_URL)

        test_csv_file = os.path.join(data_dir, _TEST_FILE_NAME)
        train_csv_file = os.path.join(data_dir, _TRAIN_FILE_NAME)

        if self.config.name == "sentiment140":
            return [
                nlp.SplitGenerator(
                    name=nlp.Split.TRAIN,
                    # These kwargs will be passed to _generate_examples
                    gen_kwargs={"file_path": train_csv_file},
                ),
                nlp.SplitGenerator(
                    name=nlp.Split.TEST,
                    # These kwargs will be passed to _generate_examples
                    gen_kwargs={"file_path": test_csv_file},
                ),
            ]
        else:
            raise NotImplementedError("{} does not exist".format(self.config.name))

    def _generate_examples(self, file_path):
        """Yields examples."""

        with open(file_path, encoding="ISO-8859-1") as f:
            data = csv.reader(f, delimiter=",", quotechar='"')
            for row_id, row in enumerate(data):
                sentiment, tweet_id, date, query, user_name, message = row
                yield "{}_{}".format(row_id, tweet_id), {
                    "text": message,
                    "date": date,
                    "user": user_name,
                    "sentiment": int(sentiment),
                    "query": query,
                }
