---
annotations_creators:
- crowdsourced
language_creators:
- found
languages:
- en
licenses:
- other-Microsoft Research Data License
multilinguality:
- monolingual
size_categories:
- 1K<n<10K
source_datasets:
- extended|other-Open-American-National-Corpus-(OANC1)
task_categories:
- conditional-text-generation
task_ids:
- summarization
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

- **Homepage:** https://msropendata.com/datasets/f8ce2ec9-7fbd-48f7-a8bb-2d2279373563
- **Repository:**
- **Paper:** https://www.microsoft.com/en-us/research/wp-content/uploads/2016/09/Sentence_Compression_final-1.pdf
- **Leaderboard:**
- **Point of Contact:**

### Dataset Summary

This dataset contains sentences and short paragraphs with corresponding shorter (compressed) versions. There are up to five compressions for each input text, together with quality judgements of their meaning preservation and grammaticality. The dataset is derived using source texts from the Open American National Corpus (ww.anc.org) and crowd-sourcing.

### Supported Tasks and Leaderboards

Text Summarization

### Languages

English

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

```
{'domain': 'Newswire',
 'source_id': '106',
 'source_text': '" Except for this small vocal minority, we have just not gotten a lot of groundswell against this from members, " says APA president Philip G. Zimbardo of Stanford University.',
 'targets': {'compressed_text': ['"Except for this small vocal minority, we have not gotten a lot of groundswell against this," says APA president Zimbardo.',
   '"Except for a vocal minority, we haven\'t gotten much groundswell from members, " says Philip G. Zimbardo of Stanford University.',
   'APA president of Stanford has stated that except for a vocal minority they have not gotten a lot of pushback from members.',
   'APA president Philip G. Zimbardo of Stanford says they have not had much opposition against this.'],
  'judge_id': ['2', '22', '10', '0'],
  'num_ratings': [3, 3, 3, 3],
  'ratings': [[6, 6, 6], [11, 6, 6], [6, 11, 6], [6, 11, 11]]}}
```

- source_id: index of article per original dataset
- source_text: uncompressed original text
- domain: source of the article
- targets:
  - compressed_text: compressed version of `source_text`
  - judge_id: anonymized ids of crowdworkers who proposed compression
  - num_ratings: number of ratings available for each proposed compression
  - ratings: see table below

Ratings system (excerpted from authors' README):

- 6 =	Most important meaning Flawless language      (3 on meaning and 3 on grammar as per the paper's terminology)
- 7	= Most important meaning Minor errors           (3 on meaning and 2 on grammar)
- 9	= Most important meaning Disfluent or incomprehensible (3 on meaning and 1 on grammar)
- 11 = Much meaning Flawless language                (2 on meaning and 3 on grammar)
- 12 = Much meaning Minor errors                     (2 on meaning and 2 on grammar)
- 14 = Much meaning Disfluent or incomprehensible    (2 on meaning and 1 on grammar)
- 21 = Little or none meaning Flawless language      (1 on meaning and 3 on grammar)
- 22 = Little or none meaning Minor errors           (1 on meaning and 2 on grammar)
- 24 = Little or none meaning Disfluent or incomprehensible (1 on meaning and 1 on grammar)

See **README.txt** from data archive for additional details.

### Data Splits

There are 4,936 source texts in the training, 448 in the development, and 785 in the test set.

## Dataset Creation

### Annotations

#### Annotation process

Compressions were created using UHRS, an inhouse crowd-sourcing system similar to Amazon’s Mechanical Turk, in two annotation rounds, one for shortening and a second to rate compression quality:

1. In the first round, five workers were tasked with abridging each source text by at least 25%, while remaining grammatical and fluent, and retaining the meaning of the original.
2. In the second round, 3-5 judges (raters) were asked to evaluate the grammaticality of each compression on a scale from 1 (major errors, disfluent) through 3 (fluent), and again analogously for meaning preservation on a scale from 1 (orthogonal) through 3 (most important meaning-preserving).

## Additional Information

### Licensing Information

Microsoft Research Data License Agreement
### Citation Information

@inproceedings{Toutanova2016ADA,
  title={A Dataset and Evaluation Metrics for Abstractive Compression of Sentences and Short Paragraphs},
  author={Kristina Toutanova and Chris Brockett and Ke M. Tran and Saleema Amershi},
  booktitle={EMNLP},
  year={2016}
}

### Contributions

Thanks to [@jeromeku](https://github.com/jeromeku) for adding this dataset.