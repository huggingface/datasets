---
annotations_creators:
- no-annotation
language_creators:
- found
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
- summarization
---

# Dataset Card for SciTLDR

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

## Dataset Description

- **Homepage:** https://github.com/allenai/scitldr
- **Repository:** https://github.com/allenai/scitldr
- **Paper:** https://arxiv.org/abs/2004.15011
- **Leaderboard:** 
- **Point of Contact:** {isabelc,kylel,armanc,danw}@allenai.org

### Dataset Summary
`SciTLDR`: Extreme Summarization of Scientific Documents

SciTLDR is a new multi-target dataset of 5.4K TLDRs over 3.2K papers. SciTLDR contains both author-written and expert-derived TLDRs, where the latter are collected using a novel annotation protocol that produces high-quality summaries while minimizing annotation burden.

### Supported Tasks and Leaderboards

summarization

### Languages

English

## Dataset Structure

SciTLDR is split in to a 60/20/20 train/dev/test split. For each file, each line is a json, formatted as follows
```
{
   "source":[
      "sent0",
      "sent1",
      "sent2",
      ...
   ],
   "source_labels":[binary list in which 1 is the oracle sentence],
   "rouge_scores":[precomputed rouge-1 scores],
   "paper_id":"PAPER-ID",
   "target":[
     "author-tldr",
      "pr-tldr0", 
      "pr-tldr1",
      ... 
   ],
   "title":"TITLE"
}
```
The keys `rouge_scores` and `source_labels` are not necessary for any code to run, precomputed Rouge scores are provided for future research.

### Data Instances

{
    "source": [
        "Mixed precision training (MPT) is becoming a practical technique to improve the speed and energy efficiency of training deep neural networks by leveraging the fast hardware support for IEEE half-precision floating point that is available in existing GPUs.",
        "MPT is typically used in combination with a technique called loss scaling, that works by scaling up the loss value up before the start of backpropagation in order to minimize the impact of numerical underflow on training.",
        "Unfortunately, existing methods make this loss scale value a hyperparameter that needs to be tuned per-model, and a single scale cannot be adapted to different layers at different training stages.",
        "We introduce a loss scaling-based training method called adaptive loss scaling that makes MPT easier and more practical to use, by removing the need to tune a model-specific loss scale hyperparameter.",
        "We achieve this by introducing layer-wise loss scale values which are automatically computed during training to deal with underflow more effectively than existing methods.",
        "We present experimental results on a variety of networks and tasks that show our approach can shorten the time to convergence and improve accuracy, compared with using the existing state-of-the-art MPT and single-precision floating point."
    ],
    "source_labels": [
        0,
        0,
        0,
        1,
        0,
        0
    ],
    "rouge_scores": [
        0.2399999958000001,
        0.26086956082230633,
        0.19999999531250012,
        0.38095237636054424,
        0.2051282003944774,
        0.2978723360796741
    ],
    "paper_id": "rJlnfaNYvB",
    "target": [
        "We devise adaptive loss scaling to improve mixed precision training that surpass the state-of-the-art results.",
        "Proposal for an adaptive loss scaling method during backpropagation for mix precision training where scale rate is decided automatically to reduce the underflow.",
        "The authors propose a method to train models in FP16 precision that adopts a more elaborate way to minimize underflow in every layer simultaneously and automatically."
    ],
    "title": "Adaptive Loss Scaling for Mixed Precision Training"
}

### Data Fields

- `source`: The Abstract, Introduction and Conclusion (AIC) or Full text of the paper, with one sentence per line.
- `source_labels`: Binary 0 or 1, 1 denotes the oracle sentence.
- `rouge_scores`: Precomputed ROUGE baseline scores for each sentence.
- `paper_id`: Arxiv Paper ID.
- `target`: Multiple summaries for each sentence, one sentence per line.
- `title`: Title of the paper.
### Data Splits

|                   | train | valid  | test |
|-------------------|-------|--------|------|
| SciTLDR-A         | 1992  | 618    | 619  |
| SciTLDR-AIC       | 1992  | 618    | 619  |
| SciTLDR-FullText  | 1992  | 618    | 619  |

## Dataset Creation

[More Information Needed]

### Curation Rationale

[More Information Needed]

### Source Data

#### Initial Data Collection and Normalization

[More Information Needed]

#### Who are the source language producers?
https://allenai.org/

### Annotations

#### Annotation process

Given the title and first 128 words of a reviewer comment about a paper,
re-write the summary (if it exists) into a single sentence or an incomplete
phrase. Summaries must be no more than one sentence.
Most summaries are between 15 and 25 words. The average rewritten summary is
20 words long.

#### Who are the annotators?

[More Information Needed]

### Personal and Sensitive Information

[More Information Needed]

## Considerations for Using the Data

### Social Impact of Dataset

To encourage further research in the area of extreme summarization of scientific documents.

### Discussion of Biases

[More Information Needed]

### Other Known Limitations

[More Information Needed]

## Additional Information

### Dataset Curators

[More Information Needed]

### Licensing Information

Apache License 2.0

### Citation Information
@article{cachola2020tldr,
  title={{TLDR}: Extreme Summarization of Scientific Documents},
  author={Isabel Cachola and Kyle Lo and Arman Cohan and Daniel S. Weld},
  journal={arXiv:2004.15011},
  year={2020},
}
