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

import json
import os
import re

import datasets


_CITATION = """\
@inproceedings{cmu_dog_emnlp18,
    title={A Dataset for Document Grounded Conversations},
    author={Zhou, Kangyan and Prabhumoye, Shrimai and Black, Alan W},
    year={2018},
    booktitle={Proceedings of the 2018 Conference on Empirical Methods in Natural Language Processing}
}

@inproceedings{khanuja-etal-2020-gluecos,
    title = "{GLUEC}o{S}: An Evaluation Benchmark for Code-Switched {NLP}",
    author = "Khanuja, Simran  and
      Dandapat, Sandipan  and
      Srinivasan, Anirudh  and
      Sitaram, Sunayana  and
      Choudhury, Monojit",
    booktitle = "Proceedings of the 58th Annual Meeting of the Association for Computational Linguistics",
    month = jul,
    year = "2020",
    address = "Online",
    publisher = "Association for Computational Linguistics",
    url = "https://www.aclweb.org/anthology/2020.acl-main.329",
    pages = "3575--3585"
}
"""

_DESCRIPTION = """\
This is a collection of text conversations in Hinglish (code mixing between Hindi-English) and their corresponding English only versions. Can be used for Translating between the two.
"""

_HOMEPAGE = "http://festvox.org/cedar/data/notyet/"
_URL_HINGLISH = "http://festvox.org/cedar/data/notyet/CMUHinglishDoG.zip"
_URL_ENGLISH = "https://github.com/festvox/datasets-CMU_DoG/archive/master/Conversations.zip"


class CMUHinglishDoG(datasets.GeneratorBasedBuilder):
    """Load the CMU Hinglish DoG Data for MT"""

    def _info(self):
        features = datasets.Features(
            {
                "date": datasets.Value("string"),
                "docIdx": datasets.Value("int64"),
                "translation": datasets.Translation(languages=["en", "hi_en"]),
                "uid": datasets.Value("string"),
                "utcTimestamp": datasets.Value("string"),
                "rating": datasets.Value("int64"),
                "status": datasets.Value("int64"),
                "uid1LogInTime": datasets.Value("string"),
                "uid1LogOutTime": datasets.Value("string"),
                "uid1response": {
                    "response": datasets.Sequence(datasets.Value("int64")),
                    "type": datasets.Value("string"),
                },
                "uid2response": {
                    "response": datasets.Sequence(datasets.Value("int64")),
                    "type": datasets.Value("string"),
                },
                "user2_id": datasets.Value("string"),
                "whoSawDoc": datasets.Sequence(datasets.Value("string")),
                "wikiDocumentIdx": datasets.Value("int64"),
            }
        )
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=features,
            supervised_keys=None,
            homepage=_HOMEPAGE,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """The linking part between Hinglish data and English data is inspired from the implementation in GLUECoS.
        Refer here for the original script https://github.com/microsoft/GLUECoS/blob/7fdc51653e37a32aee17505c47b7d1da364fa77e/Data/Preprocess_Scripts/preprocess_mt_en_hi.py"""

        eng_path = dl_manager.download_and_extract(_URL_ENGLISH)
        data_dir_en = os.path.join(eng_path, "datasets-CMU_DoG-master", "Conversations")

        hi_en_path = dl_manager.download_and_extract(_URL_HINGLISH)
        data_dir_hi_en = os.path.join(hi_en_path, "CMUHinglishDoG", "Conversations_Hinglish")

        hi_en_dirs = {
            "train": os.path.join(data_dir_hi_en, "train"),
            "valid": os.path.join(data_dir_hi_en, "valid"),
            "test": os.path.join(data_dir_hi_en, "test"),
        }

        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={
                    "hi_en_dir": hi_en_dirs["train"],
                    "data_dir_en": data_dir_en,
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                gen_kwargs={
                    "hi_en_dir": hi_en_dirs["test"],
                    "data_dir_en": data_dir_en,
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                gen_kwargs={
                    "hi_en_dir": hi_en_dirs["valid"],
                    "data_dir_en": data_dir_en,
                },
            ),
        ]

    def _generate_examples(self, hi_en_dir, data_dir_en):
        """Yields examples."""
        english_files_train = os.listdir(os.path.join(data_dir_en, "train"))
        english_files_val = os.listdir(os.path.join(data_dir_en, "valid"))
        english_files_test = os.listdir(os.path.join(data_dir_en, "test"))

        hinglish_files = os.listdir(hi_en_dir)
        key = 0
        for f in hinglish_files:
            en_file_path = f.split(".json")[0] + ".json"
            found = True
            # Looks for the corresponding english file in all 3 splits
            if en_file_path in english_files_train:
                en = json.load(open(os.path.join(os.path.join(data_dir_en, "train"), en_file_path)))
            elif en_file_path in english_files_val:
                en = json.load(open(os.path.join(os.path.join(data_dir_en, "valid"), en_file_path)))
            elif en_file_path in english_files_test:
                en = json.load(open(os.path.join(os.path.join(data_dir_en, "test"), en_file_path)))
            else:
                found = False
            if found:
                hi_en = json.load(open(os.path.join(hi_en_dir, f)))

                assert len(en["history"]) == len(hi_en["history"])

                for x, y in zip(en["history"], hi_en["history"]):
                    assert x["docIdx"] == y["docIdx"]
                    assert x["uid"] == y["uid"]
                    assert x["utcTimestamp"] == y["utcTimestamp"]

                    x["text"] = re.sub("\t|\n", " ", x["text"])
                    y["text"] = re.sub("\t|\n", " ", y["text"])
                    line = {
                        "date": hi_en["date"],
                        "uid": x["uid"],
                        "docIdx": x["docIdx"],
                        "utcTimestamp": x["utcTimestamp"],
                        "translation": {"hi_en": y["text"], "en": x["text"]},
                        "rating": hi_en["rating"],
                        "status": hi_en["status"],
                        "uid1LogOutTime": hi_en.get("uid1LogOutTime"),
                        "uid1LogInTime": hi_en["uid1LogInTime"],
                        "uid1response": {
                            "response": hi_en["uid1response"]["response"] if "uid1response" in hi_en else [],
                            "type": hi_en["uid1response"]["type"] if "uid1response" in hi_en else None,
                        },
                        "uid2response": {
                            "response": hi_en["uid2response"]["response"] if "uid2response" in hi_en else [],
                            "type": hi_en["uid2response"]["type"] if "uid2response" in hi_en else None,
                        },
                        "user2_id": hi_en["user2_id"],
                        "whoSawDoc": hi_en["whoSawDoc"],
                        "wikiDocumentIdx": hi_en["wikiDocumentIdx"],
                    }

                    yield key, line
                    key += 1
