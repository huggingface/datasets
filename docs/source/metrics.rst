Metrics
=======

Datasets provides various common and NLP-specific `Metrics <https://huggingface.co/metrics>`_ for you to measure your model's performance. In the final part of this tutorial, you will load a metric and use it to evaluate your model's predictions.

You can take a look at all the available metrics with :func:`datasets.list_metrics`:

    >>> from datasets import list_metrics
    >>> metrics_list = list_metrics()
    >>> len(metrics_list)
    28
    >>> print(metrics_list)
    ['accuracy', 'bertscore', 'bleu', 'bleurt', 'cer', 'comet', 'coval', 'cuad', 'f1', 'gleu', 'glue', 'indic_glue', 'matthews_correlation', 'meteor', 'pearsonr', 'precision', 'recall', 'rouge', 'sacrebleu', 'sari', 'seqeval', 'spearmanr', 'squad', 'squad_v2', 'super_glue', 'wer', 'wiki_split', 'xnli']

Load metric
-------------

Datasets makes it extremely easy to load a metric. In fact, you will notice that it is very similar to loading a dataset. You can load a metric from the Hub with :func:`datasets.load_metric`:

    >>> from datasets import load_metric
    >>> metric = load_metric('glue', 'mrpc')

This will load the metric associated with the MRPC dataset from the GLUE benchmark.

Select a configuration
----------------------

If you are using a benchmark dataset, you need to select a metric that is associated with the configuration you are using. Select a metric configuration by providing the configuration name:

    >>> metric = load_metric('glue', 'mrpc')

Metrics object
--------------

Before you begin using a :class:`datasets.Metric` object, you should get to know it a little better. As with a dataset, you can quickly get some basic information about a metric. For example, you can use :obj:`datasets.Metric.inputs_descriptions` to produce information about a metric's expected input format and some usage examples:

    >>> print(metric.inputs_description)
    Compute GLUE evaluation metric associated to each GLUE dataset.
    Args:
        predictions: list of predictions to score.
            Each translation should be tokenized into a list of tokens.
        references: list of lists of references for each translation.
            Each reference should be tokenized into a list of tokens.
    Returns: depending on the GLUE subset, one or several of:
        "accuracy": Accuracy
        "f1": F1 score
        "pearson": Pearson Correlation
        "spearmanr": Spearman Correlation
        "matthews_correlation": Matthew Correlation
    Examples:
        ...
        ...
        >>> glue_metric = datasets.load_metric('glue', 'mrpc')  # 'mrpc' or 'qqp'
        >>> references = [0, 1]
        >>> predictions = [0, 1]
        >>> results = glue_metric.compute(predictions=predictions, references=references)
        >>> print(results)
        {'accuracy': 1.0, 'f1': 1.0}
        ...
        ...
        >>> glue_metric = datasets.load_metric('glue', 'cola')
        >>> references = [0, 1]
        >>> predictions = [0, 1]
        >>> results = glue_metric.compute(predictions=predictions, references=references)
        >>> print(results)
        {'matthews_correlation': 1.0}

Notice for the MRPC configuration, the metric expects the input format to be zero or one. For a complete list of attributes you can return with your metric, take a look at :class:`datasets.MetricInfo`.

Compute metric
--------------

Once you have loaded a metric, you are ready to use it to evaluate a model's predictions. Provide the model predictions and references to :func:`datasets.Metric.compute`:

    >>> model_predictions = model(model_inputs)
    >>> final_score = metric.compute(predictions=model_predictions, references=gold_references)

What's next?
------------

Congratulations, you have completed your first Datasets tutorial! 🤗 

Over the course of this tutorial, you learned the basic steps of using Datasets. You loaded a dataset from the Hub, and learned how to access the information stored inside the dataset. Next, you tokenized the dataset into sequences of integers, and formatted it so you can use it with PyTorch or TensorFlow. Finally, you loaded a metric to evaluate your model's performance. This is really all you need to get started with Datasets! 

Now that you have a solid grasp of what Datasets can do, you can begin formulating your own questions about how you can use it with your custom dataset. Please take a look at our how-to guides for more practical help on solving common use-cases, or read our conceptual guides to deepen your understanding about Datasets.