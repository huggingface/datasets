Using a Metric
==============================================================

Evaluating a model's predictions with :class:`nlp.Metric` involve just a couple of methods:
- :func:`nlp.Metric.add` and :func:`nlp.Metric.add_batch` are used to add paris of predictions/reference (or just predictions if the metrics doesn't make use of references) to a temporary (and memory efficient) cache table,
- :func:`nlp.Metric.compute` then compute the metric score from the stored predictions/references.

A typical **two-steps workflow** to compute the metric is thus as follow:

.. code-block::

    import nlp

    metric = nlp.load_metric('my_metric')

    for model_input, gold_references in evaluation_dataloader:
        model_prediction = model(model_inputs)
        metric.add_batch(predictions=model_prediction, references=gold_references)

    final_score = metric.compute()

Alternatively, when the model predictions can be computed in one step, a **single-step workflow** can be used by directly feeding the predictions/references to :func:`nlp.Metric.compute` as follow:

.. code-block::

    import nlp

    metric = nlp.load_metric('my_metric')

    model_prediction = model(model_inputs)

    final_score = metric.compute(predictions=model_prediction, references=gold_references)


.. note::

    Uner the hood, both the two-steps workflow and the single-step workflow use a temporary cache table to store predictions/references before computing the scores. This is convenient for several reasons that we briefly detail here. The `nlp` library is designed to handle a wide range of metrics and in particular metrics whose scores depends on the evaluation set in non-additive ways (``f(A∪B) ≠ f(A) + f(B)``). Storing predictions/references make this quite convenient. The library is also designed to be efficient in terms of CPU/GPU memory even when the predictions/references pairs involve large objects by using memory-mapped temporary cache files thus effectively requiring almost no CPU/GPU memory to store prediction. Lastly, storing predictions/references pairs in temporary cache files enable easy distributed computation for the metrics by using the cahce file as synchronization objects across the various processes.

Adding predictions and references
-----------------------------------------

Adding model predictions and references can be done using either one of the :func:`nlp.Metric.add`, :func:`nlp.Metric.add_batch` and :func:`nlp.Metric.compute` methods (only once for the last one).

:func:`nlp.Metric.add`, :func:`nlp.Metric.add_batch` are pretty intuitve to use. They only accept two arguments:
- ``predictions`` (for :func:`nlp.Metric.add_batch`) and ``prediction`` (for :func:`nlp.Metric.add`) should contains the predictions of a model to be evaluated by mean of the metric. For :func:`nlp.Metric.add` this will be a single prediction, for :func:`nlp.Metric.add_batch` this will be a batch of predictions.
- ``references`` (for :func:`nlp.Metric.add_batch`) and ``reference`` (for :func:`nlp.Metric.add`) should contains the references that the model predictions should be compared to if this metric require references. For :func:`nlp.Metric.add` this will be the reference associated to a single prediction, for :func:`nlp.Metric.add_batch` this will be references associated to a batch of predictions. Note that some metrics accept several references to compare each model prediction to.

:func:`nlp.Metric.add` and :func:`nlp.Metric.add_batch` require **named arguments** to avoid the silent error of mixing predictions with references.

The model predictions and references can be provided in a wide number of formats (python lists, numpy arrays, pytorch tensors, tensorflow tensors), the metric object will take care of converting them to a suitable format for temporary storage and computation (as well as bringing them back to cpu and detaching them from gradients for PyTorch tensors).

The exact format of the inputs is specific to each metric script and can be found in :obj:`nlp.Metric.features`, :obj:`nlp.Metric.inputs_descriptions` and the string representation of the :class:`nlp.Metric` object:

.. code-block::

    >>> import nlp

    >>> metric = nlp.load_metric('./metrics/sacrebleu')

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
    {'predictions': Value(dtype='string', id='sequence'), 'references': Sequence(feature=Value(dtype='string', id='sequence'), length=-1, id='references')}

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
    >>> score = metric.add_batch(predictions=sys_batch, references=reference_batch)
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
    """, stored examples: 3)

We have stored three evaluation examples in our metric, now let's compute the score.

Conmputing the metric scores
-----------------------------------------

