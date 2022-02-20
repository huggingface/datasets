Dataset features
================

:class:`datasets.Features` defines the internal structure of a dataset. It is used to specify the underlying serialization format. What's more interesting to you though is that :class:`datasets.Features` contains high-level information about everything from the column names and types, to the :class:`datasets.ClassLabel`. You can think of :class:`datasets.Features` as the backbone of a dataset.

The :class:`datasets.Features` format is simple: ``dict[column_name, column_type]``. It is a dictionary of column name and column type pairs. The column type provides a wide range of options for describing the type of data you have.

Let's have a look at the features of the MRPC dataset from the GLUE benchmark:

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
* The ``sentence1`` and ``sentence2`` data types are ``string``.

🤗 Datasets supports many other data types such as ``bool``, ``float32`` and ``binary`` to name just a few.

.. seealso::

   Refer to :class:`datasets.Value` for a full list of supported data types.

The :class:`datasets.ClassLabel` feature informs 🤗 Datasets the ``label`` column contains two classes. The classes are labeled ``not_equivalent`` and ``equivalent``. Labels are stored as integers in the dataset. When you retrieve the labels, :func:`datasets.ClassLabel.int2str` and :func:`datasets.ClassLabel.str2int` carries out the conversion from integer value to label name, and vice versa.

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

The ``answers`` field is constructed using the :class:`datasets.Sequence` feature because it contains two subfields, ``text`` and ``answer_start``, which are lists of ``string`` and ``int32``, respectively.

.. tip::

   See the :ref:`flatten` section to learn how you can extract the nested subfields as their own independent columns.

The array feature type is useful for creating arrays of various sizes. You can create arrays with two dimensions using :class:`datasets.Array2D`, and even arrays with five dimensions using :class:`datasets.Array5D`. 

.. code::

   >>> features = Features({'a': Array2D(shape=(1, 3), dtype='int32'))

The array type also allows the first dimension of the array to be dynamic. This is useful for handling sequences with variable lengths such as sentences, without having to pad or truncate the input to a uniform shape.

.. code::

   >>> features = Features({'a': Array3D(shape=(None, 5, 2), dtype='int32')})