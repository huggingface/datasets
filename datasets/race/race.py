"""TODO(race): Add a description here."""

from __future__ import absolute_import, division, print_function

import json
import os
from pathlib import Path

import datasets


_CITATION = """\
@article{lai2017large,
    title={RACE: Large-scale ReAding Comprehension Dataset From Examinations},
    author={Lai, Guokun and Xie, Qizhe and Liu, Hanxiao and Yang, Yiming and Hovy, Eduard},
    journal={arXiv preprint arXiv:1704.04683},
    year={2017}
}
"""

_DESCRIPTION = """\
Race is a large-scale reading comprehension dataset with more than 28,000 passages and nearly 100,000 questions. The
 dataset is collected from English examinations in China, which are designed for middle school and high school students.
The dataset can be served as the training and test sets for machine comprehension.

"""

_URL = "http://www.cs.cmu.edu/~glai1/data/race/RACE.tar.gz"


class Race(datasets.GeneratorBasedBuilder):
    """ReAding Comprehension Dataset From Examination dataset from CMU"""

    VERSION = datasets.Version("0.1.0")

    BUILDER_CONFIGS = [
        datasets.BuilderConfig(name="high", description="Exams designed for high school students", version=VERSION),
        datasets.BuilderConfig(
            name="middle", description="Exams designed for middle school students", version=VERSION
        ),
        datasets.BuilderConfig(
            name="all", description="Exams designed for both high school and middle school students", version=VERSION
        ),
    ]

    def _info(self):
        return datasets.DatasetInfo(
            # This is the description that will appear on the datasets page.
            description=_DESCRIPTION,
            # datasets.features.FeatureConnectors
            features=datasets.Features(
                {
                    "example_id": datasets.Value("string"),
                    "article": datasets.Value("string"),
                    "answer": datasets.Value("string"),
                    "question": datasets.Value("string"),
                    "options": datasets.features.Sequence(datasets.Value("string"))
                    # These are the features of your dataset like images, labels ...
                }
            ),
            # If there's a common (input, target) tuple from the features,
            # specify them here. They'll be used if as_supervised=True in
            # builder.as_dataset.
            supervised_keys=None,
            # Homepage of the dataset for documentation
            homepage="http://www.cs.cmu.edu/~glai1/data/race/",
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        # Downloads the data and defines the splits
        # dl_manager is a datasets.download.DownloadManager that can be used to
        dl_dir = dl_manager.download_and_extract(_URL)
        case = str(self.config.name)
        if case == "all":
            case = ""
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={"train_test_or_eval": os.path.join(dl_dir, f"RACE/test/{case}")},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={"train_test_or_eval": os.path.join(dl_dir, f"RACE/train/{case}")},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={"train_test_or_eval": os.path.join(dl_dir, f"RACE/dev/{case}")},
            ),
        ]

    def _generate_examples(self, train_test_or_eval):
        """Yields examples."""
        current_path = Path(train_test_or_eval)
        files_in_dir = [str(f.absolute()) for f in sorted(current_path.glob("**/*.txt"))]
        for file in sorted(files_in_dir):
            with open(file, encoding="utf-8") as f:
                data = json.load(f)
                questions = data["questions"]
                answers = data["answers"]
                options = data["options"]
                for i in range(len(questions)):
                    question = questions[i]
                    answer = answers[i]
                    option = options[i]
                    yield i, {
                        "example_id": data["id"],
                        "article": data["article"],
                        "question": question,
                        "answer": answer,
                        "options": option,
                    }
