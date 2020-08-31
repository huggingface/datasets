Loading a Metric
==============================================================

The library also provides a selection of metrics focusing in particular on:
- providing a common API accross a range of NLP metrics
- providing metrics associated to some benchmark datasets provided by the libray such as GLUE or SQuAD
- providing access to recent and more complex metrics such as BLEURT or BERTScore
- allowing a simple use of metrics in distributed and large-scale settings.

Metrics have a lot in common with how :class:`nlp.Datasets` are loaded and provided using :func:`nlp.load_dataset`.

Like datasets, metrics are added as small scripts wrapping common metrics in a common API.

A :class:`nlp.Metric` can be created from various source:

- from a metric script provided on the `HuggingFace Hub <https://huggingface.co/datasets>`__, or
- from a local metric script.

In this section we detail these options.

From the HuggingFace Hub
-------------------------------------------------

Over 13 metrics  are provided on the `HuggingFace Hub <https://huggingface.co/datasets>`__.

.. note::

    You can also add new metric to the Hub to share with the community as detailed in the guide on :doc:`adding a new metric </add_metric>`.

All the metrics currently available on the `Hub <https://huggingface.co/datasets>`__ can be listed using :func:`nlp.list_metrics`:

.. code-block::

    >>> from nlp import list_metrics
    >>> metrics_list = list_metrics()
    >>> len(metrics_list)
    13
    >>> print(', '.join(metric.id for metric in metrics_list))
    bertscore, bleu, bleurt, coval, gleu, glue, meteor,
    rouge, sacrebleu, seqeval, squad, squad_v2, xnli


To load a metric from the Hub we use the :func:`nlp.load_metric` command and give it the short name of the metric you would like to load as listed above.

Let's load the metric associated to the **MRPC subset of the GLUE benchmark for Natural Language Understanding**. You can explore this dataset and find more details about it `on the online viewer here <https://huggingface.co/nlp/viewer/?dataset=glue&config=mrpc>`__ :

.. code-block::

    >>> from nlp import load_metric
    >>> metric = load_metric('glue', 'mrpc')

This call to :func:`nlp.load_metric` does the following steps under the hood:

1. Download and import the **GLUE metric python script** from the Hub if it's not already stored in the library.

.. note::

    Metric scripts are small python scripts which define the API of the metrics and contain the meta-information on the metric (citation, homepage, etc).
    Metric script sometime need to import additional packages. If these packages are not installed an explicit message with information on how to install the additional packages should be raised.
    You can find the GLUE metric script `here <https://github.com/huggingface/nlp/tree/master/metrics/glue/glue.py>`__ for instance.

2. Run the python metric script which will **instantiate and return a :class:`nlp.Metric` object** which is in charge of storing predictions/references and computing the metric values.

.. note::

    The :class:`nlp.Metric` object use Apache Arrow Tables as the internal storing format for predictions and references. It allows to store predictions and references directly on disk with memory-mapping and thus do lazy computation of the metrics, in particular to easily gather the predictions in a distributed setup. The default in 🤗nlp is to always memory-map metrics data on drive.

Selecting a configuration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Some metrics comprise several :obj:`configurations`. A Configuration define a specific behavior for a metric which can be selected among several behaviors.

This is in particular useful for composite benchmarks like GLUE which comprise several sub-sets with different associated metrices.

For instance the GLUE benchmark has 


. Examples of dataset with several configurations are:

- the **GLUE** dataset which is an agregated benchmark comprised of 10 subsets: COLA, SST2, MRPC, QQP, STSB, MNLI, QNLI, RTE, WNLI and the diagnostic subset AX.
