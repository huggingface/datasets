import nlp
from .bleu import compute_bleu  # From: https://github.com/tensorflow/nmt/blob/master/nmt/scripts/bleu.py

class Bleu(nlp.Metric):
    def compute(self, predictions, refencences):
        score = compute_bleu(refencences, predictions)
        return score[0]
