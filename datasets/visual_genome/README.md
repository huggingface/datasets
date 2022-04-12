---
annotations_creators:
- found
language_creators:
- found
languages:
- en
licenses:
- cc-by-4.0
multilinguality:
- monolingual
size_categories:
- 100K<n<1M
source_datasets:
- original
task_categories:
  region-descriptions:
  - image-to-text
  objects:
  - object-detection
  objects-attributes:
  - object-attribute-detection
  relationships:
  - relationship-detection
  question-anwering:
  - visual-question-answering
task_ids:
  region-descriptions:
  - image-captioning
paperswithcode_id: visual-genome
pretty_name: VisualGenome
---

# Dataset Card for Visual Genome

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

- **Homepage:** https://visualgenome.org/
- **Repository:** 
- **Paper:** https://visualgenome.org/static/paper/Visual_Genome.pdf
- **Leaderboard:**
- **Point of Contact:** ranjaykrishna [at] gmail [dot] com

### Dataset Summary

Visual Genome is a dataset, a knowledge base, an ongoing effort to connect structured image concepts to language.

From the paper:
> Despite progress in perceptual tasks such as
image classification, computers still perform poorly on
cognitive tasks such as image description and question
answering. Cognition is core to tasks that involve not
just recognizing, but reasoning about our visual world.
However, models used to tackle the rich content in images for cognitive tasks are still being trained using the
same datasets designed for perceptual tasks. To achieve
success at cognitive tasks, models need to understand
the interactions and relationships between objects in an
image. When asked “What vehicle is the person riding?”,
computers will need to identify the objects in an image
as well as the relationships riding(man, carriage) and
pulling(horse, carriage) to answer correctly that “the
person is riding a horse-drawn carriage.”

Visual Genome has:
 - 108,077 image
 - 5.4 Million Region Descriptions
 - 1.7 Million Visual Question Answers
 - 3.8 Million Object Instances
 - 2.8 Million Attributes
 - 2.3 Million Relationships

From the paper:
> Our dataset contains over 108K images where each
image has an average of 35 objects, 26 attributes, and 21
pairwise relationships between objects. We canonicalize
the objects, attributes, relationships, and noun phrases
in region descriptions and questions answer pairs to
WordNet synsets.

### Dataset Preprocessing

### Supported Tasks and Leaderboards

### Languages

All of annotations use English as primary language.

## Dataset Structure

### Data Instances

#### region-descriptions

An example of looks as follows.

```
{
  "image": <PIL.JpegImagePlugin.JpegImageFile image mode=RGB size=800x600 at 0x7F2F60698610>,
  "image_id": 1,
  "url": "https://cs.stanford.edu/people/rak248/VG_100K_2/1.jpg",
  "width": 800,
  "height": 600,
  "coco_id": null,
  "flickr_id": null,
  "regions": [
    {
      "region_id": 1382,
      "image_id": 1,
      "phrase": "the clock is green in colour",
      "x": 421,
      "y": 57,
      "width": 82,
      "height": 139
    },
    ...
  ]
}
```

#### objects

An example of looks as follows.


#### objects-attributes

An example of looks as follows.


#### relationships

An example of looks as follows.


#### question-answering

An example of looks as follows.

### Data Fields

#### region-descriptions

- `image`: A `PIL.Image.Image` object containing the image. Note that when accessing the image column: `dataset[0]["image"]` the image file is automatically decoded. Decoding of a large number of image files might take a significant amount of time. Thus it is important to first query the sample index before the `"image"` column, *i.e.* `dataset[0]["image"]` should **always** be preferred over `dataset["image"][0]`
- `image_id`: Unique numeric ID of the image.
- `url`:  URL of source image.
- `width`: Image width.
- `height`: Image height.
- `coco_id`: Id mapping to MSCOCO indexing.
- `flickr_id`: Id mapping to Flicker indexing.
- `regions`: Holds a list of Region dataclasses:
  - `region_id`: Unique numeric ID of the region.
  - `image_id`: Unique numeric ID of the image.
  - `x`: x coordinate of bounding box's top left corner.
  - `y`: y coordinate of bounding box's top left corner.
  - `width`: Bounding box width.
  - `heigh`: Bounding box height.

#### objects

#### objects-attributes

#### relationships

#### question-answering

// TODO @thomas21
- `image_id`: Unique alphanumeric ID of the image post (assigned by Reddit).
- `author`: Reddit username of the image post author.
- `image_url`: Static URL for downloading the image associated with the post.
- `raw_caption`: Textual description of the image, written by the post author.
- `caption`: Cleaned version of "raw_caption" by us (see Q35).
- `subreddit`: Name of subreddit where the post was submitted.
- `score`: Net upvotes (discounting downvotes) received by the image post. This field is equal to `None` if the image post is a crosspost.
- `created_utc`: Integer time epoch (in UTC) when the post was submitted to Reddit.
- `permalink`: Partial URL of the Reddit post (https://reddit.com/<permalink>).
- `crosspost_parents`: List of parent posts. This field is optional.


### Data Splits

All the data is contained in training set.

## Dataset Creation

### Curation Rationale

### Source Data

#### Initial Data Collection and Normalization

#### Who are the source language producers?

### Annotations

#### Annotation process

#### Who are the annotators?

From the paper:
> We used Amazon Mechanical Turk (AMT) as our primary source of annotations. Overall, a total of over
33, 000 unique workers contributed to the dataset. The
dataset was collected over the course of 6 months after
15 months of experimentation and iteration on the data
representation. Approximately 800, 000 Human Intelligence Tasks (HITs) were launched on AMT, where
each HIT involved creating descriptions, questions and
answers, or region graphs. Each HIT was designed such
that workers manage to earn anywhere between $6-$8
per hour if they work continuously, in line with ethical
research standards on Mechanical Turk (Salehi et al.,
2015). Visual Genome HITs achieved a 94.1% retention
rate, meaning that 94.1% of workers who completed one
of our tasks went ahead to do more. [...] 93.02% of workers contributed from the United States.
The majority of our workers were
between the ages of 25 and 34 years old. Our youngest
contributor was 18 years and the oldest was 68 years
old. We also had a near-balanced split of 54.15% male
and 45.85% female workers.

### Personal and Sensitive Information

## Considerations for Using the Data

### Social Impact of Dataset

### Discussion of Biases

### Other Known Limitations

## Additional Information

### Dataset Curators

### Licensing Information

Visual Genome by Ranjay Krishna is licensed under a Creative Commons Attribution 4.0 International License.

### Citation Information

```
@inproceedings{krishnavisualgenome,
  title={Visual Genome: Connecting Language and Vision Using Crowdsourced Dense Image Annotations},
  author={Krishna, Ranjay and Zhu, Yuke and Groth, Oliver and Johnson, Justin and Hata, Kenji and Kravitz, Joshua and Chen, Stephanie and Kalantidis, Yannis and Li, Li-Jia and Shamma, David A and Bernstein, Michael and Fei-Fei, Li},
  year = {2016},
  url = {https://arxiv.org/abs/1602.07332},
}
```

### Contributions

Thanks to [@thomasw21](https://github.com/thomasw21) for adding this dataset.

from datasets import load_dataset
import json

def get_first(config):
  dset = load_dataset("datasets/visual_genome", config, split="train")
  elt = dset[0]
  del elt["image"]
  print(json.dumps(elt, indent=2))

get_first("region-descriptions")