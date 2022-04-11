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
"""Movie Dialog Dataset."""

import datasets


_CITATION = """\
@misc{dodge2016evaluating,
      title={Evaluating Prerequisite Qualities for Learning End-to-End Dialog Systems},
      author={Jesse Dodge and Andreea Gane and Xiang Zhang and Antoine Bordes and Sumit Chopra and Alexander Miller and Arthur Szlam and Jason Weston},
      year={2016},
      eprint={1511.06931},
      archivePrefix={arXiv},
      primaryClass={cs.CL}
}
"""


_DESCRIPTION = """\
The Movie Dialog dataset (MDD) is designed to measure how well
models can perform at goal and non-goal orientated dialog
centered around the topic of movies (question answering,
recommendation and discussion).

"""

_HOMEPAGE = "https://research.fb.com/downloads/babi/"

_LICENSE = """Creative Commons Attribution 3.0 License"""

ZIP_URL = "http://www.thespermwhale.com/jaseweston/babi/movie_dialog_dataset.tgz"
REDDIT_URL = "http://tinyurl.com/p6tyohj"
dir = "movie_dialog_dataset/"
dir2 = ""
paths = {
    "task1_qa": {
        "train": dir + "task1_qa/task1_qa_train.txt",
        "dev": dir + "task1_qa/task1_qa_dev.txt",
        "test": dir + "task1_qa/task1_qa_test.txt",
    },
    "task2_recs": {
        "train": dir + "task2_recs/task2_recs_train.txt",
        "dev": dir + "task2_recs/task2_recs_dev.txt",
        "test": dir + "task2_recs/task2_recs_test.txt",
    },
    "task3_qarecs": {
        "train": dir + "task3_qarecs/task3_qarecs_train.txt",
        "dev": dir + "task3_qarecs/task3_qarecs_dev.txt",
        "test": dir + "task3_qarecs/task3_qarecs_test.txt",
    },
    "task4_reddit": {
        "train": "task4_reddit/task4_reddit_train.txt",
        "dev": "task4_reddit/task4_reddit_dev.txt",
        "test": "task4_reddit/task4_reddit_test.txt",
        "cand_valid": "task4_reddit/task4_reddit_cand-valid.txt",
        "cand_test": "task4_reddit/task4_reddit_cand-test.txt",
    },
}


class Mdd(datasets.GeneratorBasedBuilder):
    """The Movie Dialog Dataset"""

    VERSION = datasets.Version("1.1.0")

    BUILDER_CONFIGS = [
        datasets.BuilderConfig(
            name="task1_qa", version=VERSION, description="This part of my dataset covers task1_qa part of the dataset"
        ),
        datasets.BuilderConfig(
            name="task2_recs",
            version=VERSION,
            description="This part of my dataset covers task2_recs part of the dataset",
        ),
        datasets.BuilderConfig(
            name="task3_qarecs",
            version=VERSION,
            description="This part of my dataset covers task3_qarecs part of the dataset",
        ),
        datasets.BuilderConfig(
            name="task4_reddit",
            version=VERSION,
            description="This part of my dataset covers task4_reddit part of the dataset",
        ),
    ]

    def _info(self):
        features = datasets.Features(
            {
                "dialogue_turns": datasets.Sequence(
                    {
                        "speaker": datasets.Value("int32"),
                        "utterance": datasets.Value("string"),
                    }
                ),
            }
        )
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
        if self.config.name != "task4_reddit":
            my_urls = ZIP_URL  # Cannot download just one single type as it is a compressed file.
        else:
            my_urls = REDDIT_URL
        archive = dl_manager.download(my_urls)
        splits = [
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
                gen_kwargs={"filepath": paths[self.config.name]["dev"], "files": dl_manager.iter_archive(archive)},
            ),
        ]
        if self.config.name == "task4_reddit":
            splits += [
                datasets.SplitGenerator(
                    name=datasets.Split("cand_valid"),
                    # These kwargs will be passed to _generate_examples
                    gen_kwargs={
                        "filepath": paths[self.config.name]["cand_valid"],
                        "files": dl_manager.iter_archive(archive),
                    },
                ),
                datasets.SplitGenerator(
                    name=datasets.Split("cand_test"),
                    # These kwargs will be passed to _generate_examples
                    gen_kwargs={
                        "filepath": paths[self.config.name]["cand_test"],
                        "files": dl_manager.iter_archive(archive),
                    },
                ),
            ]
        return splits

    def _generate_examples(self, filepath, files):
        for path, f in files:
            if path == filepath:
                if "cand" not in filepath:
                    dialogue_turns = []
                    example_idx = 0
                    for idx, line in enumerate(f):
                        line = line.decode("utf-8")
                        if line.strip() == "":
                            if dialogue_turns != []:
                                yield example_idx, {"dialogue_turns": dialogue_turns}
                                example_idx += 1
                                dialogue_turns = []
                        elif line.strip().split()[0] == "1":  # New convo
                            if dialogue_turns != []:  # Already some convo, flush it out
                                yield example_idx, {"dialogue_turns": dialogue_turns}
                                example_idx += 1
                                dialogue_turns = []
                            exchange = line[len(line.split()[0]) :].strip().split("\t")  # Skip the number in the front
                            sp1 = exchange[0]
                            sp2 = exchange[-1]  # Might contain multiple tabs in between.
                            dialogue_turns.append({"speaker": 0, "utterance": sp1})
                            dialogue_turns.append({"speaker": 1, "utterance": sp2})
                        else:
                            exchange = line[len(line.split()[0]) :].strip().split("\t")  # Skip the number in the front
                            sp1 = exchange[0]
                            sp2 = exchange[-1]  # Might contain multiple tabs in between.
                            dialogue_turns.append({"speaker": 0, "utterance": sp1})
                            dialogue_turns.append({"speaker": 1, "utterance": sp2})
                    else:
                        if dialogue_turns != []:
                            yield example_idx, {"dialogue_turns": dialogue_turns}
                else:
                    dialogue_turns = []
                    example_idx = 0
                    for idx, line in enumerate(f):
                        line = line.decode("utf-8")
                        if line.strip() == "":
                            if dialogue_turns != []:
                                yield example_idx, {"dialogue_turns": dialogue_turns}
                                example_idx += 1
                                dialogue_turns = []
                        elif line.strip().split()[0] == "1":  # New convo
                            if dialogue_turns != []:  # Already some convo, flush it out
                                yield example_idx, {"dialogue_turns": dialogue_turns}
                                example_idx += 1
                                dialogue_turns = []
                            exchange = line[len(line.split()[0]) :].strip()  # Skip the number in the front
                            sp1 = exchange
                            dialogue_turns.append({"speaker": 0, "utterance": sp1})
                        else:
                            exchange = line[len(line.split()[0]) :].strip()  # Skip the number in the front
                            sp1 = exchange
                            dialogue_turns.append({"speaker": 0, "utterance": sp1})
                    else:  # Last line, new example
                        if dialogue_turns != []:
                            yield example_idx, {"dialogue_turns": dialogue_turns}
                break
