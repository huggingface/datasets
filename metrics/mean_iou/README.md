# Metric Card for Mean IoU 


## Metric Description

IoU (Intersection over Union) is the area of overlap between the predicted segmentation and the ground truth divided by the area of union between the predicted segmentation and the ground truth. 

For binary (two classes) or multi-class segmentation, the *mean IoU* of the image is calculated by taking the IoU of each class and averaging them.

## How to Use

The Mean IoU metric takes two numeric arrays as input corresponding to the predicted and ground truth segmentations:
```python
>>> import numpy as np
>>> mean_iou = datasets.load_metric("mean_iou")
>>> predicted = np.array([[2, 2, 3], [8, 2, 4], [3, 255, 2]])
>>> ground_truth = np.array([[1, 2, 2], [8, 2, 1], [3, 255, 1]])
>>> results = mean_iou.compute(predictions=predicted, references=ground_truth, num_labels=10, ignore_index=255)
```

### Inputs
**Mandatory inputs**
- `predictions` (`List[ndarray]`): List of predicted segmentation maps, each of shape (height, width). Each segmentation map can be of a different size.
- `references` (`List[ndarray]`): List of ground truth segmentation maps, each of shape (height, width). Each segmentation map can be of a different size.
- `num_labels` (`int`): Number of classes (categories). 
- `ignore_index` (`int`): Index that will be ignored during evaluation.

**Optional inputs**
- `nan_to_num` (`int`): If specified, NaN values will be replaced by the number defined by the user.
- `label_map` (`dict`): If specified, dictionary mapping old label indices to new label indices.
- `reduce_labels` (`bool`): Whether or not to reduce all label values of segmentation maps by 1. Usually used for datasets where 0 is used for background, and background itself is not included in all classes of a dataset (e.g. ADE20k). The background label will be replaced by 255. The default value is `False`.

### Output Values
The metric returns a dictionary with the following elements:
- `mean_iou` (`float`): Mean Intersection-over-Union (IoU averaged over all categories).
- `mean_accuracy` (`float`): Mean accuracy (averaged over all categories). 
- `overall_accuracy` (`float`): Overall accuracy on all images.
- `per_category_accuracy` (`ndarray` of shape `(num_labels,)`): Per category accuracy.
- `per_category_iou` (`ndarray` of shape `(num_labels,)`): Per category IoU.

The values of all of the scores reported range from from `0.0` (minimum) and `1.0` (maximum).

Output Example:
```python
{'mean_iou': 0.47750000000000004, 'mean_accuracy': 0.5916666666666666, 'overall_accuracy': 0.5263157894736842, 'per_category_iou': array([0.   , 0.   , 0.375, 0.4  , 0.5  , 0.   , 0.5  , 1.   , 1.   , 1.   ]), 'per_category_accuracy': array([0.        , 0.        , 0.75      , 0.66666667, 1.        , 0.        , 0.5       , 1.        , 1.        , 1.        ])}
```

#### Values from Popular Papers

The [leaderboard for the CityScapes dataset](https://paperswithcode.com/sota/semantic-segmentation-on-cityscapes) reports a Mean IOU ranging from 64 to 84; that of [ADE20k](https://paperswithcode.com/sota/semantic-segmentation-on-ade20k) ranges from 30 to a peak of 59.9, indicating that the dataset is more difficult for current approaches (as of 2022). 


### Examples

```python
>>> from datasets import load_metric
>>> import numpy as np
>>> mean_iou = load_metric("mean_iou")
>>> # suppose one has 3 different segmentation maps predicted
>>> predicted_1 = np.array([[1, 2], [3, 4], [5, 255]])
>>> actual_1 = np.array([[0, 3], [5, 4], [6, 255]])
>>> predicted_2 = np.array([[2, 7], [9, 2], [3, 6]])
>>> actual_2 = np.array([[1, 7], [9, 2], [3, 6]])
>>> predicted_3 = np.array([[2, 2, 3], [8, 2, 4], [3, 255, 2]])
>>> actual_3 = np.array([[1, 2, 2], [8, 2, 1], [3, 255, 1]])
>>> predictions = [predicted_1, predicted_2, predicted_3]
>>> references = [actual_1, actual_2, actual_3]
>>> results = mean_iou.compute(predictions=predictions, references=references, num_labels=10, ignore_index=255, reduce_labels=False)
>>> print(results) # doctest: +NORMALIZE_WHITESPACE
{'mean_iou': 0.47750000000000004, 'mean_accuracy': 0.5916666666666666, 'overall_accuracy': 0.5263157894736842, 'per_category_iou': array([0.   , 0.   , 0.375, 0.4  , 0.5  , 0.   , 0.5  , 1.   , 1.   , 1.   ]), 'per_category_accuracy': array([0.        , 0.        , 0.75      , 0.66666667, 1.        , 0.        , 0.5       , 1.        , 1.        , 1.        ])}
``` 


## Limitations and Bias
Mean IOU is an average metric, so it will not show you where model predictions differ from the ground truth (i.e. if there are particular regions or classes that the model does poorly on). Further error analysis is needed to gather actional insights that can be used to inform model improvements. 

## Citation(s)
```bibtex
@software{MMSegmentation_Contributors_OpenMMLab_Semantic_Segmentation_2020,
author = {{MMSegmentation Contributors}},
license = {Apache-2.0},
month = {7},
title = {{OpenMMLab Semantic Segmentation Toolbox and Benchmark}},
url = {https://github.com/open-mmlab/mmsegmentation},
year = {2020}
}"
```


## Further References
- [Wikipedia article - Jaccard Index](https://en.wikipedia.org/wiki/Jaccard_index)
