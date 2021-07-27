Dataset features
================

:class:`datasets.Features` defines the internal structure of a dataset, and are used to specify the underlying serialization format. What's more relevant to you though is that :class:`datasets.Features` contains high-level information about everything from the column names and types, to the :class:`datasets.ClassLabel`. Datasets uses the `Apache Arrow Automatic Type Inference <https://arrow.apache.org/docs/python/json.html#automatic-type-inference>`_ to generate the features of your dataset. This guide will help you gain a better understanding about Datasets features.

.. tip::

    See the Troubleshooting section from How-to Load a dataset to see how you can manually specify features in case Arrow inferred an unexpected data type.

The format of :class:`datasets.Features` is simple: ``dict[column_name, column_type]``. The column type provides a wide range of options for describing the type of data you have. Let's take a look at the features of the MRPC dataset again:

   >>> from datasets import load_dataset
   >>> dataset = load_dataset('glue', 'mrpc', split='train')
   >>> dataset.features
   {'idx': Value(dtype='int32', id=None),
    'label': ClassLabel(num_classes=2, names=['not_equivalent', 'equivalent'], names_file=None, id=None),
    'sentence1': Value(dtype='string', id=None),
    'sentence2': Value(dtype='string', id=None),
   }

The :class:`datasets.Value` feature tells Datasets that the ``idx`` data type is ``int32``, and the sentences' data types are ``string``. A large number of other data types are supported such as ``bool``, ``float32`` and ``binary`` to name just a few. Take a look at the :class:`datasets.Value` reference for a full list of supported data types.
 

:class:`datasets.ClassLabel` informs Datasets that the ``label`` column contains two classes with the labels ``not_equivalent`` and ``equivalent``. The labels are stored as integers in the dataset. When you retrieve the labels, :func:`datasets.ClassLabel.str2int` and :func:`datasets.ClassLabel.int2str` carries out the conversion from integer value to label name, and vice versa.

If your data type contains a list of objects, then you want to use the :class:`datasets.Sequence` feature. Remember the SQuAD dataset?

   >>> from datasets import load_dataset
   >>> dataset = load_dataset('squad', split='train')
   >>> dataset.features
   {'answers': Sequence(feature={'text': Value(dtype='string', id=None), 'answer_start': Value(dtype='int32', id=None)}, length=-1, id=None),
   'context': Value(dtype='string', id=None),
   'id': Value(dtype='string', id=None),
   'question': Value(dtype='string', id=None),
   'title': Value(dtype='string', id=None)}

The ``answers`` field is constructed using the :class:`datasets.Sequence` feature because it contains ``text`` and ``answer_start``. 

.. tip::

    See the Flatten section from How-to Process a dataset to see how you can extract the nested sub-fields as their own independent columns.

Lastly, there are two specific features for machine translation: :class:`datasets.Translation` and :class:`datasets.TranslationVariableLanguages`. 

[I think for the translation features, we should either add some example code like we did for the other features or remove it all together.]