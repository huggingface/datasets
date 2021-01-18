---
---

# Dataset Card for "social_bias_frames"

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

## [Dataset Description](#dataset-description)

- **Homepage:** [https://homes.cs.washington.edu/~msap/social-bias-frames/](https://homes.cs.washington.edu/~msap/social-bias-frames/)
- **Repository:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Paper:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Point of Contact:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Size of downloaded dataset files:** 6.03 MB
- **Size of the generated dataset:** 42.41 MB
- **Total amount of disk used:** 48.45 MB

### [Dataset Summary](#dataset-summary)

Social Bias Frames is a new way of representing the biases and offensiveness that are implied in language.
For example, these frames are meant to distill the implication that "women (candidates) are less qualified"
behind the statement "we shouldn’t lower our standards to hire more women."

### [Supported Tasks](#supported-tasks)

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### [Languages](#languages)

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

## [Dataset Structure](#dataset-structure)

We show detailed information for up to 5 configurations of the dataset.

### [Data Instances](#data-instances)

#### default

- **Size of downloaded dataset files:** 6.03 MB
- **Size of the generated dataset:** 42.41 MB
- **Total amount of disk used:** 48.45 MB

An example of 'validation' looks as follows.
```
{
    "HITId": "3Z8UJEJOCZ74QHXOTFP0JOOGD7039J",
    "WorkerId": "7162172225567546910",
    "annotatorAge": "27.0",
    "annotatorGender": "woman",
    "annotatorMinority": "women",
    "annotatorPolitics": "liberal",
    "annotatorRace": "white",
    "dataSource": "t/davidson",
    "intentYN": "1.0",
    "offensiveYN": "1.0",
    "post": "Every half-breed cop in America is trying to rape white women.",
    "sexPhrase": "rape white women",
    "sexReason": "rape",
    "sexYN": "1.0",
    "speakerMinorityYN": "0.0",
    "targetCategory": "race",
    "targetMinority": "mixed folks",
    "targetStereotype": "mixed folks are rapists.",
    "whoTarget": "1.0"
}
```

### [Data Fields](#data-fields)

The data fields are the same among all splits.

#### default
- `whoTarget`: a `string` feature.
- `intentYN`: a `string` feature.
- `sexYN`: a `string` feature.
- `sexReason`: a `string` feature.
- `offensiveYN`: a `string` feature.
- `annotatorGender`: a `string` feature.
- `annotatorMinority`: a `string` feature.
- `sexPhrase`: a `string` feature.
- `speakerMinorityYN`: a `string` feature.
- `WorkerId`: a `string` feature.
- `HITId`: a `string` feature.
- `annotatorPolitics`: a `string` feature.
- `annotatorRace`: a `string` feature.
- `annotatorAge`: a `string` feature.
- `post`: a `string` feature.
- `targetMinority`: a `string` feature.
- `targetCategory`: a `string` feature.
- `targetStereotype`: a `string` feature.
- `dataSource`: a `string` feature.

### [Data Splits Sample Size](#data-splits-sample-size)

| name  |train |validation|test |
|-------|-----:|---------:|----:|
|default|112900|     16738|17501|

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
@inproceedings{sap2020socialbiasframes,
   title={Social Bias Frames: Reasoning about Social and Power Implications of Language},
   author={Sap, Maarten and Gabriel, Saadia and Qin, Lianhui and Jurafsky, Dan and Smith, Noah A and Choi, Yejin},
   year={2020},
   booktitle={ACL},
}

```

