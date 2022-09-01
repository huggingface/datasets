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

import os

import datasets


_CITATION = ""

# You can copy an official description
_DESCRIPTION = """\
The dataset is based on the Hutter Prize (http://prize.hutter1.net) and contains the first 10^8 byte of Wikipedia
"""

_HOMEPAGE = "https://cs.fit.edu/~mmahoney/compression/textdata.html"

_LICENSE = ""

# The HuggingFace Datasets library doesn't host the datasets but only points to the original files.
# This can be an arbitrary nested dict/list of URLs (see below in `_split_generators` method)
_URLS = {"source": "http://cs.fit.edu/~mmahoney/compression/enwik8.zip"}


class Enwik8(datasets.GeneratorBasedBuilder):

    VERSION = datasets.Version("1.1.0")

    BUILDER_CONFIGS = [
        datasets.BuilderConfig(
            name="enwik8",
            version=VERSION,
            description="This version of the dataset contains a split by line version with all content",
        ),
        datasets.BuilderConfig(
            name="enwik8-raw",
            version=VERSION,
            description="This version of the dataset contains a raw string version split with all content",
        ),
    ]

    DEFAULT_CONFIG_NAME = "enwik8"

    def _info(self):

        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "text": datasets.Value("string"),
                }
            ),
            homepage=_HOMEPAGE,
            license=_LICENSE,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):

        urls = _URLS["source"]
        data_dir = dl_manager.download_and_extract(urls)

        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={
                    "filepath": os.path.join(data_dir, "enwik8"),
                    "split": "train",
                },
            )
        ]

    # method parameters are unpacked from `gen_kwargs` as given in `_split_generators`
    def _generate_examples(self, filepath, split):
        with open(filepath, encoding="utf-8") as f:
            if self.config.name.endswith("raw"):
                yield 0, {"text": f.read()}
            else:
                for key, line in enumerate(f):
                    yield key, {"text": line.strip()}
