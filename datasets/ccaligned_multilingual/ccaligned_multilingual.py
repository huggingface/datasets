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
"""Ccaligned Multilingual Translation Dataset"""


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


_LICENSE = ""  # Unknown


_URLs = {
    "documents": "http://www.statmt.org/cc-aligned/",
    "sentences": "http://www.statmt.org/cc-aligned/sentence-aligned/",
}

reverse_mapped_sentences = [
    "af_ZA",
    "ak_GH",
    "am_ET",
    "ar_AR",
    "as_IN",
    "ay_BO",
    "az_AZ",
    "az_IR",
    "be_BY",
    "bg_BG",
    "bm_ML",
    "bn_IN",
    "br_FR",
    "bs_BA",
    "ca_ES",
    "cb_IQ",
    "cs_CZ",
    "cx_PH",
    "cy_GB",
    "da_DK",
    "de_DE",
    "el_GR",
]  # Some languages have the reverse source languages in the URLs.


class CcalignedMultilingualConfig(datasets.BuilderConfig):
    def __init__(self, *args, type=None, language_code=None, **kwargs):
        super().__init__(
            *args,
            name=f"{type}-{language_code}",
            **kwargs,
        )
        self.type = type
        self.language_code = language_code


class CcalignedMultilingual(datasets.GeneratorBasedBuilder):
    """The Ccaligned Multilingual Dataset."""

    VERSION = datasets.Version("1.0.0")

    BUILDER_CONFIGS = [
        CcalignedMultilingualConfig(
            type="documents",
            language_code="zz_TR",
            version=VERSION,
            description="The dataset containing document-pairs for en_XX-zz_TR.",
        ),
        CcalignedMultilingualConfig(
            type="sentences",
            language_code="zz_TR",
            version=VERSION,
            description="The dataset containing sentence-pairs for en_XX-zz_TR.",
        ),
        CcalignedMultilingualConfig(
            type="documents",
            language_code="tz_MA",
            version=VERSION,
            description="The dataset containing document-pairs for en_XX-tz_MA.",
        ),
        CcalignedMultilingualConfig(
            type="sentences",
            language_code="tz_MA",
            version=VERSION,
            description="The dataset containing sentence-pairs for en_XX-tz_MA.",
        ),
        CcalignedMultilingualConfig(
            type="documents",
            language_code="ak_GH",
            version=VERSION,
            description="The dataset containing document-pairs for en_XX-ak_GH.",
        ),
        CcalignedMultilingualConfig(
            type="sentences",
            language_code="ak_GH",
            version=VERSION,
            description="The dataset containing sentence-pairs for en_XX-ak_GH.",
        ),
    ]

    BUILDER_CONFIG_CLASS = CcalignedMultilingualConfig

    # DEFAULT_CONFIG_NAME = "documents-zz_TR" # Not Needed

    def _info(self):
        if self.config.name[:9] == "documents":
            features = datasets.Features(
                {
                    "Domain": datasets.Value("string"),
                    "Source_URL": datasets.Value("string"),
                    "Target_URL": datasets.Value("string"),
                    "translation": datasets.Translation(languages=("en_XX", self.config.language_code)),
                }
            )
        else:
            features = datasets.Features(
                {
                    "translation": datasets.Translation(languages=("en_XX", self.config.language_code)),
                    "LASER_similarity": datasets.Value("float"),
                }
            )

        return datasets.DatasetInfo(
            # This is the description that will appear on the datasets page.
            description=_DESCRIPTION,
            # This defines the different columns of the dataset and their types
            features=features,  # Here we define them above because they are different between the two configurations
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
        my_urls = _URLs[self.config.name[:9]]
        if self.config.name[:9] == "sentences" and self.config.language_code in reverse_mapped_sentences:
            url = my_urls + self.config.language_code + "-en_XX.tsv.xz"
            from_english = False
        else:
            url = my_urls + "en_XX-" + self.config.language_code + ".tsv.xz"
            from_english = True
        data_file = dl_manager.download_and_extract(url)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "filepath": os.path.join(data_file),
                    "from_english": from_english,  # Whether the translation is from english or to english, only useful in case of sentence-pairs
                },
            )
        ]

    def _generate_examples(self, filepath, from_english=False):
        """Yields examples."""
        lc = self.config.language_code
        reverse = lc in reverse_mapped_sentences
        with open(filepath, encoding="utf-8") as f:
            for id_, row in enumerate(f):
                data = row.split("\t")
                if self.config.name[:9] == "documents":
                    yield id_, {
                        "Domain": data[0],
                        "Source_URL": data[1],
                        "Target_URL": data[3],
                        "translation": {"en_XX": data[2].strip(), lc: data[4].strip()},
                    }
                else:
                    if not reverse:
                        yield id_, {
                            "translation": {"en_XX": data[0].strip(), lc: data[1].strip()},
                            "LASER_similarity": data[2],
                        }
                    else:
                        yield id_, {
                            "translation": {lc: data[0].strip(), "en_XX": data[1].strip()},
                            "LASER_similarity": data[2],
                        }
