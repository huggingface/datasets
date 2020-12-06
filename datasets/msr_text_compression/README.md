---
YAML tags:
- copy-paste the tags obtained with the tagging app: http://34.68.228.168:8501/
---

# Dataset Card for [Dataset Name]

## Table of Contents
- [Dataset Card for [Dataset Name]](#dataset-card-for-dataset-name)
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

## Dataset Description

- **Homepage:** https://msropendata.com/datasets/f8ce2ec9-7fbd-48f7-a8bb-2d2279373563
- **Repository:**
- **Paper:** https://www.microsoft.com/en-us/research/wp-content/uploads/2016/09/Sentence_Compression_final-1.pdf
- **Leaderboard:**
- **Point of Contact:**

### Dataset Summary

This dataset contains sentences and short paragraphs with corresponding shorter (compressed) versions. There are up to five compressions for each input text, together with quality judgements of their meaning preservation and grammaticality. The dataset is derived using source texts from the Open American National Corpus (ww.anc.org) and crowd-sourcing.

### Supported Tasks and Leaderboards

[More Information Needed]

### Languages

[More Information Needed]

## Dataset Structure

### Data Instances

It contains approximately 6,000 source texts with multiple compressions (about 26,000 pairs of source and compressed texts), representing business letters, newswire, journals, and technical documents sampled from the Open American National Corpus (OANC1).

- Each source text is accompanied by up to five crowd-sourced rewrites constrained to a preset
compression ratio and annotated with quality judgments. Multiple rewrites permit study of the impact of operations on human compression quality and facilitate automatic evaluation.
- This dataset is the first to provide compressions at the multi-sentence (two-sentence paragraph)
level, which may present a stepping stone to whole document summarization.
- Many of these two-sentence paragraphs are compressed both as paragraphs and separately sentence-bysentence, offering data that may yield insights
into the impact of multi-sentence operations on human compression quality.

| Description       | Source | Target | Average CPS | Meaning Quality | Grammar Quality |
| :------------- | :----------: | -----------: | -----------: | -----------: | -----------: |
|  1-Sentence | 3764   | 15523    | 4.12 | 2.78 | 2.81 |
|  2-Sentence | 2405   | 10900    | 4.53 | 2.78 | 2.83 |

**Note**: Average CPS = Average Compressions per Source Text

### Data Fields

[More Information Needed]

### Data Splits

There are 4,936 source texts in the training, 448 in the development, and 785 in the test set.

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

Compressions were created using UHRS, an inhouse crowd-sourcing system similar to Amazon’s Mechanical Turk, in two annotation rounds, one for shortening and a second to rate compression quality:

1. In the first round, five workers were tasked with abridging each source text by at least 25%, while remaining grammatical and fluent, and retaining the meaning of the original.
2. In the second round, 3-5 judges (raters) were asked to evaluate the grammaticality of each compression on a scale from 1 (major errors, disfluent) through 3 (fluent), and again analogously for meaning preservation on a scale from 1 (orthogonal) through 3 (most important meaning-preserving).

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
