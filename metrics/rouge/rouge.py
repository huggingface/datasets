import nlp
from .nmt_rouge import rouge  # From: https://github.com/tensorflow/nmt/blob/master/nmt/scripts/rouge.py

class Rouge(nlp.Metric):
    def _compute(self, predictions, references):
        score = rouge(predictions, references)
        return score
