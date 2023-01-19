# Image classification

Image classification datasets are used to train a model to classify an entire image. There are a wide variety of applications enabled by these datasets such as identifying endangered wildlife species or screening for disease in medical images. This guide will show you how to apply transformations to an image classification dataset.

Before you start, make sure you have up-to-date versions of `albumentations` and `cv2` installed:

```bash
pip install -U albumentations opencv-python
```

This guide uses the [Beans](https://huggingface.co/datasets/beans) dataset for identifying the type of bean plant disease based on an image of its leaf.

Load the dataset and take a look at an example:

```py
>>> from datasets import load_dataset

>>> dataset = load_dataset("beans")
>>> dataset["train"][10]
{'image': <PIL.JpegImagePlugin.JpegImageFile image mode=RGB size=500x500 at 0x7F8D2F4D7A10>,
 'image_file_path': '/root/.cache/huggingface/datasets/downloads/extracted/b0a21163f78769a2cf11f58dfc767fb458fc7cea5c05dccc0144a2c0f0bc1292/train/angular_leaf_spot/angular_leaf_spot_train.204.jpg',
 'labels': 0}
```

The dataset has three fields:

* `image`: a PIL image object.
* `image_file_path`: the path to the image file.
* `labels`: the label or category of the image.

Next, check out an image:

<div class="flex justify-center">
    <img src="https://huggingface.co/datasets/huggingface/documentation-images/resolve/main/datasets/img_clf.png">
</div>

Now apply some augmentations with `albumentations`. You'll randomly crop the image, flip it horizontally, and adjust its brightness.

```py
>>> import cv2
>>> import albumentations
>>> import numpy as np

>>> transform = albumentations.Compose([
...     albumentations.RandomCrop(width=256, height=256),
...     albumentations.HorizontalFlip(p=0.5),
...     albumentations.RandomBrightnessContrast(p=0.2),
... ])
```

Create a function to apply the transformation to the images:

```py
>>> def transforms(examples):
...     examples["pixel_values"] = [
...         transform(image=np.array(image))["image"] for image in examples["image"]
...     ]
... 
...     return examples
```

Use the [`~Dataset.set_transform`] function to apply the transformation on-the-fly to batches of the dataset to consume less disk space:

```py
>>> dataset.set_transform(transforms)
```

You can verify the transformation worked by indexing into the `pixel_values` of the first example:

```py
>>> import numpy as np
>>> import matplotlib.pyplot as plt

>>> img = dataset["train"][0]["pixel_values"]
>>> plt.imshow(img)
```

<div class="flex justify-center">
    <img class="block dark:hidden" src="https://huggingface.co/datasets/huggingface/documentation-images/resolve/main/datasets/img_clf_aug.png">
    <img class="hidden dark:block" src="https://huggingface.co/datasets/huggingface/documentation-images/resolve/main/datasets/img_clf_aug.png"/>
</div>

<Tip>

Now that you know how to process a dataset for image classification, learn
[how to train an image classification model](https://colab.research.google.com/github/huggingface/notebooks/blob/main/examples/image_classification.ipynb)
and use it for inference.

</Tip>