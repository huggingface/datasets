"""Mathematics Aptitude Test of Heuristics (MATH) dataset."""


import glob
import json
import os

import datasets


_CITATION = """\
@article{hendrycksmath2021,
  title={Measuring Mathematical Problem Solving With the MATH Dataset},
  author={Dan Hendrycks
    and Collin Burns
    and Saurav Kadavath
    and Akul Arora
    and Steven Basart
    and Eric Tang
    and Dawn Song
    and Jacob Steinhardt},
  journal={arXiv preprint arXiv:2103.03874},
  year={2021}
}
"""


_DESCRIPTION = """\
The Mathematics Aptitude Test of Heuristics (MATH) dataset consists of problems
from mathematics competitions, including the AMC 10, AMC 12, AIME, and more.
Each problem in MATH has a full step-by-step solution, which can be used to teach
models to generate answer derivations and explanations.
"""


_HOMEPAGE = "https://github.com/hendrycks/math"


_LICENSE = "https://github.com/hendrycks/math/blob/main/LICENSE"


_URL = "https://people.eecs.berkeley.edu/~hendrycks/MATH.tar"


class CompetitionMathDataset(datasets.GeneratorBasedBuilder):
    """Mathematics Aptitude Test of Heuristics (MATH) dataset."""

    VERSION = datasets.Version("1.0.0")

    def _info(self):
        features = datasets.Features(
            {
                "problem": datasets.Value("string"),
                "level": datasets.Value("string"),
                "type": datasets.Value("string"),
                "solution": datasets.Value("string"),
            }
        )
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=features,
            supervised_keys=None,
            homepage=_HOMEPAGE,
            license=_LICENSE,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        download_dir = dl_manager.download_and_extract(_URL)
        math_dir = os.path.join(download_dir, "MATH")
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={"math_dir": math_dir, "split": "train"},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                gen_kwargs={"math_dir": math_dir, "split": "test"},
            ),
        ]

    def _generate_examples(self, math_dir, split):
        """Yields examples as (key, example) tuples."""
        filepaths = glob.glob(os.path.join(math_dir, split, "*", "*"))
        for id_, filepath in enumerate(filepaths):
            with open(filepath, "rb") as fin:
                example = json.load(fin)
                yield id_, example
