# coding=utf-8
# Copyright 2020 The TensorFlow Datasets Authors and the HuggingFace NLP Authors.
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

from __future__ import absolute_import, division, print_function

import json
import logging

import nlp


_CITATION = """\
@inproceedings{fb_kilt,
    author    = {Fabio Petroni and Angela Fan and Sebastian Riedel},
    title     = {{KILT:} Knowledge Intensive Language Tasks},
    booktitle = {ArXiv},
    year      = {2020},
"""

_DESCRIPTION = """\
KILT tasks training and evaluation data.
- [FEVER](https://fever.ai) | Fact Checking | fever
- [Natural Questions](https://ai.google.com/research/NaturalQuestions) | Open Domain QA  | nq
- [HotpotQA](https://hotpotqa.github.io) | Open Domain QA | hotpotqa
- [TriviaQA](http://nlp.cs.washington.edu/triviaqa) | Open Domain QA | triviaqa
- [ELI5](https://facebookresearch.github.io/ELI5/explore.html) | Open Domain QA | eli5
- [T-REx](https://hadyelsahar.github.io/t-rex) | Slot Filling | trex
- [Zero-Shot RE](http://nlp.cs.washington.edu/zeroshot) | Slot Filling | structured_zeroshot
- [AIDA CoNLL-YAGO](https://www.mpi-inf.mpg.de/departments/databases-and-information-systems/research/ambiverse-nlu/aida/downloads) | Entity Linking | aidayago2
- [WNED-WIKI](https://github.com/U-Alberta/wned) | Entity Linking | wned
- [WNED-CWEB](https://github.com/U-Alberta/wned) | Entity Linking | cweb
- [Wizard of Wikipedia](https://parl.ai/projects/wizard_of_wikipedia) | Dialogue | wow
"""
 

_DATA_URLS = {
    "fever": {
        "train": "http://dl.fbaipublicfiles.com/KILT/fever-train-kilt.jsonl",
        "validation": "http://dl.fbaipublicfiles.com/KILT/fever-dev-kilt.jsonl",
        "test": "http://dl.fbaipublicfiles.com/KILT/fever-test_without_answers-kilt.jsonl",
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
    "triviaqa": {
        "train": "http://dl.fbaipublicfiles.com/KILT/triviaqa-train_id-kilt.jsonl",
        "validation": "http://dl.fbaipublicfiles.com/KILT/triviaqa-dev_id-kilt.jsonl",
        "test": "http://dl.fbaipublicfiles.com/KILT/triviaqa-test_id_without_answers-kilt.jsonl",
    },
    "eli5": {
        "train": "http://dl.fbaipublicfiles.com/KILT/eli5-train-kilt.jsonl",
        "validation": "http://dl.fbaipublicfiles.com/KILT/eli5-dev-kilt.jsonl",
        "test": "http://dl.fbaipublicfiles.com/KILT/eli5-test_without_answers-kilt.jsonl",
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
    "wow": {
        "train": "http://dl.fbaipublicfiles.com/KILT/wow-train-kilt.jsonl",
        "validation": "http://dl.fbaipublicfiles.com/KILT/wow-dev-kilt.jsonl",
        "test": "http://dl.fbaipublicfiles.com/KILT/wow-test_without_answers-kilt.jsonl",
    },
}

class KILTTasksConfig(nlp.BuilderConfig):
    """BuilderConfig for KILTTasks."""

    def __init__(self, **kwargs):
        """BuilderConfig for KILTTasks.

    Args:
.
      **kwargs: keyword arguments forwarded to super.
    """
        super(KILTTasksConfig, self).__init__(
            version=nlp.Version("1.0.0", "KILT tasks training and evaluation data"), **kwargs
        )


class KILTTasks(nlp.GeneratorBasedBuilder):
    """WikipediaKILT: Wikipedia pre-processed for KILT. Version 1.0."""

    BUILDER_CONFIGS = [
        KILTTasksConfig(name="all_tasks", description="All KILT tasks traiing and evaluation data",),
    ]

    def _info(self):
        return nlp.DatasetInfo(
            description=_DESCRIPTION,
            features=nlp.Features(
                {
                    'id': nlp.Value("string"),
                    'input': nlp.Value("string"),
                    'meta': nlp.Features(
                        {
                            'left_context': nlp.Value("string"),
                            'mention': nlp.Value("string"),
                            'right_context': nlp.Value("string"),
                            'partial_evidence': nlp.features.Sequence(
                                {
                                    'start_paragraph_id': nlp.Value("int32"),
                                    'end_paragraph_id': nlp.Value("int32"),
                                    'title': nlp.Value("string"),
                                    'section': nlp.Value("string"),
                                    'wikipedia_id': nlp.Value("string"),
                                    'meta': nlp.features.Sequence(
                                        {
                                            'evidence_span': nlp.Value("string"),
                                        }
                                    ),
                                }
                            ),
                            'obj_surface': nlp.features.Sequence({'text': nlp.Value("string")}),
                            'sub_surface': nlp.features.Sequence({'text': nlp.Value("string")}),
                            'subj_aliases': nlp.features.Sequence({'text': nlp.Value("string")}),
                            'template_questions': nlp.features.Sequence({'text': nlp.Value("string")}),
                        }
                    ),
                    'output': nlp.features.Sequence(
                        {
                            'answer': nlp.Value("string"),
                            'meta': nlp.Features({'score': nlp.Value("int32")}),
                            'provenance': nlp.features.Sequence(
                                {
                                    'bleu_score': nlp.Value("float32"),
                                    'start_character': nlp.Value("int32"),
                                    'start_paragraph_id': nlp.Value("int32"),
                                    'end_character': nlp.Value("int32"),
                                    'end_paragraph_id': nlp.Value("int32"),
                                    'meta': nlp.Features(
                                        {
                                            'fever_page_id': nlp.Value("string"),
                                            'fever_sentence_id': nlp.Value("int32"),
                                            'annotation_id': nlp.Value("string"), #  int runs into overflow issues
                                            'yes_no_answer':  nlp.Value("string"),
                                            'evidence_span': nlp.features.Sequence({'text': nlp.Value("string")}),
                                        }
                                    ),
                                    'section': nlp.Value("string"),
                                    'title': nlp.Value("string"),
                                    'wikipedia_id': nlp.Value("string"),
                                }
                            ),
                        }
                    ),
                }

            ),
            # No default supervised_keys (as we have to pass both premise
            # and hypothesis as input).
            supervised_keys=None,
            homepage="https://facebookresearch.github.io/KILT/",
            citation=_CITATION,
        )


    def _split_generators(self, dl_manager):
        file_paths = {}
        for task_name, task_urls in _DATA_URLS.items():
            file_paths[task_name] = dl_manager.download_and_extract(task_urls)

        return [
            nlp.SplitGenerator(name=split + '_' + task, gen_kwargs={"filepath": downloaded_path})
            for task, split_paths in file_paths.items() for split, downloaded_path in split_paths.items()
        ]

    def _generate_examples(self, filepath):
        """Generate Wikipedia articles for KILT.

        Args:
          filepath: a string

        Yields:
          dictionaries representing article data and metadata
        """
        logging.info("generating examples from = %s", filepath)
        with open(filepath, encoding="utf-8") as f:
            for idx, line in enumerate(f):
                article = json.loads(line.strip())
                article['input'] = article.get('input', '')
                # meta
                article['meta'] = article.get('meta', {})
                for k in ['left_context', 'mention', 'right_context']:
                    article['meta'][k] = article['meta'].get(k, '')
                for k in ['obj_surface', 'sub_surface', 'subj_aliases', 'template_questions']:
                    article['meta'][k] = {'text': article['meta'].get(k, [])}
                article['meta']['partial_evidence'] = article['meta'].get('partial_evidence', [])
                if 'partial_evidence' in article['meta']:
                    dct_list = {}
                    for k in ['start_paragraph_id', 'end_paragraph_id']:
                        dct_list[k] = [dct.get(k, -1) for dct in article['meta']['partial_evidence']]
                    for k in ['title', 'section', 'wikipedia_id']:
                        dct_list[k] = [dct.get(k, '') for dct in article['meta']['partial_evidence']]
                    if any(['meta' in dct for dct in article['meta']['partial_evidence']]):
                        dct_list['meta'] = [dct.get('meta', {}) for dct in article['meta']['partial_evidence']]
                        for meta in dct_list['meta']:
                            meta['evidence_span'] = meta.get('evidence_span', [])
                    else:
                        dct_list['meta'] = []
                    article['meta']['partial_evidence'] = dct_list
                # output
                article['output'] = article.get('output', [])
                dct_list = {}
                dct_list['answer'] = [dct.get('answer', '') for dct in article['output']]
                if any(['meta' in dct for dct in article['output']]):
                    dct_list['meta'] = [dct.get('meta', {'score': 0}) for dct in article['output']]
                else:
                    dct_list['meta'] = []
                dct_list['provenance'] = []
                for dct in article['output']:
                    if 'provenance' in dct:
                        prov_list = dct['provenance']
                        prov_dct_list = {}
                        prov_dct_list['bleu_score'] = [prov.get('bleu_score', 0.) for prov in prov_list]
                        if any(['meta' in prov for prov in prov_list]):
                            prov_dct_list['meta'] = [prov.get('meta', {}) for prov in prov_list]
                            for meta_dct in prov_dct_list['meta']:
                                meta_dct['fever_page_id'] = meta_dct.get('fever_page_id', '')
                                meta_dct['fever_sentence_id'] = meta_dct.get('fever_sentence_id', -1)
                                meta_dct['yes_no_answer'] = meta_dct.get('yes_no_answer', '')
                                meta_dct['annotation_id'] = str(meta_dct.get('annotation_id', -1))
                                meta_dct['evidence_span'] = {'text': meta_dct.get('evidence_span', [])}
                        else:
                            prov_dct_list['meta'] = []
                        for k in ['start_character', 'start_paragraph_id', 'end_character', 'end_paragraph_id']:
                            prov_dct_list[k] = [prov.get(k, -1) for prov in prov_list]
                        for k in ['section', 'title', 'wikipedia_id']:
                            prov_dct_list[k] = [prov.get(k, '') for prov in prov_list]
                        dct_list['provenance'] += [prov_dct_list]
                article['output'] = dct_list
                yield idx, article



