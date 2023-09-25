# Metric Card for SQuAD

## Metric description
This metric wraps the official scoring script for version 1 of the [Stanford Question Answering Dataset (SQuAD)](https://huggingface.co/datasets/squad). 

SQuAD is a reading comprehension dataset, consisting of questions posed by crowdworkers on a set of Wikipedia articles, where the answer to every question is a segment of text, or span, from the corresponding reading passage, or the question might be unanswerable.

## How to use 

The metric takes two files or two lists of question-answers dictionaries as inputs : one with the predictions of the model and the other with the references to be compared to:

```python
from datasets import load_metric
squad_metric = load_metric("squad")
results = squad_metric.compute(predictions=predictions, references=references)
```
## Output values

This metric outputs a dictionary with two values: the average exact match score and the average [F1 score](https://huggingface.co/metrics/f1).

```
{'exact_match': 100.0, 'f1': 100.0}
```

The range of `exact_match` is 0-100, where 0.0 means no answers were matched and 100.0 means all answers were matched. 

The range of `f1` is 0-1 -- its lowest possible value is 0, if either the precision or the recall is 0, and its highest possible value is 1.0, which means perfect precision and recall.

### Values from popular papers
The [original SQuAD paper](https://nlp.stanford.edu/pubs/rajpurkar2016squad.pdf) reported an F1 score of 51.0% and an Exact Match score of 40.0%. They also report that human performance on the dataset represents an F1 score of 90.5% and an Exact Match score of 80.3%.

For more recent model performance, see the [dataset leaderboard](https://paperswithcode.com/dataset/squad).

## Examples 

Maximal values for both exact match and F1 (perfect match):

```python
from datasets import load_metric
squad_metric = load_metric("squad")
predictions = [{'prediction_text': '1976', 'id': '56e10a3be3433e1400422b22'}]
references = [{'answers': {'answer_start': [97], 'text': ['1976']}, 'id': '56e10a3be3433e1400422b22'}]
results = squad_metric.compute(predictions=predictions, references=references)
results
{'exact_match': 100.0, 'f1': 100.0}
```

Minimal values for both exact match and F1 (no match):

```python
from datasets import load_metric
squad_metric = load_metric("squad")
predictions = [{'prediction_text': '1999', 'id': '56e10a3be3433e1400422b22'}]
references = [{'answers': {'answer_start': [97], 'text': ['1976']}, 'id': '56e10a3be3433e1400422b22'}]
results = squad_metric.compute(predictions=predictions, references=references)
results
{'exact_match': 0.0, 'f1': 0.0}
```

Partial match (2 out of 3 answers correct) : 

```python
from datasets import load_metric
squad_metric = load_metric("squad")
predictions = [{'prediction_text': '1976', 'id': '56e10a3be3433e1400422b22'}, {'prediction_text': 'Beyonce', 'id': '56d2051ce7d4791d0090260b'},  {'prediction_text': 'climate change', 'id': '5733b5344776f419006610e1'}]
references = [{'answers': {'answer_start': [97], 'text': ['1976']}, 'id': '56e10a3be3433e1400422b22'}, {'answers': {'answer_start': [233], 'text': ['Beyoncé and Bruno Mars']}, 'id': '56d2051ce7d4791d0090260b'}, {'answers': {'answer_start': [891], 'text': ['climate change']}, 'id': '5733b5344776f419006610e1'}]
results = squad_metric.compute(predictions=predictions, references=references)
results
{'exact_match': 66.66666666666667, 'f1': 66.66666666666667}
```

## Limitations and bias
This metric works only with datasets that have the same format as [SQuAD v.1 dataset](https://huggingface.co/datasets/squad).

The SQuAD dataset does contain a certain amount of noise, such as duplicate questions as well as missing answers, but these represent a minority of the 100,000 question-answer pairs. Also, neither exact match nor F1 score reflect whether models do better on certain types of questions (e.g. who questions) or those that cover a certain gender or geographical area -- carrying out more in-depth error analysis can complement these numbers. 


## Citation

    @inproceedings{Rajpurkar2016SQuAD10,
    title={SQuAD: 100, 000+ Questions for Machine Comprehension of Text},
    author={Pranav Rajpurkar and Jian Zhang and Konstantin Lopyrev and Percy Liang},
    booktitle={EMNLP},
    year={2016}
    }
    
## Further References 

- [The Stanford Question Answering Dataset: Background, Challenges, Progress (blog post)](https://rajpurkar.github.io/mlx/qa-and-squad/)
- [Hugging Face Course -- Question Answering](https://huggingface.co/course/chapter7/7)
