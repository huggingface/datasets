# Datasets versioning

*  [Semantic](#semantic)
*  [Supported versions](#supported-versions)
*  [Loading a specific version](#loading-a-specific-version)
*  [Experiments](#experiments)
*  [BUILDER_CONFIGS and versions](#builder-configs-and-versions)

## Semantic

Every `DatasetBuilder` defined in TFDS comes with a version, for example:

```py
class MNIST(tfds.core.GeneratorBasedBuilder):
  VERSION = tfds.core.Version("1.0.0")
```

The version follows
[Semantic Versioning 2.0.0](https://semver.org/spec/v2.0.0.html):
`MAJOR.MINOR.PATCH`. The purpose of the version is to be able to guarantee
reproducibility: loading a given dataset at a fixed version yields the same
data. More specifically:

 - If `PATCH` version is incremented, data as read by the client is the same,
 although data might be serialized differently on disk, or the metadata might
 have changed. For any given slice, the slicing API returns the same set of
 records.
 - If `MINOR` version is incremented, existing data as read by the client is the
 same, but there is additional data (features in each record). For any given
 slice, the  slicing API returns the same set of records.
 - If `MAJOR` version is incremented, the existing data has been changed and/or
 the slicing API doesn't necessarily return the same set of records for a given
 slice.

When a code change is made to the TFDS library and that code change impacts the
way a dataset is being serialized and/or read by the client, then the
corresponding builder version is incremented according to the above guidelines.

Note that the above semantic is best effort, and there might be un-noticed bugs
impacting a dataset while the version was not incremented. Such bugs are
eventually fixed, but if you heavily rely on the versioning, we advise you to
use TFDS from a released version (as opposed to `HEAD`).

Also note that some datasets have another versioning scheme independent from
the TFDS version. For example, the Open Images dataset has several versions,
and in TFDS, the corresponding builders are `open_images_v4`, `open_images_v5`,
...

## Supported versions

A `DatasetBuilder` can support several versions, which can be both higher or
lower than the canonical version. For example:

```py
class Imagenet2012(tfds.core.GeneratorBasedBuilder):
  VERSION = tfds.core.Version('2.0.1', 'Encoding fix. No changes from user POV')
  SUPPORTED_VERSIONS = [
      tfds.core.Version('3.0.0', 'S3: tensorflow.org/datasets/splits'),
      tfds.core.Version('1.0.0'),
      tfds.core.Version('0.0.9', tfds_version_to_prepare="v1.0.0"),
  ]
```

The choice to continue supporting an older version is done on a case-by-case
basis, mainly based on the popularity of the dataset and version. Eventually, we
aim at only supporting a limited number versions per dataset, ideally one. In
the above example, we can see that version `2.0.0` is not supported anymore, as
identical to `2.0.1` from a reader perspective.

Supported versions with a higher number than the canonical version number are
considered experimental and might be broken. They will however eventually be
made canonical.

A version can specify `tfds_version_to_prepare`. This means this dataset version
can only be used with current version of TFDS code if it has already been
prepared by an older version of the code, but cannot be prepared. The
value of `tfds_version_to_prepare` specifies the last known version of TFDS
which can be used to download and prepare the dataset at this version.

## Loading a specific version

When loading a dataset or a `DatasetBuilder`, you can specify the version to
use. For example:

```py
tfds.load('imagenet2012:2.0.1')
tfds.builder('imagenet2012:2.0.1')

tfds.load('imagenet2012:2.0.0')  # Error: unsupported version.

# Resolves to 3.0.0 for now, but would resolve to 3.1.1 if when added.
tfds.load('imagenet2012:3.*.*')
```

If using TFDS for a publication, we advise you to:

 - **fix the `MAJOR` component of the version only**;
 - **advertise which version of the dataset was used in your results.**

Doing so should make it easier for your future self, your readers and
reviewers to reproduce your results.

## Experiments

To gradually roll out changes in TFDS which are impacting many dataset builders,
we introduced the notion of experiments. When first introduced, an experiment
is disabled by default, but specific dataset versions can decide to enable it.
This will typically be done on "future" versions (not made canonical yet) at
first. For example:

```py
class MNIST(tfds.core.GeneratorBasedBuilder):
  VERSION = tfds.core.Version("1.0.0")
  SUPPORTED_VERSIONS = [
      tfds.core.Version("2.0.0", "S3: tensorflow.org/datasets/splits",
                        experiments={tfds.core.Experiment.S3: True}),
  ]
```

Once an experiment has been verified to work as expected, it will be extended to
all or most datasets, at which point it can be enabled by default, and the above
definition would then look like:

```py
class MNIST(tfds.core.GeneratorBasedBuilder):
  VERSION = tfds.core.Version("1.0.0",
                              experiments={tfds.core.Experiment.S3: False})
  SUPPORTED_VERSIONS = [
      tfds.core.Version("2.0.0", "S3: tensorflow.org/datasets/splits"),
  ]
```

Once an experiment is used across all datasets versions (there is no dataset
version left specifying `{experiment: False}`), the experiment can be deleted.

Experiments and their description are defined in `core/utils/version.py`.

## BUILDER_CONFIGS and versions

Some datasets define several `BUILDER_CONFIGS`. When that is the case, `version`
and `supported_versions` are defined on the config objects themselves. Other
than that, semantics and usage are identical. For example:

```py
class OpenImagesV4(tfds.core.GeneratorBasedBuilder):

  BUILDER_CONFIGS = [
      OpenImagesV4Config(
          name='original',
          version=tfds.core.Version('0.2.0'),
          supported_versions=[
            tfds.core.Version('1.0.0', "Major change in data"),
          ],
          description='Images at their original resolution and quality.'),
      ...
  ]

tfds.load('open_images_v4/original:1.*.*')
```
