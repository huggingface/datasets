# Evaluate predictions

<Tip warning={true}>

Metrics is deprecated in 🤗 Datasets. To learn more about how to use metrics, take a look at the library 🤗 [Evaluate](https://huggingface.co/docs/evaluate/index)! In addition to metrics, you can find more tools for evaluating models and datasets.

</Tip>

🤗 Datasets provides various common and NLP-specific [metrics](https://huggingface.co/metrics) for you to measure your models performance. In this section of the tutorials, you will load a metric and use it to evaluate your models predictions.

You can see what metrics are available with [`list_metrics`]:

```py
>>> from datasets import list_metrics
>>> metrics_list = list_metrics()
>>> len(metrics_list)
28
>>> print(metrics_list)
['accuracy', 'bertscore', 'bleu', 'bleurt', 'cer', 'comet', 'coval', 'cuad', 'f1', 'gleu', 'glue', 'indic_glue', 'matthews_correlation', 'meteor', 'pearsonr', 'precision', 'recall', 'rouge', 'sacrebleu', 'sari', 'seqeval', 'spearmanr', 'squad', 'squad_v2', 'super_glue', 'wer', 'wiki_split', 'xnli']
```

## Load metric

It is very easy to load a metric with 🤗 Datasets. In fact, you will notice that it is very similar to loading a dataset! Load a metric from the Hub with [`load_metric`]:

```py
>>> from datasets import load_metric
>>> metric = load_metric('glue', 'mrpc')
```

This will load the metric associated with the MRPC dataset from the GLUE benchmark.

## Select a configuration

If you are using a benchmark dataset, you need to select a metric that is associated with the configuration you are using. Select a metric configuration by providing the configuration name:

```py
>>> metric = load_metric('glue', 'mrpc')
```

## Metrics object

Before you begin using a [`Metric`] object, you should get to know it a little better. As with a dataset, you can return some basic information about a metric. For example, access the `inputs_description` parameter in [`datasets.MetricInfo`] to get more information about a metrics expected input format and some usage examples:

```py
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
    >>> glue_metric = datasets.load_metric('glue', 'sst2')  # 'sst2' or any of ["mnli", "mnli_mismatched", "mnli_matched", "qnli", "rte", "wnli", "hans"]
    >>> references = [0, 1]
    >>> predictions = [0, 1]
    >>> results = glue_metric.compute(predictions=predictions, references=references)
    >>> print(results)
    {'accuracy': 1.0}
    ...
    >>> glue_metric = datasets.load_metric('glue', 'mrpc')  # 'mrpc' or 'qqp'
    >>> references = [0, 1]
    >>> predictions = [0, 1]
    >>> results = glue_metric.compute(predictions=predictions, references=references)
    >>> print(results)
    {'accuracy': 1.0, 'f1': 1.0}
    ...
```

Notice for the MRPC configuration, the metric expects the input format to be zero or one. For a complete list of attributes you can return with your metric, take a look at [`MetricInfo`].

## Compute metric

Once you have loaded a metric, you are ready to use it to evaluate a models predictions. Provide the model predictions and references to [`~datasets.Metric.compute`]:

```py
>>> model_predictions = model(model_inputs)
>>> final_score = metric.compute(predictions=model_predictions, references=gold_references)
```
