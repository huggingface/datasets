# coding=utf-8
# Copyright 2021 The TensorFlow Datasets Authors and the HuggingFace Datasets Authors.
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

# Lint as: python3

import csv
import os

import pandas as pd

import datasets


_VERSION = "1.0.0"

_CITATION = """
@misc{wang2020covost,
    title={CoVoST 2: A Massively Multilingual Speech-to-Text Translation Corpus},
    author={Changhan Wang and Anne Wu and Juan Pino},
    year={2020},
    eprint={2007.10310},
    archivePrefix={arXiv},
    primaryClass={cs.CL}
"""

_DESCRIPTION = """
CoVoST 2, a large-scale multilingual speech translation corpus covering translations from 21 languages into English \
and from English into 15 languages. The dataset is created using Mozilla’s open source Common Voice database of \
crowdsourced voice recordings.

Note that in order to limit the required storage for preparing this dataset, the audio
is stored in the .mp3 format and is not converted to a float32 array. To convert, the audio
file to a float32 array, please make use of the `.map()` function as follows:


```python
import torchaudio

def map_to_array(batch):
    speech_array, _ = torchaudio.load(batch["file"])
    batch["speech"] = speech_array.numpy()
    return batch

dataset = dataset.map(map_to_array, remove_columns=["file"])
```
"""

_HOMEPAGE = "https://github.com/facebookresearch/covost"

# fmt: off
XX_EN_LANGUAGES = ["fr", "de", "es", "ca", "it", "ru", "zh-CN", "pt", "fa", "et", "mn", "nl", "tr", "ar", "sv-SE", "lv", "sl", "ta", "ja", "id", "cy"]
EN_XX_LANGUAGES = ["de", "tr", "fa", "sv-SE", "mn", "zh-CN", "cy", "ca", "sl", "et", "id", "ar", "ta", "lv", "ja"]
# fmt: on

COVOST_URL_TEMPLATE = "https://dl.fbaipublicfiles.com/covost/covost_v2.{src_lang}_{tgt_lang}.tsv.tar.gz"


def _get_builder_configs():
    builder_configs = [
        datasets.BuilderConfig(name=f"en_{lang}", version=datasets.Version(_VERSION)) for lang in EN_XX_LANGUAGES
    ]

    builder_configs += [
        datasets.BuilderConfig(name=f"{lang}_en", version=datasets.Version(_VERSION)) for lang in XX_EN_LANGUAGES
    ]
    return builder_configs


class Covost2(datasets.GeneratorBasedBuilder):
    """CoVOST2 Dataset."""

    VERSION = datasets.Version(_VERSION)

    BUILDER_CONFIGS = _get_builder_configs()

    @property
    def manual_download_instructions(self):
        return """\
        You should download the Common Voice v4 dataset from https://commonvoice.mozilla.org/en/datasets.
        and unpack it to a path `{COVOST_ROOT}/{SOURCE_LANG_ID}` and then pass the `{COVOST_ROOT}` path as `data_dir`
        via `datasets.load_dataset('covost2', data_dir="path/to/covost_root")`
        """

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                client_id=datasets.Value("string"),
                file=datasets.Value("string"),
                sentence=datasets.Value("string"),
                translation=datasets.Value("string"),
                id=datasets.Value("string"),
            ),
            supervised_keys=("file", "translation"),
            homepage=_HOMEPAGE,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        data_root = os.path.abspath(os.path.expanduser(dl_manager.manual_dir))
        source_lang, target_lang = self.config.name.split("_")
        source_path = os.path.join(data_root, source_lang)

        if not os.path.exists(source_path):
            raise FileNotFoundError(
                "{} does not exist. Make sure you insert a manual dir via `datasets.load_dataset('covost2', data_dir=...)` that includes files uncompressed files from the COVOST2 archive. Manual download instructions: {}".format(
                    data_dir, self.manual_download_instructions
                )

        covost_url = COVOST_URL_TEMPLATE.format(src_lang=source_lang, tgt_lang=target_lang)
        extracted_path = dl_manager.download_and_extract(covost_url)

        covost_tsv_path = os.path.join(extracted_path, f"covost_v2.{source_lang}_{target_lang}.tsv")
        cv_tsv_path = os.path.join(source_path, "validated.tsv")

        covost_tsv = self._load_df_from_tsv(covost_tsv_path)
        cv_tsv = self._load_df_from_tsv(cv_tsv_path)

        df = pd.merge(
            left=cv_tsv[["path", "sentence", "client_id"]],
            right=covost_tsv[["path", "translation", "split"]],
            how="inner",
            on="path",
        )

        train_df = df[(df["split"] == "train") | (df["split"] == f"train_covost")]
        valid_df = df[df["split"] == "dev"]
        test_df = df[df["split"] == "test"]

        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN, gen_kwargs={"df": train_df, "source_path": source_path}
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION, gen_kwargs={"df": valid_df, "source_path": source_path}
            ),
            datasets.SplitGenerator(name=datasets.Split.TEST, gen_kwargs={"df": test_df, "source_path": source_path}),
        ]

    def _generate_examples(self, df, source_path):
        for i, row in df.iterrows():
            yield i, {
                "id": row["path"].replace(".mp3", ""),
                "client_id": row["client_id"],
                "sentence": row["sentence"],
                "translation": row["translation"],
                "file": os.path.join(source_path, "clips", row["path"]),
            }

    def _load_df_from_tsv(self, path):
        return pd.read_csv(
            path,
            sep="\t",
            header=0,
            encoding="utf-8",
            escapechar="\\",
            quoting=csv.QUOTE_NONE,
            na_filter=False,
        )
