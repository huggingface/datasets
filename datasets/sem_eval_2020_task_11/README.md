---
annotations_creators:
- expert-generated
language_creators:
- found
languages:
- en
licenses:
- unknown
multilinguality:
- monolingual
size_categories:
- n<1K
source_datasets:
- original
task_categories:
- text-classification
- structure-prediction
task_ids:
- text-classification-other-propaganda-technique-classification
- structure-prediction-other-propaganda-span-identification
paperswithcode_id: null
pretty_name: "SemEval-2020 Task 11"
---

# Dataset Card for SemEval-2020 Task 11

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

- **Homepage:** [PTC TASKS ON "DETECTION OF PROPAGANDA TECHNIQUES IN NEWS ARTICLES"](https://propaganda.qcri.org/ptc/index.html)
- **Paper:** [SemEval-2020 Task 11: Detection of Propaganda Techniques in News Articles](https://arxiv.org/abs/2009.02696)
- **Leaderboard:** [PTC Tasks Leaderboard](https://propaganda.qcri.org/ptc/leaderboard.php)
- **Point of Contact:** [Task organizers contact](semeval-2020-task-11-organizers@googlegroups.com)

### Dataset Summary

Propagandistic news articles use specific techniques to convey their message, such as whataboutism, red Herring, and name calling, among many others. The Propaganda Techniques Corpus (PTC) allows to study automatic algorithms to detect them. We provide a permanent leaderboard to allow researchers both to advertise their progress and to be up-to-speed with the state of the art on the tasks offered (see below for a definition).

### Supported Tasks and Leaderboards


More information on scoring methodology can be found in [propaganda tasks evaluation document](https://propaganda.qcri.org/ptc/data/propaganda_tasks_evaluation.pdf)

### Languages

This dataset consists of English news articles

## Dataset Structure

### Data Instances

Each example is structured as follows:

```
{
  "span_identification": {
    "end_char_offset": [720, 6322, ...],
    "start_char_offset": [683, 6314, ...]
  },
  "technique_classification": {
    "end_char_offset": [720,6322, ...],
    "start_char_offset": [683,6314, ...],
    "technique": [7,8, ...]
  },
  "text": "Newt Gingrich: The truth about Trump, Putin, and Obama\n\nPresident Trump..."
}

```

### Data Fields

- `text`: The full text of the news article.
- `span_identification`: a dictionary feature containing:
  - `start_char_offset`: The start character offset of the span for the SI task
  - `end_char_offset`: The end character offset of the span for the SI task
- `technique_classification`: a dictionary feature containing:
  - `start_char_offset`: The start character offset of the span for the TC task
  - `end_char_offset`: The start character offset of the span for the TC task
  - `technique`: the propaganda technique classification label, with possible values including `Appeal_to_Authority`, `Appeal_to_fear-prejudice`, `Bandwagon,Reductio_ad_hitlerum`, `Black-and-White_Fallacy`, `Causal_Oversimplification`.

### Data Splits

|                            | Train  | Valid | Test |
| -----                      | ------ | ----- | ---- |
| Input Sentences            |   371  |   75  |  90  |
| Total Annotations  SI      |  5468  |  940  |   0  |
| Total Annotations  TC      |  6128  | 1063  |   0  |

## Dataset Creation

### Curation Rationale

[More Information Needed]

### Source Data

#### Initial Data Collection and Normalization

In order to build the PTC-SemEval20 corpus, we retrieved a sample of news articles from the period
starting in mid-2017 and ending in early 2019. We selected 13 propaganda and 36 non-propaganda news
media outlets, as labeled by Media Bias/Fact Check,3
and we retrieved articles from these sources. We
deduplicated the articles on the basis of word n-grams matching (Barron-Cede ´ no and Rosso, 2009) and ˜
we discarded faulty entries (e.g., empty entries from blocking websites).

#### Who are the source language producers?

[More Information Needed]

### Annotations

#### Annotation process

The annotation job consisted of both spotting a propaganda snippet and, at the same time, labeling
it with a specific propaganda technique. The annotation guidelines are shown in the appendix; they
are also available online.4 We ran the annotation in two phases: (i) two annotators label an article
independently and (ii) the same two annotators gather together with a consolidator to discuss dubious
instances (e.g., spotted only by one annotator, boundary discrepancies, label mismatch, etc.). This protocol
was designed after a pilot annotation stage, in which a relatively large number of snippets had been spotted
by one annotator only. The annotation team consisted of six professional annotators from A Data Pro trained to spot and label the propaganda snippets from free text. The job was carried out on an instance of
the Anafora annotation platform (Chen and Styler, 2013), which we tailored for our propaganda annotation
task.
We evaluated the annotation process in terms of γ agreement (Mathet et al., 2015) between each of
the annotators and the final gold labels. The γ agreement on the annotated articles is on average 0.6;
see (Da San Martino et al., 2019b) for a more detailed discussion of inter-annotator agreement. The
training and the development part of the PTC-SemEval20 corpus are the same as the training and the
testing datasets described in (Da San Martino et al., 2019b). The test part of the PTC-SemEval20 corpus
consists of 90 additional articles selected from the same sources as for training and development. For
the test articles, we further extended the annotation process by adding one extra consolidation step: we
revisited all the articles in that partition and we performed the necessary adjustments to the spans and to
the labels as necessary, after a thorough discussion and convergence among at least three experts who
were not involved in the initial annotations.

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

```
@misc{martino2020semeval2020,
      title={SemEval-2020 Task 11: Detection of Propaganda Techniques in News Articles}, 
      author={G. Da San Martino and A. Barrón-Cedeño and H. Wachsmuth and R. Petrov and P. Nakov},
      year={2020},
      eprint={2009.02696},
      archivePrefix={arXiv},
      primaryClass={cs.CL}
}
```

### Contributions

Thanks to [@ZacharySBrown](https://github.com/ZacharySBrown) for adding this dataset.