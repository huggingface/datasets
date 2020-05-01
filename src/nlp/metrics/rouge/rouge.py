"""ROUGE metric implementation.

Copy from tf_seq2seq/seq2seq/metrics/rouge.py.
This is a modified and slightly extended verison of
https://github.com/miso-belica/sumy/blob/dev/sumy/evaluation/rouge.py.
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import itertools
import numpy as np

#pylint: disable=C0103


def _get_ngrams(n, text):
  """Calcualtes n-grams.

  Args:
    n: which n-grams to calculate
    text: An array of tokens

  Returns:
    A set of n-grams
  """
  ngram_set = set()
  text_length = len(text)
  max_index_ngram_start = text_length - n
  for i in range(max_index_ngram_start + 1):
    ngram_set.add(tuple(text[i:i + n]))
  return ngram_set


def _split_into_words(sentences):
  """Splits multiple sentences into words and flattens the result"""
  return list(itertools.chain(*[_.split(" ") for _ in sentences]))


def _get_word_ngrams(n, sentences):
  """Calculates word n-grams for multiple sentences.
  """
  assert len(sentences) > 0
  assert n > 0

  words = _split_into_words(sentences)
  return _get_ngrams(n, words)


def _len_lcs(x, y):
  """
  Returns the length of the Longest Common Subsequence between sequences x
  and y.
  Source: http://www.algorithmist.com/index.php/Longest_Common_Subsequence

  Args:
    x: sequence of words
    y: sequence of words

  Returns
    integer: Length of LCS between x and y
  """
  table = _lcs(x, y)
  n, m = len(x), len(y)
  return table[n, m]


def _lcs(x, y):
  """
  Computes the length of the longest common subsequence (lcs) between two
  strings. The implementation below uses a DP programming algorithm and runs
  in O(nm) time where n = len(x) and m = len(y).
  Source: http://www.algorithmist.com/index.php/Longest_Common_Subsequence

  Args:
    x: collection of words
    y: collection of words

  Returns:
    Table of dictionary of coord and len lcs
  """
  n, m = len(x), len(y)
  table = dict()
  for i in range(n + 1):
    for j in range(m + 1):
      if i == 0 or j == 0:
        table[i, j] = 0
      elif x[i - 1] == y[j - 1]:
        table[i, j] = table[i - 1, j - 1] + 1
      else:
        table[i, j] = max(table[i - 1, j], table[i, j - 1])
  return table


def _recon_lcs(x, y):
  """
  Returns the Longest Subsequence between x and y.
  Source: http://www.algorithmist.com/index.php/Longest_Common_Subsequence

  Args:
    x: sequence of words
    y: sequence of words

  Returns:
    sequence: LCS of x and y
  """
  i, j = len(x), len(y)
  table = _lcs(x, y)

  def _recon(i, j):
    """private recon calculation"""
    if i == 0 or j == 0:
      return []
    elif x[i - 1] == y[j - 1]:
      return _recon(i - 1, j - 1) + [(x[i - 1], i)]
    elif table[i - 1, j] > table[i, j - 1]:
      return _recon(i - 1, j)
    else:
      return _recon(i, j - 1)

  recon_tuple = tuple(map(lambda x: x[0], _recon(i, j)))
  return recon_tuple


def rouge_n(evaluated_sentences, reference_sentences, n=2):
  """
  Computes ROUGE-N of two text collections of sentences.
  Sourece: http://research.microsoft.com/en-us/um/people/cyl/download/
  papers/rouge-working-note-v1.3.1.pdf

  Args:
    evaluated_sentences: The sentences that have been picked by the summarizer
    reference_sentences: The sentences from the referene set
    n: Size of ngram.  Defaults to 2.

  Returns:
    A tuple (f1, precision, recall) for ROUGE-N

  Raises:
    ValueError: raises exception if a param has len <= 0
  """
  if len(evaluated_sentences) <= 0 or len(reference_sentences) <= 0:
    raise ValueError("Collections must contain at least 1 sentence.")

  evaluated_ngrams = _get_word_ngrams(n, evaluated_sentences)
  reference_ngrams = _get_word_ngrams(n, reference_sentences)
  reference_count = len(reference_ngrams)
  evaluated_count = len(evaluated_ngrams)

  # Gets the overlapping ngrams between evaluated and reference
  overlapping_ngrams = evaluated_ngrams.intersection(reference_ngrams)
  overlapping_count = len(overlapping_ngrams)

  # Handle edge case. This isn't mathematically correct, but it's good enough
  if evaluated_count == 0:
    precision = 0.0
  else:
    precision = overlapping_count / evaluated_count

  if reference_count == 0:
    recall = 0.0
  else:
    recall = overlapping_count / reference_count

  f1_score = 2.0 * ((precision * recall) / (precision + recall + 1e-8))

  # return overlapping_count / reference_count
  return f1_score, precision, recall


def _f_p_r_lcs(llcs, m, n):
  """
  Computes the LCS-based F-measure score
  Source: http://research.microsoft.com/en-us/um/people/cyl/download/papers/
  rouge-working-note-v1.3.1.pdf

  Args:
    llcs: Length of LCS
    m: number of words in reference summary
    n: number of words in candidate summary

  Returns:
    Float. LCS-based F-measure score
  """
  r_lcs = llcs / m
  p_lcs = llcs / n
  beta = p_lcs / (r_lcs + 1e-12)
  num = (1 + (beta**2)) * r_lcs * p_lcs
  denom = r_lcs + ((beta**2) * p_lcs)
  f_lcs = num / (denom + 1e-12)
  return f_lcs, p_lcs, r_lcs


def rouge_l_sentence_level(evaluated_sentences, reference_sentences):
  """
  Computes ROUGE-L (sentence level) of two text collections of sentences.
  http://research.microsoft.com/en-us/um/people/cyl/download/papers/
  rouge-working-note-v1.3.1.pdf

  Calculated according to:
  R_lcs = LCS(X,Y)/m
  P_lcs = LCS(X,Y)/n
  F_lcs = ((1 + beta^2)*R_lcs*P_lcs) / (R_lcs + (beta^2) * P_lcs)

  where:
  X = reference summary
  Y = Candidate summary
  m = length of reference summary
  n = length of candidate summary

  Args:
    evaluated_sentences: The sentences that have been picked by the summarizer
    reference_sentences: The sentences from the referene set

  Returns:
    A float: F_lcs

  Raises:
    ValueError: raises exception if a param has len <= 0
  """
  if len(evaluated_sentences) <= 0 or len(reference_sentences) <= 0:
    raise ValueError("Collections must contain at least 1 sentence.")
  reference_words = _split_into_words(reference_sentences)
  evaluated_words = _split_into_words(evaluated_sentences)
  m = len(reference_words)
  n = len(evaluated_words)
  lcs = _len_lcs(evaluated_words, reference_words)
  return _f_p_r_lcs(lcs, m, n)


def _union_lcs(evaluated_sentences, reference_sentence):
  """
  Returns LCS_u(r_i, C) which is the LCS score of the union longest common
  subsequence between reference sentence ri and candidate summary C. For example
  if r_i= w1 w2 w3 w4 w5, and C contains two sentences: c1 = w1 w2 w6 w7 w8 and
  c2 = w1 w3 w8 w9 w5, then the longest common subsequence of r_i and c1 is
  "w1 w2" and the longest common subsequence of r_i and c2 is "w1 w3 w5". The
  union longest common subsequence of r_i, c1, and c2 is "w1 w2 w3 w5" and
  LCS_u(r_i, C) = 4/5.

  Args:
    evaluated_sentences: The sentences that have been picked by the summarizer
    reference_sentence: One of the sentences in the reference summaries

  Returns:
    float: LCS_u(r_i, C)

  ValueError:
    Raises exception if a param has len <= 0
  """
  if len(evaluated_sentences) <= 0:
    raise ValueError("Collections must contain at least 1 sentence.")

  lcs_union = set()
  reference_words = _split_into_words([reference_sentence])
  combined_lcs_length = 0
  for eval_s in evaluated_sentences:
    evaluated_words = _split_into_words([eval_s])
    lcs = set(_recon_lcs(reference_words, evaluated_words))
    combined_lcs_length += len(lcs)
    lcs_union = lcs_union.union(lcs)

  union_lcs_count = len(lcs_union)
  union_lcs_value = union_lcs_count / combined_lcs_length
  return union_lcs_value


def rouge_l_summary_level(evaluated_sentences, reference_sentences):
  """
  Computes ROUGE-L (summary level) of two text collections of sentences.
  http://research.microsoft.com/en-us/um/people/cyl/download/papers/
  rouge-working-note-v1.3.1.pdf

  Calculated according to:
  R_lcs = SUM(1, u)[LCS<union>(r_i,C)]/m
  P_lcs = SUM(1, u)[LCS<union>(r_i,C)]/n
  F_lcs = ((1 + beta^2)*R_lcs*P_lcs) / (R_lcs + (beta^2) * P_lcs)

  where:
  SUM(i,u) = SUM from i through u
  u = number of sentences in reference summary
  C = Candidate summary made up of v sentences
  m = number of words in reference summary
  n = number of words in candidate summary

  Args:
    evaluated_sentences: The sentences that have been picked by the summarizer
    reference_sentence: One of the sentences in the reference summaries

  Returns:
    A float: F_lcs

  Raises:
    ValueError: raises exception if a param has len <= 0
  """
  if len(evaluated_sentences) <= 0 or len(reference_sentences) <= 0:
    raise ValueError("Collections must contain at least 1 sentence.")

  # total number of words in reference sentences
  m = len(_split_into_words(reference_sentences))

  # total number of words in evaluated sentences
  n = len(_split_into_words(evaluated_sentences))

  union_lcs_sum_across_all_references = 0
  for ref_s in reference_sentences:
    union_lcs_sum_across_all_references += _union_lcs(evaluated_sentences,
                                                      ref_s)
  return _f_p_r_lcs(union_lcs_sum_across_all_references, m, n)


def rouge(hypotheses, references):
  """Calculates average rouge scores for a list of hypotheses and
  references"""

  # Filter out hyps that are of 0 length
  # hyps_and_refs = zip(hypotheses, references)
  # hyps_and_refs = [_ for _ in hyps_and_refs if len(_[0]) > 0]
  # hypotheses, references = zip(*hyps_and_refs)

  # Calculate ROUGE-1 F1, precision, recall scores
  rouge_1 = [
      rouge_n([hyp], [ref], 1) for hyp, ref in zip(hypotheses, references)
  ]
  rouge_1_f, rouge_1_p, rouge_1_r = map(np.mean, zip(*rouge_1))

  # Calculate ROUGE-2 F1, precision, recall scores
  rouge_2 = [
      rouge_n([hyp], [ref], 2) for hyp, ref in zip(hypotheses, references)
  ]
  rouge_2_f, rouge_2_p, rouge_2_r = map(np.mean, zip(*rouge_2))

  # Calculate ROUGE-L F1, precision, recall scores
  rouge_l = [
      rouge_l_sentence_level([hyp], [ref])
      for hyp, ref in zip(hypotheses, references)
  ]
  rouge_l_f, rouge_l_p, rouge_l_r = map(np.mean, zip(*rouge_l))

  return {
      "rouge_1/f_score": rouge_1_f,
      "rouge_1/r_score": rouge_1_r,
      "rouge_1/p_score": rouge_1_p,
      "rouge_2/f_score": rouge_2_f,
      "rouge_2/r_score": rouge_2_r,
      "rouge_2/p_score": rouge_2_p,
      "rouge_l/f_score": rouge_l_f,
      "rouge_l/r_score": rouge_l_r,
      "rouge_l/p_score": rouge_l_p,
  }
