# Metric Card for seqeval

## Metric description

seqeval is a Python framework for sequence labeling evaluation. seqeval can evaluate the performance of chunking tasks such as named-entity recognition, part-of-speech tagging, semantic role labeling and so on. 


## How to use 

Seqeval produces labelling scores along with its sufficient statistics from a source against one or more references.

It takes two mandatory arguments:

`predictions`: a list of lists of predicted labels, i.e. estimated targets as returned by a tagger.

`references`: a list of lists of reference labels, i.e. the ground truth/target values.

It can also take several optional arguments:

`suffix` (boolean): `True` if the IOB tag is a suffix (after type) instead of a prefix (before type), `False` otherwise. The default value is `False`, i.e. the IOB tag is a prefix (before type).

`scheme`: the target tagging scheme, which can be one of [`IOB1`, `IOB2`, `IOE1`, `IOE2`, `IOBES`, `BILOU`]. The default value is `None`.

`mode`: whether to count correct entity labels with incorrect I/B tags as true positives or not. If you want to only count exact matches, pass `mode="strict"` and a specific `scheme` value. The default is `None`.

`sample_weight`: An array-like of shape (n_samples,) that provides weights for individual samples. The default is `None`. 

`zero_division`: Which value to substitute as a metric value when encountering zero division. Should be one of [`0`,`1`,`"warn"`]. `"warn"` acts as `0`, but the warning is raised.


```python
>>> from datasets import load_metric
>>> seqeval = load_metric('seqeval')
>>> predictions = [['O', 'O', 'B-MISC', 'I-MISC', 'I-MISC', 'I-MISC', 'O'], ['B-PER', 'I-PER', 'O']]
>>> references = [['O', 'O', 'O', 'B-MISC', 'I-MISC', 'I-MISC', 'O'], ['B-PER', 'I-PER', 'O']]
>>> results = seqeval.compute(predictions=predictions, references=references)
```

## Output values

This metric returns a dictionary with a summary of scores for overall and per type:

Overall:

`accuracy`: the average [accuracy](https://huggingface.co/metrics/accuracy), on a scale between 0.0 and 1.0.
    
`precision`: the average [precision](https://huggingface.co/metrics/precision), on a scale between 0.0 and 1.0.
    
`recall`: the average [recall](https://huggingface.co/metrics/recall), on a scale between 0.0 and 1.0.

`f1`: the average [F1 score](https://huggingface.co/metrics/f1), which is the harmonic mean of the precision and recall. It also has a scale of 0.0 to 1.0.

Per type (e.g. `MISC`, `PER`, `LOC`,...):

`precision`: the average [precision](https://huggingface.co/metrics/precision), on a scale between 0.0 and 1.0.

`recall`: the average [recall](https://huggingface.co/metrics/recall), on a scale between 0.0 and 1.0.

`f1`: the average [F1 score](https://huggingface.co/metrics/f1), on a scale between 0.0 and 1.0.


### Values from popular papers
The 1995 "Text Chunking using Transformation-Based Learning" [paper](https://aclanthology.org/W95-0107) reported a baseline recall of 81.9% and a precision of 78.2% using non Deep Learning-based methods. 

More recently, seqeval continues being used for reporting performance on tasks such as [named entity detection](https://www.mdpi.com/2306-5729/6/8/84/htm) and [information extraction](https://ieeexplore.ieee.org/abstract/document/9697942/).


## Examples 

Maximal values (full match) :

```python
>>> from datasets import load_metric
>>> seqeval = load_metric('seqeval')
>>> predictions = [['O', 'O', 'B-MISC', 'I-MISC', 'I-MISC', 'I-MISC', 'O'], ['B-PER', 'I-PER', 'O']]
>>> references = [['O', 'O', 'B-MISC', 'I-MISC', 'I-MISC', 'I-MISC', 'O'], ['B-PER', 'I-PER', 'O']]
>>> results = seqeval.compute(predictions=predictions, references=references)
>>> print(results)
{'MISC': {'precision': 1.0, 'recall': 1.0, 'f1': 1.0, 'number': 1}, 'PER': {'precision': 1.0, 'recall': 1.0, 'f1': 1.0, 'number': 1}, 'overall_precision': 1.0, 'overall_recall': 1.0, 'overall_f1': 1.0, 'overall_accuracy': 1.0}

```

Minimal values (no match):

```python
>>> from datasets import load_metric
>>> seqeval = load_metric('seqeval')
>>> predictions = [['O', 'B-MISC', 'I-MISC'], ['B-PER', 'I-PER', 'O']]
>>> references = [['B-MISC', 'O', 'O'], ['I-PER', '0', 'I-PER']]
>>> results = seqeval.compute(predictions=predictions, references=references)
>>> print(results)
{'MISC': {'precision': 0.0, 'recall': 0.0, 'f1': 0.0, 'number': 1}, 'PER': {'precision': 0.0, 'recall': 0.0, 'f1': 0.0, 'number': 2}, '_': {'precision': 0.0, 'recall': 0.0, 'f1': 0.0, 'number': 1}, 'overall_precision': 0.0, 'overall_recall': 0.0, 'overall_f1': 0.0, 'overall_accuracy': 0.0}
```

Partial match:

```python
>>> from datasets import load_metric
>>> seqeval = load_metric('seqeval')
>>> predictions = [['O', 'O', 'B-MISC', 'I-MISC', 'I-MISC', 'I-MISC', 'O'], ['B-PER', 'I-PER', 'O']]
>>> references = [['O', 'O', 'O', 'B-MISC', 'I-MISC', 'I-MISC', 'O'], ['B-PER', 'I-PER', 'O']]
>>> results = seqeval.compute(predictions=predictions, references=references)
>>> print(results)
{'MISC': {'precision': 0.0, 'recall': 0.0, 'f1': 0.0, 'number': 1}, 'PER': {'precision': 1.0, 'recall': 1.0, 'f1': 1.0, 'number': 1}, 'overall_precision': 0.5, 'overall_recall': 0.5, 'overall_f1': 0.5, 'overall_accuracy': 0.8}
```

## Limitations and bias

seqeval supports following IOB formats (short for inside, outside, beginning) : `IOB1`, `IOB2`, `IOE1`, `IOE2`, `IOBES`, `IOBES` (only in strict mode) and `BILOU` (only in strict mode). 

For more information about IOB formats, refer to the [Wikipedia page](https://en.wikipedia.org/wiki/Inside%E2%80%93outside%E2%80%93beginning_(tagging)) and the description of the [CoNLL-2000 shared task](https://aclanthology.org/W02-2024).


## Citation

```bibtex
@inproceedings{ramshaw-marcus-1995-text,
    title = "Text Chunking using Transformation-Based Learning",
    author = "Ramshaw, Lance  and
      Marcus, Mitch",
    booktitle = "Third Workshop on Very Large Corpora",
    year = "1995",
    url = "https://www.aclweb.org/anthology/W95-0107",
}
```

```bibtex
@misc{seqeval,
  title={{seqeval}: A Python framework for sequence labeling evaluation},
  url={https://github.com/chakki-works/seqeval},
  note={Software available from https://github.com/chakki-works/seqeval},
  author={Hiroki Nakayama},
  year={2018},
}
```
    
## Further References 
- [README for seqeval at GitHub](https://github.com/chakki-works/seqeval)
- [CoNLL-2000 shared task](https://www.clips.uantwerpen.be/conll2002/ner/bin/conlleval.txt)
