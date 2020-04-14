# Customizing feature decoding

*   [Usage examples](#usage-examples)
    *   [Skipping the image decoding](#skipping-the-image-decoding)
    *   [Filter/shuffle dataset before images get decoded](#filtershuffle-dataset-before-images-get-decoded)
    *   [Cropping and decoding at the same time](#cropping-and-decoding-at-the-same-time)
    *   [Customizing video decoding](#customizing-video-decoding)

The `tfds.decode` API allows you override the default feature decoding. The main
use case is to skip the image decoding for better performance.

Warning: This API gives you access to the low-level `tf.train.Example` format on
disk (as defined by the `FeatureConnector`). This API is targeted towards
advanced users who want better read performance with images.

## Usage examples

### Skipping the image decoding

To keep full control over the decoding pipeline, or to apply a filter before the
images get decoded (for better performance), you can skip the image decoding
entirely. This works with both `tfds.features.Image` and `tfds.features.Video`.

```python
ds = tfds.load('imagenet2012', split='train', decoders={
    'image': tfds.decode.SkipDecoding(),
})

for example in ds.take(1):
  assert example['image'].dtype == tf.string  # Images are not decoded
```

### Filter/shuffle dataset before images get decoded

Similarly to the previous example, you can use `tfds.decode.SkipDecoding()` to
insert additional `tf.data` pipeline customization before decoding the image.
That way the filtered images won't be decoded and you can use a bigger shuffle
buffer.

```python
# Load the base dataset without decoding
ds, ds_info = tfds.load(
    'imagenet2012',
    split='train',
    decoders={
        'image': tfds.decode.SkipDecoding(),  # Image won't be decoded here
    },
    as_supervised=True,
    with_info=True,
)
# Apply filter and shuffle
ds = ds.filter(lambda image, label: label != 10)
ds = ds.shuffle(10000)
# Then decode with ds_info.features['image']
ds = ds.map(
    lambda image, label: ds_info.features['image'].decode_example(image), label)

```

### Cropping and decoding at the same time

To override the default `tf.io.decode_image` operation, you can create a new
`tfds.decode.Decoder` object using the `tfds.decode.make_decoder()` decorator.

```python
@tfds.decode.make_decoder()
def decode_example(serialized_image, feature):
  crop_y, crop_x, crop_height, crop_width = 10, 10, 64, 64
  return tf.image.decode_and_crop_jpeg(
      serialized_image,
      [crop_y, crop_x, crop_height, crop_width],
      channels=feature.feature.shape[-1],
  )

ds = tfds.load('imagenet2012', split='train', decoders={
    # With video, decoders are applied to individual frames
    'image': decode_example(),
})
```

Which is equivalent to:

```python
def decode_example(serialized_image, feature):
  crop_y, crop_x, crop_height, crop_width = 10, 10, 64, 64
  return tf.image.decode_and_crop_jpeg(
      serialized_image,
      [crop_y, crop_x, crop_height, crop_width],
      channels=feature.shape[-1],
  )

ds, ds_info = tfds.load(
    'imagenet2012',
    split='train',
    with_info=True,
    decoders={
        'image': tfds.decode.SkipDecoding(),  # Skip frame decoding
    },
)
ds = ds.map(functools.partial(decode_example, feature=ds_info.features['image']))
```

### Customizing video decoding

Video are `Sequence(Image())`. When applying custom decoders, they will be
applied to individual frames. This mean decoders for images are automatically
compatible with video.

```python
@tfds.decode.make_decoder()
def decode_example(serialized_image, feature):
  crop_y, crop_x, crop_height, crop_width = 10, 10, 64, 64
  return tf.image.decode_and_crop_jpeg(
      serialized_image,
      [crop_y, crop_x, crop_height, crop_width],
      channels=feature.feature.shape[-1],
  )

ds = tfds.load('ucf101', split='train', decoders={
    # With video, decoders are applied to individual frames
    'video': decode_example(),
})
```

Which is equivalent to:

```python
def decode_frame(serialized_image):
  """Decodes a single frame."""
  crop_y, crop_x, crop_height, crop_width = 10, 10, 64, 64
  return tf.image.decode_and_crop_jpeg(
      serialized_image,
      [crop_y, crop_x, crop_height, crop_width],
      channels=ds_info.features['video'].shape[-1],
  )


def decode_video(example):
  """Decodes all individual frames of the video."""
  video = example['video']
  video = tf.map_fn(
      decode_frame,
      video,
      dtype=ds_info.features['video'].dtype,
      parallel_iterations=10,
      back_prop=False,
  )
  example['video'] = video
  return example


ds, ds_info = tfds.load('ucf101', split='train', with_info=True, decoders={
    'video': tfds.decode.SkipDecoding(),  # Skip frame decoding
})
ds = ds.map(decode_video)  # Decode the video
```
