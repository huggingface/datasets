# Process image data

This guide shows specific methods for processing image datasets. Learn how to:

- Use [`~Dataset.map`] with image dataset.
- Apply data augmentations to a dataset with [`~Dataset.set_transform`].

For a guide on how to process any type of dataset, take a look at the <a class="underline decoration-sky-400 decoration-2 font-semibold" href="./process">general process guide</a>.

## Map

The [`~Dataset.map`] function can apply transforms over an entire dataset.

For example, create a basic [`Resize`](https://pytorch.org/vision/stable/generated/torchvision.transforms.Resize.html) function:

```py
>>> def transforms(examples):
...     examples["pixel_values"] = [image.convert("RGB").resize((100,100)) for image in examples["image"]]
...     return examples
```

Now use the [`~Dataset.map`] function to resize the entire dataset, and set `batched=True` to speed up the process by accepting batches of examples. The transform returns `pixel_values` as a cacheable `PIL.Image` object:

```py
>>> dataset = dataset.map(transforms, remove_columns=["image"], batched=True)
>>> dataset[0]
{'label': 6,
 'pixel_values': <PIL.PngImagePlugin.PngImageFile image mode=RGB size=100x100 at 0x7F058237BB10>}
```

The cache file saves time because you don't have to execute the same transform twice. The [`~Dataset.map`] function is best for operations you only run once per training - like resizing an image - instead of using it for operations executed for each epoch, like data augmentations.

[`~Dataset.map`] takes up some memory, but you can reduce its memory requirements with the following parameters:

- [`batch_size`](./package_reference/main_classes#datasets.DatasetDict.map.batch_size) determines the number of examples that are processed in one call to the transform function.
- [`writer_batch_size`](./package_reference/main_classes#datasets.DatasetDict.map.writer_batch_size) determines the number of processed examples that are kept in memory before they are stored away.

Both parameter values default to 1000, which can be expensive if you are storing images. Lower these values to use less memory when you use [`~Dataset.map`].

## Apply transforms

🤗 Datasets applies data augmentations from any library or package to your dataset. Transforms can be applied on-the-fly on batches of data with [`~Dataset.set_transform`], which consumes less disk space.

<Tip>

The following example uses [torchvision](https://pytorch.org/vision/stable/index.html), but feel free to use other data augmentation libraries like [Albumentations](https://albumentations.ai/docs/), [Kornia](https://kornia.readthedocs.io/en/latest/), and [imgaug](https://imgaug.readthedocs.io/en/latest/).

</Tip>

For example, if you'd like to change the color properties of an image randomly:

```py
>>> from torchvision.transforms import Compose, ColorJitter, ToTensor

>>> jitter = Compose(
...     [
...          ColorJitter(brightness=0.25, contrast=0.25, saturation=0.25, hue=0.7),
...          ToTensor(),
...     ]
... )
```

Create a function to apply the `ColorJitter` transform:

```py
>>> def transforms(examples):
...     examples["pixel_values"] = [jitter(image.convert("RGB")) for image in examples["image"]]
...     return examples
```

Apply the transform with the [`~Dataset.set_transform`] function:

```py
>>> dataset.set_transform(transforms)
```