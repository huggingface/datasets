""" Official evaluation script for CUAD dataset. """

import argparse
import json
import re
import string
import sys

import numpy as np


IOU_THRESH = 0.5


def get_jaccard(prediction, ground_truth):
    remove_tokens = [".", ",", ";", ":"]

    for token in remove_tokens:
        ground_truth = ground_truth.replace(token, "")
        prediction = prediction.replace(token, "")

    ground_truth, prediction = ground_truth.lower(), prediction.lower()
    ground_truth, prediction = ground_truth.replace("/", " "), prediction.replace("/", " ")
    ground_truth, prediction = set(ground_truth.split(" ")), set(prediction.split(" "))

    intersection = ground_truth.intersection(prediction)
    union = ground_truth.union(prediction)
    jaccard = len(intersection) / len(union)
    return jaccard


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


def compute_precision_recall(predictions, ground_truths, qa_id):
    tp, fp, fn = 0, 0, 0

    substr_ok = "Parties" in qa_id

    # first check if ground truth is empty
    if len(ground_truths) == 0:
        if len(predictions) > 0:
            fp += len(predictions)  # false positive for each one
    else:
        for ground_truth in ground_truths:
            assert len(ground_truth) > 0
            # check if there is a match
            match_found = False
            for pred in predictions:
                if substr_ok:
                    is_match = get_jaccard(pred, ground_truth) >= IOU_THRESH or ground_truth in pred
                else:
                    is_match = get_jaccard(pred, ground_truth) >= IOU_THRESH
                if is_match:
                    match_found = True

            if match_found:
                tp += 1
            else:
                fn += 1

        # now also get any fps by looping through preds
        for pred in predictions:
            # Check if there's a match. if so, don't count (don't want to double count based on the above)
            # but if there's no match, then this is a false positive.
            # (Note: we get the true positives in the above loop instead of this loop so that we don't double count
            # multiple predictions that are matched with the same answer.)
            match_found = False
            for ground_truth in ground_truths:
                assert len(ground_truth) > 0
                if substr_ok:
                    is_match = get_jaccard(pred, ground_truth) >= IOU_THRESH or ground_truth in pred
                else:
                    is_match = get_jaccard(pred, ground_truth) >= IOU_THRESH
                if is_match:
                    match_found = True

            if not match_found:
                fp += 1

    precision = tp / (tp + fp) if tp + fp > 0 else np.nan
    recall = tp / (tp + fn) if tp + fn > 0 else np.nan

    return precision, recall


def process_precisions(precisions):
    """
    Processes precisions to ensure that precision and recall don't both get worse.
    Assumes the list precision is sorted in order of recalls
    """
    precision_best = precisions[::-1]
    for i in range(1, len(precision_best)):
        precision_best[i] = max(precision_best[i - 1], precision_best[i])
    precisions = precision_best[::-1]
    return precisions


def get_aupr(precisions, recalls):
    processed_precisions = process_precisions(precisions)
    aupr = np.trapz(processed_precisions, recalls)
    if np.isnan(aupr):
        return 0
    return aupr


def get_prec_at_recall(precisions, recalls, recall_thresh):
    """Assumes recalls are sorted in increasing order"""
    processed_precisions = process_precisions(precisions)
    prec_at_recall = 0
    for prec, recall in zip(processed_precisions, recalls):
        if recall >= recall_thresh:
            prec_at_recall = prec
            break
    return prec_at_recall


def exact_match_score(prediction, ground_truth):
    return normalize_answer(prediction) == normalize_answer(ground_truth)


def metric_max_over_ground_truths(metric_fn, predictions, ground_truths):
    score = 0
    for pred in predictions:
        for ground_truth in ground_truths:
            score = metric_fn(pred, ground_truth)
            if score == 1:  # break the loop when one prediction matches the ground truth
                break
        if score == 1:
            break
    return score


def evaluate(dataset, predictions):
    f1 = exact_match = total = 0
    precisions = []
    recalls = []
    for article in dataset:
        for paragraph in article["paragraphs"]:
            for qa in paragraph["qas"]:
                total += 1
                if qa["id"] not in predictions:
                    message = "Unanswered question " + qa["id"] + " will receive score 0."
                    print(message, file=sys.stderr)
                    continue
                ground_truths = list(map(lambda x: x["text"], qa["answers"]))
                prediction = predictions[qa["id"]]
                precision, recall = compute_precision_recall(prediction, ground_truths, qa["id"])

                precisions.append(precision)
                recalls.append(recall)

                if precision == 0 and recall == 0:
                    f1 += 0
                else:
                    f1 += 2 * (precision * recall) / (precision + recall)

                exact_match += metric_max_over_ground_truths(exact_match_score, prediction, ground_truths)

    precisions = [x for _, x in sorted(zip(recalls, precisions))]
    recalls.sort()

    f1 = 100.0 * f1 / total
    exact_match = 100.0 * exact_match / total
    aupr = get_aupr(precisions, recalls)

    prec_at_90_recall = get_prec_at_recall(precisions, recalls, recall_thresh=0.9)
    prec_at_80_recall = get_prec_at_recall(precisions, recalls, recall_thresh=0.8)

    return {
        "exact_match": exact_match,
        "f1": f1,
        "aupr": aupr,
        "prec_at_80_recall": prec_at_80_recall,
        "prec_at_90_recall": prec_at_90_recall,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Evaluation for CUAD")
    parser.add_argument("dataset_file", help="Dataset file")
    parser.add_argument("prediction_file", help="Prediction File")
    args = parser.parse_args()
    with open(args.dataset_file) as dataset_file:
        dataset_json = json.load(dataset_file)
        dataset = dataset_json["data"]
    with open(args.prediction_file) as prediction_file:
        predictions = json.load(prediction_file)
    print(json.dumps(evaluate(dataset, predictions)))
