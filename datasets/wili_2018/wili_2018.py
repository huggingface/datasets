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

"""WiLI-2018, the Wikipedia language identification benchmark dataset"""


import datasets
from datasets.tasks import TextClassification


_CITATION = """\
@dataset{thoma_martin_2018_841984,
  author       = {Thoma, Martin},
  title        = {{WiLI-2018 - Wikipedia Language Identification database}},
  month        = jan,
  year         = 2018,
  publisher    = {Zenodo},
  version      = {1.0.0},
  doi          = {10.5281/zenodo.841984},
  url          = {https://doi.org/10.5281/zenodo.841984}
}
"""

_DESCRIPTION = """\
It is a benchmark dataset for language identification and contains 235000 paragraphs of 235 languages
"""

# TODO: Add a link to an official homepage for the dataset here
_HOMEPAGE = "https://zenodo.org/record/841984"

# TODO: Add the licence for the dataset here if you can find it
_LICENSE = "ODC Open Database License v1.0"


# This can be an arbitrary nested dict/list of URLs (see below in `_split_generators` method)
_TRAIN_DOWNLOAD_URL = "https://drive.google.com/uc?export=download&id=1ZzlIQvw1KNBG97QQCfdatvVrrbeLaM1u"
_TEST_DOWNLOAD_URL = "https://drive.google.com/uc?export=download&id=1Xx4kFc1Xdzz8AhDasxZ0cSa-a35EQSDZ"

_CLASSES = [
    "cdo",
    "glk",
    "jam",
    "lug",
    "san",
    "rue",
    "wol",
    "new",
    "mwl",
    "bre",
    "ara",
    "hye",
    "xmf",
    "ext",
    "cor",
    "yor",
    "div",
    "asm",
    "lat",
    "cym",
    "hif",
    "ace",
    "kbd",
    "tgk",
    "rus",
    "nso",
    "mya",
    "msa",
    "ava",
    "cbk",
    "urd",
    "deu",
    "swa",
    "pus",
    "bxr",
    "udm",
    "csb",
    "yid",
    "vro",
    "por",
    "pdc",
    "eng",
    "tha",
    "hat",
    "lmo",
    "pag",
    "jav",
    "chv",
    "nan",
    "sco",
    "kat",
    "bho",
    "bos",
    "kok",
    "oss",
    "mri",
    "fry",
    "cat",
    "azb",
    "kin",
    "hin",
    "sna",
    "dan",
    "egl",
    "mkd",
    "ron",
    "bul",
    "hrv",
    "som",
    "pam",
    "nav",
    "ksh",
    "nci",
    "khm",
    "sgs",
    "srn",
    "bar",
    "cos",
    "ckb",
    "pfl",
    "arz",
    "roa-tara",
    "fra",
    "mai",
    "zh-yue",
    "guj",
    "fin",
    "kir",
    "vol",
    "hau",
    "afr",
    "uig",
    "lao",
    "swe",
    "slv",
    "kor",
    "szl",
    "srp",
    "dty",
    "nrm",
    "dsb",
    "ind",
    "wln",
    "pnb",
    "ukr",
    "bpy",
    "vie",
    "tur",
    "aym",
    "lit",
    "zea",
    "pol",
    "est",
    "scn",
    "vls",
    "stq",
    "gag",
    "grn",
    "kaz",
    "ben",
    "pcd",
    "bjn",
    "krc",
    "amh",
    "diq",
    "ltz",
    "ita",
    "kab",
    "bel",
    "ang",
    "mhr",
    "che",
    "koi",
    "glv",
    "ido",
    "fao",
    "bak",
    "isl",
    "bcl",
    "tet",
    "jpn",
    "kur",
    "map-bms",
    "tyv",
    "olo",
    "arg",
    "ori",
    "lim",
    "tel",
    "lin",
    "roh",
    "sqi",
    "xho",
    "mlg",
    "fas",
    "hbs",
    "tam",
    "aze",
    "lad",
    "nob",
    "sin",
    "gla",
    "nap",
    "snd",
    "ast",
    "mal",
    "mdf",
    "tsn",
    "nds",
    "tgl",
    "nno",
    "sun",
    "lzh",
    "jbo",
    "crh",
    "pap",
    "oci",
    "hak",
    "uzb",
    "zho",
    "hsb",
    "sme",
    "mlt",
    "vep",
    "lez",
    "nld",
    "nds-nl",
    "mrj",
    "spa",
    "ceb",
    "ina",
    "heb",
    "hun",
    "que",
    "kaa",
    "mar",
    "vec",
    "frp",
    "ell",
    "sah",
    "eus",
    "ces",
    "slk",
    "chr",
    "lij",
    "nep",
    "srd",
    "ilo",
    "be-tarask",
    "bod",
    "orm",
    "war",
    "glg",
    "mon",
    "gle",
    "min",
    "ibo",
    "ile",
    "epo",
    "lav",
    "lrc",
    "als",
    "mzn",
    "rup",
    "fur",
    "tat",
    "myv",
    "pan",
    "ton",
    "kom",
    "wuu",
    "tcy",
    "tuk",
    "kan",
    "ltg",
]


class Wili_2018(datasets.GeneratorBasedBuilder):
    """WiLI Language Identification Dataset"""

    VERSION = datasets.Version("1.1.0")

    BUILDER_CONFIGS = [
        datasets.BuilderConfig(
            name="WiLI-2018 dataset",
            version=VERSION,
            description="Plain text of import of WiLI-2018",
        )
    ]

    def _info(self):

        return datasets.DatasetInfo(
            # This is the description that will appear on the datasets page.
            description=_DESCRIPTION,
            # This defines the different columns of the dataset and their types
            features=datasets.Features(
                {"sentence": datasets.Value("string"), "label": datasets.features.ClassLabel(names=_CLASSES)}
            ),
            supervised_keys=None,
            homepage=_HOMEPAGE,
            license=_LICENSE,
            citation=_CITATION,
            task_templates=[TextClassification(text_column="sentence", label_column="label")],
        )

    def _split_generators(self, dl_manager):
        train_path = dl_manager.download_and_extract(_TRAIN_DOWNLOAD_URL)
        test_path = dl_manager.download_and_extract(_TEST_DOWNLOAD_URL)
        return [
            datasets.SplitGenerator(name=datasets.Split.TRAIN, gen_kwargs={"filepath": train_path}),
            datasets.SplitGenerator(name=datasets.Split.TEST, gen_kwargs={"filepath": test_path}),
        ]

    def _generate_examples(self, filepath):

        with open(filepath, encoding="utf-8") as f:
            for id_, line in enumerate(f):
                text, label = line.rsplit(",", 1)
                text = text.strip('"')
                label = int(label.strip())
                yield id_, {"sentence": text, "label": label - 1}
