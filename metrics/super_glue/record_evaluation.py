"""
Official evaluation script for ReCoRD v1.0.
(Some functions are adopted from the SQuAD evaluation script.)
"""

from __future__ import print_function

import argparse
import json
import re
import string
import sys
from collections import Counter


def normalize_answer(s):
    """Lower text and remove punctuation, articles and extra whitespace."""

    def remove_articles(text):
        return re.sub(r"\b(a|an|the)\b", " ", text)

    def white_space_fix(text):
        return " ".join(text.split())

    def remove_punc(text):
        exclude = set(string.punctuation)
        return "".join(ch for ch in text if ch not in exclude)

    def lower(text):
        return text.lower()

    return white_space_fix(remove_articles(remove_punc(lower(s))))


def f1_score(prediction, ground_truth):
    prediction_tokens = normalize_answer(prediction).split()
    ground_truth_tokens = normalize_answer(ground_truth).split()
    common = Counter(prediction_tokens) & Counter(ground_truth_tokens)
    num_same = sum(common.values())
    if num_same == 0:
        return 0
    precision = 1.0 * num_same / len(prediction_tokens)
    recall = 1.0 * num_same / len(ground_truth_tokens)
    f1 = (2 * precision * recall) / (precision + recall)
    return f1


def exact_match_score(prediction, ground_truth):
    return normalize_answer(prediction) == normalize_answer(ground_truth)


def metric_max_over_ground_truths(metric_fn, prediction, ground_truths):
    scores_for_ground_truths = []
    for ground_truth in ground_truths:
        score = metric_fn(prediction, ground_truth)
        scores_for_ground_truths.append(score)
    return max(scores_for_ground_truths)


def evaluate(dataset, predictions):
    f1 = exact_match = total = 0
    correct_ids = []
    for passage in dataset:
        for qa in passage["qas"]:
            total += 1
            if qa["id"] not in predictions:
                message = "Unanswered question {} will receive score 0.".format(qa["id"])
                print(message, file=sys.stderr)
                continue

            ground_truths = list(map(lambda x: x["text"], qa["answers"]))
            prediction = predictions[qa["id"]]

            _exact_match = metric_max_over_ground_truths(exact_match_score, prediction, ground_truths)
            if int(_exact_match) == 1:
                correct_ids.append(qa["id"])
            exact_match += _exact_match

            f1 += metric_max_over_ground_truths(f1_score, prediction, ground_truths)

    exact_match = exact_match / total
    f1 = f1 / total

    return {"exact_match": exact_match, "f1": f1}, correct_ids


if __name__ == "__main__":
    expected_version = "1.0"
    parser = argparse.ArgumentParser("Official evaluation script for ReCoRD v1.0.")
    parser.add_argument("data_file", help="The dataset file in JSON format.")
    parser.add_argument("pred_file", help="The model prediction file in JSON format.")
    parser.add_argument("--output_correct_ids", action="store_true", help="Output the correctly answered query IDs.")
    args = parser.parse_args()

    with open(args.data_file) as data_file:
        dataset_json = json.load(data_file)
        if dataset_json["version"] != expected_version:
            print(
                "Evaluation expects v-{}, but got dataset with v-{}".format(expected_version, dataset_json["version"]),
                file=sys.stderr,
            )
        dataset = dataset_json["data"]

    with open(args.pred_file) as pred_file:
        predictions = json.load(pred_file)

    metrics, correct_ids = evaluate(dataset, predictions)

    if args.output_correct_ids:
        print("Output {} correctly answered question IDs.".format(len(correct_ids)))
        with open("correct_ids.json", "w") as f:
            json.dump(correct_ids, f)
