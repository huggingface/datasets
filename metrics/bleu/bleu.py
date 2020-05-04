import nlp
from .nmt_bleu import compute_bleu  # From: https://github.com/tensorflow/nmt/blob/master/nmt/scripts/bleu.py

class Bleu(nlp.Metric):
    def _compute(self, predictions, references):
        score = compute_bleu(references, predictions)
        (bleu, precisions, bp, ratio, translation_length, reference_length) = score
        return {'bleu': bleu,
                'precisions': precisions,
                'bp': bp,
                'ratio': ratio,
                'translation_length': translation_length,
                'reference_length': reference_length}
