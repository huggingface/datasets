# Metric Card for chrF(++)


## Metric Description
ChrF and ChrF++ are two MT evaluation metrics that use the F-score statistic for character n-gram matches. ChrF++ additionally includes word n-grams, which correlate more strongly with direct assessment. We use the implementation that is already present in sacrebleu.

While this metric is included in sacreBLEU, the implementation here is slightly different from sacreBLEU in terms of the required input format. Here, the length of the references and hypotheses lists need to be the same, so you may need to transpose your references compared to sacrebleu's required input format. See https://github.com/huggingface/datasets/issues/3154#issuecomment-950746534

See the [sacreBLEU README.md](https://github.com/mjpost/sacreBLEU#chrf--chrf) for more information.


## How to Use
At minimum, this metric requires a `list` of predictions and a `list` of `list`s of references:
```python
>>> prediction = ["The relationship between cats and dogs is not exactly friendly.", "a good bookshop is just a genteel black hole that knows how to read."]
>>> reference = [["The relationship between dogs and cats is not exactly friendly.", ], ["A good bookshop is just a genteel Black Hole that knows how to read."]]
>>> chrf = datasets.load_metric("chrf")
>>> results = chrf.compute(predictions=prediction, references=reference)
>>> print(results)
{'score': 84.64214891738334, 'char_order': 6, 'word_order': 0, 'beta': 2}
```

### Inputs
- **`predictions`** (`list` of `str`): The predicted sentences.
- **`references`** (`list` of `list` of `str`): The references. There should be one reference sub-list for each prediction sentence.
- **`char_order`** (`int`): Character n-gram order. Defaults to `6`. 
- **`word_order`** (`int`): Word n-gram order. If equals to 2, the metric is referred to as chrF++. Defaults to `0`.
- **`beta`** (`int`): Determine the importance of recall w.r.t precision. Defaults to `2`.
- **`lowercase`** (`bool`): If `True`, enables case-insensitivity. Defaults to `False`.
- **`whitespace`** (`bool`): If `True`, include whitespaces when extracting character n-grams. Defaults to `False`.
- **`eps_smoothing`** (`bool`): If `True`, applies epsilon smoothing similar to reference chrF++.py, NLTK, and Moses implementations. If `False`, takes into account effective match order similar to sacreBLEU < 2.0.0. Defaults to `False`.



### Output Values
The output is a dictionary containing the following fields:
- **`'score'`** (`float`): The chrF (chrF++) score.
- **`'char_order'`** (`int`): The character n-gram order.
- **`'word_order'`** (`int`): The word n-gram order. If equals to `2`, the metric is referred to as chrF++.
- **`'beta'`** (`int`): Determine the importance of recall w.r.t precision.


The output is formatted as below:
```python
{'score': 61.576379378113785, 'char_order': 6, 'word_order': 0, 'beta': 2}
```

The chrF(++) score can be any value between `0.0` and `100.0`, inclusive.

#### Values from Popular Papers


### Examples
A simple example of calculating chrF:
```python
>>> prediction = ["The relationship between cats and dogs is not exactly friendly.", "a good bookshop is just a genteel black hole that knows how to read."]
>>> reference = [["The relationship between dogs and cats is not exactly friendly.", ], ["A good bookshop is just a genteel Black Hole that knows how to read."]]
>>> chrf = datasets.load_metric("chrf")
>>> results = chrf.compute(predictions=prediction, references=reference)
>>> print(results)
{'score': 84.64214891738334, 'char_order': 6, 'word_order': 0, 'beta': 2}
```

The same example, but with the argument `word_order=2`, to calculate chrF++ instead of chrF:
```python
>>> prediction = ["The relationship between cats and dogs is not exactly friendly.", "a good bookshop is just a genteel black hole that knows how to read."]
>>> reference = [["The relationship between dogs and cats is not exactly friendly.", ], ["A good bookshop is just a genteel Black Hole that knows how to read."]]
>>> chrf = datasets.load_metric("chrf")
>>> results = chrf.compute(predictions=prediction,
...                         references=reference,
...                         word_order=2)
>>> print(results)
{'score': 82.87263732906315, 'char_order': 6, 'word_order': 2, 'beta': 2}
```

The same chrF++ example as above, but with `lowercase=True` to normalize all case:
```python
>>> prediction = ["The relationship between cats and dogs is not exactly friendly.", "a good bookshop is just a genteel black hole that knows how to read."]
>>> reference = [["The relationship between dogs and cats is not exactly friendly.", ], ["A good bookshop is just a genteel Black Hole that knows how to read."]]
>>> chrf = datasets.load_metric("chrf")
>>> results = chrf.compute(predictions=prediction,
...                         references=reference,
...                         word_order=2,
...                         lowercase=True)
>>> print(results)
{'score': 92.12853119829202, 'char_order': 6, 'word_order': 2, 'beta': 2}
```


## Limitations and Bias
- According to [Popović 2017](https://www.statmt.org/wmt17/pdf/WMT70.pdf), chrF+ (where `word_order=1`) and chrF++ (where `word_order=2`) produce scores that correlate better with human judgements than chrF (where `word_order=0`) does. 

## Citation
```bibtex
@inproceedings{popovic-2015-chrf,
    title = "chr{F}: character n-gram {F}-score for automatic {MT} evaluation",
    author = "Popovi{\'c}, Maja",
    booktitle = "Proceedings of the Tenth Workshop on Statistical Machine Translation",
    month = sep,
    year = "2015",
    address = "Lisbon, Portugal",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/W15-3049",
    doi = "10.18653/v1/W15-3049",
    pages = "392--395",
}
@inproceedings{popovic-2017-chrf,
    title = "chr{F}++: words helping character n-grams",
    author = "Popovi{\'c}, Maja",
    booktitle = "Proceedings of the Second Conference on Machine Translation",
    month = sep,
    year = "2017",
    address = "Copenhagen, Denmark",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/W17-4770",
    doi = "10.18653/v1/W17-4770",
    pages = "612--618",
}
@inproceedings{post-2018-call,
    title = "A Call for Clarity in Reporting {BLEU} Scores",
    author = "Post, Matt",
    booktitle = "Proceedings of the Third Conference on Machine Translation: Research Papers",
    month = oct,
    year = "2018",
    address = "Belgium, Brussels",
    publisher = "Association for Computational Linguistics",
    url = "https://www.aclweb.org/anthology/W18-6319",
    pages = "186--191",
}
```

## Further References
- See the [sacreBLEU README.md](https://github.com/mjpost/sacreBLEU#chrf--chrf) for more information on this implementation.