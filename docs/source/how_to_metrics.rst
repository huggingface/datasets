Use Metrics
===========

In the tutorial, you saw how to compute a metric over an entire evaluation dataset. However, in some situations you may want to add more data and compute the metric over these predictions. This guide will show you how to compute the metric over these new additions.

Add predictions and references
------------------------------

When you want to add model predictions and references to a :class:`datasets.Metric` instance, use 

* :func:`datasets.Metric.add` to add a single ``prediction`` and ``reference``.
    
* :func:`datasets.Metric.add_batch` to add a batch of ``predictions`` and ``references``.

Use :func:`datasets.Metric.add_batch` by giving it your model predictions and the references the model predictions should be evaluated against:

    >>> import datasets
    >>> metric = datasets.load_metric('my_metric')
    >>> for model_input, gold_references in evaluation_dataset:
            model_predictions = model(model_inputs)
            metric.add_batch(predictions=model_predictions, references=gold_references)
    >>> final_score = metric.compute()

.. tip::

    Metrics accepts various input formats (Python lists, NumPy arrays, PyTorch tensors, etc.) and converts them to an appropriate format for storage and computation.

Compute scores
--------------

The most straightforward way to calculate a metric is to call :func:`datasets.Metric.compute`. But some metrics have additional arguments that allow you to modify the metric's behavior. Let's load the `SacreBLEU <https://huggingface.co/metrics/sacrebleu>`_ metric and compute it with a different smoothing method.

1. Load the SacreBLEU metric:

    >>> import datasets
    >>> metric = datasets.load_metric('sacrebleu')

2. Inspect the different argument methods for computing the metric:

    >>> print(metric.inputs_description)
    Produces BLEU scores along with its sufficient statistics
    from a source against one or more references.
    >>>
    Args:
        predictions: The system stream (a sequence of segments).
        references: A list of one or more reference streams (each a sequence of segments).
        smooth_method: The smoothing method to use. (Default: 'exp').
        smooth_value: The smoothing value. Only valid for 'floor' and 'add-k'. (Defaults: floor: 0.1, add-k: 1).
        tokenize: Tokenization method to use for BLEU. If not provided, defaults to 'zh' for Chinese, 'ja-mecab' for
            Japanese and '13a' (mteval) otherwise.
        lowercase: Lowercase the data. If True, enables case-insensitivity. (Default: False).
        force: Insist that your tokenized input is actually detokenized.
    ...

3. Compute the metric with the ``floor`` method and a different ``smooth_value``:

    >>> score = metric.compute(smooth_method="floor", smooth_value=0.2)
