"""TODO(coqa): Add a description here."""

from __future__ import absolute_import, division, print_function

import json

import datasets


# TODO(coqa): BibTeX citation
_CITATION = """\
@InProceedings{SivaAndAl:Coca,
       author = {Siva, Reddy and Danqi, Chen and  Christopher D., Manning},
        title = {WikiQA: A Challenge Dataset for Open-Domain Question Answering},
      journal = { arXiv},
         year = {2018},

}
"""

# TODO(coqa):
_DESCRIPTION = """\
CoQA: A Conversational Question Answering Challenge
"""

_TRAIN_DATA_URL = "https://datasets.stanford.edu/data/coqa/coqa-train-v1.0.json"
_DEV_DATA_URL = "https://datasets.stanford.edu/data/coqa/coqa-dev-v1.0.json"


class Coqa(datasets.GeneratorBasedBuilder):
    """TODO(coqa): Short description of my dataset."""

    # TODO(coqa): Set up version.
    VERSION = datasets.Version("1.0.0")

    def _info(self):
        # TODO(coqa): Specifies the datasets.DatasetInfo object
        return datasets.DatasetInfo(
            # This is the description that will appear on the datasets page.
            description=_DESCRIPTION,
            # datasets.features.FeatureConnectors
            features=datasets.Features(
                {
                    "source": datasets.Value("string"),
                    "story": datasets.Value("string"),
                    "questions": datasets.features.Sequence(datasets.Value("string")),
                    "answers": datasets.features.Sequence(
                        {
                            "input_text": datasets.Value("string"),
                            "answer_start": datasets.Value("int32"),
                            "answer_end": datasets.Value("int32"),
                        }
                    ),
                }
            ),
            # If there's a common (input, target) tuple from the features,
            # specify them here. They'll be used if as_supervised=True in
            # builder.as_dataset.
            supervised_keys=None,
            # Homepage of the dataset for documentation
            homepage="https://stanfordnlp.github.io/coqa/",
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        # TODO(coqa): Downloads the data and defines the splits
        # dl_manager is a datasets.download.DownloadManager that can be used to
        # download and extract URLs
        urls_to_download = {"train": _TRAIN_DATA_URL, "dev": _DEV_DATA_URL}
        downloaded_files = dl_manager.download_and_extract(urls_to_download)

        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN, gen_kwargs={"filepath": downloaded_files["train"], "split": "train"}
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION, gen_kwargs={"filepath": downloaded_files["dev"], "split": "validation"}
            ),
        ]

    def _generate_examples(self, filepath, split):
        """Yields examples."""
        # TODO(coqa): Yields (key, example) tuples from the dataset
        with open(filepath, encoding="utf-8") as f:
            data = json.load(f)
            for row in data["data"]:
                questions = [question["input_text"] for question in row["questions"]]
                story = row["story"]
                source = row["source"]
                answers_start = [answer["span_start"] for answer in row["answers"]]
                answers_end = [answer["span_end"] for answer in row["answers"]]
                answers = [answer["input_text"] for answer in row["answers"]]
                yield row["id"], {
                    "source": source,
                    "story": story,
                    "questions": questions,
                    "answers": {"input_text": answers, "answer_start": answers_start, "answer_end": answers_end},
                }
