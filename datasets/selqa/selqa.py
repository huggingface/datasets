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
"""SelQA: A New Benchmark for Selection-Based Question Answering"""


import csv
import json

import datasets


# TODO: Add BibTeX citation
# Find for instance the citation on arxiv or on the dataset repo/website
_CITATION = """\
@InProceedings{7814688,
  author={T. {Jurczyk} and M. {Zhai} and J. D. {Choi}},
  booktitle={2016 IEEE 28th International Conference on Tools with Artificial Intelligence (ICTAI)},
  title={SelQA: A New Benchmark for Selection-Based Question Answering},
  year={2016},
  volume={},
  number={},
  pages={820-827},
  doi={10.1109/ICTAI.2016.0128}
}
"""

# TODO: Add description of the dataset here
# You can copy an official description
_DESCRIPTION = """\
The SelQA dataset provides crowdsourced annotation for two selection-based question answer tasks,
answer sentence selection and answer triggering.
"""

# TODO: Add a link to an official homepage for the dataset here
_HOMEPAGE = ""

# TODO: Add the licence for the dataset here if you can find it
_LICENSE = ""

# TODO: Add link to the official dataset URLs here
# The HuggingFace dataset library don't host the datasets but only point to the original files
# This can be an arbitrary nested dict/list of URLs (see below in `_split_generators` method)
types = {
    "answer_selection": "ass",
    "answer_triggering": "at",
}

modes = {"analysis": "json", "experiments": "tsv"}


class SelqaConfig(datasets.BuilderConfig):
    """ "BuilderConfig for SelQA Dataset"""

    def __init__(self, mode, type_, **kwargs):
        super(SelqaConfig, self).__init__(**kwargs)
        self.mode = mode
        self.type_ = type_


# TODO: Name of the dataset usually match the script name with CamelCase instead of snake_case
class Selqa(datasets.GeneratorBasedBuilder):
    """A New Benchmark for Selection-based Question Answering."""

    VERSION = datasets.Version("1.1.0")

    # This is an example of a dataset with multiple configurations.
    # If you don't want/need to define several sub-sets in your dataset,
    # just remove the BUILDER_CONFIG_CLASS and the BUILDER_CONFIGS attributes.

    # If you need to make complex sub-parts in the datasets with configurable options
    # You can create your own builder configuration class to store attribute, inheriting from datasets.BuilderConfig
    BUILDER_CONFIG_CLASS = SelqaConfig

    # You will be able to load one or the other configurations in the following list with
    # data = datasets.load_dataset('my_dataset', 'first_domain')
    # data = datasets.load_dataset('my_dataset', 'second_domain')
    BUILDER_CONFIGS = [
        SelqaConfig(
            name="answer_selection_analysis",
            mode="analysis",
            type_="answer_selection",
            version=VERSION,
            description="This part covers answer selection analysis",
        ),
        SelqaConfig(
            name="answer_selection_experiments",
            mode="experiments",
            type_="answer_selection",
            version=VERSION,
            description="This part covers answer selection experiments",
        ),
        SelqaConfig(
            name="answer_triggering_analysis",
            mode="analysis",
            type_="answer_triggering",
            version=VERSION,
            description="This part covers answer triggering analysis",
        ),
        SelqaConfig(
            name="answer_triggering_experiments",
            mode="experiments",
            type_="answer_triggering",
            version=VERSION,
            description="This part covers answer triggering experiments",
        ),
    ]

    DEFAULT_CONFIG_NAME = "answer_selection_analysis"  # It's not mandatory to have a default configuration. Just use one if it make sense.

    def _info(self):
        if (
            self.config.mode == "experiments"
        ):  # This is the name of the configuration selected in BUILDER_CONFIGS above
            features = datasets.Features(
                {
                    "question": datasets.Value("string"),
                    "candidate": datasets.Value("string"),
                    "label": datasets.ClassLabel(names=["0", "1"]),
                }
            )
        else:
            if self.config.type_ == "answer_selection":
                features = datasets.Features(
                    {
                        "section": datasets.Value("string"),
                        "question": datasets.Value("string"),
                        "article": datasets.Value("string"),
                        "is_paraphrase": datasets.Value("bool"),
                        "topic": datasets.ClassLabel(
                            names=[
                                "MUSIC",
                                "TV",
                                "TRAVEL",
                                "ART",
                                "SPORT",
                                "COUNTRY",
                                "MOVIES",
                                "HISTORICAL EVENTS",
                                "SCIENCE",
                                "FOOD",
                            ]
                        ),
                        "answers": datasets.Sequence(datasets.Value("int32")),
                        "candidates": datasets.Sequence(datasets.Value("string")),
                        "q_types": datasets.Sequence(
                            datasets.ClassLabel(names=["what", "why", "when", "who", "where", "how", ""])
                        ),
                    }
                )
            else:
                features = datasets.Features(
                    {
                        "section": datasets.Value("string"),
                        "question": datasets.Value("string"),
                        "article": datasets.Value("string"),
                        "is_paraphrase": datasets.Value("bool"),
                        "topic": datasets.ClassLabel(
                            names=[
                                "MUSIC",
                                "TV",
                                "TRAVEL",
                                "ART",
                                "SPORT",
                                "COUNTRY",
                                "MOVIES",
                                "HISTORICAL EVENTS",
                                "SCIENCE",
                                "FOOD",
                            ]
                        ),
                        "q_types": datasets.Sequence(
                            datasets.ClassLabel(names=["what", "why", "when", "who", "where", "how", ""])
                        ),
                        "candidate_list": datasets.Sequence(
                            {
                                "article": datasets.Value("string"),
                                "section": datasets.Value("string"),
                                "candidates": datasets.Sequence(datasets.Value("string")),
                                "answers": datasets.Sequence(datasets.Value("int32")),
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
        # TODO: This method is tasked with downloading/extracting the data and defining the splits depending on the configuration
        # If several configurations are possible (listed in BUILDER_CONFIGS), the configuration selected by the user is in self.config.name

        # dl_manager is a datasets.download.DownloadManager that can be used to download and extract URLs
        # It can accept any type or nested list/dict and will give back the same structure with the url replaced with path to local files.
        # By default the archives will be extracted and a path to a cached folder where they are extracted is returned instead of the archive
        urls = {
            "train": f"https://raw.githubusercontent.com/emorynlp/selqa/master/{types[self.config.type_]}/selqa-{types[self.config.type_]}-train.{modes[self.config.mode]}",
            "dev": f"https://raw.githubusercontent.com/emorynlp/selqa/master/{types[self.config.type_]}/selqa-{types[self.config.type_]}-dev.{modes[self.config.mode]}",
            "test": f"https://raw.githubusercontent.com/emorynlp/selqa/master/{types[self.config.type_]}/selqa-{types[self.config.type_]}-test.{modes[self.config.mode]}",
        }
        data_dir = dl_manager.download_and_extract(urls)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "filepath": data_dir["train"],
                    "split": "train",
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={"filepath": data_dir["test"], "split": "test"},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "filepath": data_dir["dev"],
                    "split": "dev",
                },
            ),
        ]

    def _generate_examples(self, filepath, split):
        """Yields examples."""
        # TODO: This method will receive as arguments the `gen_kwargs` defined in the previous `_split_generators` method.
        # It is in charge of opening the given file and yielding (key, example) tuples from the dataset
        # The key is not important, it's more here for legacy reason (legacy from tfds)
        with open(filepath, encoding="utf-8") as f:
            if self.config.mode == "experiments":
                csv_reader = csv.DictReader(
                    f, delimiter="\t", quoting=csv.QUOTE_NONE, fieldnames=["question", "candidate", "label"]
                )
                for id_, row in enumerate(csv_reader):
                    yield id_, row
            else:
                if self.config.type_ == "answer_selection":
                    for row in f:
                        data = json.loads(row)
                        for id_, item in enumerate(data):
                            yield id_, {
                                "section": item["section"],
                                "question": item["question"],
                                "article": item["article"],
                                "is_paraphrase": item["is_paraphrase"],
                                "topic": item["topic"],
                                "answers": item["answers"],
                                "candidates": item["candidates"],
                                "q_types": item["q_types"],
                            }
                else:
                    for row in f:
                        data = json.loads(row)
                        for id_, item in enumerate(data):
                            candidate_list = []
                            for entity in item["candidate_list"]:
                                candidate_list.append(
                                    {
                                        "article": entity["article"],
                                        "section": entity["section"],
                                        "answers": entity["answers"],
                                        "candidates": entity["candidates"],
                                    }
                                )
                            yield id_, {
                                "section": item["section"],
                                "question": item["question"],
                                "article": item["article"],
                                "is_paraphrase": item["is_paraphrase"],
                                "topic": item["topic"],
                                "q_types": item["q_types"],
                                "candidate_list": candidate_list,
                            }
