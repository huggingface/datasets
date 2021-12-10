Evaluate predictions
====================

🤗 Datasets provides various common and NLP-specific `metrics <https://huggingface.co/metrics>`_ for you to measure your models performance. In this section of the tutorials, you will load a metric and use it to evaluate your models predictions.

You can see what metrics are available with :func:`datasets.list_metrics`:

.. code-block::

   >>> from datasets import list_metrics
   >>> metrics_list = list_metrics()
   >>> len(metrics_list) #doctest: +SKIP
   28
   >>> print(metrics_list) #doctest: +SKIP
   ['accuracy', 'bertscore', 'bleu', 'bleurt', 'cer', 'comet', 'coval', 'cuad', 'f1', 'gleu', 'glue', 'indic_glue', 'matthews_correlation', 'meteor', 'pearsonr', 'precision', 'recall', 'rouge', 'sacrebleu', 'sari', 'seqeval', 'spearmanr', 'squad', 'squad_v2', 'super_glue', 'wer', 'wiki_split', 'xnli']

Load metric
-------------

It is very easy to load a metric with 🤗 Datasets. In fact, you will notice that it is very similar to loading a dataset! Load a metric from the Hub with :func:`datasets.load_metric`:

.. code-block::

   >>> from datasets import load_metric
   >>> metric = load_metric('glue', 'mrpc')

This will load the metric associated with the MRPC dataset from the GLUE benchmark.

Select a configuration
----------------------

If you are using a benchmark dataset, you need to select a metric that is associated with the configuration you are using. Select a metric configuration by providing the configuration name:

.. code::

   >>> metric = load_metric('glue', 'mrpc')

Metrics object
--------------

Before you begin using a :class:`datasets.Metric` object, you should get to know it a little better. As with a dataset, you can return some basic information about a metric. For example, use :obj:`datasets.Metric.inputs_descriptions` to get more information about a metrics expected input format and some usage examples:

.. code-block::

   >>> metric.inputs_description
   '\nCompute GLUE evaluation metric associated to each GLUE dataset.\nArgs:\n    predictions: list of predictions to score.\n        Each translation should be tokenized into a list of tokens.\n    references: list of lists of references for each translation.\n        Each reference should be tokenized into a list of tokens.\nReturns: depending on the GLUE subset, one or several of:\n    "accuracy": Accuracy\n    "f1": F1 score\n    "pearson": Pearson Correlation\n    "spearmanr": Spearman Correlation\n    "matthews_correlation": Matthew Correlation\nExamples:\n\n    >>> glue_metric = datasets.load_metric(\'glue\', \'sst2\')  # \'sst2\' or any of ["mnli", "mnli_mismatched", "mnli_matched", "qnli", "rte", "wnli", "hans"]\n    >>> references = [0, 1]\n    >>> predictions = [0, 1]\n    >>> results = glue_metric.compute(predictions=predictions, references=references)\n    >>> print(results)\n    {\'accuracy\': 1.0}\n\n    >>> glue_metric = datasets.load_metric(\'glue\', \'mrpc\')  # \'mrpc\' or \'qqp\'\n    >>> references = [0, 1]\n    >>> predictions = [0, 1]\n    >>> results = glue_metric.compute(predictions=predictions, references=references)\n    >>> print(results)\n    {\'accuracy\': 1.0, \'f1\': 1.0}\n\n    >>> glue_metric = datasets.load_metric(\'glue\', \'stsb\')\n    >>> references = [0., 1., 2., 3., 4., 5.]\n    >>> predictions = [0., 1., 2., 3., 4., 5.]\n    >>> results = glue_metric.compute(predictions=predictions, references=references)\n    >>> print({"pearson": round(results["pearson"], 2), "spearmanr": round(results["spearmanr"], 2)})\n    {\'pearson\': 1.0, \'spearmanr\': 1.0}\n\n    >>> glue_metric = datasets.load_metric(\'glue\', \'cola\')\n    >>> references = [0, 1]\n    >>> predictions = [0, 1]\n    >>> results = glue_metric.compute(predictions=predictions, references=references)\n    >>> print(results)\n    {\'matthews_correlation\': 1.0}\n'

Notice for the MRPC configuration, the metric expects the input format to be zero or one. For a complete list of attributes you can return with your metric, take a look at :class:`datasets.MetricInfo`.

Compute metric
--------------

Once you have loaded a metric, you are ready to use it to evaluate a models predictions. Provide the model predictions and references to :obj:`datasets.Metric.compute`:

.. code-block::

   >>> model_predictions = model(model_inputs) #doctest: +SKIP
   >>> final_score = metric.compute(predictions=model_predictions, references=gold_references) #doctest: +SKIP