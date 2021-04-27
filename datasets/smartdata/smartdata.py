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
"""\
DFKI SmartData Corpus is a dataset of 2598 German-language documents
which has been annotated with fine-grained geo-entities, such as streets,
stops and routes, as well as standard named entity types."""


import re
from json import JSONDecodeError, JSONDecoder

import datasets


_CITATION = """\
@InProceedings{SCHIERSCH18.85,
  author = {Martin Schiersch and Veselina Mironova and Maximilian Schmitt and Philippe Thomas and Aleksandra Gabryszak and Leonhard Hennig},
  title = "{A German Corpus for Fine-Grained Named Entity Recognition and Relation Extraction of Traffic and Industry Events}",
  booktitle = {Proceedings of the Eleventh International Conference on Language Resources and Evaluation (LREC 2018)},
  year = {2018},
  month = {May 7-12, 2018},
  address = {Miyazaki, Japan},
  editor = {Nicoletta Calzolari (Conference chair) and Khalid Choukri and Christopher Cieri and Thierry Declerck and Sara Goggi and Koiti Hasida and Hitoshi Isahara and Bente Maegaard and Joseph Mariani and Hélène Mazo and Asuncion Moreno and Jan Odijk and Stelios Piperidis and Takenobu Tokunaga},
  publisher = {European Language Resources Association (ELRA)},
  isbn = {979-10-95546-00-9},
  language = {english}
  }
"""

_DESCRIPTION = """\
DFKI SmartData Corpus is a dataset of 2598 German-language documents
which has been annotated with fine-grained geo-entities, such as streets,
stops and routes, as well as standard named entity types. It has also
been annotated with a set of 15 traffic- and industry-related n-ary
relations and events, such as Accidents, Traffic jams, Acquisitions,
and Strikes. The corpus consists of newswire texts, Twitter messages,
and traffic reports from radio stations, police and railway companies.
It allows for training and evaluating both named entity recognition
algorithms that aim for fine-grained typing of geo-entities, as well
as n-ary relation extraction systems."""

_HOMEPAGE = "https://www.dfki.de/web/forschung/projekte-publikationen/publikationen-uebersicht/publikation/9427/"

_LICENSE = "CC-BY 4.0"

_URLs = {
    "train": "https://github.com/DFKI-NLP/smartdata-corpus/raw/master/v3_20200302/train.json.gz",
    "dev": "https://github.com/DFKI-NLP/smartdata-corpus/raw/master/v3_20200302/dev.json.gz",
    "test": "https://github.com/DFKI-NLP/smartdata-corpus/raw/master/v3_20200302/test.json.gz",
}


class Smartdata(datasets.GeneratorBasedBuilder):
    """DFKI SmartData Corpus is a dataset of 2598 German-language documents
    which has been annotated with fine-grained geo-entities, such as streets,
    stops and routes, as well as standard named entity types."""

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
        datasets.BuilderConfig(name="smartdata-v3_20200302", version=VERSION, description="SmartData v3"),
    ]

    def _info(self):
        features = datasets.Features(
            {
                "id": datasets.Value("string"),
                "tokens": datasets.Sequence(datasets.Value("string")),
                "ner_tags": datasets.Sequence(
                    datasets.features.ClassLabel(
                        names=[
                            "O",
                            "B-DATE",
                            "I-DATE",
                            "B-DISASTER_TYPE",
                            "I-DISASTER_TYPE",
                            "B-DISTANCE",
                            "I-DISTANCE",
                            "B-DURATION",
                            "I-DURATION",
                            "B-LOCATION",
                            "I-LOCATION",
                            "B-LOCATION_CITY",
                            "I-LOCATION_CITY",
                            "B-LOCATION_ROUTE",
                            "I-LOCATION_ROUTE",
                            "B-LOCATION_STOP",
                            "I-LOCATION_STOP",
                            "B-LOCATION_STREET",
                            "I-LOCATION_STREET",
                            "B-NUMBER",
                            "I-NUMBER",
                            "B-ORGANIZATION",
                            "I-ORGANIZATION",
                            "B-ORGANIZATION_COMPANY",
                            "I-ORGANIZATION_COMPANY",
                            "B-ORG_POSITION",
                            "I-ORG_POSITION",
                            "B-PERSON",
                            "I-PERSON",
                            "B-TIME",
                            "I-TIME",
                            "B-TRIGGER",
                            "I-TRIGGER",
                        ]
                    )
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

        # dl_manager is a datasets.download.DownloadManager that can be used to download and extract URLs
        # It can accept any type or nested list/dict and will give back the same structure with the url replaced with path to local files.
        # By default the archives will be extracted and a path to a cached folder where they are extracted is returned instead of the archive
        data_dir = dl_manager.download_and_extract(_URLs)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={"filepath": data_dir["train"], "split": "train"},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={"filepath": data_dir["test"], "split": "test"},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={"filepath": data_dir["dev"], "split": "dev"},
            ),
        ]

    def _generate_examples(self, filepath, split):
        """Yields examples."""

        NOT_WHITESPACE = re.compile(r"[^\s]")

        def decode_stacked(document, pos=0, decoder=JSONDecoder()):
            while True:
                match = NOT_WHITESPACE.search(document, pos)
                if not match:
                    return
                pos = match.start()
                try:
                    obj, pos = decoder.raw_decode(document, pos)
                except JSONDecodeError:
                    raise
                yield obj

        with open(filepath, encoding="utf-8") as f:
            raw = f.read()

        for a in decode_stacked(raw):
            text = a["text"]["string"]
            aid = a["id"]
            toks = []
            lbls = []
            for x in a["tokens"]["array"]:
                toks.append(text[x["span"]["start"] : x["span"]["end"]])
                lbls.append(x["ner"]["string"])

            yield aid, {
                "id": aid,
                "tokens": toks,
                "ner_tags": lbls,
            }
