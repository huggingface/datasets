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
Webbnyheter 2012 from Spraakbanken, semi-manually annotated and adapted for CoreNLP Swedish NER. Semi-manually defined in this case as: Bootstrapped from Swedish Gazetters then manually correcte/reviewed by two independent native speaking swedish annotators. No annotator agreement calculated.
"""
_HOMEPAGE_URL = "https://github.com/klintan/swedish-ner-corpus"
_TRAIN_URL = "https://raw.githubusercontent.com/klintan/swedish-ner-corpus/master/train_corpus.txt"
_TEST_URL = "https://raw.githubusercontent.com/klintan/swedish-ner-corpus/master/test_corpus.txt"
_CITATION = None


class SwedishNERCorpus(datasets.GeneratorBasedBuilder):
    VERSION = datasets.Version("1.0.0")

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "id": datasets.Value("string"),
                    "tokens": datasets.Sequence(datasets.Value("string")),
                    "ner_tags": datasets.Sequence(
                        datasets.features.ClassLabel(names=["0", "LOC", "MISC", "ORG", "PER"])
                    ),
                },
            ),
            supervised_keys=None,
            homepage=_HOMEPAGE_URL,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        train_path = dl_manager.download_and_extract(_TRAIN_URL)
        test_path = dl_manager.download_and_extract(_TEST_URL)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={"datapath": train_path},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                gen_kwargs={"datapath": test_path},
            ),
        ]

    def _generate_examples(self, datapath):
        sentence_counter = 0
        with open(datapath, encoding="utf-8") as f:
            current_words = []
            current_labels = []
            for row in f:
                row = row.rstrip()
                row_split = row.split()
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
