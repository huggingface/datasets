import nlp
import sacrebleu

class Sacrebleu(nlp.Metric):
    def _compute(self, predictions, references, **kwargs):
        output = sacrebleu.corpus_bleu(predictions, references, **kwargs)
        output_dict = {
            'score': output.score,
            'counts': output.counts,
            'totals': output.totals,
            'precisions': output.precisions,
            'bp': output.bp,
            'sys_len': output.sys_len,
            'ref_len': output.ref_len,
        }
        return output_dict
