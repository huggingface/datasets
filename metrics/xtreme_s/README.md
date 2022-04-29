# Metric Card for XTREME-S


## Metric Description

The XTREME-S metric aims to evaluate model performance on the Cross-lingual TRansfer Evaluation of Multilingual Encoders for Speech (XTREME-S) benchmark.

This benchmark was designed to evaluate speech representations across languages, tasks, domains and data regimes. It covers 102 languages from 10+ language families, 3 different domains and 4 task families: speech recognition, translation, classification and retrieval.

## How to Use

There are two steps: (1) loading the XTREME-S metric relevant to the subset of the benchmark being used for evaluation; and (2) calculating the metric.

1. **Loading the relevant XTREME-S metric** : the subsets of XTREME-S are the following: `mls`, `voxpopuli`, `covost2`, `fleurs-asr`, `fleurs-lang_id`,  `minds14`  and `babel`. More information about the different subsets can be found on the [XTREME-S benchmark page](https://huggingface.co/datasets/google/xtreme_s).


```python
>>> from datasets import load_metric
>>> xtreme_s_metric = datasets.load_metric('xtreme_s', 'mls')
```

2. **Calculating the metric**: the metric takes two inputs : 

- `predictions`: a list of predictions to score, with each prediction a `str`. 

- `references`: a list of lists of references for each translation, with each reference a `str`. 

```python
>>> references = ["it is sunny here", "paper and pen are essentials"]
>>> predictions = ["it's sunny", "paper pen are essential"]
>>> results = xtreme_s_metric.compute(predictions=predictions, references=references)
```

It also has two optional arguments: 

- `bleu_kwargs`: a `dict` of keywords to be passed when computing the `bleu` metric for the `covost2` subset. Keywords can be one of `smooth_method`, `smooth_value`, `force`, `lowercase`, `tokenize`, `use_effective_order`.

- `wer_kwargs`: optional dict of keywords to be passed when computing `wer` and `cer`, which are computed for the `mls`, `fleurs-asr`, `voxpopuli`, and `babel` subsets. Keywords are `concatenate_texts`.

## Output values

The output of the metric depends on the XTREME-S subset chosen, consisting of a dictionary that contains one or several of the following metrics:

- `accuracy`: the proportion of correct predictions among the total number of cases processed, with a range between 0 and 1 (see [accuracy](https://huggingface.co/metrics/accuracy) for more information). This is returned for the `fleurs-lang_id` and `minds14` subsets.

- `f1`: the harmonic mean of the precision and recall (see [F1 score](https://huggingface.co/metrics/f1) for more information). Its range is 0-1 -- its lowest possible value is 0, if either the precision or the recall is 0, and its highest possible value is 1.0, which means perfect precision and recall. It is returned for the `minds14` subset.

- `wer`: Word error rate (WER) is a common metric of the performance of an automatic speech recognition system. The lower the value, the better the performance of the ASR system, with a WER of 0 being a perfect score (see [WER score](https://huggingface.co/metrics/wer) for more information). It is returned for the `mls`, `fleurs-asr`, `voxpopuli` and `babel` subsets of the benchmark.

- `cer`:  Character error rate (CER) is similar to WER, but operates on character instead of word. The lower the CER value, the better the performance of the ASR system, with a CER of 0 being a perfect score (see [CER score](https://huggingface.co/metrics/cer) for more information).  It is returned for the `mls`, `fleurs-asr`, `voxpopuli` and `babel` subsets of the benchmark.

- `bleu`: the BLEU score, calculated according to the SacreBLEU metric approach. It can take any value between 0.0 and 100.0, inclusive, with higher values being better (see [SacreBLEU](https://huggingface.co/metrics/sacrebleu) for more details).  This is returned for the `covost2` subset.


### Values from popular papers
The [original XTREME-S paper](https://arxiv.org/pdf/2203.10752.pdf) reported average WERs ranging from 9.2 to 14.6, a BLEU score of 20.6, an accuracy of 73.3 and F1 score of 86.9, depending on the subsets of the dataset tested on. 

## Examples 

For the `mls` subset (which outputs `wer` and `cer`):

```python
>>> from datasets import load_metric
>>> xtreme_s_metric = datasets.load_metric('xtreme_s', 'mls')  
>>> references = ["it is sunny here", "paper and pen are essentials"]
>>> predictions = ["it's sunny", "paper pen are essential"]
>>> results = xtreme_s_metric.compute(predictions=predictions, references=references)
>>> print({k: round(v, 2) for k, v in results.items()})
{'wer': 0.56, 'cer': 0.27}
```

For the `covost2` subset (which outputs `bleu`):

```python
>>> from datasets import load_metric
>>> xtreme_s_metric = datasets.load_metric('xtreme_s', 'covost2')
>>> references = ["bonjour paris", "il est necessaire de faire du sport de temps en temp"]
>>> predictions = ["bonjour paris", "il est important de faire du sport souvent"]
>>> results = xtreme_s_metric.compute(predictions=predictions, references=references)
>>> print({k: round(v, 2) for k, v in results.items()})
{'bleu': 31.65}
```

For the `fleurs-lang_id` subset (which outputs `accuracy`):

```python
>>> from datasets import load_metric
>>> xtreme_s_metric = datasets.load_metric('xtreme_s', 'fleurs-lang_id')
>>> references = [0, 1, 0, 0, 1]
>>> predictions = [0, 1, 1, 0, 0]
>>> results = xtreme_s_metric.compute(predictions=predictions, references=references)
>>> print({k: round(v, 2) for k, v in results.items()})
{'accuracy': 0.6}
 ```
 
For the `minds14` subset (which outputs `f1` and `accuracy`):

```python
>>> from datasets import load_metric
>>> xtreme_s_metric = datasets.load_metric('xtreme_s', 'minds14')
>>> references = [0, 1, 0, 0, 1]
>>> predictions = [0, 1, 1, 0, 0]
>>> results = xtreme_s_metric.compute(predictions=predictions, references=references)
>>> print({k: round(v, 2) for k, v in results.items()})
{'f1': 0.58, 'accuracy': 0.6}
```

## Limitations and bias
This metric works only with datasets that have the same format as the [XTREME-S dataset](https://huggingface.co/datasets/google/xtreme_s).

While the XTREME-S dataset is meant to represent a variety of languages and tasks, it has inherent biases: it is missing many languages that are important and under-represented in NLP datasets. 

It also has a particular focus on read-speech because common evaluation benchmarks like CoVoST-2 or LibriSpeech evaluate on this type of speech, which results in a mismatch between performance obtained in a read-speech setting and a more noisy setting (in production or live deployment, for instance). 

## Citation

```bibtex
@article{conneau2022xtreme,
  title={XTREME-S: Evaluating Cross-lingual Speech Representations},
  author={Conneau, Alexis and Bapna, Ankur and Zhang, Yu and Ma, Min and von Platen, Patrick and Lozhkov, Anton and Cherry, Colin and Jia, Ye and Rivera, Clara and Kale, Mihir and others},
  journal={arXiv preprint arXiv:2203.10752},
  year={2022}
}
```
    
## Further References 

- [XTREME-S dataset](https://huggingface.co/datasets/google/xtreme_s)
- [XTREME-S github repository](https://github.com/google-research/xtreme)
