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
"""Medical Dialog dataset in english and chinese"""


import copy
import os
import re

import datasets


_CITATION = """\
@article{chen2020meddiag,
  title={MedDialog: a large-scale medical dialogue dataset},
  author={Chen, Shu and Ju, Zeqian and Dong, Xiangyu and Fang, Hongchao and Wang, Sicheng and Yang, Yue and Zeng, Jiaqi and Zhang, Ruisi and Zhang, Ruoyu and Zhou, Meng and Zhu, Penghui and Xie, Pengtao},
  journal={arXiv preprint arXiv:2004.03329},
  year={2020}
}
"""


_DESCRIPTION = """\
The MedDialog dataset (English) contains conversations (in English) between doctors and patients.\
It has 0.26 million dialogues. The data is continuously growing and more dialogues will be added. \
The raw dialogues are from healthcaremagic.com and icliniq.com.\

All copyrights of the data belong to healthcaremagic.com and icliniq.com.
"""

_HOMEPAGE = "https://github.com/UCSD-AI4H/Medical-Dialogue-System"

_LICENSE = ""


class MedicalDialog(datasets.GeneratorBasedBuilder):
    VERSION = datasets.Version("1.0.0")

    BUILDER_CONFIGS = [
        datasets.BuilderConfig(name="en", description="The dataset of medical dialogs in English.", version=VERSION),
        datasets.BuilderConfig(name="zh", description="The dataset of medical dialogs in Chinese.", version=VERSION),
    ]

    @property
    def manual_download_instructions(self):
        return """\
    \n  For English:\nYou need to go to https://drive.google.com/drive/folders/1g29ssimdZ6JzTST6Y8g6h-ogUNReBtJD?usp=sharing,\
    and manually download the dataset from Google Drive. Once it is completed,
    a file named Medical-Dialogue-Dataset-English-<timestamp-info>.zip will appear in your Downloads folder(
    or whichever folder your browser chooses to save files to). Unzip the folder to obtain
    a folder named "Medical-Dialogue-Dataset-English" several text files.

    Now, you can specify the path to this folder for the data_dir argument in the
    datasets.load_dataset(...) option.
    The <path/to/folder> can e.g. be "/Downloads/Medical-Dialogue-Dataset-English".
    The data can then be loaded using the below command:\
         `datasets.load_dataset("medical_dialog", name="en", data_dir="/Downloads/Medical-Dialogue-Dataset-English")`.

    \n  For Chinese:\nFollow the above process. Change the 'name' to 'zh'.The download link is https://drive.google.com/drive/folders/1r09_i8nJ9c1nliXVGXwSqRYqklcHd9e2

    **NOTE**
    - A caution while downloading from drive. It is better to download single files since creating a zip might not include files <500 MB. This has been observed mutiple times.
    - After downloading the files and adding them to the appropriate folder, the path of the folder can be given as input tu the data_dir path.
    """

    def _info(self):
        if self.config.name == "zh":
            features = datasets.Features(
                {
                    "file_name": datasets.Value("string"),
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

        if self.config.name == "en":
            features = datasets.Features(
                {
                    "file_name": datasets.Value("string"),
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
            # This is the description that will appear on the datasets page.
            description=_DESCRIPTION,
            features=features,
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
        path_to_manual_file = os.path.abspath(os.path.expanduser(dl_manager.manual_dir))
        if not os.path.exists(path_to_manual_file):
            raise FileNotFoundError(
                f"{path_to_manual_file} does not exist. Make sure you insert a manual dir via `datasets.load_dataset('medical_dialog', data_dir=...)`. Manual download instructions: {self.manual_download_instructions})"
            )

        filepaths = [
            os.path.join(path_to_manual_file, txt_file_name)
            for txt_file_name in sorted(os.listdir(path_to_manual_file))
            if txt_file_name.endswith("txt")
        ]

        return [datasets.SplitGenerator(name=datasets.Split.TRAIN, gen_kwargs={"filepaths": filepaths})]

    def _generate_examples(self, filepaths):
        """Yields examples. Iterates over each file and give the creates the corresponding features.

        NOTE:
        - The code makes some assumption on the structure of the raw .txt file.
        - There are some checks to separate different id's. Hopefully, should not cause further issues later when more txt files are added.
        """
        data_lang = self.config.name
        id_ = -1
        for filepath in filepaths:
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
                                        sen = f_in.readline().rstrip()
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
                                        last_dialog["file_name"] = filepath
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
