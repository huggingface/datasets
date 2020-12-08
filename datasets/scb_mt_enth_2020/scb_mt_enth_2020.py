from __future__ import absolute_import, division, print_function

import json
import os

import datasets


_CITATION = """\
@article{lowphansirikul2020scb,
  title={scb-mt-en-th-2020: A Large English-Thai Parallel Corpus},
  author={Lowphansirikul, Lalita and Polpanumas, Charin and Rutherford, Attapol T and Nutanong, Sarana},
  journal={arXiv preprint arXiv:2007.03541},
  year={2020}
}
"""

_DESCRIPTION = """\
scb-mt-en-th-2020: A Large English-Thai Parallel Corpus
The primary objective of our work is to build a large-scale English-Thai dataset for machine translation.
We construct an English-Thai machine translation dataset with over 1 million segment pairs, curated from various sources,
namely news, Wikipedia articles, SMS messages, task-based dialogs, web-crawled data and government documents.
Methodology for gathering data, building parallel texts and removing noisy sentence pairs are presented in a reproducible manner.
We train machine translation models based on this dataset. Our models' performance are comparable to that of
Google Translation API (as of May 2020) for Thai-English and outperform Google when the Open Parallel Corpus (OPUS) is
included in the training data for both Thai-English and English-Thai translation.
The dataset, pre-trained models, and source code to reproduce our work are available for public use.
"""


class ScbMtEnth2020Config(datasets.BuilderConfig):
    """BuilderConfig for ScbMtEnth2020."""

    def __init__(self, language_pair=(None, None), **kwargs):
        """BuilderConfig for ScbMtEnth2020.

        Args:
          **kwargs: keyword arguments forwarded to super.
        """
        super(ScbMtEnth2020Config, self).__init__(
            name=f"{language_pair[0]}{language_pair[1]}",
            description="Translate {language_pair[0]} to {language_pair[1]}",
            version=datasets.Version("1.0.0"),
            **kwargs,
        )
        self.language_pair = language_pair


class ScbMtEnth2020(datasets.GeneratorBasedBuilder):
    """scb-mt-en-th-2020: A Large English-Thai Parallel Corpus"""

    _DOWNLOAD_URL = "https://archive.org/download/scb_mt_enth_2020/data.zip"
    _TRAIN_FILE = "train.jsonl"
    _VAL_FILE = "valid.jsonl"
    _TEST_FILE = "test.jsonl"
    BUILDER_CONFIG_CLASS = ScbMtEnth2020Config
    BUILDER_CONFIGS = [
        ScbMtEnth2020Config(
            language_pair=("en", "th"),
        ),
        ScbMtEnth2020Config(
            language_pair=("th", "en"),
        ),
    ]

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "translation": datasets.features.Translation(languages=self.config.language_pair),
                    "subdataset": datasets.Value("string"),
                }
            ),
            supervised_keys=None,
            homepage="https://airesearch.in.th/",
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        arch_path = dl_manager.download_and_extract(self._DOWNLOAD_URL)
        data_dir = os.path.join(arch_path, "data")
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN, gen_kwargs={"filepath": os.path.join(data_dir, self._TRAIN_FILE)}
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION, gen_kwargs={"filepath": os.path.join(data_dir, self._VAL_FILE)}
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST, gen_kwargs={"filepath": os.path.join(data_dir, self._TEST_FILE)}
            ),
        ]

    def _generate_examples(self, filepath):
        """Generate examples."""
        source, target = self.config.language_pair
        with open(filepath, encoding="utf-8") as f:
            for id_, row in enumerate(f):
                data = json.loads(row)
                yield id_, {
                    "translation": {source: data[source], target: data[target]},
                    "subdataset": data["subdataset"],
                }
