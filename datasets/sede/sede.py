"""SEDE: Text-to-SQL in the Wild: A Naturally-Occurring Dataset Based on Stack Exchange Data."""


import json

import datasets


logger = datasets.logging.get_logger(__name__)

_CITATION = """\
@misc{hazoom2021texttosql,
      title={Text-to-SQL in the Wild: A Naturally-Occurring Dataset Based on Stack Exchange Data},
      author={Moshe Hazoom and Vibhor Malik and Ben Bogin},
      year={2021},
      eprint={2106.05006},
      archivePrefix={arXiv},
      primaryClass={cs.CL}
}
"""

_DESCRIPTION = """\
SEDE (Stack Exchange Data Explorer) is new dataset for Text-to-SQL tasks with more than 12,000 SQL queries and their
natural language description. It's based on a real usage of users from the Stack Exchange Data Explorer platform,
which brings complexities and challenges never seen before in any other semantic parsing dataset like
including complex nesting, dates manipulation, numeric and text manipulation, parameters, and most
importantly: under-specification and hidden-assumptions.

Paper (NLP4Prog workshop at ACL2021): https://arxiv.org/abs/2106.05006
"""


class SEDEConfig(datasets.BuilderConfig):
    """BuilderConfig for SEDE."""

    def __init__(self, **kwargs):
        """BuilderConfig for SEDE.

        Args:
          **kwargs: keyword arguments forwarded to super.
        """
        super(SEDEConfig, self).__init__(**kwargs)


class SEDE(datasets.GeneratorBasedBuilder):
    """SEDE Dataset: A Naturally-Occurring Dataset Based on Stack Exchange Data."""

    _DOWNLOAD_URL = "https://raw.githubusercontent.com/hirupert/sede/main/data/sede"
    _TRAIN_FILE = "train.jsonl"
    _VAL_FILE = "val.jsonl"
    _TEST_FILE = "test.jsonl"

    BUILDER_CONFIGS = [
        SEDEConfig(
            name="sede",
            version=datasets.Version("1.0.0"),
            description="SEDE Dataset: A Naturally-Occurring Dataset Based on Stack Exchange Data.",
        ),
    ]

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "QuerySetId": datasets.Value("uint32"),
                    "Title": datasets.Value("string"),
                    "Description": datasets.Value("string"),
                    "QueryBody": datasets.Value("string"),
                    "CreationDate": datasets.Value("string"),
                    "validated": datasets.Value("bool"),
                }
            ),
            license="Apache-2.0 License",
            supervised_keys=None,
            homepage="https://github.com/hirupert/sede",
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        train_path = dl_manager.download_and_extract(self._DOWNLOAD_URL + "/" + self._TRAIN_FILE)
        val_path = dl_manager.download_and_extract(self._DOWNLOAD_URL + "/" + self._VAL_FILE)
        test_path = dl_manager.download_and_extract(self._DOWNLOAD_URL + "/" + self._TEST_FILE)
        return [
            datasets.SplitGenerator(name=datasets.Split.TRAIN, gen_kwargs={"data_filepath": train_path}),
            datasets.SplitGenerator(name=datasets.Split.VALIDATION, gen_kwargs={"data_filepath": val_path}),
            datasets.SplitGenerator(name=datasets.Split.TEST, gen_kwargs={"data_filepath": test_path}),
        ]

    def _generate_examples(self, data_filepath):
        """Generate SEDE examples."""
        logger.info("generating examples from = %s", data_filepath)
        with open(data_filepath, encoding="utf-8") as f:
            for idx, sample_str in enumerate(f):
                sample_json = json.loads(sample_str)
                yield idx, sample_json
