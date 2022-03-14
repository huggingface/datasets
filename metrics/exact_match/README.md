# Metric Card for Exact Match


## Metric Description
A given predicted string's exact match score is 1 if it is the exact same as its reference string, and is 0 otherwise.

- **Example 1**: The exact match score of prediction "Happy Birthday!" is 0, given its reference is "Happy New Year!".
- **Example 2**: The exact match score of prediction "The Colour of Magic (1983)" is 1, given its reference is also "The Colour of Magic (1983)".

The exact match score of a set of predictions is the sum of all of the individual exact match scores in the set, divided by the total number of predictions in the set.

- **Example**: The exact match score of the set {Example 1, Example 2} (above) is 0.5.


## How to Use

```python
from datasets import load_metric
exact_match_metric = load_metric("exact_match")
results = exact_match_metric.compute(predictions=predictions, references=references)
```

### Inputs
- **predictions**: Predicted labels, as returned by a model.
- **references**: Ground truth labels.
- **regexes_to_ignore**: List, defaults to None. Regex expressions of characters to ignore when calculating the exact matches. Note: the regex changes are applied after capitalization is normalized.
- **ignore_capitalization**: Boolean, defaults to False. If true, turns everything to lowercase so that capitalization differences are ignored.

### Output Values
This metric outputs a dictionary with one value: the average exact match score.

```
{'exact_match': 100.0}
```

This metric's range is 0-100, inclusive. Here, 0.0 means no prediction/reference pairs were matches, while 100.0 means they all were.

#### Values from Popular Papers
The exact match metric is often included in other metrics, such as SQuAD. For example, the [original SQuAD paper](https://nlp.stanford.edu/pubs/rajpurkar2016squad.pdf) reported an Exact Match score of 40.0%. They also report that the human performance Exact Match score on the dataset was 80.3%.

### Examples
Without including any regexes to ignore:
```python
exact_match = datasets.load_metric("exact_match")
refs = ["the cat", "theater", "YELLING", "agent007"]
preds = ["cat?", "theater", "yelling", "agent"]
results = exact_match.compute(references=refs, predictions=preds)
round(results["exact_match"], 1)
25.0
```

Ignoring regexes "the" and "yell", as well as ignoring case and punctuation:
```python
exact_match = datasets.load_metric("exact_match")
refs = ["the cat", "theater", "YELLING", "agent007"]
preds = ["cat?", "theater", "yelling", "agent"]
results = exact_match.compute(references=refs, predictions=preds, regexes_to_ignore=["the ", "yell"], ignore_case=True, ignore_punctuation=True)
round(results["exact_match"], 1)
50.0
```
Note that in the example above, because the regexes are ignored before the case is normalized, "yell" from "YELLING" is not deleted.

Ignoring "the", "yell", and "YELL", as well as ignoring case and punctuation:
```python
exact_match = datasets.load_metric("exact_match")
refs = ["the cat", "theater", "YELLING", "agent007"]
preds = ["cat?", "theater", "yelling", "agent"]
results = exact_match.compute(references=refs, predictions=preds, regexes_to_ignore=["the ", "yell", "YELL"], ignore_case=True, ignore_punctuation=True)
round(results["exact_match"], 1)
75.0
```

Ignoring "the", "yell", and "YELL", as well as ignoring case, punctuation, and numbers:
```python
exact_match = datasets.load_metric("exact_match")
refs = ["the cat", "theater", "YELLING", "agent007"]
preds = ["cat?", "theater", "yelling", "agent"]
results = exact_match.compute(references=refs, predictions=preds, regexes_to_ignore=["the ", "yell", "YELL"], ignore_case=True, ignore_punctuation=True, ignore_numbers=True)
round(results["exact_match"], 1)
100.0
```



## Limitations and Bias
This metric is limited in that it outputs the same score for something that is completely wrong as for something that is correct except for a single character. In other words, there is no award for being *almost* right.

## Citation

## Further References
- Also used in the [SQuAD metric](https://github.com/huggingface/datasets/tree/master/metrics/squad) 
