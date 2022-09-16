# Metric Card for CUAD

## Metric description

This metric wraps the official scoring script for version 1 of the [Contract Understanding Atticus Dataset (CUAD)](https://huggingface.co/datasets/cuad), which is a corpus of more than 13,000 labels in 510 commercial legal contracts that have been manually labeled to identify 41 categories of important clauses that lawyers look for when reviewing contracts in connection with corporate transactions.

The CUAD metric computes several scores: [Exact Match](https://huggingface.co/metrics/exact_match), [F1 score](https://huggingface.co/metrics/f1), Area Under the Precision-Recall Curve, [Precision](https://huggingface.co/metrics/precision) at 80% [recall](https://huggingface.co/metrics/recall) and Precision at 90% recall.

## How to use 

The CUAD metric takes two inputs :


`predictions`, a list of question-answer dictionaries with the following key-values:
- `id`: the id of the question-answer pair as given in the references.
- `prediction_text`: a list of possible texts for the answer, as a list of strings depending on a threshold on the confidence probability of each prediction.


`references`: a list of question-answer dictionaries with the following key-values:
 - `id`: the id of the question-answer pair (the same as above).
 - `answers`: a dictionary *in the CUAD dataset format* with the following keys:
   - `text`: a list of possible texts for the answer, as a list of strings.
   - `answer_start`: a list of start positions for the answer, as a list of ints.

 Note that `answer_start` values are not taken into account to compute the metric.

```python
from datasets import load_metric
cuad_metric = load_metric("cuad")
predictions = [{'prediction_text': ['The seller:', 'The buyer/End-User: Shenzhen LOHAS Supply Chain Management Co., Ltd.'], 'id': 'LohaCompanyltd_20191209_F-1_EX-10.16_11917878_EX-10.16_Supply Agreement__Parties'}]
references = [{'answers': {'answer_start': [143, 49], 'text': ['The seller:', 'The buyer/End-User: Shenzhen LOHAS Supply Chain Management Co., Ltd.']}, 'id': 'LohaCompanyltd_20191209_F-1_EX-10.16_11917878_EX-10.16_Supply Agreement__Parties'}]
results = cuad_metric.compute(predictions=predictions, references=references)
```
## Output values

The output of the CUAD metric consists of a dictionary that contains one or several of the following metrics:

`exact_match`: The normalized answers that exactly match the reference answer, with a range between 0.0 and 1.0 (see [exact match](https://huggingface.co/metrics/exact_match) for more information).

`f1`: The harmonic mean of the precision and recall (see [F1 score](https://huggingface.co/metrics/f1) for more information). Its range is between 0.0 and 1.0 -- its lowest possible value is 0, if either the precision or the recall is 0, and its highest possible value is 1.0, which means perfect precision and recall.

`aupr`: The Area Under the Precision-Recall curve, with a range between 0.0 and 1.0, with a higher value representing both high recall and high precision, and a low value representing low values for both. See the [Wikipedia article](https://en.wikipedia.org/wiki/Receiver_operating_characteristic#Area_under_the_curve) for more information.

`prec_at_80_recall`: The fraction of true examples among the predicted examples at a recall rate of 80%. Its range is between 0.0 and 1.0. For more information, see [precision](https://huggingface.co/metrics/precision) and [recall](https://huggingface.co/metrics/recall).

`prec_at_90_recall`: The fraction of true examples among the predicted examples at a recall rate of 90%. Its range is between 0.0 and 1.0. 


### Values from popular papers
The [original CUAD paper](https://arxiv.org/pdf/2103.06268.pdf) reports that a [DeBERTa model](https://huggingface.co/microsoft/deberta-base) attains
an AUPR of 47.8%, a Precision at 80% Recall of 44.0%, and a Precision at 90% Recall of 17.8% (they do not report F1 or Exact Match separately).

For more recent model performance, see the [dataset leaderboard](https://paperswithcode.com/dataset/cuad).

## Examples 

Maximal values :

```python
from datasets import load_metric
cuad_metric = load_metric("cuad")
predictions = [{'prediction_text': ['The seller:', 'The buyer/End-User: Shenzhen LOHAS Supply Chain Management Co., Ltd.'], 'id': 'LohaCompanyltd_20191209_F-1_EX-10.16_11917878_EX-10.16_Supply Agreement__Parties'}]
references = [{'answers': {'answer_start': [143, 49], 'text': ['The seller:', 'The buyer/End-User: Shenzhen LOHAS Supply Chain Management Co., Ltd.']}, 'id': 'LohaCompanyltd_20191209_F-1_EX-10.16_11917878_EX-10.16_Supply Agreement__Parties'}]
results = cuad_metric.compute(predictions=predictions, references=references)
print(results)
{'exact_match': 100.0, 'f1': 100.0, 'aupr': 0.0, 'prec_at_80_recall': 1.0, 'prec_at_90_recall': 1.0}
```

Minimal values:

```python
from datasets import load_metric
cuad_metric = load_metric("cuad")
predictions = [{'prediction_text': ['The Company appoints the Distributor as an exclusive distributor of Products in the Market, subject to the terms and conditions of this Agreement.'], 'id': 'LIMEENERGYCO_09_09_1999-EX-10-DISTRIBUTOR AGREEMENT__Exclusivity_0'}]
references = [{'answers': {'answer_start': [143], 'text': 'The seller'}, 'id': 'LIMEENERGYCO_09_09_1999-EX-10-DISTRIBUTOR AGREEMENT__Exclusivity_0'}]
results = cuad_metric.compute(predictions=predictions, references=references)
print(results)
{'exact_match': 0.0, 'f1': 0.0, 'aupr': 0.0, 'prec_at_80_recall': 0, 'prec_at_90_recall': 0}
```

Partial match: 

```python
from datasets import load_metric
cuad_metric = load_metric("cuad")
predictions = [{'prediction_text': ['The seller:', 'The buyer/End-User: Shenzhen LOHAS Supply Chain Management Co., Ltd.'], 'id': 'LohaCompanyltd_20191209_F-1_EX-10.16_11917878_EX-10.16_Supply Agreement__Parties'}]
predictions = [{'prediction_text': ['The Company appoints the Distributor as an exclusive distributor of Products in the Market, subject to the terms and conditions of this Agreement.', 'The buyer/End-User: Shenzhen LOHAS Supply Chain Management Co., Ltd.'], 'id': 'LohaCompanyltd_20191209_F-1_EX-10.16_11917878_EX-10.16_Supply Agreement__Parties'}]
results = cuad_metric.compute(predictions=predictions, references=references)
print(results)
{'exact_match': 100.0, 'f1': 50.0, 'aupr': 0.0, 'prec_at_80_recall': 0, 'prec_at_90_recall': 0}
```

## Limitations and bias
This metric works only with datasets that have the same format as the [CUAD dataset](https://huggingface.co/datasets/cuad). The limitations of the biases of this dataset are not discussed, but could exhibit annotation bias given the homogeneity of annotators for this dataset.

In terms of the metric itself, the accuracy of AUPR has been debated because its estimates are quite noisy and because of the fact that reducing the Precision-Recall Curve to a single number ignores the fact that it is about the tradeoffs between the different systems or performance points plotted and not the performance of an individual system. Reporting the original F1 and exact match scores is therefore useful to ensure a more complete representation of system performance.


## Citation

```bibtex
@article{hendrycks2021cuad,
      title={CUAD: An Expert-Annotated NLP Dataset for Legal Contract Review},
      author={Dan Hendrycks and Collin Burns and Anya Chen and Spencer Ball},
      journal={arXiv preprint arXiv:2103.06268},
      year={2021}
}
```
    
## Further References 

- [CUAD dataset homepage](https://www.atticusprojectai.org/cuad-v1-performance-announcements)
