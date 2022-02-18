import numpy as np

from datasets import load_metric


metric = load_metric("./metrics/mean_iou")

predicted = np.random.rand(3, 2)
ground_truth = np.random.rand(3, 2)

results = metric.compute(predictions=predicted, references=ground_truth)
