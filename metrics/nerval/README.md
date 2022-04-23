# Metric Card for nerval

## Metric description

Nerval is a Python framework to evaluate Named Entity Recognition (NER) models.
It generates entity-level confusion matrix and classification report.
For more information see the README.md file at https://github.com/mdadda/nerval.

## Labelling schemes supported:
IO
BIO1 (IOB1)
BIO2 (IOB2)
IOE1
IOE2
IOBES
BILOU
BMEWO

## How to use
Args:
    predictions: List of Lists of predicted labels (Estimated targets as returned by a tagger)
    references: List of Lists of reference labels (Ground truth (correct) target values)
    scheme: Specify labelling scheme.
        - BIO for the following schemes: IO / BIO1 (IOB1) / BIO2 (IOB2) / IOBES / BILOU / BMEWO
        - IOE for the following schemes: IOE1 / IOE2
        - BIO is the default scheme.

Returns:
A dictionary with 3 items:
    - classification_report: a pandas dataframe
    - confusion_matrix : a numpy 2d-array
    - cm_labels : a the list of labels for the confusion matrix. This is needed to plot the confusion matrix. The nerval package includes a plot_confusion_matrix() function.

Example:
```python
>>> from datasets import load_metric
>>> nerval = load_metric('nerval')

>>> y_true = [['O', 'B-PER', 'I-PER', 'O', 'O', 'O', 'O', 'B-LOC', 'I-LOC']]
>>> y_pred = [['O', 'B-PER', 'O', 'O', 'O', 'O', 'O', 'O', 'B-LOC']]

>>> results = nerval.compute(predictions=y_pred, references=y_true, scheme='BIO')

   True Entities: 2
   Pred Entities: 2

   True Entities with 3 or more tags: 0
   Pred Entities with 3 or more tags: 0

   True positives:  0
   False positives (true = 'O'):  1
   False positives (true <> pred):  1
   ToT False positives:  2
   False negatives:  1

>>> print(results['classification_report'])
   precision  recall  f1_score  true_entities  pred_entities
   PER                0.00    0.00      0.00           1.00           0.00
   LOC                0.00    0.00      0.00           1.00           1.00
   PER__              0.00    0.00      0.00           0.00           1.00
   micro_avg          0.00    0.00      0.00           2.00           2.00
   macro_avg          0.00    0.00      0.00           2.00           2.00
   weighted_avg       0.00    0.00      0.00           2.00           2.00

>>> print(results['confusion_matrix'])
   [[0 1 0 0]
    [1 0 0 0]
    [0 0 0 1]
    [0 0 0 0]]

>>> print(results['cm_labels'])
   ['LOC', 'O', 'PER', 'PER__']
```

### Note 1:
y_true and y_pred could be:
- flat lists
- lists of flat lists
- lists of nested lists.
Flat lists and lists of nested lists will be converted to lists of lists.

### Note 2:
The __ at the end of some entities means that true and pred have the same entity name for the first token but the prediction is somewhat different from the true label.
Example:
```
>>> y_true = ['B-ORG', 'I-ORG', 'I-ORG']
>>> y_pred = ['B-ORG']

>>> y_true = ['B-ORG', 'I-ORG', 'I-ORG']
>>> y_pred = ['B-ORG', 'I-ORG', 'I-ORG', 'I-ORG', 'I-ORG']

>>> y_true = ['B-ORG', 'I-ORG', 'I-ORG']
>>> y_pred = ['B-ORG', 'I-PER']

>>> y_true = ['B-ORG', 'I-ORG', 'I-ORG']
>>> y_pred = ['I-ORG', 'I-PER']
```

### Note 3:
In case of division by zero, the result will default to zero.

## Installation
To use the plot_confusion_matrix function:
```bash
pip install nerval
conda install -c conda-forge nerval
```

## Citation
```bibtex
@misc{nerval,
  title={{nerval}: Entity-level confusion matrix and classification report to evaluate Named Entity Recognition (NER) models.},
  url={https://github.com/mdadda/nerval},
  note={Software available from https://github.com/mdadda/nerval},
  author={Mariangela D'Addato},
  year={2022},
}
```

## Further References
- [nerval on GitHub](https://github.com/mdadda/nerval)
