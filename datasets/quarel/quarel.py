"""TODO(quarel): Add a description here."""

from __future__ import absolute_import, division, print_function

import json
import os

import datasets


# TODO(quarel): BibTeX citation
_CITATION = """\
@inproceedings{quarel_v1,
    title={QuaRel: A Dataset and Models for Answering Questions about Qualitative Relationships},
    author={Oyvind Tafjord, Peter Clark, Matt Gardner, Wen-tau Yih, Ashish Sabharwal},
    year={2018},
    journal={arXiv:1805.05377v1}
}
"""

# TODO(quarel):
_DESCRIPTION = """
QuaRel is a crowdsourced dataset of 2771 multiple-choice story questions, including their logical forms.
"""
_URL = "https://s3-us-west-2.amazonaws.com/ai2-website/data/quarel-dataset-v1-nov2018.zip"


class Quarel(datasets.GeneratorBasedBuilder):
    """TODO(quarel): Short description of my dataset."""

    # TODO(quarel): Set up version.
    VERSION = datasets.Version("0.1.0")

    def _info(self):
        # TODO(quarel): Specifies the datasets.DatasetInfo object
        return datasets.DatasetInfo(
            # This is the description that will appear on the datasets page.
            description=_DESCRIPTION,
            # datasets.features.FeatureConnectors
            features=datasets.Features(
                {
                    # These are the features of your dataset like images, labels ...
                    "id": datasets.Value("string"),
                    "answer_index": datasets.Value("int32"),
                    "logical_forms": datasets.features.Sequence(datasets.Value("string")),
                    "logical_form_pretty": datasets.Value("string"),
                    "world_literals": datasets.features.Sequence(
                        {"world1": datasets.Value("string"), "world2": datasets.Value("string")}
                    ),
                    "question": datasets.Value("string"),
                }
            ),
            # If there's a common (input, target) tuple from the features,
            # specify them here. They'll be used if as_supervised=True in
            # builder.as_dataset.
            supervised_keys=None,
            # Homepage of the dataset for documentation
            homepage="https://allenai.org/data/quarel",
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        # TODO(quarel): Downloads the data and defines the splits
        # dl_manager is a datasets.download.DownloadManager that can be used to
        # download and extract URLs
        dl_dir = dl_manager.download_and_extract(_URL)
        data_dir = os.path.join(dl_dir, "quarel-dataset-v1")
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={"filepath": os.path.join(data_dir, "quarel-v1-train.jsonl")},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={"filepath": os.path.join(data_dir, "quarel-v1-test.jsonl")},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={"filepath": os.path.join(data_dir, "quarel-v1-dev.jsonl")},
            ),
        ]

    def _generate_examples(self, filepath):
        """Yields examples."""
        # TODO(quarel): Yields (key, example) tuples from the dataset
        with open(filepath, encoding="utf-8") as f:
            for id_, row in enumerate(f):
                data = json.loads(row)
                yield id_, {
                    "id": data["id"],
                    "answer_index": data["answer_index"],
                    "logical_forms": data["logical_forms"],
                    "world_literals": {
                        "world1": [data["world_literals"]["world1"]],
                        "world2": [data["world_literals"]["world2"]],
                    },
                    "logical_form_pretty": data["logical_form_pretty"],
                    "question": data["question"],
                }
