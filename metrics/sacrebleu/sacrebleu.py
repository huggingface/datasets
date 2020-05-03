import nlp
import sacrebleu

class Sacrebleu(nlp.Metric):
    def compute(self, predictions, references):
        return sacrebleu.corpus_bleu(predictions, references)
