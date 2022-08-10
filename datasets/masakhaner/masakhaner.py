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
"""MasakhaNER: Named Entity Recognition for African Languages"""

import datasets


logger = datasets.logging.get_logger(__name__)


_CITATION = """\
@article{Adelani2021MasakhaNERNE,
  title={MasakhaNER: Named Entity Recognition for African Languages},
  author={D. Adelani and Jade Abbott and Graham Neubig and Daniel D'Souza and Julia Kreutzer and Constantine Lignos
  and Chester Palen-Michel and Happy Buzaaba and Shruti Rijhwani and Sebastian Ruder and Stephen Mayhew and
  Israel Abebe Azime and S. Muhammad and Chris C. Emezue and Joyce Nakatumba-Nabende and Perez Ogayo and
  Anuoluwapo Aremu and Catherine Gitau and Derguene Mbaye and J. Alabi and Seid Muhie Yimam and Tajuddeen R. Gwadabe and
  Ignatius Ezeani and Rubungo Andre Niyongabo and Jonathan Mukiibi and V. Otiende and Iroro Orife and Davis David and
  Samba Ngom and Tosin P. Adewumi and Paul Rayson and Mofetoluwa Adeyemi and Gerald Muriuki and Emmanuel Anebi and
  C. Chukwuneke and N. Odu and Eric Peter Wairagala and S. Oyerinde and Clemencia Siro and Tobius Saul Bateesa and
  Temilola Oloyede and Yvonne Wambui and Victor Akinode and Deborah Nabagereka and Maurice Katusiime and
  Ayodele Awokoya and Mouhamadane Mboup and D. Gebreyohannes and Henok Tilaye and Kelechi Nwaike and Degaga Wolde and
   Abdoulaye Faye and Blessing Sibanda and Orevaoghene Ahia and Bonaventure F. P. Dossou and Kelechi Ogueji and
   Thierno Ibrahima Diop and A. Diallo and Adewale Akinfaderin and T. Marengereke and Salomey Osei},
  journal={ArXiv},
  year={2021},
  volume={abs/2103.11811}
}
"""

_DESCRIPTION = """\
MasakhaNER is the first large publicly available high-quality dataset for named entity recognition (NER) in ten African languages.

Named entities are phrases that contain the names of persons, organizations, locations, times and quantities.

Example:
[PER Wolff] , currently a journalist in [LOC Argentina] , played with [PER Del Bosque] in the final years of the seventies in [ORG Real Madrid] .
MasakhaNER is a named entity dataset consisting of PER, ORG, LOC, and DATE entities annotated by Masakhane for ten African languages:
- Amharic
- Hausa
- Igbo
- Kinyarwanda
- Luganda
- Luo
- Nigerian-Pidgin
- Swahili
- Wolof
- Yoruba

The train/validation/test sets are available for all the ten languages.

For more details see https://arxiv.org/abs/2103.11811
"""

_URL = "https://github.com/masakhane-io/masakhane-ner/raw/main/data/"
_TRAINING_FILE = "train.txt"
_DEV_FILE = "dev.txt"
_TEST_FILE = "test.txt"


class MasakhanerConfig(datasets.BuilderConfig):
    """BuilderConfig for Masakhaner"""

    def __init__(self, **kwargs):
        """BuilderConfig for Masakhaner.

        Args:
          **kwargs: keyword arguments forwarded to super.
        """
        super(MasakhanerConfig, self).__init__(**kwargs)


class Masakhaner(datasets.GeneratorBasedBuilder):
    """Masakhaner dataset."""

    BUILDER_CONFIGS = [
        MasakhanerConfig(name="amh", version=datasets.Version("1.0.0"), description="Masakhaner Amharic dataset"),
        MasakhanerConfig(name="hau", version=datasets.Version("1.0.0"), description="Masakhaner Hausa dataset"),
        MasakhanerConfig(name="ibo", version=datasets.Version("1.0.0"), description="Masakhaner Igbo dataset"),
        MasakhanerConfig(name="kin", version=datasets.Version("1.0.0"), description="Masakhaner Kinyarwanda dataset"),
        MasakhanerConfig(name="lug", version=datasets.Version("1.0.0"), description="Masakhaner Luganda dataset"),
        MasakhanerConfig(name="luo", version=datasets.Version("1.0.0"), description="Masakhaner Luo dataset"),
        MasakhanerConfig(
            name="pcm", version=datasets.Version("1.0.0"), description="Masakhaner Nigerian-Pidgin dataset"
        ),
        MasakhanerConfig(name="swa", version=datasets.Version("1.0.0"), description="Masakhaner Swahili dataset"),
        MasakhanerConfig(name="wol", version=datasets.Version("1.0.0"), description="Masakhaner Wolof dataset"),
        MasakhanerConfig(name="yor", version=datasets.Version("1.0.0"), description="Masakhaner Yoruba dataset"),
    ]

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "id": datasets.Value("string"),
                    "tokens": datasets.Sequence(datasets.Value("string")),
                    "ner_tags": datasets.Sequence(
                        datasets.features.ClassLabel(
                            names=[
                                "O",
                                "B-PER",
                                "I-PER",
                                "B-ORG",
                                "I-ORG",
                                "B-LOC",
                                "I-LOC",
                                "B-DATE",
                                "I-DATE",
                            ]
                        )
                    ),
                }
            ),
            supervised_keys=None,
            homepage="https://arxiv.org/abs/2103.11811",
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        urls_to_download = {
            "train": f"{_URL}{self.config.name}/{_TRAINING_FILE}",
            "dev": f"{_URL}{self.config.name}/{_DEV_FILE}",
            "test": f"{_URL}{self.config.name}/{_TEST_FILE}",
        }
        downloaded_files = dl_manager.download_and_extract(urls_to_download)

        return [
            datasets.SplitGenerator(name=datasets.Split.TRAIN, gen_kwargs={"filepath": downloaded_files["train"]}),
            datasets.SplitGenerator(name=datasets.Split.VALIDATION, gen_kwargs={"filepath": downloaded_files["dev"]}),
            datasets.SplitGenerator(name=datasets.Split.TEST, gen_kwargs={"filepath": downloaded_files["test"]}),
        ]

    def _generate_examples(self, filepath):
        logger.info("⏳ Generating examples from = %s", filepath)
        with open(filepath, encoding="utf-8") as f:
            guid = 0
            tokens = []
            ner_tags = []
            for line in f:
                if line == "" or line == "\n":
                    if tokens:
                        yield guid, {
                            "id": str(guid),
                            "tokens": tokens,
                            "ner_tags": ner_tags,
                        }
                        guid += 1
                        tokens = []
                        ner_tags = []
                else:
                    # Masakhaner tokens are space separated
                    splits = line.split(" ")
                    tokens.append(splits[0])
                    ner_tags.append(splits[1].rstrip())
            # last example
            if tokens:
                yield guid, {
                    "id": str(guid),
                    "tokens": tokens,
                    "ner_tags": ner_tags,
                }
