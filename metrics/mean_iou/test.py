import numpy as np

from datasets import load_metric


mean_iou = load_metric("./metrics/mean_iou")

# suppose one has 3 different segmentation maps predicted
predicted_1 = np.array([[1, 2], [3, 4], [5, 255]])
actual_1 = np.array([[0, 3], [5, 4], [6, 255]])

predicted_2 = np.array([[2, 7], [9, 2], [3, 6]])
actual_2 = np.array([[1, 7], [9, 2], [3, 6]])

predicted_3 = np.array([[2, 2, 3], [8, 2, 4], [3, 255, 2]])
actual_3 = np.array([[1, 2, 2], [8, 2, 1], [3, 255, 1]])

predicted = [predicted_1, predicted_2, predicted_3]
ground_truth = [actual_1, actual_2, actual_3]

results = mean_iou.compute(
    predictions=predicted, references=ground_truth, num_labels=10, ignore_index=255, reduce_labels=False
)
print(results)
