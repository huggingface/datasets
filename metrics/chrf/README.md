# Metric Card for chrF(++)


## Metric Description
ChrF and ChrF++ are two MT evaluation metrics that use the F-score statistic for character n-gram matches. ChrF++ additionally includes word n-grams, which correlate more strongly with direct assessment. We use the implementation that is already present in sacrebleu.

While this metric is included in sacreBLEU, the implementation here is slightly different from sacreBLEU in terms of the required input format. Here, the length of the references and hypotheses lists need to be the same, so you may need to transpose your references compared to sacrebleu's required input format. See https://github.com/huggingface/datasets/issues/3154#issuecomment-950746534

See the [sacreBLEU README.md](https://github.com/mjpost/sacreBLEU#chrf--chrf) for more information.


## How to Use
At minimum, this metric requires a `list` of predictions and a `list` of `list`s of references:
```python
>>> prediction = ["The relationship between Obama and Netanyahu is not exactly friendly."]
>>> reference = [["The ties between Obama and Netanyahu are not particularly friendly."]]
>>> chrf = datasets.load_metric("chrf")
>>> results = chrf.compute(predictions=prediction, references=reference)
>>> print(results)
{'score': 61.576379378113785, 'char_order': 6, 'word_order': 0, 'beta': 2}
```

### Inputs
- **`predictions`** (`list` of `str`): The predicted sentences.
- **`references`** (`list` of `list` of `str`): The references. There should be one reference sub-list for each prediction sentence.
- **`char_order`** (`int`): Character n-gram order. Defaults to `6`. 
- **`word_order`** (`int`): Word n-gram order. If equals to 2, the metric is referred to as chrF++. Defaults to `0`.
- **`beta`** (`int`): Determine the importance of recall w.r.t precision. Defaults to `2`.
- **`lowercase`** (`bool`): If `True`, enables case-insensitivity. Defaults to `False`.
- **`whitespace`** (`bool`): If `True`, include whitespaces when extracting character n-grams. Defaults to `False`.
- **`eps_smoothing`** (`bool`): If `True`, applies epsilon smoothing similar to reference chrF++.py, NLTK and Moses implementations. If `False`, takes into account effective match order similar to sacreBLEU < 2.0.0. Defaults to `False`.



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

*State the possible values that the metric's output can take, as well as what is considered a good score.*

#### Values from Popular Papers
*Give examples, preferrably with links, to papers that have reported this metric, along with the values they have reported.*

### Examples
*Give code examples of the metric being used. Try to include examples that clear up any potential ambiguity left from the metric description above.*

## Limitations and Bias
*Note any limitations or biases that the metric has.*

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