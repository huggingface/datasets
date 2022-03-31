# Metric Card for METEOR

## Metric description

METEOR (Metric for Evaluation of Translation with Explicit ORdering) is a machine translation evaluation metric, which is calculated based on the harmonic mean of precision and recall, with recall weighted more than precision. 

METEOR is based on a generalized concept of unigram matching between the machine-produced translation and human-produced reference translations. Unigrams can be matched based on their surface forms, stemmed forms, and meanings. Once all generalized unigram matches between the two strings have been found, METEOR computes a score for this matching using a combination of unigram-precision, unigram-recall, and a measure of fragmentation that is designed to directly capture how well-ordered the matched words in the machine translation are in relation to the reference. 


## How to use 

METEOR has two mandatory arguments:

`predictions`: a list of predictions to score. Each prediction should be a string with tokens separated by spaces.

`references`: a list of references for each prediction. Each reference should be a string with tokens separated by spaces.

It also has several optional parameters:

`alpha`: Parameter for controlling relative weights of precision and recall. The default value is `0.9`.

`beta`: Parameter for controlling shape of penalty as a function of fragmentation. The default value is `3`.

`gamma`: The relative weight assigned to fragmentation penalty. The default is `0.5`. 

Refer to the [METEOR paper](https://aclanthology.org/W05-0909.pdf) for more information about parameter values and ranges.

```python
>>> from datasets import load_metric
>>> meteor = load_metric('meteor')
>>> predictions = ["It is a guide to action which ensures that the military always obeys the commands of the party"]
>>> references = ["It is a guide to action that ensures that the military will forever heed Party commands"]
>>> results = meteor.compute(predictions=predictions, references=references)
```

## Output values

The metric outputs a dictionary containing the METEOR score. Its values range from 0 to 1. 


### Values from popular papers
The [METEOR paper](https://aclanthology.org/W05-0909.pdf) does not report METEOR score values for different models, but it does report that METEOR gets an R correlation value of 0.347 with human evaluation on the Arabic data and 0.331 on the Chinese data. 


## Examples 

Maximal values :

```python
>>> from datasets import load_metric
>>> meteor = load_metric('meteor')
>>> predictions = ["It is a guide to action which ensures that the military always obeys the commands of the party"]
>>> references = ["It is a guide to action which ensures that the military always obeys the commands of the party"]
>>> results = meteor.compute(predictions=predictions, references=references)
>>> print(round(results['meteor'], 2))
1.0
```

Minimal values:

```python
>>> from datasets import load_metric
>>> meteor = load_metric('meteor')
>>> predictions = ["It is a guide to action which ensures that the military always obeys the commands of the party"]
>>> references = ["Hello world"]
>>> results = meteor.compute(predictions=predictions, references=references)
>>> print(round(results['meteor'], 2))
0.0
```

Partial match:

```python
>>> from datasets import load_metric
>>> meteor = load_metric('meteor')
>>> predictions = ["It is a guide to action which ensures that the military always obeys the commands of the party"]
>>> references = ["It is a guide to action that ensures that the military will forever heed Party commands"]
>>> results = meteor.compute(predictions=predictions, references=references)
>>> print(round(results['meteor'], 2))
0.69
```

## Limitations and bias

While the correlation between METEOR and human judgments was measured for Chinese and Arabic and found to be significant, further experimentation is needed to check its correlation for other languages. 

Furthermore, while the alignment and matching done in METEOR is based on unigrams, using multiple word entities (e.g. bigrams) could contribute to improving its accuracy -- this has been proposed in [more recent publications](https://www.cs.cmu.edu/~alavie/METEOR/pdf/meteor-naacl-2010.pdf) on the subject.


## Citation

```bibtex
@inproceedings{banarjee2005,
  title     = {{METEOR}: An Automatic Metric for {MT} Evaluation with Improved Correlation with Human Judgments},
  author    = {Banerjee, Satanjeev  and Lavie, Alon},
  booktitle = {Proceedings of the {ACL} Workshop on Intrinsic and Extrinsic Evaluation Measures for Machine Translation and/or Summarization},
  month     = jun,
  year      = {2005},
  address   = {Ann Arbor, Michigan},
  publisher = {Association for Computational Linguistics},
  url       = {https://www.aclweb.org/anthology/W05-0909},
  pages     = {65--72},
}
```
    
## Further References 
- [METEOR -- Wikipedia](https://en.wikipedia.org/wiki/METEOR)
- [METEOR score -- NLTK](https://www.nltk.org/_modules/nltk/translate/meteor_score.html)

