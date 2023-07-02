# Copyright 2020 The HuggingFace Datasets Authors.
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
""" KLUE-MRC metric. """

import datasets

from .evaluate import (
    apply_no_ans_threshold,
    find_all_best_thresh,
    get_raw_scores,
    make_eval_dict,
    make_qid_to_has_ans,
    merge_eval,
)


_CITATION = """
@inproceedings{NEURIPS DATASETS AND BENCHMARKS2021_98dce83d,
 author = {Park, Sungjoon and Moon, Jihyung and Kim, Sungdong and Cho, Won Ik and Han, Ji Yoon and Park, Jangwon and Song, Chisung and Kim, Junseong and Song, Youngsook and Oh, Taehwan and Lee, Joohong and Oh, Juhyun and Lyu, Sungwon and Jeong, Younghoon and Lee, Inkwon and Seo, Sangwoo and Lee, Dongjun and Kim, Hyunwoo and Lee, Myeonghwa and Jang, Seongbo and Do, Seungwon and Kim, Sunkyoung and Lim, Kyungtae and Lee, Jongwon and Park, Kyumin and Shin, Jamin and Kim, Seonghyun and Park, Lucy and Park, Lucy and Oh, Alice and Ha (NAVER AI Lab), Jung-Woo and Cho, Kyunghyun and Cho, Kyunghyun},
 booktitle = {Proceedings of the Neural Information Processing Systems Track on Datasets and Benchmarks},
 editor = {J. Vanschoren and S. Yeung},
 pages = {},
 publisher = {Curran},
 title = {KLUE: Korean Language Understanding Evaluation},
 url = {https://datasets-benchmarks-proceedings.neurips.cc/paper_files/paper/2021/file/98dce83da57b0395e163467c9dae521b-Paper-round2.pdf},
 volume = {1},
 year = {2021}
}
"""

_DESCRIPTION = """
This metric wrap the unofficial scoring script for Machine Reading Comprehension task of
Korean Language Understanding Evaluation (KLUE-MRC).

KLUE-MRC is a korean reading comprehension dataset, which has the same task format with SQuAD 2.0—consisting of questions where
the answer to every question is a segment of text, or span, from the corresponding reading passage, or the question might be unanswerable.

As KLUE-MRC has the same task format with SQuAD 2.0, this evaluation script use the same metrics of SQuAD 2.0—F1 and EM.

KLUE-MRC consists of 12,286 question paraphrasing, 7,931 multi-sentence reasoning and 9,269 unanswerable questions.
Totally, 29,313 examples are made with 22,343 documents, 23,717 passaages.
"""

_KWARGS_DESCRIPTION = """
Computes KLUE-MRC scores (F1 and EM).
Args:
    predictions: List of triple for question-answers to score with the following elements:
        - the question-answer 'id' field as given in the references (see below)
        - the text of the answer
        - the probability that the question has no answer
    references: List of question-answers dictionaries with the following key-values:
            - 'id': id of the question-answer pair (see above),
            - 'answers': a list of Dict {'text': text of the answer as a string}
    no_answer_threshold: float
        Probability threshold to decide that a question has no answer.
Returns:
    'exact': Exact match (the normalized answer exactly match the gold answer)
    'f1': The F-score of predicted tokens versus the gold answer
    'total': Number of score considered
    'HasAns_exact': Exact match (the normalized answer exactly match the gold answer)
    'HasAns_f1': The F-score of predicted tokens versus the gold answer
    'HasAns_total': Number of score considered
    'NoAns_exact': Exact match (the normalized answer exactly match the gold answer)
    'NoAns_f1': The F-score of predicted tokens versus the gold answer
    'NoAns_total': Number of score considered
    'best_exact': Best exact match (with varying threshold)
    'best_exact_thresh': No-answer probability threshold associated to the best exact match
    'best_f1': Best F1 (with varying threshold)
    'best_f1_thresh': No-answer probability threshold associated to the best F1
Examples:

    >>> predictions = [{'prediction_text': '2020', 'id': 'klue-mrc-v1_train_12311', 'no_answer_probability': 0.}]
    >>> references = [{'id': 'klue-mrc-v1_train_12311', 'answers': { "answer_start": [ 38 ], "text": [ "2020" ] }, 'unanswerable': false}]
    >>> klue_mrc_metric = datasets.load_metric("klue_mrc")
    >>> results = klue_mrc_metric.compute(predictions=predictions, references=references)
    >>> print(results)
    {'exact': 100.0, 'f1': 100.0, 'total': 1, 'HasAns_exact': 100.0, 'HasAns_f1': 100.0, 'HasAns_total': 1, 'best_exact': 100.0, 'best_exact_thresh': 0.0, 'best_f1': 100.0, 'best_f1_thresh': 0.0}
"""


@datasets.utils.file_utils.add_start_docstrings(_DESCRIPTION, _KWARGS_DESCRIPTION)
class KLUEMRC(datasets.Metric):
    def _info(self):
        return datasets.MetricInfo(
            description=_DESCRIPTION,
            citation=_CITATION,
            inputs_description=_KWARGS_DESCRIPTION,
            features=datasets.Features(
                {
                    "predictions": {
                        "id": datasets.Value("string"),
                        "prediction_text": datasets.Value("string"),
                        "no_answer_probability": datasets.Value("float32"),
                    },
                    "references": {
                        "id": datasets.Value("string"),
                        "answers": datasets.features.Sequence(
                            {"text": datasets.Value("string"), "answer_start": datasets.Value("int32")}
                        ),
                        "unanswerable": datasets.Value("bool"),
                    },
                }
            ),
            codebase_urls=["https://rajpurkar.github.io/SQuAD-explorer/"],
            reference_urls=["https://klue-benchmark.com/tasks/72/overview/description"],
        )

    def _compute(self, predictions, references, no_answer_threshold=1.0):
        no_answer_probabilities = {p["id"]: p["no_answer_probability"] for p in predictions}
        dataset = [{"paragraphs": [{"qas": references}]}]
        predictions = {p["id"]: p["prediction_text"] for p in predictions}

        qid_to_has_ans = make_qid_to_has_ans(dataset)  # maps qid to True/False
        has_ans_qids = [k for k, v in qid_to_has_ans.items() if v]
        no_ans_qids = [k for k, v in qid_to_has_ans.items() if not v]

        exact_raw, f1_raw = get_raw_scores(dataset, predictions)
        exact_thresh = apply_no_ans_threshold(exact_raw, no_answer_probabilities, qid_to_has_ans, no_answer_threshold)
        f1_thresh = apply_no_ans_threshold(f1_raw, no_answer_probabilities, qid_to_has_ans, no_answer_threshold)
        out_eval = make_eval_dict(exact_thresh, f1_thresh)

        if has_ans_qids:
            has_ans_eval = make_eval_dict(exact_thresh, f1_thresh, qid_list=has_ans_qids)
            merge_eval(out_eval, has_ans_eval, "HasAns")
        if no_ans_qids:
            no_ans_eval = make_eval_dict(exact_thresh, f1_thresh, qid_list=no_ans_qids)
            merge_eval(out_eval, no_ans_eval, "NoAns")
        find_all_best_thresh(out_eval, predictions, exact_raw, f1_raw, no_answer_probabilities, qid_to_has_ans)
        return dict(out_eval)
