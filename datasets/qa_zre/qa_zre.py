"""A dataset reducing relation extraction to simple reading comprehension questions"""
from __future__ import absolute_import, division, print_function

import csv
import os

import datasets


_CITATION = """\
@inproceedings{levy-etal-2017-zero,
    title = "Zero-Shot Relation Extraction via Reading Comprehension",
    author = "Levy, Omer  and
      Seo, Minjoon  and
      Choi, Eunsol  and
      Zettlemoyer, Luke",
    booktitle = "Proceedings of the 21st Conference on Computational Natural Language Learning ({C}o{NLL} 2017)",
    month = aug,
    year = "2017",
    address = "Vancouver, Canada",
    publisher = "Association for Computational Linguistics",
    url = "https://www.aclweb.org/anthology/K17-1034",
    doi = "10.18653/v1/K17-1034",
    pages = "333--342",
}
"""

_DESCRIPTION = """\
A dataset reducing relation extraction to simple reading comprehension questions
"""

_DATA_URL = "http://nlp.cs.washington.edu/zeroshot/relation_splits.tar.bz2"


class QaZre(datasets.GeneratorBasedBuilder):
    """QA-ZRE: Reducing relation extraction to simple reading comprehension questions"""

    VERSION = datasets.Version("0.1.0")

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "relation": datasets.Value("string"),
                    "question": datasets.Value("string"),
                    "subject": datasets.Value("string"),
                    "context": datasets.Value("string"),
                    "answers": datasets.features.Sequence(datasets.Value("string")),
                }
            ),
            # If there's a common (input, target) tuple from the features,
            # specify them here. They'll be used if as_supervised=True in
            # builder.as_dataset.
            supervised_keys=None,
            # Homepage of the dataset for documentation
            homepage="http://nlp.cs.washington.edu/zeroshot",
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        dl_dir = dl_manager.download_and_extract(_DATA_URL)
        dl_dir = os.path.join(dl_dir, "relation_splits")

        return [
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                gen_kwargs={
                    "filepaths": [os.path.join(dl_dir, "test." + str(i)) for i in range(10)],
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                gen_kwargs={
                    "filepaths": [os.path.join(dl_dir, "dev." + str(i)) for i in range(10)],
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={
                    "filepaths": [os.path.join(dl_dir, "train." + str(i)) for i in range(10)],
                },
            ),
        ]

    def _generate_examples(self, filepaths):
        """Yields examples."""

        for filepath in filepaths:
            with open(filepath, encoding="utf-8") as f:
                data = csv.reader(f, delimiter="\t")
                for idx, row in enumerate(data):
                    yield idx, {
                        "relation": row[0],
                        "question": row[1],
                        "subject": row[2],
                        "context": row[3],
                        "answers": row[4:],
                    }
