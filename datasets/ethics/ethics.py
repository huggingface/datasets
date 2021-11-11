"""ETHICS: Justice Dataset."""


import csv
import os

import datasets


_CITATION = """\
@article{hendrycksethics2021,
  title={Aligning {AI} With Shared Human Values},
  author={Dan Hendrycks
    and Collin Burns
    and Steven Basart
    and Andrew Critch
    and Jerry Li
    and Dawn Song
    and Jacob Steinhardt},
  journal={arXiv preprint arXiv:2008.02275},
  year={2021}
}
"""


_DESCRIPTION = """\
The dataset is based in natural language scenarios, which enables us to construct diverse situations involving interpersonal relationships, everyday events, and thousands of objects. This means models must connect diverse facts about the world to their ethical consequences. For instance, taking a penny lying on the street is usually acceptable, whereas taking cash from a wallet lying on the street is not. 

The ETHICS dataset has contextualized scenarios about justice, deontology, virtue ethics, utilitarianism, and commonsense moral intuitions. To do well on the ETHICS dataset, models must know
about the morally relevant factors emphasized by each of these ethical systems.
"""


_HOMEPAGE = "https://github.com/hendrycks/ethics"


_LICENSE = "https://github.com/hendrycks/ethics/blob/master/LICENSE"


_URL = "https://people.eecs.berkeley.edu/~hendrycks/ethics.tar"

_DOMAIN_TO_DATA_FILE_PREFIX = {
    "commonsense_morality": "cm",
    "deontology": "deontology",
    "justice": "justice",
    "utilitarianism": "util",
    "virtue_ethics": "virtue",
}

_DOMAIN_TO_SUBFOLDER = {
    "commonsense_morality": "commonsense",
    "deontology": "deontology",
    "justice": "justice",
    "utilitarianism": "utilitarianism",
    "virtue_ethics": "virtue",
}


class NewDataset(datasets.GeneratorBasedBuilder):
    """ETHICS: Justice Dataset."""

    VERSION = datasets.Version("1.0.0")

    BUILDER_CONFIGS = [
        datasets.BuilderConfig(name="commonsense_morality", version=VERSION),
        datasets.BuilderConfig(name="deontology", version=VERSION),
        datasets.BuilderConfig(name="justice", version=VERSION),
        datasets.BuilderConfig(name="utilitarianism", version=VERSION),
        datasets.BuilderConfig(name="virtue_ethics", version=VERSION),
    ]

    def _info(self):

        features = {
            "commonsense_morality": datasets.Features(
                {
                    "label": datasets.ClassLabel(2),
                    "input": datasets.Value("string"),
                    "is_short": datasets.ClassLabel(names=["True", "False"]),
                    "edited": datasets.ClassLabel(names=["True", "False"]),
                }
            ),
            "deontology": datasets.Features(
                {
                    "label": datasets.ClassLabel(2),
                    "scenario": datasets.Value("string"),
                    "excuse": datasets.Value("string"),
                }
            ),
            "justice": datasets.Features(
                {
                    "label": datasets.ClassLabel(2),
                    "scenario": datasets.Value("string"),
                }
            ),
            "utilitarianism": datasets.Features(
                {
                    "more_pleasant": datasets.Value("string"),
                    "less_pleasant": datasets.Value("string"),
                }
            ),
            "virtue_ethics": datasets.Features(
                {
                    "label": datasets.ClassLabel(2),
                    "scenario": datasets.Value("string"),
                }
            ),
        }[self.config.name]

        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=features,
            supervised_keys=None,
            homepage=_HOMEPAGE,
            license=_LICENSE,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        data_dir = dl_manager.download_and_extract(_URL)
        return [
            datasets.SplitGenerator(
                name=datasets.NamedSplit("train"),
                gen_kwargs={
                    "filepath": os.path.join(
                        data_dir,
                        "ethics",
                        _DOMAIN_TO_SUBFOLDER[self.config.name],
                        f"{_DOMAIN_TO_DATA_FILE_PREFIX[self.config.name]}_train.csv",
                    ),
                    "split": "train",
                },
            ),
            datasets.SplitGenerator(
                name=datasets.NamedSplit("test"),
                gen_kwargs={
                    "filepath": os.path.join(
                        data_dir,
                        "ethics",
                        _DOMAIN_TO_SUBFOLDER[self.config.name],
                        f"{_DOMAIN_TO_DATA_FILE_PREFIX[self.config.name]}_test.csv",
                    ),
                    "split": "test",
                },
            ),
            datasets.SplitGenerator(
                name=datasets.NamedSplit("test_hard"),
                gen_kwargs={
                    "filepath": os.path.join(
                        data_dir,
                        "ethics",
                        _DOMAIN_TO_SUBFOLDER[self.config.name],
                        f"{_DOMAIN_TO_DATA_FILE_PREFIX[self.config.name]}_test_hard.csv",
                    ),
                    "split": "test_hard",
                },
            ),
        ]

    def _generate_examples(self, filepath, split):
        """Yields examples as (key, example) tuples."""
        with open(filepath, encoding="utf-8") as f:
            fieldnames = None
            if self.config.name == "utilitarianism":
                fieldnames = ["more_pleasant", "less_pleasant"]

            reader = csv.DictReader(f, fieldnames=fieldnames)
            for _id, row in enumerate(reader):
                yield _id, row
