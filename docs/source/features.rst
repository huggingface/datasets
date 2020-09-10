Dataset features
===========================

:class:`datasets.Features` define the internal structure and typings for each example in the dataset. Features are used to specify the underlying serailization format but also contain high-level informations regarding the fields, e.g. conversion methods from names to integer values for a class label field.

Here is a brief presentation of the various types of features which can be used to define the dataset fields (aka columns):

- :class:`datasets.Features` is the base class and should be only called once and instantiated with a dictionary of field names and field sub-features as detailed in the rest of this list,
- a python :obj:`dict` specifies that the field is a nested field containing a mapping of sub-fields to sub-fields features. It's possible to have nested fields of nested fields in an arbitrary manner.
- a python :obj:`list` or a :class:`datasets.Sequence` specifies that the field contains a list of objects. The python :obj:`list` or :class:`datasets.Sequence` should be provided with a single sub-feature as an example of the feature type hosted in this list. Python :obj:`list` are simplest to define and write while :class:`datasets.Sequence` provide a few more specific behaviors like the possibility to specify a fixed length for the list (slightly more efficient).

.. note::

	A :class:`datasets.Sequence` with a internal dictionary feature will be automatically converted into a dictionary of lists. This behavior is implemented to have a compatilbity layer with the TensorFlow Datasets library but may be un-wanted in some cases. If you don't want this behavior, you can use a python :obj:`list` instead of the :class:`datasets.Sequence`.

- a :class:`datasets.ClassLabel` feature specifies a field with a predefined set of classes which can have labels associated to them and will be stored as integers in the dataset. This field will be stored and retrieved as an integer value and two conversion methods, :func:`datasets.ClassLabel.str2int` and :func:`datasets.ClassLabel.int2str` can be used to convert from the label names to the associate integer value and vice-versa.

- a :class:`datasets.Value` feature specifies a single typed value, e.g. ``int64`` or ``string``. The types supported are all the `non-nested types of Apache Arrow <https://arrow.apache.org/docs/python/api/datatypes.html#factory-functions>`__ among which the most commonly used ones are ``int64``, ``float32`` and ``string``.

- finally, two features are specific to Machine Translation: :class:`datasets.Translation` and :class:`datasets.TranslationVariableLanguages`. We refer to the package reference for more details on these features.

