"""Turkish Product Reviews"""


import os

import datasets
from datasets.tasks import TextClassification


logger = datasets.logging.get_logger(__name__)


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
            task_templates=[TextClassification(text_column="sentence", label_column="sentiment")],
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        archive = dl_manager.download(_URL)
        return [
            datasets.SplitGenerator(name=datasets.Split.TRAIN, gen_kwargs={"files": dl_manager.iter_archive(archive)}),
        ]

    def _generate_examples(self, files):
        """Generate TurkishProductReviews examples."""
        for file_idx, (path, f) in enumerate(files):
            _, file_extension = os.path.splitext(path)
            label = "negative" if file_extension == ".neg" else "positive"
            for idx, line in enumerate(f):
                line = line.decode("utf-8").strip()
                yield f"{file_idx}_{idx}", {
                    "sentence": line,
                    "sentiment": label,
                }
