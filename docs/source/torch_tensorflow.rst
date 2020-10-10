Using a Dataset with PyTorch/Tensorflow
==============================================================

Once your dataset is processed, you often want to use it with a framework such as PyTorch, Tensorflow, Numpy or Pandas. For instance we may want to use our dataset in a ``torch.Dataloader`` or a ``tf.data.Dataset`` and train a model with it.

🤗datasets provides a simple way to do this through what is called the format of a dataset.

The format of a :class:`datasets.Dataset` instance defines which columns of the dataset are returned by the :func:`datasets.Dataset.__getitem__` method and cast them in PyTorch, Tensorflow, Numpy or Pandas types.

By default, all the columns of the dataset are returned as python object. Setting a specific format allow to cast dataset examples as PyTorch/Tensorflow/Numpy/Pandas tensors, arrays or DataFrames and to filter out some columns. A typical examples is columns with strings which are usually not used to train a model and cannot be converted in PyTorch tensors. We may still want to keep them in the dataset though, for instance for the evaluation of the model so it's interesting to just "mask" them during model training.

.. note::
    The format of the dataset has no effect on the internal table storing the data, it just dynamically change the view of the dataset and examples which is returned when calling :func:`datasets.Dataset.__getitem__`.

Setting the format
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The format of a :class:`datasets.Dataset` instance can be set using the :func:`datasets.Dataset.set_format` which take as arguments:

- ``type``: an optional string defining the type of the objects that should be returned by :func:`datasets.Dataset.__getitem__`:

    - ``None``/``'python'`` (default): return python objects,
    - ``'torch'``/``'pytorch'``/``'pt'``: return PyTorch tensors,
    - ``'tensorflow'``/``'tf'``: return Tensorflow tensors,
    - ``'numpy'``/``'np'``: return Numpy arrays,
    - ``'pandas'``/``'pd'``: return Pandas DataFrames.

- ``columns``: an optional list of column names (string) defining the list of the columns which should be formated and returned by :func:`datasets.Dataset.__getitem__`. Set to None to return all the columns in the dataset (default).
- ``output_all_columns``: an optional boolean to return as python object the columns which are not selected to be formated (see the above arguments). This can be used for instance if you cannot format some columns (e.g. string columns cannot be formated as PyTorch Tensors) but would still like to have these columns returned. See an example below.

Here is how we can apply a format to a simple dataset using :func:`datasets.Dataset.set_format` and wrap it in a ``torch.utils.data.DataLoader`` or a ``tf.data.Dataset``:

.. code-block::

    >>> ## PYTORCH CODE
    >>> import torch
    >>> from datasets import load_dataset
    >>> from transformers import AutoTokenizer
    >>> dataset = load_dataset('glue', 'mrpc', split='train')
    >>> tokenizer = AutoTokenizer.from_pretrained('bert-base-cased')
    >>> dataset = dataset.map(lambda e: tokenizer(e['sentence1'], truncation=True, padding='max_length'), batched=True)
    >>>
    >>> dataset.set_format(type='torch', columns=['input_ids', 'token_type_ids', 'attention_mask', 'label'])
    >>> dataloader = torch.utils.data.DataLoader(dataset, batch_size=32)
    >>> next(iter(dataloader))
    {'attention_mask': tensor([[1, 1, 1,  ..., 0, 0, 0],
                               ...,
                               [1, 1, 1,  ..., 0, 0, 0]]),
    'input_ids': tensor([[  101,  7277,  2180,  ...,     0,     0,     0],
                         ...,
                         [  101,  1109,  4173,  ...,     0,     0,     0]]),
    'label': tensor([1, 0, 1, 0, 1, 1, 0, 1]),
    'token_type_ids': tensor([[0, 0, 0,  ..., 0, 0, 0],
                              ...,
                              [0, 0, 0,  ..., 0, 0, 0]])}
    >>> ## TENSORFLOW CODE
    >>> import tensorflow as tf
    >>> from datasets import load_dataset
    >>> from transformers import AutoTokenizer
    >>> dataset = load_dataset('glue', 'mrpc', split='train')
    >>> tokenizer = AutoTokenizer.from_pretrained('bert-base-cased')
    >>> dataset = dataset.map(lambda e: tokenizer(e['sentence1'], truncation=True, padding='max_length'), batched=True)
    >>>
    >>> dataset.set_format(type='tensorflow', columns=['input_ids', 'token_type_ids', 'attention_mask', 'label'])
    >>> features = {x: dataset[x].to_tensor(default_value=0, shape=[None, tokenizer.max_len]) for x in ['input_ids', 'token_type_ids', 'attention_mask']}
    >>> tfdataset = tf.data.Dataset.from_tensor_slices((features, dataset["label"])).batch(32)
    >>> next(iter(tfdataset))
    ({'input_ids': <tf.Tensor: shape=(32, 512), dtype=int32, numpy=
    array([[  101,  7277,  2180, ...,     0,     0,     0],
           ...,
           [  101,   142,  1813, ...,     0,     0,     0]], dtype=int32)>, 'token_type_ids': <tf.Tensor: shape=(32, 512), dtype=int32, numpy=
    array([[0, 0, 0, ..., 0, 0, 0],
           ...,
           [0, 0, 0, ..., 0, 0, 0]], dtype=int32)>, 'attention_mask': <tf.Tensor: shape=(32, 512), dtype=int32, numpy=
    array([[1, 1, 1, ..., 0, 0, 0],
           ...,
           [1, 1, 1, ..., 0, 0, 0]], dtype=int32)>}, <tf.Tensor: shape=(32,), dtype=int64, numpy=
    array([1, 0, 1, 0, 1, 1, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 1, 1, 1,
           0, 1, 1, 1, 0, 0, 1, 1, 1, 0])>)

In this examples we filtered out the string columns `sentence1` and `sentence2` since they cannot be converted easily as tensors (at least in PyTorch). As detailed above, we could still output them as python object by setting ``output_all_columns=True``.

Reseting the format
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Reseting the format to the default behavior (returning all columns as python object) can be done either by calling :func:`datasets.Dataset.reset_format` or by calling :func:`datasets.Dataset.set_format` with no arguments.

Accessing the format
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The current format of the dataset can be queried by accessing the :obj:`datasets.Dataset.format` property which return a dictionnary with the current values of the ``type``, ``columns`` and ``output_all_columns`` values.

This dict can be stored and used as named argument inputs for :func:`datasets.Dataset.set_format` if necessary (``dataset.set_format(**dataset.format)``).
