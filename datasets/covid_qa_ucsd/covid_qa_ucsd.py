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
"""Covid Dialog dataset in English and Chinese"""


import copy
import os
import re
import textwrap

import datasets


# BibTeX citation
_CITATION = """\
@article{ju2020CovidDialog,
  title={CovidDialog: Medical Dialogue Datasets about COVID-19},
  author={Ju, Zeqian and Chakravorty, Subrato and He, Xuehai and Chen, Shu and Yang, Xingyi and Xie, Pengtao},
  journal={ https://github.com/UCSD-AI4H/COVID-Dialogue},
  year={2020}
}
"""

# Official description of the dataset
_DESCRIPTION = textwrap.dedent(
    """
    COVID-Dialogue-Dataset is amedical dialogue dataset about COVID-19 and other types of pneumonia.
    Patients who are concerned that they may be infected by COVID-19 or other pneumonia consult doctors and doctors provide advice.
    There are 603 consultations in English and 1393 consultations in Chinese.
    """
)

# Link to an official homepage for the dataset here
_HOMEPAGE = "https://github.com/UCSD-AI4H/COVID-Dialogue"

_LICENSE = ""
_CHINESE_QA = "COVID-Dialogue-Dataset-Chinese.txt"
_ENGLISH_QA = "COVID-Dialogue-Dataset-English.txt"


class CovidQaUcsd(datasets.GeneratorBasedBuilder):
    """Dataset has one file having consulatations purely based on COVID queries"""

    VERSION = datasets.Version("1.0.0")

    BUILDER_CONFIGS = [
        datasets.BuilderConfig(
            name="en", version=VERSION, description="The dataset of medical dialogs related to Covid in English."
        ),
        datasets.BuilderConfig(
            name="zh", version=VERSION, description="The dataset of medical dialogs related to Covid in Chinese."
        ),
    ]

    @property
    def manual_download_instructions(self):
        return """\
                \nBoth the English and Chinese text files are present in https://github.com/UCSD-AI4H/COVID-Dialogue.
                It is present as COVID-Dialogue-Dataset-English.txt (for the english dialogues) and COVID-Dialogue-Dataset-Chinese.txt
                (for the Chinese Dialog).

                To load the dataset, simple pass the folder where the file is saved to the 'data_dir' param in the datasets.load_dataset(...) option.
                The data directory can e.g. be "/Downloads/".
                The data can then be loaded using the below command:\n
                `datasets.load_dataset("covid_qa_ucsd", name="en", data_dir="/Downloads/")`.

                Just change the 'name' parameter to 'zh' for Chinese.
                TAKE CARE NOT TO CHANGE THE NAME OF THE INPUT FILE
        """

    def _info(self):
        # This method specifies the datasets.DatasetInfo object which contains informations and typings for the dataset
        if self.config.name == "zh":  # For english dialouge data
            features = datasets.Features(
                {
                    "dialogue_id": datasets.Value("int32"),
                    "dialogue_url": datasets.Value("string"),
                    "dialogue_turns": datasets.Sequence(
                        {
                            "speaker": datasets.ClassLabel(names=["病人", "医生"]),
                            "utterance": datasets.Value("string"),
                        }
                    ),
                }
            )

        if self.config.name == "en":  # For english dialouge data
            features = datasets.Features(
                {
                    "dialogue_id": datasets.Value("int32"),
                    "dialogue_url": datasets.Value("string"),
                    "dialogue_turns": datasets.Sequence(
                        {
                            "speaker": datasets.ClassLabel(names=["Patient", "Doctor"]),
                            "utterance": datasets.Value("string"),
                        }
                    ),
                }
            )

        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=features,
            supervised_keys=None,
            homepage=_HOMEPAGE,
            license=_LICENSE,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        if self.config.name == "zh":
            path_to_manual_file = os.path.join(os.path.abspath(os.path.expanduser(dl_manager.manual_dir)), _CHINESE_QA)
        if self.config.name == "en":
            path_to_manual_file = os.path.join(os.path.abspath(os.path.expanduser(dl_manager.manual_dir)), _ENGLISH_QA)

        if not os.path.exists(path_to_manual_file):
            raise FileNotFoundError(
                f"{path_to_manual_file} does not exist. Make sure the file is present in the directory specified in the data_dir specified in the input {dl_manager.manual_dir} `datasets.load_dataset('covid_qa_ucsd', 'en', data_dir=...)`. Manual download instructions: {self.manual_download_instructions})"
            )

        return [datasets.SplitGenerator(name=datasets.Split.TRAIN, gen_kwargs={"filepath": path_to_manual_file})]

    def _generate_examples(self, filepath):
        """Yields examples. Iterates over the file and creates appropriate dialogue data

        NOTE:
        - The code makes some assumption on the structure of the raw .txt file.
        - There are some checks to separate different id's. Hopefully, should not cause further issues later when more txt files are added.
        """
        data_lang = self.config.name
        id_ = -1
        with open(filepath, encoding="utf-8") as f_in:
            # Parameters to just "sectionize" the raw data
            last_part = ""
            last_dialog = {}
            last_list = []
            last_user = ""
            check_list = []

            # These flags are present to have a single function address both chinese and english data
            # English data is a little hahazard (i.e. the sentences spans multiple different lines),
            # Chinese is compact with one line for doctor and patient.
            conv_flag = False
            des_flag = False

            while True:
                line = f_in.readline()
                if not line:
                    break

                # Extracting the dialog id
                if line[:2] == "id":  # Hardcode alert!
                    # Handling ID references that may come in the description
                    # These were observed in the Chinese dataset and were not
                    # followed by numbers
                    try:
                        dialogue_id = int(re.findall(r"\d+", line)[0])
                    except IndexError:
                        continue

                # Extracting the url
                if line[:4] == "http":  # Hardcode alert!
                    dialogue_url = line.rstrip()

                # Extracting the patient info from description.
                if line[:11] == "Description":  # Hardcode alert!
                    last_part = "description"
                    last_dialog = {}
                    last_list = []
                    last_user = ""
                    last_conv = {"speaker": "", "utterance": ""}
                    while True:
                        line = f_in.readline()
                        if (not line) or (line in ["\n", "\n\r"]):
                            break
                        else:
                            if data_lang == "zh":  # Condition in chinese
                                if line[:5] == "病情描述：":  # Hardcode alert!
                                    last_user = "病人"
                                    sen = line[6:].rstrip()
                                    des_flag = True

                            if data_lang == "en":
                                last_user = "Patient"
                                sen = line.rstrip()
                                des_flag = True

                            if des_flag:
                                if sen == "":
                                    continue
                                if sen in check_list:
                                    last_conv["speaker"] = ""
                                    last_conv["utterance"] = ""
                                else:
                                    last_conv["speaker"] = last_user
                                    last_conv["utterance"] = sen
                                    check_list.append(sen)
                                des_flag = False
                                break

                # Extracting the conversation info from dialogue.
                elif line[:8] == "Dialogue":  # Hardcode alert!
                    if last_part == "description" and len(last_conv["utterance"]) > 0:
                        last_part = "dialogue"
                        if data_lang == "zh":
                            last_user = "病人"

                        if data_lang == "en":
                            last_user = "Patient"

                        while True:
                            line = f_in.readline()
                            if (not line) or (line in ["\n", "\n\r"]):
                                conv_flag = False
                                last_user = ""
                                last_list.append(copy.deepcopy(last_conv))
                                # To ensure close of conversation, only even number of sentences
                                # are extracted
                                last_turn = len(last_list)
                                if int(last_turn / 2) > 0:
                                    temp = int(last_turn / 2)
                                    id_ += 1
                                    last_dialog["dialogue_id"] = dialogue_id
                                    last_dialog["dialogue_url"] = dialogue_url
                                    last_dialog["dialogue_turns"] = last_list[: temp * 2]
                                    yield id_, last_dialog
                                break

                            if data_lang == "zh":
                                if line[:3] == "病人：" or line[:3] == "医生：":  # Hardcode alert!
                                    user = line[:2]  # Hardcode alert!
                                    line = f_in.readline()
                                    conv_flag = True

                            # The elif block is to ensure that multi-line sentences are captured.
                            # This has been observed only in english.
                            if data_lang == "en":
                                if line.strip() == "Patient:" or line.strip() == "Doctor:":  # Hardcode alert!
                                    user = line.replace(":", "").rstrip()
                                    line = f_in.readline()
                                    conv_flag = True
                                elif line[:2] != "id":  # Hardcode alert!
                                    conv_flag = True

                            # Continues till the next ID is parsed
                            if conv_flag:
                                sen = line.rstrip()
                                if sen == "":
                                    continue

                                if user == last_user:
                                    last_conv["utterance"] = last_conv["utterance"] + sen
                                else:
                                    last_user = user
                                    last_list.append(copy.deepcopy(last_conv))
                                    last_conv["utterance"] = sen
                                    last_conv["speaker"] = user
