# coding=utf-8
# Lint as: python3
"""ELI5-Category: A categorized open-domain QA dataset."""


import json

import datasets


logger = datasets.logging.get_logger(__name__)

_CITATION = """\
@inproceedings{eli5-category,
  author    = {Jingsong Gao and
               Qingren Zhou and
               Rui Qiu},
  title     = {{ELI5-Category:} A categorized open-domain QA dataset},
  year      = {2021}
}
"""

_DESCRIPTION = """\
The ELI5-Category dataset is a smaller but newer and categorized version of the original ELI5 dataset. \
After 2017, a tagging system was introduced to this subreddit so that the questions can be categorized \
into different topics according to their tags. Since the training and validation set is built by questions \
in different topics, the dataset is expected to alleviate the train/validation overlapping issue \
in the original ELI5 dataset.
"""


class ELI5CategoryConfig(datasets.BuilderConfig):
    """BuilderConfig for ELI5Category."""

    def __init__(self, **kwargs):
        """BuilderConfig for ELI5Category.
        Args:
          **kwargs: keyword arguments forwarded to super.
        """
        super(ELI5CategoryConfig, self).__init__(**kwargs)


class ELI5Category(datasets.GeneratorBasedBuilder):
    """ELI5-Category: A categorized open-domain QA dataset."""

    VERSION = datasets.Version("1.0.0")

    BUILDER_CONFIGS = [
        ELI5CategoryConfig(
            name="default",
            version=datasets.Version("1.0.0"),
            description="Default config",
        ),
    ]

    DEFAULT_CONFIG_NAME = "default"

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "q_id": datasets.Value("string"),
                    "title": datasets.Value("string"),
                    "selftext": datasets.Value("string"),
                    "category": datasets.Value("string"),
                    "subreddit": datasets.Value("string"),
                    "answers": {
                        "a_id": datasets.features.Sequence(datasets.Value("string")),
                        "text": datasets.features.Sequence(datasets.Value("string")),
                        "score": datasets.features.Sequence(datasets.Value("int32")),
                        "text_urls": datasets.features.Sequence(datasets.features.Sequence(datasets.Value("string"))),
                    },
                    "title_urls": datasets.features.Sequence(datasets.Value("string")),
                    "selftext_urls": datasets.features.Sequence(datasets.Value("string")),
                }
            ),
            supervised_keys=None,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        _URL = "https://jingshensn2.github.io/eli5c/datasets/"
        downloaded_files = dl_manager.download_and_extract(
            {
                "train": _URL + "eli5-category-train.json.gz",
                "val1": _URL + "eli5-category-validation-1.json.gz",
                "val2": _URL + "eli5-category-validation-2.json.gz",
                "test": _URL + "eli5-category-test.json.gz",
            }
        )
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={"filepath": downloaded_files["train"]},
            ),
            datasets.SplitGenerator(
                name=datasets.Split("validation1"),
                gen_kwargs={"filepath": downloaded_files["val1"]},
            ),
            datasets.SplitGenerator(
                name=datasets.Split("validation2"),
                gen_kwargs={"filepath": downloaded_files["val2"]},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                gen_kwargs={"filepath": downloaded_files["test"]},
            ),
        ]

    def _generate_examples(self, filepath):
        logger.info("generating examples from = %s", filepath)
        with open(filepath, encoding="utf-8") as f:
            example = json.load(f)
            for id_, row in enumerate(example):
                yield id_, row
