---
annotations_creators:
- expert-generated
language_creators:
- expert-generated
language:
- en
language_bcp47:
- en-US
license:
- cc-by-sa-4.0
multilinguality:
- monolingual
paperswithcode_id: onestopqa
pretty_name: OneStopQA
size_categories:
- 1K<n<10K
source_datasets:
- original
- extended|onestop_english
task_categories:
- question-answering
task_ids:
- multiple-choice-qa
---

# Dataset Card for OneStopQA

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
  - [Contributions](#contributions)

## Dataset Description

- **Homepage:** [OneStopQA repository](https://github.com/berzak/onestop-qa)
- **Repository:** [OneStopQA repository](https://github.com/berzak/onestop-qa)
- **Paper:** [STARC: Structured Annotations for Reading Comprehension](https://arxiv.org/abs/2004.14797)
- **Leaderboard:** [Needs More Information]
- **Point of Contact:** [Needs More Information]

### Dataset Summary

OneStopQA is a multiple choice reading comprehension dataset annotated according to the STARC (Structured Annotations for Reading Comprehension) scheme. The reading materials are Guardian articles taken from the [OneStopEnglish corpus](https://github.com/nishkalavallabhi/OneStopEnglishCorpus). Each article comes in three difficulty levels, Elementary, Intermediate and Advanced. Each paragraph is annotated with three multiple choice reading comprehension questions. The reading comprehension questions can be answered based on any of the three paragraph levels.

### Supported Tasks and Leaderboards

[Needs More Information]

### Languages

English (`en-US`).

The original Guardian articles were manually converted from British to American English.

## Dataset Structure

### Data Instances

An example of instance looks as follows.

```json
{
  "title": "101-Year-Old Bottle Message",
  "paragraph": "Angela Erdmann never knew her grandfather. He died in 1946, six years before she was born. But, on Tuesday 8th April, 2014, she described the extraordinary moment when she received a message in a bottle, 101 years after he had lobbed it into the Baltic Sea. Thought to be the world’s oldest message in a bottle, it was presented to Erdmann by the museum that is now exhibiting it in Germany.",
  "paragraph_index": 1,
  "level": "Adv",
  "question": "How did Angela Erdmann find out about the bottle?", 
  "answers": ["A museum told her that they had it", 
              "She coincidentally saw it at the museum where it was held", 
              "She found it in her basement on April 28th, 2014", 
              "A friend told her about it"],
  "a_span": [56, 70], 
  "d_span": [16, 34]
}
```
Where, 

| Answer | Description                                                | Textual Span    |
|--------|------------------------------------------------------------|-----------------|
| a      | Correct answer.                                            | Critical Span   |
| b      | Incorrect answer. A miscomprehension of the critical span. | Critical Span   |
| c      | Incorrect answer. Refers to an additional span.            | Distractor Span |
| d      | Incorrect answer. Has no textual support.                  | -               |

The order of the answers in the `answers` list corresponds to the order of the answers in the table.

### Data Fields

- `title`: A `string` feature. The article title.
- `paragraph`: A `string` feature. The paragraph from the article. 
- `paragraph_index`: An `int` feature. Corresponds to the paragraph index in the article.
- `question`: A `string` feature. The given question.
- `answers`: A list of `string` feature containing the four possible answers.
- `a_span`: A list of start and end indices (inclusive) of the critical span.
- `d_span`: A list of start and end indices (inclusive) of the distractor span.

*Span indices are according to word positions after whitespace tokenization. 

**In the rare case where a span is spread over multiple sections, 
the span list will contain multiple instances of start and stop indices in the format:
  [start_1, stop_1, start_2, stop_2,...].


### Data Splits

Articles: 30  
Paragraphs: 162  
Questions: 486  
Question-Paragraph Level pairs: 1,458  

No preconfigured split is currently provided.


## Dataset Creation

### Curation Rationale

[Needs More Information]

### Source Data

#### Initial Data Collection and Normalization

[Needs More Information]

#### Who are the source language producers?

[Needs More Information]

### Annotations

#### Annotation process

The annotation and piloting process of the dataset is described in Appendix A in 
[STARC: Structured Annotations for Reading Comprehension](https://aclanthology.org/2020.acl-main.507.pdf).

#### Who are the annotators?

[Needs More Information]

### Personal and Sensitive Information

[Needs More Information]

## Considerations for Using the Data

### Social Impact of Dataset

[Needs More Information]

### Discussion of Biases

[Needs More Information]

### Other Known Limitations

[Needs More Information]

## Additional Information

### Dataset Curators

[Needs More Information]

### Licensing Information

<a rel="license" href="http://creativecommons.org/licenses/by-sa/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-sa/4.0/88x31.png" /></a><br />This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-sa/4.0/">Creative Commons Attribution-ShareAlike 4.0 International License</a>.

### Citation Information

[STARC: Structured Annotations for Reading Comprehension](http://people.csail.mit.edu/berzak/papers/acl2020.pdf)  
```
@inproceedings{starc2020,  
      author    = {Berzak, Yevgeni and Malmaud, Jonathan and Levy, Roger},  
      title     = {STARC: Structured Annotations for Reading Comprehension},  
      booktitle = {ACL},  
      year      = {2020},  
      publisher = {Association for Computational Linguistics} 
      }
```
### Contributions

Thanks to [@scaperex](https://github.com/scaperex) for adding this dataset.