---
annotations_creators:
- crowdsourced
language_creators:
- crowdsourced
languages:
- en-US
licenses:
- cc-by-4.0
multilinguality:
- monolingual
pretty_name: TextVQA
size_categories:
- unknown
source_datasets:
- original
task_categories:
- question-answering
task_ids:
- visual-question-answering
---

# Dataset Card for [Needs More Information]

## Table of Contents
- [Dataset Description](#dataset-description)
  - [Dataset Summary](#dataset-summary)
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
  - [Contributions](#contributions)

## Dataset Description

- **Homepage:** https://textvqa.org
- **Repository:** https://github.com/facebookresearch/mmf
- **Paper:** https://arxiv.org/abs/1904.08920
- **Leaderboard:** https://eval.ai/web/challenges/challenge-page/874/overview
- **Point of Contact:** mailto:amanpreet@nyu.edu

### Dataset Summary

TextVQA requires models to read and reason about text in images to answer questions about them.
Specifically, models need to incorporate a new modality of text present in the images and reason
over it to answer TextVQA questions. TextVQA dataset contains 45,336 questions over 28,408 images
from the OpenImages dataset. The dataset uses [VQA accuracy](https://visualqa.org/evaluation.html) metric for evaluation.

### Supported Tasks and Leaderboards

- `visual-question-answering`: The dataset can be used for Visual Question Answering tasks where given an image, you have to answer a question based on the image. For the TextVQA dataset specifically, the questions require reading and reasoning about the scene text in the given image.

### Languages

The questions in the dataset are in English.

## Dataset Structure

### Data Instances

A typical sample mainly contains the question in `question` field, an image object in `image` field, OpenImage image id in `image_id` and lot of other useful metadata. 10 answers per questions are contained in the `answers` attribute.

An example look like below: 

```
  {'question': 'who is this copyrighted by?',
   'image_id': '00685bc495504d61',
   'image': 
   'image_classes': ['Vehicle', 'Tower', 'Airplane', 'Aircraft'],
   'flickr_original_url': 'https://farm2.staticflickr.com/5067/5620759429_4ea686e643_o.jpg',
   'flickr_300k_url': 'https://c5.staticflickr.com/6/5067/5620759429_f43a649fb5_z.jpg',
   'image_width': 786,
   'image_height': 1024,
   'answers': ['simon clancy',
    'simon ciancy',
    'simon clancy',
    'simon clancy',
    'the brand is bayard',
    'simon clancy',
    'simon clancy',
    'simon clancy',
    'simon clancy',
    'simon clancy'],
   'question_tokens': ['who', 'is', 'this', 'copyrighted', 'by'],
   'question_id': 3,
   'set_name': 'train'
  },
```

### Data Fields

{
      "question_id": "INT, incremental unique ID for the question",
      "question": "what is ....?",
      "question_tokens": [
        "token_1",
        "token_2",
        "...",
        "token_N"
      ],
      "image_id": "OpenImages Image ID",
      "image_classes": [
        "OpenImages_class_1",
        "OpenImages_class_2",
        "...",
        "OpenImages_class_n"
      ],
      "flickr_original_url": "OpenImages original flickr url",
      "flickr_300k_url": "OpenImages flickr 300k thumbnail url",
      "image_width": "INT, Width of the image",
      "image_height": "INT, Height of the image",
      "set_name": "Dataset split question belongs to",
      "answers": [
        "answer_1",
        "answer_2",
        "...",
        "answer_10"
      ]
}

### Data Splits

There are three splits. `train`, `validation` and `test`. `train` and `validation` share images and have their answers available. For test set predictions, you need to go to the [EvalAI leaderboard] and upload your predictions there. Please see instructions at [https://textvqa.org/challenge/](https://textvqa.org/challenge/).

## Dataset Creation

### Curation Rationale

[Needs More Information]

### Source Data

#### Initial Data Collection and Normalization

[Needs More Information]

#### Who are the source language producers?

English Crowdsource Annotators 

### Annotations

#### Annotation process

See the [paper](https://arxiv.org/abs/1904.08920).

#### Who are the annotators?

See the [paper](https://arxiv.org/abs/1904.08920).

### Personal and Sensitive Information

See the [paper](https://arxiv.org/abs/1904.08920).

## Considerations for Using the Data

### Social Impact of Dataset

See the [paper](https://arxiv.org/abs/1904.08920).

### Discussion of Biases

See the [paper](https://arxiv.org/abs/1904.08920).

### Other Known Limitations

See the [paper](https://arxiv.org/abs/1904.08920).

## Additional Information

### Dataset Curators

[Amanpreet Singh](https://github.com/apsdehal)

### Licensing Information

CC by 4.0

### Citation Information

```
@inproceedings{singh2019towards,
    title={Towards VQA Models That Can Read},
    author={Singh, Amanpreet and Natarjan, Vivek and Shah, Meet and Jiang, Yu and Chen, Xinlei and Parikh, Devi and Rohrbach, Marcus},
    booktitle={Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition},
    pages={8317-8326},
    year={2019}
}
```

### Contributions

Thanks to [@apsdehal](https://github.com/apsdehal) for adding this dataset.