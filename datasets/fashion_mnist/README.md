---
annotations_creators:
- expert-generated
language_creators:
- found
language:
- en
license:
- mit
multilinguality:
- monolingual
size_categories:
- 10K<n<100K
source_datasets:
- original
task_categories:
- image-classification
task_ids:
- multi-class-image-classification
paperswithcode_id: fashion-mnist
pretty_name: FashionMNIST
---

# Dataset Card for FashionMNIST

## Table of Contents
- [Dataset Description](#dataset-description)
  - [Dataset Summary](#dataset-summary)
  - [Supported Tasks and Leaderboards](#supported-tasks-and-leaderboards)
  - [Languages](#languages)
- [Dataset Structure](#dataset-structure)
  - [Data Instances](#data-instances)
  - [Data Fields](#data-fields)
  - [Data Splits](#data-splits)
- [Dataset Creation](#dataset-creation)
  - [Curation Rationale](#curation-rationale)
  - [Source Data](#source-data)
  - [Annotations](#annotations)
  - [Personal and Sensitive Information](#personal-and-sensitive-information)
- [Considerations for Using the Data](#considerations-for-using-the-data)
  - [Social Impact of Dataset](#social-impact-of-dataset)
  - [Discussion of Biases](#discussion-of-biases)
  - [Other Known Limitations](#other-known-limitations)
- [Additional Information](#additional-information)
  - [Dataset Curators](#dataset-curators)
  - [Licensing Information](#licensing-information)
  - [Citation Information](#citation-information)
  - [Contributions](#contributions)

## Dataset Description

- **Homepage:** [GitHub](https://github.com/zalandoresearch/fashion-mnist)
- **Repository:** [GitHub](https://github.com/zalandoresearch/fashion-mnist)
- **Paper:** [arXiv](https://arxiv.org/pdf/1708.07747.pdf)
- **Leaderboard:**
- **Point of Contact:**

### Dataset Summary

Fashion-MNIST is a dataset of Zalando's article images—consisting of a training set of 60,000 examples and a test set of 10,000 examples. Each example is a 28x28 grayscale image, associated with a label from 10 classes. We intend Fashion-MNIST to serve as a direct drop-in replacement for the original MNIST dataset for benchmarking machine learning algorithms. It shares the same image size and structure of training and testing splits.

### Supported Tasks and Leaderboards

- `image-classification`: The goal of this task is to classify a given image of Zalando's article into one of 10 classes. The leaderboard is available [here](https://paperswithcode.com/sota/image-classification-on-fashion-mnist).

### Languages

[More Information Needed]

## Dataset Structure

### Data Instances

A data point comprises an image and its label.

```
{
  'image': <PIL.PngImagePlugin.PngImageFile image mode=L size=28x28 at 0x27601169DD8>,
  'label': 9
}
```

### Data Fields

- `image`: A `PIL.Image.Image` object containing the 28x28 image. Note that when accessing the image column: `dataset[0]["image"]` the image file is automatically decoded. Decoding of a large number of image files might take a significant amount of time. Thus it is important to first query the sample index before the `"image"` column, *i.e.* `dataset[0]["image"]` should **always** be preferred over `dataset["image"][0]`.
- `label`: an integer between 0 and 9 representing the classes with the following mapping:
  | Label | Description |
  | --- | --- |
  | 0 | T-shirt/top |
  | 1 | Trouser |
  | 2 | Pullover |
  | 3 | Dress |
  | 4 | Coat |
  | 5 | Sandal |
  | 6 | Shirt |
  | 7 | Sneaker |
  | 8 | Bag |
  | 9 | Ankle boot |

### Data Splits

The data is split into training and test set. The training set contains 60,000 images and the test set 10,000 images.

## Dataset Creation

### Curation Rationale

**From the arXiv paper:**
The original MNIST dataset contains a lot of handwritten digits. Members of the AI/ML/Data Science community love this dataset and use it as a benchmark to validate their algorithms. In fact, MNIST is often the first dataset researchers try. "If it doesn't work on MNIST, it won't work at all", they said. "Well, if it does work on MNIST, it may still fail on others."

Here are some good reasons:

- MNIST is too easy. Convolutional nets can achieve 99.7% on MNIST. Classic machine learning algorithms can also achieve 97% easily. Check out our side-by-side benchmark for Fashion-MNIST vs. MNIST, and read "Most pairs of MNIST digits can be distinguished pretty well by just one pixel."
- MNIST is overused. In this April 2017 Twitter thread, Google Brain research scientist and deep learning expert Ian Goodfellow calls for people to move away from MNIST.
- MNIST can not represent modern CV tasks, as noted in this April 2017 Twitter thread, deep learning expert/Keras author François Chollet.

### Source Data

#### Initial Data Collection and Normalization

**From the arXiv paper:**
Fashion-MNIST is based on the assortment on Zalando’s website. Every fashion product on Zalando has a set of pictures shot by professional photographers, demonstrating different aspects of the product, i.e. front and back looks, details, looks with model and in an outfit. The original picture has a light-gray background (hexadecimal color: #fdfdfd) and stored in 762 × 1000 JPEG format. For efficiently serving different frontend components, the original picture is resampled with multiple resolutions, e.g. large, medium, small, thumbnail and tiny.

We use the front look thumbnail images of 70,000 unique products to build Fashion-MNIST. Those products come from different gender groups: men, women, kids and neutral. In particular, whitecolor products are not included in the dataset as they have low contrast to the background. The thumbnails (51 × 73) are then fed into the following conversion pipeline:

1. Converting the input to a PNG image.
2. Trimming any edges that are close to the color of the corner pixels. The “closeness” is defined by the distance within 5% of the maximum possible intensity in RGB space.
3. Resizing the longest edge of the image to 28 by subsampling the pixels, i.e. some rows and columns are skipped over.
4. Sharpening pixels using a Gaussian operator of the radius and standard deviation of 1.0, with increasing effect near outlines.
5. Extending the shortest edge to 28 and put the image to the center of the canvas.
6. Negating the intensities of the image.
7. Converting the image to 8-bit grayscale pixels.

#### Who are the source language producers?

**From the arXiv paper:**
Every fashion product on Zalando has a set of pictures shot by professional photographers, demonstrating different aspects of the product, i.e. front and back looks, details, looks with model and in an outfit.

### Annotations

#### Annotation process

**From the arXiv paper:**
For the class labels, they use the silhouette code of the product. The silhouette code is manually labeled by the in-house fashion experts and reviewed by a separate team at Zalando. Each product Zalando is the Europe’s largest online fashion platform. Each product contains only one silhouette code.

#### Who are the annotators?

**From the arXiv paper:**
The silhouette code is manually labeled by the in-house fashion experts and reviewed by a separate team at Zalando.

### Personal and Sensitive Information

[More Information Needed]

## Considerations for Using the Data

### Social Impact of Dataset

[More Information Needed]

### Discussion of Biases

[More Information Needed]

### Other Known Limitations

[More Information Needed]

## Additional Information

### Dataset Curators

Han Xiao and Kashif Rasul and Roland Vollgraf

### Licensing Information

MIT Licence

### Citation Information

```
@article{DBLP:journals/corr/abs-1708-07747,
  author    = {Han Xiao and
               Kashif Rasul and
               Roland Vollgraf},
  title     = {Fashion-MNIST: a Novel Image Dataset for Benchmarking Machine Learning
               Algorithms},
  journal   = {CoRR},
  volume    = {abs/1708.07747},
  year      = {2017},
  url       = {http://arxiv.org/abs/1708.07747},
  archivePrefix = {arXiv},
  eprint    = {1708.07747},
  timestamp = {Mon, 13 Aug 2018 16:47:27 +0200},
  biburl    = {https://dblp.org/rec/bib/journals/corr/abs-1708-07747},
  bibsource = {dblp computer science bibliography, https://dblp.org}
}
```

### Contributions

Thanks to [@gchhablani](https://github.com/gchablani) for adding this dataset.
