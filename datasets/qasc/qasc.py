"""TODO(qasc): Add a description here."""

from __future__ import absolute_import, division, print_function

import json
import os

import datasets


# TODO(qasc): BibTeX citation
_CITATION = """\
@article{allenai:qasc,
      author    = {Tushar Khot and Peter Clark and Michal Guerquin and Peter Jansen and Ashish Sabharwal},
      title     = {QASC: A Dataset for Question Answering via Sentence Composition},
      journal   = {arXiv:1910.11473v2},
      year      = {2020},
}
"""

# TODO(qasc):
_DESCRIPTION = """
QASC is a question-answering dataset with a focus on sentence composition. It consists of 9,980 8-way multiple-choice
questions about grade school science (8,134 train, 926 dev, 920 test), and comes with a corpus of 17M sentences.
"""
_URl = "http://data.allenai.org/downloads/qasc/qasc_dataset.tar.gz"


class Qasc(datasets.GeneratorBasedBuilder):
    """TODO(qasc): Short description of my dataset."""

    # TODO(qasc): Set up version.
    VERSION = datasets.Version("0.1.0")

    def _info(self):
        # TODO(qasc): Specifies the datasets.DatasetInfo object
        return datasets.DatasetInfo(
            # This is the description that will appear on the datasets page.
            description=_DESCRIPTION,
            # datasets.features.FeatureConnectors
            features=datasets.Features(
                {
                    "id": datasets.Value("string"),
                    "question": datasets.Value("string"),
                    "choices": datasets.features.Sequence(
                        {"text": datasets.Value("string"), "label": datasets.Value("string")}
                    ),
                    "answerKey": datasets.Value("string"),
                    "fact1": datasets.Value("string"),
                    "fact2": datasets.Value("string"),
                    "combinedfact": datasets.Value("string"),
                    "formatted_question": datasets.Value("string"),
                    # These are the features of your dataset like images, labels ...
                }
            ),
            # If there's a common (input, target) tuple from the features,
            # specify them here. They'll be used if as_supervised=True in
            # builder.as_dataset.
            supervised_keys=None,
            # Homepage of the dataset for documentation
            homepage="https://allenai.org/data/qasc",
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        # TODO(qasc): Downloads the data and defines the splits
        # dl_manager is a datasets.download.DownloadManager that can be used to
        # download and extract URLs
        dl_dir = dl_manager.download_and_extract(_URl)
        data_dir = os.path.join(dl_dir, "QASC_Dataset")
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={"filepath": os.path.join(data_dir, "train.jsonl")},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={"filepath": os.path.join(data_dir, "test.jsonl")},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={"filepath": os.path.join(data_dir, "dev.jsonl")},
            ),
        ]

    def _generate_examples(self, filepath):
        """Yields examples."""
        # TODO(qasc): Yields (key, example) tuples from the dataset
        with open(filepath, encoding="utf-8") as f:
            for row in f:
                data = json.loads(row)
                answerkey = data.get("answerKey", "")
                id_ = data["id"]
                question = data["question"]["stem"]
                choices = data["question"]["choices"]
                text_choices = [choice["text"] for choice in choices]
                label_choices = [choice["label"] for choice in choices]
                fact1 = data.get("fact1", "")
                fact2 = data.get("fact2", "")
                combined_fact = data.get("combinedfact", "")
                formatted_question = data.get("formatted_question", "")
                yield id_, {
                    "id": id_,
                    "answerKey": answerkey,
                    "question": question,
                    "choices": {"text": text_choices, "label": label_choices},
                    "fact1": fact1,
                    "fact2": fact2,
                    "combinedfact": combined_fact,
                    "formatted_question": formatted_question,
                }
