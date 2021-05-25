Splits and slicing
===========================

Similarly to Tensorfow Datasets, all :class:`DatasetBuilder` s expose various data subsets defined as splits (eg:
``train``, ``test``). When constructing a :class:`datasets.Dataset` instance using either
:func:`datasets.load_dataset()` or :func:`datasets.DatasetBuilder.as_dataset()`, one can specify which
split(s) to retrieve. It is also possible to retrieve slice(s) of split(s)
as well as combinations of those.

Slicing API
---------------------------------------------------

Slicing instructions are specified in :obj:`datasets.load_dataset` or :obj:`datasets.DatasetBuilder.as_dataset`.

Instructions can be provided as either strings or :obj:`ReadInstruction`. Strings
are more compact and readable for simple cases, while :obj:`ReadInstruction` 
might be easier to use with variable slicing parameters.

Examples
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Examples using the string API:

.. code-block::

    # The full `train` split.
    train_ds = datasets.load_dataset('bookcorpus', split='train')

    # The full `train` split and the full `test` split as two distinct datasets.
    train_ds, test_ds = datasets.load_dataset('bookcorpus', split=['train', 'test'])

    # The full `train` and `test` splits, concatenated together.
    train_test_ds = datasets.load_dataset('bookcorpus', split='train+test')

    # From record 10 (included) to record 20 (excluded) of `train` split.
    train_10_20_ds = datasets.load_dataset('bookcorpus', split='train[10:20]')

    # The first 10% of `train` split.
    train_10pct_ds = datasets.load_dataset('bookcorpus', split='train[:10%]')

    # The first 10% of `train` + the last 80% of `train`.
    train_10_80pct_ds = datasets.load_dataset('bookcorpus', split='train[:10%]+train[-80%:]')

    # 10-fold cross-validation (see also next section on rounding behavior):
    # The validation datasets are each going to be 10%:
    # [0%:10%], [10%:20%], ..., [90%:100%].
    # And the training datasets are each going to be the complementary 90%:
    # [10%:100%] (for a corresponding validation set of [0%:10%]),
    # [0%:10%] + [20%:100%] (for a validation set of [10%:20%]), ...,
    # [0%:90%] (for a validation set of [90%:100%]).
    vals_ds = datasets.load_dataset('bookcorpus', split=[
        f'train[{k}%:{k+10}%]' for k in range(0, 100, 10)
    ])
    trains_ds = datasets.load_dataset('bookcorpus', split=[
        f'train[:{k}%]+train[{k+10}%:]' for k in range(0, 100, 10)
    ])


Examples using the ``ReadInstruction`` API (equivalent as above):

.. code-block::

    # The full `train` split.
    train_ds = datasets.load_dataset('bookcorpus', split=datasets.ReadInstruction('train'))

    # The full `train` split and the full `test` split as two distinct datasets.
    train_ds, test_ds = datasets.load_dataset('bookcorpus', split=[
        datasets.ReadInstruction('train'),
        datasets.ReadInstruction('test'),
    ])

    # The full `train` and `test` splits, concatenated together.
    ri = datasets.ReadInstruction('train') + datasets.ReadInstruction('test')
    train_test_ds = datasets.load_dataset('bookcorpus', split=ri)

    # From record 10 (included) to record 20 (excluded) of `train` split.
    train_10_20_ds = datasets.load_dataset('bookcorpus', split=datasets.ReadInstruction(
        'train', from_=10, to=20, unit='abs'))

    # The first 10% of `train` split.
    train_10_20_ds = datasets.load_dataset('bookcorpus', split=datasets.ReadInstruction(
        'train', to=10, unit='%'))

    # The first 10% of `train` + the last 80% of `train`.
    ri = (datasets.ReadInstruction('train', to=10, unit='%') +
        datasets.ReadInstruction('train', from_=-80, unit='%'))
    train_10_80pct_ds = datasets.load_dataset('bookcorpus', split=ri)

    # 10-fold cross-validation (see also next section on rounding behavior):
    # The validation datasets are each going to be 10%:
    # [0%:10%], [10%:20%], ..., [90%:100%].
    # And the training datasets are each going to be the complementary 90%:
    # [10%:100%] (for a corresponding validation set of [0%:10%]),
    # [0%:10%] + [20%:100%] (for a validation set of [10%:20%]), ...,
    # [0%:90%] (for a validation set of [90%:100%]).
    vals_ds = datasets.load_dataset('bookcorpus', [
        datasets.ReadInstruction('train', from_=k, to=k+10, unit='%')
        for k in range(0, 100, 10)])
    trains_ds = datasets.load_dataset('bookcorpus', [
        (datasets.ReadInstruction('train', to=k, unit='%') +
        datasets.ReadInstruction('train', from_=k+10, unit='%'))
        for k in range(0, 100, 10)])

Percent slicing and rounding
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If a slice of a split is requested using the percent (``%``) unit, and the
requested slice boundaries do not divide evenly by 100, then the default
behaviour is to round boundaries to the nearest integer (``closest``). This means
that some slices may contain more examples than others. For example:

.. code-block::

    # Assuming `train` split contains 999 records.
    # 19 records, from 500 (included) to 519 (excluded).
    train_50_52_ds = datasets.load_dataset('bookcorpus', split='train[50%:52%]')
    # 20 records, from 519 (included) to 539 (excluded).
    train_52_54_ds = datasets.load_dataset('bookcorpus', split='train[52%:54%]')

Alternatively, the ``pct1_dropremainder`` rounding can be used, so specified
percentage boundaries are treated as multiples of 1%. This option should be used
when consistency is needed (eg: ``len(5%) == 5 * len(1%)``). This means the last
examples may be truncated if ``info.splits[split_name].num_examples % 100 != 0``.

.. code-block::

    # 18 records, from 450 (included) to 468 (excluded).
    train_50_52pct1_ds = datasets.load_dataset('bookcorpus', split=datasets.ReadInstruction(
        'train', from_=50, to=52, unit='%', rounding='pct1_dropremainder'))
    # 18 records, from 468 (included) to 486 (excluded).
    train_52_54pct1_ds = datasets.load_dataset('bookcorpus', split=datasets.ReadInstruction(
        'train', from_=52, to=54, unit='%', rounding='pct1_dropremainder'))
    # Or equivalently:
    train_50_52pct1_ds = datasets.load_dataset('bookcorpus', split='train[50%:52%](pct1_dropremainder)')
    train_52_54pct1_ds = datasets.load_dataset('bookcorpus', split='train[52%:54%](pct1_dropremainder)')
