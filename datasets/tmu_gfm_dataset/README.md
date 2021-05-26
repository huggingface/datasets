---
annotations_creators:
- crowdsourced
language_creators:
- machine-generated
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
- conditional-text-generation
task_ids:
- conditional-text-generation-other-grammatical-error-correction
paperswithcode_id: null
---

# Dataset Card for TMU-GFM-Dataset

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

- **Homepage:** [N/A]
- **Repository:** https://github.com/tmu-nlp/TMU-GFM-Dataset
- **Paper:** [SOME: Reference-less Sub-Metrics Optimized for Manual Evaluations of Grammatical Error Correction](https://www.aclweb.org/anthology/2020.coling-main.573.pdf)
- **Leaderboard:** [N/A]
- **Point of Contact:** Check the paper.

### Dataset Summary

Authors collected manual evaluations for the grammaticality, fluency, and meaning preservation of the system outputs of 1,381 sentences from CoNLL 2013.
To collect the manual evaluations for various system outputs, each source sentence was corrected by the following five typical systems: statistical machine translation (SMT) (Grundkiewicz and Junczys-Dowmunt, 2018), recurrent neural network (RNN) (Luong et al., 2015), convolutional neural network (CNN) (Chollampatt and Ng, 2018), self-attention network (SAN) (Vaswani et al., 2017), and SAN with copy mechanism (SAN+Copy) (Zhao et al., 2019).
Manual evaluation for the grammaticality, fluency, and meaning preservation were assigned to a total of 4,223 sentences.

### Supported Tasks and Leaderboards

Grammatical Error Correction

### Languages

English

## Dataset Structure

### Data Instances

An example from the TMU-GFM-Dataset looks as follows:

```
{'ave_f': 3.4000000953674316,
 'ave_g': 3.4000000953674316,
 'ave_m': 3.5999999046325684,
 'fluency': [3, 4, 3, 4, 3],
 'grammer': [3, 4, 3, 4, 3],
 'meaning': [3, 4, 4, 4, 3],
 'output': 'After all, there will be an endless battle between the technology and human mentality.',
 'source': 'Afterall there will be an endless battle between the technology and human mentality.',
 'system': 'lstm,cnn'}
```

### Data Fields

The are 9 columns in the tmu-gfm-dataset.

- source: source sentence.
- output: system output sentence.
- grammer: Grammaticaliry annotations by 5 annotators.
- fluency: Fluency annotations by 5 annotators.
- meaning: Meaning Preservation annotations by 5 annotators.
- system: Which system the output sentence is from.
- ave_g: Average grammer score.
- ave_f: Average fluency score.
- ave_m: Average meaning score.

### Data Splits

Authors divided the dataset into train/dev/test with 3,376/422/423 sentences and used for fine-tuning BERT in thier paper.

## Dataset Creation

### Curation Rationale

The authors proposed a reference-less metric trained on manual evaluations of system outputs for grammatical error correction (GEC). 
They said that previous studies have shown that reference-less metrics are promising; however, existing metrics are not optimized for manual evaluation of the system output because there is no dataset of system output with manual evaluation.
To achieve a better correlation with manual evaluation, they created a dataset to optimize each sub-metric to the manual evaluation of GEC systems. Their annotators evaluated the output of five typical GEC systems.

### Source Data

#### Initial Data Collection and Normalization

Authors collected manual evaluations for the grammaticality, fluency, and meaning preservation of the system outputs of 1,381 sentences from CoNLL 2013.
To collect the manual evaluations for various system outputs, each source sentence was corrected by the following five typical systems: statistical machine translation (SMT) (Grundkiewicz and Junczys-Dowmunt, 2018), recurrent neural network (RNN) (Luong et al., 2015), convolutional neural network (CNN) (Chollampatt and Ng, 2018), self-attention network (SAN) (Vaswani et al., 2017), and SAN with copy mechanism (SAN+Copy) (Zhao et al., 2019).

#### Who are the source language producers?

machine-generated

### Annotations

#### Annotation process

By excluding duplicate corrected sentences, manual evaluation for the grammaticality, fluency, and meaning preservation were assigned to a total of 4,223 sentences, as follows: 
- Grammaticality: Annotators evaluated the grammatical correctness of the system output. The authors followed the five-point scale evaluation criteria (4: Perfect, 3: Comprehensible, 2: Somewhat comprehensible, 1: Incomprehensible, and 0: Other) proposed by Heilman et al. (2014). 
- Fluency: Annotators evaluated how natural the sentence sounds for native speakers. The authors followed the criteria (4: Extremely natural, 3: Somewhat natural, 2: Somewhat unnatural, and 1: Extremely unnatural) proposed by Lau et al. (2015). 
- Meaning preservation: Annotators evaluated the extent to which the meaning of source sentences is preserved in system output. The authors followed the criteria (4: Identical, 3: Minor differences, 2: Moderate differences, 1: Sub- stantially different, and 0: Other) proposed by Xu et al. (2016).

Finally, the authors created a dataset with manual evaluations for a total of 4,221 sentences, excluding sentences in which three or more annotators answered “0: Other.”

#### Who are the annotators?

Five native English annotators reqruited by using Amazon Mechaincal turk

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

@inproceedings{yoshimura-etal-2020-reference,
    title = "{SOME}: Reference-less Sub-Metrics Optimized for Manual Evaluations of Grammatical Error Correction",
    author = "Yoshimura, Ryoma  and
      Kaneko, Masahiro  and
      Kajiwara, Tomoyuki  and
      Komachi, Mamoru",
    booktitle = "Proceedings of the 28th International Conference on Computational Linguistics",
    month = dec,
    year = "2020",
    address = "Barcelona, Spain (Online)",
    publisher = "International Committee on Computational Linguistics",
    url = "https://www.aclweb.org/anthology/2020.coling-main.573",
    pages = "6516--6522",
    abstract = "We propose a reference-less metric trained on manual evaluations of system outputs for grammatical error correction (GEC). Previous studies have shown that reference-less metrics are promising; however, existing metrics are not optimized for manual evaluations of the system outputs because no dataset of the system output exists with manual evaluation. This study manually evaluates outputs of GEC systems to optimize the metrics. Experimental results show that the proposed metric improves correlation with the manual evaluation in both system- and sentence-level meta-evaluation. Our dataset and metric will be made publicly available.",
}

### Contributions

Thanks to [@forest1988](https://github.com/forest1988) for adding this dataset.