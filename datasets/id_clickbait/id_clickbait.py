# coding=utf-8
# Copyright 2020 The HuggingFace Datasets Authors and the current dataset script contributor.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""CLICK-ID: A Novel Dataset for Indonesian Clickbait Headlines"""


import csv
import glob
import os

import datasets


logger = datasets.logging.get_logger(__name__)


_CITATION = """\
@inproceedings{id_clickbait,
  author    = {Andika William, Yunita Sari},
  title     = {CLICK-ID: A Novel Dataset for Indonesian Clickbait Headlines},
  year      = {2020},
  url       = {http://dx.doi.org/10.17632/k42j7x2kpn.1},
}
"""

_DESCRIPTION = """\
The CLICK-ID dataset is a collection of Indonesian news headlines that was collected from 12 local online news
publishers; detikNews, Fimela, Kapanlagi, Kompas, Liputan6, Okezone, Posmetro-Medan, Republika, Sindonews, Tempo,
Tribunnews, and Wowkeren. This dataset is comprised of mainly two parts; (i) 46,119 raw article data, and (ii)
15,000 clickbait annotated sample headlines. Annotation was conducted with 3 annotator examining each headline.
Judgment were based only on the headline. The majority then is considered as the ground truth. In the annotated
sample, our annotation shows 6,290 clickbait and 8,710 non-clickbait.
"""

_HOMEPAGE = "https://github.com/feryandi/Dataset-Artikel"

_LICENSE = "Creative Commons Attribution 4.0 International license"

_URLs = ["https://md-datasets-cache-zipfiles-prod.s3.eu-west-1.amazonaws.com/k42j7x2kpn-1.zip"]


class IdClickbaitConfig(datasets.BuilderConfig):
    """BuilderConfig for IdClickbait"""

    def __init__(self, label_classes=None, path=None, **kwargs):
        """BuilderConfig for IdClickbait.
        Args:
          **kwargs: keyword arguments forwarded to super.
        """
        super(IdClickbaitConfig, self).__init__(**kwargs)
        self.label_classes = label_classes
        self.path = path


class IdClickbait(datasets.GeneratorBasedBuilder):
    VERSION = datasets.Version("1.0.0")

    BUILDER_CONFIGS = [
        IdClickbaitConfig(
            name="annotated",
            version=VERSION,
            description="Annotated clickbait dataset",
            label_classes=["non-clickbait", "clickbait"],
            path="annotated/csv",
        ),
        IdClickbaitConfig(name="raw", version=VERSION, description="Raw dataset", path="raw/csv"),
    ]

    BUILDER_CONFIG_CLASS = IdClickbaitConfig

    def _info(self):
        if self.config.name == "annotated":
            features = datasets.Features(
                {
                    "id": datasets.Value("string"),
                    "title": datasets.Value("string"),
                    "label": datasets.features.ClassLabel(names=self.config.label_classes),
                }
            )
        else:
            features = datasets.Features(
                {
                    "id": datasets.Value("string"),
                    "title": datasets.Value("string"),
                    "source": datasets.Value("string"),
                    "date": datasets.Value("string"),
                    "category": datasets.Value("string"),
                    "sub-category": datasets.Value("string"),
                    "content": datasets.Value("string"),
                    "url": datasets.Value("string"),
                }
            )
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=features,
            supervised_keys=None,
            homepage=_HOMEPAGE,
            license=_LICENSE,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        my_urls = _URLs[0]
        data_dir = dl_manager.download_and_extract(my_urls)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={
                    "article_dir": os.path.join(data_dir, self.config.path),
                    "split": "train",
                },
            )
        ]

    def _generate_examples(self, article_dir, split):
        logger.info("⏳ Generating %s examples from = %s", split, article_dir)
        id = 0
        for path in sorted(glob.glob(os.path.join(article_dir, "**/*.csv"), recursive=True)):
            with open(path, encoding="utf-8-sig", newline="") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if self.config.name == "annotated":
                        yield id, {
                            "id": str(id),
                            "title": row["title"],
                            "label": row["label"],
                        }
                    else:
                        yield id, {
                            "id": str(id),
                            "title": row["title"],
                            "source": row["source"],
                            "date": row["date"],
                            "category": row["category"],
                            "sub-category": row["sub-category"],
                            "content": row["content"],
                            "url": row["url"],
                        }
                    id += 1
