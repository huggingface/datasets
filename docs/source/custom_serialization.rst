Custom serialization functions
==============================

When you process a dataset with methods such as :func:`datasets.Dataset.map` or :func:`datasets.Dataset.filter`, it
fingerprints that process. ``datasets`` serializes (*pickles*) the objects that are related to the mapping or filtering
function, and generates a unique fingerprint for that specific serialization. The consequence is that every different
processing function will have a distinct fingerprint. This allows the library to use a very effective caching mechanic:
if you process a dataset in the exact same way as you have already done before, it will find that that unique
fingerprint already exists in cache. It can then simply retrieve the processed dataset from cache instead of running
the, potentially expensive, preprocessing process again.

In most cases, this works really well out of the box! However, sometimes you may find that your tedious data-crunching
functions are running every time instead of being loaded from cache. This means that there is an object that is part of
your processing function whose serialization is different on every run. Consequently, the fingerprint will also be
different and ``datasets`` thinks it is a different processing function altogether. This is particularly likely to
happen with complex, deep objects or third-party libraries. Luckily, it is possible to register your own serialization
methods for specific objects to ensure deterministic serialization!

Register your own serialization function
----------------------------------------

In this section we will go over an example on how to register your own serialization function. We will use the popular linguistic parser `spaCy <https://spacy.io/>`_ as an example.

In the following snippet, we load up a large text file with plain text. We would like to tokenize the text with spaCy. We can easily do this with ``datasets`` by running our tokenization function in :func:`map()` on our dataset.

.. code-block::

    >>> input_file = /your/large/text/file.txt
    >>> # Load the spaCy parser
    >>> nlp = spacy.load("en_core_web_sm", disable=["parser", "tagger", "ner", "lemmatizer"])

    >>> # Batch-processing with spaCy's nlp.pipe() is fast!
    >>> def tokenize(batch):
    >>>     return {"tokenized": [" ".join([t.text for t in doc])
    >>>                           for doc in nlp.pipe(batch["text"])]}

    >>> # Load our text file as a Dataset
    >>> ds = load_dataset("text", data_files=input_file)
    >>> # Tokenize batches of data efficiently
    >>> ds = ds["train"].map(tokenize, batched=True, batch_size=128)

This works great out of the box and provides us with a dataset with two columns: ``text`` and ``tokenized``, exactly
was we wanted! However, when you run this exact code again you will notice that the tokenization step was not cached
and that the whole dataset needs to be processed again! This happens because of the reason described above: some
underlying object in spaCy is not deterministic across runs, so the caching system thinks this is a completely
different function.

.. tip::

    As a rule of thumb when debugging behavior like above: read the documentation of the libraries that you are using
    - they may provide useful background on how they save/load and serialize their own objects!

In the spaCy documentation we find that it has `built-in serialization methods <https://spacy.io/usage/saving-loading#pipeline>`_
that are preferred over other means of automatic serialization, like the one that we use in ``datasets`` (``dill``).
Specifically, they use a custom method to convert their pipeline to a deterministic bytes-object with ``nlp.to_bytes()``.
So, ultimately what we would like is to tell ``datasets`` that whenever it encounters an object of the type like ``nlp``
(``English``, in this case), to use the built-in serialization method of spaCy before using our own to ensure that
the serialization process is deterministic.

To this end, we can *register* a function to a type with the decorator :func:`datasets.utils.py_utils.pklregister`.
This is relatively easy and straightforward and does not require other changes to our code above.

.. code-block::

    >>> # We only need to add this part
    >>> @pklregister(English)
    >>> def pickle_spacy_language(pickler, nlp: English):
    >>>     # Instead of pickler.save(nlp) (default, but not deterministic):
    >>>     pickler.save(nlp.to_bytes())

    >>> # Same as above...
    >>> input_file = /your/large/text/file.txt
    >>> # Load the spaCy parser
    >>> nlp = spacy.load("en_core_web_sm", disable=["parser", "tagger", "ner", "lemmatizer"])

    >>> # Batch-processing with spaCy's nlp.pipe() is fast!
    >>> def tokenize(batch):
    >>>     return {"tokenized": [" ".join([t.text for t in doc])
    >>>                           for doc in nlp.pipe(batch["text"])]}

    >>> # Load our text file as a Dataset
    >>> ds = load_dataset("text", data_files=input_file)
    >>> # Tokenize batches of data efficiently
    >>> ds = ds["train"].map(tokenize, batched=True, batch_size=128)

If you run this code twice, you'll find that the second run retireves the cached dataset successfully! The registered
function above tells ``datasets`` that when it encounters an object of type ``English``, it should not try to
pickle (serialize) this with the default method (``pickler.save(nlp)``) because we know that that is not deterministic
and will lead to problems during caching, as illustrated above. Instead it should first use spaCy's built-in
:func:`to_bytes` method and then :func:`pickler.save` the result.

.. caution::

    Do not forget :func:`pickler.save` in your custom functions! Depending on your exact use-case and objects,
    this is a crucial part of creating unique, and deterministic, serialized objects.


Registering functions for sub-classes
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

TODO

Temporarily using a user-defined serialization function
-------------------------------------------------------

TODO
