# Metric Card for Google BLEU (GLEU)


## Metric Description
The BLEU score has some undesirable properties when used for single
sentences, as it was designed to be a corpus measure. The Google BLEU score, also known as GLEU score, is designed to limit these undesirable properties when used for single sentences.

To calculate this score, all sub-sequences of 1, 2, 3 or 4 tokens in output and target sequence (n-grams) are recorded. The precision and recall, described below, are then computed.

- **precision:** the ratio of the number of matching n-grams to the number of total n-grams in the generated output sequence
- **recall:** the ratio of the number of matching n-grams to the number of total n-grams in the target (ground truth) sequence

The minimum value of precision and recall is then returned as the score.


## Intended Uses
This metric is generally used to evaluate machine translation models. It is especially used when scores of individual (prediction, reference) sentence pairs are needed, as opposed to when averaging over the (prediction, reference) scores for a whole corpus. That being said, it can also be used when averaging over the scores for a whole corpus.

Because it performs better on individual sentence pairs as compared to BLEU, Google BLEU has also been used in RL experiments.

## How to Use
This metric takes a list of predicted sentences, as well as a list of references. 

```python
sentence1 = "the cat sat on the mat"
sentence2 = "the cat ate the mat"
google_bleu = datasets.load_metric("google_bleu")
result = google_bleu.compute(predictions=[sentence1], references=[sentence2])
print(result)
>>> True
```

### Inputs
- **predictions** (list of str): list of translations to score. Each translation should be tokenized into a list of tokens.
- **references** (list of list of str): list of lists of references for each translation. Each reference should be tokenized into a list of tokens.
- **min_len** (int): The minimum order of n-gram this function should extract. Defaults to 1.
- **max_len** (int): The maximum order of n-gram this function should extract. Defaults to 4.

### Output Values
This metric returns the following in a dict:
- **google_bleu** (float): google_bleu score

The output format is as follows:
```python
{'google_bleu': google_bleu score}
```

This metric can take on values from 0 to 1, inclusive. Higher scores are better, with 0 indicating no matches, and 1 indicating a perfect match. 

Note that this score is symmetrical when switching output and target. This means that, given two sentences, `sentence1` and `sentence2`, whatever score is output when `sentence1` is the predicted sentence and  `sencence2` is the reference sentence will be the same as when the sentences are swapped and `sentence2` is the predicted sentence while `sentence1` is the reference sentence. In code, this looks like:

```python
sentence1 = "the cat sat on the mat".split()
sentence2 = "the cat ate the mat".split()
google_bleu = datasets.load_metric("google_bleu")
result_a = google_bleu.compute(predictions=[sentence1], references=[[sentence2]])
result_b = google_bleu.compute(predictions=[sentence2], references=[[sentence1]])
print(result_a == result_b)
>>> True
```

#### Values from Popular Papers


### Examples
Example with one reference per sample:
```python
hyp1 = ['It', 'is', 'a', 'guide', 'to', 'action', 'which',
        'ensures', 'that', 'the', 'rubber', 'duck', 'always',
        'disobeys', 'the', 'commands', 'of', 'the', 'cat']
ref1a = ['It', 'is', 'the', 'guiding', 'principle', 'which',
         'guarantees', 'the', 'rubber', 'duck', 'forces', 'never',
         'being', 'under', 'the', 'command', 'of', 'the', 'cat']

hyp2 = ['he', 'read', 'the', 'book', 'because', 'he', 'was',
        'interested', 'in', 'world', 'history']
ref2a = ['he', 'was', 'interested', 'in', 'world', 'history',
         'because', 'he', 'read', 'the', 'book']

list_of_references = [[ref1a], [ref2a]]
hypotheses = [hyp1, hyp2]
google_bleu = datasets.load_metric("google_bleu")
results = google_bleu.compute(predictions=hypotheses, references=list_of_references)
print(round(results["google_bleu"], 2))
>>> 0.44
```

Example with multiple references for the first sample:
```python
hyp1 = ['It', 'is', 'a', 'guide', 'to', 'action', 'which',
        'ensures', 'that', 'the', 'rubber', 'duck', 'always',
        'disobeys', 'the', 'commands', 'of', 'the', 'cat']
ref1a = ['It', 'is', 'the', 'guiding', 'principle', 'which',
         'guarantees', 'the', 'rubber', 'duck', 'forces', 'never',
         'being', 'under', 'the', 'command', 'of', 'the', 'cat']
ref1b = ['It', 'is', 'a', 'guide', 'to', 'action', 'that',
         'ensures', 'that', 'the', 'rubber', 'duck', 'will', 'never',
         'heed', 'the', 'cat', 'commands']
ref1c = ['It', 'is', 'the', 'practical', 'guide', 'for', 'the',
         'rubber', 'duck', 'army', 'never', 'to', 'heed', 'the',
         'directions', 'of', 'the', 'cat']

hyp2 = ['he', 'read', 'the', 'book', 'because', 'he', 'was',
        'interested', 'in', 'world', 'history']
ref2a = ['he', 'was', 'interested', 'in', 'world', 'history',
         'because', 'he', 'read', 'the', 'book']

list_of_references = [[ref1a, ref1b, ref1c], [ref2a]]
hypotheses = [hyp1, hyp2]
google_bleu = datasets.load_metric("google_bleu")
results = google_bleu.compute(predictions=hypotheses, references=list_of_references)
print(round(results["google_bleu"], 2))
>>> 0.61
```

Example with multiple references for the first sample, and with `min_len` adjusted to `2`, instead of the default `1`:
```python
hyp1 = ['It', 'is', 'a', 'guide', 'to', 'action', 'which',
        'ensures', 'that', 'the', 'rubber', 'duck', 'always',
        'disobeys', 'the', 'commands', 'of', 'the', 'cat']
ref1a = ['It', 'is', 'the', 'guiding', 'principle', 'which',
         'guarantees', 'the', 'rubber', 'duck', 'forces', 'never',
         'being', 'under', 'the', 'command', 'of', 'the', 'cat']
ref1b = ['It', 'is', 'a', 'guide', 'to', 'action', 'that',
         'ensures', 'that', 'the', 'rubber', 'duck', 'will', 'never',
         'heed', 'the', 'cat', 'commands']
ref1c = ['It', 'is', 'the', 'practical', 'guide', 'for', 'the',
         'rubber', 'duck', 'army', 'never', 'to', 'heed', 'the',
         'directions', 'of', 'the', 'cat']

hyp2 = ['he', 'read', 'the', 'book', 'because', 'he', 'was',
        'interested', 'in', 'world', 'history']
ref2a = ['he', 'was', 'interested', 'in', 'world', 'history',
         'because', 'he', 'read', 'the', 'book']

list_of_references = [[ref1a, ref1b, ref1c], [ref2a]]
hypotheses = [hyp1, hyp2]
google_bleu = datasets.load_metric("google_bleu")
results = google_bleu.compute(predictions=hypotheses, references=list_of_references, min_len=2)
print(results["google_bleu"])
>>> 0.53
```

Example with multiple references for the first sample, with `min_len` adjusted to `2`, instead of the default `1`, and `max_len` adjusted to `6` instead of the default `4`:
```python
hyp1 = ['It', 'is', 'a', 'guide', 'to', 'action', 'which',
        'ensures', 'that', 'the', 'rubber', 'duck', 'always',
        'disobeys', 'the', 'commands', 'of', 'the', 'cat']
ref1a = ['It', 'is', 'the', 'guiding', 'principle', 'which',
         'guarantees', 'the', 'rubber', 'duck', 'forces', 'never',
         'being', 'under', 'the', 'command', 'of', 'the', 'cat']
ref1b = ['It', 'is', 'a', 'guide', 'to', 'action', 'that',
         'ensures', 'that', 'the', 'rubber', 'duck', 'will', 'never',
         'heed', 'the', 'cat', 'commands']
ref1c = ['It', 'is', 'the', 'practical', 'guide', 'for', 'the',
         'rubber', 'duck', 'army', 'never', 'to', 'heed', 'the',
         'directions', 'of', 'the', 'cat']

hyp2 = ['he', 'read', 'the', 'book', 'because', 'he', 'was',
        'interested', 'in', 'world', 'history']
ref2a = ['he', 'was', 'interested', 'in', 'world', 'history',
         'because', 'he', 'read', 'the', 'book']

list_of_references = [[ref1a, ref1b, ref1c], [ref2a]]
hypotheses = [hyp1, hyp2]
google_bleu = datasets.load_metric("google_bleu")
results = google_bleu.compute(predictions=hypotheses, references=list_of_references, min_len=2, max_len=6)
print(results["google_bleu"])
>>> 0.4
```

## Limitations and Bias


## Citation
```bibtex
@misc{wu2016googles,
title={Google's Neural Machine Translation System: Bridging the Gap between Human and Machine Translation},
author={Yonghui Wu and Mike Schuster and Zhifeng Chen and Quoc V. Le and Mohammad Norouzi and Wolfgang Macherey and Maxim Krikun and Yuan Cao and Qin Gao and Klaus Macherey and Jeff Klingner and Apurva Shah and Melvin Johnson and Xiaobing Liu and Łukasz Kaiser and Stephan Gouws and Yoshikiyo Kato and Taku Kudo and Hideto Kazawa and Keith Stevens and George Kurian and Nishant Patil and Wei Wang and Cliff Young and Jason Smith and Jason Riesa and Alex Rudnick and Oriol Vinyals and Greg Corrado and Macduff Hughes and Jeffrey Dean},
year={2016},
eprint={1609.08144},
archivePrefix={arXiv},
primaryClass={cs.CL}
}
```
## Further References
- This Hugging Face implementation uses the [nltk.translate.gleu_score implementation](https://www.nltk.org/_modules/nltk/translate/gleu_score.html)