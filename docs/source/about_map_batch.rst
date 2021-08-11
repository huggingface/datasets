Batch mapping
=============

Combining the utility of :func:`datasets.Dataset.map` with batch mode is very powerful. It allows you to speed up processing, and freely control the size of the generated dataset. 

Need for speed
--------------

The primary objective of batch mapping is to speed up processing. Often times, it is faster to work with batches of data instead of single examples. Naturally, batch mapping lends itself to tokenization. For example, the 🤗 `Tokenizers <https://huggingface.co/docs/tokenizers/python/latest/>`_ library works faster with batches because it parallelizes the tokenization of all the examples in a batch.

Input size != output size
-------------------------

The ability to control the generated dataset size can be taken advantage of for many interesting use-cases. In the How-to :ref:`map` section, there are examples of using batch mapping to:

* Split long sentences into shorter chunks.
* Augment a dataset with additional tokens.

It is helpful to understand how this works, so you can come up with your own ways to use batch mapping. At this point, you may be wondering how you can control the size of the generated dataset. The answer is: **the mapped function does not have to return an output batch of the same size**.

In other words, your input can be a batch of size ``N`` and return a batch of size ``M``. The output ``M`` can be greater than or less than ``N``. This means you can concatenate your examples, divide it up, and even add more examples!

However, you need to remember that each field in the output dictionary must contain the **same number of elements** as the other fields in the output dictionary. Otherwise, it is not possible to define the number of examples in the output returned by the mapped function. The number can vary between successive batches processed by the mapped function. For a single batch though, all fields of the output dictionary should have the same number of elements.

TO DO:

Maybe add a code example of when the number of elements in the field of an output dictionary aren't the same, so the user knows what not to do.

