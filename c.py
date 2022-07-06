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

# Special thanks to @lvwerra -- we reference his repository here: https://huggingface.co/datasets/lvwerra/github-code/
"""Code Clippy Github Code dataset."""

import os


import datasets
from huggingface_hub import HfApi, HfFolder
from datasets.data_files import DataFilesDict

import gzip
import json

_REPO_NAME = "CodedotAI/code_clippy_github"

_LANG_TO_EXTENSION = {
    "C": [".c"],
    "C#": [".cs"],
    "C++": [".cpp"],
    "CSS": [".css"],
    "Dart" : [".dart"],
    "GO": [".go"],
    "HTML":[".html"],
    "Java": [".java"],
    "JavaScript": [".js"],
    "Jupyter Notebooks (Python)": [".ipynb"],
    "Kotlin" : [".kt"],
    "Lisp" : [".lisp"],
    "Matlab" : [".m"],
    "PHP": [".php"],
    "Perl": [".pl"],
    "Python": [".py"],
    "R" : [".r"],
    "Ruby": [".rb"],
    "Rust": [".rs"],
    "SQL": [".sql"],
    "Shell": [".sh"],
    "Swift" : [".swift"],
    "TypeScript": [".ts"],
}

_LICENSES = [
    'mit',
    'apache-2.0',
    'gpl-2.0',
    'gpl-3.0',
    'bsd-3-clause',
    'bsd-2-clause',
    'unlicense',
    'apacheagpl-3.0',
    'lgpl-3.0',
    'cc0-1.0',
    'epl-1.0',
    'lgpl-2.1',
    'mpl-2.0',
    'isc',
    'artistic-2.0'
 ]

_DESCRIPTION = """\
The Code Clippy dataset consists of various public codebases from GitHub in 22 programming languages with 23 extensions \
    totalling about 16 TB of data when uncompressed. The dataset was created from the public GitHub dataset on Google BiqQuery.
"""

_HOMEPAGE = "https://cloud.google.com/blog/topics/public-datasets/github-on-bigquery-analyze-all-the-open-source-code/"


_EXTENSION_TO_LANG = {}
for lang in _LANG_TO_EXTENSION:
    for extension in _LANG_TO_EXTENSION[lang]:
        _EXTENSION_TO_LANG[extension] = lang


        
_LANG_CONFIGS = ["all"] + list(_LANG_TO_EXTENSION.keys())
_LICENSE_CONFIGS = ["all"] + _LICENSES
        
class CodeClippyGithubConfig(datasets.BuilderConfig):
    """BuilderConfig for the Code Clippy Github dataset."""

    def __init__(self, *args, languages=["all"], licenses=["all"], **kwargs):
        """BuilderConfig for the Code Clippy Github dataset.
        Args:
            languages (:obj:`List[str]`): List of languages to load.
            licenses (:obj:`List[str]`): List of licenses to load.
            **kwargs: keyword arguments forwarded to super.
        """
        super().__init__(
            *args,
            name="+".join(languages)+"-"+"+".join(licenses),
            **kwargs,
        )
        
        languages = set(languages)
        licenses = set(licenses)
        
        assert all([language in _LANG_CONFIGS for language in languages]), f"Language not in {_LANG_CONFIGS}."
        assert all([license in _LICENSE_CONFIGS for license in licenses]), f"License not in {_LICENSE_CONFIGS}."
        
        if "all" in languages:
            assert len(languages)==1, "Passed 'all' together with other languages."
            self.filter_languages = False
        else:
            self.filter_languages = True
            
        if "all" in licenses:
            assert len(licenses)==1, "Passed 'all' together with other licenses."
            self.filter_licenses = False
        else:
            self.filter_licenses = True
        
        self.languages = set(languages)
        self.licenses = set(licenses)


        
class CodeClippyGithub(datasets.GeneratorBasedBuilder):
    """Code Clippy Github dataset."""

    VERSION = datasets.Version("1.0.0")
    
    BUILDER_CONFIG_CLASS = CodeClippyGithubConfig
    BUILDER_CONFIGS = [CodeClippyGithubConfig(languages=[lang], licenses=[license]) for lang in _LANG_CONFIGS
                                                                        for license in _LICENSE_CONFIGS]
    DEFAULT_CONFIG_NAME = "all-all"
    
    
    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features({"code_text": datasets.Value("string"),
                                        "repo_name": datasets.Value("string"),
                                        "file_path": datasets.Value("string"), 
                                        "language": datasets.Value("string"),
                                        "license": datasets.Value("string"),
                                        "size": datasets.Value("int32")}),
            supervised_keys=None,
            homepage=_HOMEPAGE,
            license="Multiple: see the 'license' field of each sample.",
            
        )

    def _split_generators(self, dl_manager):
        
        hfh_dataset_info = HfApi(datasets.config.HF_ENDPOINT).dataset_info(
            _REPO_NAME,
            timeout=100.0,
        )

        patterns = datasets.data_files.get_patterns_in_dataset_repository(hfh_dataset_info)
        data_files = datasets.data_files.DataFilesDict.from_hf_repo(
            patterns,
            dataset_info=hfh_dataset_info,
        )

        files = dl_manager.download_and_extract(data_files["train"])
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={
                    "files": files,
                },
            ),
        ]

    def _generate_examples(self, files):
        key = 0
        for file_idx, file in enumerate(files):
            with gzip.open(file, "rb") as f:
                
                uncompressed_data = f.readlines()
                
                for batch_idx, code_base in enumerate(uncompressed_data):
                    j_dict = json.loads(code_base.decode('utf-8'))
                   
                   
                        
                    lang = lang_from_name(j_dict['path'])
                    license = j_dict["license"]
                    
                    if self.config.filter_languages and not lang in self.config.languages:
                        continue
                    if self.config.filter_licenses and not license in self.config.licenses:
                        continue
                    # TODO: Add more features like header comments, filename, and other features useful in a prompt.
                    yield key, {"code_text": j_dict['content'],
                                "repo_name": j_dict['repo_name'],
                                "file_path": j_dict['path'],
                                "license": license,
                                "language": lang,
                                "size": int(j_dict['f0_'])}    
                    key += 1

                        
def lang_from_name(name):
    for extension in _EXTENSION_TO_LANG:
        if name.endswith(extension):
            return _EXTENSION_TO_LANG[extension]