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
are more compact and readable for simple cases, while :obj:`ReadInstruction` provide
more options and might be easier to use with variable slicing parameters.

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

    # The first 10% of train split.
    train_10pct_ds = datasets.load_dataset('bookcorpus', split='train[:10%]')

    # The first 10% of train + the last 80% of train.
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

    # The first 10% of train split.
    train_10_20_ds = datasets.load_dataset('bookcorpus', split=datasets.ReadInstruction(
        'train', to=10, unit='%'))

    # The first 10% of train + the last 80% of train.
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
