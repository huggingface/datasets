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
"""OHSUMED: An Interactive Retrieval Evaluation and New Large Test Collection for Research."""


import datasets


# TODO: Add BibTeX citation
# Find for instance the citation on arxiv or on the dataset repo/website
_CITATION = """\
@InProceedings{10.1007/978-1-4471-2099-5_20,
author="Hersh, William
and Buckley, Chris
and Leone, T. J.
and Hickam, David",
editor="Croft, Bruce W.
and van Rijsbergen, C. J.",
title="OHSUMED: An Interactive Retrieval Evaluation and New Large Test Collection for Research",
booktitle="SIGIR '94",
year="1994",
publisher="Springer London",
address="London",
pages="192--201",
abstract="A series of information retrieval experiments was carried out with a computer installed in a medical practice setting for relatively inexperienced physician end-users. Using a commercial MEDLINE product based on the vector space model, these physicians searched just as effectively as more experienced searchers using Boolean searching. The results of this experiment were subsequently used to create a new large medical test collection, which was used in experiments with the SMART retrieval system to obtain baseline performance data as well as compare SMART with the other searchers.",
isbn="978-1-4471-2099-5"
}
"""

# TODO: Add description of the dataset here
# You can copy an official description
_DESCRIPTION = """\
The OHSUMED test collection is a set of 348,566 references from
MEDLINE, the on-line medical information database, consisting of
titles and/or abstracts from 270 medical journals over a five-year
period (1987-1991). The available fields are title, abstract, MeSH
indexing terms, author, source, and publication type.
"""

# TODO: Add a link to an official homepage for the dataset here
_HOMEPAGE = "http://davis.wpi.edu/xmdv/datasets/ohsumed.html"

# TODO: Add the licence for the dataset here if you can find it
_LICENSE = "CC BY-NC 4.0"

# TODO: Add link to the official dataset URLs here
# The HuggingFace dataset library don't host the datasets but only point to the original files
# This can be an arbitrary nested dict/list of URLs (see below in `_split_generators` method)
_URLs = {"ohsumed": "https://trec.nist.gov/data/filtering/t9.filtering.tar.gz"}


# TODO: Name of the dataset usually match the script name with CamelCase instead of snake_case
class Ohsumed(datasets.GeneratorBasedBuilder):
    """OHSUMED: An Interactive Retrieval Evaluation and New Large Test Collection for Research."""

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
            name="ohsumed",
            version=VERSION,
            description="Config for the entire ohsumed dataset. An Interactive Retrieval Evaluation and New Large Test Collection for Research",
        )
    ]

    def _info(self):
        # TODO: This method specifies the datasets.DatasetInfo object which contains informations and typings for the dataset
        features = datasets.Features(
            {
                "seq_id": datasets.Value("int64"),
                "medline_ui": datasets.Value("int64"),
                "mesh_terms": datasets.Value("string"),
                "title": datasets.Value("string"),
                "publication_type": datasets.Value("string"),
                "abstract": datasets.Value("string"),
                "author": datasets.Value("string"),
                "source": datasets.Value("string"),
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
        my_urls = _URLs[self.config.name]
        archive = dl_manager.download(my_urls)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "filepath": "ohsu-trec/trec9-train/ohsumed.87",
                    "files": dl_manager.iter_archive(archive),
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "filepath": "ohsu-trec/trec9-test/ohsumed.88-91",
                    "files": dl_manager.iter_archive(archive),
                },
            ),
        ]

    def _generate_examples(self, filepath, files):
        """Yields examples."""
        # TODO: This method will receive as arguments the `gen_kwargs` defined in the previous `_split_generators` method.
        # It is in charge of opening the given file and yielding (key, example) tuples from the dataset
        # The key is not important, it's more here for legacy reason (legacy from tfds)

        def ohsumed_dict():
            """Returns a dict."""

            data = {
                "seq_id": -1,
                "medline_ui": -1,
                "mesh_terms": "",
                "title": "",
                "publication_type": "",
                "abstract": "",
                "author": "",
                "source": "",
            }

            return data

        tag = ""
        column_map = {
            ".I": "seq_id",
            ".U": "medline_ui",
            ".M": "mesh_terms",
            ".T": "title",
            ".P": "publication_type",
            ".W": "abstract",
            ".A": "author",
            ".S": "source",
        }

        for path, f in files:
            if path == filepath:
                data = ohsumed_dict()

                for line in f.readlines():
                    line = line.decode("utf-8").strip()

                    if line.startswith(".I"):
                        tag = ".I"
                        if data["medline_ui"] != -1:
                            id_ = data["seq_id"] + "_" + data["medline_ui"]
                            yield id_, {
                                "seq_id": data["seq_id"],
                                "medline_ui": data["medline_ui"],
                                "mesh_terms": str(data["mesh_terms"]),
                                "title": str(data["title"]),
                                "publication_type": str(data["publication_type"]),
                                "abstract": str(data["abstract"]),
                                "author": str(data["author"]),
                                "source": str(data["source"]),
                            }
                        else:
                            data = ohsumed_dict()
                            line = line.replace(".I", "").strip()
                            data["seq_id"] = line
                    elif tag and not line.startswith("."):
                        key = column_map[tag]
                        data[key] = line
                    elif ".U" in line:
                        tag = ".U"
                    elif ".M" in line:
                        tag = ".M"
                    elif ".T" in line:
                        tag = ".T"
                    elif ".P" in line:
                        tag = ".P"
                    elif ".W" in line:
                        tag = ".W"
                    elif ".A" in line:
                        tag = ".A"
                    elif ".S" in line:
                        tag = ".S"
                break
