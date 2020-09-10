"""TODO(jeopardy): Add a description here."""

from __future__ import absolute_import, division, print_function

import json

import datasets


# TODO(jeopardy): BibTeX citation
_CITATION = """
"""

# TODO(jeopardy):
_DESCRIPTION = """
Dataset containing 216,930 Jeopardy questions, answers and other data.

The json file is an unordered list of questions where each question has
'category' : the question category, e.g. "HISTORY"
'value' : integer $ value of the question as string, e.g. "200"
Note: This is "None" for Final Jeopardy! and Tiebreaker questions
'question' : text of question
Note: This sometimes contains hyperlinks and other things messy text such as when there's a picture or video question
'answer' : text of answer
'round' : one of "Jeopardy!","Double Jeopardy!","Final Jeopardy!" or "Tiebreaker"
Note: Tiebreaker questions do happen but they're very rare (like once every 20 years)
'show_number' : int of show number, e.g '4680'
'air_date' : string of the show air date in format YYYY-MM-DD
"""
_URL = "https://www.reddit.com/r/datasets/comments/1uyd0t/200000_jeopardy_questions_in_a_json_file/"
_DATA_URL = "http://skeeto.s3.amazonaws.com/share/JEOPARDY_QUESTIONS1.json.gz"
_DATA_FILE = "JEOPARDY_QUESTIONS1.json"


class Jeopardy(datasets.GeneratorBasedBuilder):
    """TODO(jeopardy): Short description of my dataset."""

    # TODO(jeopardy): Set up version.
    VERSION = datasets.Version("0.1.0")

    def _info(self):
        # TODO(jeopardy): Specifies the datasets.DatasetInfo object
        return datasets.DatasetInfo(
            # This is the description that will appear on the datasets page.
            description=_DESCRIPTION,
            # datasets.features.FeatureConnectors
            features=datasets.Features(
                {
                    "category": datasets.Value("string"),
                    "air_date": datasets.Value("string"),
                    "question": datasets.Value("string"),
                    "value": datasets.Value("int32"),
                    "answer": datasets.Value("string"),
                    "round": datasets.Value("string"),
                    "show_number": datasets.Value("int32"),
                    # These are the features of your dataset like images, labels ...
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
        # TODO(jeopardy): Downloads the data and defines the splits
        # dl_manager is a datasets.download.DownloadManager that can be used to
        # download and extract URLs
        filepath = dl_manager.download_and_extract(_DATA_URL)

        return [
            datasets.SplitGenerator(name=datasets.Split.TRAIN, gen_kwargs={"filepath": filepath}),
        ]

    def _generate_examples(self, filepath):
        """Yields examples."""
        # TODO(jeopardy): Yields (key, example) tuples from the dataset
        with open(filepath, encoding="utf-8") as f:
            data = json.load(f)
            for i, example in enumerate(data):
                category = example["category"]
                air_date = example["air_date"]
                question = example["question"]
                if example["value"] is None:
                    value = -1  # for Final Jeopardy! and Tiebreaker questions
                else:
                    value = int(example["value"][1:].replace(",", ""))
                answer = example["answer"]
                round = example["round"]
                show_number = int(example["show_number"])
                yield i, {
                    "category": category,
                    "air_date": air_date,
                    "question": question,
                    "value": value,
                    "answer": answer,
                    "round": round,
                    "category": category,
                    "show_number": show_number,
                }
