---
annotations_creators:
- no-annotation
language_creators:
- machine-generated
- expert-generated
languages:
- en
licenses:
- cc-by-4.0
multilinguality:
- monolingual
size_categories:
- 1M<n<10M
source_datasets:
- extended|yffc100M
task_categories:
- other
task_ids:
- other-image-self-supervised pretraining
paperswithcode_id: pass
pretty_name: Pictures without humAns for Self-Supervision
---

# Dataset Card for PASS

## Table of Contents
- [Table of Contents](#table-of-contents)
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

- **Homepage:** [PASS homepage](https://www.robots.ox.ac.uk/~vgg/research/pass/)
- **Repository:** [PASS repository](https://github.com/yukimasano/PASS)
- **Paper:** [PASS: An ImageNet replacement for self-supervised pretraining without humans](https://arxiv.org/abs/2109.13228)
- **Leaderboard:** [Pretrained models with scores](https://github.com/yukimasano/PASS#pretrained-models)
- **Point of Contact:** [Yuki M. Asano](mailto:yukiATMARKrobots.ox.ac.uk)

### Dataset Summary

PASS is a large-scale image dataset, containing 1.4 million images, that does not include any humans and which can be used for high-quality pretraining while significantly reducing privacy concerns.

### Supported Tasks and Leaderboards

From the paper:

> **Has the dataset been used for any tasks already?** In the paper we show and benchmark the
intended use of this dataset as a pretraining dataset. For this the dataset is used an unlabelled image collection on which visual features are learned and then transferred to downstream tasks. We show that with this dataset it is possible to learn competitive visual features, without any humans in the pretraining dataset and with complete license information.

> **Is there a repository that links to any or all papers or systems that use the dataset?** We will
be listing these at the repository.

> **What (other) tasks could the dataset be used for?** We believe this dataset might allow researchers and practitioners to further evaluate the differences that pretraining datasets can have on the learned features. Furthermore, since the meta-data is available for the images, it is possible to investigate the effect of image resolution on self-supervised learning methods, a domain largely underresearched thus far, as the current de-facto standard, ImageNet, only comes in one size.

> **Is there anything about the composition of the dataset or the way it was collected and preprocessed/cleaned/labeled that might impact future uses?** Given that this dataset is a subset of a dataset that randomly samples images from flickr, the image distribution is biased towards European and American creators. As in the main papers discussion, this can lead to non-generalizeable features, or even biased features as the images taken in other countries might be more likely to further reflect and propagate stereotypes [84], though in our case these do not refer to sterotypes about humans.

> **Are there tasks for which the dataset should not be used?** This dataset is meant for research
purposes only. The dataset should also not be used for, e.g. connecting images and usernames, as
this might risk de-anonymising the dataset in the long term. The usernames are solely provided for
attribution.

### Languages

English.

## Dataset Structure

### Data Instances

A data point comprises an image and its meta-data:

```
{
  'image': <PIL.JpegImagePlugin.JpegImageFile image mode=RGB size=500x375 at 0x7FFAD48E35F8>, 'creator_username': 'NTShieldsy',
  'hash': 'e1662344ffa8c231d198c367c692cc',
  'gps_latitude': 21.206675,
  'gps_longitude': 39.166558,
  'date_taken': datetime.datetime(2012, 8, 9, 18, 0, 20)
}
```

### Data Fields

- `image`: A `PIL.Image.Image` object containing the image. Note that when accessing the image column: `dataset[0]["image"]` the image file is automatically decoded. Decoding of a large number of image files might take a significant amount of time. Thus it is important to first query the sample index before the `"image"` column, *i.e.* `dataset[0]["image"]` should **always** be preferred over `dataset["image"][0]`.
- `creator_username`: The photographer.
- `hash`: The hash, as computed from YFCC-100M.
- `gps_latitude`: Latitude of image if existent, otherwise None.
- `gps_longitude`: Longitude of image if existent, otherwise None.
- `date_taken`: Datetime of image if existent, otherwise None.

### Data Splits

All the data is contained in training set. The training set has 1.4M (1,439,719) instances.

From the paper:

> **Are there recommended data splits (e.g., training, development/validation, testing)?** As outlined in the intended usecases, this dataset is meant for pretraining representations. As such, the models derived from training on this dataset need to be evaluated on different datasets, so called down-stream tasks. Thus the recommended split is to use all samples for training.

## Dataset Creation

### Curation Rationale

From the paper:

> **For what purpose was the dataset created?** Neural networks pretrained on large image collections have been shown to transfer well to other visual tasks where there is little labelled data, i.e. transferring a model works better than starting with a randomly initialized network every time for a new task, as many visual features can be repurposed. This dataset has as its goal to provide a safer large-scale dataset for such pretraining of visual features. In particular, this dataset does not contain any humans or human parts and does not contain any labels. The first point is important, as the current standard for pretraining, ImageNet and its face-blurred version only provide pseudo-anonymity and furthermore do not provide correct licences to the creators. The second point is relevant as pretraining is moving towards the self-supervised paradigm, where labels are not required. Yet most methods are developed on the highly curated ImageNet dataset, yielding potentially non-generalizeable research.

### Source Data

#### Initial Data Collection and Normalization

From the paper:

* **Collection process**:

    > **How was the data associated with each instance acquired?** The data was collected from the
    publicly available dataset YFCC-100M which is hosted on the AWS public datasets platform. We have used the meta-data, namely the copyright information to filter only images with the CC-BY licence and have downloaded these using the aws command line interface, allowing for quick and stable downloading. In addition, all files were subsequently scanned for viruses using Sophos SAVScan virus detection utility, v.5.74.0.

    > **What mechanisms or procedures were used to collect the data (e.g., hardware apparatus or sensor, manual human curation, software program, software API)?** Our dataset is a subset
    of the YFCC-100M dataset. The YFCC-100M dataset itself was created by effectively randomly
    selecting publicly available images from flickr, resulting in approximately 98M images.

    > **Does the dataset contain all possible instances or is it a sample (not necessarily random) of instances from a larger set?** The dataset is a sample of a larger set—all possible digital photographs. As outlined in Section 3 we start from an existing dataset, YFCC-100M, and stratify the images (removing images with people and personal information, removing images with harmful content, removing images with unsuitable licenses, each user contributes at most 80 images to the dataset). This leaves 1.6M images, out of which we take a random sample of 1.28M images to replicate the size of the ImageNet dataset. While this dataset can thus be extended, this is the set that we have verified to not contain humans, human parts and disturbing content.

    > **Over what timeframe was the data collected?** The images underlying the dataset were downloaded between March and June 2021 from the AWS public datasets’ S3 bucket, following the
    download code provided in the repo. However the images contained were originally and taken
    anywhere from 2000 to 2015, with the majority being shot between 2010-2014.

* **Preprocessing/cleaning/labeling**:

   > **Was any preprocessing/cleaning/labeling of the data done (e.g., discretization or bucketing,tokenization, part-of-speech tagging, SIFT feature extraction, removal of instances, processing of missing values)?** After the download of approx. 17M images, the corrupted, or single-color images were removed from the dataset prior to the generation of the dataset(s) used in the paper. The images were not further preprocessed or edited.

   > **Was the “raw” data saved in addition to the preprocessed/cleaned/labeled data (e.g., to support unanticipated future uses)?** Yes. The creators of the dataset maintain a copy of the 17M original images with the CC-BY licence of YFCC100M that sits at the start of our dataset creation pipeline. Is the software used to preprocess/clean/label the instances available? We have only used basic Python primitives for this. For the annotations we have used VIA [27, 28].

#### Who are the source language producers?

From the paper:

> **Who was involved in the data collection process (e.g., students, crowdworkers, contractors) and how were they compensated (e.g., how much were crowdworkers paid)?** As described, the data was collected automatically by simply downloading images from a publicly hosted S3 bucket. The human verification was done using a professional data annotation company that pays 150% of the local minimum wage.

### Annotations

#### Annotation process

This dataset doesn't contain annotations.

#### Who are the annotators?

This dataset doesn't contain annotations.

### Personal and Sensitive Information

From the paper:

> **Does the dataset contain data that might be considered confidential (e.g., data that is protected by legal privilege or by doctor-patient confidentiality, data that includes the content of individuals’ non-public communications)?** No.

> **Does the dataset contain data that, if viewed directly, might be offensive, insulting, threatening, or might otherwise cause anxiety?** No. Besides checking for human presence in the images, the annotators were also given the choice of flagging images for disturbing content, which once flagged was removed.

> **Does the dataset relate to people? If not, you may skip the remaining questions in this section.**
No.

> **Does the dataset identify any subpopulations (e.g., by age, gender)?** NA

> **Is it possible to identify individuals (i.e., one or more natural persons), either directly or indirectly (i.e., in combination with other data) from the dataset?** NA

> **Does the dataset contain data that might be considered sensitive in any way (e.g., data that reveals racial or ethnic origins, sexual orientations, religious beliefs, political opinions or union memberships, or locations; financial or health data; biometric or genetic data; forms of government identification, such as social security numbers; criminal history)?** NA

> **Were any ethical review processes conducted (e.g., by an institutional review board)?** No

## Considerations for Using the Data

### Social Impact of Dataset

[More Information Needed]

### Discussion of Biases

From the paper:

> **Is your dataset free of biases?** No. There are many kinds of biases that can either be quantified, e.g. geo-location (most images originate from the US and Europe) or camera-model (most images are taken with professional DSLR cameras not easily affordable), there are likely many more biases that this dataset does contain. The only thing that this dataset does not contain are humans and parts of humans, as far as our validation procedure is accurate.

### Other Known Limitations

From the paper:

> **Can you guarantee compliance to GDPR?** No, we cannot comment on legal issues.

## Additional Information

### Dataset Curators

YM. Asano, C. Rupprecht, A. Zisserman and A. Vedaldi.

From the paper:

> **Who created the dataset (e.g., which team, research group) and on behalf of which entity (e.g., company, institution, organization)?** The dataset has been constructued by the research group
“Visual Geometry Group” at the University of Oxford at the Engineering Science Department.

### Licensing Information

The PASS dataset is available to download for commercial/research purposes under a [Creative Commons Attribution 4.0 International License](https://creativecommons.org/licenses/by/4.0/). A complete version of the license can be found [here](https://www.robots.ox.ac.uk/~vgg/research/pass/license_pass.txt). The whole dataset only contains CC-BY licensed images with full attribution information.

### Citation Information

```bibtex
@Article{asano21pass,
author = "Yuki M. Asano and Christian Rupprecht and Andrew Zisserman and Andrea Vedaldi",
title = "PASS: An ImageNet replacement for self-supervised pretraining without humans",
journal = "NeurIPS Track on Datasets and Benchmarks",
year = "2021"
}
```

### Contributions

Thanks to [@mariosasko](https://github.com/mariosasko) for adding this dataset.