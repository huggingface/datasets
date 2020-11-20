Loading a Metric
==============================================================

The library also provides a selection of metrics focusing in particular on:

- providing a common API accross a range of NLP metrics,
- providing metrics associated to some benchmark datasets provided by the libray such as GLUE or SQuAD,
- providing access to recent and somewhat complex metrics such as BLEURT or BERTScore,
- allowing simple use of metrics in distributed and large-scale settings.

Metrics in the `datasets` library have a lot in common with how :class:`datasets.Datasets` are loaded and provided using :func:`datasets.load_dataset`.

Like datasets, metrics are added to the library as small scripts wrapping them in a common API.

A :class:`datasets.Metric` can be created from various source:

- from a metric script provided on the `HuggingFace Hub <https://huggingface.co/metrics>`__, or
- from a metric script provide at a local path in the filesystem.

In this section we detail these options to access metrics.

From the HuggingFace Hub
-------------------------------------------------

A range of metrics are provided on the `HuggingFace Hub <https://huggingface.co/metrics>`__.

.. note::

    You can also add new metric to the Hub to share with the community as detailed in the guide on :doc:`adding a new metric<add_metric>`.

All the metrics currently available on the `Hub <https://huggingface.co/metrics>`__ can be listed using :func:`datasets.list_metrics`:

.. code-block::

    >>> from datasets import list_metrics
    >>> metrics_list = list_metrics()
    >>> len(metrics_list)
    13
    >>> print(', '.join(metric.id for metric in metrics_list))
    bertscore, bleu, bleurt, coval, gleu, glue, meteor,
    rouge, sacrebleu, seqeval, squad, squad_v2, xnli


To load a metric from the Hub we use the :func:`datasets.load_metric` command and give it the short name of the metric you would like to load as listed above.

Let's load the metric associated to the **MRPC subset of the GLUE benchmark for Natural Language Understanding**. You can explore this dataset and find more details about it `on the online viewer here <https://huggingface.co/nlp/viewer/?dataset=glue&config=mrpc>`__ :

.. code-block::

    >>> from datasets import load_metric
    >>> metric = load_metric('glue', 'mrpc')
    >>>
    >>> # Example of typical usage
    >>> for batch in dataset:
    >>>     inputs, references = batch
    >>>     predictions = model(inputs)
    >>>     metric.add_batch(predictions=predictions, references=references)
    >>> score = metric.compute()

This call to :func:`datasets.load_metric` does the following steps under the hood:

1. Download and import the **GLUE metric python script** from the Hub if it's not already stored in the library.

.. note::

    Metric scripts are small python scripts which define the API of the metrics and contain the meta-information on the metric (citation, homepage, etc).
    Metric script sometime need to import additional packages. If these packages are not installed an explicit message with information on how to install the additional packages should be raised.
    You can find the GLUE metric script `here <https://github.com/huggingface/datasets/tree/master/metrics/glue/glue.py>`__ for instance.

2. Run the python metric script which will **instantiate and return a :class:`datasets.Metric` object** which is in charge of storing predictions/references and computing the metric values.

.. note::

    The :class:`datasets.Metric` object use Apache Arrow Tables as the internal storing format for predictions and references. It allows to store predictions and references directly on disk with memory-mapping and thus do lazy computation of the metrics, in particular to easily gather the predictions in a distributed setup. The default in 🤗datasets is to always memory-map metrics data on drive.

Using a custom metric script
-----------------------------------------------------------

If the provided metrics are not adapted for your use case or you want to test and use a novel metric script, you can also easily write and use your own metric script.

You can use a local metric script just by providing its path instead of the usual shortcut name:

.. code-block::

    >>> from datasets import load_metric
    >>> metric = load_metric('PATH/TO/MY/METRIC/SCRIPT')
    >>>
    >>> # Example of typical usage
    >>> for batch in dataset:
    >>>     inputs, references = batch
    >>>     predictions = model(inputs)
    >>>     metric.add_batch(predictions=predictions, references=references)
    >>> score = metric.compute()

We provide more details on how to create your own metric script on the :doc:`add_metric` page and you can also find some inspiration in all the already provided metric scripts on the `GitHub repository <https://github.com/huggingface/datasets/tree/master/metrics>`__.


Special arguments for loading
-----------------------------------------------------------

In addition to the name of the metric, the :func:`datasets.load_metric` function accept a few arguments to customize the behaviors of the metrics. We detail them in this section.

Selecting a configuration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Some metrics comprise several :obj:`configurations`. A Configuration define a specific behavior for a metric which can be selected among several behaviors.

This is in particular useful for composite benchmarks like GLUE which comprise several sub-sets with different associated metrices.

For instance the GLUE benchmark comprise 11 sub-sets and this metric was further extended with support for the adversarial `HANS dataset by McCoy et al. <https://www.aclweb.org/anthology/P19-1334>`__ so the GLUE metric is provided with 12 configurations coresponding to various sub-set of this Natural Language Inference benchmark: "sst2", "mnli", "mnli_mismatched", "mnli_matched", "cola", "stsb", "mrpc", "qqp", "qnli", "rte", "wnli", "hans".

To select a specific configuration of a metric, just provide its name as the second argument to :func:`datasets.load_metric`.

.. code-block::

    >>> from datasets import load_metric
    >>> metric = load_metric('glue', 'mrpc')

Distributed setups
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In several settings, computing metrics in distributed or parrallel processing environments can be tricky since the evaluation on different sub-sets of the data is done in separate python processes. The ``datasets`` library make this easier to deal with as we detail in this section.

.. note::

    When a metric score is additive with regards to the dataset sub-set (meaning that ``f(A∪B) = f(A) + f(B)``) you can use distributed reduce operations to gather the scores computed by different processes. But when a metric is non additive (``f(A∪B) ≠ f(A) + f(B)``) which happens even for simple metrics like F1, you cannot simply gather the results of metrics evaluation on different sub-sets. A usual way to overcome this issue is to fallback on (inefficient) single process evaluation (e.g. evaluating metrics on a single GPU). The ``datasets`` library solve this problem by allowing distributed evaluation for any type of metric as detailed in this section.

Let's first see how to use a metric in a distributed setting before giving a few words about the internals. Let's say we train and evaluate a model in 8 parallel processes (e.g. using PyTorch's `DistributedDataParallel <https://pytorch.org/tutorials/intermediate/ddp_tutorial.html>`__ on a server with 8 GPUs).

We assume your python script can have access to:

- the total number of processes as an integer we'll call ``num_process`` (in our example 8),
- the process id of each process as an integer between 0 and ``num_process-1`` that we'll call ``rank`` (in our case betwen 0 and 7 included).

Here is how we can instantiate the metric in such a distributed script:

.. code-block::

    >>> from datasets import load_metric
    >>> metric = load_metric('glue', 'mrpc', num_process=num_process, process_id=process_id)

And that's it, you can use the metric on each node as described in :doc:`using_metrics` without taking special care for the distributed setting. In particular, the predictions and references can be computed and provided to the metric separately on each process. By default, the final evaluation of the metric will be done on the first node (rank 0) only when calling :func:`datasets.Metric.compute` after gathering the predictions and references from all the nodes. Computing on other processes (rank > 0) returns ``None``.

Under the hood :class:`datasets.Metric` use an Apache Arrow table to store (temporarly) predictions and references for each node on the hard-drive thereby avoiding to cluter the GPU or CPU memory. Once the final metric evalution is requested with :func:`datasets.Metric.compute`, the first node get access to all the nodes temp files and read them to compute the metric in one time.

This way it's possible to perform distributed predictions (which is important for evaluation speed in distributed setting) while allowing to use complex non-additive metrics and avoiding to cluter GPU/CPU memory for prediction storage.

The synchronization is basically provided by the hard drive file access and filelocks.


Multiple and independant distributed setups
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In some cases, several **independant and not related** distributed evaluations might be running on the same server and the same file system at the same time (e.g. two independant multi-processing trainings running on the same server) and it is then important to distinguish these experiemnts and allow them to operate in independantly.

In this situation you should provide an ``experiment_id`` to :func:`datasets.load_metric` which has to be a unique identifier of the current distributed experiment.

This identifier will be added to the cache file used by each process of this evaluation to avoid conflicting access to the same cache files for storing predictions and references for each node.

.. note::
    Specifying an ``experiment_id`` to :func:`datasets.load_metric` is only required in the specific situation where you have **independant (i.e. not related) distributed** evaluations running on the same file system at the same time.

Here is an example:

    >>> from datasets import load_metric
    >>> metric = load_metric('glue', 'mrpc', num_process=num_process, process_id=process_id, experiment_id="My_experiment_10")

Cache file and in-memory
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

As detailed in :doc:`using_metrics`, each time you call :func:`datasets.Metric.add_batch` or :func:`datasets.Metric.add` in a typical setup as illustrated below, the new predictions and references are added to a temporary storing table.

.. code-block::

    >>> from datasets import load_metric
    >>> metric = load_metric('glue', 'mrpc')
    >>>
    >>> # Example of typical usage
    >>> for batch in dataset:
    >>>     inputs, references = batch
    >>>     predictions = model(inputs)
    >>>     metric.add_batch(predictions=predictions, references=references)
    >>> score = metric.compute()

By default this table is stored on the drive to avoid consuming GPU/CPU memory.

You can control the location where this temporary table is stored with the ``cache_dir`` argument of :func:`datasets.load_metric`. ``cache_dir`` should be provided with the path of a directory in a writable file system.

Here is an example:

.. code-block::

    >>> from datasets import load_metric
    >>> metric = load_metric('glue', 'mrpc', cache_dir="MY/CACHE/DIRECTORY")

Alternatively, it's possible to avoiding storing the predictions and references on the drive and keep them in CPU memory (RAM) by setting the ``keep_in_memory`` argument of :func:`datasets.load_metric` to ``True`` as shown here:

.. code-block::

    >>> from datasets import load_metric
    >>> metric = load_metric('glue', 'mrpc', keep_in_memory=True)


.. note::
    Keeping the predictions in-memory is not possible in distributed setting since the CPU memory spaces of the various process are not shared.
