Adding a FAISS or Elastic Search index to a Dataset
====================================================================

It can be interesting to do documents retrieval in a dataset.

For example, one way to do Open Domain Question Answering, one way to do that is to first retrieve documents that may be relevant to answer a question, and then we can use a model to generate an answer given the retrieved documents.

FAISS is a library for dense retrieval. It means that it retrieves documents based on their vector representations, by doing a nearest neighbors search.
As we now have models that can have good semantic vectorized representations of documents, this has become an interesting tool for document retrieval.

On the other hand there exist other tools like ElasticSearch for exact match retrieval in texts (sparse retrieval).

Both FAISS and ElasticSearch can be used in :class:`nlp.Dataset`, using these methods:

- :func:`nlp.Dataset.add_faiss_index` to add a FAISS index
- :func:`nlp.Dataset.add_elasticsearch_index` to add an ElasticSearch index

.. note::

    One :class:`nlp.Dataset` can have several indexes, each identified by its :obj:`index_name`. By default it corresponds to the name of the column used to build the index.

Then as soon as you have your index you can query it using these methods:

- :func:`nlp.Dataset.search` to retrieve the scores and the ids of the examples. There is a version to do batched queries: :func:`nlp.Dataset.search_batch`.
- :func:`nlp.Dataset.get_nearest_examples` to retrieve the scores and the content of the examples. There is a version to do batched queries: :func:`nlp.Dataset.get_nearest_examples_batch`.

Adding a FAISS index
----------------------------------

The :func:`nlp.Dataset.add_faiss_index` method is in charge of building, training and adding vectors to a FAISS index.

One way to get good vector representations for text passages is to use the DPR model. We'll compute the representations of only 100 examples just to give you the idea of how it works.

.. code-block::

    >>> from transformers import DPRContextEncoder, DPRContextEncoderTokenizer
    >>> import torch
    >>> torch.set_grad_enabled(False)
    >>> ctx_encoder = DPRContextEncoder.from_pretrained("facebook/dpr-ctx_encoder-single-nq-base")
    >>> ctx_tokenizer = DPRContextEncoderTokenizer.from_pretrained("facebook/dpr-ctx_encoder-single-nq-base")

Then you can load your dataset and compute the representations:

.. code-block::

    >>> from nlp import load_dataset
    >>> ds = load_dataset('crime_and_punish', split='train[:100]')
    >>> ds_with_embeddings = ds.map(lambda example: {'embeddings': ctx_encoder(**ctx_tokenizer(example["line"], return_tensors="pt"))[0][0].numpy()})

We can create the index:

.. code-block::

    >>> ds_with_embeddings.add_faiss_index(column='embeddings')

Now have an index named 'embeddings' that we can query. Let's load the question encoder from DPR to have vector representations of questions.

.. code-block::

    >>> from transformers import DPRQuestionEncoder, DPRQuestionEncoderTokenizer
    >>> q_encoder = DPRQuestionEncoder.from_pretrained("facebook/dpr-question_encoder-single-nq-base")
    >>> q_tokenizer = DPRQuestionEncoderTokenizer.from_pretrained("facebook/dpr-question_encoder-single-nq-base")

.. code-block::

    >>> question = "Is it serious ?" 
    >>> question_embedding = q_encoder(**q_tokenizer(question, return_tensors="pt"))[0][0].numpy()
    >>> scores, retrieved_examples = ds_with_embeddings.get_nearest_examples('embeddings', question_embedding, k=10)
    >>> retrieved_examples["line"][0]
    '_that_ serious? It is not serious at all. It’s simply a fantasy to amuse\r\n'


When you are done with your queries you can save your index on disk:

.. code-block::

    ds_with_embeddings.save_faiss_index('embeddings', 'my_index.faiss')

And reload it later:

.. code-block::

    >>> ds = load_dataset('crime_and_punish', split='train[:100]')
    >>> ds.load_faiss_index('embeddings', 'my_index.faiss')


Adding an ElasticSearch index
----------------------------------

[UNDER CONSTRUCTION]
