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
import shutil
from pathlib import Path
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
_URL_ENGLISH = (
    "https://github.com/festvox/datasets-CMU_DoG/archive/master/Conversations.zip"
)


class CMUHinglishDoG(datasets.GeneratorBasedBuilder):
    """Load the CMU Hinglish DoG Data for MT"""

    def _info(self):
        features = datasets.Features(
            {
                "date": datasets.Value("string"),
                "history": datasets.Sequence(
                    {
                        "docIdx": datasets.Value("int64"),
                        "text": datasets.Value("string"),
                        "uid": datasets.Value("string"),
                        "utcTimestamp": datasets.Value("string"),
                    }
                ),
                "rating": datasets.Value("int64"),
                "status": datasets.Value("int64"),
                "uid1LogInTime": datasets.Value("string"),
                "uid1LogOutTime": datasets.Value("string"),
                "uid1response": datasets.Sequence(
                    {
                        "feedback": datasets.Value("string"),
                        "response": datasets.Sequence([datasets.Value("int64")]),
                        "type": datasets.Value("string"),
                    }
                ),
                "uid2response": datasets.Sequence(
                    {
                        "feedback": datasets.Value("string"),
                        "response": datasets.Sequence([datasets.Value("int64")]),
                        "type": datasets.Value("string"),
                    }
                ),
                "user2_id": datasets.Value("string"),
                "whoSawDoc": datasets.Sequence([datasets.Value("string")]),
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

        # WikiData file is not required for this
        if os.path.isdir(os.path.join(eng_path, "datasets-CMU_DoG-master", "WikiData")):
            shutil.rmtree(os.path.join(eng_path, "datasets-CMU_DoG-master", "WikiData"))

        data_dir_en = os.path.join(eng_path, "datasets-CMU_DoG-master", "Conversations")

        hi_en_path = dl_manager.download_and_extract(_URL_HINGLISH)
        data_dir_hi_en = os.path.join(
            hi_en_path, "CMUHinglishDoG", "Conversations_Hinglish"
        )

        # Extensions in Hinglish dataset are .json_1 and .json_2, converting them to .json
        for split in os.listdir(data_dir_hi_en):
            for f in os.listdir(os.path.join(data_dir_hi_en, split)):
                f = os.path.join(os.path.join(data_dir_hi_en, split, f))
                p = Path(f)
                os.rename(f, p.with_suffix(".json"))

        hi_en_dirs = {
            "train": os.path.join(data_dir_hi_en, "train"),
            "valid": os.path.join(data_dir_hi_en, "valid"),
            "test": os.path.join(data_dir_hi_en, "test"),
        }

        en_dirs = {
            "train": os.path.join(data_dir_en, "train"),
            "valid": os.path.join(data_dir_en, "valid"),
            "test": os.path.join(data_dir_en, "test"),
        }
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={
                    "hi_en_dir": hi_en_dirs["train"],
                    "en_dir": en_dirs["train"],
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                gen_kwargs={"hi_en_dir": hi_en_dirs["test"], "en_dir": en_dirs["test"]},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                gen_kwargs={
                    "hi_en_dir": hi_en_dirs["valid"],
                    "en_dir": en_dirs["valid"],
                },
            ),
        ]

    def _generate_examples(self, hi_en_dir, en_dir):
        """Yields examples."""
        english_files = os.listdir(en_dir)
        hinglish_files = os.listdir(hi_en_dir)
        key = 0
        for f in hinglish_files:
            en_file_path = f.split(".json")[0] + ".json"

            if en_file_path in english_files:
                en = json.load(open(os.path.join(en_dir, en_file_path)))
                hi_en = json.load(open(os.path.join(hi_en_dir, f)))

                assert len(en["history"]) == len(hi_en["history"])
                for x, y in zip(en["history"], hi_en["history"]):
                    assert x["docIdx"] == y["docIdx"]
                    assert x["uid"] == y["uid"]
                    assert x["utcTimestamp"] == y["utcTimestamp"]

                    x["text"] = re.sub("\t|\n", " ", x["text"])
                    y["text"] = re.sub("\t|\n", " ", y["text"])
                    line = {
                        "uid": x["uid"],
                        "docIdx": x["docIdx"],
                        "hi_en": y["text"],
                        "en": x["text"],
                    }

                    yield key, line
                    key += 1
