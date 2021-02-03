---
---

# Dataset Card for "compguesswhat"

## Table of Contents
- [Dataset Description](#dataset-description)
  - [Dataset Summary](#dataset-summary)
  - [Supported Tasks](#supported-tasks)
  - [Languages](#languages)
- [Dataset Structure](#dataset-structure)
  - [Data Instances](#data-instances)
  - [Data Fields](#data-fields)
  - [Data Splits Sample Size](#data-splits-sample-size)
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

## [Dataset Description](#dataset-description)

- **Homepage:** [https://compguesswhat.github.io/](https://compguesswhat.github.io/)
- **Repository:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Paper:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Point of Contact:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Size of downloaded dataset files:** 106.86 MB
- **Size of the generated dataset:** 258.55 MB
- **Total amount of disk used:** 365.41 MB

### [Dataset Summary](#dataset-summary)

        CompGuessWhat?! is an instance of a multi-task framework for evaluating the quality of learned neural representations,
        in particular concerning attribute grounding. Use this dataset if you want to use the set of games whose reference
        scene is an image in VisualGenome. Visit the website for more details: https://compguesswhat.github.io

### [Supported Tasks](#supported-tasks)

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### [Languages](#languages)

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

## [Dataset Structure](#dataset-structure)

We show detailed information for up to 5 configurations of the dataset.

### [Data Instances](#data-instances)

#### compguesswhat-original

- **Size of downloaded dataset files:** 102.24 MB
- **Size of the generated dataset:** 166.29 MB
- **Total amount of disk used:** 268.53 MB

An example of 'validation' looks as follows.
```
This example was too long and was cropped:

{
    "id": 2424,
    "image": "{\"coco_url\": \"http://mscoco.org/images/270512\", \"file_name\": \"COCO_train2014_000000270512.jpg\", \"flickr_url\": \"http://farm6.stat...",
    "objects": "{\"area\": [1723.5133056640625, 4838.5361328125, 287.44476318359375, 44918.7109375, 3688.09375, 522.1935424804688], \"bbox\": [[5.61...",
    "qas": {
        "answer": ["Yes", "No", "No", "Yes"],
        "id": [4983, 4996, 5006, 5017],
        "question": ["Is it in the foreground?", "Does it have wings?", "Is it a person?", "Is it a vehicle?"]
    },
    "status": "success",
    "target_id": 1197044,
    "timestamp": "2016-07-08 15:07:38"
}
```

#### compguesswhat-zero_shot

- **Size of downloaded dataset files:** 4.62 MB
- **Size of the generated dataset:** 92.26 MB
- **Total amount of disk used:** 96.88 MB

An example of 'nd_valid' looks as follows.
```
This example was too long and was cropped:

{
    "id": 0,
    "image": {
        "coco_url": "https://s3.amazonaws.com/nocaps/val/004e21eb2e686f40.jpg",
        "date_captured": "2018-11-06 11:04:33",
        "file_name": "004e21eb2e686f40.jpg",
        "height": 1024,
        "id": 6,
        "license": 0,
        "open_images_id": "004e21eb2e686f40",
        "width": 768
    },
    "objects": "{\"IsOccluded\": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], \"IsTruncated\": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], \"area\": [3...",
    "status": "incomplete",
    "target_id": "004e21eb2e686f40_30"
}
```

### [Data Fields](#data-fields)

The data fields are the same among all splits.

#### compguesswhat-original
- `id`: a `int32` feature.
- `target_id`: a `int32` feature.
- `timestamp`: a `string` feature.
- `status`: a `string` feature.
- `id`: a `int32` feature.
- `file_name`: a `string` feature.
- `flickr_url`: a `string` feature.
- `coco_url`: a `string` feature.
- `height`: a `int32` feature.
- `width`: a `int32` feature.
- `width`: a `int32` feature.
- `height`: a `int32` feature.
- `url`: a `string` feature.
- `coco_id`: a `int32` feature.
- `flickr_id`: a `string` feature.
- `image_id`: a `string` feature.
- `qas`: a dictionary feature containing:
  - `question`: a `string` feature.
  - `answer`: a `string` feature.
  - `id`: a `int32` feature.
- `objects`: a dictionary feature containing:
  - `id`: a `int32` feature.
  - `bbox`: a `list` of `float32` features.
  - `category`: a `string` feature.
  - `area`: a `float32` feature.
  - `category_id`: a `int32` feature.
  - `segment`: a dictionary feature containing:
    - `feature`: a `float32` feature.

#### compguesswhat-zero_shot
- `id`: a `int32` feature.
- `target_id`: a `string` feature.
- `status`: a `string` feature.
- `id`: a `int32` feature.
- `file_name`: a `string` feature.
- `coco_url`: a `string` feature.
- `height`: a `int32` feature.
- `width`: a `int32` feature.
- `license`: a `int32` feature.
- `open_images_id`: a `string` feature.
- `date_captured`: a `string` feature.
- `objects`: a dictionary feature containing:
  - `id`: a `string` feature.
  - `bbox`: a `list` of `float32` features.
  - `category`: a `string` feature.
  - `area`: a `float32` feature.
  - `category_id`: a `int32` feature.
  - `IsOccluded`: a `int32` feature.
  - `IsTruncated`: a `int32` feature.
  - `segment`: a dictionary feature containing:
    - `MaskPath`: a `string` feature.
    - `LabelName`: a `string` feature.
    - `BoxID`: a `string` feature.
    - `BoxXMin`: a `string` feature.
    - `BoxXMax`: a `string` feature.
    - `BoxYMin`: a `string` feature.
    - `BoxYMax`: a `string` feature.
    - `PredictedIoU`: a `string` feature.
    - `Clicks`: a `string` feature.

### [Data Splits Sample Size](#data-splits-sample-size)

#### compguesswhat-original

|                      |train|validation|test|
|----------------------|----:|---------:|---:|
|compguesswhat-original|46341|      9738|9621|

#### compguesswhat-zero_shot

|                       |nd_valid|od_valid|nd_test|od_test|
|-----------------------|-------:|-------:|------:|------:|
|compguesswhat-zero_shot|    5343|    5372|  13836|  13300|

## [Dataset Creation](#dataset-creation)

### [Curation Rationale](#curation-rationale)

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### [Source Data](#source-data)

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### [Annotations](#annotations)

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### [Personal and Sensitive Information](#personal-and-sensitive-information)

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

## [Considerations for Using the Data](#considerations-for-using-the-data)

### [Social Impact of Dataset](#social-impact-of-dataset)

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### [Discussion of Biases](#discussion-of-biases)

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### [Other Known Limitations](#other-known-limitations)

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

## [Additional Information](#additional-information)

### [Dataset Curators](#dataset-curators)

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### [Licensing Information](#licensing-information)

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### [Citation Information](#citation-information)

```
        @inproceedings{suglia2020compguesswhat,
          title={CompGuessWhat?!: a Multi-task Evaluation Framework for Grounded Language Learning},
          author={Suglia, Alessandro, Konstas, Ioannis, Vanzo, Andrea, Bastianelli, Emanuele, Desmond Elliott, Stella Frank and Oliver Lemon},
          booktitle={Proceedings of the 58th Annual Meeting of the Association for Computational Linguistics},
          year={2020}
        }

```


### Contributions

Thanks to [@thomwolf](https://github.com/thomwolf), [@aleSuglia](https://github.com/aleSuglia), [@lhoestq](https://github.com/lhoestq) for adding this dataset.