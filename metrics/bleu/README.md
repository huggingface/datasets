# Metric Card for BLEU


## Metric Description
BLEU (Bilingual Evaluation Understudy) is an algorithm for evaluating the quality of text which has been machine-translated from one natural language to another. Quality is considered to be the correspondence between a machine's output and that of a human: "the closer a machine translation is to a professional human translation, the better it is" – this is the central idea behind BLEU. BLEU was one of the first metrics to claim a high correlation with human judgements of quality, and remains one of the most popular automated and inexpensive metrics. 

Scores are calculated for individual translated segments—generally sentences—by comparing them with a set of good quality reference translations. Those scores are then averaged over the whole corpus to reach an estimate of the translation's overall quality. Neither intelligibility nor grammatical correctness are not taken into account. 

## Intended Uses
BLEU and BLEU-derived metrics are most often used for machine translation.

## How to Use

This metric takes as input lists of predicted sentences and reference sentences:

```python
>>> predictions = [
...     ["hello", "there", "general", "kenobi",
...     ["foo", "bar" "foobar"]
... ]
>>> references = [
...     [["hello", "there", "general", "kenobi"]],
...     [["foo", "bar", "foobar"]]
... ]
>>> bleu = datasets.load_metric("bleu")
>>> results = bleu.compute(predictions=predictions, references=references)
>>> print(results)
{'bleu': 0.6370964381207871, 'precisions': [0.8333333333333334, 0.75, 1.0, 1.0], 'brevity_penalty': 0.7165313105737893, 'length_ratio': 0.75, 'translation_length': 6, 'reference_length': 8}
```

### Inputs
- **predictions** (`list` of `list`s): Translations to score. Each translation should be tokenized into a list of tokens.
- **references** (`list` of `list`s): references for each translation. Each reference should be tokenized into a list of tokens.
- **max_order** (`int`): Maximum n-gram order to use when computing BLEU score. Defaults to `4`.
- **smooth** (`boolean`): Whether or not to apply Lin et al. 2004 smoothing. Defaults to `False`.

### Output Values
- **bleu** (`float`): bleu score
- **precisions** (`list` of `float`s): geometric mean of n-gram precisions,
- **brevity_penalty** (`float`): brevity penalty,
- **length_ratio** (`float`): ratio of lengths,
- **translation_length** (`int`): translation_length,
- **reference_length** (`int`): reference_length

Output Example:
```python
{'bleu': 1.0, 'precisions': [1.0, 1.0, 1.0, 1.0], 'brevity_penalty': 1.0, 'length_ratio': 1.167, 'translation_length': 7, 'reference_length': 6}
```

BLEU's output is always a number between 0 and 1. This value indicates how similar the candidate text is to the reference texts, with values closer to 1 representing more similar texts. Few human translations will attain a score of 1, since this would indicate that the candidate is identical to one of the reference translations. For this reason, it is not necessary to attain a score of 1. Because there are more opportunities to match, adding additional reference translations will increase the BLEU score.

#### Values from Popular Papers
The [original BLEU paper](https://aclanthology.org/P02-1040/) (Papineni et al. 2002) compares BLEU scores of five different models on the same 500-sentence corpus. These scores ranged from 0.0527 to 0.2571.

The [Attention is All you Need paper](https://proceedings.neurips.cc/paper/2017/file/3f5ee243547dee91fbd053c1c4a845aa-Paper.pdf) (Vaswani et al. 2017) got a BLEU score of 0.284 on the WMT 2014 English-to-German translation task, and 0.41 on the WMT 2014 English-to-French translation task.

### Examples

Example where each sample has 1 reference:
```python
>>> predictions = [
...     ["hello", "there", "general", "kenobi",
...     ["foo", "bar" "foobar"]
... ]
>>> references = [
...     [["hello", "there", "general", "kenobi"]],
...     [["foo", "bar", "foobar"]]
... ]
>>> bleu = datasets.load_metric("bleu")
>>> results = bleu.compute(predictions=predictions, references=references)
>>> print(results)
{'bleu': 0.6370964381207871, 'precisions': [0.8333333333333334, 0.75, 1.0, 1.0], 'brevity_penalty': 0.7165313105737893, 'length_ratio': 0.75, 'translation_length': 6, 'reference_length': 8}
```

Example where the second sample has 2 references:
```python
>>> predictions = [
...     ["hello", "there", "general", "kenobi",
...     ["foo", "bar" "foobar"]
... ]
>>> references = [
...     [["hello", "there", "general", "kenobi"], ["hello", "there", "!"]],
...     [["foo", "bar", "foobar"]]
... ]
>>> bleu = datasets.load_metric("bleu")
>>> results = bleu.compute(predictions=predictions, references=references)
>>> print(results)
{'bleu': 1.0, 'precisions': [1.0, 1.0, 1.0, 1.0], 'brevity_penalty': 1.0, 'length_ratio': 1.1666666666666667, 'translation_length': 7, 'reference_length': 6}
```

## Limitations and Bias
This metric hase multiple known limitations and biases:
- BLEU compares overlap in tokens from the predictions and references, instead of comparing meaning. This can lead to discrepencies between BLEU scores and human ratings. 
- BLEU scores are not comparable across different datasets, nor are they comparable across different languages.
- BLEU scores can vary greatly depending on which parameters are used to generate the scores, especially when different tokenization and normalization techniques are used. It is therefore not possible to compare BLEU scores generated using different parameters, or when these parameters are unknown.
- Shorter predicted translations achieve higher scores than longer ones, simply due to how the score is calculated. A brevity penalty is introduced to attempt to counteract this.


## Citation
```bibtex
@INPROCEEDINGS{Papineni02bleu:a,
    author = {Kishore Papineni and Salim Roukos and Todd Ward and Wei-jing Zhu},
    title = {BLEU: a Method for Automatic Evaluation of Machine Translation},
    booktitle = {},
    year = {2002},
    pages = {311--318}
}
@inproceedings{lin-och-2004-orange,
    title = "{ORANGE}: a Method for Evaluating Automatic Evaluation Metrics for Machine Translation",
    author = "Lin, Chin-Yew  and
      Och, Franz Josef",
    booktitle = "{COLING} 2004: Proceedings of the 20th International Conference on Computational Linguistics",
    month = "aug 23{--}aug 27",
    year = "2004",
    address = "Geneva, Switzerland",
    publisher = "COLING",
    url = "https://www.aclweb.org/anthology/C04-1072",
    pages = "501--507",
}
```

## Further References
- This Hugging Face implementation uses [this Tensorflow implementation](https://github.com/tensorflow/nmt/blob/master/nmt/scripts/bleu.py)
