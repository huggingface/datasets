Adding a FAISS or Elastic Search index to a :class:`nlp.Dataset`
====================================================================


.. code-block::

    >>> len(mrpc)
    3668
    >>> mrpc[0]
    {'sentence1': 'Amrozi accused his brother , whom he called " the witness " , of deliberately distorting his evidence .', 'sentence2': 'Referring to him as only " the witness " , Amrozi accused his brother of deliberately distorting his evidence .', 'label': 1, 'idx': 0}
    >>> mrpc[:4]
    {'sentence1': ['Amrozi accused his brother , whom he called " the witness " , of deliberately distorting his evidence .', "Yucaipa owned Dominick 's before selling the chain to Safeway in 1998 for $ 2.5 billion .", 'They had published an advertisement on the Internet on June 10 , offering the cargo for sale , he added .', 'Around 0335 GMT , Tab shares were up 19 cents , or 4.4 % , at A $ 4.56 , having earlier set a record high of A $ 4.57 .'], 'sentence2': ['Referring to him as only " the witness " , Amrozi accused his brother of deliberately distorting his evidence .', "Yucaipa bought Dominick 's in 1995 for $ 693 million and sold it to Safeway for $ 1.8 billion in 1998 .", "On June 10 , the ship 's owners had published an advertisement on the Internet , offering the explosives for sale .", 'Tab shares jumped 20 cents , or 4.6 % , to set a record closing high at A $ 4.57 .'], 'label': [1, 0, 1, 0], 'idx': [0, 1, 2, 3]}
    >>> mrpc[[1, 2, 3]]
    {'sentence1': ["Yucaipa owned Dominick 's before selling the chain to Safeway in 1998 for $ 2.5 billion .", 'They had published an advertisement on the Internet on June 10 , offering the cargo for sale , he added .', 'Around 0335 GMT , Tab shares were up 19 cents , or 4.4 % , at A $ 4.56 , having earlier set a record high of A $ 4.57 .'], 'sentence2': ["Yucaipa bought Dominick 's in 1995 for $ 693 million and sold it to Safeway for $ 1.8 billion in 1998 .", "On June 10 , the ship 's owners had published an advertisement on the Internet , offering the explosives for sale .", 'Tab shares jumped 20 cents , or 4.6 % , to set a record closing high at A $ 4.57 .'], 'label': [0, 1, 0], 'idx': [1, 2, 3]}

The dataset is actually a table with columns. Columns are typed and you can query along columns by indexing with their names:

.. code-block::

    >>> print(mrpc)
    Dataset(schema: {'sentence1': 'string', 'sentence2': 'string', 'label': 'int64', 'idx': 'int32'}, num_rows: 3668)
    >>> mrpc['sentence1'][:5]
    ['Amrozi accused his brother , whom he called " the witness " , of deliberately distorting his evidence .', "Yucaipa owned Dominick 's before selling the chain to Safeway in 1998 for $ 2.5 billion .", 'They had published an advertisement on the Internet on June 10 , offering the cargo for sale , he added .', 'Around 0335 GMT , Tab shares were up 19 cents , or 4.4 % , at A $ 4.56 , having earlier set a record high of A $ 4.57 .', 'The stock rose $ 2.11 , or about 11 percent , to close Friday at $ 21.51 on the New York Stock Exchange .']

.. note::

    The :func:`nlp.Dataset.__getitem__` method will return a different format depending on the key you give it:

    - Single example are accessed using integer like :obj:`dataset[0]` and are returned as dict of values.
    - Batches of examples are accessed using slices or lists of integers like :obj:`dataset[10:20]` or :obj:`dataset[[1, 5, 10]]` are returned as dict of lists of values.
    - Columns are accessed using column names as string like `dataset['sentence1']` are returned as a list of values.

    This may seems surprising at first but in our experiments it's actually a lot easier to use for data processing than returning the same format for each of these views on the dataset.

