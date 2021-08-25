Dataset features
================

:class:`datasets.Features` defines the internal structure of a dataset. The :class:`datasets.Features` are used to specify the underlying serialization format. What's more interesting to you though is that :class:`datasets.Features` contains high-level information about everything from the column names and types, to the :class:`datasets.ClassLabel`. You can think of :class:`datasets.Features` as the backbone of a dataset.

The :class:`datasets.Features` format is simple: ``dict[column_name, column_type]``. It is a dictionary of a column name, and column type. The column type provides a wide range of options for describing the type of data you have. 

Let's have a look at the features of the MRPC dataset:

.. code-block::

   >>> from datasets import load_dataset
   >>> dataset = load_dataset('glue', 'mrpc', split='train')
   >>> dataset.features
   {'idx': Value(dtype='int32', id=None),
    'label': ClassLabel(num_classes=2, names=['not_equivalent', 'equivalent'], names_file=None, id=None),
    'sentence1': Value(dtype='string', id=None),
    'sentence2': Value(dtype='string', id=None),
   }

The :class:`datasets.Value` feature tells 🤗 Datasets:

* The ``idx`` data type is ``int32``.
* The ``sentence`` data types are ``string``. 

🤗 Datasets supports many other data types such as ``bool``, ``float32`` and ``binary`` to name just a few. 

.. seealso::

   Refer to :class:`datasets.Value` for a full list of supported data types.
 
The :class:`datasets.ClassLabel` feature informs 🤗 Datasets the ``label`` column contains two classes. The classes are labeled ``not_equivalent`` and ``equivalent``. Labels are stored as integers in the dataset. When you retrieve the labels, :func:`datasets.ClassLabel.str2int` and :func:`datasets.ClassLabel.int2str` carries out the conversion from integer value to label name, and vice versa.

If your data type contains a list of objects, then you want to use the :class:`datasets.Sequence` feature. Remember the SQuAD dataset?

.. code-block::

   >>> from datasets import load_dataset
   >>> dataset = load_dataset('squad', split='train')
   >>> dataset.features
   {'answers': Sequence(feature={'text': Value(dtype='string', id=None), 'answer_start': Value(dtype='int32', id=None)}, length=-1, id=None),
   'context': Value(dtype='string', id=None),
   'id': Value(dtype='string', id=None),
   'question': Value(dtype='string', id=None),
   'title': Value(dtype='string', id=None)}

The ``answers`` field is constructed using the :class:`datasets.Sequence` feature because it contains two subfields: ``text`` and ``answer_start``. 

.. tip::

   See the :ref:`flatten` section to learn how you can extract the nested subfields as their own independent columns.