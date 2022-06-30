---
annotations_creators:
- found
language_creators:
- found
language:
- en
license:
- unknown
multilinguality:
- monolingual
size_categories:
- 1M<n<10M
source_datasets:
- original
task_categories:
- image-to-text
task_ids:
- image-captioning
paperswithcode_id: sbu-captions-dataset
pretty_name: SBU Captioned Photo Dataset
---

# Dataset Card for SBU Captioned Photo Dataset

## Table of Contents
- [Table of Contents](#table-of-contents)
- [Dataset Description](#dataset-description)
  - [Dataset Summary](#dataset-summary)
  - [Dataset Preprocessing](#dataset-preprocessing)
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

- **Homepage:** [SBU Captioned Photo Dataset homepage](http://www.cs.virginia.edu/~vicente/sbucaptions/)
- **Repository:**
- **Paper:** [Im2Text: Describing Images Using 1 Million Captioned Photographs](https://papers.nips.cc/paper/2011/hash/5dd9db5e033da9c6fb5ba83c7a7ebea9-Abstract.html)
- **Leaderboard:**
- **Point of Contact:** [Vicente Ordóñez Román](mailto:vicente@virginia.edu)

### Dataset Summary

SBU Captioned Photo Dataset is a collection of associated captions and images from Flickr.

### Dataset Preprocessing

This dataset doesn't download the images locally by default. Instead, it exposes URLs to the images. To fetch the images, use the following code:

```python
from concurrent.futures import ThreadPoolExecutor
from functools import partial
import io
import urllib

import PIL.Image

from datasets import load_dataset
from datasets.utils.file_utils import get_datasets_user_agent


USER_AGENT = get_datasets_user_agent()


def fetch_single_image(image_url, timeout=None, retries=0):
    for _ in range(retries + 1):
        try:
            request = urllib.request.Request(
                image_url,
                data=None,
                headers={"user-agent": USER_AGENT},
            )
            with urllib.request.urlopen(request, timeout=timeout) as req:
                image = PIL.Image.open(io.BytesIO(req.read()))
            break
        except Exception:
            image = None
    return image


def fetch_images(batch, num_threads, timeout=None, retries=0):
    fetch_single_image_with_args = partial(fetch_single_image, timeout=timeout, retries=retries)
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        batch["image"] = list(executor.map(fetch_single_image_with_args, batch["image_url"]))
    return batch


num_threads = 20
dset = load_dataset("sbu_captions")
dset = dset.map(fetch_images, batched=True, batch_size=100, fn_kwargs={"num_threads": num_threads})
```

### Supported Tasks and Leaderboards

- `image-to-text`: This dataset can be used to train a model for Image Captioning where the goal is to predict a caption given the image.

### Languages

All captions are in English.

## Dataset Structure

### Data Instances

Each instance in SBU Captioned Photo Dataset represents a single image with a caption and a user_id:

```
{
  'img_url': 'http://static.flickr.com/2723/4385058960_b0f291553e.jpg', 
  'user_id': '47889917@N08', 
  'caption': 'A wooden chair in the living room'
}
```

### Data Fields

- `image_url`: Static URL for downloading the image associated with the post.
- `caption`: Textual description of the image.
- `user_id`: Author of caption.

### Data Splits

All the data is contained in training split. The training set has 1M instances.

## Dataset Creation

### Curation Rationale

From the paper:
> One contribution is our technique for the automatic collection of this new dataset – performing a huge number of Flickr queries and then filtering the noisy results down to 1 million images with associated visually
relevant captions. Such a collection allows us to approach the extremely challenging problem of description generation using relatively simple non-parametric methods and produces surprisingly effective results.

### Source Data

The source images come from Flickr.

#### Initial Data Collection and Normalization

One key contribution of our paper is a novel web-scale database of photographs with associated
descriptive text. To enable effective captioning of novel images, this database must be good in two
ways: 1) It must be large so that image based matches to a query are reasonably similar, 2) The
captions associated with the data base photographs must be visually relevant so that transferring
captions between pictures is useful. To achieve the first requirement we query Flickr using a huge
number of pairs of query terms (objects, attributes, actions, stuff, and scenes). This produces a very
large, but noisy initial set of photographs with associated text.

#### Who are the source language producers?

The Flickr users.

### Annotations

#### Annotation process

Text descriptions associated with the images are inherited as annotations/captions.

#### Who are the annotators?

The Flickr users.

### Personal and Sensitive Information

## Considerations for Using the Data

### Social Impact of Dataset

### Discussion of Biases

### Other Known Limitations

## Additional Information

### Dataset Curators

Vicente Ordonez, Girish Kulkarni and Tamara L. Berg.

### Licensing Information

Not specified.

### Citation Information

```bibtex
@inproceedings{NIPS2011_5dd9db5e,
 author = {Ordonez, Vicente and Kulkarni, Girish and Berg, Tamara},
 booktitle = {Advances in Neural Information Processing Systems},
 editor = {J. Shawe-Taylor and R. Zemel and P. Bartlett and F. Pereira and K.Q. Weinberger},
 pages = {},
 publisher = {Curran Associates, Inc.},
 title = {Im2Text: Describing Images Using 1 Million Captioned Photographs},
 url = {https://proceedings.neurips.cc/paper/2011/file/5dd9db5e033da9c6fb5ba83c7a7ebea9-Paper.pdf},
 volume = {24},
 year = {2011}
}
```

### Contributions

Thanks to [@thomasw21](https://github.com/thomasw21) for adding this dataset.
