# Metric Card for SuperGLUE

## Metric description
This metric is used to compute the SuperGLUE evaluation metric associated to each of the subsets of the [SuperGLUE dataset](https://huggingface.co/datasets/super_glue). 

SuperGLUE is a new benchmark styled after GLUE with a new set of more difficult language understanding tasks, improved resources, and a new public leaderboard.


## How to use 

There are two steps: (1) loading the SuperGLUE metric relevant to the subset of the dataset being used for evaluation; and (2) calculating the metric.

1. **Loading the relevant SuperGLUE metric** : the subsets of SuperGLUE are the following: `boolq`, `cb`, `copa`, `multirc`, `record`, `rte`, `wic`, `wsc`, `wsc.fixed`, `axb`, `axg`.

More information about the different subsets of the SuperGLUE dataset can be found on the [SuperGLUE dataset page](https://huggingface.co/datasets/super_glue) and on the [official dataset website](https://super.gluebenchmark.com/).

2. **Calculating the metric**: the metric takes two inputs : one list with the predictions of the model to score and one list of reference labels. The structure of both inputs depends on the SuperGlUE subset being used:

Format of `predictions`:
- for `record`: list of question-answer dictionaries with the following keys:
    - `idx`: index of the question as specified by the dataset
    - `prediction_text`: the predicted answer text
- for `multirc`: list of question-answer dictionaries with the following keys:
    - `idx`: index of the question-answer pair as specified by the dataset
    - `prediction`: the predicted answer label
- otherwise: list of predicted labels

Format of `references`:
- for `record`: list of question-answers dictionaries with the following keys:
    - `idx`: index of the question as specified by the dataset
    - `answers`: list of possible answers
- otherwise: list of reference labels

```python
from datasets import load_metric
super_glue_metric = load_metric('super_glue', 'copa') 
predictions = [0, 1]
references = [0, 1]
results = super_glue_metric.compute(predictions=predictions, references=references)
```
## Output values

The output of the metric depends on the SuperGLUE subset chosen, consisting of a dictionary that contains one or several of the following metrics:

`exact_match`: A given predicted string's exact match score is 1 if it is the exact same as its reference string, and is 0 otherwise. (See [Exact Match](https://huggingface.co/metrics/exact_match) for more information).

`f1`: the harmonic mean of the precision and recall (see [F1 score](https://huggingface.co/metrics/f1) for more information). Its range is 0-1 -- its lowest possible value is 0, if either the precision or the recall is 0, and its highest possible value is 1.0, which means perfect precision and recall.

`matthews_correlation`: a measure of the quality of binary and multiclass classifications (see [Matthews Correlation](https://huggingface.co/metrics/matthews_correlation) for more information). Its range of values is between -1 and +1, where a coefficient of +1 represents a perfect prediction, 0 an average random prediction and -1 an inverse prediction.

### Values from popular papers
The [original SuperGLUE paper](https://arxiv.org/pdf/1905.00537.pdf) reported average scores ranging from 47 to 71.5%, depending on the model used (with all evaluation values scaled by 100 to make computing the average possible). 

For more recent model performance, see the [dataset leaderboard](https://super.gluebenchmark.com/leaderboard).

## Examples 

Maximal values for the COPA subset (which outputs `accuracy`):

```python
from datasets import load_metric
super_glue_metric = load_metric('super_glue', 'copa')  # any of ["copa", "rte", "wic", "wsc", "wsc.fixed", "boolq", "axg"]
predictions = [0, 1]
references = [0, 1]
results = super_glue_metric.compute(predictions=predictions, references=references)
print(results)
{'accuracy': 1.0}
```

Minimal values for the MultiRC subset (which outputs `pearson` and `spearmanr`):

```python
from datasets import load_metric
super_glue_metric = load_metric('super_glue', 'multirc')
predictions = [{'idx': {'answer': 0, 'paragraph': 0, 'question': 0}, 'prediction': 0}, {'idx': {'answer': 1, 'paragraph': 2, 'question': 3}, 'prediction': 1}]
references = [1,0]
results = super_glue_metric.compute(predictions=predictions, references=references)
print(results)
{'exact_match': 0.0, 'f1_m': 0.0, 'f1_a': 0.0}
```

Partial match for the COLA subset (which outputs `matthews_correlation`) 

```python
from datasets import load_metric
super_glue_metric = load_metric('super_glue', 'axb')
references = [0, 1]
predictions = [1,1]
results = super_glue_metric.compute(predictions=predictions, references=references)
print(results)
{'matthews_correlation': 0.0}
```

## Limitations and bias
This metric works only with datasets that have the same format as the [SuperGLUE dataset](https://huggingface.co/datasets/super_glue).

The dataset also includes Winogender, a subset of the dataset that is designed to measure gender bias in coreference resolution systems. However, as noted in the SuperGLUE paper, this subset has its limitations: *"It offers only positive predictive value: A poor bias score is clear evidence that a model exhibits gender bias, but a good score does not mean that the model is unbiased.[...] Also, Winogender does not cover all forms of social bias, or even all forms of gender. For instance, the version of the data used here offers no coverage of gender-neutral they or non-binary pronouns."

## Citation

```bibtex
@article{wang2019superglue,
  title={Super{GLUE}: A Stickier Benchmark for General-Purpose Language Understanding Systems},
  author={Wang, Alex and Pruksachatkun, Yada and Nangia, Nikita and Singh, Amanpreet and Michael, Julian and Hill, Felix and Levy, Omer and Bowman, Samuel R},
  journal={arXiv preprint arXiv:1905.00537},
  year={2019}
}
```
    
## Further References 

- [SuperGLUE benchmark homepage](https://super.gluebenchmark.com/)
