import nlp
from .rouge import rouge  # From: https://github.com/tensorflow/nmt/blob/master/nmt/scripts/rouge.py

class Rouge(nlp.Metric):
    def compute(self, predictions, refencences):
        score = rouge(predictions, refencences)
        return score[0]
