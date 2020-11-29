"""TODO(hellaswag): Add a description here."""

from __future__ import absolute_import, division, print_function

import json

import datasets


# TODO(hellaswag): BibTeX citation
_CITATION = """\
@inproceedings{zellers2019hellaswag,
    title={HellaSwag: Can a Machine Really Finish Your Sentence?},
    author={Zellers, Rowan and Holtzman, Ari and Bisk, Yonatan and Farhadi, Ali and Choi, Yejin},
    booktitle ={Proceedings of the 57th Annual Meeting of the Association for Computational Linguistics},
    year={2019}
}
"""

# TODO(hellaswag):
_DESCRIPTION = """
"""
_URL = "https://github.com/rowanz/hellaswag/raw/master/data/"
_URLS = {
    "train": _URL + "hellaswag_train.jsonl",
    "test": _URL + "hellaswag_test.jsonl",
    "dev": _URL + "hellaswag_val.jsonl",
}


class Hellaswag(datasets.GeneratorBasedBuilder):
    """TODO(hellaswag): Short description of my dataset."""

    # TODO(hellaswag): Set up version.
    VERSION = datasets.Version("0.1.0")

    def _info(self):
        # TODO(hellaswag): Specifies the datasets.DatasetInfo object
        return datasets.DatasetInfo(
            # This is the description that will appear on the datasets page.
            description=_DESCRIPTION,
            # datasets.features.FeatureConnectors
            features=datasets.Features(
                {
                    # These are the features of your dataset like images, labels ...
                    "ind": datasets.Value("int32"),
                    "activity_label": datasets.Value("string"),
                    "ctx_a": datasets.Value("string"),
                    "ctx_b": datasets.Value("string"),
                    "ctx": datasets.Value("string"),
                    "endings": datasets.features.Sequence(datasets.Value("string")),
                    "source_id": datasets.Value("string"),
                    "split": datasets.Value("string"),
                    "split_type": datasets.Value("string"),
                    "label": datasets.Value("string"),
                }
            ),
            # If there's a common (input, target) tuple from the features,
            # specify them here. They'll be used if as_supervised=True in
            # builder.as_dataset.
            supervised_keys=None,
            # Homepage of the dataset for documentation
            homepage="https://rowanzellers.com/hellaswag/",
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        # TODO(hellaswag): Downloads the data and defines the splits
        # dl_manager is a datasets.download.DownloadManager that can be used to
        # download and extract URLs
        urls_to_download = _URLS
        dl_dir = dl_manager.download_and_extract(urls_to_download)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={"filepath": dl_dir["train"]},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={"filepath": dl_dir["test"]},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={"filepath": dl_dir["dev"]},
            ),
        ]

    def _generate_examples(self, filepath):
        """Yields examples."""
        # TODO(hellaswag): Yields (key, example) tuples from the dataset
        with open(filepath, encoding="utf-8") as f:
            for id_, row in enumerate(f):
                data = json.loads(row)
                yield id_, {
                    "ind": int(data["ind"]),
                    "activity_label": data["activity_label"],
                    "ctx_a": data.get("ctx_a", ""),
                    "ctx_b": data.get("ctx_b", ""),
                    "ctx": data["ctx"],
                    "endings": data.get("endings", []),
                    "source_id": data["source_id"],
                    "split": data["split"],
                    "split_type": data["split_type"],
                    "label": str(data.get("label", "")),
                }
