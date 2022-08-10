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
"""WUT Relations Between Sentences Corpus"""


import csv

import datasets


# TODO: Add BibTeX citation
# Find for instance the citation on arxiv or on the dataset repo/website
_CITATION = """\
@misc{11321/305,
 title = {{WUT} Relations Between Sentences Corpus},
 author = {Oleksy, Marcin and Fikus, Dominika and Wolski, Michal and Podbielska, Malgorzata and Turek, Agnieszka and Kędzia, Pawel},
 url = {http://hdl.handle.net/11321/305},
 note = {{CLARIN}-{PL} digital repository},
 copyright = {Attribution-{ShareAlike} 3.0 Unported ({CC} {BY}-{SA} 3.0)},
 year = {2016}
}
"""

# TODO: Add description of the dataset here
# You can copy an official description
_DESCRIPTION = """\
WUT Relations Between Sentences Corpus contains 2827 pairs of related sentences.
Relationships are derived from Cross-document Structure Theory (CST), which enables multi-document summarization through identification of cross-document rhetorical relationships within a cluster of related documents.
Every relation was marked by at least 3 annotators.
"""

# TODO: Add a link to an official homepage for the dataset here
_HOMEPAGE = "https://clarin-pl.eu/dspace/handle/11321/305"

# TODO: Add the licence for the dataset here if you can find it
_LICENSE = "Attribution-ShareAlike 3.0 Unported (CC BY-SA 3.0)"

# TODO: Add link to the official dataset URLs here
# The HuggingFace dataset library don't host the datasets but only point to the original files
# This can be an arbitrary nested dict/list of URLs (see below in `_split_generators` method)
_URL = "https://clarin-pl.eu/dspace/bitstream/handle/11321/305/sem_rels-betw-sents.csv"


# TODO: Name of the dataset usually match the script name with CamelCase instead of snake_case
class Wrbsc(datasets.GeneratorBasedBuilder):
    """WUT Relations Between Sentences Corpus"""

    VERSION = datasets.Version("1.1.0")

    def _info(self):
        # TODO: This method specifies the datasets.DatasetInfo object which contains informations and typings for the dataset
        features = datasets.Features(
            {
                "sentence1": datasets.Value("string"),
                "sentence2": datasets.Value("string"),
                "relationship": datasets.ClassLabel(
                    names=[
                        "Krzyżowanie_się",
                        "Tło_historyczne",
                        "Źródło",
                        "Dalsze_informacje",
                        "Zawieranie",
                        "Opis",
                        "Uszczegółowienie",
                        "Parafraza",
                        "Spełnienie",
                        "Mowa_zależna",
                        "Zmiana_poglądu",
                        "Streszczenie",
                        "Tożsamość",
                        "Sprzeczność",
                        "Modalność",
                        "Cytowanie",
                    ]
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
        filepath = dl_manager.download(_URL)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "filepath": filepath,
                    "split": "train",
                },
            ),
        ]

    def _generate_examples(self, filepath, split):
        """Yields examples."""
        # TODO: This method will receive as arguments the `gen_kwargs` defined in the previous `_split_generators` method.
        # It is in charge of opening the given file and yielding (key, example) tuples from the dataset
        # The key is not important, it's more here for legacy reason (legacy from tfds)

        with open(filepath, encoding="utf-8") as f:
            reader = csv.DictReader(
                f, delimiter="\t", fieldnames=["0", "1", "s1", "s2", "r", "2"], quoting=csv.QUOTE_NONE
            )
            for idx, row in enumerate(reader):
                yield idx, {
                    "sentence1": row["s1"][1:-1],
                    "sentence2": row["s2"][1:-1],
                    "relationship": row["r"],
                }
