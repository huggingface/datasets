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

The exact format of the inputs is specific to each metric script and can be read in the 
