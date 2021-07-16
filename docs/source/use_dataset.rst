Use Datasets
============

So far, you loaded a dataset from the Hub and learned how to access the information stored inside the dataset. For the final part of the tutorial, you will tokenize and use your dataset with a framework such as PyTorch or TensorFlow. By default, all Dataset columns are returned as Python objects. But you can bridge this gap by setting the format of a dataset. Formatting casts the columns into compatible PyTorch or TensorFlow types.

.. note::
    
    Often times you may want to modify the structure and content of your dataset before you use it to train a model. For example, you may want to remove a column or cast it as a different type. Datasets provides the necessary tools to do this, but since each dataset is so different, the processing approach will vary individually. For more detailed information about preprocessing data, take a look at our `guide <https://huggingface.co/transformers/preprocessing.html#>`_ from the Transformers library. Then come back and view our how-to guide to see all the different methods for processing your custom dataset. 

Tokenize
--------

Tokenization divides text into individual words called tokens. Tokens are then converted into numbers. This is what the model receives as its input. 

The first step is to install the Transformers library:

.. code-block::

    pip install transformers

Next you will import a tokenizer. It is important to use the tokenizer that is associated with the model you are using, so the text is split in the same way. In this example, you will load the BERT tokenizer because you are using the BERT model.

    >>> from transformers import BertTokenizerFast
    >>> tokenizer = BertTokenizerFast.from_pretrained('bert-base-cased')

Now you can use the tokenizer on the ``sentence1`` field of the dataset.

    >>> encoded_dataset = dataset.map(lambda examples: tokenizer(examples['sentence1']), batched=True)
    >>> encoded_dataset.column_names
    ['sentence1', 'sentence2', 'label', 'idx', 'input_ids', 'token_type_ids', 'attention_mask']
    >>> encoded_dataset[0]
    {'sentence1': 'Amrozi accused his brother , whom he called " the witness " , of deliberately distorting his evidence .',
     'sentence2': 'Referring to him as only " the witness " , Amrozi accused his brother of deliberately distorting his evidence .',
     'label': 1,
     'idx': 0,
     'input_ids': [  101,  7277,  2180,  5303,  4806,  1117,  1711,   117,  2292, 1119,  1270,   107,  1103,  7737,   107,   117,  1104,  9938, 4267, 12223, 21811,  1117,  2554,   119,   102],
     'token_type_ids': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     'attention_mask': [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    }

The tokenization process creates three new columns: ``input_ids``, ``token_type_ids``, and ``attention_mask``. These will be the inputs to the model.

Format
------

The format is set with :func:`datasets.Datasets.set_format()` which accepts three arguments:

1. ``type`` is a string defining the type of column to cast to. For example, ``torch`` returns PyTorch tensors and ``tensorflow`` returns TensorFlow tensors.
   
2. ``columns`` specifies which columns should be formatted.

After you set the format, wrap the dataset in a ``torch.utils.data.DataLoader`` or a ``tf.data.Dataset``.

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
   >>> features = {x: dataset[x].to_tensor(default_value=0, shape=[None, tokenizer.model_max_length]) for x in ['input_ids', 'token_type_ids', 'attention_mask']}
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

What's next?
------------

Congratulations, you have completed your first Datasets tutorial! 🤗 

Over the course of this tutorial, you learned the basic steps of using Datasets. You loaded a dataset from the Hub, and learned how to access the information stored inside the dataset. Next, you tokenized the dataset into sequences of integers, and formatted it so you can use it with PyTorch or TensorFlow. This is really all you need to get started with Datasets! 

Now that you have a solid grasp of what Datasets can do, you can begin formulating your own questions about how you can use it with your custom dataset. Please take a look at our how-to guides for more practical help on solving common use-cases, or read our conceptual guides to deepen your understanding about Datasets.