# Metric Card for GLUE

## Metric description
This metric is used to compute the GLUE evaluation metric associated to each [GLUE dataset](https://huggingface.co/datasets/glue). 

GLUE, the General Language Understanding Evaluation benchmark is a collection of resources for training, evaluating, and analyzing natural language understanding systems.

## How to use 

There are two steps: (1) loading the GLUE metric relevant to the subset of the GLUE dataset being used for evaluation; and (2) calculating the metric.

1. **Loading the relevant GLUE metric** : the subsets of GLUE are the following: `sst2`,  `mnli`, `mnli_mismatched`, `mnli_matched`, `qnli`, `rte`, `wnli`, `cola`,`stsb`, `mrpc`, `qqp`, and `hans`.

More information about the different subsets of the GLUE dataset can be found on the [GLUE dataset page](https://huggingface.co/datasets/glue).

2. **Calculating the metric**: the metric takes two inputs : one list with the predictions of the model to score and one lists of references for each translation.

```python
from datasets import load_metric
glue_metric = load_metric('glue', 'sst2')
references = [0, 1]
predictions = [0, 1]
results = glue_metric.compute(predictions=predictions, references=references)
```
## Output values

The output of the metric depends on the GLUE subset chosen, consisting of a dictionary that contains one or several of the following metrics:

`accuracy`: the proportion of correct predictions among the total number of cases processed, with a range between 0 and 1 (see [accuracy](https://huggingface.co/metrics/accuracy) for more information). 

`f1`: the harmonic mean of the precision and recall (see [F1 score](https://huggingface.co/metrics/f1) for more information). Its range is 0-1 -- its lowest possible value is 0, if either the precision or the recall is 0, and its highest possible value is 1.0, which means perfect precision and recall.

`pearson`: a measure of the linear relationship between two datasets (see [Pearson correlation](https://huggingface.co/metrics/pearsonr) for more information). Its range is between -1 and +1, with 0 implying no correlation, and -1/+1 implying an exact linear relationship. Positive correlations imply that as x increases, so does y, whereas negative correlations imply that as x increases, y decreases. 

`spearmanr`:  a nonparametric measure of the monotonicity of the relationship between two datasets(see [Spearman Correlation](https://huggingface.co/metrics/spearmanr) for more information). `spearmanr` has the same range as `pearson`.

`matthews_correlation`: a measure of the quality of binary and multiclass classifications (see [Matthews Correlation](https://huggingface.co/metrics/matthews_correlation) for more information). Its range of values is between -1 and +1, where a coefficient of +1 represents a perfect prediction, 0 an average random prediction and -1 an inverse prediction.

The `cola` subset returns `matthews_correlation`, the `stsb` subset returns `pearson` and `spearmanr`, the `mrpc` and `qqp` subsets return both `accuracy` and `f1`, and all other subsets of GLUE return only accuracy. 

### Values from popular papers
The [original GLUE paper](https://huggingface.co/datasets/glue) reported average scores ranging from 58 to 64%, depending on the model used (with all evaluation values scaled by 100 to make computing the average possible).

For more recent model performance, see the [dataset leaderboard](https://paperswithcode.com/dataset/glue).

## Examples 

Maximal values for the MRPC subset (which outputs `accuracy` and `f1`):

```python
from datasets import load_metric
glue_metric = load_metric('glue', 'mrpc')  # 'mrpc' or 'qqp'
references = [0, 1]
predictions = [0, 1]
results = glue_metric.compute(predictions=predictions, references=references)
print(results)
{'accuracy': 1.0, 'f1': 1.0}
```

Minimal values for the STSB subset (which outputs `pearson` and `spearmanr`):

```python
from datasets import load_metric
glue_metric = load_metric('glue', 'stsb')
references = [0., 1., 2., 3., 4., 5.]
predictions = [-10., -11., -12., -13., -14., -15.]
results = glue_metric.compute(predictions=predictions, references=references)
print(results)
{'pearson': -1.0, 'spearmanr': -1.0}
```

Partial match for the COLA subset (which outputs `matthews_correlation`) 

```python
from datasets import load_metric
glue_metric = load_metric('glue', 'cola')
references = [0, 1]
predictions = [1, 1]
results = glue_metric.compute(predictions=predictions, references=references)
results
{'matthews_correlation': 0.0}
```

## Limitations and bias
This metric works only with datasets that have the same format as the [GLUE dataset](https://huggingface.co/datasets/glue).

While the GLUE dataset is meant to represent "General Language Understanding", the tasks represented in it are not necessarily representative of language understanding, and should not be interpreted as such. 

Also, while the GLUE subtasks were considered challenging during its creation in 2019, they are no longer considered as such given the impressive progress made since then. A more complex (or "stickier") version of it, called [SuperGLUE](https://huggingface.co/datasets/super_glue), was subsequently created.

## Citation

```bibtex
 @inproceedings{wang2019glue,
  title={{GLUE}: A Multi-Task Benchmark and Analysis Platform for Natural Language Understanding},
  author={Wang, Alex and Singh, Amanpreet and Michael, Julian and Hill, Felix and Levy, Omer and Bowman, Samuel R.},
  note={In the Proceedings of ICLR.},
  year={2019}
}
```
    
## Further References 

- [GLUE benchmark homepage](https://gluebenchmark.com/)
- [Fine-tuning a model with the Trainer API](https://huggingface.co/course/chapter3/3?)
