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
"""The WikiTableQuestions dataset is a large-scale dataset for the task of question answering on semi-structured tables."""

import os

import datasets


# Find for instance the citation on arxiv or on the dataset repo/website
_CITATION = """\
@inproceedings{pasupat-liang-2015-compositional,
    title = "Compositional Semantic Parsing on Semi-Structured Tables",
    author = "Pasupat, Panupong and Liang, Percy",
    booktitle = "Proceedings of the 53rd Annual Meeting of the Association for Computational Linguistics and the 7th International Joint Conference on Natural Language Processing (Volume 1: Long Papers)",
    month = jul,
    year = "2015",
    address = "Beijing, China",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/P15-1142",
    doi = "10.3115/v1/P15-1142",
    pages = "1470--1480",
}
"""

# You can copy an official description
_DESCRIPTION = """\
This WikiTableQuestions dataset is a large-scale dataset for the task of question answering on semi-structured tables.
"""

_HOMEPAGE = "https://nlp.stanford.edu/software/sempre/wikitable"

_LICENSE = "Creative Commons Attribution Share Alike 4.0 International"

# The HuggingFace Datasets library doesn't host the datasets but only points to the original files.
# This can be an arbitrary nested dict/list of URLs (see below in `_split_generators` method)
_DATA_URL = (
    "https://github.com/ppasupat/WikiTableQuestions/releases/download/v1.0.2/WikiTableQuestions-1.0.2-compact.zip"
)


class WikiTableQuestions(datasets.GeneratorBasedBuilder):
    """WikiTableQuestions: a large-scale dataset for the task of question answering on semi-structured tables."""

    VERSION = datasets.Version("1.0.2")

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
            name="random-split-1",
            version=VERSION,
            description="The random-split-1-train/dev.tsv and pristine-unseen-tables.tsv",
        ),
        datasets.BuilderConfig(
            name="random-split-2",
            version=VERSION,
            description="The random-split-2-train/dev.tsv and pristine-unseen-tables.tsv",
        ),
        datasets.BuilderConfig(
            name="random-split-3",
            version=VERSION,
            description="The random-split-3-train/dev.tsv and pristine-unseen-tables.tsv",
        ),
        datasets.BuilderConfig(
            name="random-split-4",
            version=VERSION,
            description="The random-split-4-train/dev.tsv and pristine-unseen-tables.tsv",
        ),
        datasets.BuilderConfig(
            name="random-split-5",
            version=VERSION,
            description="The random-split-5-train/dev.tsv and pristine-unseen-tables.tsv",
        ),
    ]

    DEFAULT_CONFIG_NAME = (
        "random-split-1"  # It's not mandatory to have a default configuration. Just use one if it make sense.
    )

    def _info(self):
        features = datasets.Features(
            {
                "id": datasets.Value("string"),
                "question": datasets.Value("string"),
                "answers": datasets.features.Sequence(datasets.Value("string")),
                "table": {
                    "header": datasets.features.Sequence(datasets.Value("string")),
                    "rows": datasets.features.Sequence(datasets.features.Sequence(datasets.Value("string"))),
                    "name": datasets.Value("string"),
                },
            }
        )
        return datasets.DatasetInfo(
            # This is the description that will appear on the datasets page.
            description=_DESCRIPTION,
            # This defines the different columns of the dataset and their types
            features=features,  # Here we define them above because they are different between the two configurations
            # If there's a common (input, target) tuple from the features, uncomment supervised_keys line below and
            # specify them. They'll be used if as_supervised=True in builder.as_dataset.
            # supervised_keys=("sentence", "label"),
            # Homepage of the dataset for documentation
            homepage=_HOMEPAGE,
            # License for the dataset if available
            license=_LICENSE,
            # Citation for the dataset
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        train_file = "{}-train.tsv".format(self.config.name)
        dev_file = "{}-dev.tsv".format(self.config.name)
        test_file = "pristine-unseen-tables.tsv"
        # dl_manager is a datasets.download.DownloadManager that can be used to download and extract URLS
        urls = _DATA_URL
        root_dir = os.path.join(dl_manager.download_and_extract(urls), "WikiTableQuestions")
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={"main_filepath": os.path.join(root_dir, "data", train_file), "root_dir": root_dir},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={"main_filepath": os.path.join(root_dir, "data", test_file), "root_dir": root_dir},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={"main_filepath": os.path.join(root_dir, "data", dev_file), "root_dir": root_dir},
            ),
        ]

    def _read_table_from_file(self, table_name: str, root_dir: str):
        def _extract_table_content(_line: str):
            _vals = [_.replace("\n", " ").strip() for _ in _line.strip("\n").split("\t")]
            return _vals

        rows = []
        # assert ".csv" in _wtq_table_name
        # use the normalized table file
        table_name = table_name.replace(".csv", ".tsv")
        with open(os.path.join(root_dir, table_name), "r", encoding="utf8") as table_f:
            table_lines = table_f.readlines()
            # the first line is header
            header = _extract_table_content(table_lines[0])
            for line in table_lines[1:]:
                rows.append(_extract_table_content(line))
        return {"header": header, "rows": rows, "name": table_name}

    # method parameters are unpacked from `gen_kwargs` as given in `_split_generators`
    def _generate_examples(self, main_filepath, root_dir):
        # The `key` is for legacy reasons (tfds) and is not important in itself, but must be unique for each example.
        with open(main_filepath, encoding="utf-8") as f:
            # skip the first line since it is the tsv header
            next(f)
            for idx, line in enumerate(f):
                example_id, question, table_name, answer = line.strip("\n").split("\t")
                answer = answer.split("|")
                # must contain rows and header keys
                table_content = self._read_table_from_file(table_name, root_dir)

                yield idx, {"id": example_id, "question": question, "answers": answer, "table": table_content}
