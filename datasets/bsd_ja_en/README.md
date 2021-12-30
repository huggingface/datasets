---
annotations_creators:
- expert-generated
language_creators:
- expert-generated
languages:
- en
- ja
licenses:
- cc-by-nc-sa-4.0
multilinguality:
- translation
size_categories:
- 10K<n<100K
source_datasets:
- original
task_categories:
- conditional-text-generation
task_ids:
- machine-translation
paperswithcode_id: business-scene-dialogue
---

# Dataset Card for Business Scene Dialogue 

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

- **Homepage:** [Github](https://raw.githubusercontent.com/tsuruoka-lab/BSD/)
- **Repository:** [Github](https://raw.githubusercontent.com/tsuruoka-lab/BSD/)
- **Paper:** [Rikters et al., 2019](https://www.aclweb.org/anthology/D19-5204)
- **Leaderboard:**
- **Point of Contact:** Matīss Rikters

### Dataset Summary
This is the Business Scene Dialogue (BSD) dataset, 
a Japanese-English parallel corpus containing written conversations
in various business scenarios. 

The dataset was constructed in 3 steps: 
  1) selecting business scenes, 
  2) writing monolingual conversation scenarios according to the selected scenes, and 
  3) translating the scenarios into the other language. 

Half of the monolingual scenarios were written in Japanese 
and the other half were written in English.


### Supported Tasks and Leaderboards

[More Information Needed]

### Languages
English, Japanese.

## Dataset Structure

### Data Instances
Each instance contains a conversation identifier, a sentence number that indicates its
position within the conversation, speaker name in English and Japanese, 
text in English and Japanese, original language, scene of the scenario (tag), 
and title of the scenario (title).
```python
		{
      "id": "190315_E004_13",
			"no": 14,
			"speaker": "Mr. Sam Lee",
			"ja_speaker": "サム リーさん",
			"en_sentence": "Would you guys consider a different scheme?",
			"ja_sentence": "別の事業案も考慮されますか？",
			"original_language": "en",
			"tag": "phone call",
			"title": "Phone: Review spec and scheme"
		}
```

### Data Fields
- id: dialogue identifier
- no: sentence pair number within a dialogue
- en_speaker: speaker name in English
- ja_speaker: speaker name in Japanese
- en_sentence: sentence in English
- ja_sentence: sentence in Japanese
- original_language: language in which monolingual scenario was written
- tag: scenario
- title: scenario title

### Data Splits
- There are a total of 24171 sentences /  808 business scenarios.
- Train: 20000 sentences / 670 scenarios
- Dev: 2051 sentences / 69 scenarios
- Test: 2120 sentences / 69 scenarios

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

[More Information Needed]

### Licensing Information
This dataset was released under the Creative Commons Attribution-NonCommercial-ShareAlike (CC BY-NC-SA) license.

### Citation Information
```
@inproceedings{rikters-etal-2019-designing,
    title = "Designing the Business Conversation Corpus",
    author = "Rikters, Mat{\=\i}ss  and
      Ri, Ryokan  and
      Li, Tong  and
      Nakazawa, Toshiaki",
    booktitle = "Proceedings of the 6th Workshop on Asian Translation",
    month = nov,
    year = "2019",
    address = "Hong Kong, China",
    publisher = "Association for Computational Linguistics",
    url = "https://www.aclweb.org/anthology/D19-5204",
    doi = "10.18653/v1/D19-5204",
    pages = "54--61"
}
```
### Contributions

Thanks to [@j-chim](https://github.com/j-chim) for adding this dataset.