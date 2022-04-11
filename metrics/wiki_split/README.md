# Metric Card for WikiSplit

## Metric description

WikiSplit is the combination of three metrics: [SARI](https://huggingface.co/metrics/sari), [exact match](https://huggingface.co/metrics/exact_match) and [SacreBLEU](https://huggingface.co/metrics/sacrebleu). 

It can be used to evaluate the quality of sentence splitting approaches, which require rewriting a long sentence into two or more coherent short sentences, e.g. based on the [WikiSplit dataset](https://huggingface.co/datasets/wiki_split).

## How to use 

The WIKI_SPLIT metric takes three inputs:

`sources`: a list of source sentences, where each sentence should be a string.

`predictions`: a list of predicted sentences, where each sentence should be a string.

`references`: a list of lists of reference sentences, where each sentence should be a string.

```python
>>> from datasets import load_metric
>>> wiki_split = load_metric("wiki_split")
>>> sources = ["About 95 species are currently accepted ."]
>>> predictions = ["About 95 you now get in ."]
>>> references= [["About 95 species are currently known ."]]
>>> results = wiki_split.compute(sources=sources, predictions=predictions, references=references)
```
## Output values

This metric outputs a dictionary containing three scores:

`sari`: the [SARI](https://huggingface.co/metrics/sari) score, whose range is between `0.0` and `100.0` -- the higher the value, the better the performance of the model being evaluated, with a SARI of 100 being a perfect score.

`sacrebleu`: the [SacreBLEU](https://huggingface.co/metrics/sacrebleu) score, which can take any value between `0.0` and `100.0`, inclusive.

`exact`: the [exact match](https://huggingface.co/metrics/exact_match) score, which represents the sum of all of the individual exact match scores in the set, divided by the total number of predictions in the set. It ranges from `0.0` to `100`, inclusive. Here, `0.0` means no prediction/reference pairs were matches, while `100.0` means they all were.

```python
>>> print(results)
{'sari': 21.805555555555557, 'sacrebleu': 14.535768424205482, 'exact': 0.0}
```

### Values from popular papers

This metric was initially used by [Rothe et al.(2020)](https://arxiv.org/pdf/1907.12461.pdf) to evaluate the performance of different split-and-rephrase approaches on the [WikiSplit dataset](https://huggingface.co/datasets/wiki_split). They reported a SARI score of 63.5, a SacreBLEU score of 77.2, and an EXACT_MATCH score of 16.3.

## Examples 

Perfect match between prediction and reference:

```python
>>> from datasets import load_metric
>>> wiki_split = load_metric("wiki_split")
>>> sources = ["About 95 species are currently accepted ."]
>>> predictions = ["About 95 species are currently accepted ."]
>>> references= [["About 95 species are currently accepted ."]]
>>> results = wiki_split.compute(sources=sources, predictions=predictions, references=references)
>>> print(results)
{'sari': 100.0, 'sacrebleu': 100.00000000000004, 'exact': 100.0
```

Partial match between prediction and reference:

```python
>>> from datasets import load_metric
>>> wiki_split = load_metric("wiki_split")
>>> sources = ["About 95 species are currently accepted ."]
>>> predictions = ["About 95 you now get in ."]
>>> references= [["About 95 species are currently known ."]]
>>> results = wiki_split.compute(sources=sources, predictions=predictions, references=references)
>>> print(results)
{'sari': 21.805555555555557, 'sacrebleu': 14.535768424205482, 'exact': 0.0}
```

No match between prediction and reference:

```python
>>> from datasets import load_metric
>>> wiki_split = load_metric("wiki_split")
>>> sources = ["About 95 species are currently accepted ."]
>>> predictions = ["Hello world ."]
>>> references= [["About 95 species are currently known ."]]
>>> results = wiki_split.compute(sources=sources, predictions=predictions, references=references)
>>> print(results)
{'sari': 14.047619047619046, 'sacrebleu': 0.0, 'exact': 0.0}
```
## Limitations and bias

This metric is not the official metric to evaluate models on the [WikiSplit dataset](https://huggingface.co/datasets/wiki_split). It was initially proposed by [Rothe et al.(2020)](https://arxiv.org/pdf/1907.12461.pdf), whereas the [original paper introducing the WikiSplit dataset (2018)](https://aclanthology.org/D18-1080.pdf) uses different metrics to evaluate performance, such as corpus-level [BLEU](https://huggingface.co/metrics/bleu) and sentence-level BLEU. 

## Citation

```bibtex
@article{rothe2020leveraging,
  title={Leveraging pre-trained checkpoints for sequence generation tasks},
  author={Rothe, Sascha and Narayan, Shashi and Severyn, Aliaksei},
  journal={Transactions of the Association for Computational Linguistics},
  volume={8},
  pages={264--280},
  year={2020},
  publisher={MIT Press}
}
```

## Further References 

- [WikiSplit dataset](https://huggingface.co/datasets/wiki_split)
- [WikiSplit paper (Botha et al., 2018)](https://aclanthology.org/D18-1080.pdf) 
