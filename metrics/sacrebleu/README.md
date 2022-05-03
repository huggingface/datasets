# Metric Card for SacreBLEU


## Metric Description
SacreBLEU provides hassle-free computation of shareable, comparable, and reproducible BLEU scores. Inspired by Rico Sennrich's `multi-bleu-detok.perl`, it produces the official Workshop on Machine Translation (WMT) scores but works with plain text. It also knows all the standard test sets and handles downloading, processing, and tokenization.

See the [README.md] file at https://github.com/mjpost/sacreBLEU for more information.

## How to Use
This metric takes a set of predictions and a set of references as input, along with various optional parameters.


```python
>>> predictions = ["hello there general kenobi", "foo bar foobar"]
>>> references = [["hello there general kenobi", "hello there !"],
...                 ["foo bar foobar", "foo bar foobar"]]
>>> sacrebleu = datasets.load_metric("sacrebleu")
>>> results = sacrebleu.compute(predictions=predictions, 
...                             references=references)
>>> print(list(results.keys()))
['score', 'counts', 'totals', 'precisions', 'bp', 'sys_len', 'ref_len']
>>> print(round(results["score"], 1))
100.0
```

### Inputs
- **`predictions`** (`list` of `str`): list of translations to score. Each translation should be tokenized into a list of tokens.
- **`references`** (`list` of `list` of `str`): A list of lists of references. The contents of the first sub-list are the references for the first prediction, the contents of the second sub-list are for the second prediction, etc. Note that there must be the same number of references for each prediction (i.e. all sub-lists must be of the same length).
- **`smooth_method`** (`str`): The smoothing method to use, defaults to `'exp'`. Possible values are:
    - `'none'`: no smoothing
    - `'floor'`: increment zero counts
    - `'add-k'`: increment num/denom by k for n>1
    - `'exp'`: exponential decay
- **`smooth_value`** (`float`): The smoothing value. Only valid when `smooth_method='floor'` (in which case `smooth_value` defaults to `0.1`) or `smooth_method='add-k'` (in which case `smooth_value` defaults to `1`).
- **`tokenize`** (`str`): Tokenization method to use for BLEU. If not provided, defaults to `'zh'` for Chinese, `'ja-mecab'` for Japanese and `'13a'` (mteval) otherwise. Possible values are:
    - `'none'`: No tokenization.
    - `'zh'`: Chinese tokenization.
    - `'13a'`: mimics the `mteval-v13a` script from Moses.
    - `'intl'`: International tokenization, mimics the `mteval-v14` script from Moses
    - `'char'`: Language-agnostic character-level tokenization.
    - `'ja-mecab'`: Japanese tokenization. Uses the [MeCab tokenizer](https://pypi.org/project/mecab-python3).
- **`lowercase`** (`bool`): If `True`, lowercases the input, enabling case-insensitivity. Defaults to `False`.
- **`force`** (`bool`): If `True`, insists that your tokenized input is actually detokenized. Defaults to `False`.
- **`use_effective_order`** (`bool`): If `True`, stops including n-gram orders for which precision is 0. This should be `True`, if sentence-level BLEU will be computed. Defaults to `False`.

### Output Values
- `score`: BLEU score
- `counts`: Counts
- `totals`: Totals
- `precisions`: Precisions
- `bp`: Brevity penalty
- `sys_len`: predictions length
- `ref_len`: reference length

The output is in the following format:
```python
{'score': 39.76353643835252, 'counts': [6, 4, 2, 1], 'totals': [10, 8, 6, 4], 'precisions': [60.0, 50.0, 33.333333333333336, 25.0], 'bp': 1.0, 'sys_len': 10, 'ref_len': 7}
```
The score can take any value between `0.0` and `100.0`, inclusive.

#### Values from Popular Papers


### Examples

```python
>>> predictions = ["hello there general kenobi", 
...                 "on our way to ankh morpork"]
>>> references = [["hello there general kenobi", "hello there !"],
...                 ["goodbye ankh morpork", "ankh morpork"]]
>>> sacrebleu = datasets.load_metric("sacrebleu")
>>> results = sacrebleu.compute(predictions=predictions, 
...                             references=references)
>>> print(list(results.keys()))
['score', 'counts', 'totals', 'precisions', 'bp', 'sys_len', 'ref_len']
>>> print(round(results["score"], 1))
39.8
```

## Limitations and Bias
Because what this metric calculates is BLEU scores, it has the same limitations as that metric, except that sacreBLEU is more easily reproducible.

## Citation
```bibtex
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
- See the [sacreBLEU README.md file](https://github.com/mjpost/sacreBLEU) for more information.