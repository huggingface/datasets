---
annotations_creators:
- found
language_creators:
- found
language:
- en
license:
- cc-by-4.0
multilinguality:
- monolingual
size_categories:
- 100K<n<1M
source_datasets:
- original
task_categories:
- image-to-text
- object-detection
- visual-question-answering
task_ids:
- image-captioning
paperswithcode_id: visual-genome
pretty_name: VisualGenome
configs:
- objects
- question_answers
- region_descriptions
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

When loading a specific configuration, users has to append a version dependent suffix:
```python
from datasets import load_dataset
load_dataset("visual_genome", "region_description_v1.2.0")
```

#### region_descriptions

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

```
{
  "image": <PIL.JpegImagePlugin.JpegImageFile image mode=RGB size=800x600 at 0x7F2F60698610>,
  "image_id": 1,
  "url": "https://cs.stanford.edu/people/rak248/VG_100K_2/1.jpg",
  "width": 800,
  "height": 600,
  "coco_id": null,
  "flickr_id": null,
  "objects": [
    {
      "object_id": 1058498,
      "x": 421,
      "y": 91,
      "w": 79,
      "h": 339,
      "names": [
        "clock"
      ],
      "synsets": [
        "clock.n.01"
      ]
    },
    ...
  ]
}
```

#### attributes

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
  "attributes": [
    {
      "object_id": 1058498,
      "x": 421,
      "y": 91,
      "w": 79,
      "h": 339,
      "names": [
        "clock"
      ],
      "synsets": [
        "clock.n.01"
      ],
      "attributes": [
        "green",
        "tall"
      ]
    },
    ...
  }
]
```

#### relationships

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
  "relationships": [
    {
      "relationship_id": 15927,
      "predicate": "ON",
      "synsets": "['along.r.01']",
      "subject": {
        "object_id": 5045,
        "x": 119,
        "y": 338,
        "w": 274,
        "h": 192,
        "names": [
          "shade"
        ],
        "synsets": [
          "shade.n.01"
        ]
      },
      "object": {
        "object_id": 5046,
        "x": 77,
        "y": 328,
        "w": 714,
        "h": 262,
        "names": [
          "street"
        ],
        "synsets": [
          "street.n.01"
        ]
      }
    }
    ...
  }
]
```
#### question_answers

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
  "qas": [
    {
      "qa_id": 986768,
      "image_id": 1,
      "question": "What color is the clock?",
      "answer": "Green.",
      "a_objects": [],
      "q_objects": []
    },
    ...
  }
]
```

### Data Fields

When loading a specific configuration, users has to append a version dependent suffix:
```python
from datasets import load_dataset
load_dataset("visual_genome", "region_description_v1.2.0")
```

#### region_descriptions

- `image`: A `PIL.Image.Image` object containing the image. Note that when accessing the image column: `dataset[0]["image"]` the image file is automatically decoded. Decoding of a large number of image files might take a significant amount of time. Thus it is important to first query the sample index before the `"image"` column, *i.e.* `dataset[0]["image"]` should **always** be preferred over `dataset["image"][0]`
- `image_id`: Unique numeric ID of the image.
- `url`:  URL of source image.
- `width`: Image width.
- `height`: Image height.
- `coco_id`: Id mapping to MSCOCO indexing.
- `flickr_id`: Id mapping to Flicker indexing.
- `regions`: Holds a list of `Region` dataclasses:
  - `region_id`: Unique numeric ID of the region.
  - `image_id`: Unique numeric ID of the image.
  - `x`: x coordinate of bounding box's top left corner.
  - `y`: y coordinate of bounding box's top left corner.
  - `width`: Bounding box width.
  - `height`: Bounding box height.

#### objects

- `image`: A `PIL.Image.Image` object containing the image. Note that when accessing the image column: `dataset[0]["image"]` the image file is automatically decoded. Decoding of a large number of image files might take a significant amount of time. Thus it is important to first query the sample index before the `"image"` column, *i.e.* `dataset[0]["image"]` should **always** be preferred over `dataset["image"][0]`
- `image_id`: Unique numeric ID of the image.
- `url`:  URL of source image.
- `width`: Image width.
- `height`: Image height.
- `coco_id`: Id mapping to MSCOCO indexing.
- `flickr_id`: Id mapping to Flicker indexing.
- `objects`: Holds a list of `Object` dataclasses:
  - `object_id`: Unique numeric ID of the object.
  - `x`: x coordinate of bounding box's top left corner.
  - `y`: y coordinate of bounding box's top left corner.
  - `w`: Bounding box width.
  - `h`: Bounding box height.
  - `names`: List of names associated with the object. This field can hold multiple values in the sense the multiple names are considered as acceptable. For example: ['monitor', 'computer'] at https://cs.stanford.edu/people/rak248/VG_100K/3.jpg
  - `synsets`: List of `WordNet synsets`.

#### attributes

- `image`: A `PIL.Image.Image` object containing the image. Note that when accessing the image column: `dataset[0]["image"]` the image file is automatically decoded. Decoding of a large number of image files might take a significant amount of time. Thus it is important to first query the sample index before the `"image"` column, *i.e.* `dataset[0]["image"]` should **always** be preferred over `dataset["image"][0]`
- `image_id`: Unique numeric ID of the image.
- `url`:  URL of source image.
- `width`: Image width.
- `height`: Image height.
- `coco_id`: Id mapping to MSCOCO indexing.
- `flickr_id`: Id mapping to Flicker indexing.
- `attributes`: Holds a list of `Object` dataclasses:
  - `object_id`: Unique numeric ID of the region.
  - `x`: x coordinate of bounding box's top left corner.
  - `y`: y coordinate of bounding box's top left corner.
  - `w`: Bounding box width.
  - `h`: Bounding box height.
  - `names`: List of names associated with the object. This field can hold multiple values in the sense the multiple names are considered as acceptable. For example: ['monitor', 'computer'] at https://cs.stanford.edu/people/rak248/VG_100K/3.jpg
  - `synsets`: List of `WordNet synsets`.
  - `attributes`: List of attributes associated with the object.

#### relationships

- `image`: A `PIL.Image.Image` object containing the image. Note that when accessing the image column: `dataset[0]["image"]` the image file is automatically decoded. Decoding of a large number of image files might take a significant amount of time. Thus it is important to first query the sample index before the `"image"` column, *i.e.* `dataset[0]["image"]` should **always** be preferred over `dataset["image"][0]`
- `image_id`: Unique numeric ID of the image.
- `url`:  URL of source image.
- `width`: Image width.
- `height`: Image height.
- `coco_id`: Id mapping to MSCOCO indexing.
- `flickr_id`: Id mapping to Flicker indexing.
- `relationships`: Holds a list of `Relationship` dataclasses:
  - `relationship_id`: Unique numeric ID of the object.
  - `predicate`: Predicate defining relationship between a subject and an object.
  - `synsets`: List of `WordNet synsets`.
  - `subject`: Object dataclass. See subsection on `objects`.
  - `object`: Object dataclass. See subsection on `objects`.

#### question_answers

- `image`: A `PIL.Image.Image` object containing the image. Note that when accessing the image column: `dataset[0]["image"]` the image file is automatically decoded. Decoding of a large number of image files might take a significant amount of time. Thus it is important to first query the sample index before the `"image"` column, *i.e.* `dataset[0]["image"]` should **always** be preferred over `dataset["image"][0]`
- `image_id`: Unique numeric ID of the image.
- `url`:  URL of source image.
- `width`: Image width.
- `height`: Image height.
- `coco_id`: Id mapping to MSCOCO indexing.
- `flickr_id`: Id mapping to Flicker indexing.
- `qas`: Holds a list of `Question-Answering` dataclasses:
  - `qa_id`: Unique numeric ID of the question-answer pair.
  - `image_id`: Unique numeric ID of the image.
  - `question`: Question.
  - `answer`: Answer.
  - `q_objects`: List of object dataclass associated with `question` field. See subsection on `objects`.
  - `a_objects`: List of object dataclass associated with `answer` field. See subsection on `objects`.

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

```bibtex
@inproceedings{krishnavisualgenome,
  title={Visual Genome: Connecting Language and Vision Using Crowdsourced Dense Image Annotations},
  author={Krishna, Ranjay and Zhu, Yuke and Groth, Oliver and Johnson, Justin and Hata, Kenji and Kravitz, Joshua and Chen, Stephanie and Kalantidis, Yannis and Li, Li-Jia and Shamma, David A and Bernstein, Michael and Fei-Fei, Li},
  year = {2016},
  url = {https://arxiv.org/abs/1602.07332},
}
```

### Contributions

Due to limitation of the dummy_data creation, we provide a `fix_generated_dummy_data.py` script that fix the dataset in-place.

Thanks to [@thomasw21](https://github.com/thomasw21) for adding this dataset.
