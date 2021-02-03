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
"""CCAligned Multilingual Translation Dataset"""

from __future__ import absolute_import, division, print_function

import csv
import json
import os

import datasets


_CITATION = """\
@inproceedings{elkishky_ccaligned_2020,
 author = {El-Kishky, Ahmed and Chaudhary, Vishrav and Guzm{\'a}n, Francisco and Koehn, Philipp},
 booktitle = {Proceedings of the 2020 Conference on Empirical Methods in Natural Language Processing (EMNLP 2020)},
 month = {November},
 title = {{CCAligned}: A Massive Collection of Cross-lingual Web-Document Pairs},
 year = {2020}
 address = "Online",
 publisher = "Association for Computational Linguistics",
 url = "https://www.aclweb.org/anthology/2020.emnlp-main.480",
 doi = "10.18653/v1/2020.emnlp-main.480",
 pages = "5960--5969"
}
"""

_DESCRIPTION = """\
CCAligned consists of parallel or comparable web-document pairs in 137 languages aligned with English. These web-document pairs were constructed by performing language identification on raw web-documents, and ensuring corresponding language codes were corresponding in the URLs of web documents. This pattern matching approach yielded more than 100 million aligned documents paired with English. Recognizing that each English document was often aligned to mulitple documents in different target language, we can join on English documents to obtain aligned documents that directly pair two non-English documents (e.g., Arabic-French).
"""

_HOMEPAGE = "http://www.statmt.org/cc-aligned/"


_LICENSE = "" # Unknown


_URLs = {
    'documents': "http://www.statmt.org/cc-aligned/",
    'sentences': "http://www.statmt.org/cc-aligned/sentence-aligned/",
}



class CCAlignedMultilingual(datasets.GeneratorBasedBuilder):
    """The CCAligned Multilingual Dataset."""

    VERSION = datasets.Version("1.0.0")

    BUILDER_CONFIGS = [
        datasets.BuilderConfig(name="documents", version=VERSION, description="The dataset containing document-pairs."),
        datasets.BuilderConfig(name="sentences", version=VERSION, description="The dataset containing sentence-pairs."),
    ]

    DEFAULT_CONFIG_NAME = "documents"
    def _info(self):
        if self.config.name == "documents":
            features = datasets.Features(
                {
                    "Domain": datasets.Value("string"),
                    "Source_URL": datasets.Value("string"),
                    "Source_Content": datasets.Value("string"),
                    "Target_URL": datasets.Value("string"),
                    "Target_Content": datasets.Value("string"),
                }
            )
        else:
            features = datasets.Features(
                {
                    "Source_Sentence": datasets.Value("string"),
                    "Target_Sentence": datasets.Value("string"),
                    "LASER_similarity": datasets.Value("float")
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
        my_urls = _URLs[self.config.name]
        url = os.path.join(my_urls, self.config.language_code)
        data_file = dl_manager.download_and_extract(url)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "filepath": os.path.join(data_file),
                },
            )
        ]

    def _generate_examples(self, filepath):
        """ Yields examples. """
        with open(filepath, encoding="utf-8") as f:
            for id_, row in enumerate(f):
                data = row.split('\t')
                if self.config.name == "first_domain":
                    yield id_, {
                        "Domain": data[0],
                        "Source_URL": data[1],
                        "Source_Content": data[2],
                        "Target_URL": data[3],
                        "Target_Content": data[4],
                    }
                else:
                    yield id_, {
                        "Source_Sentence": data[0],
                        "Target_Sentence": data[1],
                        "LASER_similarity": data[2]
                    }
