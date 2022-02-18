import numpy as np

from datasets import load_metric


metric = load_metric("./metrics/mean_iou")

predicted_1 = np.array([[1, 2], [3, 4], [5, 6]])
actual_1 = np.array([[1, 3], [5, 4], [6, 6]])

predicted_2 = np.array([[2, 2], [9, 2], [3, 6]])
actual_2 = np.array([[1, 2], [8, 2], [3, 6]])

predicted = [predicted_1, predicted_2]
ground_truth = [actual_1, actual_2]
# ground_truth = [np.random.randint(low=0, high=30, size=(3, 2), dtype=np.uint8)]

results = metric.compute(predictions=predicted, references=ground_truth, num_labels=30, ignore_index=255)
print("Results:", results)
