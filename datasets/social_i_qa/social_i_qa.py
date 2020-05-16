"""TODO(social_i_qa): Add a description here."""

from __future__ import absolute_import, division, print_function

import json
import os

import nlp


# TODO(social_i_qa): BibTeX citation
_CITATION = """
"""

# TODO(social_i_qa):
_DESCRIPTION = """\
We introduce Social IQa: Social Interaction QA, a new question-answering benchmark for testing social commonsense intelligence. Contrary to many prior benchmarks that focus on physical or taxonomic knowledge, Social IQa focuses on reasoning about people’s actions and their social implications. For example, given an action like "Jesse saw a concert" and a question like "Why did Jesse do this?", humans can easily infer that Jesse wanted "to see their favorite performer" or "to enjoy the music", and not "to see what's happening inside" or "to see if it works". The actions in Social IQa span a wide variety of social situations, and answer candidates contain both human-curated answers and adversarially-filtered machine-generated candidates. Social IQa contains over 37,000 QA pairs for evaluating models’ abilities to reason about the social implications of everyday events and situations. (Less)
"""
_URL = "https://storage.googleapis.com/ai2-mosaic/public/socialiqa/socialiqa-train-dev.zip"


class SocialIQa(nlp.GeneratorBasedBuilder):
    """TODO(social_i_qa): Short description of my dataset."""

    # TODO(social_i_qa): Set up version.
    VERSION = nlp.Version("0.1.0")

    def _info(self):
        # TODO(social_i_qa): Specifies the nlp.DatasetInfo object
        return nlp.DatasetInfo(
            # This is the description that will appear on the datasets page.
            description=_DESCRIPTION,
            # nlp.features.FeatureConnectors
            features=nlp.Features(
                {
                    # These are the features of your dataset like images, labels ...
                    "context": nlp.Value("string"),
                    "question": nlp.Value("string"),
                    "answerA": nlp.Value("string"),
                    "answerB": nlp.Value("string"),
                    "answerC": nlp.Value("string"),
                    "label": nlp.Value("string"),
                }
            ),
            # If there's a common (input, target) tuple from the features,
            # specify them here. They'll be used if as_supervised=True in
            # builder.as_dataset.
            supervised_keys=None,
            # Homepage of the dataset for documentation
            homepage="https://leaderboard.allenai.org/socialiqa/submissions/get-started",
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        # TODO(social_i_qa): Downloads the data and defines the splits
        # dl_manager is a nlp.download.DownloadManager that can be used to
        # download and extract URLs
        dl_dir = dl_manager.download_and_extract(_URL)
        dl_dir = os.path.join(dl_dir, "socialiqa-train-dev")
        return [
            nlp.SplitGenerator(
                name=nlp.Split.TRAIN,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "filepath": os.path.join(dl_dir, "train.jsonl"),
                    "labelpath": os.path.join(dl_dir, "train-labels.lst"),
                },
            ),
            nlp.SplitGenerator(
                name=nlp.Split.VALIDATION,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "filepath": os.path.join(dl_dir, "dev.jsonl"),
                    "labelpath": os.path.join(dl_dir, "dev-labels.lst"),
                },
            ),
        ]

    def _generate_examples(self, filepath, labelpath):
        """Yields examples."""
        # TODO(social_i_qa): Yields (key, example) tuples from the dataset
        with open(labelpath) as f:
            labels = [label for label in f]
        with open(filepath) as f1:
            for id_, row in enumerate(f1):
                data = json.loads(row)
                label = labels[id_]
                context = data["context"]
                answerA = data["answerA"]
                answerB = data["answerB"]
                answerC = data["answerC"]
                question = data["question"]
                yield id_, {
                    "context": context,
                    "question": question,
                    "answerA": answerA,
                    "answerB": answerB,
                    "answerC": answerC,
                    "label": label,
                }
