from .utils import n_grams, tokenize
import collections
import math

MAX_ORDER = 4
def bleu_score(reference_corpus, translation_corpus, n,
                 smooth=False):
    """Computes BLEU score of translated segments against one or more references.
    Args:
        reference_corpus: list of lists of references for each translation. Each
            reference should be tokenized into a list of tokens.
        translation_corpus: list of translations to score. Each translation
            should be tokenized into a list of tokens.
        n:  n-gram order to use when computing BLEU score. (maximum value to 4)
        smooth: Whether or not to apply Lin et al. 2004 smoothing.
    Returns:
        3-Tuple with the BLEU score, n-gram precisions, geometric mean of n-gram
        precisions and brevity penalty.
    """
    assert n <=MAX_ORDER, "Please setcompute_bleu a smaller value for n. The n-gram order should be less or equal to 4"
    matches_by_order = [0] * n
    possible_matches_by_order = [0] * n
    reference_length = 0
    translation_length = 0
    for (references, translation) in zip(reference_corpus,
                                        translation_corpus):
        reference_length += min(len(tokenize(r)) for r in references)
        translation = tokenize(translation)
        translation_length += len(translation)

        ref_ngram_counts = collections.Counter()
        for reference in references:
            reference = tokenize(reference)
            ref_ngram_counts |= n_grams(reference, n)
        translation_ngram_counts = n_grams(translation, n)
        overlap = translation_ngram_counts & ref_ngram_counts
        for ngram in overlap:
            matches_by_order[len(ngram)-1] += overlap[ngram]
        for order in range(1, n+1):
            possible_matches = len(translation) - order + 1
        if possible_matches > 0:
            possible_matches_by_order[order-1] += possible_matches

    precisions = [0] * n
    for i in range(0, n):
        if smooth:
            precisions[i] = ((matches_by_order[i] + 1.) /
                        (possible_matches_by_order[i] + 1.))
        else:
            if possible_matches_by_order[i] > 0:
                precisions[i] = (float(matches_by_order[i]) /
                            possible_matches_by_order[i])
            else:
                precisions[i] = 0.0

    if min(precisions) > 0:
        p_log_sum = sum((1. / n) * math.log(p) for p in precisions)
        geo_mean = math.exp(p_log_sum)
    else:
        geo_mean = 0

    ratio = float(translation_length) / reference_length

    if ratio > 1.0:
        bp = 1.
    else:
        bp = math.exp(1 - 1. / ratio)

    bleu = geo_mean * bp

    return bleu


    
    
