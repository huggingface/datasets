"""

This file is using the seqeval lib to compute accuracy, f1, precision and recall scores.
seqeval support the following metrics: 
        accuracy_score, 
        f1_score, 
        precision_score, 
        recal_score
for documentation, please refer to https://github.com/chakki-works/seqeval

you can use seqeval with nlp as follow:
    from nlp.metrics.seqeval import Seqeval
    references = [['O', 'O', 'O', 'B-MISC', 'I-MISC', 'I-MISC', 'O'], ['B-PER', 'I-PER', 'O']]
    predictions = [['O', 'O', 'B-MISC', 'I-MISC', 'I-MISC', 'I-MISC', 'O'], ['B-PER', 'I-PER', 'O']]
    Seqeval.compute(predictions, references, accuracy=True, f1=True)
    this will return a dictionary with two values (accuracy_score and f1_score)
    you can also set the precision and recal to true if you want to compute them

"""

from nlp import metric

try:
     from seqeval.metrics import accuracy_score, recall_score, f1_score, precision_score
except:
    raise ImportError("You need to install seqeval. Run `pip install seqeval[cpu]` if you are running on CPU or `pip install seqeval[gpu]` on GPU")

class Seqeval(metric.Metric):
    
    def compute(predictions, references, accuracy=True, f1=False, recal=False, precision=False):
        scores = {}
        if accuracy:
            scores['Accuracy'] = _accuracy_score(predictions, references)
        if f1:
            scores['F1_score'] = _f1_score(predictions, references)
        if precision:
            scores['Precision'] = _precision_score(precision, references)
        if recal:
            scores['Recal'] = _recall_score(predictions, references)
            
        return scores
    
def _accuracy_score(predictions, references):
    return accuracy_score(predictions, references)

def _f1_score(predictions, references):
    return f1_score(predictions, references)

def _precision_score(predictions, references):
    return precision_score(predictions, references)

def _recall_score(predictions, references):
    return recall_score(predictions, references)