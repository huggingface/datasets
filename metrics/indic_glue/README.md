# Metric Card for IndicGLUE

## Metric description
This metric is used to compute the evaluation metric for the [IndicGLUE dataset](https://huggingface.co/datasets/indic_glue). 

IndicGLUE is a natural language understanding benchmark for Indian languages. It contains a wide variety of tasks and covers 11 major Indian languages - Assamese (`as`), Bengali (`bn`), Gujarati (`gu`), Hindi (`hi`), Kannada (`kn`), Malayalam (`ml`), Marathi(`mr`), Oriya(`or`), Panjabi (`pa`), Tamil(`ta`) and Telugu (`te`).

## How to use 

There are two steps: (1) loading the IndicGLUE metric relevant to the subset of the dataset being used for evaluation; and (2) calculating the metric.

1. **Loading the relevant IndicGLUE metric** : the subsets of IndicGLUE are the following: `wnli`, `copa`, `sna`, `csqa`, `wstp`, `inltkh`, `bbca`, `cvit-mkb-clsr`, `iitp-mr`, `iitp-pr`, `actsa-sc`, `md`, and`wiki-ner`.

More information about the different subsets of the Indic GLUE dataset can be found on the [IndicGLUE dataset page](https://indicnlp.ai4bharat.org/indic-glue/).

2. **Calculating the metric**: the metric takes two inputs : one list with the predictions of the model to score and one lists of references for each translation for all subsets of the dataset except for `cvit-mkb-clsr`, where each prediction and reference is a vector of floats.

```python
from datasets import load_metric
indic_glue_metric = load_metric('indic_glue', 'wnli')  
references = [0, 1]
predictions = [0, 1]
results = indic_glue_metric.compute(predictions=predictions, references=references)
```
    
## Output values

The output of the metric depends on the IndicGLUE subset chosen, consisting of a dictionary that contains one or several of the following metrics:

`accuracy`: the proportion of correct predictions among the total number of cases processed, with a range between 0 and 1 (see [accuracy](https://huggingface.co/metrics/accuracy) for more information). 

`f1`: the harmonic mean of the precision and recall (see [F1 score](https://huggingface.co/metrics/f1) for more information). Its range is 0-1 -- its lowest possible value is 0, if either the precision or the recall is 0, and its highest possible value is 1.0, which means perfect precision and recall.

`precision@10`: the fraction of the true examples among the top 10 predicted examples, with a range between 0 and 1 (see [precision](https://huggingface.co/metrics/precision) for more information). 

The `cvit-mkb-clsr` subset returns `precision@10`, the `wiki-ner` subset returns `accuracy` and `f1`, and all other subsets of Indic GLUE return only accuracy. 

### Values from popular papers

The [original IndicGlue paper](https://aclanthology.org/2020.findings-emnlp.445.pdf) reported an average accuracy of 0.766 on the dataset, which varies depending on the subset selected.

## Examples 

Maximal values for the WNLI subset (which outputs `accuracy`):

```python
from datasets import load_metric
indic_glue_metric = load_metric('indic_glue', 'wnli') 
references = [0, 1]
predictions = [0, 1]
results = indic_glue_metric.compute(predictions=predictions, references=references)
print(results)
{'accuracy': 1.0}
```

Minimal values for the Wiki-NER subset (which outputs `accuracy` and `f1`):

```python
>>> from datasets import load_metric
>>> indic_glue_metric = load_metric('indic_glue', 'wiki-ner')
>>> references = [0, 1]
>>> predictions = [1,0]
>>> results = indic_glue_metric.compute(predictions=predictions, references=references)
>>> print(results)
{'accuracy': 1.0, 'f1': 1.0}
```

Partial match for the CVIT-Mann Ki Baat subset (which outputs `precision@10`) 

```python
>>> from datasets import load_metric
>>> indic_glue_metric = load_metric('indic_glue', 'cvit-mkb-clsr')
>>> references = [[0.5, 0.5, 0.5], [0.1, 0.2, 0.3]]
>>> predictions = [[0.5, 0.5, 0.5], [0.1, 0.2, 0.3]]
>>> results = indic_glue_metric.compute(predictions=predictions, references=references)
>>> print(results)
{'precision@10': 1.0}
```

## Limitations and bias
This metric works only with datasets that have the same format as the [IndicGLUE dataset](https://huggingface.co/datasets/glue).

## Citation

```bibtex
    @inproceedings{kakwani2020indicnlpsuite,
    title={{IndicNLPSuite: Monolingual Corpora, Evaluation Benchmarks and Pre-trained Multilingual Language Models for Indian Languages}},
    author={Divyanshu Kakwani and Anoop Kunchukuttan and Satish Golla and Gokul N.C. and Avik Bhattacharyya and Mitesh M. Khapra and Pratyush Kumar},
    year={2020},
    booktitle={Findings of EMNLP},
}
```
    
## Further References 
- [IndicNLP website](https://indicnlp.ai4bharat.org/home/)
- 
