---
annotations_creators:
- found
language_creators:
- found
language:
- en
license:
- other
multilinguality:
- monolingual
size_categories:
- 10M<n<100M
source_datasets:
- original
task_categories:
- image-to-text
task_ids:
- image-captioning
paperswithcode_id: cc12m
pretty_name: Conceptual 12M
---

# Dataset Card for Conceptual 12M

## Table of Contents
- [Dataset Description](#dataset-description)
  - [Dataset Summary](#dataset-summary)
  - [Dataset Preprocessing](#dataset-preprocessing)
  - [Supported Tasks](#supported-tasks-and-leaderboards)
  - [Languages](#languages)
- [Dataset Structure](#dataset-structure)
  - [Data Instances](#data-instances)
  - [Data Fields](#data-instances)
  - [Data Splits](#data-instances)
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

## Dataset Description

- **Repository:** [Conceptual 12M repository](https://github.com/google-research-datasets/conceptual-12m)
- **Paper:** [Conceptual 12M: Pushing Web-Scale Image-Text Pre-Training To Recognize Long-Tail Visual Concepts](https://arxiv.org/abs/2102.08981)
- **Point of Contact:** [Conceptual Captions e-mail](mailto:conceptual-captions@google.com)

### Dataset Summary

Conceptual 12M (CC12M) is a dataset with 12 million  image-text pairs specifically meant to be used for visionand-language pre-training.
Its data collection pipeline is a relaxed version of the one used in Conceptual Captions 3M (CC3M).

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
dset = load_dataset("conceptual_12m")
dset = dset.map(fetch_images, batched=True, batch_size=100, fn_kwargs={"num_threads": num_threads})
```

### Supported Tasks and Leaderboards

- `image-captioning`: This dataset can be used to train model for the Image Captioning task.

### Languages

All captions are in English.

## Dataset Structure

### Data Instances

Each instance represents a single image with a caption:

```
{
  'image_url': 'http://lh6.ggpht.com/-IvRtNLNcG8o/TpFyrudaT6I/AAAAAAAAM6o/_11MuAAKalQ/IMG_3422.JPG?imgmax=800',
  'caption': 'a very typical bus station'
}
```

### Data Fields

- `image_url`: Static URL for downloading the image associated with the post.
- `caption`: Textual description of the image.

### Data Splits

There is only training data, with a total of 12423374 rows

## Dataset Creation

### Curation Rationale

Conceptual 12M shares the same pipeline with Conceptual Captions (CC3M), but relaxes some processing steps.

### Source Data

#### Initial Data Collection and Normalization

From the paper:
> To arrive at CC12M, we keep
the image-text filtering intact, and relax the unimodal filters only. First, for image-based filtering, we set the maximum ratio of larger to smaller dimension to 2.5 instead of 2. 
We still keep only JPEG images with size greater than
400 pixels, and still exclude images that trigger pornography detectors. Second, in text-based filtering, we allow text
between 3 and 256 words in the alt-text. We still discard
candidates with no noun or no determiner, but permit ones
without prepositions. We discard the heuristics regarding
high unique-word ratio covering various POS tags and word
capitalization. We set the maximum fraction of word repetition allowed to 0.2. Given a larger pool of text due to the
above relaxations, the threshold for counting a word type as
rare is increased from 5 to 20

> The main motivation for CC3M to
perform text transformation is that a majority of candidate
captions contain ultrafine-grained entities such as proper
names (people, venues, locations, etc.), making it extremely
difficult to learn as part of the image captioning task. In
contrast, we are not restricted by the end task of image caption generation. Our intuition is that relatively more difficult pre-training data would lead to better transferability.
We thus do not perform hypernimization or digit substitution. [...] The only exception to the “keep alt-texts as
raw as possible” rule is performing person-name substitutions, which we identify as necessary to protect the privacy
of the individuals in these images. For this step, we use the
Google Cloud Natural Language APIs to detect all named
entities of type Person, and substitute them by a special token <PERSON>. Around 25% of all the alt-texts in CC12M
are transformed in this fashion.

#### Who are the source language producers?

Not specified.

### Annotations

#### Annotation process

Annotations are extracted jointly with the images using the automatic pipeline.

#### Who are the annotators?

Not specified.

### Personal and Sensitive Information

From the paper:

> The only exception to the “keep alt-texts as
raw as possible” rule is performing person-name substitutions, which we identify as necessary to protect the privacy
of the individuals in these images. For this step, we use the
Google Cloud Natural Language APIs to detect all named
entities of type Person, and substitute them by a special token <PERSON>. Around 25% of all the alt-texts in CC12M
are transformed in this fashion.

## Considerations for Using the Data

### Social Impact of Dataset

[More Information Needed]

### Discussion of Biases

[More Information Needed]

### Other Known Limitations

[More Information Needed]

## Additional Information

### Dataset Curators

Soravit Changpinyo, Piyush Sharma, Nan Ding and Radu Soricut.

### Licensing Information

The dataset may be freely used for any purpose, although acknowledgement of
Google LLC ("Google") as the data source would be appreciated. The dataset is
provided "AS IS" without any warranty, express or implied. Google disclaims all
liability for any damages, direct or indirect, resulting from the use of the
dataset.

### Citation Information

```bibtex
@inproceedings{changpinyo2021cc12m,
  title = {{Conceptual 12M}: Pushing Web-Scale Image-Text Pre-Training To Recognize Long-Tail Visual Concepts},
  author = {Changpinyo, Soravit and Sharma, Piyush and Ding, Nan and Soricut, Radu},
  booktitle = {CVPR},
  year = {2021},
}
```

### Contributions

Thanks to [@thomasw21](https://github.com/thomasw21) for adding this dataset.