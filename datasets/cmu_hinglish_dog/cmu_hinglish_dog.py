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
_URL_ENGLISH = "https://github.com/festvox/datasets-CMU_DoG/archive/master.zip"


class CMUHinglishDoG(datasets.GeneratorBasedBuilder):
    """Load the CMU Hinglish DoG Data for MT"""

    def _info(self):
        features = datasets.Features(
            {
                "hi_en": datasets.Value("string"),
                "en": datasets.Value("string"),
                "uid": datasets.Value("string"),
                "docIdx": datasets.Value("int64"),
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

        my_urls = {
            "train": os.path.join(data_dir_hi_en, "train"),
            "valid": os.path.join(data_dir_hi_en, "valid"),
            "test": os.path.join(data_dir_hi_en, "test"),
        }

        for split in ["train", "valid", "test"]:
            english_files = os.listdir(os.path.join(data_dir_en, "train"))
            hinglish_files = os.listdir(my_urls[split])
            sentences = []
            for f in hinglish_files:
                en_file_path = f.split(".json")[0] + ".json"

                if en_file_path in english_files:
                    en = json.load(open(os.path.join(data_dir_en, "train", en_file_path)))
                    hi_en = json.load(open(os.path.join(my_urls[split], f)))

                    assert len(en["history"]) == len(hi_en["history"])
                    for x, y in zip(en["history"], hi_en["history"]):
                        assert x["docIdx"] == y["docIdx"]
                        assert x["uid"] == y["uid"]
                        assert x["utcTimestamp"] == y["utcTimestamp"]

                        x["text"] = re.sub("\t|\n", " ", x["text"])
                        y["text"] = re.sub("\t|\n", " ", y["text"])
                        to_append = {"uid": x["uid"], "docIdx": x["docIdx"], "hi_en": y["text"], "en": x["text"]}

                        sentences.append(to_append)

            f = open(my_urls[split] + ".txt", "w", encoding="utf-8")
            for _sentence in sentences:
                json.dump(_sentence, f)
                f.write("\n")

        return [
            datasets.SplitGenerator(name=datasets.Split.TRAIN, gen_kwargs={"filepath": my_urls["train"] + ".txt"}),
            datasets.SplitGenerator(name=datasets.Split.TEST, gen_kwargs={"filepath": my_urls["valid"] + ".txt"}),
            datasets.SplitGenerator(name=datasets.Split.VALIDATION, gen_kwargs={"filepath": my_urls["test"] + ".txt"}),
        ]

    def _generate_examples(self, filepath):
        """Yields examples."""
        with open(filepath, encoding="utf-8") as f:

            for key, line in enumerate(f):
                line = json.loads(line)
                yield key, line
