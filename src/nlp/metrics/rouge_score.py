from nlp.metrics import metric_utils
import os
CURRENT_FILE_DIRECTORY = os.path.dirname(os.path.abspath(__file__))

metric_utils.load_metric_module(CURRENT_FILE_DIRECTORY, name='rouge_import.py')
  ## we only have one file remote import
try:
    from nlp.metrics.rouge.rouge import rouge
except ImportError:
    raise ImportError('No module named rouge')
from nlp.metrics import metric

class Rouge(metric.Metric):
    def compute(predictions, refencences):
        score = rouge(predictions, refencences)
        return score


