# Splits and slicing

All `DatasetBuilder`s expose various data subsets defined as splits (eg:
`train`, `test`). When constructing a `tf.data.Dataset` instance using either
`tfds.load()` or `tfds.DatasetBuilder.as_dataset()`, one can specify which
split(s) to retrieve. It is also possible to retrieve slice(s) of split(s)
as well as combinations of those.

*   [Slicing API](#slicing-api)
    *   [Examples](#examples)
    *   [Percentage slicing and rounding](#percentage-slicing-and-rounding)
    *   [Reproducibility](#reproducibility)

## Slicing API

Slicing instructions are specified in `tfds.load` or `tfds.DatasetBuilder.as_dataset`.

Instructions can be provided as either strings or `ReadInstruction`s. Strings
are more compact and readable for simple cases, while `ReadInstruction`s provide
more options and might be easier to use with variable slicing parameters.

### Examples

Examples using the string API:

```py
# The full `train` split.
train_ds = tfds.load('mnist', split='train')

# The full `train` split and the full `test` split as two distinct datasets.
train_ds, test_ds = tfds.load('mnist', split=['train', 'test'])

# The full `train` and `test` splits, concatenated together.
train_test_ds = tfds.load('mnist', split='train+test')

# From record 10 (included) to record 20 (excluded) of `train` split.
train_10_20_ds = tfds.load('mnist', split='train[10:20]')

# The first 10% of train split.
train_10pct_ds = tfds.load('mnist', split='train[:10%]')

# The first 10% of train + the last 80% of train.
train_10_80pct_ds = tfds.load('mnist', split='train[:10%]+train[-80%:]')

# 10-fold cross-validation (see also next section on rounding behavior):
# The validation datasets are each going to be 10%:
# [0%:10%], [10%:20%], ..., [90%:100%].
# And the training datasets are each going to be the complementary 90%:
# [10%:100%] (for a corresponding validation set of [0%:10%]),
# [0%:10%] + [20%:100%] (for a validation set of [10%:20%]), ...,
# [0%:90%] (for a validation set of [90%:100%]).
vals_ds = tfds.load('mnist', split=[
    f'train[{k}%:{k+10}%]' for k in range(0, 100, 10)
])
trains_ds = tfds.load('mnist', split=[
    f'train[:{k}%]+train[{k+10}%:]' for k in range(0, 100, 10)
])
```

Examples using the `ReadInstruction` API (equivalent as above):

```py
# The full `train` split.
train_ds = tfds.load('mnist', split=tfds.core.ReadInstruction('train'))

# The full `train` split and the full `test` split as two distinct datasets.
train_ds, test_ds = tfds.load('mnist', split=[
    tfds.core.ReadInstruction('train'),
    tfds.core.ReadInstruction('test'),
])

# The full `train` and `test` splits, concatenated together.
ri = tfds.core.ReadInstruction('train') + tfds.core.ReadInstruction('test')
train_test_ds = tfds.load('mnist', split=ri)

# From record 10 (included) to record 20 (excluded) of `train` split.
train_10_20_ds = tfds.load('mnist', split=tfds.core.ReadInstruction(
    'train', from_=10, to=20, unit='abs'))

# The first 10% of train split.
train_10_20_ds = tfds.load('mnist', split=tfds.core.ReadInstruction(
    'train', to=10, unit='%'))

# The first 10% of train + the last 80% of train.
ri = (tfds.core.ReadInstruction('train', to=10, unit='%') +
      tfds.core.ReadInstruction('train', from_=-80, unit='%'))
train_10_80pct_ds = tfds.load('mnist', split=ri)

# 10-fold cross-validation (see also next section on rounding behavior):
# The validation datasets are each going to be 10%:
# [0%:10%], [10%:20%], ..., [90%:100%].
# And the training datasets are each going to be the complementary 90%:
# [10%:100%] (for a corresponding validation set of [0%:10%]),
# [0%:10%] + [20%:100%] (for a validation set of [10%:20%]), ...,
# [0%:90%] (for a validation set of [90%:100%]).
vals_ds = tfds.load('mnist', [
    tfds.core.ReadInstruction('train', from_=k, to=k+10, unit='%')
    for k in range(0, 100, 10)])
trains_ds = tfds.load('mnist', [
    (tfds.core.ReadInstruction('train', to=k, unit='%') +
     tfds.core.ReadInstruction('train', from_=k+10, unit='%'))
    for k in range(0, 100, 10)])
```

### Percentage slicing and rounding

If a slice of a split is requested using the percent (`%`) unit, and the
requested slice boundaries do not divide evenly by `100`, then the default
behaviour it to round boundaries to the nearest integer (`closest`). This means
that some slices may contain more examples than others. For example:

```py
# Assuming "train" split contains 101 records.
# 100 records, from 0 to 100.
tfds.load("mnist", split="test[:99%]")
# 2 records, from 49 to 51.
tfds.load("mnist", split="test[49%:50%]")
```

Alternatively, the user can use the rounding `pct1_dropremainder`, so specified
percentage boundaries are treated as multiples of 1%. This option should be used
when consistency is needed (eg: `len(5%) == 5 * len(1%)`).

Example:

```py
# Records 0 (included) to 99 (excluded).
tfds.load("mnist", split="test[:99%]", rounding="pct1_dropremainder")
```

### Reproducibility

The sub-split API guarantees that any given split slice (or `ReadInstruction`)
will always produce the same set of records on a given dataset, as long as the
major version of the dataset is constant.

For example, `tfds.load("mnist:3.0.0", split="train[10:20]")` and
`tfds.load("mnist:3.2.0", split="train[10:20]")` will always contain the same
elements - regardless of platform, architecture, etc. - even though some of
the records might have different values (eg: imgage encoding, label, ...).
