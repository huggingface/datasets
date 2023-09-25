# Metric Card for SQuAD v2

## Metric description
This metric wraps the official scoring script for version 2 of the [Stanford Question Answering Dataset (SQuAD)](https://huggingface.co/datasets/squad_v2).

SQuAD is a reading comprehension dataset, consisting of questions posed by crowdworkers on a set of Wikipedia articles, where the answer to every question is a segment of text, or span, from the corresponding reading passage, or the question might be unanswerable.

SQuAD 2.0 combines the 100,000 questions in SQuAD 1.1 with over 50,000 unanswerable questions written adversarially by crowdworkers to look similar to answerable ones. To do well on SQuAD2.0, systems must not only answer questions when possible, but also determine when no answer is supported by the paragraph and abstain from answering.

## How to use 

The metric takes two files or two lists - one representing model predictions and the other the references to compare them to. 

*Predictions* : List of triple for question-answers to score with the following key-value pairs:
* `'id'`:  the question-answer identification field of the question and answer pair 
* `'prediction_text'` : the text of the answer
* `'no_answer_probability'` : the probability that the question has no answer

*References*: List of question-answers dictionaries with the following key-value pairs:
* `'id'`: id of the question-answer pair (see above),
* `'answers'`: a list of Dict {'text': text of the answer as a string}
*  `'no_answer_threshold'`: the probability threshold to decide that a question has no answer.

```python
from datasets import load_metric
squad_metric = load_metric("squad_v2")
results = squad_metric.compute(predictions=predictions, references=references)
```
## Output values

This metric outputs a dictionary with 13 values: 
* `'exact'`: Exact match (the normalized answer exactly match the gold answer) (see the `exact_match` metric (forthcoming))
* `'f1'`: The average F1-score of predicted tokens versus the gold answer (see the [F1 score](https://huggingface.co/metrics/f1) metric)
* `'total'`: Number of scores considered
* `'HasAns_exact'`: Exact match (the normalized answer exactly match the gold answer)
* `'HasAns_f1'`:  The F-score of predicted tokens versus the gold answer
* `'HasAns_total'`: How many of the questions have answers
* `'NoAns_exact'`: Exact match (the normalized answer exactly match the gold answer)
* `'NoAns_f1'`: The F-score of predicted tokens versus the gold answer
* `'NoAns_total'`: How many of the questions have no answers
* `'best_exact'` : Best exact match (with varying threshold)
* `'best_exact_thresh'`: No-answer probability threshold associated to the best exact match
* `'best_f1'`: Best F1 score (with varying threshold)
* `'best_f1_thresh'`: No-answer probability threshold associated to the best F1


The range of `exact_match` is 0-100, where 0.0 means no answers were matched and 100.0 means all answers were matched. 

The range of `f1` is 0-1 -- its lowest possible value is 0, if either the precision or the recall is 0, and its highest possible value is 1.0, which means perfect precision and recall.

The range of `total` depends on the length of predictions/references: its minimal value is 0, and maximal value is the total number of questions in the predictions and references.

### Values from popular papers
The [SQuAD v2 paper](https://arxiv.org/pdf/1806.03822.pdf) reported an F1 score of 66.3% and an Exact Match score of 63.4%. 
They also report that human performance on the dataset represents an F1 score of 89.5% and an Exact Match score of 86.9%.

For more recent model performance, see the [dataset leaderboard](https://paperswithcode.com/dataset/squad).

## Examples 

Maximal values for both exact match and F1 (perfect match):

```python
from datasets import load_metric
squad_v2_ metric = load_metric("squad_v2")
predictions = [{'prediction_text': '1976', 'id': '56e10a3be3433e1400422b22', 'no_answer_probability': 0.}]
references = [{'answers': {'answer_start': [97], 'text': ['1976']}, 'id': '56e10a3be3433e1400422b22'}]
results = squad_v2_metric.compute(predictions=predictions, references=references)
results
{'exact': 100.0, 'f1': 100.0, 'total': 1, 'HasAns_exact': 100.0, 'HasAns_f1': 100.0, 'HasAns_total': 1, 'best_exact': 100.0, 'best_exact_thresh': 0.0, 'best_f1': 100.0, 'best_f1_thresh': 0.0}
```

Minimal values for both exact match and F1 (no match):

```python
from datasets import load_metric
squad_metric = load_metric("squad_v2")
predictions = [{'prediction_text': '1999', 'id': '56e10a3be3433e1400422b22', 'no_answer_probability': 0.}]
references = [{'answers': {'answer_start': [97], 'text': ['1976']}, 'id': '56e10a3be3433e1400422b22'}]
results = squad_v2_metric.compute(predictions=predictions, references=references)
results
{'exact': 0.0, 'f1': 0.0, 'total': 1, 'HasAns_exact': 0.0, 'HasAns_f1': 0.0, 'HasAns_total': 1, 'best_exact': 0.0, 'best_exact_thresh': 0.0, 'best_f1': 0.0, 'best_f1_thresh': 0.0}
```

Partial match (2 out of 3 answers correct) : 

```python
from datasets import load_metric
squad_metric = load_metric("squad_v2")
predictions = [{'prediction_text': '1976', 'id': '56e10a3be3433e1400422b22', 'no_answer_probability': 0.}, {'prediction_text': 'Beyonce', 'id': '56d2051ce7d4791d0090260b', 'no_answer_probability': 0.},  {'prediction_text': 'climate change', 'id': '5733b5344776f419006610e1', 'no_answer_probability': 0.}]
references = [{'answers': {'answer_start': [97], 'text': ['1976']}, 'id': '56e10a3be3433e1400422b22'}, {'answers': {'answer_start': [233], 'text': ['Beyoncé and Bruno Mars']}, 'id': '56d2051ce7d4791d0090260b'}, {'answers': {'answer_start': [891], 'text': ['climate change']}, 'id': '5733b5344776f419006610e1'}]
results = squad_v2_metric.compute(predictions=predictions, references=references)
results
{'exact': 66.66666666666667, 'f1': 66.66666666666667, 'total': 3, 'HasAns_exact': 66.66666666666667, 'HasAns_f1': 66.66666666666667, 'HasAns_total': 3, 'best_exact': 66.66666666666667, 'best_exact_thresh': 0.0, 'best_f1': 66.66666666666667, 'best_f1_thresh': 0.0}
```

## Limitations and bias
This metric works only with the datasets in the same format as the [SQuAD v.2 dataset](https://huggingface.co/datasets/squad_v2).

The SQuAD datasets do contain a certain amount of noise, such as duplicate questions as well as missing answers, but these represent a minority of the 100,000 question-answer pairs. Also, neither exact match nor F1 score reflect whether models do better on certain types of questions (e.g. who questions) or those that cover a certain gender or geographical area -- carrying out more in-depth error analysis can complement these numbers. 


## Citation

```bibtex
@inproceedings{Rajpurkar2018SQuAD2,
title={Know What You Don't Know: Unanswerable Questions for SQuAD},
author={Pranav Rajpurkar and Jian Zhang and Percy Liang},
booktitle={ACL 2018},
year={2018}
}
```
    
## Further References 

- [The Stanford Question Answering Dataset: Background, Challenges, Progress (blog post)](https://rajpurkar.github.io/mlx/qa-and-squad/)
- [Hugging Face Course -- Question Answering](https://huggingface.co/course/chapter7/7)
