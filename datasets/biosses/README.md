---
annotations_creators:
- expert-generated
language_creators:
- found
languages:
- en
licenses:
- gpl-3.0
multilinguality:
- monolingual
size_categories:
- n<1K
source_datasets:
- original
task_categories:
- text-classification
task_ids:
- text-scoring
- semantic-similarity-scoring
paperswithcode_id: biosses
pretty_name: BIOSSES
---

# Dataset Card for BIOSSES

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

- **Homepage:** https://tabilab.cmpe.boun.edu.tr/BIOSSES/DataSet.html
- **Repository:** https://github.com/gizemsogancioglu/biosses
- **Paper:** [BIOSSES: a semantic sentence similarity estimation system for the biomedical domain](https://academic.oup.com/bioinformatics/article/33/14/i49/3953954)
- **Point of Contact:** [Gizem Soğancıoğlu](gizemsogancioglu@gmail.com) and [Arzucan Özgür](gizemsogancioglu@gmail.com)

### Dataset Summary

BIOSSES is a benchmark dataset for biomedical sentence similarity estimation. The dataset comprises 100 sentence pairs, in which each sentence was selected from the [TAC (Text Analysis Conference) Biomedical Summarization Track Training Dataset](https://tac.nist.gov/2014/BiomedSumm/) containing articles from the biomedical domain. The sentence pairs in BIOSSES were selected from citing sentences, i.e. sentences that have a citation to a reference article. 

The sentence pairs were evaluated by five different human experts that judged their similarity and gave scores ranging from 0 (no relation) to 4 (equivalent). In the original paper the mean of the scores assigned by the five human annotators was taken as the gold standard. The Pearson correlation between the gold standard scores and the scores estimated by the models was used as the evaluation metric. The strength of correlation can be assessed by the general guideline proposed by Evans (1996) as follows:

- very strong: 0.80–1.00
- strong: 0.60–0.79
- moderate: 0.40–0.59
- weak: 0.20–0.39
- very weak: 0.00–0.19


### Supported Tasks and Leaderboards

Biomedical Semantic Similarity Scoring.

### Languages

English.

## Dataset Structure

### Data Instances

For each instance, there are two sentences (i.e. sentence 1 and 2), and its corresponding similarity score (the mean of the scores assigned by the five human annotators).

```
{'sentence 1': 'Here, looking for agents that could specifically kill KRAS mutant cells, they found that knockdown of GATA2 was synthetically lethal with KRAS mutation'
 'sentence 2': 'Not surprisingly, GATA2 knockdown in KRAS mutant cells resulted in a striking reduction of active GTP-bound RHO proteins, including the downstream ROCK kinase'
 'score': 2.2}
```


### Data Fields

- `sentence 1`: string
- `sentence 2`: string
- `score`: float ranging from 0 (no relation) to 4 (equivalent)

### Data Splits

No data splits provided.

## Dataset Creation

### Curation Rationale

### Source Data

The [TAC (Text Analysis Conference) Biomedical Summarization Track Training Dataset](https://tac.nist.gov/2014/BiomedSumm/).

#### Initial Data Collection and Normalization

[More Information Needed]

#### Who are the source language producers?

[More Information Needed]

### Annotations

#### Annotation process

The sentence pairs were evaluated by five different human experts that judged their similarity and gave scores ranging from 0 (no relation) to 4 (equivalent). The score range was described based on the guidelines of SemEval 2012 Task 6 on STS (Agirre et al., 2012). Besides the annotation instructions, example sentences from the biomedical literature were provided to the annotators for each of the similarity degrees. 

The table below shows the Pearson correlation of the scores of each annotator with respect to the average scores of the remaining four annotators. It is observed that there is strong association among the scores of the annotators. The lowest correlations are 0.902, which can be considered as an upper bound for an algorithmic measure evaluated on this dataset.

|           |Correlation r  |
|----------:|--------------:|
|Annotator A|         	0.952|
|Annotator B|         	0.958|
|Annotator C|         	0.917|
|Annotator D|         	0.902|
|Annotator E|         	0.941|


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

- Gizem Soğancıoğlu, gizemsogancioglu@gmail.com 
- Hakime Öztürk, hakime.ozturk@boun.edu.tr
- Arzucan Özgür, gizemsogancioglu@gmail.com
Bogazici University, Istanbul, Turkey

### Licensing Information

BIOSSES is made available under the terms of [The GNU Common Public License v.3.0](https://www.gnu.org/licenses/gpl-3.0.en.html).

### Citation Information
@article{souganciouglu2017biosses,
  title={BIOSSES: a semantic sentence similarity estimation system for the biomedical domain},
  author={So{\u{g}}anc{\i}o{\u{g}}lu, Gizem and {\"O}zt{\"u}rk, Hakime and {\"O}zg{\"u}r, Arzucan},
  journal={Bioinformatics},
  volume={33},
  number={14},
  pages={i49--i58},
  year={2017},
  publisher={Oxford University Press}
}

### Contributions

Thanks to [@bwang482](https://github.com/bwang482) for adding this dataset.