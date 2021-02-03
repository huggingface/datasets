"""Turkish Product Reviews"""

from __future__ import absolute_import, division, print_function

import logging
import os

import datasets


_CITATION = ""

_DESCRIPTION = """
Turkish Product Reviews.
This repository contains 235.165 product reviews collected online. There are 220.284 positive, 14881 negative reviews.
"""

_URL = "https://github.com/fthbrmnby/turkish-text-data/raw/master/reviews.tar.gz"
_FILES_PATHS = ["reviews.pos", "reviews.neg"]

_HOMEPAGE = "https://github.com/fthbrmnby/turkish-text-data"


class TurkishProductReviews(datasets.GeneratorBasedBuilder):
    VERSION = datasets.Version("1.0.0")

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "sentence": datasets.Value("string"),
                    "sentiment": datasets.ClassLabel(names=["negative", "positive"]),
                }
            ),
            citation=_CITATION,
            homepage=_HOMEPAGE,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        dl_paths = dl_manager.download_and_extract(_URL)
        filenames = list(os.listdir(dl_paths))
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN, gen_kwargs={"filepath": dl_paths, "filenames": filenames}
            ),
        ]

    def _generate_examples(self, filepath, filenames):
        """Generate TurkishProductReviews examples."""
        logging.info("⏳ Generating examples from = %s", filepath)
        for f in sorted(filenames):
            filename, file_extension = os.path.splitext(f)
            label = "negative" if file_extension == "neg" else "positive"

            file_fullpath = os.path.join(filepath, f)
            with open(file_fullpath, encoding="utf-8") as f:
                for idx, line in enumerate(f):
                    line = line.strip()
                    yield idx, {
                        "sentence": line,
                        "sentiment": label,
                    }
