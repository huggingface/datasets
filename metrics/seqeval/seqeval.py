import nlp

from seqeval.metrics import accuracy_score, precision_score, recall_score, f1_score

class Seqeval(nlp.Metric):
    """ Seqeval uses the seqeval library (https://github.com/chakki-works/seqeval) to compute accuracy, f1, precision and recall scores.
        seqeval support the following metrics: 
                accuracy_score, 
                f1_score, 
                precision_score, 
                recal_score
        for documentation, please refer to https://github.com/chakki-works/seqeval

        you can use seqeval with nlp as follow:
            import nlp
            seqeval = nlp.load_metric('seqeval')
            references = [['O', 'O', 'O', 'B-MISC', 'I-MISC', 'I-MISC', 'O'], ['B-PER', 'I-PER', 'O']]
            predictions = [['O', 'O', 'B-MISC', 'I-MISC', 'I-MISC', 'I-MISC', 'O'], ['B-PER', 'I-PER', 'O']]
            seqeval.compute(predictions, references, accuracy=True, f1=True)
            # this will return a dictionary with two values (accuracy_score and f1_score)
            # you can also set the precision and recal to true if you want to compute them

    """
    def _compute(self, predictions, references, accuracy=True, precision=True, recall=True, f1=True, **kwargs):
        scores = {}
        if accuracy:
            scores['accuracy'] = accuracy_score(references, predictions)
        if precision:
            scores['precision'] = precision_score(references, predictions, **kwargs)
        if recall:
            scores['recall'] = recall_score(references, predictions, **kwargs)
        if f1:
            scores['f1'] = f1_score(references, predictions, **kwargs)
            
        return scores
