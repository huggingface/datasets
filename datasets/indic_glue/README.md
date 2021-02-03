---
---

# Dataset Card for "indic_glue"

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

- **Homepage:** [https://indicnlp.ai4bharat.org/indic-glue/#natural-language-inference](https://indicnlp.ai4bharat.org/indic-glue/#natural-language-inference)
- **Repository:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Paper:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Point of Contact:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Size of downloaded dataset files:** 3351.18 MB
- **Size of the generated dataset:** 1573.33 MB
- **Total amount of disk used:** 4924.51 MB

### [Dataset Summary](#dataset-summary)

    IndicGLUE is a natural language understanding benchmark for Indian languages. It contains a wide
    variety of tasks and covers 11 major Indian languages - as, bn, gu, hi, kn, ml, mr, or, pa, ta, te.

The Winograd Schema Challenge (Levesque et al., 2011) is a reading comprehension task
in which a system must read a sentence with a pronoun and select the referent of that pronoun from
a list of choices. The examples are manually constructed to foil simple statistical methods: Each
one is contingent on contextual information provided by a single word or phrase in the sentence.
To convert the problem into sentence pair classification, we construct sentence pairs by replacing
the ambiguous pronoun with each possible referent. The task is to predict if the sentence with the
pronoun substituted is entailed by the original sentence. We use a small evaluation set consisting of
new examples derived from fiction books that was shared privately by the authors of the original
corpus. While the included training set is balanced between two classes, the test set is imbalanced
between them (65% not entailment). Also, due to a data quirk, the development set is adversarial:
hypotheses are sometimes shared between training and development examples, so if a model memorizes the
training examples, they will predict the wrong label on corresponding development set
example. As with QNLI, each example is evaluated separately, so there is not a systematic correspondence
between a model's score on this task and its score on the unconverted original task. We
call converted dataset WNLI (Winograd NLI). This dataset is translated and publicly released for 3
Indian languages by AI4Bharat.

### [Supported Tasks](#supported-tasks)

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### [Languages](#languages)

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

## [Dataset Structure](#dataset-structure)

We show detailed information for up to 5 configurations of the dataset.

### [Data Instances](#data-instances)

#### actsa-sc.te

- **Size of downloaded dataset files:** 0.36 MB
- **Size of the generated dataset:** 1.63 MB
- **Total amount of disk used:** 1.99 MB

An example of 'validation' looks as follows.
```
This example was too long and was cropped:

{
    "label": 0,
    "text": "\"ప్రయాణాల్లో ఉన్నవారికోసం బస్ స్టేషన్లు, రైల్వే స్టేషన్లలో పల్స్పోలియో బూతులను ఏర్పాటు చేసి చిన్నారులకు పోలియో చుక్కలు వేసేలా ఏర..."
}
```

#### bbca.hi

- **Size of downloaded dataset files:** 5.50 MB
- **Size of the generated dataset:** 26.35 MB
- **Total amount of disk used:** 31.85 MB

An example of 'train' looks as follows.
```
This example was too long and was cropped:

{
    "label": "pakistan",
    "text": "\"नेटिजन यानि इंटरनेट पर सक्रिय नागरिक अब ट्विटर पर सरकार द्वारा लगाए प्रतिबंधों के समर्थन या विरोध में अपने विचार व्यक्त करते है..."
}
```

#### copa.en

- **Size of downloaded dataset files:** 0.72 MB
- **Size of the generated dataset:** 0.11 MB
- **Total amount of disk used:** 0.83 MB

An example of 'validation' looks as follows.
```
{
    "choice1": "I swept the floor in the unoccupied room.",
    "choice2": "I shut off the light in the unoccupied room.",
    "label": 1,
    "premise": "I wanted to conserve energy.",
    "question": "effect"
}
```

#### copa.gu

- **Size of downloaded dataset files:** 0.72 MB
- **Size of the generated dataset:** 0.22 MB
- **Total amount of disk used:** 0.94 MB

An example of 'train' looks as follows.
```
This example was too long and was cropped:

{
    "choice1": "\"સ્ત્રી જાણતી હતી કે તેનો મિત્ર મુશ્કેલ સમયમાંથી પસાર થઈ રહ્યો છે.\"...",
    "choice2": "\"મહિલાને લાગ્યું કે તેના મિત્રએ તેની દયાળુ લાભ લીધો છે.\"...",
    "label": 0,
    "premise": "મહિલાએ તેના મિત્રની મુશ્કેલ વર્તન સહન કરી.",
    "question": "cause"
}
```

#### copa.hi

- **Size of downloaded dataset files:** 0.72 MB
- **Size of the generated dataset:** 0.22 MB
- **Total amount of disk used:** 0.94 MB

An example of 'validation' looks as follows.
```
{
    "choice1": "मैंने उसका प्रस्ताव ठुकरा दिया।",
    "choice2": "उन्होंने मुझे उत्पाद खरीदने के लिए राजी किया।",
    "label": 0,
    "premise": "मैंने सेल्समैन की पिच पर शक किया।",
    "question": "effect"
}
```

### [Data Fields](#data-fields)

The data fields are the same among all splits.

#### actsa-sc.te
- `text`: a `string` feature.
- `label`: a classification label, with possible values including `positive` (0), `negative` (1).

#### bbca.hi
- `label`: a `string` feature.
- `text`: a `string` feature.

#### copa.en
- `premise`: a `string` feature.
- `choice1`: a `string` feature.
- `choice2`: a `string` feature.
- `question`: a `string` feature.
- `label`: a `int32` feature.

#### copa.gu
- `premise`: a `string` feature.
- `choice1`: a `string` feature.
- `choice2`: a `string` feature.
- `question`: a `string` feature.
- `label`: a `int32` feature.

#### copa.hi
- `premise`: a `string` feature.
- `choice1`: a `string` feature.
- `choice2`: a `string` feature.
- `question`: a `string` feature.
- `label`: a `int32` feature.

### [Data Splits Sample Size](#data-splits-sample-size)

#### actsa-sc.te

|           |train|validation|test|
|-----------|----:|---------:|---:|
|actsa-sc.te| 4328|       541| 541|

#### bbca.hi

|       |train|test|
|-------|----:|---:|
|bbca.hi| 3467| 866|

#### copa.en

|       |train|validation|test|
|-------|----:|---------:|---:|
|copa.en|  400|       100| 500|

#### copa.gu

|       |train|validation|test|
|-------|----:|---------:|---:|
|copa.gu|  362|        88| 448|

#### copa.hi

|       |train|validation|test|
|-------|----:|---------:|---:|
|copa.hi|  362|        88| 449|

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
    @inproceedings{kakwani2020indicnlpsuite,
    title={{IndicNLPSuite: Monolingual Corpora, Evaluation Benchmarks and Pre-trained Multilingual Language Models for Indian Languages}},
    author={Divyanshu Kakwani and Anoop Kunchukuttan and Satish Golla and Gokul N.C. and Avik Bhattacharyya and Mitesh M. Khapra and Pratyush Kumar},
    year={2020},
    booktitle={Findings of EMNLP},
}

@inproceedings{kakwani2020indicnlpsuite,
title={{IndicNLPSuite: Monolingual Corpora, Evaluation Benchmarks and Pre-trained Multilingual Language Models for Indian Languages}},
author={Divyanshu Kakwani and Anoop Kunchukuttan and Satish Golla and Gokul N.C. and Avik Bhattacharyya and Mitesh M. Khapra and Pratyush Kumar},
year={2020},
booktitle={Findings of EMNLP},
}
@inproceedings{Levesque2011TheWS,
title={The Winograd Schema Challenge},
author={H. Levesque and E. Davis and L. Morgenstern},
booktitle={KR},
year={2011}
}

```


### Contributions

Thanks to [@sumanthd17](https://github.com/sumanthd17) for adding this dataset.