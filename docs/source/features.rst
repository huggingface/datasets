Dataset features
===========================

:class:`datasets.Features` defines the internal structure of a dataset. Features are used to specify the underlying serialization format but also contain high-level information regarding the fields, e.g. column names, types, and conversion methods from names to integer values for a class label field.

A brief summary of how to use this class:

- :class:`datasets.Features` should be only called once and instantiated with a ``dict[str, FieldType]``, where keys are your desired column names, and values are the type of that column.

`FieldType` can be one of a few possibilities:

- a :class:`datasets.Value` feature specifies a single typed value, e.g. ``int64`` or ``string``. The dtypes supported are as follows:
    - null
    - bool
    - int8
    - int16
    - int32
    - int64
    - uint8
    - uint16
    - uint32
    - uint64
    - float16
    - float32 (alias float)
    - float64 (alias double)
    - timestamp[(s|ms|us|ns)]
    - timestamp[(s|ms|us|ns), tz=(tzstring)]
    - binary
    - large_binary
    - string
    - large_string

- a python :obj:`dict` specifies that the field is a nested field containing a mapping of sub-fields to sub-fields features. It's possible to have nested fields of nested fields in an arbitrary manner.

- a python :obj:`list` or a :class:`datasets.Sequence` specifies that the field contains a list of objects. The python :obj:`list` or :class:`datasets.Sequence` should be provided with a single sub-feature as an example of the feature type hosted in this list. Python :obj:`list` are simplest to define and write while :class:`datasets.Sequence` provide a few more specific behaviors like the possibility to specify a fixed length for the list (slightly more efficient).

.. note::

    A :class:`datasets.Sequence` with a internal dictionary feature will be automatically converted into a dictionary of lists. This behavior is implemented to have a compatilbity layer with the TensorFlow Datasets library but may be un-wanted in some cases. If you don't want this behavior, you can use a python :obj:`list` instead of the :class:`datasets.Sequence`.

- a :class:`datasets.ClassLabel` feature specifies a field with a predefined set of classes which can have labels associated to them and will be stored as integers in the dataset. This field will be stored and retrieved as an integer value and two conversion methods, :func:`datasets.ClassLabel.str2int` and :func:`datasets.ClassLabel.int2str` can be used to convert from the label names to the associate integer value and vice-versa.

- finally, two features are specific to Machine Translation: :class:`datasets.Translation` and :class:`datasets.TranslationVariableLanguages`. We refer to the package reference for more details on these features.

