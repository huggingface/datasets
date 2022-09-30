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
"""IWSLT 2017 dataset """


import os

import datasets


_HOMEPAGE = "https://sites.google.com/site/iwsltevaluation2017/TED-tasks"

_DESCRIPTION = """\
The IWSLT 2017 Multilingual Task addresses text translation, including zero-shot translation, with a single MT system across all directions including English, German, Dutch, Italian and Romanian. As unofficial task, conventional bilingual text translation is offered between English and Arabic, French, Japanese, Chinese, German and Korean.
"""

_CITATION = """\
@inproceedings{cettolo-etal-2017-overview,
    title = "Overview of the {IWSLT} 2017 Evaluation Campaign",
    author = {Cettolo, Mauro  and
      Federico, Marcello  and
      Bentivogli, Luisa  and
      Niehues, Jan  and
      St{\\"u}ker, Sebastian  and
      Sudoh, Katsuhito  and
      Yoshino, Koichiro  and
      Federmann, Christian},
    booktitle = "Proceedings of the 14th International Conference on Spoken Language Translation",
    month = dec # " 14-15",
    year = "2017",
    address = "Tokyo, Japan",
    publisher = "International Workshop on Spoken Language Translation",
    url = "https://aclanthology.org/2017.iwslt-1.1",
    pages = "2--14",
}
"""

REPO_URL = "https://huggingface.co/datasets/iwslt2017/resolve/main/"
MULTI_URL = REPO_URL + "data/2017-01-trnmted/texts/DeEnItNlRo/DeEnItNlRo/DeEnItNlRo-DeEnItNlRo.zip"
BI_URL = REPO_URL + "data/2017-01-trnted/texts/{source}/{target}/{source}-{target}.zip"


class IWSLT2017Config(datasets.BuilderConfig):
    """BuilderConfig for NewDataset"""

    def __init__(self, pair, is_multilingual, **kwargs):
        """

        Args:
            pair: the language pair to consider
            is_multilingual: Is this pair in the multilingual dataset (download source is different)
            **kwargs: keyword arguments forwarded to super.
        """
        self.pair = pair
        self.is_multilingual = is_multilingual
        super().__init__(**kwargs)


# XXX: Artificially removed DE from here, as it also exists within bilingual data
MULTI_LANGUAGES = ["en", "it", "nl", "ro"]
BI_LANGUAGES = ["ar", "de", "en", "fr", "ja", "ko", "zh"]
MULTI_PAIRS = [f"{source}-{target}" for source in MULTI_LANGUAGES for target in MULTI_LANGUAGES if source != target]
BI_PAIRS = [
    f"{source}-{target}"
    for source in BI_LANGUAGES
    for target in BI_LANGUAGES
    if source != target and (source == "en" or target == "en")
]

PAIRS = MULTI_PAIRS + BI_PAIRS


class IWSLT217(datasets.GeneratorBasedBuilder):
    """The IWSLT 2017 Evaluation Campaign includes a multilingual TED Talks MT task."""

    VERSION = datasets.Version("1.0.0")

    # This is an example of a dataset with multiple configurations.
    # If you don't want/need to define several sub-sets in your dataset,
    # just remove the BUILDER_CONFIG_CLASS and the BUILDER_CONFIGS attributes.
    BUILDER_CONFIG_CLASS = IWSLT2017Config
    BUILDER_CONFIGS = [
        IWSLT2017Config(
            name="iwslt2017-" + pair,
            description="A small dataset",
            version=datasets.Version("1.0.0"),
            pair=pair,
            is_multilingual=pair in MULTI_PAIRS,
        )
        for pair in PAIRS
    ]

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {"translation": datasets.features.Translation(languages=self.config.pair.split("-"))}
            ),
            homepage=_HOMEPAGE,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        source, target = self.config.pair.split("-")
        if self.config.is_multilingual:
            dl_dir = dl_manager.download_and_extract(MULTI_URL)
            data_dir = os.path.join(dl_dir, "DeEnItNlRo-DeEnItNlRo")
            years = [2010]
        else:
            bi_url = BI_URL.format(source=source, target=target)
            dl_dir = dl_manager.download_and_extract(bi_url)
            data_dir = os.path.join(dl_dir, f"{source}-{target}")
            years = [2010, 2011, 2012, 2013, 2014, 2015]
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={
                    "source_files": [
                        os.path.join(
                            data_dir,
                            f"train.tags.{self.config.pair}.{source}",
                        )
                    ],
                    "target_files": [
                        os.path.join(
                            data_dir,
                            f"train.tags.{self.config.pair}.{target}",
                        )
                    ],
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                gen_kwargs={
                    "source_files": [
                        os.path.join(
                            data_dir,
                            f"IWSLT17.TED.tst{year}.{self.config.pair}.{source}.xml",
                        )
                        for year in years
                    ],
                    "target_files": [
                        os.path.join(
                            data_dir,
                            f"IWSLT17.TED.tst{year}.{self.config.pair}.{target}.xml",
                        )
                        for year in years
                    ],
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                gen_kwargs={
                    "source_files": [
                        os.path.join(
                            data_dir,
                            f"IWSLT17.TED.dev2010.{self.config.pair}.{source}.xml",
                        )
                    ],
                    "target_files": [
                        os.path.join(
                            data_dir,
                            f"IWSLT17.TED.dev2010.{self.config.pair}.{target}.xml",
                        )
                    ],
                },
            ),
        ]

    def _generate_examples(self, source_files, target_files):
        """Yields examples."""
        id_ = 0
        source, target = self.config.pair.split("-")
        for source_file, target_file in zip(source_files, target_files):
            with open(source_file, "r", encoding="utf-8") as sf:
                with open(target_file, "r", encoding="utf-8") as tf:
                    for source_row, target_row in zip(sf, tf):
                        source_row = source_row.strip()
                        target_row = target_row.strip()

                        if source_row.startswith("<"):
                            if source_row.startswith("<seg"):
                                # Remove <seg id="1">.....</seg>
                                # Very simple code instead of regex or xml parsing
                                part1 = source_row.split(">")[1]
                                source_row = part1.split("<")[0]
                                part1 = target_row.split(">")[1]
                                target_row = part1.split("<")[0]

                                source_row = source_row.strip()
                                target_row = target_row.strip()
                            else:
                                continue

                        yield id_, {"translation": {source: source_row, target: target_row}}
                        id_ += 1
