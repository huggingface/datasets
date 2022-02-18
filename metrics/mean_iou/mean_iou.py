# Copyright 2022 The HuggingFace Datasets Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Mean IoU (Intersection-over-Union) metric."""

from collections import OrderedDict
from typing import Dict, Optional

import numpy as np

import datasets


_DESCRIPTION = """
IoU is the area of overlap between the predicted segmentation and the ground truth divided by the area of union
between the predicted segmentation and the ground truth. For binary (two classes) or multi-class segmentation,
the mean IoU of the image is calculated by taking the IoU of each class and averaging them.
"""

_KWARGS_DESCRIPTION = """
Args:
    predictions (`List[ndarray]`):
        List of predicted segmentation maps, each of shape (height, width). Each segmentation map can be of a different size.
    references (`List[ndarray]`):
        List of ground truth segmentation maps, each of shape (height, width). Each segmentation map can be of a different size.
    num_labels (`int`):
        Number of classes (categories).
    ignore_index (`int`):
        Index that will be ignored during evaluation.
    nan_to_num (`int`, *optional*):
        If specified, NaN values will be replaced by the number defined by the user.
    label_map (`dict`, *optional*):
        If specified, dictionary mapping old label indices to new label indices.
    reduce_labels (`bool`, *optional*, defaults to `False`):
        Whether or not to reduce all label values of segmentation maps by 1. Usually used for datasets where 0 is used for background,
        and background itself is not included in all classes of a dataset (e.g. ADE20k). The background label will be replaced by 255.

Returns:
    `Dict[str, float | ndarray]` comprising various elements:
    - *overall_accuracy* (`float`):
        Overall accuracy on all images.
    - *per_category_accuracy* (`ndarray` of shape `(num_labels,)`):
        Per category accuracy.
    - *per_category_iou* (`ndarray` of shape `(num_labels,)`):
        Per category IoU.

Examples:

    >>> from datasets import load_metric
    >>> import numpy as np
    
    >>> mean_iou_metric = datasets.load_metric("mean_iou")

    >>> # suppose one has 3 different segmentation maps predicted
    >>> predicted_1 = np.array([[1, 2], [3, 4], [5, 6]])
    >>> actual_1 = np.array([[1, 3], [5, 4], [6, 6]])

    >>> predicted_2 = np.array([[2, 2], [9, 2], [3, 6]])
    >>> actual_2 = np.array([[1, 2], [8, 2], [3, 6]])

    >>> predicted_3 = np.array([[2, 2, 3], [8, 2, 4], [3, 6, 2]])
    >>> actual_3 = np.array([[1, 2, 2], [8, 2, 1], [3, 6, 1]])

    >>> predicted = [predicted_1, predicted_2, predicted_3]
    >>> ground_truth = [actual_1, actual_2, actual_3]

    >>> results = metric.compute(predictions=predicted, references=ground_truth)
"""

_CITATION = """\
@software{MMSegmentation_Contributors_OpenMMLab_Semantic_Segmentation_2020,
author = {{MMSegmentation Contributors}},
license = {Apache-2.0},
month = {7},
title = {{OpenMMLab Semantic Segmentation Toolbox and Benchmark}},
url = {https://github.com/open-mmlab/mmsegmentation},
year = {2020}
}"""


def intersect_and_union(pred_label, label, num_labels, ignore_index, label_map=dict(), reduce_labels=False):
    """Calculate intersection and Union.

    Args:
        pred_label (`ndarray`):
            Prediction segmentation map of shape (height, width).
        label (`ndarray`):
            Ground truth segmentation map of shape (height, width).
        num_labels (`int`):
            Number of categories.
        ignore_index (`int`):
            Index that will be ignored during evaluation.
        label_map (`dict`, *optional*):
            Mapping old labels to new labels. The parameter will work only when label is str. Default: dict().
        reduce_labels (`bool`, *optional*, defaults to `False`):
            Whether or not to reduce all label values of segmentation maps by 1. Usually used for datasets where 0 is used for background,
        and background itself is not included in all classes of a dataset (e.g. ADE20k). The background label will be replaced by 255.

     Returns:
         area_intersect (`ndarray`):
            The intersection of prediction and ground truth histogram on all classes.
         area_union (`ndarray`):
            The union of prediction and ground truth histogram on all classes.
         area_pred_label (`ndarray`):
            The prediction histogram on all classes.
         area_label (`ndarray`):
            The ground truth histogram on all classes.
    """
    if label_map is not None:
        for old_id, new_id in label_map.items():
            label[label == old_id] = new_id

    if reduce_labels:
        label[label == 0] = 255
        label = label - 1
        label[label == 254] = 255

    mask = label != ignore_index
    mask = np.not_equal(label, ignore_index)
    pred_label = np.array(pred_label)[mask]
    label = np.array(label)[mask]

    intersect = pred_label[pred_label == label]

    area_intersect = np.histogram(intersect, bins=num_labels, range=(0, num_labels - 1))[0]
    area_pred_label = np.histogram(pred_label, bins=num_labels, range=(0, num_labels - 1))[0]
    area_label = np.histogram(label, bins=num_labels, range=(0, num_labels - 1))[0]

    area_union = area_pred_label + area_label - area_intersect

    return area_intersect, area_union, area_pred_label, area_label


def total_intersect_and_union(results, gt_seg_maps, num_labels, ignore_index, label_map=dict(), reduce_labels=False):
    """Calculate Total Intersection and Union, by calculating `intersect_and_union` for each (predicted, ground truth) pair.

    Args:
        results (`ndarray`):
            List of prediction segmentation maps, each of shape (height, width).
        gt_seg_maps (`ndarray`):
            List of ground truth segmentation maps, each of shape (height, width).
        num_labels (`int`):
            Number of categories.
        ignore_index (`int`):
            Index that will be ignored during evaluation.
        label_map (`dict`, *optional*):
            Mapping old labels to new labels. The parameter will work only when label is str. Default: dict().
        reduce_labels (`bool`, *optional*, defaults to `False`):
            Whether or not to reduce all label values of segmentation maps by 1. Usually used for datasets where 0 is used for background,
        and background itself is not included in all classes of a dataset (e.g. ADE20k). The background label will be replaced by 255.

     Returns:
         total_area_intersect (`ndarray`):
            The intersection of prediction and ground truth histogram on all classes.
         total_area_union (`ndarray`):
            The union of prediction and ground truth histogram on all classes.
         total_area_pred_label (`ndarray`):
            The prediction histogram on all classes.
         total_area_label (`ndarray`):
            The ground truth histogram on all classes.
    """
    total_area_intersect = np.zeros((num_labels,), dtype=np.float64)
    total_area_union = np.zeros((num_labels,), dtype=np.float64)
    total_area_pred_label = np.zeros((num_labels,), dtype=np.float64)
    total_area_label = np.zeros((num_labels,), dtype=np.float64)
    for result, gt_seg_map in zip(results, gt_seg_maps):
        area_intersect, area_union, area_pred_label, area_label = intersect_and_union(
            result, gt_seg_map, num_labels, ignore_index, label_map, reduce_labels
        )
        total_area_intersect += area_intersect
        total_area_union += area_union
        total_area_pred_label += area_pred_label
        total_area_label += area_label
    return total_area_intersect, total_area_union, total_area_pred_label, total_area_label


def mean_iou(results, gt_seg_maps, num_labels, ignore_index, nan_to_num=None, label_map=dict(), reduce_labels=False):
    """Calculate Mean Intersection and Union (mIoU).

    Args:
        results (`ndarray`):
            List of prediction segmentation maps, each of shape (height, width).
        gt_seg_maps (`ndarray`):
            List of ground truth segmentation maps, each of shape (height, width).
        num_labels (`int`):
            Number of categories.
        ignore_index (`int`):
            Index that will be ignored during evaluation.
        label_map (`dict`, *optional*):
            Mapping old labels to new labels. The parameter will work only when label is str. Default: dict().
        reduce_labels (`bool`, *optional*, defaults to `False`):
            Whether or not to reduce all label values of segmentation maps by 1. Usually used for datasets where 0 is used for background,
        and background itself is not included in all classes of a dataset (e.g. ADE20k). The background label will be replaced by 255.

     Returns:
        `Dict[str, float | ndarray]` comprising various elements:
        - *overall_accuracy* (`float`):
            Overall accuracy on all images.
        - *per_category_accuracy* (`ndarray` of shape `(num_labels,)`):
            Per category accuracy.
        - *per_category_iou* (`ndarray` of shape `(num_labels,)`):
            Per category IoU.
    """
    total_area_intersect, total_area_union, total_area_pred_label, total_area_label = total_intersect_and_union(
        results, gt_seg_maps, num_labels, ignore_index, label_map, reduce_labels
    )

    # compute metrics
    metrics = OrderedDict()

    all_acc = total_area_intersect.sum() / total_area_label.sum()
    iou = total_area_intersect / total_area_union
    acc = total_area_intersect / total_area_label
    metrics["overall_accuracy"] = all_acc
    metrics["per_category_iou"] = iou
    metrics["per_category_accuracy"] = acc

    if nan_to_num is not None:
        metrics = OrderedDict(
            {metric: np.nan_to_num(metric_value, nan=nan_to_num) for metric, metric_value in metrics.items()}
        )

    return metrics


@datasets.utils.file_utils.add_start_docstrings(_DESCRIPTION, _KWARGS_DESCRIPTION)
class Mean_IoU(datasets.Metric):
    def _info(self):
        return datasets.MetricInfo(
            description=_DESCRIPTION,
            citation=_CITATION,
            inputs_description=_KWARGS_DESCRIPTION,
            features=datasets.Features(
                # 1st Seq - height dim, 2nd - width dim
                {
                    "predictions": datasets.Sequence(datasets.Sequence(datasets.Value("uint8"))),
                    "references": datasets.Sequence(datasets.Sequence(datasets.Value("uint8"))),
                }
            ),
            reference_urls=[
                "https://github.com/open-mmlab/mmsegmentation/blob/71c201b1813267d78764f306a297ca717827c4bf/mmseg/core/evaluation/metrics.py"
            ],
        )

    def _compute(
        self,
        predictions,
        references,
        num_labels: int,
        ignore_index: bool,
        nan_to_num: Optional[int] = None,
        label_map: Optional[
            Dict[int, int]
        ] = None,  # in the body: label_map = label_map if label_map is not None else {}
        reduce_labels: bool = False,
    ):
        iou_result = mean_iou(
            results=predictions,
            gt_seg_maps=references,
            num_labels=num_labels,
            ignore_index=ignore_index,
            nan_to_num=nan_to_num,
            label_map=label_map,
            reduce_labels=reduce_labels,
        )
        return iou_result
