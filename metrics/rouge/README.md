# Metric Card for ROUGE

## Metric Description
ROUGE, or Recall-Oriented Understudy for Gisting Evaluation, is a set of metrics and a software package used for evaluating automatic summarization and machine translation software in natural language processing. The metrics compare an automatically produced summary or translation against a reference or a set of references (human-produced) summary or translation.

Note that ROUGE is case insensitive, meaning that upper case letters are treated the same way as lower case letters.

This metrics is a wrapper around the [Google Research reimplementation of ROUGE](https://github.com/google-research/google-research/tree/master/rouge)

## How to Use
At minimum, this metric takes as input a list of predictions and a list of references:
```python
>>> rouge = datasets.load_metric('rouge')
>>> predictions = ["hello there", "general kenobi"]
>>> references = ["hello there", "general kenobi"]
>>> results = rouge.compute(predictions=predictions,
...                         references=references)
>>> print(list(results.keys()))
['rouge1', 'rouge2', 'rougeL', 'rougeLsum']
>>> print(results["rouge1"])
AggregateScore(low=Score(precision=1.0, recall=1.0, fmeasure=1.0), mid=Score(precision=1.0, recall=1.0, fmeasure=1.0), high=Score(precision=1.0, recall=1.0, fmeasure=1.0))
>>> print(results["rouge1"].mid.fmeasure)
1.0
```

### Inputs
- **predictions** (`list`): list of predictions to score. Each prediction
        should be a string with tokens separated by spaces.
- **references** (`list`): list of reference for each prediction. Each
        reference should be a string with tokens separated by spaces.
- **rouge_types** (`list`): A list of rouge types to calculate. Defaults to `['rouge1', 'rouge2', 'rougeL', 'rougeLsum']`.
    - Valid rouge types:
        - `"rouge1"`: unigram (1-gram) based scoring
        - `"rouge2"`: bigram (2-gram) based scoring
        - `"rougeL"`: Longest common subsequence based scoring.
        - `"rougeLSum"`: splits text using `"\n"`
        - See [here](https://github.com/huggingface/datasets/issues/617) for more information
- **use_aggregator** (`boolean`): If True, returns aggregates. Defaults to `True`.
- **use_stemmer** (`boolean`): If `True`, uses Porter stemmer to strip word suffixes. Defaults to `False`.

### Output Values
The output is a dictionary with one entry for each rouge type in the input list `rouge_types`. If `use_aggregator=False`, each dictionary entry is a list of Score objects, with one score for each sentence. Each Score object includes the `precision`, `recall`, and `fmeasure`. E.g. if `rouge_types=['rouge1', 'rouge2']` and `use_aggregator=False`, the output is:

```python
{'rouge1': [Score(precision=1.0, recall=0.5, fmeasure=0.6666666666666666), Score(precision=1.0, recall=1.0, fmeasure=1.0)], 'rouge2': [Score(precision=0.0, recall=0.0, fmeasure=0.0), Score(precision=1.0, recall=1.0, fmeasure=1.0)]}
```

If `rouge_types=['rouge1', 'rouge2']` and `use_aggregator=True`, the output is of the following format:
```python
{'rouge1': AggregateScore(low=Score(precision=1.0, recall=1.0, fmeasure=1.0), mid=Score(precision=1.0, recall=1.0, fmeasure=1.0), high=Score(precision=1.0, recall=1.0, fmeasure=1.0)), 'rouge2': AggregateScore(low=Score(precision=1.0, recall=1.0, fmeasure=1.0), mid=Score(precision=1.0, recall=1.0, fmeasure=1.0), high=Score(precision=1.0, recall=1.0, fmeasure=1.0))}
```

The `precision`, `recall`, and `fmeasure` values all have a range of 0 to 1.


#### Values from Popular Papers


### Examples
An example without aggregation:
```python
>>> rouge = datasets.load_metric('rouge')
>>> predictions = ["hello goodbye", "ankh morpork"]
>>> references = ["goodbye", "general kenobi"]
>>> results = rouge.compute(predictions=predictions,
...                         references=references)
>>> print(list(results.keys()))
['rouge1', 'rouge2', 'rougeL', 'rougeLsum']
>>> print(results["rouge1"])
[Score(precision=0.5, recall=0.5, fmeasure=0.5), Score(precision=0.0, recall=0.0, fmeasure=0.0)]
```

The same example, but with aggregation:
```python
>>> rouge = datasets.load_metric('rouge')
>>> predictions = ["hello goodbye", "ankh morpork"]
>>> references = ["goodbye", "general kenobi"]
>>> results = rouge.compute(predictions=predictions,
...                         references=references,
...                         use_aggregator=True)
>>> print(list(results.keys()))
['rouge1', 'rouge2', 'rougeL', 'rougeLsum']
>>> print(results["rouge1"])
AggregateScore(low=Score(precision=0.0, recall=0.0, fmeasure=0.0), mid=Score(precision=0.25, recall=0.25, fmeasure=0.25), high=Score(precision=0.5, recall=0.5, fmeasure=0.5))
```

The same example, but only calculating `rouge_1`:
```python
>>> rouge = datasets.load_metric('rouge')
>>> predictions = ["hello goodbye", "ankh morpork"]
>>> references = ["goodbye", "general kenobi"]
>>> results = rouge.compute(predictions=predictions,
...                         references=references,
...                         rouge_types=['rouge_1'],
...                         use_aggregator=True)
>>> print(list(results.keys()))
['rouge1']
>>> print(results["rouge1"])
AggregateScore(low=Score(precision=0.0, recall=0.0, fmeasure=0.0), mid=Score(precision=0.25, recall=0.25, fmeasure=0.25), high=Score(precision=0.5, recall=0.5, fmeasure=0.5))
```

## Limitations and Bias
See [Schluter (2017)](https://aclanthology.org/E17-2007/) for an in-depth discussion of many of ROUGE's limits.

## Citation
```bibtex
@inproceedings{lin-2004-rouge,
    title = "{ROUGE}: A Package for Automatic Evaluation of Summaries",
    author = "Lin, Chin-Yew",
    booktitle = "Text Summarization Branches Out",
    month = jul,
    year = "2004",
    address = "Barcelona, Spain",
    publisher = "Association for Computational Linguistics",
    url = "https://www.aclweb.org/anthology/W04-1013",
    pages = "74--81",
}
```

## Further References
- This metrics is a wrapper around the [Google Research reimplementation of ROUGE](https://github.com/google-research/google-research/tree/master/rouge)