# coding=utf-8
# Copyright 2021 The HuggingFace Datasets Authors and the current dataset script contributor.
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
"""RO-STS-Parallel: a Parallel English-Romanian Dataset by translating the Semantic Textual Similarity dataset"""


import datasets


# Find for instance the citation on arxiv or on the dataset repo/website
_CITATION = """\
Article under review
"""

# You can copy an official description
_DESCRIPTION = """\
The RO-STS-Parallel (a Parallel Romanian English dataset - translation of the Semantic Textual Similarity) contains 17256 sentences in Romanian and English. It is a high-quality translation of the English STS benchmark dataset into Romanian.
"""

_HOMEPAGE = "https://github.com/dumitrescustefan/RO-STS"

_LICENSE = "CC BY-SA 4.0 License"

# The HuggingFace dataset library don't host the datasets but only point to the original files
# This can be an arbitrary nested dict/list of URLs (see below in `_split_generators` method)
_URL = "https://github.com/dumitrescustefan/RO-STS/tree/master/dataset/ro-en"
# _TRAINING_FILE_RO = "RO-STS.train.ro"
# _TRAINING_FILE_EN = "RO-STS.train.en"
# _TEST_FILE_RO = "RO-STS.test.ro"
# _TEST_FILE_EN = "RO-STS.test.en"
# _DEV_FILE_RO = "RO-STS.dev.ro"
# _DEV_FILE_EN = "RO-STS.dev.en"
_DATA_URL = "https://raw.githubusercontent.com/dumitrescustefan/RO-STS/master/dataset/ro-en/RO-STS.{}.{}"


class ROSTSParallelConfig(datasets.BuilderConfig):
    """BuilderConfig for RO-STS-Parallel dataset"""

    def __init__(self, language_pair=(None, None), **kwargs):

        # description = ("RO-STS Parallel dataset, translation from %s to %s") % (language_pair[0], language_pair[1])
        super(ROSTSParallelConfig, self).__init__(**kwargs)
        self.language_pair = language_pair


class RoStsParallel(datasets.GeneratorBasedBuilder):
    """RO-STS-Parallel dataset"""

    VERSION = datasets.Version("1.0.0")
    BUILDER_CONFIGS = [
        ROSTSParallelConfig(
            name="ro_sts_parallel", version=VERSION, description="RO-STS Parallel dataset", language_pair=("ro", "en")
        )
    ]

    def _info(self):

        source, target = self.config.language_pair
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {"translation": datasets.features.Translation(languages=self.config.language_pair)}
            ),
            supervised_keys=(source, target),
            homepage=_HOMEPAGE,
            license=_LICENSE,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""

        source, target = self.config.language_pair

        files = {}
        for split in ("train", "dev", "test"):
            if split == "train":
                dl_dir_src = dl_manager.download_and_extract(_DATA_URL.format("train", source))
                dl_dir_tar = dl_manager.download_and_extract(_DATA_URL.format("train", target))
            if split == "dev":
                dl_dir_src = dl_manager.download_and_extract(_DATA_URL.format("dev", source))
                dl_dir_tar = dl_manager.download_and_extract(_DATA_URL.format("dev", target))
            if split == "test":
                dl_dir_src = dl_manager.download_and_extract(_DATA_URL.format("test", source))
                dl_dir_tar = dl_manager.download_and_extract(_DATA_URL.format("test", target))

            files[split] = {"source_file": dl_dir_src, "target_file": dl_dir_tar}

        return [
            datasets.SplitGenerator(name=datasets.Split.TRAIN, gen_kwargs=files["train"]),
            datasets.SplitGenerator(name=datasets.Split.VALIDATION, gen_kwargs=files["dev"]),
            datasets.SplitGenerator(name=datasets.Split.TEST, gen_kwargs=files["test"]),
        ]

    def _generate_examples(self, source_file, target_file):
        """This function returns the examples in the raw (text) form."""
        with open(source_file, encoding="utf-8") as f:
            source_sentences = f.read().split("\n")
        with open(target_file, encoding="utf-8") as f:
            target_sentences = f.read().split("\n")

        source, target = self.config.language_pair
        for idx, (l1, l2) in enumerate(zip(source_sentences, target_sentences)):
            result = {"translation": {source: l1, target: l2}}
            yield idx, result
