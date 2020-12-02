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
"""TODO: Code refinement aims to automatically fix bugs in the code,
 which can contribute to reducing the cost of bug-fixes for developers."""

from __future__ import absolute_import, division, print_function


import datasets


# TODO: Add BibTeX citation
# Find for instance the citation on arxiv or on the dataset repo/website
_CITATION = """\
@article{CodeXGLUE,
  title={CodeXGLUE: A Benchmark Dataset and Open Challenge for Code Intelligence},
  year={2020},
}
"""

# TODO: Add description of the dataset here
# You can copy an official description
_DESCRIPTION = """\
Millions of open-source projects with numerous bug fixes
are available in code repositories. This proliferation
of software development histories can be leveraged to
learn how to fix common programming bugs
Code refinement aims to automatically fix bugs in the code,
which can contribute to reducing the cost of bug-fixes for developers.
Given a piece of Java code with bugs,
the task is to remove the bugs to output the refined code. """
# TODO: Add the licence for the dataset here if you can find it
_LICENSE = "MIT License"

# TODO: Add link to the official dataset URLs here
# The HuggingFace dataset library don't host the datasets but only point to the original files
# This can be an arbitrary nested dict/list of URLs (see below in `_split_generators` method)
_URLs = {
    "code_refinement_small": {
        "train_fix": "https://raw.githubusercontent.com/microsoft/CodeXGLUE/main/Code-Code/code-refinement/data/small/train.buggy-fixed.fixed",
        "valid_fix": "https://raw.githubusercontent.com/microsoft/CodeXGLUE/main/Code-Code/code-refinement/data/small/valid.buggy-fixed.fixed",
        "test_fix": "https://raw.githubusercontent.com/microsoft/CodeXGLUE/main/Code-Code/code-refinement/data/small/test.buggy-fixed.fixed",
        "train_bug": "https://raw.githubusercontent.com/microsoft/CodeXGLUE/main/Code-Code/code-refinement/data/small/train.buggy-fixed.buggy",
        "valid_bug": "https://raw.githubusercontent.com/microsoft/CodeXGLUE/main/Code-Code/code-refinement/data/small/valid.buggy-fixed.buggy",
        "test_bug": "https://raw.githubusercontent.com/microsoft/CodeXGLUE/main/Code-Code/code-refinement/data/small/test.buggy-fixed.buggy",
    },
    "code_refinement_medium": {
        "train_fix": "https://raw.githubusercontent.com/microsoft/CodeXGLUE/main/Code-Code/code-refinement/data/medium/train.buggy-fixed.fixed",
        "valid_fix": "https://raw.githubusercontent.com/microsoft/CodeXGLUE/main/Code-Code/code-refinement/data/medium/valid.buggy-fixed.fixed",
        "test_fix": "https://raw.githubusercontent.com/microsoft/CodeXGLUE/main/Code-Code/code-refinement/data/medium/test.buggy-fixed.fixed",
        "train_bug": "https://raw.githubusercontent.com/microsoft/CodeXGLUE/main/Code-Code/code-refinement/data/medium/train.buggy-fixed.buggy",
        "valid_bug": "https://raw.githubusercontent.com/microsoft/CodeXGLUE/main/Code-Code/code-refinement/data/medium/valid.buggy-fixed.buggy",
        "test_bug": "https://raw.githubusercontent.com/microsoft/CodeXGLUE/main/Code-Code/code-refinement/data/medium/test.buggy-fixed.buggy",
    },
}


# TODO: Name of the dataset usually match the script name with CamelCase instead of snake_case
class Code_Refinement(datasets.GeneratorBasedBuilder):
    """TODO: Short description of my dataset."""

    VERSION = datasets.Version("1.1.0")

    # This is an example of a dataset with multiple configurations.
    # If you don't want/need to define several sub-sets in your dataset,
    # just remove the BUILDER_CONFIG_CLASS and the BUILDER_CONFIGS attributes.

    # If you need to make complex sub-parts in the datasets with configurable options
    # You can create your own builder configuration class to store attribute, inheriting from datasets.BuilderConfig
    # BUILDER_CONFIG_CLASS = MyBuilderConfig

    # You will be able to load one or the other configurations in the following list with
    # data = datasets.load_dataset('my_dataset', 'first_domain')
    # data = datasets.load_dataset('my_dataset', 'second_domain')
    BUILDER_CONFIGS = [
        datasets.BuilderConfig(
            name="code_refinement_small",
            description="small version of the code_refinement dataset",
        ),
        datasets.BuilderConfig(
            name="code_refinement_medium",
            description="medium version of the code_refinement dataset",
        ),
    ]

    DEFAULT_CONFIG_NAME = "code_refinement_small"  # It's not mandatory to have a default configuration. Just use one if it make sense.

    def _info(self):
        # TODO: This method pecifies the datasets.DatasetInfo object which contains informations and typings for the dataset
        if (
            self.config.name == "code_refinement_small"
        ):  # This is the name of the configuration selected in BUILDER_CONFIGS above
            features = datasets.Features(
                {
                    "bug": datasets.Value("string"),
                    "fix": datasets.Value("string"),
                }
            )
        else:  # This is an example to show how to have different features for "first_domain" and "second_domain"
            features = datasets.Features(
                {
                    "bug": datasets.Value("string"),
                    "fix": datasets.Value("string"),
                }
            )
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=features,  # Here we define them above because they are different between the two configurations
            supervised_keys=["code", "ml4code"],
            # Homepage of the dataset for documentation
            homepage="https://github.com/microsoft/CodeXGLUE",
            # License for the dataset if available
            license=_LICENSE,
            # Citation for the dataset
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        # TODO: This method is tasked with downloading/extracting the data and defining the splits depending on the configuration
        # If several configurations are possible (listed in BUILDER_CONFIGS), the configuration selected by the user is in self.config.name

        # dl_manager is a datasets.download.DownloadManager that can be used to download and extract URLs
        # It can accept any type or nested list/dict and will give back the same structure with the url replaced with path to local files.
        # By default the archives will be extracted and a path to a cached folder where they are extracted is returned instead of the archive
        my_urls = _URLs[self.config.name]
        dl_path = dl_manager.download(my_urls)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={
                    "filename": [dl_path["train_bug"], dl_path["train_fix"]],
                    "split": "train",
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                gen_kwargs={
                    "filename": [dl_path["valid_bug"], dl_path["valid_fix"]],
                    "split": "validation",
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                gen_kwargs={
                    "filename": [dl_path["test_bug"], dl_path["test_fix"]],
                    "split": "test",
                },
            ),
        ]

    def _generate_examples(self, filename, split):
        """ Yields examples. """
        # TODO: This method will receive as arguments the `gen_kwargs` defined in the previous `_split_generators` method.
        # It is in charge of opening the given file and yielding (key, example) tuples from the dataset
        # The key is not important, it's more here for legacy reason (legacy from tfds)
        fix_file = filename[1]
        bug_file = filename[0]
        id_ = 0
        with open(fix_file, encoding="utf-8") as fix_f, open(
            bug_file, encoding="utf-8"
        ) as bug_f:
            for fix, bug in zip(fix_f, bug_f):
                yield id_, {
                    "bug": bug,
                    "fix": fix,
                }
