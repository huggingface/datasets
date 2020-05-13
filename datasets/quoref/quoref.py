"""TODO(quoref): Add a description here."""

from __future__ import absolute_import, division, print_function

import json
import os

import nlp


# TODO(quoref): BibTeX citation
_CITATION = """\
@article{allenai:quoref,
      author    = {Pradeep Dasigi and Nelson F. Liu and Ana Marasovic and Noah A. Smith and  Matt Gardner},
      title     = {Quoref: A Reading Comprehension Dataset with Questions Requiring Coreferential Reasoning},
      journal   = {arXiv:1908.05803v2 },
      year      = {2019},
}
"""

# TODO(quoref):
_DESCRIPTION = """\
Quoref is a QA dataset which tests the coreferential reasoning capability of reading comprehension systems. In this 
span-selection benchmark containing 24K questions over 4.7K paragraphs from Wikipedia, a system must resolve hard 
coreferences before selecting the appropriate span(s) in the paragraphs for answering questions.
"""

_URL = "https://quoref-dataset.s3-us-west-2.amazonaws.com/train_and_dev/quoref-train-dev-v0.1.zip"


class Quoref(nlp.GeneratorBasedBuilder):
    """TODO(quoref): Short description of my dataset."""

    # TODO(quoref): Set up version.
    VERSION = nlp.Version("0.1.0")

    def _info(self):
        # TODO(quoref): Specifies the nlp.DatasetInfo object
        return nlp.DatasetInfo(
            # This is the description that will appear on the datasets page.
            description=_DESCRIPTION,
            # nlp.features.FeatureConnectors
            features=nlp.Features(
                {
                    "id": nlp.Value("string"),
                    "question": nlp.Value("string"),
                    "context": nlp.Value("string"),
                    "title": nlp.Value("string"),
                    "url": nlp.Value("string"),
                    "answers": nlp.features.Sequence(
                        {"answer_start": nlp.Value("int32"), "text": nlp.Value("string"),}
                    )
                    # These are the features of your dataset like images, labels ...
                }
            ),
            # If there's a common (input, target) tuple from the features,
            # specify them here. They'll be used if as_supervised=True in
            # builder.as_dataset.
            supervised_keys=None,
            # Homepage of the dataset for documentation
            homepage="https://leaderboard.allenai.org/quoref/submissions/get-started",
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        # TODO(quoref): Downloads the data and defines the splits
        # dl_manager is a nlp.download.DownloadManager that can be used to
        # download and extract URLs
        dl_dir = dl_manager.download_and_extract(_URL)
        data_dir = os.path.join(dl_dir, "quoref-train-dev-v0.1")
        return [
            nlp.SplitGenerator(
                name=nlp.Split.TRAIN,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={"filepath": os.path.join(data_dir, "quoref-train-v0.1.json")},
            ),
            nlp.SplitGenerator(
                name=nlp.Split.VALIDATION,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={"filepath": os.path.join(data_dir, "quoref-dev-v0.1.json")},
            ),
        ]

    def _generate_examples(self, filepath):
        """Yields examples."""
        # TODO(quoref): Yields (key, example) tuples from the dataset
        with open(filepath) as f:
            data = json.load(f)
            for article in data["data"]:
                title = article.get("title", "").strip()
                url = article.get("url", "").strip()
                for paragraph in article["paragraphs"]:
                    context = paragraph["context"].strip()
                    for qa in paragraph["qas"]:
                        question = qa["question"].strip()
                        id_ = qa["id"]

                        answer_starts = [answer["answer_start"] for answer in qa["answers"]]
                        answers = [answer["text"].strip() for answer in qa["answers"]]

                        # Features currently used are "context", "question", and "answers".
                        # Others are extracted here for the ease of future expansions.
                        yield id_, {
                            "title": title,
                            "context": context,
                            "question": question,
                            "id": id_,
                            "answers": {"answer_start": answer_starts, "text": answers,},
                            "url": url,
                        }
