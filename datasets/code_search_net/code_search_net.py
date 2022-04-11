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

# Lint as: python3
"""CodeSearchNet corpus: proxy dataset for semantic code search"""

# TODO: add licensing info in the examples
# TODO: log richer informations (especially while extracting the jsonl.gz files)
# TODO: enable custom configs; such as: "java+python"
# TODO: enable fetching examples with a given license, eg: "java_MIT"


import json
import os

import datasets


_CITATION = """\
@article{husain2019codesearchnet,
    title={{CodeSearchNet} challenge: Evaluating the state of semantic code search},
    author={Husain, Hamel and Wu, Ho-Hsiang and Gazit, Tiferet and Allamanis, Miltiadis and Brockschmidt, Marc},
    journal={arXiv preprint arXiv:1909.09436},
    year={2019}
}
"""

_DESCRIPTION = """\
CodeSearchNet corpus contains about 6 million functions from open-source code \
spanning six programming languages (Go, Java, JavaScript, PHP, Python, and Ruby). \
The CodeSearchNet Corpus also contains automatically generated query-like \
natural language for 2 million functions, obtained from mechanically scraping \
and preprocessing associated function documentation.
"""

_HOMEPAGE = "https://github.com/github/CodeSearchNet"

_LICENSE = "Various"

_S3_BUCKET_URL = "https://s3.amazonaws.com/code-search-net/CodeSearchNet/v2/"
_AVAILABLE_LANGUAGES = ["python", "java", "javascript", "go", "ruby", "php"]
_URLs = {language: _S3_BUCKET_URL + f"{language}.zip" for language in _AVAILABLE_LANGUAGES}
# URLs for "all" are just the concatenation of URLs for all languages
_URLs["all"] = _URLs.copy()


class CodeSearchNet(datasets.GeneratorBasedBuilder):
    """ "CodeSearchNet corpus: proxy dataset for semantic code search."""

    VERSION = datasets.Version("1.0.0", "Add CodeSearchNet corpus dataset")
    BUILDER_CONFIGS = [
        datasets.BuilderConfig(
            name="all",
            version=VERSION,
            description="All available languages: Java, Go, Javascript, Python, PHP, Ruby",
        ),
        datasets.BuilderConfig(
            name="java",
            version=VERSION,
            description="Java language",
        ),
        datasets.BuilderConfig(
            name="go",
            version=VERSION,
            description="Go language",
        ),
        datasets.BuilderConfig(
            name="python",
            version=VERSION,
            description="Pyhton language",
        ),
        datasets.BuilderConfig(
            name="javascript",
            version=VERSION,
            description="Javascript language",
        ),
        datasets.BuilderConfig(
            name="ruby",
            version=VERSION,
            description="Ruby language",
        ),
        datasets.BuilderConfig(
            name="php",
            version=VERSION,
            description="PHP language",
        ),
    ]

    DEFAULT_CONFIG_NAME = "all"

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "repository_name": datasets.Value("string"),
                    "func_path_in_repository": datasets.Value("string"),
                    "func_name": datasets.Value("string"),
                    "whole_func_string": datasets.Value("string"),
                    "language": datasets.Value("string"),
                    "func_code_string": datasets.Value("string"),
                    "func_code_tokens": datasets.Sequence(datasets.Value("string")),
                    "func_documentation_string": datasets.Value("string"),
                    "func_documentation_tokens": datasets.Sequence(datasets.Value("string")),
                    "split_name": datasets.Value("string"),
                    "func_code_url": datasets.Value("string"),
                    # TODO - add licensing info in the examples
                }
            ),
            # No default supervised keys
            supervised_keys=None,
            homepage=_HOMEPAGE,
            license=_LICENSE,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators.

        Note: The original data is stored in S3, and follows this unusual directory structure:
            ```
            .
            ├── <language_name>  # e.g. python
            │   └── final
            │       └── jsonl
            │           ├── test
            │           │   └── <language_name>_test_0.jsonl.gz
            │           ├── train
            │           │   ├── <language_name>_train_0.jsonl.gz
            │           │   ├── <language_name>_train_1.jsonl.gz
            │           │   ├── ...
            │           │   └── <language_name>_train_n.jsonl.gz
            │           └── valid
            │               └── <language_name>_valid_0.jsonl.gz
            ├── <language_name>_dedupe_definitions_v2.pkl
            └── <language_name>_licenses.pkl
            ```
        """
        data_urls = _URLs[self.config.name]
        if isinstance(data_urls, str):
            data_urls = {self.config.name: data_urls}
        # Download & extract the language archives
        data_dirs = [
            os.path.join(directory, lang, "final", "jsonl")
            for lang, directory in dl_manager.download_and_extract(data_urls).items()
        ]

        split2dirs = {
            split_name: [os.path.join(directory, split_name) for directory in data_dirs]
            for split_name in ["train", "test", "valid"]
        }

        split2paths = dl_manager.extract(
            {
                split_name: [
                    os.path.join(directory, entry_name)
                    for directory in split_dirs
                    for entry_name in os.listdir(directory)
                ]
                for split_name, split_dirs in split2dirs.items()
            }
        )

        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={
                    "filepaths": split2paths["train"],
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                gen_kwargs={
                    "filepaths": split2paths["test"],
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                gen_kwargs={
                    "filepaths": split2paths["valid"],
                },
            ),
        ]

    def _generate_examples(self, filepaths):
        """Yields the examples by iterating through the available jsonl files."""
        for file_id_, filepath in enumerate(filepaths):
            with open(filepath, encoding="utf-8") as f:
                for row_id_, row in enumerate(f):
                    # Key of the example = file_id + row_id,
                    # to ensure all examples have a distinct key
                    id_ = f"{file_id_}_{row_id_}"
                    data = json.loads(row)
                    yield id_, {
                        "repository_name": data["repo"],
                        "func_path_in_repository": data["path"],
                        "func_name": data["func_name"],
                        "whole_func_string": data["original_string"],
                        "language": data["language"],
                        "func_code_string": data["code"],
                        "func_code_tokens": data["code_tokens"],
                        "func_documentation_string": data["docstring"],
                        "func_documentation_tokens": data["docstring_tokens"],
                        "split_name": data["partition"],
                        "func_code_url": data["url"],
                    }
