---
annotations_creators:
- crowdsourced
- expert-generated
language_creators:
- crowdsourced
- expert-generated
languages:
- en
licenses:
- unknown
multilinguality:
- monolingual
size_categories:
- 1K<n<10K
source_datasets:
- extended|natural_questions
- extended|other-Common-Crawl
- original
task_categories:
- other
- question-answering
task_ids:
- abstractive-qa
- extractive-qa
- other-other-query-based-multi-document-summarization
paperswithcode_id: aquamuse
---

# Dataset Card for AQuaMuSe
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

- **Homepage:** https://github.com/google-research-datasets/aquamuse
- **Repository:** https://github.com/google-research-datasets/aquamuse
- **Paper:** https://arxiv.org/pdf/2010.12694.pdf
- **Leaderboard:**
- **Point of Contact:**

### Dataset Summary

AQuaMuSe is a novel scalable approach to automatically mine dual query based multi-document summarization datasets for extractive and abstractive summaries using question answering dataset (Google Natural Questions) and large document corpora (Common Crawl)

This dataset contains versions of automatically generated datasets for abstractive and extractive query-based multi-document summarization as described in [AQuaMuSe paper](https://arxiv.org/pdf/2010.12694.pdf).
### Supported Tasks and Leaderboards

- **Abstractive** and **Extractive** query-based multi-document summarization
- Question Answering

### Languages

en : English

## Dataset Structure

### Data Instances

- `input_urls`: a `list` of `string` features. 
- `query`: a `string` feature.
- `target`: a `string` feature


Example: 

```
{
    'input_urls': ['https://boxofficebuz.com/person/19653-charles-michael-davis'],
     'query': 'who is the actor that plays marcel on the originals',
     'target': "In February 2013, it was announced that Davis was cast in a lead role on The CW's new show The 
Originals, a spinoff of The Vampire Diaries, centered on the Original Family as they move to New Orleans, where 
Davis' character (a vampire named Marcel) currently rules."
}
```

### Data Fields

 - `input_urls`: a `list` of `string` features. 
  - List of URLs to input documents pointing to  [Common Crawl](https://commoncrawl.org/2017/07/june-2017-crawl-archive-now-available)  to be summarized. 
  - Dependencies: Documents URLs references the  [Common Crawl June 2017 Archive](https://commoncrawl.org/2017/07/june-2017-crawl-archive-now-available).
  
 - `query`: a `string` feature.
  - Input query to be used as summarization context. This is  derived from  [Natural Questions](https://ai.google.com/research/NaturalQuestions/)  user queries.
  
 -  `target`: a `string` feature
  - Summarization target, derived from  [Natural Questions](https://ai.google.com/research/NaturalQuestions/)  long answers.
### Data Splits
 - This dataset has two high-level configurations `abstractive` and `extractive`
 - Each configuration has the data splits of `train`, `dev` and `test`
 - The original format of the data was in [TFrecords](https://www.tensorflow.org/tutorials/load_data/tfrecord), which has been parsed to the format as specified in [Data Instances](#data-instances)
 
## Dataset Creation

### Curation Rationale

The dataset is automatically generated datasets for abstractive and extractive query-based multi-document summarization as described in [AQuaMuSe paper](https://arxiv.org/pdf/2010.12694.pdf).
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

The dataset curator is [sayalikulkarni](https://github.com/google-research-datasets/aquamuse/commits?author=sayalikulkarni), who is the contributor for the official GitHub repository for this dataset and also one of the authors of this dataset’s paper. As the account handles of other authors are not available currently who were also part of the curation of this dataset, the authors of the paper are mentioned here as follows, Sayali Kulkarni, Sheide Chammas, Wan Zhu, Fei Sha, and Eugene Ie.

### Licensing Information

[More Information Needed]

### Citation Information

@misc{kulkarni2020aquamuse,
      title={AQuaMuSe: Automatically Generating Datasets for Query-Based Multi-Document Summarization}, 
      author={Sayali Kulkarni and Sheide Chammas and Wan Zhu and Fei Sha and Eugene Ie},
      year={2020},
      eprint={2010.12694},
      archivePrefix={arXiv},
      primaryClass={cs.CL}
}

### Contributions

Thanks to [@Karthik-Bhaskar](https://github.com/Karthik-Bhaskar) for adding this dataset.