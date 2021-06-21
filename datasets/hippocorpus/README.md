---
annotations_creators:
- expert-generated
language_creators:
- expert-generated
languages:
- en
licenses:
- other-my-license
multilinguality:
- monolingual
size_categories:
- 1K<n<10K
source_datasets:
- original
task_categories:
- text-scoring
task_ids:
- text-scoring-other-narrative-flow
paperswithcode_id: null
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

- **Homepage:** [Hippocorpus](https://msropendata.com/datasets/0a83fb6f-a759-4a17-aaa2-fbac84577318)
- **Repository:** [Hippocorpus](https://msropendata.com/datasets/0a83fb6f-a759-4a17-aaa2-fbac84577318)
- **Paper:** [Recollection versus Imagination: Exploring Human Memory and Cognition via Neural Language Models](http://erichorvitz.com/cognitive_studies_narrative.pdf)
- **Point of Contact:** [Eric Horvitz](mailto:horvitz@microsoft.com)


### Dataset Summary
 
To examine the cognitive processes of remembering and imagining and their traces in language, we introduce Hippocorpus, a dataset of 6,854 English diary-like short stories about recalled and imagined events. Using a crowdsourcing framework, we first collect recalled stories and summaries from workers, then provide these summaries to other workers who write imagined stories. Finally, months later, we collect a retold version of the recalled stories from a subset of recalled authors. Our dataset comes paired with author demographics (age, gender, race), their openness to experience, as well as some variables regarding the author's relationship to the event (e.g., how personal the event is, how often they tell its story, etc.).

### Supported Tasks and Leaderboards

[More Information Needed]

### Languages

The dataset can be found in English

## Dataset Structure

[More Information Needed]

### Data Instances

[More Information Needed]

### Data Fields

This CSV file contains all the stories in Hippcorpus v2 (6854 stories)

These are the columns in the file:
- `AssignmentId`: Unique ID of this story
- `WorkTimeInSeconds`: Time in seconds that it took the worker to do the entire HIT (reading instructions, storywriting, questions)
- `WorkerId`: Unique ID of the worker (random string, not MTurk worker ID)
- `annotatorAge`: Lower limit of the age bucket of the worker. Buckets are: 18-24, 25-29, 30-34, 35-39, 40-44, 45-49, 50-54, 55+
- `annotatorGender`: Gender of the worker
- `annotatorRace`: Race/ethnicity of the worker
- `distracted`: How distracted were you while writing your story? (5-point Likert)
- `draining`: How taxing/draining was writing for you emotionally? (5-point Likert)
- `frequency`: How often do you think about or talk about this event? (5-point Likert)
- `importance`: How impactful, important, or personal is this story/this event to you? (5-point Likert)
- `logTimeSinceEvent`: Log of time (days) since the recalled event happened
- `mainEvent`: Short phrase describing the main event described
- `memType`: Type of story (recalled, imagined, retold)
- `mostSurprising`: Short phrase describing what the most surpring aspect of the story was
- `openness`: Continuous variable representing the openness to experience of the worker
- `recAgnPairId`: ID of the recalled story that corresponds to this retold story (null for imagined stories). Group on this variable to get the recalled-retold pairs.
- `recImgPairId`: ID of the recalled story that corresponds to this imagined story (null for retold stories). Group on this variable to get the recalled-imagined pairs.
- `similarity`: How similar to your life does this event/story feel to you? (5-point Likert)
- `similarityReason`: Free text annotation of similarity
- `story`: Story about the imagined or recalled event (15-25 sentences)
- `stressful`: How stressful was this writing task? (5-point Likert)
- `summary`: Summary of the events in the story (1-3 sentences)
- `timeSinceEvent`: Time (num. days) since the recalled event happened

### Data Splits

[More Information Needed]

## Dataset Creation

[More Information Needed]

### Curation Rationale

[More Information Needed]

### Source Data

[More Information Needed]

#### Initial Data Collection and Normalization

[More Information Needed]

#### Who are the source language producers?

[More Information Needed]

### Annotations

[More Information Needed]

#### Annotation process

[More Information Needed]

#### Who are the annotators?

[More Information Needed]

### Personal and Sensitive Information

[More Information Needed]

## Considerations for Using the Data

[More Information Needed]

### Social Impact of Dataset

[More Information Needed]

### Discussion of Biases

[More Information Needed]

### Other Known Limitations

[More Information Needed]

## Additional Information

[More Information Needed]

### Dataset Curators

The dataset was initially created by Maarten Sap, Eric Horvitz, Yejin Choi, Noah A. Smith, James W. Pennebaker, during work done at Microsoft Research.

### Licensing Information

Hippocorpus is distributed under the [Open Use of Data Agreement v1.0](https://msropendata-web-api.azurewebsites.net/licenses/f1f352a6-243f-4905-8e00-389edbca9e83/view).

### Citation Information

```
@inproceedings{sap-etal-2020-recollection,
    title = "Recollection versus Imagination: Exploring Human Memory and Cognition via Neural Language Models",
    author = "Sap, Maarten  and
      Horvitz, Eric  and
      Choi, Yejin  and
      Smith, Noah A.  and
      Pennebaker, James",
    booktitle = "Proceedings of the 58th Annual Meeting of the Association for Computational Linguistics",
    month = jul,
    year = "2020",
    address = "Online",
    publisher = "Association for Computational Linguistics",
    url = "https://www.aclweb.org/anthology/2020.acl-main.178",
    doi = "10.18653/v1/2020.acl-main.178",
    pages = "1970--1978",
    abstract = "We investigate the use of NLP as a measure of the cognitive processes involved in storytelling, contrasting imagination and recollection of events. To facilitate this, we collect and release Hippocorpus, a dataset of 7,000 stories about imagined and recalled events. We introduce a measure of narrative flow and use this to examine the narratives for imagined and recalled events. Additionally, we measure the differential recruitment of knowledge attributed to semantic memory versus episodic memory (Tulving, 1972) for imagined and recalled storytelling by comparing the frequency of descriptions of general commonsense events with more specific realis events. Our analyses show that imagined stories have a substantially more linear narrative flow, compared to recalled stories in which adjacent sentences are more disconnected. In addition, while recalled stories rely more on autobiographical events based on episodic memory, imagined stories express more commonsense knowledge based on semantic memory. Finally, our measures reveal the effect of narrativization of memories in stories (e.g., stories about frequently recalled memories flow more linearly; Bartlett, 1932). Our findings highlight the potential of using NLP tools to study the traces of human cognition in language.",
}
```

### Contributions

Thanks to [@manandey](https://github.com/manandey) for adding this dataset.