# Copyright 2022 The HuggingFace Datasets Authors and the current dataset script contributor.
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

import numpy as np

import datasets


_DESCRIPTION = """
IoU is the area of overlap between the predicted segmentation and the ground truth divided by the area of union
between the predicted segmentation and the ground truth. For binary (two classes) or multi-class segmentation,
the mean IoU of the image is calculated by taking the IoU of each class and averaging them.
"""

_KWARGS_DESCRIPTION = """
Args:
    predictions: Predicted segmentation maps.
    references: Ground truth segmentation maps.
    num_labels (int): Number of classes (categories).
    ignore_index (int): Index that will be ignored in evaluation.
    nan_to_num (int, optional): If specified, NaN values will be replaced by the numbers defined by the user. Default: None.
    label_map (dict): Mapping old labels to new labels. Default: dict().
    reduce_zero_label (bool): Whether ignore zero label. Default: False.
Returns:
    dict[str, float | ndarray]:
            <aAcc> float: Overall accuracy on all images.
            <Acc> ndarray: Per category accuracy, shape (num_labels, ).
            <IoU> ndarray: Per category IoU, shape (num_labels, ).
Examples:

    >>> mean_iou_metric = datasets.load_metric("mean_iou")
    >>> results = mean_iou_metric.compute(references=[0, 1], predictions=[0, 1])
    >>> print(results)
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


def intersect_and_union(pred_label, label, num_classes, ignore_index, label_map=dict(), reduce_zero_label=False):
    """Calculate intersection and Union.

    Args:
        pred_label (ndarray):
            Prediction segmentation map.
        label (ndarray):
            Ground truth segmentation map.
        num_classes (int):
            Number of categories.
        ignore_index (int):
            Index that will be ignored in evaluation.
        label_map (dict):
            Mapping old labels to new labels. The parameter will work only when label is str. Default: dict().
        reduce_zero_label (bool):
            Whether ignore zero label. The parameter will work only when label is str. Default: False.
     Returns:
         (ndarray): The intersection of prediction and ground truth histogram on all classes.
         (ndarray): The union of prediction and ground truth histogram on all classes.
         (ndarray): The prediction histogram on all classes.
         (ndarray): The ground truth histogram on all classes.
    """

    if label_map is not None:
        for old_id, new_id in label_map.items():
            label[label == old_id] = new_id

    if reduce_zero_label:
        label[label == 0] = 255
        label = label - 1
        label[label == 254] = 255

    mask = label != ignore_index
    pred_label = pred_label[mask]
    label = label[mask]

    intersect = pred_label[pred_label == label]

    area_intersect = np.histogram(intersect.float(), bins=num_classes, range=np.arange(0, num_classes - 1))
    area_pred_label = np.histogram(pred_label.float(), bins=num_classes, range=np.arange(0, num_classes - 1))
    area_label = np.histogram(label.float(), bins=num_classes, range=np.arange(0, num_classes - 1))
    area_union = area_pred_label + area_label - area_intersect

    return area_intersect, area_union, area_pred_label, area_label


def total_intersect_and_union(
    results, gt_seg_maps, num_classes, ignore_index, label_map=dict(), reduce_zero_label=False
):
    """Calculate Total Intersection and Union.

    Args:
        results (list[ndarray]): List of prediction segmentation maps.
        gt_seg_maps (list[ndarray]): list of ground truth segmentation maps.
        num_classes (int): Number of categories.
        ignore_index (int): Index that will be ignored in evaluation.
        label_map (dict): Mapping old labels to new labels. Default: dict().
        reduce_zero_label (bool): Whether ignore zero label. Default: False.

     Returns:
         ndarray:
            The intersection of prediction and ground truth histogram on all classes.
         ndarray:
            The union of prediction and ground truth histogram on all classes.
         ndarray:
            The prediction histogram on all classes.
         ndarray:
            The ground truth histogram on all classes.
    """
    total_area_intersect = np.zeros((num_classes,), dtype=np.float64)
    total_area_union = np.zeros((num_classes,), dtype=np.float64)
    total_area_pred_label = np.zeros((num_classes,), dtype=np.float64)
    total_area_label = np.zeros((num_classes,), dtype=np.float64)
    for result, gt_seg_map in zip(results, gt_seg_maps):
        area_intersect, area_union, area_pred_label, area_label = intersect_and_union(
            result, gt_seg_map, num_classes, ignore_index, label_map, reduce_zero_label
        )
        total_area_intersect += area_intersect
        total_area_union += area_union
        total_area_pred_label += area_pred_label
        total_area_label += area_label
    return total_area_intersect, total_area_union, total_area_pred_label, total_area_label


def mean_iou(
    results, gt_seg_maps, num_classes, ignore_index, nan_to_num=None, label_map=dict(), reduce_zero_label=False
):
    """Calculate Mean Intersection and Union (mIoU)

    Args:
        results (list[ndarray]):
            List of prediction segmentation maps.
        gt_seg_maps (list[ndarray]):
            List of ground truth segmentation maps.
        num_classes (int):
            Number of categories.
        ignore_index (int):
            Index that will be ignored in evaluation.
        nan_to_num (int, optional):
            If specified, NaN values will be replaced by the numbers defined by the user. Default: None.
        label_map (dict):
            Mapping old labels to new labels. Default: dict().
        reduce_zero_label (bool):
            Whether to ignore the zero label. Default: False.

     Returns:
        dict[str, float | ndarray]:
            <aAcc> float: Overall accuracy on all images.
            <Acc> ndarray: Per category accuracy, shape (num_classes, ).
            <IoU> ndarray: Per category IoU, shape (num_classes, ).
    """
    total_area_intersect, total_area_union, total_area_pred_label, total_area_label = total_intersect_and_union(
        results, gt_seg_maps, num_classes, ignore_index, label_map, reduce_zero_label
    )

    # compute metrics
    all_acc = total_area_intersect.sum() / total_area_label.sum()
    ret_metrics = OrderedDict({"aAcc": all_acc})
    iou = total_area_intersect / total_area_union
    acc = total_area_intersect / total_area_label
    ret_metrics["IoU"] = iou
    ret_metrics["Acc"] = acc

    ret_metrics = {metric: value.numpy() for metric, value in ret_metrics.items()}
    if nan_to_num is not None:
        ret_metrics = OrderedDict(
            {metric: np.nan_to_num(metric_value, nan=nan_to_num) for metric, metric_value in ret_metrics.items()}
        )

    return ret_metrics


@datasets.utils.file_utils.add_start_docstrings(_DESCRIPTION, _KWARGS_DESCRIPTION)
class Mean_IoU(datasets.Metric):
    def _info(self):
        return datasets.MetricInfo(
            description=_DESCRIPTION,
            citation=_CITATION,
            inputs_description=_KWARGS_DESCRIPTION,
            features=datasets.Features(
                {
                    "predictions": datasets.Sequence(
                        datasets.Sequence(datasets.Sequence(datasets.Value("uint8")))
                    ),  # 1st Seq - batch dim, 2nd -  height dim, 3rd - width dim
                    "references": datasets.Sequence(datasets.Sequence(datasets.Sequence(datasets.Value("uint8")))),
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
        num_classes: int,
        ignore_index: bool,
        nan_to_num: Optional[int] = None,
        label_map: Optional[
            Dict[int, int]
        ] = None,  # in the body: label_map = label_map if label_map is not None else {}
        reduce_zero_label: bool = False,
    ):
        iou_result = mean_iou(
            predictions,
            references,
            num_classes=num_classes,
            ignore_index=ignore_index,
            nan_to_num=nan_to_num,
            label_map=label_map,
            reduce_zero_label=reduce_zero_label,
        )
        return iou_result
