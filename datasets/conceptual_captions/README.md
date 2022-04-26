---
annotations_creators:
- found
language_creators:
- found
languages:
- en
licenses:
- other
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
paperswithcode_id: conceptual-captions
pretty_name: Conceptual Captions
---

# Dataset Card for Conceptual Captions

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

- **Homepage:** [Conceptual Captions homepage](https://ai.google.com/research/ConceptualCaptions/)
- **Repository:** [Conceptual Captions repository](https://github.com/google-research-datasets/conceptual-captions)
- **Paper:** [Conceptual Captions: A Cleaned, Hypernymed, Image Alt-text Dataset For Automatic Image Captioning](https://www.aclweb.org/anthology/P18-1238/)
- **Leaderboard:** [Conceptual Captions leaderboard](https://ai.google.com/research/ConceptualCaptions/competition?active_tab=leaderboard)https://ai.google.com/research/ConceptualCaptions/leaderboard?active_tab=leaderboard
- **Point of Contact:** [Conceptual Captions e-mail](mailto:conceptual-captions@google.com)

### Dataset Summary

Conceptual Captions is a dataset consisting of ~3.3M images annotated with captions. In contrast with the curated style of other image caption annotations, Conceptual Caption images and their raw descriptions are harvested from the web, and therefore represent a wider variety of styles. More precisely, the raw descriptions are harvested from the Alt-text HTML attribute associated with web images. To arrive at the current version of the captions, we have developed an automatic pipeline that extracts, filters, and transforms candidate image/caption pairs, with the goal of achieving a balance of cleanliness, informativeness, fluency, and learnability of the resulting captions.

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


def fetch_single_image(image_url, timeout=None, retries=0):
    for _ in range(retries + 1):
        try:
            request = urllib.request.Request(
                image_url,
                data=None,
                headers={"user-agent": get_datasets_user_agent()},
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
dset = load_dataset("conceptual_captions")
dset = dset.map(fetch_images, batched=True, batch_size=100, fn_kwargs={"num_threads": num_threads})
```

### Supported Tasks and Leaderboards

- `image-captioning`: This dataset can be used to train model for the Image Captioning task. The leaderboard for this task is available [here](https://ai.google.com/research/ConceptualCaptions/competition?active_tab=leaderboard). Official submission output captions are scored against the reference captions from the hidden test set using [this](https://github.com/tylin/coco-caption) implementation of the CIDEr (primary), ROUGE-L and SPICE metrics.

### Languages

All captions are in English.

## Dataset Structure

### Data Instances

#### `unlabeled`

Each instance in this configuration represents a single image with a caption:

```
{
  'image_url': 'http://lh6.ggpht.com/-IvRtNLNcG8o/TpFyrudaT6I/AAAAAAAAM6o/_11MuAAKalQ/IMG_3422.JPG?imgmax=800',
  'caption': 'a very typical bus station'
}
```

#### `labeled`

Each instance in this configuration represents a single image with a caption with addtional machine-generated image labels and confidence scores:

```
{
  'image_url': 'https://thumb1.shutterstock.com/display_pic_with_logo/261388/223876810/stock-vector-christmas-tree-on-a-black-background-vector-223876810.jpg',
  'caption': 'christmas tree on a black background .',
  'labels': ['christmas tree', 'christmas decoration', 'font', 'text', 'graphic design', 'illustration','interior design', 'tree', 'christmas eve', 'ornament', 'fir', 'plant', 'pine', 'pine family', 'graphics'],
  'MIDs': ['/m/025nd', '/m/05fc9mj', '/m/03gq5hm', '/m/07s6nbt', '/m/03c31', '/m/01kr8f', '/m/0h8nzzj', '/m/07j7r', '/m/014r1s', '/m/05ykl4', '/m/016x4z', '/m/05s2s', '/m/09t57', '/m/01tfm0', '/m/021sdg'],
  'confidence_scores': [0.9818305373191833, 0.952756941318512, 0.9227379560470581, 0.8524878621101379, 0.7597672343254089, 0.7493422031402588, 0.7332468628883362, 0.6869218349456787, 0.6552258133888245, 0.6357356309890747, 0.5992692708969116, 0.585474967956543, 0.5222904086112976, 0.5113164782524109, 0.5036579966545105]
}
```

### Data Fields

#### `unlabeled`

- `image_url`: Static URL for downloading the image associated with the post.
- `caption`: Textual description of the image.

#### `labeled`

- `image_url`: Static URL for downloading the image associated with the post.
- `caption`: Textual description of the image.
- `labels`: A sequence of machine-generated labels obtained using the [Google Cloud Vision API](https://cloud.google.com/vision).
- `MIDs`:  A sequence of machine-generated identifiers (MID) corresponding to the label's Google Knowledge Graph entry.
- `confidence_scores`: A sequence of confidence scores denoting how likely the corresponing labels are present on the image.

### Data Splits

#### `unlabeled`

The basic version of the dataset split into Training and Validation splits. The Training split consists of 3,318,333 image-URL/caption pairs and the Validation split consists of 15,840 image-URL/caption pairs.

#### `labeled`

The labeled version of the dataset with a single. The entire data is contained in Training split, which is a subset of 2,007,090 image-URL/caption pairs from the Training set of the `unlabeled` config.

## Dataset Creation

### Curation Rationale

From the paper:
> In this paper, we make contributions to both the data and modeling categories. First, we present a new dataset of caption annotations Conceptual Captions (Fig. 1), which has an order of magnitude more images than the COCO dataset. Conceptual Captions consists of about 3.3M himage, descriptioni pairs. In contrast with the curated style of the COCO images, Conceptual Captions images and their raw descriptions are harvested from the web, and therefore represent a wider variety of styles.

### Source Data

#### Initial Data Collection and Normalization

From the homepage:
>For Conceptual Captions, we developed a fully automatic pipeline that extracts, filters, and transforms >candidate image/caption pairs, with the goal of achieving a balance of cleanliness, informativeness, fluency, >and learnability of the resulting captions. Because no human annotators are involved, the Conceptual Captions >dataset generation process is highly scalable.
>
>To generate this dataset, we started with a Flume pipeline that processes billions of Internet webpages, >extracting, filtering, and processing candidate image and caption pairs, and keeping those that pass through >several filters.
>
>We first screen for certain properties like size, aspect ratio, adult content scores. These filters discard >more than 65% of the candidates. Next, we use Alt-Texts for text-based filtering, removing captions with >non-descriptive text (such as SEO tags or hashtags); we also discard texts with high sentiment polarity or >adult content scores, resulting in just 3% of the incoming candidates passing through.
>
>In the next step, we filter out candidates for which none of the text tokens can be mapped to the visual >content of the image. We use image classifiers (e.g., Google Cloud Vision APIs) to assign class labels to >images and match these labels against the candidate text (allowing morphological transformations), discarding >around 60% of the candidates that reach this stage.
>
>The candidates passing the above filters tend to be good Alt-text image descriptions. However, a large >majority of these use proper names (for people, venues, locations, etc.), brands, dates, quotes, etc. This >creates two distinct problems. First, some of these cannot be inferred based on the image pixels alone. This >is problematic because unless the image has the necessary visual information it is not useful for training. >Second, even if the proper names could be inferred from the image it is extremely difficult for a model to >learn to perform both fine-grained classification and natural-language descriptions simultaneously. We posit >that if automatic determination of names, locations, brands, etc. is needed, it should be done as a separate >task that may leverage image meta-information (e.g. GPS info), or complementary techniques such as OCR.
>
>We address the above problems with the insight that proper names should be replaced by words that represent >the same general notion, i.e., by their concept. For example, we remove locations (“Crowd at a concert in Los >Angeles“ becomes “Crowd at a concert”), names (e.g., “Former Miss World Priyanka Chopra on the red carpet” >becomes “actor on the red carpet”), proper noun modifiers (e.g., “Italian cuisine” becomes just “cuisine”) >and noun phrases (e.g., “actor and actor” becomes “actors”). Around 20% of the samples are discarded during >this transformation because it can leave sentences too short, or otherwise inconsistent.
>
>Finally, we perform another round of filtering to identify concepts with low-count. We cluster all resolved >entities (e.g., “actor”, “dog”, “neighborhood”, etc.) and keep only the candidate types which have a count of >over 100 mentions. This retains around 16K entity concepts such as: “person”, “actor”, “artist”, “player” and >“illustration”. The less frequent ones that we dropped include “baguette”, “bridle”, “deadline”, “ministry” >and “funnel”.

#### Who are the source language producers?

Not specified.

### Annotations

#### Annotation process

Annotations are extracted jointly with the images using the automatic pipeline.

#### Who are the annotators?

Not specified.

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

Piyush Sharma, Nan Ding, Sebastian Goodman and Radu Soricut.

### Licensing Information

The dataset may be freely used for any purpose, although acknowledgement of
Google LLC ("Google") as the data source would be appreciated. The dataset is
provided "AS IS" without any warranty, express or implied. Google disclaims all
liability for any damages, direct or indirect, resulting from the use of the
dataset.

### Citation Information

```bibtex
@inproceedings{sharma2018conceptual,
  title = {Conceptual Captions: A Cleaned, Hypernymed, Image Alt-text Dataset For Automatic Image Captioning},
  author = {Sharma, Piyush and Ding, Nan and Goodman, Sebastian and Soricut, Radu},
  booktitle = {Proceedings of ACL},
  year = {2018},
}
```

### Contributions

Thanks to [@abhishekkrthakur](https://github.com/abhishekkrthakur) and [@mariosasko](https://github.com/mariosasko) for adding this dataset.
