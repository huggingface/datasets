# coding=utf-8
# Lint as: python3
"""OffensEval-TR 2020: A Corpus of Turkish Offensive Language on Social Media"""


import csv
import os

import datasets


logger = datasets.logging.get_logger(__name__)


_CITATION = """\
@InProceedings{coltekin2020lrec,
 author  = {Cagri Coltekin},
 year  = {2020},
 title  = {A Corpus of Turkish Offensive Language on Social Media},
 booktitle  = {Proceedings of The 12th Language Resources and Evaluation Conference},
 pages  = {6174--6184},
 address  = {Marseille, France},
 url  = {https://www.aclweb.org/anthology/2020.lrec-1.758},
}
"""


_DESCRIPTION = """\
OffensEval-TR 2020 is a Turkish offensive language corpus. The corpus consist of randomly sampled tweets and annotated in a similar way to OffensEval and GermEval.
"""

_HOMEPAGE = "https://coltekin.github.io/offensive-turkish/"
_DOWNLOAD_URL = "https://coltekin.github.io/offensive-turkish/offenseval2020-turkish.zip"
_FOLDER_NAME = "offenseval-tr-{split}-v1"


class OffensEval2020TRConfig(datasets.BuilderConfig):
    """BuilderConfig for OffensEval2020TR."""

    def __init__(self, **kwargs):
        """BuilderConfig for OffensEval2020TR.

        Args:
          **kwargs: keyword arguments forwarded to super.
        """
        super(OffensEval2020TRConfig, self).__init__(**kwargs)


class Offenseval2020TR(datasets.GeneratorBasedBuilder):
    """OffensEval-TR 2020: A Corpus of Turkish Offensive Language on Social Media"""

    BUILDER_CONFIGS = [
        OffensEval2020TRConfig(
            name="offenseval2020-turkish",
            version=datasets.Version("1.0.0"),
            description="OffensEval-TR 2020: A Corpus of Turkish Offensive Language on Social Media",
        ),
    ]

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "id": datasets.Value("int32"),
                    "tweet": datasets.Value("string"),
                    "subtask_a": datasets.features.ClassLabel(names=["NOT", "OFF"]),
                }
            ),
            supervised_keys=None,
            homepage=_HOMEPAGE,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        dl_dir = dl_manager.download_and_extract(_DOWNLOAD_URL)
        data_dir = os.path.join(dl_dir, self.config.name)

        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={
                    "filepath": os.path.join(
                        data_dir, _FOLDER_NAME.format(split="training"), "offenseval-tr-training-v1.tsv"
                    ),
                    "labelpath": None,
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                gen_kwargs={
                    "filepath": os.path.join(
                        data_dir, _FOLDER_NAME.format(split="testset"), "offenseval-tr-testset-v1.tsv"
                    ),
                    "labelpath": os.path.join(
                        data_dir, _FOLDER_NAME.format(split="testset"), "offenseval-tr-labela-v1.tsv"
                    ),
                },
            ),
        ]

    def _generate_examples(self, filepath, labelpath):
        """Generate OffensEval2020TR examples."""
        logger.info("⏳ Generating examples from = %s", filepath)

        if labelpath:
            with open(filepath, encoding="utf-8") as f:
                with open(labelpath, encoding="utf-8") as f2:
                    reader_testset = csv.DictReader(f, delimiter="\t", quoting=csv.QUOTE_NONE)
                    reader_label = csv.DictReader(
                        f2, delimiter=",", quoting=csv.QUOTE_NONE, fieldnames=["id", "subtask_a"]
                    )
                    list_label = list(reader_label)
                    for idx, row in enumerate(reader_testset):
                        row_label = list_label[idx]
                        yield idx, {"id": row["id"], "tweet": row["tweet"], "subtask_a": row_label["subtask_a"]}
        else:
            with open(filepath, encoding="utf-8") as f:
                reader = csv.DictReader(f, delimiter="\t", quoting=csv.QUOTE_NONE)
                for idx, row in enumerate(reader):
                    yield idx, {"id": row["id"], "tweet": row["tweet"], "subtask_a": row["subtask_a"]}
