Using a Metric
==============================================================

Evaluating a model's predictions with :class:`datasets.Metric` involves just a couple of methods:

- :func:`datasets.Metric.add` and :func:`datasets.Metric.add_batch` are used to add pairs of predictions/reference (or just predictions if a metric doesn't make use of references) to a temporary and memory efficient cache table,
- :func:`datasets.Metric.compute` then gather all the cached predictions and reference to compute the metric score.

A typical **two-steps workflow** to compute the metric is thus as follow:

.. code-block::

    import datasets

    metric = datasets.load_metric('my_metric')

    for model_input, gold_references in evaluation_dataset:
        model_predictions = model(model_inputs)
        metric.add_batch(predictions=model_predictions, references=gold_references)

    final_score = metric.compute()

Alternatively, when the model predictions over the whole evaluation dataset can be computed in one step, a **single-step workflow** can be used by directly feeding the predictions/references to the :func:`datasets.Metric.compute` method as follow:

.. code-block::

    import datasets

    metric = datasets.load_metric('my_metric')

    model_prediction = model(model_inputs)

    final_score = metric.compute(predictions=model_prediction, references=gold_references)


.. note::

    Uner the hood, both the two-steps workflow and the single-step workflow use memory-mapped temporary cache tables to store predictions/references before computing the scores (similarly to a :class:`datasets.Dataset`). This is convenient for several reasons:

    -  let us easily handle metrics whose scores depends on the evaluation set in non-additive ways, i.e. when f(A∪B) ≠ f(A) + f(B),
    - very efficient in terms of CPU/GPU memory (effectively requiring no CPU/GPU memory to use the metrics),
    - enable easy distributed computation for the metrics by using the cache file as synchronization objects across the various processes.

Adding predictions and references
-----------------------------------------

Adding model predictions and references to a :class:`datasets.Metric` instance can be done using either one of :func:`datasets.Metric.add`, :func:`datasets.Metric.add_batch` and :func:`datasets.Metric.compute` methods.

There methods are pretty simple to use and only accept two arguments for predictions/references:

- ``predictions`` (for :func:`datasets.Metric.add_batch`) and ``prediction`` (for :func:`datasets.Metric.add`) should contains the predictions of a model to be evaluated by mean of the metric. For :func:`datasets.Metric.add` this will be a single prediction, for :func:`datasets.Metric.add_batch` this will be a batch of predictions.
- ``references`` (for :func:`datasets.Metric.add_batch`) and ``reference`` (for :func:`datasets.Metric.add`) should contains the references that the model predictions should be compared to (if the metric requires references). For :func:`datasets.Metric.add` this will be the reference associated to a single prediction, for :func:`datasets.Metric.add_batch` this will be references associated to a batch of predictions. Note that some metrics accept several references to compare each model prediction to.

:func:`datasets.Metric.add` and :func:`datasets.Metric.add_batch` require the use of **named arguments** to avoid the silent error of mixing predictions with references.

The model predictions and references can be provided in a wide number of formats (python lists, numpy arrays, pytorch tensors, tensorflow tensors), the metric object will take care of converting them to a suitable format for temporary storage and computation (as well as bringing them back to cpu and detaching them from gradients for PyTorch tensors).

The exact format of the inputs is specific to each metric script and can be found in :obj:`datasets.Metric.features`, :obj:`datasets.Metric.inputs_descriptions` and the string representation of the :class:`datasets.Metric` object.

Here is an example for the sacrebleu metric:

.. code-block::

    >>> import datasets
    >>> metric = datasets.load_metric('sacrebleu')
    >>> print(metric)
    Metric(name: "sacrebleu", features: {'predictions': Value(dtype='string', id='sequence'), 'references': Sequence(feature=Value(dtype='string', id='sequence'), length=-1, id='references')}, usage: """
    Produces BLEU scores along with its sufficient statistics
    from a source against one or more references.
    Args:
        predictions: The system stream (a sequence of segments)
        references: A list of one or more reference streams (each a sequence of segments)
        smooth: The smoothing method to use
        smooth_value: For 'floor' smoothing, the floor to use
        force: Ignore data that looks already tokenized
        lowercase: Lowercase the data
        tokenize: The tokenizer to use
    Returns:
        'score': BLEU score,
        'counts': Counts,
        'totals': Totals,
        'precisions': Precisions,
        'bp': Brevity penalty,
        'sys_len': predictions length,
        'ref_len': reference length,
    """)
    >>> print(metric.features)
    {'predictions': Value(dtype='string', id='sequence'),
     'references': Sequence(feature=Value(dtype='string', id='sequence'), length=-1, id='references')}
    >>> print(metric.inputs_description)
    Produces BLEU scores along with its sufficient statistics
    from a source against one or more references.
    Args:
        predictions: The system stream (a sequence of segments)
        references: A list of one or more reference streams (each a sequence of segments)
        smooth: The smoothing method to use
        smooth_value: For 'floor' smoothing, the floor to use
        force: Ignore data that looks already tokenized
        lowercase: Lowercase the data
        tokenize: The tokenizer to use
    Returns:
        'score': BLEU score,
        'counts': Counts,
        'totals': Totals,
        'precisions': Precisions,
        'bp': Brevity penalty,
        'sys_len': predictions length,
        'ref_len': reference length,

Here we can see that the ``sacrebleu`` metric expect a sequence of segments as predictions and a list of one or several sequences of segments as references.

You can find more information on the segments in the description, homepage and publication of ``sacrebleu`` which can be access with the respective attributes on the metric:

.. code-block::

    >>> print(metric.description)
    SacreBLEU provides hassle-free computation of shareable, comparable, and reproducible BLEU scores.
    Inspired by Rico Sennrich's `multi-bleu-detok.perl`, it produces the official WMT scores but works with plain text.
    It also knows all the standard test sets and handles downloading, processing, and tokenization for you.
    See the [README.md] file at https://github.com/mjpost/sacreBLEU for more information.
    >>> print(metric.homepage)
    https://github.com/mjpost/sacreBLEU
    >>> print(metric.citation)
    @inproceedings{post-2018-call,
        title = "A Call for Clarity in Reporting {BLEU} Scores",
        author = "Post, Matt",
        booktitle = "Proceedings of the Third Conference on Machine Translation: Research Papers",
        month = oct,
        year = "2018",
        address = "Belgium, Brussels",
        publisher = "Association for Computational Linguistics",
        url = "https://www.aclweb.org/anthology/W18-6319",
        pages = "186--191",
    }

Let's use ``sacrebleu`` with the official quick-start example on its homepage at https://github.com/mjpost/sacreBLEU:

.. code-block::

    >>> reference_batch = [['The dog bit the man.', 'The dog had bit the man.'],
    ...                    ['It was not unexpected.', 'No one was surprised.'],
    ...                    ['The man bit him first.', 'The man had bitten the dog.']]
    >>> sys_batch = ['The dog bit the man.', "It wasn't surprising.", 'The man had just bitten him.']
    >>> metric.add_batch(predictions=sys_batch, references=reference_batch)
    >>> print(len(metric)
    3

Note that the format of the inputs is a bit different than the official sacrebleu format: we provide the references for each prediction in a list inside the list associated to the prediction while the official example is nested the other way around (list for the reference numbers and inside list for the examples).

Querying the length of a Metric object will return the number of  we can see on the last line, we have stored three evaluation examples in our metric. 

Now let's compute the sacrebleu score from these 3 evaluation datapoints.

Computing the metric scores
-----------------------------------------

The evaluation of a metric scores is done by using the :func:`datasets.Metric.compute` method.

This method can accept several arguments:

- predictions and references: you can add predictions and references (to be added at the end of the cache if you have used :func:`datasets.Metric.add` or :func:`datasets.Metric.add_batch` before)
- specific arguments that can be required or can modify the behavior of some metrics (print the metric input description to see the details with ``print(metric)`` or ``print(metric.inputs_description)``).

In the simplest case (when the predictions and references have already been added with ``add`` or ``add_batch`` and no specific argument need to be set to modify the default behavior of the metric, we can just call :func:`datasets.Metric.compute`:

.. code-block::

    >>> score = metric.compute()
    Done writing 3 examples in 265 bytes /Users/thomwolf/.cache/huggingface/metrics/sacrebleu/default/default_experiment-0430a7c7-31cb-48bf-9fb0-2a0b6c03ad81-1-0.arrow.
    Set __getitem__(key) output type to python objects for no columns  (when key is int or slice) and don't output other (un-formatted) columns.
    >>> print(score)
    {'score': 48.530827009929865, 'counts': [14, 7, 5, 3], 'totals': [17, 14, 11, 8], 'precisions': [82.3529411764706, 50.0, 45.45454545454545, 37.5], 'bp': 0.9428731438548749, 'sys_len': 17, 'ref_len': 18}

If needed and if possible for the metric, you can pass additional arguments to the :func:`datasets.Metric.compute` method to control more precisely the behavior of the metric.
These additional arguments are detailed in the metric information.

For example ``sacrebleu`` accepts the following additional arguments:

- smooth: The smoothing method to use
- smooth_value: For 'floor' smoothing, the floor to use
- force: Ignore data that looks already tokenized
- lowercase: Lowercase the data
- tokenize: The tokenizer to use

You can list these arguments with ``print(metric)`` or ``print(metric.inputs_description)`` as we saw in the previous section and have more details on the official ``sacrebleu`` homepage and publication (accessible with ``print(metric.homepage)`` and ``print(metric.citation)``):

.. code-block::

    >>> print(metric.inputs_description)
    Produces BLEU scores along with its sufficient statistics
    from a source against one or more references.
    Args:
        predictions: The system stream (a sequence of segments)
        references: A list of one or more reference streams (each a sequence of segments)
        smooth: The smoothing method to use
        smooth_value: For 'floor' smoothing, the floor to use
        force: Ignore data that looks already tokenized
        lowercase: Lowercase the data
        tokenize: The tokenizer to use
    Returns:
        'score': BLEU score,
        'counts': Counts,
        'totals': Totals,
        'precisions': Precisions,
        'bp': Brevity penalty,
        'sys_len': predictions length,
        'ref_len': reference length,

Distributed usage
^^^^^^^^^^^^^^^^^^^^^^^^^^

Using the metric in a distributed or multiprocessing setting is exactly identical with the only specific behavior that the metric will only be computed on the first node (``process_id=0``). On the other processes, :func:`datasets.Metric.compute` will return ``None``. You should still run :func:`datasets.Metric.compute` on each node though to finalize the prediction/reference writing.

We detailed on the :doc:`loading_metrics` page how to load a metric in a distributed setup.

Here is now a sample script showing how to instantiate and run a metric computation in a distributed/multi-processing setup:

Here is how we can instantiate the metric in such a distributed script:

.. code-block::

    >>> from datasets import load_metric

    >>> # NUM_PROCESS is the total number of processes in the pool (it CANNOT evolve dynamically at the moment)
    >>> # PROCESS_ID is the rank of rank of current process ranging from 0 to NUM_PROCESS (it also CANNOT evolve dynamically at the moment)
    >>> # For instance with pytorch:
    >>> #  NUM_PROCESS = torch.distributed.get_world_size()
    >>> #  PROCESS_ID = torch.distributed.get_rank()

    >>> metric = load_metric('sacrebleu', num_process=NUM_PROCESS, process_id=PROCESS_ID)

    >>> for model_input, gold_references in evaluation_dataset:
    ...     model_predictions = model(model_inputs)
    ...     metric.add_batch(predictions=model_predictions, references=gold_references)

    >>> final_score = metric.compute()  # final_score is returned on process with process_id==0 and will be `None` on the other processes
