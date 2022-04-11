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
"""Children's Book Test Dataset."""


import datasets


_CITATION = """\
@misc{hill2016goldilocks,
      title={The Goldilocks Principle: Reading Children's Books with Explicit Memory Representations},
      author={Felix Hill and Antoine Bordes and Sumit Chopra and Jason Weston},
      year={2016},
      eprint={1511.02301},
      archivePrefix={arXiv},
      primaryClass={cs.CL}
}
"""


_DESCRIPTION = """\
The Children’s Book Test (CBT) is designed to measure directly
how well language models can exploit wider linguistic context.
The CBT is built from books that are freely available.
"""

_HOMEPAGE = "https://research.fb.com/downloads/babi/"

_LICENSE = """GNU Free Documentation License v1.3"""

ZIP_URL = "http://www.thespermwhale.com/jaseweston/babi/CBTest.tgz"
dir = "CBTest/data/"
paths = {
    "raw": {"train": dir + "cbt_train.txt", "valid": dir + "cbt_valid.txt", "test": dir + "cbt_test.txt"},
    "V": {
        "train": dir + "cbtest_V_train.txt",
        "valid": dir + "cbtest_V_valid_2000ex.txt",
        "test": dir + "cbtest_V_test_2500ex.txt",
    },
    "P": {
        "train": dir + "cbtest_P_train.txt",
        "valid": dir + "cbtest_P_valid_2000ex.txt",
        "test": dir + "cbtest_P_test_2500ex.txt",
    },
    "NE": {
        "train": dir + "cbtest_NE_train.txt",
        "valid": dir + "cbtest_NE_valid_2000ex.txt",
        "test": dir + "cbtest_NE_test_2500ex.txt",
    },
    "CN": {
        "train": dir + "cbtest_CN_train.txt",
        "valid": dir + "cbtest_CN_valid_2000ex.txt",
        "test": dir + "cbtest_CN_test_2500ex.txt",
    },
}


class Cbt(datasets.GeneratorBasedBuilder):
    """TODO: Short description of my dataset."""

    VERSION = datasets.Version("1.1.0")

    BUILDER_CONFIGS = [
        datasets.BuilderConfig(
            name="raw", version=VERSION, description="This part of my dataset covers the raw CBT books"
        ),
        datasets.BuilderConfig(
            name="V", version=VERSION, description="This part of my dataset covers the verb answer CBT dataset"
        ),
        datasets.BuilderConfig(
            name="P", version=VERSION, description="This part of my dataset covers the preposition answer CBT dataset"
        ),
        datasets.BuilderConfig(
            name="NE",
            version=VERSION,
            description="This part of my dataset covers the named entity answer CBT dataset",
        ),
        datasets.BuilderConfig(
            name="CN", version=VERSION, description="This part of my dataset covers the common noun answer CBT dataset"
        ),
    ]

    def _info(self):
        if self.config.name in ["V", "P", "NE", "CN"]:
            features = datasets.Features(
                {
                    "sentences": datasets.Sequence(datasets.Value("string")),  # There are 20 sentences
                    "question": datasets.Value("string"),
                    "answer": datasets.Value("string"),
                    "options": datasets.Sequence(datasets.Value("string")),
                }
            )
        else:  # This is an example to show how to have different features for "first_domain" and "second_domain"
            features = datasets.Features({"title": datasets.Value("string"), "content": datasets.Value("string")})
        return datasets.DatasetInfo(
            # This is the description that will appear on the datasets page.
            description=_DESCRIPTION,
            # This defines the different columns of the dataset and their types
            features=features,  # Here we define them above because they are different between the two configurations
            # If there's a common (input, target) tuple from the features,
            # specify them here. They'll be used if as_supervised=True in
            # builder.as_dataset.
            supervised_keys=None,
            # Homepage of the dataset for documentation
            homepage=_HOMEPAGE,
            # License for the dataset if available
            license=_LICENSE,
            # Citation for the dataset
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        my_urls = ZIP_URL  # Cannot download just one single type as it is a compressed file.
        archive = dl_manager.download(my_urls)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={"filepath": paths[self.config.name]["train"], "files": dl_manager.iter_archive(archive)},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={"filepath": paths[self.config.name]["test"], "files": dl_manager.iter_archive(archive)},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={"filepath": paths[self.config.name]["valid"], "files": dl_manager.iter_archive(archive)},
            ),
        ]

    def _generate_examples(self, filepath, files):
        """Yields examples as (key, example) tuples."""
        for path, f in files:
            if path == filepath:
                if self.config.name != "raw":
                    sentences = []
                    example_idx = 0
                    for idx, line in enumerate(f):
                        line = line.decode("utf-8")
                        if line.strip() == "":
                            continue

                        elif line.split()[0] == "21":
                            splitline = line.split("\t")  # question, answer options are tab separated
                            question = splitline[0]
                            answer = splitline[1]
                            options = splitline[-1]
                            question = question[2:].strip()  # The first two indices contain `21`.
                            answer = answer.strip()
                            options = options.strip().split("|")
                            yield example_idx, {
                                "sentences": sentences,
                                "question": question,
                                "options": options,
                                "answer": answer,
                            }

                            sentences = []
                            example_idx += 1
                        else:
                            if len(line.split()[0]) == 1:
                                sentences.append(line[1:].strip())
                            else:
                                sentences.append(line[2:].strip())
                                # Text might contain double spaces.
                else:
                    book_idx = 0
                    book_sentences = []
                    for idx, line in enumerate(f):
                        line = line.decode("utf-8")
                        if line[:12] == "_BOOK_TITLE_":
                            if idx == 0:  # First line:
                                title = line.split(":")[1].strip()
                            else:
                                yield book_idx, {
                                    "title": title,
                                    "content": "".join(book_sentences),
                                }
                                title = line.split(":")[1].strip()
                                book_sentences = []
                                book_idx += 1
                        else:
                            book_sentences.append(line)
                    else:
                        yield book_idx, {
                            "title": title,
                            "content": "".join(book_sentences),
                        }
                        book_sentences = []
                        book_idx += 1
                break
