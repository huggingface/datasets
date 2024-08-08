# Dataset features

[`Features`] defines the internal structure of a dataset. It is used to specify the underlying serialization format. What's more interesting to you though is that [`Features`] contains high-level information about everything from the column names and types, to the [`ClassLabel`]. You can think of [`Features`] as the backbone of a dataset.

The [`Features`] format is simple: `dict[column_name, column_type]`. It is a dictionary of column name and column type pairs. The column type provides a wide range of options for describing the type of data you have.

Let's have a look at the features of the MRPC dataset from the GLUE benchmark:

```py
>>> from datasets import load_dataset
>>> dataset = load_dataset('glue', 'mrpc', split='train')
>>> dataset.features
{'idx': Value(dtype='int32', id=None),
 'label': ClassLabel(num_classes=2, names=['not_equivalent', 'equivalent'], names_file=None, id=None),
 'sentence1': Value(dtype='string', id=None),
 'sentence2': Value(dtype='string', id=None),
}
```

The [`Value`] feature tells 🤗 Datasets:

- The `idx` data type is `int32`.
- The `sentence1` and `sentence2` data types are `string`.

🤗 Datasets supports many other data types such as `bool`, `float32` and `binary` to name just a few.

<Tip>

Refer to [`Value`] for a full list of supported data types.

</Tip>

The [`ClassLabel`] feature informs 🤗 Datasets the `label` column contains two classes. The classes are labeled `not_equivalent` and `equivalent`. Labels are stored as integers in the dataset. When you retrieve the labels, [`ClassLabel.int2str`] and [`ClassLabel.str2int`] carries out the conversion from integer value to label name, and vice versa.

If your data type contains a list of objects, then you want to use the [`Sequence`] feature. Remember the SQuAD dataset?

```py
>>> from datasets import load_dataset
>>> dataset = load_dataset('squad', split='train')
>>> dataset.features
{'answers': Sequence(feature={'text': Value(dtype='string', id=None), 'answer_start': Value(dtype='int32', id=None)}, length=-1, id=None),
'context': Value(dtype='string', id=None),
'id': Value(dtype='string', id=None),
'question': Value(dtype='string', id=None),
'title': Value(dtype='string', id=None)}
```

The `answers` field is constructed using the [`Sequence`] feature because it contains two subfields, `text` and `answer_start`, which are lists of `string` and `int32`, respectively.

<Tip>

See the [flatten](./process#flatten) section to learn how you can extract the nested subfields as their own independent columns.

</Tip>

The array feature type is useful for creating arrays of various sizes. You can create arrays with two dimensions using [`Array2D`], and even arrays with five dimensions using [`Array5D`]. 

```py
>>> features = Features({'a': Array2D(shape=(1, 3), dtype='int32')})
```

The array type also allows the first dimension of the array to be dynamic. This is useful for handling sequences with variable lengths such as sentences, without having to pad or truncate the input to a uniform shape.

```py
>>> features = Features({'a': Array3D(shape=(None, 5, 2), dtype='int32')})
```

## Audio feature

Audio datasets have a column with type [`Audio`], which contains three important fields:

* `array`: the decoded audio data represented as a 1-dimensional array.
* `path`: the path to the downloaded audio file.
* `sampling_rate`: the sampling rate of the audio data.

When you load an audio dataset and call the audio column, the [`Audio`] feature automatically decodes and resamples the audio file:

```py
>>> from datasets import load_dataset, Audio

>>> dataset = load_dataset("PolyAI/minds14", "en-US", split="train")
>>> dataset[0]["audio"]
{'array': array([ 0.        ,  0.00024414, -0.00024414, ..., -0.00024414,
         0.        ,  0.        ], dtype=float32),
 'path': '/root/.cache/huggingface/datasets/downloads/extracted/f14948e0e84be638dd7943ac36518a4cf3324e8b7aa331c5ab11541518e9368c/en-US~JOINT_ACCOUNT/602ba55abb1e6d0fbce92065.wav',
 'sampling_rate': 8000}
```

<Tip warning={true}>

Index into an audio dataset using the row index first and then the `audio` column - `dataset[0]["audio"]` - to avoid decoding and resampling all the audio files in the dataset. Otherwise, this can be a slow and time-consuming process if you have a large dataset.

</Tip>

With `decode=False`, the [`Audio`] type simply gives you the path or the bytes of the audio file, without decoding it into an `array`, 

```py
>>> dataset = load_dataset("PolyAI/minds14", "en-US", split="train").cast_column("audio", Audio(decode=False))
>>> dataset[0]
{'audio': {'bytes': None,
  'path': '/root/.cache/huggingface/datasets/downloads/extracted/f14948e0e84be638dd7943ac36518a4cf3324e8b7aa331c5ab11541518e9368c/en-US~JOINT_ACCOUNT/602ba55abb1e6d0fbce92065.wav'},
 'english_transcription': 'I would like to set up a joint account with my partner',
 'intent_class': 11,
 'lang_id': 4,
 'path': '/root/.cache/huggingface/datasets/downloads/extracted/f14948e0e84be638dd7943ac36518a4cf3324e8b7aa331c5ab11541518e9368c/en-US~JOINT_ACCOUNT/602ba55abb1e6d0fbce92065.wav',
 'transcription': 'I would like to set up a joint account with my partner'}
```

## Image feature

Image datasets have a column with type [`Image`], which loads `PIL.Image` objects from images stored as bytes:

When you load an image dataset and call the image column, the [`Image`] feature automatically decodes the image file:

```py
>>> from datasets import load_dataset, Image

>>> dataset = load_dataset("beans", split="train")
>>> dataset[0]["image"]
<PIL.JpegImagePlugin.JpegImageFile image mode=RGB size=500x500 at 0x125506CF8>
```

<Tip warning={true}>

Index into an image dataset using the row index first and then the `image` column - `dataset[0]["image"]` - to avoid decoding all the image files in the dataset. Otherwise, this can be a slow and time-consuming process if you have a large dataset.

</Tip>

With `decode=False`, the [`Image`] type simply gives you the path or the bytes of the image file, without decoding it into an `PIL.Image`, 

```py
>>> dataset = load_dataset("beans", split="train").cast_column("image", Image(decode=False))
>>> dataset[0]["image"]
{'bytes': None,
 'path': '/Users/username/.cache/huggingface/datasets/downloads/extracted/772e7c1fba622cff102b85dd74bcce46e8168634df4eaade7bedd3b8d91d3cd7/train/healthy/healthy_train.265.jpg'}
```

Depending on the dataset, you may get the path to the local downloaded image, or the content of the image as bytes if the dataset is not made of individual files.

You can also define a dataset of images from numpy arrays:

```python
>>> ds = Dataset.from_dict({"i": [np.zeros(shape=(16, 16, 3), dtype=np.uint8)]}, features=Features({"i": Image()}))
```

And in this case the numpy arrays are encoded into PNG (or TIFF if the pixels values precision is important).

For multi-channels arrays like RGB or RGBA, only uint8 is supported. If you use a larger precision, you get a warning and the array is downcasted to uint8.
For gray-scale images you can use the integer or float precision you want as long as it is compatible with `Pillow`. A warning is shown if your image integer or float precision is too high, and in this case the array is downcated: an int64 array is downcasted to int32, and a float64 array is downcasted to float32. 
