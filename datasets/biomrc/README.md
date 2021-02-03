---
---

# Dataset Card for "biomrc"

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

- **Homepage:** [http://nlp.cs.aueb.gr/](http://nlp.cs.aueb.gr/)
- **Repository:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Paper:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Point of Contact:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Size of downloaded dataset files:** 1226.28 MB
- **Size of the generated dataset:** 5539.64 MB
- **Total amount of disk used:** 6765.92 MB

### [Dataset Summary](#dataset-summary)

We introduce BIOMRC, a large-scale cloze-style biomedical MRC dataset. Care was taken to reduce noise, compared to the previous BIOREAD dataset of Pappas et al. (2018). Experiments show that simple heuristics do not perform well on the new dataset and that two neural MRC models that had been tested on BIOREAD perform much better on BIOMRC, indicating that the new dataset is indeed less noisy or at least that its task is more feasible. Non-expert human performance is also higher on the new dataset compared to BIOREAD, and biomedical experts perform even better. We also introduce a new BERT-based MRC model, the best version of which substantially outperforms all other methods tested, reaching or surpassing the accuracy of biomedical experts in some experiments. We make the new dataset available in three different sizes, also releasing our code, and providing a leaderboard.

### [Supported Tasks](#supported-tasks)

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### [Languages](#languages)

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

## [Dataset Structure](#dataset-structure)

We show detailed information for up to 5 configurations of the dataset.

### [Data Instances](#data-instances)

#### biomrc_large_A

- **Size of downloaded dataset files:** 389.18 MB
- **Size of the generated dataset:** 1831.85 MB
- **Total amount of disk used:** 2221.02 MB

An example of 'train' looks as follows.
```
This example was too long and was cropped:

{
    "abstract": "\"OBJECTIVES: @entity9 is a @entity10 that may result from greater occipital nerve entrapment. Entrapped peripheral nerves typica...",
    "answer": "@entity9 :: (MESH:D009437,Disease) :: ['unilateral occipital neuralgia']\n",
    "entities_list": ["@entity1 :: ('9606', 'Species') :: ['patients']", "@entity10 :: ('MESH:D006261', 'Disease') :: ['headache', 'Headache']", "@entity9 :: ('MESH:D009437', 'Disease') :: ['Occipital neuralgia', 'unilateral occipital neuralgia']"],
    "title": "Sonographic evaluation of the greater occipital nerve in XXXX .\n"
}
```

#### biomrc_large_B

- **Size of downloaded dataset files:** 327.17 MB
- **Size of the generated dataset:** 1469.61 MB
- **Total amount of disk used:** 1796.78 MB

An example of 'train' looks as follows.
```
This example was too long and was cropped:

{
    "abstract": "\"BACKGROUND: Adults with physical disabilities are less likely than others to receive @entity2 screening. It is not known, howev...",
    "answer": "@entity2",
    "entities_list": ["@entity2", "@entity1", "@entity0", "@entity3"],
    "title": "Does a standard measure of self-reported physical disability correlate with clinician perception of impairment related to XXXX screening?\n"
}
```

#### biomrc_small_A

- **Size of downloaded dataset files:** 65.69 MB
- **Size of the generated dataset:** 225.37 MB
- **Total amount of disk used:** 291.06 MB

An example of 'validation' looks as follows.
```
This example was too long and was cropped:

{
    "abstract": "\"PURPOSE: @entity120 ( @entity120 ) is a life-limiting @entity102 that presents as an elevated blood pressure in the pulmonary a...",
    "answer": "@entity148 :: (MESH:D001008,Disease) :: ['anxiety']\n",
    "entities_list": "[\"@entity1 :: ('9606', 'Species') :: ['patients']\", \"@entity308 :: ('MESH:D003866', 'Disease') :: ['depression']\", \"@entity146 :...",
    "title": "A predictive model of the effects of @entity308 , XXXX , stress, 6-minute-walk distance, and social support on health-related quality of life in an adult pulmonary hypertension population.\n"
}
```

#### biomrc_small_B

- **Size of downloaded dataset files:** 55.03 MB
- **Size of the generated dataset:** 180.84 MB
- **Total amount of disk used:** 235.87 MB

An example of 'train' looks as follows.
```
This example was too long and was cropped:

{
    "abstract": "\"Single-agent activity for @entity12 reflected by response rates of 10%-30% has been reported in @entity0 with @entity3 ( @entit...",
    "answer": "@entity10",
    "entities_list": ["@entity0", "@entity6", "@entity2", "@entity5", "@entity12", "@entity11", "@entity1", "@entity7", "@entity9", "@entity10", "@entity3", "@entity4", "@entity8"],
    "title": "No synergistic activity of @entity7 and XXXX in the treatment of @entity3 .\n"
}
```

#### biomrc_tiny_A

- **Size of downloaded dataset files:** 0.02 MB
- **Size of the generated dataset:** 0.07 MB
- **Total amount of disk used:** 0.09 MB

An example of 'test' looks as follows.
```
This example was too long and was cropped:

{
    "abstract": "\"OBJECTIVE: Decompressive craniectomy (DC) requires later cranioplasty (CP) in survivors. However, if additional ventriculoperit...",
    "answer": "@entity260 :: (MESH:D011183,Disease) :: ['Postoperative Complications']\n",
    "entities_list": ["@entity1 :: ('9606', 'Species') :: ['Patients', 'patients', 'Patient']", "@entity260 :: ('MESH:D011183', 'Disease') :: ['VPS regarding postoperative complications']", "@entity1276 :: ('MESH:D006849', 'Disease') :: ['hydrocephalus']"],
    "title": "Cranioplasty and Ventriculoperitoneal Shunt Placement after Decompressive Craniectomy: Staged Surgery Is Associated with Fewer XXXX .\n"
}
```

### [Data Fields](#data-fields)

The data fields are the same among all splits.

#### biomrc_large_A
- `abstract`: a `string` feature.
- `title`: a `string` feature.
- `entities_list`: a `list` of `string` features.
- `answer`: a `string` feature.

#### biomrc_large_B
- `abstract`: a `string` feature.
- `title`: a `string` feature.
- `entities_list`: a `list` of `string` features.
- `answer`: a `string` feature.

#### biomrc_small_A
- `abstract`: a `string` feature.
- `title`: a `string` feature.
- `entities_list`: a `list` of `string` features.
- `answer`: a `string` feature.

#### biomrc_small_B
- `abstract`: a `string` feature.
- `title`: a `string` feature.
- `entities_list`: a `list` of `string` features.
- `answer`: a `string` feature.

#### biomrc_tiny_A
- `abstract`: a `string` feature.
- `title`: a `string` feature.
- `entities_list`: a `list` of `string` features.
- `answer`: a `string` feature.

### [Data Splits Sample Size](#data-splits-sample-size)

#### biomrc_large_A

|              |train |validation|test |
|--------------|-----:|---------:|----:|
|biomrc_large_A|700000|     50000|62707|

#### biomrc_large_B

|              |train |validation|test |
|--------------|-----:|---------:|----:|
|biomrc_large_B|700000|     50000|62707|

#### biomrc_small_A

|              |train|validation|test|
|--------------|----:|---------:|---:|
|biomrc_small_A|87500|      6250|6250|

#### biomrc_small_B

|              |train|validation|test|
|--------------|----:|---------:|---:|
|biomrc_small_B|87500|      6250|6250|

#### biomrc_tiny_A

|             |test|
|-------------|---:|
|biomrc_tiny_A|  30|

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
@inproceedings{pappas-etal-2020-biomrc,
    title = "{B}io{MRC}: A Dataset for Biomedical Machine Reading Comprehension",
    author = "Pappas, Dimitris  and
      Stavropoulos, Petros  and
      Androutsopoulos, Ion  and
      McDonald, Ryan",
    booktitle = "Proceedings of the 19th SIGBioMed Workshop on Biomedical Language Processing",
    month = jul,
    year = "2020",
    address = "Online",
    publisher = "Association for Computational Linguistics",
    url = "https://www.aclweb.org/anthology/2020.bionlp-1.15",
    pages = "140--149",
    abstract = "We introduce BIOMRC, a large-scale cloze-style biomedical MRC dataset. Care was taken to reduce noise, compared to the previous BIOREAD dataset of Pappas et al. (2018). Experiments show that simple heuristics do not perform well on the new dataset and that two neural MRC models that had been tested on BIOREAD perform much better on BIOMRC, indicating that the new dataset is indeed less noisy or at least that its task is more feasible. Non-expert human performance is also higher on the new dataset compared to BIOREAD, and biomedical experts perform even better. We also introduce a new BERT-based MRC model, the best version of which substantially outperforms all other methods tested, reaching or surpassing the accuracy of biomedical experts in some experiments. We make the new dataset available in three different sizes, also releasing our code, and providing a leaderboard.",
}

```


### Contributions

Thanks to [@lewtun](https://github.com/lewtun), [@PetrosStav](https://github.com/PetrosStav), [@lhoestq](https://github.com/lhoestq), [@thomwolf](https://github.com/thomwolf) for adding this dataset.