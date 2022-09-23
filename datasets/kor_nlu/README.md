---
annotations_creators:
- found
language_creators:
- expert-generated
- found
- machine-generated
language:
- ko
license:
- cc-by-sa-4.0
multilinguality:
- monolingual
size_categories:
- 100K<n<1M
source_datasets:
- extended|snli
task_categories:
- text-classification
task_ids:
- natural-language-inference
- semantic-similarity-scoring
- text-scoring
paperswithcode_id: null
pretty_name: KorNlu
dataset_info:
- config_name: nli
  features:
  - name: premise
    dtype: string
  - name: hypothesis
    dtype: string
  - name: label
    dtype:
      class_label:
        names:
          0: entailment
          1: neutral
          2: contradiction
  splits:
  - name: test
    num_bytes: 1047250
    num_examples: 4954
  - name: train
    num_bytes: 80135707
    num_examples: 550146
  - name: validation
    num_bytes: 318170
    num_examples: 1570
  download_size: 80030037
  dataset_size: 81501127
- config_name: sts
  features:
  - name: genre
    dtype:
      class_label:
        names:
          0: main-news
          1: main-captions
          2: main-forum
          3: main-forums
  - name: filename
    dtype:
      class_label:
        names:
          0: images
          1: MSRpar
          2: MSRvid
          3: headlines
          4: deft-forum
          5: deft-news
          6: track5.en-en
          7: answers-forums
          8: answer-answer
  - name: year
    dtype:
      class_label:
        names:
          0: '2017'
          1: '2016'
          2: '2013'
          3: 2012train
          4: '2014'
          5: '2015'
          6: 2012test
  - name: id
    dtype: int32
  - name: score
    dtype: float32
  - name: sentence1
    dtype: string
  - name: sentence2
    dtype: string
  splits:
  - name: test
    num_bytes: 249671
    num_examples: 1379
  - name: train
    num_bytes: 1056664
    num_examples: 5703
  - name: validation
    num_bytes: 305009
    num_examples: 1471
  download_size: 1603824
  dataset_size: 1611344
---

# Dataset Card for [Dataset Name]

## Table of Contents
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

- **Homepage:** [Github](https://github.com/kakaobrain/KorNLUDatasets)
- **Repository:** [Github](https://github.com/kakaobrain/KorNLUDatasets)
- **Paper:** [Arxiv](https://arxiv.org/abs/2004.03289)
- **Leaderboard:**
- **Point of Contact:**

### Dataset Summary

[More Information Needed]

### Supported Tasks and Leaderboards

[More Information Needed]

### Languages

[More Information Needed]

## Dataset Structure

### Data Instances

[More Information Needed]

### Data Fields

[More Information Needed]

### Data Splits

[More Information Needed]

## Dataset Creation

### Curation Rationale

[More Information Needed]

### Source Data

#### Initial Data Collection and Normalization

[More Information Needed]

#### Who are the source language producers?

[More Information Needed]

### Annotations

#### Annotation process

[More Information Needed]

#### Who are the annotators?

[More Information Needed]

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

[More Information Needed]

### Licensing Information

[More Information Needed]

### Citation Information

[More Information Needed]
### Contributions

Thanks to [@sumanthd17](https://github.com/sumanthd17) for adding this dataset.