"""IMDB Dataset: A Large-Scale French Movie Reviews Dataset."""


import json
import os

import datasets


_CITATION = """\
@inproceedings{dontstoppretraining2020,
 author = {Suchin Gururangan and Ana Marasović and Swabha Swayamdipta and Kyle Lo and Iz Beltagy and Doug Downey and Noah A. Smith},
 title = {Don't Stop Pretraining: Adapt Language Models to Domains and Tasks},
 year = {2020},
 booktitle = {Proceedings of ACL},
}
"""

_DESCRIPTION = """\
IMDB Dataset: A Large-Scale French Movie Reviews Dataset.
"""


class AllocineConfig(datasets.BuilderConfig):
    """BuilderConfig for Allocine."""

    def __init__(self, **kwargs):
        """BuilderConfig for Allocine.
        Args:
          **kwargs: keyword arguments forwarded to super.
        """
        super(AllocineConfig, self).__init__(**kwargs)


class AllocineDataset(datasets.GeneratorBasedBuilder):
    """Allocine Dataset: A Large-Scale French Movie Reviews Dataset."""

    _DOWNLOAD_URL = "https://allennlp.s3-us-west-2.amazonaws.com/dont_stop_pretraining/data/imdb/"
    _TRAIN_FILE = "train.jsonl"
    _VAL_FILE = "dev.jsonl"
    _TEST_FILE = "test.jsonl"

    BUILDER_CONFIGS = [
        AllocineConfig(
            name="imdb_dont_stop",
            version=datasets.Version("1.0.0"),
            description="IMDB Dataset",
        ),
    ]

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "text": datasets.Value("string"),
                    "label": datasets.features.ClassLabel(names=["0", "1"]),
                }
            ),
            supervised_keys=None,
            homepage="https://github.com/allenai/dont-stop-pretraining",
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        train_path = dl_manager.download_and_extract(os.path.join(self._DOWNLOAD_URL, self._TRAIN_FILE))

        val_path = dl_manager.download_and_extract(os.path.join(self._DOWNLOAD_URL, self._VAL_FILE))

        test_path = dl_manager.download_and_extract(os.path.join(self._DOWNLOAD_URL, self._TEST_FILE))

        return [
            datasets.SplitGenerator(name=datasets.Split.TRAIN, gen_kwargs={"filepath": train_path}),
            datasets.SplitGenerator(name=datasets.Split.VALIDATION, gen_kwargs={"filepath": val_path}),
            datasets.SplitGenerator(name=datasets.Split.TEST, gen_kwargs={"filepath": test_path}),
        ]

    def _generate_examples(self, filepath):
        """Generate Allocine examples."""
        with open(filepath, encoding="utf-8") as f:
            for id_, row in enumerate(f):
                data = json.loads(row)
                text = data["text"]
                label = str(data["label"])
                yield id_, {"text": text, "label": label}
