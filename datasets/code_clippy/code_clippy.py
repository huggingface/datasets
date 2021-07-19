# coding=utf-8
# Copyright 2020 The HuggingFace Datasets Authors and the CodeClippy team
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
"""
CodeClippy dataset - opensource code from Github. Scrapped July 7 2021.
More to add here.
"""

import os
import io
from typing import List
import jsonlines
import zstandard as zstd
from pathlib import Path

import datasets


# TODO: Add BibTeX citation
# Find for instance the citation on arxiv or on the dataset repo/website
_CITATION = """\
@InProceedings{huggingface:dataset,
title = {Code Clippy},
author={CodeClippy team and all the opensource devs around the globe
},
year={2021}
}
"""

_DESCRIPTION = """
CodeClippy dataset - opensource code from Github. Scrapped July 7 2021.
"""

# TODO: Add a link to an official homepage for the dataset here
_HOMEPAGE = ""

# TODO: Add the licence for the dataset here if you can find it
_LICENSE = ""

# TODO: Add link to the official dataset URLs here (once we have those)
# The HuggingFace dataset library don't host the datasets but only point to the original files
# This can be an arbitrary nested dict/list of URLs (see below in `_split_generators` method)
_URLs = {
    "https://huggingface.co/great-new-dataset-first_domain.zip",
}

class CodeClippy(datasets.GeneratorBasedBuilder):
    """CodeClippy dataset - opensource code from Github. Scrapped July 7 2021."""

    VERSION = datasets.Version("0.1.0")

    # This is an example of a dataset with multiple configurations.
    # If you don't want/need to define several sub-sets in your dataset,
    # just remove the BUILDER_CONFIG_CLASS and the BUILDER_CONFIGS attributes.

    # If you need to make complex sub-parts in the datasets with configurable options
    # You can create your own builder configuration class to store attribute, inheriting from datasets.BuilderConfig
    # BUILDER_CONFIG_CLASS = MyBuilderConfig

    # You will be able to load one or the other configurations in the following list with
    # data = datasets.load_dataset('my_dataset', 'first_domain')
    # data = datasets.load_dataset('my_dataset', 'second_domain')
    # BUILDER_CONFIGS = [
    #     datasets.BuilderConfig(name="first_domain", version=VERSION, description="This part of my dataset covers a first domain"),
    #     datasets.BuilderConfig(name="second_domain", version=VERSION, description="This part of my dataset covers a second domain"),
    # ]

    # DEFAULT_CONFIG_NAME = "first_domain"

    def _info(self):
        features = datasets.Features(
                {
                    "id": datasets.Value("int64"),
                    "text": datasets.Value("string"),
                    "repo_name": datasets.Value("string"),
                    "stars": datasets.Value("string"),
                    "repo_language": datasets.Value("string"),
                    "file_name": datasets.Value("string"),
                    "mime_type": datasets.Value("string")
                }
                )
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=features,
            homepage= _HOMEPAGE,
            license=_LICENSE
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        # dl_manager is a datasets.download.DownloadManager that can be used to download and extract URLs
        # It can accept any type or nested list/dict and will give back the same structure with the url replaced with path to local files.
        # By default the archives will be extracted and a path to a cached folder where they are extracted is returned instead of the archive
        
        #TODO(high priority): changes this to load from the-eye
        # data_dir = dl_manager.download_and_extract(_URLs)
        data_dir = self.config.data_dir
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={"filepaths": sorted([str(fp) for fp in Path(f"{data_dir}/train").glob("*.jsonl.zst")])}
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                gen_kwargs={"filepaths": sorted([str(fp) for fp in Path(f"{data_dir}/test").glob("*.jsonl.zst")])}
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                gen_kwargs={"filepaths": sorted([str(fp) for fp in Path(f"{data_dir}/validation").glob("*.jsonl.zst")])}
            ),
        ]

    def _generate_examples(self, filepaths:List):
        """ Yields examples as (key, example) tuples. """
        id_ = 0
        dctx = zstd.ZstdDecompressor()
        for filepath in filepaths:
            with open(filepath, "rb") as f:
                f = dctx.stream_reader(f)
                f = io.TextIOWrapper(f, encoding="utf-8")
                f = jsonlines.Reader(f)
                for line in f:
                    yield id_, {"id": id_, "text": line["text"], **line["meta"]}
                    id_ += 1