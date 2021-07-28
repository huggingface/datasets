Batch mapping
=============

Combining the utility of :func:`datasets.Dataset.map` with batch mode is very powerful because it allows you to freely control the size of the generated dataset. You can get creative with this, and take advantage of it for many interesting use-cases. In the Map section of the :doc:`How-to Process <./process>` guides, there are some examples of using :func:`datasets.Dataset.map` in batched mode to:

* split long sentences into shorter chunks
* augment the dataset with additional tokens

It will be helpful to understand how this works, so you can come up with your own ways of using :func:`datasets.Dataset.map` in batched mode.

Input size != output size
-------------------------

You may be wondering how you can control the size of the generated dataset. The answer is:

✨ The mapped function accepts a batch of inputs, but the output batch is not required to be the same size. ✨

In other words, your input can be a batch of size ``N`` and return a batch of size ``M`` which can be greater or less than ``N``. This means you can concatenate your examples, divide it up, and even add more examples!

However, you need to remember that each field in the output dictionary must contain the **same number of elements** as the other field in the output dictionary. Otherwise, it is not possible to define the number of examples in the output returned by the mapped function. This number can vary between successive batches processed by the mapped function. For a single batch though, all fields of the output dictionary should have the same number of elements.

TO DO:

Maybe add a code example of when the number of elements in the field of an output dictionary aren't the same, so the user knows what not to do.

