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
import datasets


_DESCRIPTION = """\
Tags: PER(人名), LOC(地点名), GPE(行政区名), ORG(机构名)
Label	Tag	Meaning
PER	PER.NAM	名字（张三）
PER.NOM	代称、类别名（穷人）
LOC	LOC.NAM	特指名称（紫玉山庄）
LOC.NOM	泛称（大峡谷、宾馆）
GPE	GPE.NAM	行政区的名称（北京）
ORG	ORG.NAM	特定机构名称（通惠医院）
ORG.NOM	泛指名称、统称（文艺公司）
"""
_HOMEPAGE_URL = "https://github.com/OYE93/Chinese-NLP-Corpus/tree/master/NER/Weibo"
_CITATION = None
_TRAIN_URL = "https://raw.githubusercontent.com/OYE93/Chinese-NLP-Corpus/master/NER/Weibo/weiboNER_2nd_conll.train"
_TEST_URL = "https://raw.githubusercontent.com/OYE93/Chinese-NLP-Corpus/master/NER/Weibo/weiboNER_2nd_conll.test"
_VALID_URL = "https://raw.githubusercontent.com/OYE93/Chinese-NLP-Corpus/master/NER/Weibo/weiboNER_2nd_conll.dev"


class WeiboNERCorpus(datasets.GeneratorBasedBuilder):
    VERSION = datasets.Version("1.0.0")

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
                                "B-GPE.NAM",
                                "B-GPE.NOM",
                                "B-LOC.NAM",
                                "B-LOC.NOM",
                                "B-ORG.NAM",
                                "B-ORG.NOM",
                                "B-PER.NAM",
                                "B-PER.NOM",
                                "I-GPE.NAM",
                                "I-GPE.NOM",
                                "I-LOC.NAM",
                                "I-LOC.NOM",
                                "I-ORG.NAM",
                                "I-ORG.NOM",
                                "I-PER.NAM",
                                "I-PER.NOM",
                                "O",
                            ]
                        )
                    ),
                },
            ),
            supervised_keys=None,
            homepage=_HOMEPAGE_URL,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        train_path = dl_manager.download_and_extract(_TRAIN_URL)
        valid_path = dl_manager.download_and_extract(_VALID_URL)
        test_path = dl_manager.download_and_extract(_TEST_URL)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={"data_path": train_path},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                gen_kwargs={"data_path": valid_path},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                gen_kwargs={"data_path": test_path},
            ),
        ]

    def _generate_examples(self, data_path):
        sentence_counter = 0
        with open(data_path, encoding="utf-8") as f:
            current_words = []
            current_labels = []
            for row in f:
                row = row.rstrip()
                row_split = row.split("\t")
                if len(row_split) == 2:
                    token, label = row_split
                    current_words.append(token)
                    current_labels.append(label)
                else:
                    if not current_words:
                        continue
                    assert len(current_words) == len(current_labels), "word len doesnt match label length"
                    sentence = (
                        sentence_counter,
                        {
                            "id": str(sentence_counter),
                            "tokens": current_words,
                            "ner_tags": current_labels,
                        },
                    )
                    sentence_counter += 1
                    current_words = []
                    current_labels = []
                    yield sentence

            # if something remains:
            if current_words:
                sentence = (
                    sentence_counter,
                    {
                        "id": str(sentence_counter),
                        "tokens": current_words,
                        "ner_tags": current_labels,
                    },
                )
                yield sentence
