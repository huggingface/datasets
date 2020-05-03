from nlp.metrics import metric
try:
    import sacrebleu
except ImportError:
    raise ImportError("You need to first install sacrebleu by using pip install sacrebleu")

class Sacrebleu(metric.Metric):
    def compute(predictions, references):
        return sacrebleu.corpus_bleu(predictions, references)
        #return sacrebleu.corpus_bleu(predictions, references)
    