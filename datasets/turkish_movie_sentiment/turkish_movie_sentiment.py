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
# Lint as: python3
"""TurkishMovieSentiment: This dataset contains turkish movie reviews."""


import csv
import os

import datasets


logger = datasets.logging.get_logger(__name__)


_DESCRIPTION = """\
This data set is a dataset from kaggle consisting of Turkish movie reviews and scored between 0-5.
"""

_CITATION = ""
_LICENSE = "CC0: Public Domain"
_HOMEPAGE = "https://www.kaggle.com/mustfkeskin/turkish-movie-sentiment-analysis-dataset"
_FILENAME = "turkish_movie_sentiment_dataset.csv"


class TurkishMovieSentimentConfig(datasets.BuilderConfig):
    """BuilderConfig for TurkishMovieSentiment"""

    def __init__(self, **kwargs):
        """BuilderConfig for TurkishMovieSentiment.
        Args:
          **kwargs: keyword arguments forwarded to super.
        """
        super(TurkishMovieSentimentConfig, self).__init__(**kwargs)


class TurkishMovieSentiment(datasets.GeneratorBasedBuilder):
    """TurkishMovieSentiment: This dataset contains turkish movie reviews."""

    BUILDER_CONFIGS = [
        TurkishMovieSentimentConfig(
            name="turkishmoviesentiment",
            version=datasets.Version("1.0.0"),
            description="This dataset contains turkish movie reviews.",
        ),
    ]

    @property
    def manual_download_instructions(self):
        return """\
    You need to go to https://www.kaggle.com/mustfkeskin/turkish-movie-sentiment-analysis-dataset,
    and manually download the TurkishMovieSentiment. Once it is completed,
    a file named archive.zip will be appeared in your Downloads folder
    or whichever folder your browser chooses to save files to. You then have
    to unzip the file and move turkish_movie_sentiment_dataset.csv under <path/to/folder>.
    The <path/to/folder> can e.g. be "~/manual_data".
    TurkishMovieSentiment can then be loaded using the following command `datasets.load_dataset("turkishmoviesentiment", data_dir="<path/to/folder>")`.
    """

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "point": datasets.Value("float32"),
                    "comment": datasets.Value("string"),
                    "film_name": datasets.Value("string"),
                }
            ),
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
        path_to_manual_file = os.path.abspath(os.path.expanduser(dl_manager.manual_dir))
        if not os.path.exists(path_to_manual_file):
            raise FileNotFoundError(
                f"{path_to_manual_file} does not exist. Make sure you insert a manual dir via `datasets.load_dataset('turkishmoviesentiment', data_dir=...)` that includes a file name {_FILENAME}. Manual download instructions: {self.manual_download_instructions})"
            )
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN, gen_kwargs={"filepath": os.path.join(path_to_manual_file, _FILENAME)}
            )
        ]

    def _generate_examples(self, filepath):
        """Generate TurkishMovieSentiment examples."""
        logger.info("⏳ Generating examples from = %s", filepath)
        with open(filepath, encoding="utf-8") as f:
            rdr = csv.reader(f, delimiter=",")
            next(rdr)
            rownum = 0
            for row in rdr:
                rownum += 1
                yield rownum, {
                    "comment": row[0],
                    "film_name": row[1],
                    "point": row[2].replace(",", "."),  # convert string to floating point ([0-5])
                }
