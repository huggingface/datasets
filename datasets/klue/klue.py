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

"""KLUE (Korean Language Understanding Evaluation) benchmark."""


import csv
import json
import textwrap

import datasets


_KLUE_CITATION = """\
@misc{park2021klue,
      title={KLUE: Korean Language Understanding Evaluation},
      author={Sungjoon Park and Jihyung Moon and Sungdong Kim and Won Ik Cho and Jiyoon Han and Jangwon Park and Chisung Song and Junseong Kim and Yongsook Song and Taehwan Oh and Joohong Lee and Juhyun Oh and Sungwon Lyu and Younghoon Jeong and Inkwon Lee and Sangwoo Seo and Dongjun Lee and Hyunwoo Kim and Myeonghwa Lee and Seongbo Jang and Seungwon Do and Sunkyoung Kim and Kyungtae Lim and Jongwon Lee and Kyumin Park and Jamin Shin and Seonghyun Kim and Lucy Park and Alice Oh and Jungwoo Ha and Kyunghyun Cho},
      year={2021},
      eprint={2105.09680},
      archivePrefix={arXiv},
      primaryClass={cs.CL}
}
"""

_KLUE_DESCRIPTION = """\
KLUE (Korean Language Understanding Evaluation)
Korean Language Understanding Evaluation (KLUE) benchmark is a series of datasets to evaluate natural language
understanding capability of Korean language models. KLUE consists of 8 diverse and representative tasks, which are accessible
to anyone without any restrictions. With ethical considerations in mind, we deliberately design annotation guidelines to obtain
unambiguous annotations for all datasets. Futhermore, we build an evaluation system and carefully choose evaluations metrics
for every task, thus establishing fair comparison across Korean language models.
"""

_DATA_URLs = {
    "ynat": "http://klue-benchmark.com.s3.amazonaws.com/app/Competitions/000066/data/ynat-v1.tar.gz",
    "sts": "http://klue-benchmark.com.s3.amazonaws.com/app/Competitions/000067/data/klue-sts-v1.tar.gz",
    "nli": "http://klue-benchmark.com.s3.amazonaws.com/app/Competitions/000068/data/klue-nli-v1.tar.gz",
    "ner": "http://klue-benchmark.com.s3.amazonaws.com/app/Competitions/000069/data/klue-ner-v1.tar.gz",
    "re": "http://klue-benchmark.com.s3.amazonaws.com/app/Competitions/000070/data/klue-re-v1.tar.gz",
    "dp": "http://klue-benchmark.com.s3.amazonaws.com/app/Competitions/000071/data/klue-dp-v1.tar.gz",
    "mrc": "http://klue-benchmark.com.s3.amazonaws.com/app/Competitions/000072/data/klue-mrc-v1.tar.gz",
    "wos": "http://klue-benchmark.com.s3.amazonaws.com/app/Competitions/000073/data/wos-v1.tar.gz",
}

_DESCRIPTION_URLs = {
    "ynat": "https://klue-benchmark.com/tasks/66/overview/description",
    "sts": "https://klue-benchmark.com/tasks/67/overview/description",
    "nli": "https://klue-benchmark.com/tasks/68/overview/description",
    "ner": "https://klue-benchmark.com/tasks/69/overview/description",
    "re": "https://klue-benchmark.com/tasks/70/overview/description",
    "dp": "https://klue-benchmark.com/tasks/71/overview/description",
    "mrc": "https://klue-benchmark.com/tasks/72/overview/description",
    "wos": "https://klue-benchmark.com/tasks/73/overview/description",
}

_LICENSE = "CC-BY-SA-4.0"


class KlueConfig(datasets.BuilderConfig):
    """BuilderConfig for KLUE."""

    def __init__(
        self,
        features,
        data_url,
        url,
        file_map,
        **kwargs,
    ):
        """BuilderConfig for KLUE."""

        super(KlueConfig, self).__init__(version=datasets.Version("1.0.0", ""), **kwargs)
        self.features = features
        self.data_url = data_url
        self.url = url
        self.file_map = file_map


class Klue(datasets.GeneratorBasedBuilder):
    """The General Language Understanding Evaluation (GLUE) benchmark."""

    BUILDER_CONFIGS = [
        KlueConfig(
            name="ynat",
            features={
                "guid": datasets.Value("string"),
                "title": datasets.Value("string"),
                "label": datasets.features.ClassLabel(names=["IT과학", "경제", "사회", "생활문화", "세계", "스포츠", "정치"]),
                "url": datasets.Value("string"),
                "date": datasets.Value("string"),
            },
            description=textwrap.dedent(
                """\
            In topic classification (TC), the goal is to predict the topic of a given text
            snippet. We include TC in our KLUE benchmark, as inferring the topic of a text is a key
            capability that should be possessed by a language understanding system.
            Following a typical single  sentence classification task, we introduce YNAT, a Younhap
            News Agency news headlines for Topic Classification. For Korean, no dataset has been
            proposed for this task, which motivates us to construct the first Korean topic
            classification benchmark. In this task, given a news headline, a text classifier must
            predict a topic which is one of politics, economy, society, culture, world, IT/science,
            and sports. Macro-F1 score is used to evaluate a system."""
            ),
            data_url=_DATA_URLs["ynat"],
            url=_DESCRIPTION_URLs["ynat"],
            file_map={
                "train": "ynat-v1_train.json",
                "dev": "ynat-v1_dev.json",
            },
        ),
        KlueConfig(
            name="sts",
            features={
                "guid": datasets.Value("string"),
                "source": datasets.Value("string"),
                "sentence1": datasets.Value("string"),
                "sentence2": datasets.Value("string"),
                "labels": {
                    "label": datasets.Value("float64"),
                    "real-label": datasets.Value("float64"),
                    "binary-label": datasets.ClassLabel(names=["negative", "positive"]),
                },
            },
            description=textwrap.dedent(
                """\
            STS is a task which aims to predict the semantic similarity of two input sentences as
            a real value between 0 and 5. Note that we furthure binarized the prediction scores
            into two classes with a threshold score 3.0 (paraphrased or not) and evaluated with
            a classification metric.
            """
            ),
            data_url=_DATA_URLs["sts"],
            url=_DESCRIPTION_URLs["sts"],
            file_map={
                "train": "klue-sts-v1_train.json",
                "dev": "klue-sts-v1_dev.json",
            },
        ),
        KlueConfig(
            name="nli",
            features={
                "guid": datasets.Value("string"),
                "source": datasets.Value("string"),
                "premise": datasets.Value("string"),
                "hypothesis": datasets.Value("string"),
                "label": datasets.ClassLabel(names=["entailment", "neutral", "contradiction"]),
            },
            description=textwrap.dedent(
                """\
            NLI is a task to infer the relationship between a hypothesis sentence and a premise
            sentence. Given the premise, the model determines if the hypothesis is true (entailment),
            false (contradiction), or undetermined (neutral).
            """
            ),
            data_url=_DATA_URLs["nli"],
            url=_DESCRIPTION_URLs["nli"],
            file_map={
                "train": "klue-nli-v1_train.json",
                "dev": "klue-nli-v1_dev.json",
            },
        ),
        KlueConfig(
            name="ner",
            features={
                "sentence": datasets.Value("string"),
                "tokens": datasets.Sequence(datasets.Value("string")),
                "ner_tags": datasets.Sequence(
                    datasets.ClassLabel(
                        names=[
                            "B-DT",
                            "I-DT",
                            "B-LC",
                            "I-LC",
                            "B-OG",
                            "I-OG",
                            "B-PS",
                            "I-PS",
                            "B-QT",
                            "I-QT",
                            "B-TI",
                            "I-TI",
                            "O",
                        ]
                    )
                ),
            },
            description=textwrap.dedent(
                """\
            NER is a task to detect the boundaries of named entities in unstructured text and to
            classify the types. A named entity can be of one of predefined entity types such as
            person, location, organization, time expressions, quantities and monetary values.
            """
            ),
            data_url=_DATA_URLs["ner"],
            url=_DESCRIPTION_URLs["ner"],
            file_map={
                "train": "klue-ner-v1_train.tsv",
                "dev": "klue-ner-v1_dev.tsv",
            },
        ),
        KlueConfig(
            name="re",
            features={
                "guid": datasets.Value("string"),
                "sentence": datasets.Value("string"),
                "subject_entity": {
                    "word": datasets.Value("string"),
                    "start_idx": datasets.Value("int32"),
                    "end_idx": datasets.Value("int32"),
                    "type": datasets.Value("string"),
                },
                "object_entity": {
                    "word": datasets.Value("string"),
                    "start_idx": datasets.Value("int32"),
                    "end_idx": datasets.Value("int32"),
                    "type": datasets.Value("string"),
                },
                "label": datasets.ClassLabel(
                    names=[
                        "no_relation",
                        "org:dissolved",
                        "org:founded",
                        "org:place_of_headquarters",
                        "org:alternate_names",
                        "org:member_of",
                        "org:members",
                        "org:political/religious_affiliation",
                        "org:product",
                        "org:founded_by",
                        "org:top_members/employees",
                        "org:number_of_employees/members",
                        "per:date_of_birth",
                        "per:date_of_death",
                        "per:place_of_birth",
                        "per:place_of_death",
                        "per:place_of_residence",
                        "per:origin",
                        "per:employee_of",
                        "per:schools_attended",
                        "per:alternate_names",
                        "per:parents",
                        "per:children",
                        "per:siblings",
                        "per:spouse",
                        "per:other_family",
                        "per:colleagues",
                        "per:product",
                        "per:religion",
                        "per:title",
                    ]
                ),
                "source": datasets.Value("string"),
            },
            description=textwrap.dedent(
                """\
            RE is a task to identify semantic relations between entity pairs in a text. The relation
            is defined between an entity pair consisting of subject entity and object entity.
            The goal is then to pick an appropriate relationship between these two entities.
            """
            ),
            data_url=_DATA_URLs["re"],
            url=_DESCRIPTION_URLs["re"],
            file_map={
                "train": "klue-re-v1_train.json",
                "dev": "klue-re-v1_dev.json",
            },
        ),
        KlueConfig(
            name="dp",
            features={
                "sentence": datasets.Value("string"),
                "index": [datasets.Value("int32")],
                "word_form": [datasets.Value("string")],
                "lemma": [datasets.Value("string")],
                "pos": [datasets.Value("string")],
                "head": [datasets.Value("int32")],
                "deprel": [datasets.Value("string")],
            },
            description=textwrap.dedent(
                """\
            DP is a task that aims at finding relational information among words.
            The goal is to predict a graph structure and a dependency label of an input sentence
            based on the dependency grammar.
            """
            ),
            data_url=_DATA_URLs["dp"],
            url=_DESCRIPTION_URLs["dp"],
            file_map={
                "train": "klue-dp-v1_train.tsv",
                "dev": "klue-dp-v1_dev.tsv",
            },
        ),
        KlueConfig(
            name="mrc",
            features={
                "title": datasets.Value("string"),
                "context": datasets.Value("string"),
                "news_category": datasets.Value("string"),
                "source": datasets.Value("string"),
                "guid": datasets.Value("string"),
                "is_impossible": datasets.Value("bool"),
                "question_type": datasets.Value("int32"),
                "question": datasets.Value("string"),
                "answers": datasets.features.Sequence(
                    {
                        "answer_start": datasets.Value("int32"),
                        "text": datasets.Value("string"),
                    },
                ),
            },
            description=textwrap.dedent(
                """\
            MRC is a task of evaluating model that can answer a question about a given text
            passage. Specifically, we formulate the task as a span prediction task, where the
            answer is a text segment (coined as spans) in the passage.
            """
            ),
            data_url=_DATA_URLs["mrc"],
            url=_DESCRIPTION_URLs["mrc"],
            file_map={
                "train": "klue-mrc-v1_train.json",
                "dev": "klue-mrc-v1_dev.json",
            },
        ),
        KlueConfig(
            name="wos",
            features={
                "guid": datasets.Value("string"),
                "domains": [datasets.Value("string")],
                "dialogue": [
                    {
                        "role": datasets.Value("string"),
                        "text": datasets.Value("string"),
                        "state": [datasets.Value("string")],
                    }
                ],
            },
            description=textwrap.dedent(
                """\
            DST is a task to predict slot and value pairs (dialogue states) from a task-oriented
            dialogue. The potential pairs are predefined by a given task schema and knowledge
            base (KB).
            """
            ),
            data_url=_DATA_URLs["wos"],
            url=_DESCRIPTION_URLs["wos"],
            file_map={
                "train": "wos-v1_train.json",
                "dev": "wos-v1_dev.json",
            },
        ),
    ]

    def _info(self):
        return datasets.DatasetInfo(
            description=_KLUE_DESCRIPTION,
            features=datasets.Features(self.config.features),
            homepage=self.config.url,
            citation=_KLUE_CITATION,
            license=_LICENSE,
        )

    def _split_generators(self, dl_manager):
        archive = dl_manager.download(self.config.data_url)
        dir_name = self.config.data_url.split("/")[-1].replace(".tar.gz", "")
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={
                    "data_file": dir_name + "/" + self.config.file_map["train"],
                    "files": dl_manager.iter_archive(archive),
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                gen_kwargs={
                    "data_file": dir_name + "/" + self.config.file_map["dev"],
                    "files": dl_manager.iter_archive(archive),
                },
            ),
        ]

    def _generate_examples(self, data_file, files):
        if self.config.name in ["ynat", "sts", "re"]:
            for path, f in files:
                if path == data_file:
                    f = json.load(f)
                    for id_, row in enumerate(f):
                        features = {key: row[key] for key in row if key in self.config.features}
                        yield id_, features
                    break

        if self.config.name == "nli":
            for path, f in files:
                if path == data_file:
                    f = json.load(f)
                    for id_, row in enumerate(f):
                        # In train file, "source" is written as "genre"
                        features = {
                            "guid": row["guid"],
                            "source": row["source"] if "source" in row else row["genre"],
                            "premise": row["premise"],
                            "hypothesis": row["hypothesis"],
                            "label": row["gold_label"],
                        }
                        yield id_, features
                    break

        if self.config.name == "ner":
            for path, f in files:
                if path == data_file:
                    f = (line.decode("utf-8") for line in f)
                    reader = csv.reader(f, delimiter="\t", quoting=csv.QUOTE_NONE)
                    for _ in range(5):  # skip headers
                        next(reader)
                    id_ = -1
                    for row in reader:
                        if row:
                            if row[0].startswith("##"):
                                id_ += 1
                                tokens, ner_tags = [], []
                                sentence = row[1]
                            else:
                                tokens.append(row[0])
                                ner_tags.append(row[1])
                        else:  # new line
                            assert len(tokens) == len(ner_tags)
                            yield id_, {"sentence": sentence, "tokens": tokens, "ner_tags": ner_tags}
                    break

        if self.config.name == "dp":
            for path, f in files:
                if path == data_file:
                    f = (line.decode("utf-8") for line in f)
                    reader = csv.reader(f, delimiter="\t", quoting=csv.QUOTE_NONE)
                    for _ in range(5):  # skip headers
                        next(reader)
                    id_ = -1
                    for row in reader:
                        if row:
                            if row[0].startswith("##"):
                                id_ += 1
                                index = []
                                word_form = []
                                lemma = []
                                pos = []
                                head = []
                                deprel = []
                                sentence = row[1]
                            else:
                                index.append(row[0])
                                word_form.append(row[1])
                                lemma.append(row[2])
                                pos.append(row[3])
                                head.append(row[4])
                                deprel.append(row[5])
                        else:  # new line
                            assert len(index) == len(word_form) == len(lemma) == len(pos) == len(head) == len(deprel)
                            yield id_, {
                                "sentence": sentence,
                                "index": index,
                                "word_form": word_form,
                                "lemma": lemma,
                                "pos": pos,
                                "head": head,
                                "deprel": deprel,
                            }
                    break

        if self.config.name == "mrc":
            for path, f in files:
                if path == data_file:
                    f = json.load(f)
                    id_ = -1
                    for example in f["data"]:
                        title = example.get("title", "")
                        news_category = example.get("news_category", "")
                        source = example["source"]
                        for paragraph in example["paragraphs"]:
                            context = paragraph["context"].strip()
                            for qa in paragraph["qas"]:
                                guid = qa["guid"]
                                question_type = qa["question_type"]
                                is_impossible = qa["is_impossible"]
                                question = qa["question"].strip()

                                if "plausible_answers" in qa:
                                    qa["answers"].extend(qa["plausible_answers"])
                                answer_starts = [answer["answer_start"] for answer in qa["answers"]]
                                answers = [answer["text"].strip() for answer in qa["answers"]]
                                id_ += 1

                                yield id_, {
                                    "guid": guid,
                                    "title": title,
                                    "context": context,
                                    "news_category": news_category,
                                    "source": source,
                                    "question_type": question_type,
                                    "is_impossible": is_impossible,
                                    "question": question,
                                    "answers": {
                                        "answer_start": answer_starts,
                                        "text": answers,
                                    },
                                }
                    break

        if self.config.name == "wos":
            for path, f in files:
                if path == data_file:
                    f = json.load(f)
                    for id_, row in enumerate(f):
                        guid = row["guid"]
                        domains = row["domains"]
                        dialogue = row["dialogue"]
                        for utterance in dialogue:
                            if "state" not in utterance:
                                utterance["state"] = []
                        yield id_, {"guid": guid, "domains": domains, "dialogue": dialogue}
                    break
