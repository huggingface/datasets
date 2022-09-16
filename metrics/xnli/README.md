# Metric Card for XNLI

## Metric description

The XNLI metric allows to evaluate a model's score on the [XNLI dataset](https://huggingface.co/datasets/xnli), which is a subset of a few thousand examples from the [MNLI dataset](https://huggingface.co/datasets/glue/viewer/mnli) that have been translated into a 14 different languages, some of which are relatively low resource such as Swahili and Urdu.

As with MNLI, the task is to predict textual entailment (does sentence A imply/contradict/neither sentence B) and is a classification task (given two sentences, predict one of three labels).

## How to use 

The XNLI metric is computed based on the `predictions` (a list of predicted labels) and the `references` (a list of ground truth labels).

```python
from datasets import load_metric
xnli_metric = load_metric("xnli")
predictions = [0, 1]
references = [0, 1]
results = xnli_metric.compute(predictions=predictions, references=references)
```

## Output values

The output of the XNLI metric is simply the `accuracy`, i.e. the proportion of correct predictions among the total number of cases processed, with a range between 0 and 1 (see [accuracy](https://huggingface.co/metrics/accuracy) for more information). 

### Values from popular papers
The [original XNLI paper](https://arxiv.org/pdf/1809.05053.pdf) reported accuracies ranging from 59.3 (for `ur`) to 73.7 (for `en`) for the BiLSTM-max model.

For more recent model performance, see the [dataset leaderboard](https://paperswithcode.com/dataset/xnli).

## Examples 

Maximal values:

```python
>>> from datasets import load_metric
>>> xnli_metric = load_metric("xnli")
>>> predictions = [0, 1]
>>> references = [0, 1]
>>> results = xnli_metric.compute(predictions=predictions, references=references)
>>> print(results)
{'accuracy': 1.0}
```

Minimal values:

```python
>>> from datasets import load_metric
>>> xnli_metric = load_metric("xnli")
>>> predictions = [1, 0]
>>> references = [0, 1]
>>> results = xnli_metric.compute(predictions=predictions, references=references)
>>> print(results)
{'accuracy': 0.0}
```

Partial match:

```python
>>> from datasets import load_metric
>>> xnli_metric = load_metric("xnli")
>>> predictions = [1, 0, 1]
>>> references = [1, 0, 0]
>>> results = xnli_metric.compute(predictions=predictions, references=references)
>>> print(results)
{'accuracy': 0.6666666666666666}
```

## Limitations and bias

While accuracy alone does give a certain indication of performance, it can be supplemented by error analysis and a better understanding of the model's mistakes on each of the categories represented in the dataset, especially if they are unbalanced. 

While the XNLI dataset is multilingual and represents a diversity of languages, in reality, cross-lingual sentence understanding goes beyond translation, given that there are many cultural differences that have an impact on human sentiment annotations. Since the XNLI dataset was obtained by translation based on English sentences, it does not capture these cultural differences. 



## Citation

```bibtex
@InProceedings{conneau2018xnli,
  author = "Conneau, Alexis
                 and Rinott, Ruty
                 and Lample, Guillaume
                 and Williams, Adina
                 and Bowman, Samuel R.
                 and Schwenk, Holger
                 and Stoyanov, Veselin",
  title = "XNLI: Evaluating Cross-lingual Sentence Representations",
  booktitle = "Proceedings of the 2018 Conference on Empirical Methods
               in Natural Language Processing",
  year = "2018",
  publisher = "Association for Computational Linguistics",
  location = "Brussels, Belgium",
}
```
    
## Further References 

- [XNI Dataset GitHub](https://github.com/facebookresearch/XNLI)
- [HuggingFace Tasks -- Text Classification](https://huggingface.co/tasks/text-classification)
