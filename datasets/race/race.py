"""TODO(race): Add a description here."""

from __future__ import absolute_import, division, print_function

import json
import os

import nlp


# TODO(race): BibTeX citation
_CITATION = """\
@article{lai2017large,
    title={RACE: Large-scale ReAding Comprehension Dataset From Examinations},
    author={Lai, Guokun and Xie, Qizhe and Liu, Hanxiao and Yang, Yiming and Hovy, Eduard},
    journal={arXiv preprint arXiv:1704.04683},  
    year={2017}
}
"""

# TODO(race):
_DESCRIPTION = """\
Race is a large-scale reading comprehension dataset with more than 28,000 passages and nearly 100,000 questions. The
 dataset is collected from English examinations in China, which are designed for middle school and high school students.
The dataset can be served as the training and test sets for machine comprehension.

"""

_URL = "http://www.cs.cmu.edu/~glai1/data/race/RACE.tar.gz"


class Race(nlp.GeneratorBasedBuilder):
    """TODO(race): Short description of my dataset."""

    # TODO(race): Set up version.
    VERSION = nlp.Version("0.1.0")

    def _info(self):
        # TODO(race): Specifies the nlp.DatasetInfo object
        return nlp.DatasetInfo(
            # This is the description that will appear on the datasets page.
            description=_DESCRIPTION,
            # nlp.features.FeatureConnectors
            features=nlp.Features(
                {
                    "article": nlp.Value("string"),
                    "answer": nlp.Value("string"),
                    "question": nlp.Value("string"),
                    "options": nlp.features.Sequence({"option": nlp.Value("string")})
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
        # TODO(race): Downloads the data and defines the splits
        # dl_manager is a nlp.download.DownloadManager that can be used to
        # download and extract URLs
        dl_dir = dl_manager.download_and_extract(_URL)
        return [
            nlp.SplitGenerator(
                name=nlp.Split.TEST,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "files": os.listdir(os.path.join(dl_dir, "RACE/test/high")),
                    "filespath": os.path.join(dl_dir, "RACE/test/high"),
                },
            ),
            nlp.SplitGenerator(
                name=nlp.Split.TRAIN,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "files": os.listdir(os.path.join(dl_dir, "RACE/train/high")),
                    "filespath": os.path.join(dl_dir, "RACE/train/high"),
                },
            ),
            nlp.SplitGenerator(
                name=nlp.Split.VALIDATION,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "files": os.listdir(os.path.join(dl_dir, "RACE/dev/high")),
                    "filespath": os.path.join(dl_dir, "RACE/dev/high"),
                },
            ),
        ]

    def _generate_examples(self, files, filespath):
        """Yields examples."""
        # TODO(race): Yields (key, example) tuples from the dataset
        for file in files:
            filepath = os.path.join(filespath, file)
            with open(filepath) as f:
                data = json.load(f)
                questions = data["questions"]
                answers = data["answers"]
                options = data["options"]
                for i in range(len(questions)):
                    question = questions[i]
                    answer = answers[i]
                    option = options[i]
                    yield i, {
                        "article": data["article"],
                        "question": question,
                        "answer": answer,
                        "options": {"option": option},
                    }
