# Metric Card for TER

## Metric Description
TER (Translation Edit Rate, also called Translation Error Rate) is a metric to quantify the edit operations that a hypothesis requires to match a reference translation. We use the implementation that is already present in [sacrebleu](https://github.com/mjpost/sacreBLEU#ter), which in turn is inspired by the [TERCOM implementation](https://github.com/jhclark/tercom).

The implementation here is slightly different from sacrebleu in terms of the required input format. The length of the references and hypotheses lists need to be the same, so you may need to transpose your references compared to sacrebleu's required input format. See [this github issue](https://github.com/huggingface/datasets/issues/3154#issuecomment-950746534).

See the README.md file at https://github.com/mjpost/sacreBLEU#ter for more information.


## How to Use
This metric takes, at minimum, predicted sentences and reference sentences:
```python
>>> predictions = ["does this sentence match??",
...                     "what about this sentence?",
...                     "What did the TER metric user say to the developer?"]
>>> references = [["does this sentence match", "does this sentence match!?!"],
...             ["wHaT aBoUt ThIs SeNtEnCe?", "wHaT aBoUt ThIs SeNtEnCe?"],
...             ["Your jokes are...", "...TERrible"]]
>>> ter = datasets.load_metric("ter")
>>> results = ter.compute(predictions=predictions,
...                         references=references,
...                         case_sensitive=True)
>>> print(results)
{'score': 150.0, 'num_edits': 15, 'ref_length': 10.0}
```

### Inputs
This metric takes the following as input:
- **`predictions`** (`list` of `str`): The system stream (a sequence of segments).
- **`references`** (`list` of `list` of `str`): A list of one or more reference streams (each a sequence of segments).
- **`normalized`** (`boolean`): If `True`, applies basic tokenization and normalization to sentences. Defaults to `False`.
- **`ignore_punct`** (`boolean`): If `True`, applies basic tokenization and normalization to sentences. Defaults to `False`.
- **`support_zh_ja_chars`** (`boolean`): If `True`, tokenization/normalization supports processing of Chinese characters, as well as Japanese Kanji, Hiragana, Katakana, and Phonetic Extensions of Katakana. Only applies if `normalized = True`. Defaults to `False`.
- **`case_sensitive`** (`boolean`): If `False`, makes all predictions and references lowercase to ignore differences in case. Defaults to `False`.

### Output Values
This metric returns the following:
- **`score`** (`float`): TER score (num_edits / sum_ref_lengths * 100)
- **`num_edits`** (`int`): The cumulative number of edits
- **`ref_length`** (`float`): The cumulative average reference length

The output takes the following form:
```python
{'score': ter_score, 'num_edits': num_edits, 'ref_length': ref_length}
```

The metric can take on any value `0` and above. `0` is a perfect score, meaning the predictions exactly match the references and no edits were necessary. Higher scores are worse. Scores above 100 mean that the cumulative number of edits, `num_edits`, is higher than the cumulative length of the references, `ref_length`.

#### Values from Popular Papers


### Examples
Basic example with only predictions and references as inputs:
```python
>>> predictions = ["does this sentence match??",
...                     "what about this sentence?"]
>>> references = [["does this sentence match", "does this sentence match!?!"],
...             ["wHaT aBoUt ThIs SeNtEnCe?", "wHaT aBoUt ThIs SeNtEnCe?"]]
>>> ter = datasets.load_metric("ter")
>>> results = ter.compute(predictions=predictions, 
...                         references=references,
...                         case_sensitive=True)
>>> print(results)
{'score': 62.5, 'num_edits': 5, 'ref_length': 8.0}
```

Example with `normalization = True`:
```python
>>> predictions = ["does this sentence match??",
...                     "what about this sentence?"]
>>> references = [["does this sentence match", "does this sentence match!?!"],
...             ["wHaT aBoUt ThIs SeNtEnCe?", "wHaT aBoUt ThIs SeNtEnCe?"]]
>>> ter = datasets.load_metric("ter")
>>> results = ter.compute(predictions=predictions, 
...                         references=references, 
...                         normalized=True,
...                         case_sensitive=True)
>>> print(results)
{'score': 57.14285714285714, 'num_edits': 6, 'ref_length': 10.5}
```

Example ignoring punctuation and capitalization, and everything matches:
```python
>>> predictions = ["does this sentence match??",
...                     "what about this sentence?"]
>>> references = [["does this sentence match", "does this sentence match!?!"],
...             ["wHaT aBoUt ThIs SeNtEnCe?", "wHaT aBoUt ThIs SeNtEnCe?"]]
>>> ter = datasets.load_metric("ter")
>>> results = ter.compute(predictions=predictions, 
...                         references=references, 
...                         ignore_punct=True,
...                         case_sensitive=False)
>>> print(results)
{'score': 0.0, 'num_edits': 0, 'ref_length': 8.0}
```

Example ignoring punctuation and capitalization, but with an extra (incorrect) sample:
```python
>>> predictions = ["does this sentence match??",
...                    "what about this sentence?",
...                    "What did the TER metric user say to the developer?"]
>>> references = [["does this sentence match", "does this sentence match!?!"],
...             ["wHaT aBoUt ThIs SeNtEnCe?", "wHaT aBoUt ThIs SeNtEnCe?"],
...             ["Your jokes are...", "...TERrible"]]
>>> ter = datasets.load_metric("ter")
>>> results = ter.compute(predictions=predictions, 
...                         references=references,
...                         ignore_punct=True,
...                         case_sensitive=False)
>>> print(results)
{'score': 100.0, 'num_edits': 10, 'ref_length': 10.0}
```


## Limitations and Bias


## Citation
```bibtex
@inproceedings{snover-etal-2006-study,
    title = "A Study of Translation Edit Rate with Targeted Human Annotation",
    author = "Snover, Matthew  and
      Dorr, Bonnie  and
      Schwartz, Rich  and
      Micciulla, Linnea  and
      Makhoul, John",
    booktitle = "Proceedings of the 7th Conference of the Association for Machine Translation in the Americas: Technical Papers",
    month = aug # " 8-12",
    year = "2006",
    address = "Cambridge, Massachusetts, USA",
    publisher = "Association for Machine Translation in the Americas",
    url = "https://aclanthology.org/2006.amta-papers.25",
    pages = "223--231",
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
- See [the sacreBLEU github repo](https://github.com/mjpost/sacreBLEU#ter) for more information.
