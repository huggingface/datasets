---
annotations_creators:
- expert-generated
language_creators:
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
- original
task_categories:
- structure-prediction
task_ids:
- named-entity-recognition
paperswithcode_id: ncbi-disease-1
pretty_name: NCBI Disease
---

# Dataset Card for NCBI Disease

## Table of Contents
- [Dataset Card for NCBI Disease](#dataset-card-for-ncbi-disease)
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
      - [Initial Data Collection and Normalization](#initial-data-collection-and-normalization)
      - [Who are the source language producers?](#who-are-the-source-language-producers)
    - [Annotations](#annotations)
      - [Annotation process](#annotation-process)
      - [Who are the annotators?](#who-are-the-annotators)
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

- **Homepage:** [NCBI](https://www.ncbi.nlm.nih.gov/research/bionlp/Data/disease)
- **Repository:** [Github](https://github.com/spyysalo/ncbi-disease)
- **Paper:** [NCBI disease corpus: A resource for disease name recognition and concept normalization](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3951655)
- **Leaderboard:** [Named Entity Recognition on NCBI-disease](https://paperswithcode.com/sota/named-entity-recognition-ner-on-ncbi-disease)
- **Point of Contact:** [email](zhiyong.lu@nih.gov)

### Dataset Summary

This dataset contains the disease name and concept annotations of the NCBI disease corpus, a collection of 793 PubMed abstracts fully annotated at the mention and concept level to serve as a research resource for the biomedical natural language processing community. 

### Supported Tasks and Leaderboards

Named Entity Recognition: [Leaderboard](https://paperswithcode.com/sota/named-entity-recognition-ner-on-ncbi-disease)

### Languages

The text in the dataset is in English. The associated BCP-47 code is `en`.

## Dataset Structure

### Data Instances

Instances of the dataset contain an array of `tokens`, `ner_tags` and an `id`. An example of an instance of the dataset:
```
{
  'tokens': ['Identification', 'of', 'APC2', ',', 'a', 'homologue', 'of', 'the', 'adenomatous', 'polyposis', 'coli', 'tumour', 'suppressor', '.'],
  'ner_tags': [0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 2, 2, 0, 0],
  'id': '0'
  }
```

### Data Fields

- `id`: Sentence identifier.  
- `tokens`: Array of tokens composing a sentence.  
- `ner_tags`: Array of tags, where `0` indicates no disease mentioned, `1` signals the first token of a disease and `2` the subsequent disease tokens.  

### Data Splits

The data is split into a train (5433 instances), validation (924 instances) and test set (941 instances).

## Dataset Creation

### Curation Rationale

 The goal of the dataset consists on improving the state-of-the-art in disease name recognition and normalization research, by providing a high-quality gold standard thus enabling the development of machine-learning based approaches for such tasks.

### Source Data

#### Initial Data Collection and Normalization

The dataset consists on abstracts extracted from PubMed.

#### Who are the source language producers?

The source language producers are the authors of publication abstracts hosted in PubMed.

### Annotations

#### Annotation process

 Each PubMed abstract was manually annotated by two annotators with disease mentions and their corresponding concepts in Medical Subject Headings (MeSH®) or Online Mendelian Inheritance in Man (OMIM®). Manual curation was performed using PubTator, which allowed the use of pre-annotations as a pre-step to manual annotations. Fourteen annotators were randomly paired and differing annotations were discussed for reaching a consensus in two annotation phases. Finally, all results were checked against annotations of the rest of the corpus to assure corpus-wide consistency.

#### Who are the annotators?

The annotator group consisted of 14 people with backgrounds in biomedical informatics research and experience in biomedical text corpus annotation.

### Personal and Sensitive Information

[N/A]

## Considerations for Using the Data

### Social Impact of Dataset

Information encoded in natural language in biomedical literature publications is only useful if efficient and reliable ways of accessing and analyzing that information are available. Natural language processing and text mining tools are therefore essential for extracting valuable information. This dataset provides an annotated corpora that can be used to develop highly effective tools to automatically detect central biomedical concepts such as diseases.

### Discussion of Biases

To avoid annotator bias, pairs of annotators were chosen randomly for each set, so that each pair of annotators overlapped for at most two sets.

### Other Known Limitations

A handful of disease concepts were discovered that were not included in MEDIC. For those, we decided to include the appropriate OMIM identifiers.

In addition, certain disease mentions were found to not be easily represented using the standard categorizations.

Also, each PMID document was pre-annotated using the Inference Method developed for disease name normalization, which properly handles abbreviation recognition, robust string matching, etc. As such, human annotators were given the pre-annotated documents as a starting point and allowed to see each pre-annotation with a computed confidence.

## Additional Information

### Dataset Curators

Rezarta Islamaj Doğan, Robert Leaman, Zhiyong Lu

### Licensing Information

```
PUBLIC DOMAIN NOTICE

This work is a "United States Government Work" under the terms of the
United States Copyright Act. It was written as part of the authors'
official duties as a United States Government employee and thus cannot
be copyrighted within the United States. The data is freely available
to the public for use. The National Library of Medicine and the
U.S. Government have not placed any restriction on its use or
reproduction.

Although all reasonable efforts have been taken to ensure the accuracy
and reliability of the data and its source code, the NLM and the
U.S. Government do not and cannot warrant the performance or results
that may be obtained by using it. The NLM and the U.S. Government
disclaim all warranties, express or implied, including warranties of
performance, merchantability or fitness for any particular purpose.

Please cite the authors in any work or product based on this material:

An improved corpus of disease mentions in PubMed citations
http://aclweb.org/anthology-new/W/W12/W12-2411.pdf

NCBI Disease Corpus: A Resource for Disease Name Recognition and
Normalization http://www.ncbi.nlm.nih.gov/pubmed/24393765

Disease Name Normalization with Pairwise Learning to Rank
http://www.ncbi.nlm.nih.gov/pubmed/23969135
```

### Citation Information

```
@article{dougan2014ncbi,
  title={NCBI disease corpus: a resource for disease name recognition and concept normalization},
  author={Do{\u{g}}an, Rezarta Islamaj and Leaman, Robert and Lu, Zhiyong},
  journal={Journal of biomedical informatics},
  volume={47},
  pages={1--10},
  year={2014},
  publisher={Elsevier}
}
```

### Contributions

Thanks to [@edugp](https://github.com/edugp) for adding this dataset.