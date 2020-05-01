from nlp.metrics import metric_utils
import os


metric_utils.load_metric_module(os.path.dirname(os.path.abspath(__file__)), name='bleu_imports.py')
try:
    from nlp.metrics.bleu.bleu import compute_bleu
except ImportError:
    raise ImportError('No module named bleu')
from nlp.metrics import metric

class Bleu(metric.Metric):
    def compute(predictions, refencences):
        score = compute_bleu(refencences, predictions)
        return score[0]

    
    
    
