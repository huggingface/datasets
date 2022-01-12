# coding=utf-8
# Copyright 2020 The TensorFlow Datasets Authors and the HuggingFace Datasets Authors.
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
"""KILT tasks training and evaluation data"""


import json

import datasets


logger = datasets.logging.get_logger(__name__)


_CITATION = """\
@inproceedings{fb_kilt,
    author    = {Fabio Petroni and
                 Aleksandra Piktus and
                 Angela Fan and
                 Patrick Lewis and
                 Majid Yazdani and
                 Nicola De Cao and
                 James Thorne and
                 Yacine Jernite and
                 Vassilis Plachouras and
                 Tim Rockt\"aschel and
                 Sebastian Riedel},
    title     = {{KILT:} a {B}enchmark for {K}nowledge {I}ntensive {L}anguage {T}asks},
    journal   = {CoRR},
    archivePrefix = {arXiv},
    year      = {2020},
"""

_DESCRIPTION = """\
KILT tasks training and evaluation data.
- [FEVER](https://fever.ai) | Fact Checking | fever
- [AIDA CoNLL-YAGO](https://www.mpi-inf.mpg.de/departments/databases-and-information-systems/research/ambiverse-nlu/aida/downloads) | Entity Linking | aidayago2
- [WNED-WIKI](https://github.com/U-Alberta/wned) | Entity Linking | wned
- [WNED-CWEB](https://github.com/U-Alberta/wned) | Entity Linking | cweb
- [T-REx](https://hadyelsahar.github.io/t-rex) | Slot Filling | trex
- [Zero-Shot RE](http://nlp.cs.washington.edu/zeroshot) | Slot Filling | structured_zeroshot
- [Natural Questions](https://ai.google.com/research/NaturalQuestions) | Open Domain QA  | nq
- [HotpotQA](https://hotpotqa.github.io) | Open Domain QA | hotpotqa
- [TriviaQA](http://nlp.cs.washington.edu/triviaqa) | Open Domain QA | triviaqa
- [ELI5](https://facebookresearch.github.io/ELI5/explore.html) | Open Domain QA | eli5
- [Wizard of Wikipedia](https://parl.ai/projects/wizard_of_wikipedia) | Dialogue | wow

To finish linking TriviaQA questions to the IDs provided, follow the instructions [here](http://github.com/huggingface/datasets/datasets/kilt_tasks/README.md).
"""


_DATA_URLS = {
    "fever": {
        "train": "http://dl.fbaipublicfiles.com/KILT/fever-train-kilt.jsonl",
        "validation": "http://dl.fbaipublicfiles.com/KILT/fever-dev-kilt.jsonl",
        "test": "http://dl.fbaipublicfiles.com/KILT/fever-test_without_answers-kilt.jsonl",
    },
    "aidayago2": {
        "train": "http://dl.fbaipublicfiles.com/KILT/aidayago2-train-kilt.jsonl",
        "validation": "http://dl.fbaipublicfiles.com/KILT/aidayago2-dev-kilt.jsonl",
        "test": "http://dl.fbaipublicfiles.com/KILT/aidayago2-test_without_answers-kilt.jsonl",
    },
    "wned": {
        "validation": "http://dl.fbaipublicfiles.com/KILT/wned-dev-kilt.jsonl",
        "test": "http://dl.fbaipublicfiles.com/KILT/wned-test_without_answers-kilt.jsonl",
    },
    "cweb": {
        "validation": "http://dl.fbaipublicfiles.com/KILT/cweb-dev-kilt.jsonl",
        "test": "http://dl.fbaipublicfiles.com/KILT/cweb-test_without_answers-kilt.jsonl",
    },
    "trex": {
        "train": "http://dl.fbaipublicfiles.com/KILT/trex-train-kilt.jsonl",
        "validation": "http://dl.fbaipublicfiles.com/KILT/trex-dev-kilt.jsonl",
        "test": "http://dl.fbaipublicfiles.com/KILT/trex-test_without_answers-kilt.jsonl",
    },
    "structured_zeroshot": {
        "train": "http://dl.fbaipublicfiles.com/KILT/structured_zeroshot-train-kilt.jsonl",
        "validation": "http://dl.fbaipublicfiles.com/KILT/structured_zeroshot-dev-kilt.jsonl",
        "test": "http://dl.fbaipublicfiles.com/KILT/structured_zeroshot-test_without_answers-kilt.jsonl",
    },
    "nq": {
        "train": "http://dl.fbaipublicfiles.com/KILT/nq-train-kilt.jsonl",
        "validation": "http://dl.fbaipublicfiles.com/KILT/nq-dev-kilt.jsonl",
        "test": "http://dl.fbaipublicfiles.com/KILT/nq-test_without_answers-kilt.jsonl",
    },
    "hotpotqa": {
        "train": "http://dl.fbaipublicfiles.com/KILT/hotpotqa-train-kilt.jsonl",
        "validation": "http://dl.fbaipublicfiles.com/KILT/hotpotqa-dev-kilt.jsonl",
        "test": "http://dl.fbaipublicfiles.com/KILT/hotpotqa-test_without_answers-kilt.jsonl",
    },
    "triviaqa_support_only": {
        "train": "http://dl.fbaipublicfiles.com/KILT/triviaqa-train_id-kilt.jsonl",
        "validation": "http://dl.fbaipublicfiles.com/KILT/triviaqa-dev_id-kilt.jsonl",
        "test": "http://dl.fbaipublicfiles.com/KILT/triviaqa-test_id_without_answers-kilt.jsonl",
    },
    "eli5": {
        "train": "http://dl.fbaipublicfiles.com/KILT/eli5-train-kilt.jsonl",
        "validation": "http://dl.fbaipublicfiles.com/KILT/eli5-dev-kilt.jsonl",
        "test": "http://dl.fbaipublicfiles.com/KILT/eli5-test_without_answers-kilt.jsonl",
    },
    "wow": {
        "train": "http://dl.fbaipublicfiles.com/KILT/wow-train-kilt.jsonl",
        "validation": "http://dl.fbaipublicfiles.com/KILT/wow-dev-kilt.jsonl",
        "test": "http://dl.fbaipublicfiles.com/KILT/wow-test_without_answers-kilt.jsonl",
    },
}


class KiltTasks(datasets.GeneratorBasedBuilder):

    BUILDER_CONFIGS = [
        datasets.BuilderConfig(
            name="triviaqa_support_only",
            version=datasets.Version("1.0.0"),
            description="Supporting paragraphs information for the TriviaQA task",
        )
    ] + [
        datasets.BuilderConfig(
            name=k, version=datasets.Version("1.0.0"), description=f"Task data and supporting paragraphs for {k}"
        )
        for k in _DATA_URLS
        if k != "triviaqa_support_only"
    ]

    DEFAULT_CONFIG_NAME = "nq"

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "id": datasets.Value("string"),
                    "input": datasets.Value("string"),
                    "meta": {
                        "left_context": datasets.Value("string"),
                        "mention": datasets.Value("string"),
                        "right_context": datasets.Value("string"),
                        "partial_evidence": [
                            {
                                "start_paragraph_id": datasets.Value("int32"),
                                "end_paragraph_id": datasets.Value("int32"),
                                "title": datasets.Value("string"),
                                "section": datasets.Value("string"),
                                "wikipedia_id": datasets.Value("string"),
                                "meta": {"evidence_span": [datasets.Value("string")]},
                            }
                        ],
                        "obj_surface": [datasets.Value("string")],
                        "sub_surface": [datasets.Value("string")],
                        "subj_aliases": [datasets.Value("string")],
                        "template_questions": [datasets.Value("string")],
                    },
                    "output": [
                        {
                            "answer": datasets.Value("string"),
                            "meta": {"score": datasets.Value("int32")},
                            "provenance": [
                                {
                                    "bleu_score": datasets.Value("float32"),
                                    "start_character": datasets.Value("int32"),
                                    "start_paragraph_id": datasets.Value("int32"),
                                    "end_character": datasets.Value("int32"),
                                    "end_paragraph_id": datasets.Value("int32"),
                                    "meta": {
                                        "fever_page_id": datasets.Value("string"),
                                        "fever_sentence_id": datasets.Value("int32"),
                                        "annotation_id": datasets.Value("string"),  # int runs into overflow issues
                                        "yes_no_answer": datasets.Value("string"),
                                        "evidence_span": [datasets.Value("string")],
                                    },
                                    "section": datasets.Value("string"),
                                    "title": datasets.Value("string"),
                                    "wikipedia_id": datasets.Value("string"),
                                }
                            ],
                        }
                    ],
                }
            ),
            supervised_keys=None,
            homepage="https://github.com/facebookresearch/KILT",
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        file_paths = dl_manager.download_and_extract(_DATA_URLS[self.config.name])
        return [
            datasets.SplitGenerator(name=split, gen_kwargs={"filepath": downloaded_path})
            for split, downloaded_path in file_paths.items()
        ]

    def _generate_examples(self, filepath):
        logger.info("generating examples from = %s", filepath)
        with open(filepath, encoding="utf-8") as f:
            for idx, line in enumerate(f):
                article = json.loads(line.strip())
                article["input"] = article.get("input", "")
                # meta
                article["meta"] = article.get("meta", {})
                for k in ["left_context", "mention", "right_context"]:
                    article["meta"][k] = article["meta"].get(k, "")
                for k in ["obj_surface", "sub_surface", "subj_aliases", "template_questions"]:
                    article["meta"][k] = article["meta"].get(k, [])
                # partial evidence
                article["meta"]["partial_evidence"] = [
                    {
                        "start_paragraph_id": partial.get("start_paragraph_id", -1),
                        "end_paragraph_id": partial.get("end_paragraph_id", -1),
                        "title": partial.get("title", ""),
                        "section": partial.get("section", ""),
                        "wikipedia_id": partial.get("wikipedia_id", ""),
                        "meta": {"evidence_span": partial.get("meta", {}).get("evidence_span", [])},
                    }
                    for partial in article["meta"].get("partial_evidence", [])
                ]
                # output
                article["output"] = [
                    {
                        "answer": output.get("answer", ""),
                        "meta": output.get("meta", {"score": -1}),
                        "provenance": [
                            {
                                "bleu_score": provenance.get("bleu_score", -1.0),
                                "start_character": provenance.get("start_character", -1),
                                "start_paragraph_id": provenance.get("start_paragraph_id", -1),
                                "end_character": provenance.get("end_character", -1),
                                "end_paragraph_id": provenance.get("end_paragraph_id", -1),
                                "meta": {
                                    "fever_page_id": provenance.get("meta", {}).get("fever_page_id", ""),
                                    "fever_sentence_id": provenance.get("meta", {}).get("fever_sentence_id", -1),
                                    "annotation_id": str(
                                        provenance.get("meta", {}).get("annotation_id", -1)
                                    ),  # int runs into overflow issues
                                    "yes_no_answer": provenance.get("meta", {}).get("yes_no_answer", ""),
                                    "evidence_span": provenance.get("meta", {}).get("evidence_span", []),
                                },
                                "section": provenance.get("section", ""),
                                "title": provenance.get("title", ""),
                                "wikipedia_id": provenance.get("wikipedia_id", ""),
                            }
                            for provenance in output.get("provenance", [])
                        ],
                    }
                    for output in article.get("output", [])
                ]
                yield idx, article
