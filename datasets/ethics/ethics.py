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
The dataset is based in natural language scenarios, which enables us to construct diverse
situations involving interpersonal relationships, everyday events, and thousands of objects.
This means models must connect diverse facts about the world to their ethical consequences.
The ETHICS: Justice dataset contains 27K examples, and has models perform binary classification
to predict whether each given claim about desert, merit, or entitlement is reasonable or unreasonable.
"""


_HOMEPAGE = "https://github.com/hendrycks/ethics"


_LICENSE = "https://github.com/hendrycks/ethics/blob/master/LICENSE"


_URL = "https://people.eecs.berkeley.edu/~hendrycks/ethics.tar"

_DOMAIN_TO_DATA_FILE_PREFIX = {
    "commonsense": "cm",
    "deontology": "deontology",
    "justice": "justice",
    "utilitarianism": "util",
    "virtue": "virtue",
}


# TODO: Name of the dataset usually match the script name with CamelCase instead of snake_case
class NewDataset(datasets.GeneratorBasedBuilder):
    """ETHICS: Justice Dataset."""

    VERSION = datasets.Version("1.0.0")

    # This is an example of a dataset with multiple configurations.
    # If you don't want/need to define several sub-sets in your dataset,
    # just remove the BUILDER_CONFIG_CLASS and the BUILDER_CONFIGS attributes.

    # If you need to make complex sub-parts in the datasets with configurable options
    # You can create your own builder configuration class to store attribute, inheriting from datasets.BuilderConfig
    # BUILDER_CONFIG_CLASS = MyBuilderConfig

    # You will be able to load one or the other configurations in the following list with
    # data = datasets.load_dataset('my_dataset', 'first_domain')
    # data = datasets.load_dataset('my_dataset', 'second_domain')
    BUILDER_CONFIGS = [
        datasets.BuilderConfig(name="commonsense", version=VERSION, description="TODO"),
        datasets.BuilderConfig(name="deontology", version=VERSION, description="TODO"),
        datasets.BuilderConfig(name="justice", version=VERSION, description="TODO"),
        datasets.BuilderConfig(name="utilitarianism", version=VERSION, description="TODO"),
        datasets.BuilderConfig(name="virtue", version=VERSION, description="TODO"),
    ]

    def _info(self):

        features = {
            "commonsense": datasets.Features(
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
            "virtue": datasets.Features(
                {
                    "label": datasets.ClassLabel(2),
                    "scenario": datasets.Value("string"),
                }
            ),
        }[self.config.name]

        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=features,  # Here we define them above because they are different between the two configurations
            supervised_keys=None,
            homepage=_HOMEPAGE,
            license=_LICENSE,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        # TODO: This method is tasked with downloading/extracting the data and defining the splits depending on the configuration
        # If several configurations are possible (listed in BUILDER_CONFIGS), the configuration selected by the user is in self.config.name

        # dl_manager is a datasets.download.DownloadManager that can be used to download and extract URLs
        # It can accept any type or nested list/dict and will give back the same structure with the url replaced with path to local files.
        # By default the archives will be extracted and a path to a cached folder where they are extracted is returned instead of the archive
        data_dir = dl_manager.download_and_extract(_URL)
        return [
            datasets.SplitGenerator(
                name=datasets.NamedSplit("train"),
                gen_kwargs={
                    "filepath": os.path.join(
                        data_dir,
                        "ethics",
                        self.config.name,
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
                        self.config.name,
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
                        self.config.name,
                        f"{_DOMAIN_TO_DATA_FILE_PREFIX[self.config.name]}_test_hard.csv",
                    ),
                    "split": "test_hard",
                },
            ),
        ]

    def _generate_examples(
        self, filepath, split  # method parameters are unpacked from `gen_kwargs` as given in `_split_generators`
    ):
        """Yields examples as (key, example) tuples."""
        # This method handles input defined in _split_generators to yield (key, example) tuples from the dataset.
        # The `key` is here for legacy reason (tfds) and is not important in itself.

        with open(filepath, encoding="utf-8") as f:
            fieldnames = None
            if self.config.name == "utilitarianism":
                fieldnames = ["more_pleasant", "less_pleasant"]

            reader = csv.DictReader(f, fieldnames=fieldnames)
            for _id, row in enumerate(reader):
                yield _id, row
