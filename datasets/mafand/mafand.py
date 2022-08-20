# coding=utf-8
# Copyright 2020 HuggingFace Datasets Authors.
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
"""MAFAND-MT: Masakhane Anglo and Franco Africa News Dataset for Machine Translation"""

import datasets
import json

logger = datasets.logging.get_logger(__name__)

_CITATION = """\
@inproceedings{adelani-etal-2022-thousand,
    title = "A Few Thousand Translations Go a Long Way! Leveraging Pre-trained Models for {A}frican News Translation",
    author = "Adelani, David  and
      Alabi, Jesujoba  and
      Fan, Angela  and
      Kreutzer, Julia  and
      Shen, Xiaoyu  and
      Reid, Machel  and
      Ruiter, Dana  and
      Klakow, Dietrich  and
      Nabende, Peter  and
      Chang, Ernie  and
      Gwadabe, Tajuddeen  and
      Sackey, Freshia  and
      Dossou, Bonaventure F. P.  and
      Emezue, Chris  and
      Leong, Colin  and
      Beukman, Michael  and
      Muhammad, Shamsuddeen  and
      Jarso, Guyo  and
      Yousuf, Oreen  and
      Niyongabo Rubungo, Andre  and
      Hacheme, Gilles  and
      Wairagala, Eric Peter  and
      Nasir, Muhammad Umair  and
      Ajibade, Benjamin  and
      Ajayi, Tunde  and
      Gitau, Yvonne  and
      Abbott, Jade  and
      Ahmed, Mohamed  and
      Ochieng, Millicent  and
      Aremu, Anuoluwapo  and
      Ogayo, Perez  and
      Mukiibi, Jonathan  and
      Ouoba Kabore, Fatoumata  and
      Kalipe, Godson  and
      Mbaye, Derguene  and
      Tapo, Allahsera Auguste  and
      Memdjokam Koagne, Victoire  and
      Munkoh-Buabeng, Edwin  and
      Wagner, Valencia  and
      Abdulmumin, Idris  and
      Awokoya, Ayodele  and
      Buzaaba, Happy  and
      Sibanda, Blessing  and
      Bukula, Andiswa  and
      Manthalu, Sam",
    booktitle = "Proceedings of the 2022 Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies",
    month = jul,
    year = "2022",
    address = "Seattle, United States",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/2022.naacl-main.223",
    doi = "10.18653/v1/2022.naacl-main.223",
    pages = "3053--3070",
    abstract = "Recent advances in the pre-training for language models leverage large-scale datasets to create multilingual models. However, low-resource languages are mostly left out in these datasets. This is primarily because many widely spoken languages that are not well represented on the web and therefore excluded from the large-scale crawls for datasets. Furthermore, downstream users of these models are restricted to the selection of languages originally chosen for pre-training. This work investigates how to optimally leverage existing pre-trained models to create low-resource translation systems for 16 African languages. We focus on two questions: 1) How can pre-trained models be used for languages not included in the initial pretraining? and 2) How can the resulting translation models effectively transfer to new domains? To answer these questions, we create a novel African news corpus covering 16 languages, of which eight languages are not part of any existing evaluation dataset. We demonstrate that the most effective strategy for transferring both additional languages and additional domains is to leverage small quantities of high-quality translation data to fine-tune large pre-trained models.",
}
"""

_DESCRIPTION = """\
MAFAND-MT is the largest MT benchmark for African languages in the news domain, covering 21 languages. The languages covered are:
- Amharic
- Bambara
- Ghomala
- Ewe
- Fon
- Hausa
- Igbo
- Kinyarwanda
- Luganda
- Luo
- Mossi
- Nigerian-Pidgin
- Chichewa
- Shona
- Swahili
- Setswana
- Twi
- Wolof
- Xhosa
- Yoruba
- Zulu

The train/validation/test sets are available for 16 languages, and validation/test set for amh, kin, nya, sna, and xho

For more details see https://aclanthology.org/2022.naacl-main.223/
"""

_URL = "https://raw.githubusercontent.com/masakhane-io/lafand-mt/main/data/json_files/"
_TRAINING_FILE = "train.json"
_DEV_FILE = "dev.json"
_TEST_FILE = "test.json"


class MafandConfig(datasets.BuilderConfig):
    """BuilderConfig for Mafand"""

    def __init__(self, **kwargs):
        """BuilderConfig for Masakhaner.
        Args:
          **kwargs: keyword arguments forwarded to super.
        """
        super(MafandConfig, self).__init__(**kwargs)


class Mafand(datasets.GeneratorBasedBuilder):
    """Mafand dataset."""
    BUILDER_CONFIGS = [
        MafandConfig(name="en-amh", version=datasets.Version("1.0.0"),
                     description="Mafand English-Amharic dataset"),
        MafandConfig(name="en-hau", version=datasets.Version("1.0.0"),
                     description="Mafand English-Hausa dataset"),
        MafandConfig(name="en-ibo", version=datasets.Version("1.0.0"),
                     description="Mafand English-Igbo dataset"),
        MafandConfig(name="en-kin", version=datasets.Version("1.0.0"),
                     description="Mafand English-Kinyarwanda dataset"),
        MafandConfig(name="en-lug", version=datasets.Version("1.0.0"),
                     description="Mafand English-Luganda dataset"),
        MafandConfig(name="en-nya", version=datasets.Version("1.0.0"),
                     description="Mafand English-Chichewa dataset"),
        MafandConfig(name="en-pcm", version=datasets.Version("1.0.0"),
                     description="Mafand English-Naija dataset"),
        MafandConfig(name="en-sna", version=datasets.Version("1.0.0"),
                     description="Mafand English-Shona dataset"),
        MafandConfig(name="en-swa", version=datasets.Version("1.0.0"),
                     description="Mafand English-Swahili dataset"),
        MafandConfig(name="en-tsn", version=datasets.Version("1.0.0"),
                     description="Mafand English-Setswana dataset"),
        MafandConfig(name="en-twi", version=datasets.Version("1.0.0"),
                     description="Mafand English-Twi dataset"),
        MafandConfig(name="en-xho", version=datasets.Version("1.0.0"),
                     description="Mafand English-Xhosa dataset"),
        MafandConfig(name="en-yor", version=datasets.Version("1.0.0"),
                     description="Mafand English-Yoruba dataset"),
        MafandConfig(name="en-zul", version=datasets.Version("1.0.0"),
                     description="Mafand English-Zulu dataset"),
        MafandConfig(name="fr-bam", version=datasets.Version("1.0.0"),
                     description="Mafand French-Bambara dataset"),
        MafandConfig(name="fr-bbj", version=datasets.Version("1.0.0"),
                     description="Mafand French-Ghomala dataset"),
        MafandConfig(name="fr-ewe", version=datasets.Version("1.0.0"),
                     description="Mafand French-Ewe dataset"),
        MafandConfig(name="fr-fon", version=datasets.Version("1.0.0"),
                     description="Mafand French-Fon dataset"),
        MafandConfig(name="fr-mos", version=datasets.Version("1.0.0"),
                     description="Mafand French-Mossi dataset"),
        MafandConfig(name="fr-wol", version=datasets.Version("1.0.0"),
                     description="Mafand French-Wolof dataset"),
    ]

    def _info(self):
        source, target = self.config.name.split('-')
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features({"translation": datasets.features.Translation(languages=(source, target))}),
            supervised_keys=(source, target),
            homepage="https://github.com/masakhane-io/lafand-mt",
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        source, target = self.config.name.split('-')
        if target in ['amh', 'kin', 'nya', 'sna', 'xho']:
            urls_to_download = {
                "dev": f"{_URL}{self.config.name}/{_DEV_FILE}",
                "test": f"{_URL}{self.config.name}/{_TEST_FILE}",
            }
            downloaded_files = dl_manager.download_and_extract(urls_to_download)
            return [
                datasets.SplitGenerator(name=datasets.Split.VALIDATION,
                                        gen_kwargs={"filepath": downloaded_files["dev"]}),
                datasets.SplitGenerator(name=datasets.Split.TEST,
                                        gen_kwargs={"filepath": downloaded_files["test"]}),
            ]
        else:
            urls_to_download = {
                "train": f"{_URL}{self.config.name}/{_TRAINING_FILE}",
                "dev": f"{_URL}{self.config.name}/{_DEV_FILE}",
                "test": f"{_URL}{self.config.name}/{_TEST_FILE}",
            }
            downloaded_files = dl_manager.download_and_extract(urls_to_download)

            return [
                datasets.SplitGenerator(name=datasets.Split.TRAIN,
                                        gen_kwargs={"filepath": downloaded_files["train"]}),
                datasets.SplitGenerator(name=datasets.Split.VALIDATION,
                                        gen_kwargs={"filepath": downloaded_files["dev"]}),
                datasets.SplitGenerator(name=datasets.Split.TEST,
                                        gen_kwargs={"filepath": downloaded_files["test"]}),
            ]

    def _generate_examples(self, filepath):
        logger.info("⏳ Generating examples from = %s", filepath)
        with open(filepath, encoding="utf-8") as f:
            idx = 0
            for line in f:
                src_tgt = json.loads(line)
                yield idx, src_tgt
                idx += 1
