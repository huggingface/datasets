"""TODO(qasc): Add a description here."""


import json

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
        archive = dl_manager.download(_URl)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "filepath": "/".join(["QASC_Dataset", "train.jsonl"]),
                    "files": dl_manager.iter_archive(archive),
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "filepath": "/".join(["QASC_Dataset", "test.jsonl"]),
                    "files": dl_manager.iter_archive(archive),
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "filepath": "/".join(["QASC_Dataset", "dev.jsonl"]),
                    "files": dl_manager.iter_archive(archive),
                },
            ),
        ]

    def _generate_examples(self, filepath, files):
        """Yields examples."""
        # TODO(qasc): Yields (key, example) tuples from the dataset
        for path, f in files:
            if path == filepath:
                for row in f:
                    data = json.loads(row.decode("utf-8"))
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
                break
