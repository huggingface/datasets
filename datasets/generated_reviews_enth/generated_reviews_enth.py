"""`generated_reviews_enth`: Generated product reviews dataset for machine translation quality prediction, part of [scb-mt-en-th-2020](https://arxiv.org/pdf/2007.03541.pdf)"""

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
 `generated_reviews_enth`
 Generated product reviews dataset for machine translation quality prediction, part of [scb-mt-en-th-2020](https://arxiv.org/pdf/2007.03541.pdf)
 `generated_reviews_enth` is created as part of [scb-mt-en-th-2020](https://arxiv.org/pdf/2007.03541.pdf) for machine translation task.
 This dataset (referred to as `generated_reviews_yn` in [scb-mt-en-th-2020](https://arxiv.org/pdf/2007.03541.pdf)) are English product reviews
 generated by [CTRL](https://arxiv.org/abs/1909.05858), translated by Google Translate API and annotated as accepted or rejected (`correct`)
 based on fluency and adequacy of the translation by human annotators.
 This allows it to be used for English-to-Thai translation quality esitmation (binary label), machine translation, and sentiment analysis.
"""


class GeneratedReviewsEnthConfig(datasets.BuilderConfig):
    """BuilderConfig for GeneratedReviewsEnth."""

    def __init__(self, **kwargs):
        """BuilderConfig for GeneratedReviewsEnth.

        Args:
          **kwargs: keyword arguments forwarded to super.
        """
        super(GeneratedReviewsEnthConfig, self).__init__(**kwargs)
        self.language_pair = ("en", "th")


class GeneratedReviewsEnth(datasets.GeneratorBasedBuilder):
    """`generated_reviews_enth`: Generated product reviews dataset for machine translation quality prediction, part of [scb-mt-en-th-2020](https://arxiv.org/pdf/2007.03541.pdf)"""

    _DOWNLOAD_URL = "https://github.com/vistec-AI/generated_reviews_enth/raw/main/data.zip"
    _TRAIN_FILE = "train.jsonl"
    _VAL_FILE = "valid.jsonl"
    _TEST_FILE = "test.jsonl"

    BUILDER_CONFIGS = [
        GeneratedReviewsEnthConfig(
            name="generated_reviews_enth",
            version=datasets.Version("1.0.0"),
            description="`generated_reviews_enth`: Generated product reviews dataset for machine translation quality prediction, part of [scb-mt-en-th-2020](https://arxiv.org/pdf/2007.03541.pdf)",
        ),
    ]

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "translation": datasets.features.Translation(languages=self.config.language_pair),
                    "review_star": datasets.Value("int32"),
                    "correct": datasets.features.ClassLabel(names=["neg", "pos"]),
                }
            ),
            supervised_keys=None,
            homepage="https://github.com/vistec-AI/generated_reviews_enth",
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
        """Generate generated_reviews_enth examples."""
        source, target = self.config.language_pair
        with open(filepath, encoding="utf-8") as f:
            for id_, row in enumerate(f):
                data = json.loads(row)
                yield id_, {
                    "translation": {source: data["en_segment"], target: data["th_segment"]},
                    "review_star": data["review_star"],
                    "correct": data["correct"],
                }
