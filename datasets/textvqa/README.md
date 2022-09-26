---
annotations_creators:
- crowdsourced
language_creators:
- crowdsourced
language:
- en
license:
- cc-by-4.0
multilinguality:
- monolingual
pretty_name: TextVQA
size_categories:
- 10K<n<100K
source_datasets:
- original
task_categories:
- visual-question-answering
task_ids:
- visual-question-answering
---

# Dataset Card for TextVQA

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

A typical sample mainly contains the question in `question` field, an image object in `image` field, OpenImage image id in `image_id` and lot of other useful metadata. 10 answers per questions are contained in the `answers` attribute. For test set, 10 empty strings are contained in the `answers` field as the answers are not available for it.

An example look like below: 

```
  {'question': 'who is this copyrighted by?',
   'image_id': '00685bc495504d61',
   'image': <PIL.JpegImagePlugin.JpegImageFile image mode=RGB size=384x512 at 0x276021C5EB8>,
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

- `question`: string, the question that is being asked about the image
- `image_id`: string, id of the image which is same as the OpenImages id
- `image`: A `PIL.Image.Image` object containing the image about which the question is being asked. Note that when accessing the image column: `dataset[0]["image"]` the image file is automatically decoded. Decoding of a large number of image files might take a significant amount of time. Thus it is important to first query the sample index before the `"image"` column, *i.e.* `dataset[0]["image"]` should **always** be preferred over `dataset["image"][0]`.
- `image_classes`: List[str], The OpenImages classes to which the image belongs to.
- `flickr_original_url`: string, URL to original image on Flickr
- `flickr_300k_url`: string, URL to resized and low-resolution image on Flickr.
- `image_width`: int, Width of the original image.
- `image_height`: int, Height of the original image.
- `question_tokens`:  List[str], A pre-tokenized list of question.
- `answers`: List[str], List of 10 human-annotated answers for the question. These 10 answers are collected from 10 different users. The list will contain empty strings for test set for which we don't have the answers.
- `question_id`: int, Unique id of the question.
- `set_name`: string, the set to which this question belongs.

### Data Splits

There are three splits. `train`, `validation` and `test`. The `train` and `validation` sets share images with OpenImages `train` set and have their answers available. For test set answers, we return a list of ten empty strings. To get inference results and numbers on `test` set, you need to go to the [EvalAI leaderboard](https://eval.ai/web/challenges/challenge-page/874/overview) and upload your predictions there. Please see instructions at [https://textvqa.org/challenge/](https://textvqa.org/challenge/).

## Dataset Creation

### Curation Rationale

From the paper:

> Studies have shown that a dominant class of questions asked by visually impaired users on images of their surroundings involves reading text in the image. But today’s VQA models can not read! Our paper takes a first step towards addressing this problem. First, we introduce a new “TextVQA” dataset to facilitate progress on this important problem. Existing datasets either have a small proportion of questions about text (e.g., the VQA dataset) or are too small (e.g., the VizWiz dataset). TextVQA contains 45,336 questions on 28,408 images that require reasoning about text to answer.

### Source Data

#### Initial Data Collection and Normalization

The initial images were sourced from [OpenImages](https://storage.googleapis.com/openimages/web/factsfigures_v4.html) v4 dataset. These were first filtered based on automatic heuristics using an OCR system where we only took images which had at least some text detected in them. See [annotation process](#annotation-process) section to understand the next stages. 

#### Who are the source language producers?

English Crowdsource Annotators 

### Annotations

#### Annotation process

 After the automatic process of filter the images that contain text, the images were manually verified using human annotators making sure that they had text. In next stage, the annotators were asked to write questions involving scene text for the image. For some images, in this stage, two questions were collected whenever possible. Finally, in the last stage, ten different human annotators answer the questions asked in last stage.

#### Who are the annotators?

Annotators are from one of the major data collection platforms such as AMT. Exact details are not mentioned in the paper.

### Personal and Sensitive Information

The dataset does have similar PII issues as OpenImages and can at some times contain human faces, license plates, and documents. Using provided `image_classes` data field is one option to try to filter out some of this information.

## Considerations for Using the Data

### Social Impact of Dataset

The paper helped realize the importance of scene text recognition and reasoning in general purpose machine learning applications and has led to many follow-up works including [TextCaps](https://textvqa.org/textcaps) and [TextOCR](https://textvqa.org/textocr). Similar datasets were introduced over the time which specifically focus on sight-disabled users such as [VizWiz](https://vizwiz.org) or focusing specifically on the same problem as TextVQA like [STVQA](https://paperswithcode.com/dataset/st-vqa), [DocVQA](https://arxiv.org/abs/2007.00398v3) and [OCRVQA](https://ocr-vqa.github.io/). Currently, most methods train on combined dataset from TextVQA and STVQA to achieve state-of-the-art performance on both datasets.

### Discussion of Biases

Question-only bias where a model is able to answer the question without even looking at the image is discussed in the [paper](https://arxiv.org/abs/1904.08920) which was a major issue with original VQA dataset. The outlier bias in answers is prevented by collecting 10 different answers which are also taken in consideration by the evaluation metric.

### Other Known Limitations

- The dataset is english only but does involve images with non-English latin characters so can involve some multi-lingual understanding.
- The performance on the dataset is also dependent on the quality of OCR used as the OCR errors can directly lead to wrong answers.
- The metric used for calculating accuracy is same as [VQA accuracy](https://visualqa.org/evaluation.html). This involves one-to-one matching with the given answers and thus doesn't allow analyzing one-off errors through OCR.

## Additional Information

### Dataset Curators

- [Amanpreet Singh](https://github.com/apsdehal)
- Vivek Natarjan
- Meet Shah
- Yu Jiang
- Xinlei Chen
- Dhruv Batra
- Devi Parikh
- Marcus Rohrbach

### Licensing Information

CC by 4.0

### Citation Information

```bibtex
@inproceedings{singh2019towards,
    title={Towards VQA Models That Can Read},
    author={Singh, Amanpreet and Natarjan, Vivek and Shah, Meet and Jiang, Yu and Chen, Xinlei and Batra, Dhruv and Parikh, Devi and Rohrbach, Marcus},
    booktitle={Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition},
    pages={8317-8326},
    year={2019}
}
```

### Contributions

Thanks to [@apsdehal](https://github.com/apsdehal) for adding this dataset.