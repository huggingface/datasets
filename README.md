# HuggingFace Datasets

API proposal

```python
import datasets

dataset = datasets.load('squad')

print(dataset[0]). # Behave like a list - under the hook it's zero-copy reading from the disk
>>> {"id": "00990",
     "question": "Where is Boddy?",
     "context": "Bobby was at the beach",
     "answers": [{"text": "at the beach", "answer_start": 10}]
    }

# This dataset (SQuAD) is provided as just text data
# Let's encode it in model inputs
# We supply an encode examples or encode batch method
from transformers import BertTokenizer
tokenizer = BertTokenizer.from_pretrained('bert-base-cased')
def encode_example(example):
    encoding = tokenizer.encode_plus(example.context,
                                     example.question,
                                     return_tensors='pt')
    start_span = 
    end_span = 
    return dict(**encodings, {'start_span': start_span, 'end_span': end_span})

dataset.map_examples(encode_example)  # Lazy map
dataset.save('./data_cache')  # Caching on drive

dataset.get_torch_dataloader()  # Get a dataloader

# This download the dataset processing script
dataset_builder = datasets.builder('squad')
# This download the datasets files and preprocess them
dataset_builder.download_and_prepare()
# Then three options to access:
tf_dataset = dataset_builder.as_tf_dataset()  # Gives a TF Dataset (which is a PT Dataloader)
torch_dataset = dataset_builder.as_torch_dataset()
torch_dataloader = dataset_builder.as_torch_dataloader()

print(dataset[0])
>>> {"id": "00990",
     "question": "Where is Boddy?",
     "context": "Bobby was at the beach",
     "answers": [{"text": "at the beach", "answer_start": 10}]
    }

dataset.as_dataset()
```





# TensorFlow Datasets

TensorFlow Datasets provides many public datasets as `tf.data.Datasets`.

[![Kokoro](https://storage.googleapis.com/tfds-kokoro-public/kokoro-build.svg)](https://storage.googleapis.com/tfds-kokoro-public/kokoro-build.html)
[![PyPI version](https://badge.fury.io/py/tensorflow-datasets.svg)](https://badge.fury.io/py/tensorflow-datasets)

* [List of datasets](https://www.tensorflow.org/datasets/catalog/overview)
* Getting started:
  * [Introduction](https://www.tensorflow.org/datasets/overview) ([Try it in Colab](https://colab.research.google.com/github/tensorflow/datasets/blob/master/docs/overview.ipynb))
  * [End-to-end example with Keras](https://colab.research.google.com/github/tensorflow/datasets/blob/master/docs/keras_example.ipynb)
* Features & performances:
  * [Using splits and slicing API](https://www.tensorflow.org/datasets/splits)
  * [Performance advice](https://www.tensorflow.org/datasets/performances)
  * [Datasets versioning](https://www.tensorflow.org/datasets/datasets_versioning)
  * [Feature decoding](https://www.tensorflow.org/datasets/decode)
  * [Store your dataset on GCS](https://www.tensorflow.org/datasets/gcs)
* Add your dataset:
  * [Add a dataset](https://www.tensorflow.org/datasets/add_dataset)
  * [Add a huge dataset with Beam (>>100GiB)](https://www.tensorflow.org/datasets/beam_datasets)
* [API docs](https://www.tensorflow.org/datasets/api_docs/python/tfds)

Note: [`tf.data`](https://www.tensorflow.org/guide/data) is a builtin library in
TensorFlow which builds efficient data pipelines.
[TFDS](https://www.tensorflow.org/datasets) (this library) uses `tf.data` to
build an input pipeline when you load a dataset.

**Table of Contents**

* [Installation](#installation)
* [Usage](#usage)
* [`DatasetBuilder`](#datasetbuilder)
* [NumPy usage with `tfds.as_numpy`](#numpy-usage-with-tfdsasnumpy)
* [Citation](#citation)
* [Want a certain dataset?](#want-a-certain-dataset)
* [*Disclaimers*](#disclaimers)

### Installation

```sh
pip install tensorflow-datasets

# Requires TF 1.5+ to be installed.
# Some datasets require additional libraries; see setup.py extras_require
pip install tensorflow
# or:
pip install tensorflow-gpu
```

Join [our Google group](https://groups.google.com/forum/#!forum/tensorflow-datasets-public-announce)
to receive updates on the project.

### Usage

```python
import tensorflow_datasets as tfds
import tensorflow as tf

# Here we assume Eager mode is enabled (TF2), but tfds also works in Graph mode.

# Construct a tf.data.Dataset` or `torch.utils.data.DataLoader
ds_train = tfds.load('mnist', split='train', shuffle_files=True)

# Build your input pipeline
ds_train = ds_train.shuffle(1000).batch(128).prefetch(10)
for features in ds_train.take(1):
  image, label = features['image'], features['label']
```

Try it interactively in a
[Colab notebook](https://colab.research.google.com/github/tensorflow/datasets/blob/master/docs/overview.ipynb).

### `DatasetBuilder`

All datasets are implemented as subclasses of `tfds.core.DatasetBuilder`. TFDS
has two entry points:

*   `tfds.builder`: Returns the `tfds.core.DatasetBuilder` instance, giving
     control over `builder.download_and_prepare()` and
     `builder.as_dataset()`.
*   `tfds.load`: Convenience wrapper which hides the `download_and_prepare` and
    `as_dataset` calls, and directly returns the `tf.data.Dataset` or `torch.utils.data.DataLoader`.

```python
import tensorflow_datasets as tfds

# The following is the equivalent of the `load` call above.

# You can fetch the DatasetBuilder class by string
mnist_builder = tfds.builder('mnist')

# Download the dataset
mnist_builder.download_and_prepare()

# Construct a tf.data.Dataset` or `torch.utils.data.DataLoader
ds = mnist_builder.as_dataset(split='train')

# Get the `DatasetInfo` object, which contains useful information about the
# dataset and its features
info = mnist_builder.info
print(info)
```

This will print the dataset info content:

```
tfds.core.DatasetInfo(
    name='mnist',
    version=1.0.0,
    description='The MNIST database of handwritten digits.',
    homepage='http://yann.lecun.com/exdb/mnist/',
    features=FeaturesDict({
        'image': Image(shape=(28, 28, 1), dtype=tf.uint8),
        'label': ClassLabel(shape=(), dtype=tf.int64, num_classes=10)
    },
    total_num_examples=70000,
    splits={
        'test': <tfds.core.SplitInfo num_examples=10000>,
        'train': <tfds.core.SplitInfo num_examples=60000>
    },
    supervised_keys=('image', 'label'),
    citation='"""
        @article{lecun2010mnist,
          title={MNIST handwritten digit database},
          author={LeCun, Yann and Cortes, Corinna and Burges, CJ},
          journal={ATT Labs [Online]. Available: http://yann.lecun.com/exdb/mnist},
          volume={2},
          year={2010}
        }
    """',
)
```

You can also get details about the classes (number of classes and their names).

```python
info = tfds.builder('cats_vs_dogs').info

info.features['label'].num_classes  # 2
info.features['label'].names  # ['cat', 'dog']
info.features['label'].int2str(1)  # "dog"
info.features['label'].str2int('cat')  # 0
```

### NumPy Usage with `tfds.as_numpy`

As a convenience for users that want simple NumPy arrays in their programs, you
can use `tfds.as_numpy` to return a generator that yields NumPy array
records out of a `tf.data.Dataset` or `torch.utils.data.DataLoader`. This allows you to build high-performance
input pipelines with `tf.data` but use whatever you'd like for your model
components.

```python
train_ds = tfds.load("mnist", split="train")
train_ds = train_ds.shuffle(1024).batch(128).repeat(5).prefetch(10)
for example in tfds.as_numpy(train_ds):
  numpy_images, numpy_labels = example["image"], example["label"]
```

You can also use `tfds.as_numpy` in conjunction with `batch_size=-1` to
get the full dataset in NumPy arrays from the returned `tf.Tensor` object:

```python
train_ds = tfds.load("mnist", split=tfds.Split.TRAIN, batch_size=-1)
numpy_ds = tfds.as_numpy(train_ds)
numpy_images, numpy_labels = numpy_ds["image"], numpy_ds["label"]
```

Note that the library still requires `tensorflow` as an internal dependency.

### Citation

Please include the following citation when using `tensorflow-datasets` for a
paper, in addition to any citation specific to the used datasets.

```
@misc{TFDS,
  title = {{TensorFlow Datasets}, A collection of ready-to-use datasets},
  howpublished = {\url{https://www.tensorflow.org/datasets}},
}
```

## Want a certain dataset?

Adding a dataset is really straightforward by following
[our guide](https://github.com/tensorflow/datasets/tree/master/docs/add_dataset.md).

Request a dataset by opening a
[Dataset request GitHub issue](https://github.com/tensorflow/datasets/issues/new?assignees=&labels=dataset+request&template=dataset-request.md&title=%5Bdata+request%5D+%3Cdataset+name%3E).

And vote on the current
[set of requests](https://github.com/tensorflow/datasets/labels/dataset%20request)
by adding a thumbs-up reaction to the issue.

#### *Disclaimers*

*This is a utility library that downloads and prepares public datasets. We do*
*not host or distribute these datasets, vouch for their quality or fairness, or*
*claim that you have license to use the dataset. It is your responsibility to*
*determine whether you have permission to use the dataset under the dataset's*
*license.*

*If you're a dataset owner and wish to update any part of it (description,*
*citation, etc.), or do not want your dataset to be included in this*
*library, please get in touch through a GitHub issue. Thanks for your*
*contribution to the ML community!*

*If you're interested in learning more about responsible AI practices, including*
*fairness, please see Google AI's [Responsible AI Practices](https://ai.google/education/responsible-ai-practices).*

*`tensorflow/datasets` is Apache 2.0 licensed. See the `LICENSE` file.*
