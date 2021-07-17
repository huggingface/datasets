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
APPS dataset.
"""

import os
import io
from typing import List
import json
from pathlib import Path

import datasets


# TODO: Add BibTeX citation
# Find for instance the citation on arxiv or on the dataset repo/website
_CITATION = """\
@article{hendrycksapps2021,
  title={Measuring Coding Challenge Competence With APPS},
  author={Dan Hendrycks and Steven Basart and Saurav Kadavath and Mantas Mazeika and Akul Arora and Ethan Guo and Collin Burns and Samir Puranik and Horace He and Dawn Song and Jacob Steinhardt},
  journal={arXiv preprint arXiv:2105.09938},
  year={2021}
}
"""

_DESCRIPTION = """
APPs dataset
"""

# TODO: Add a link to an official homepage for the dataset here
_HOMEPAGE = "https://github.com/hendrycks/apps"

# TODO: Add the licence for the dataset here if you can find it
_LICENSE = "MIT License"

# TODO: Add link to the official dataset URLs here (once we have those)
# The HuggingFace dataset library don't host the datasets but only point to the original files
# This can be an arbitrary nested dict/list of URLs (see below in `_split_generators` method)
_URLs = [
    "https://people.eecs.berkeley.edu/~hendrycks/APPS.tar.gz",
]

class APPS(datasets.GeneratorBasedBuilder):
    """APPS dataset"""

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
                    "question": datasets.Value("string"),
                    "answer": datasets.Value("string"),
                    "starter_code": datasets.Value("string"),
                    "answer_type": datasets.Value("string"),
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
        
        data_dir = dl_manager.download_and_extract(_URLs[0])
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={"problem_dirs": sorted([p_dir[0] for p_dir in os.walk(f"{data_dir}/APPS/train")])}
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                gen_kwargs={"problem_dirs": sorted([p_dir[0] for p_dir in os.walk(f"{data_dir}/APPS/test")])}
            ),
        ]

    def _generate_examples(self, problem_dirs:List):
        """ Yields examples as (key, example) tuples. """
        id_ = 0
        skipped_problems = []
        for problem in problem_dirs:
            question_fname = os.path.join(problem, "question.txt")
            sols_fname = os.path.join(problem, "solutions.json")
            starter_code = os.path.join(problem, "starter_code.py")

            # print(question_fname)

            if os.path.exists(starter_code):
                answer_type = "\nUse Call-Based format\n"
            else:
                answer_type = "\nUse Standard Input format\n"

            if (not os.path.isfile(question_fname)) or (not os.path.isfile(sols_fname)):
                skipped_problems.append(problem)
                continue

            if (os.path.isfile(starter_code)):
                with open(starter_code, 'r') as f:
                    starter_code = f.read()
            else:
                starter_code = ""

            # Read the question description
            with open(question_fname, 'r') as f:
                question_str = f.read()

            # Read all the solutions
            with open(sols_fname, 'r') as f:
                sols_str_list = json.load(f)
                for sol_str in sols_str_list:
                    sol_str = reindent_code(sol_str)

                    yield id_, {
                        "id":id_, 
                        "question":question_str, 
                        "starter_code":starter_code, 
                        "answer_type":answer_type,
                        "answer":sol_str
                    }
                    id_ += 1


def generate_prompt(
    test_case_path, prompt_path, solutions_path, tokenizer, starter_path=None
):
    """
    Generate a prompt for a given test case.
    Original version from https://github.com/hendrycks/apps/blob/main/eval/generate_gpt_codes.py#L51.
    """
    _input = "\nQUESTION:\n"
    with open(prompt_path, "r") as f:
        data = f.readlines()
        data = "".join(data)
    _input += data
    if starter_path != None:
        with open(starter_path, "r") as f:
            data = f.readlines()
            data = "".join(data)
            data = "\n" + data  # + "\n"
        _input += data
    else:
        # _input += "\n\n"
        pass

    with open(test_case_path, "r") as f:
        data = json.load(f)
    if not data.get("fn_name"):
        _input += "\nUse Standard Input format"  # \n"
    else:
        _input += "\nUse Call-Based format"  # \n"

    _input += "\nANSWER:\n"

    return _input


def reindent_code(codestr):
    """
    Given code string, reindent it in the same way that the
    Github dataset was indented
    (from https://github.com/hendrycks/apps/blob/main/train/dataset_apps/APPSBaseDataset.py)
    """
    codestr = io.StringIO(codestr)
    ret = io.StringIO()

    run_reindent(
        codestr, 
        ret, 
        config = {
            "dry-run": False,
            "help": False,
            "to": 4,
            "from": -1,
            "tabs": True,
            "encoding": "utf-8",
            "is-tabs": False,
            "tabsize": 4,
            "all-tabs": False
        }
    )

    return ret.getvalue()

# This code come from https://github.com/hendrycks/apps/blob/main/train/dataset_lm/reindent.py
def _find_indentation(line, config):
    if len(line) and line[0] in (" ", "\t") and not line.isspace():
        if line[0] == "\t":
            config['is-tabs'] = True
        # Find indentation
        i = 0
        for char in list(line):
            if char not in (" ", "\t"):
                break
            i += 1
        config["from"] = i


def find_indentation(line, config):
    # Find indentation level used in file
    if config['from'] < 0:
        _find_indentation(line, config)

    if config['from'] >= 0:
        # Set old indent
        indent = " " if not config['is-tabs'] else "\t"
        indent = indent * config['from']

        # Set new indent
        newindent = " " if not config['tabs'] else "\t"
        if not config['tabs']:
            newindent = newindent * config['to']

        return indent, newindent

    # Continue to the next line, indentation not found
    return False


def replace_inline_tabs(content, config):
    newcontent = ""
    imagined_i = 0
    for i in range(0, len(content)):
        char = content[i]
        if char == '\t':
            spaces = config['tabsize']-(imagined_i % config['tabsize'])
            newcontent += " " * spaces
            imagined_i += spaces
        else:
            newcontent += char
            imagined_i += 1
    return newcontent


def run_reindent(fd_in, fd_out, config):
    while True:
        line = fd_in.readline()
        if not line:
            break
        line = line.rstrip('\r\n')

        # Find indentation style used in file if not set
        if config['from'] < 0:
            indent = find_indentation(line, config)
            if not indent:
                print(line, file=fd_out)
                continue
            indent, newindent = indent

        # Find current indentation level
        level = 0
        while True:
            whitespace = line[:len(indent) * (level + 1)]
            if whitespace == indent * (level + 1):
                level += 1
            else:
                break

        content = line[len(indent) * level:]
        if config['all-tabs']:
            content = replace_inline_tabs(content, config)

        line = (newindent * level) + content
        print(line, file=fd_out)