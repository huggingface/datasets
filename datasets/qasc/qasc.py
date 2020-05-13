"""TODO(qasc): Add a description here."""

from __future__ import absolute_import, division, print_function

import json
import os

import nlp


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


class Qasc(nlp.GeneratorBasedBuilder):
    """TODO(qasc): Short description of my dataset."""

    # TODO(qasc): Set up version.
    VERSION = nlp.Version("0.1.0")

    def _info(self):
        # TODO(qasc): Specifies the nlp.DatasetInfo object
        return nlp.DatasetInfo(
            # This is the description that will appear on the datasets page.
            description=_DESCRIPTION,
            # nlp.features.FeatureConnectors
            features=nlp.Features(
                {
                    "id": nlp.Value("string"),
                    "question": nlp.Value("string"),
                    "choices": nlp.features.Sequence({"text": nlp.Value("string"), "label": nlp.Value("string")}),
                    "answerKey": nlp.Value("string"),
                    "fact1": nlp.Value("string"),
                    "fact2": nlp.Value("string"),
                    "combinedfact": nlp.Value("string"),
                    "formatted_question": nlp.Value("string"),
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
        # dl_manager is a nlp.download.DownloadManager that can be used to
        # download and extract URLs
        dl_dir = dl_manager.download_and_extract(_URl)
        data_dir = os.path.join(dl_dir, "QASC_Dataset")
        return [
            nlp.SplitGenerator(
                name=nlp.Split.TRAIN,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={"filepath": os.path.join(data_dir, "train.jsonl")},
            ),
            nlp.SplitGenerator(
                name=nlp.Split.TEST,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={"filepath": os.path.join(data_dir, "test.jsonl")},
            ),
            nlp.SplitGenerator(
                name=nlp.Split.VALIDATION,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={"filepath": os.path.join(data_dir, "dev.jsonl")},
            ),
        ]

    def _generate_examples(self, filepath):
        """Yields examples."""
        # TODO(qasc): Yields (key, example) tuples from the dataset
        with open(filepath) as f:
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
