---
annotations_creators:
- found
language_creators:
- found
languages:
- en
licenses:
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

# Dataset Card for RedCaps

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

- **Homepage:** http://www.cs.virginia.edu/~vicente/sbucaptions/
- **Repository:**
- **Paper:** http://tamaraberg.com/papers/generation_nips2011.pdf
- **Leaderboard:**
- **Point of Contact:** vicente@virginia.edu

### Dataset Summary

### Dataset Preprocessing

This dataset doesn't download the images locally by default. Instead, it exposes URLs to the images. To fetch the images, use the following code:

```python
from datasets import load_dataset
from datasets.utils.file_utils import get_datasets_user_agent
import PIL.Image
import requests

def get_image(url, timeout):
  response = requests.get(
      url,
      stream=True,
      headers={"user-agent": get_datasets_user_agent()},
      timeout=timeout,
  )
  if response.ok:
    return PIL.Image.open(
        response.raw
    )
  else:
    return None

def fetch_images(batch, timeout):
    images = [
      get_image(image_url, timeout)
      for image_url in batch["image_url"]
    ]
      
    batch["image"] = list(images)
    return batch

timeout = None
num_proc = 4
dset = load_dataset("sbu_captions")
dseet = dset.map(fetch_images, batched=True, batch_size=100, fn_kwargs={"timeout": timeout}, num_proc=num_proc)
```

### Supported Tasks and Leaderboards

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

### Source Data

#### Initial Data Collection and Normalization

#### Who are the source language producers?

### Annotations

#### Annotation process

#### Who are the annotators?

### Personal and Sensitive Information

## Considerations for Using the Data

### Social Impact of Dataset

### Discussion of Biases

### Other Known Limitations

## Additional Information

### Dataset Curators

### Licensing Information

### Citation Information

```
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
