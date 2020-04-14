# Generating big datasets with Apache Beam

Some datasets are too big to be processed on a single machine. `tfds` supports
generating data across many machines by using
[Apache Beam](https://beam.apache.org/).

This doc has two sections:

*   For user who want to generate an existing Beam dataset
*   For developper who want to create a new Beam dataset

Table of content:

*   [Generating a Beam dataset](#generating-a-beam-dataset)
    *   [On Google Cloud Dataflow](#on-google-cloud-dataflow)
    *   [Locally](#locally)
    *   [Within a custom script](#with-a-custom-script)
*   [Implementing a Beam dataset](#implementing-a-beam-dataset)
    *   [Prerequisites](#prerequisites)
    *   [Instructions](#instructions)
    *   [Example](#example)
    *   [Run your pipeline](#run-your-pipeline)

## Generating a Beam dataset

Below are different examples of generating a Beam dataset, both on the cloud or
locally.

**Warning**: When generating the dataset with the
`tensorflow_datasets.scripts.download_and_prepare` script, make sure to specify
the dataset config you want to generate or it will default to generate all
existing configs. For example, for
[wikipedia](https://www.tensorflow.org/datasets/catalog/wikipedia), use
`--dataset=wikipedia/20190301.en` instead of `--dataset=wikipedia`.

### On Google Cloud Dataflow

To run the pipeline using
[Google Cloud Dataflow](https://cloud.google.com/dataflow/) and take advantage
of distributed computation, first follow the
[Quickstart instructions](https://cloud.google.com/dataflow/docs/quickstarts/quickstart-python).

Once your environment is set up, you can run the `download_and_prepare` script
using a data directory on [GCS](https://cloud.google.com/storage/) and
specifying the
[required options](https://cloud.google.com/dataflow/docs/guides/specifying-exec-params#configuring-pipelineoptions-for-execution-on-the-cloud-dataflow-service)
for the `--beam_pipeline_options` flag.

To make it easier to launch the script, it's helpful to define the following
variables using the actual values for your GCP/GCS setup and the dataset you
want to generate:

```sh
DATASET_NAME=<dataset>/<dataset-config>
GCP_PROJECT=my-project-id
GCS_BUCKET=gs://my-gcs-bucket
```

You will then need to create a file to tell Dataflow to install `tfds` on the
workers:

```sh
echo "tensorflow_datasets[$DATASET_NAME]" > /tmp/beam_requirements.txt
```

Finally, you can launch the job using the command below:

```sh
python -m tensorflow_datasets.scripts.download_and_prepare \
  --datasets=$DATASET_NAME \
  --data_dir=$GCS_BUCKET/tensorflow_datasets \
  --beam_pipeline_options=\
"runner=DataflowRunner,project=$GCP_PROJECT,job_name=$DATASET_NAME-gen,"\
"staging_location=$GCS_BUCKET/binaries,temp_location=$GCS_BUCKET/temp,"\
"requirements_file=/tmp/beam_requirements.txt"
```

### Locally

To run your script locally using the default Apache Beam runner, the command is
the same as for other datasets:

```sh
python -m tensorflow_datasets.scripts.download_and_prepare \
  --datasets=my_new_dataset
```

**Warning**: Beam datasets can be **huge** (TeraBytes) and take a significant
amount of ressources to be generated (can take weeks on a local computer). It is
recomended to generate the datasets using a distributed environement. Have a
look at the [Apache Beam Documentation](https://beam.apache.org/) for a list of
the supported runtimes.

### With a custom script

To generate the dataset on Beam, the API is the same as for other datasets, but
you have to pass the Beam options or runner to the `DownloadConfig`.

```py
# If you are running on Dataflow, Spark,..., you may have to set-up runtime
# flags. Otherwise, you can leave flags empty [].
flags = ['--runner=DataflowRunner', '--project=<project-name>', ...]

# To use Beam, you have to set at least one of `beam_options` or `beam_runner`
dl_config = tfds.download.DownloadConfig(
    beam_options=beam.options.pipeline_options.PipelineOptions(flags=flags)
)

data_dir = 'gs://my-gcs-bucket/tensorflow_datasets'
builder = tfds.builder('wikipedia/20190301.en', data_dir=data_dir)
builder.download_and_prepare(
    download_dir=FLAGS.download_dir,
    download_config=dl_config,
)
```

## Implementing a Beam dataset

### Prerequisites

In order to write Apache Beam datasets, you should be familiar with the
following concepts:

*   Be familiar with the
    [`tfds` dataset creation guide](https://github.com/tensorflow/datasets/tree/master/docs/add_dataset.md)
    as most of the content still applies for Beam datasets.
*   Get an introduction to Apache Beam with the
    [Beam programming guide](https://beam.apache.org/documentation/programming-guide/).
*   If you want to generate your dataset using Cloud Dataflow, read the
    [Google Cloud Documentation](https://cloud.google.com/dataflow/docs/quickstarts/quickstart-python)
    and the
    [Apache Beam dependency guide](https://beam.apache.org/documentation/sdks/python-pipeline-dependencies/).

### Instructions

If you are familiar with the
[dataset creation guide](https://github.com/tensorflow/datasets/tree/master/docs/add_dataset.md),
adding a Beam dataset only requires a few modifications:

*   Your `DatasetBuilder` will inherit from `tfds.core.BeamBasedBuilder` instead
    of `tfds.core.GeneratorBasedBuilder`.
*   Beam datasets should implement the abstract method `_build_pcollection(self,
    **kwargs)` instead of the method `_generate_examples(self, **kwargs)`.
    `_build_pcollection` should return a `beam.PCollection` with the examples
    associated with the split.
*   Writing a unit test for your Beam dataset is the same as with other
    datasets.

Some additional considerations:

*   Use `tfds.core.lazy_imports` to import Apache Beam. By using a lazy
    dependency, users can still read the dataset after it has been generated
    without having to install Beam.
*   Be careful with Python closures. When running the pipeline, the `beam.Map`
    and `beam.DoFn` functions are serialized using `pickle` and sent to all
    workers. This can create bugs; for instance, if you are using a mutable
    object in your functions which has been declared outside of the function,
    you may encounter `pickle` errors or unexpected behavior. The fix is
    typically to avoid mutating closed-over objects.
*   Using methods on `DatasetBuilder` in the Beam pipeline is fine. However,
    the way the class is serialized during pickle, changes done to features
    during creation will be ignored at best.

### Example

Here is an example of a Beam dataset. For a more complicated real example, have
a look at the
[`Wikipedia` dataset](https://github.com/tensorflow/datasets/tree/master/tensorflow_datasets/text/wikipedia.py).

```python
class DummyBeamDataset(tfds.core.BeamBasedBuilder):

  VERSION = tfds.core.Version('1.0.0')

  def _info(self):
    return tfds.core.DatasetInfo(
        builder=self,
        features=tfds.features.FeaturesDict({
            'image': tfds.features.Image(shape=(16, 16, 1)),
            'label': tfds.features.ClassLabel(names=['dog', 'cat']),
        }),
    )

  def _split_generators(self, dl_manager):
    ...
    return [
        tfds.core.SplitGenerator(
            name=tfds.Split.TRAIN,
            gen_kwargs=dict(file_dir='path/to/train_data/'),
        ),
        splits_lib.SplitGenerator(
            name=tfds.Split.TEST,
            gen_kwargs=dict(file_dir='path/to/test_data/'),
        ),
    ]

  def _build_pcollection(self, pipeline, file_dir):
    """Generate examples as dicts."""
    beam = tfds.core.lazy_imports.apache_beam

    def _process_example(filename):
      # Use filename as key
      return filename, {
          'image': os.path.join(file_dir, filename),
          'label': filename.split('.')[1],  # Extract label: "0010102.dog.jpeg"
      }

    return (
        pipeline
        | beam.Create(tf.io.gfile.listdir(file_dir))
        | beam.Map(_process_example)
    )

```

### Running your pipeline

To run the pipeline, have a look at the above section.

**Warning**: Do not forget to add the register checksums `--register_checksums`
flags to the `download_and_prepare` script when running the dataset the first
time to register the downloads.

```sh
python -m tensorflow_datasets.scripts.download_and_prepare \
  --register_checksums \
  --datasets=my_new_dataset
```
