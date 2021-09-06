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
"""SwedMedNER: A Named Entity Recognition Dataset on medical texts in Swedish"""


import re
import datasets


_CITATION = """\
@inproceedings{almgrenpavlovmogren2016bioner,
  title={Named Entity Recognition in Swedish Medical Journals with Deep Bidirectional Character-Based LSTMs},
  author={Simon Almgren, Sean Pavlov, Olof Mogren},
  booktitle={Proceedings of the Fifth Workshop on Building and Evaluating Resources for Biomedical Text Mining (BioTxtM 2016)},
  pages={1},
  year={2016}
}
"""


_DESCRIPTION = """\
SwedMedNER is a dataset for training and evaluating Named Entity Recognition systems on medical texts in Swedish.
It is derived from medical articles on the Swedish Wikipedia, Läkartidningen, and 1177 Vårdguiden.
"""


_LICENSE = """\
Creative Commons Attribution-ShareAlike 4.0 International Public License (CC BY-SA 4.0)
See http://creativecommons.org/licenses/by-sa/4.0/ for the summary of the license.
"""


_URL = "https://github.com/olofmogren/biomedical-ner-data-swedish"


_DATA_URL = "https://raw.githubusercontent.com/olofmogren/biomedical-ner-data-swedish/master/"


class SwedishMedicalNerConfig(datasets.BuilderConfig):
    """BuilderConfig for SwedMedNER"""

    def __init__(self, **kwargs):
        """
        Args:
          **kwargs: keyword arguments forwarded to super.
        """
        super(SwedishMedicalNerConfig, self).__init__(**kwargs)


class SwedishMedicalNer(datasets.GeneratorBasedBuilder):
    """SwedMedNER: A Named Entity Recognition Dataset on medical texts in Swedish"""

    VERSION = datasets.Version("1.0.0")

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
        datasets.BuilderConfig(name="wiki", version=VERSION, description="The Swedish Wikipedia part of the dataset"),
        datasets.BuilderConfig(name="lt", version=VERSION, description="The Läkartidningen part of the dataset"),
        datasets.BuilderConfig(name="1177", version=VERSION, description="The 1177 Vårdguiden part of the dataset"),
    ]

    def _info(self):
        if self.config.name == "wiki":  # This is the name of the configuration selected in BUILDER_CONFIGS above
            features = datasets.Features(
                {
                    "sid": datasets.Value("string"),
                    "sentence": datasets.Value("string"),
                    "entities": datasets.Sequence(
                        {
                            "start": datasets.Value("int32"),
                            "end": datasets.Value("int32"),
                            "text": datasets.Value("string"),
                            "type": datasets.Value("string"),
                        }
                    ),
                }
            )
        elif self.config.name == "lt":
            features = datasets.Features(
                {
                    "sid": datasets.Value("string"),
                    "sentence": datasets.Value("string"),
                    "entities": datasets.Sequence(
                        {
                            "start": datasets.Value("int32"),
                            "end": datasets.Value("int32"),
                            "text": datasets.Value("string"),
                            "type": datasets.Value("string"),
                        }
                    ),
                }
            )
        elif self.config.name == "1177":
            features = datasets.Features(
                {
                    "sid": datasets.Value("string"),
                    "sentence": datasets.Value("string"),
                    "entities": datasets.Sequence(
                        {
                            "start": datasets.Value("int32"),
                            "end": datasets.Value("int32"),
                            "text": datasets.Value("string"),
                            "type": datasets.Value("string"),
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
            homepage=_URL,
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
        urls_to_download = {
            "wiki": _DATA_URL + "Wiki_annotated_60.txt",
            "lt": _DATA_URL + "LT_annotated_60.txt",
            "1177": _DATA_URL + "1177_annotated_sentences.txt",
        }
        downloaded_files = dl_manager.download_and_extract(urls_to_download)

        if self.config.name == "wiki":
            return [
                datasets.SplitGenerator(name=datasets.Split.TRAIN, gen_kwargs={"filepath": downloaded_files["wiki"]})
            ]
        elif self.config.name == "lt":
            return [
                datasets.SplitGenerator(name=datasets.Split.TRAIN, gen_kwargs={"filepath": downloaded_files["lt"]})
            ]
        elif self.config.name == "1177":
            return [
                datasets.SplitGenerator(name=datasets.Split.TRAIN, gen_kwargs={"filepath": downloaded_files["1177"]})
            ]

    def _generate_examples(
        self, filepath  # method parameters are unpacked from `gen_kwargs` as given in `_split_generators`
    ):
        """Yields examples as (key, example) tuples."""
        # This method handles input defined in _split_generators to yield (key, example) tuples from the dataset.
        # The `key` is here for legacy reason (tfds) and is not important in itself.

        def find_type(s, e):
            if (s == "(") and (e == ")"):
                return "Disorder and Finding"
            elif (s == "[") and (e == "]"):
                return "Pharmaceutical Drug"
            elif (s == "{") and (e == "}"):
                return "Body Structure"
            else:
                return ""

        pattern = r"\[([^\[\]()]+)\]|\(([^\[\]()]+)\)|\{([^\[\]()]+)\}"
        with open(filepath, encoding="utf-8") as f:
            for id_, row in enumerate(f):
                sentence = row.replace("\n", "")

                if self.config.name == "1177":
                    targets = [
                        {
                            "start": m.start(0),
                            "end": m.end(0),
                            "text": sentence[m.start(0) + 2 : m.end(0) - 2],
                            "type": find_type(sentence[m.start(0)], sentence[m.end(0) - 1]),
                        }
                        for m in re.finditer(pattern, sentence)
                    ]
                    yield id_, {
                        "sid": self.config.name + "_" + str(id_),
                        "sentence": sentence,
                        "entities": targets if targets else [{"start": 999, "end": 999, "text": "", "type": ""}],
                    }
                else:
                    targets = [
                        {
                            "start": m.start(0),
                            "end": m.end(0),
                            "text": sentence[m.start(0) + 1 : m.end(0) - 1],
                            "type": find_type(sentence[m.start(0)], sentence[m.end(0) - 1]),
                        }
                        for m in re.finditer(pattern, sentence)
                    ]
                    yield id_, {
                        "sid": self.config.name + "_" + str(id_),
                        "sentence": sentence,
                        "entities": targets if targets else [{"start": 999, "end": 999, "text": "", "type": ""}],
                    }
