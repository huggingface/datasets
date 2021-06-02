---
annotations_creators:
- expert-generated
language_creators:
- found
languages:
- pl
licenses:
- cc-by-nc-sa-1.0
multilinguality:
- monolingual
size_categories:
- 10K<n<100K
source_datasets:
- original
task_categories:
- text-classification
- text-scoring
task_ids:
- multi-class-classification
- multi-label-classification
- sentiment-classification
- sentiment-scoring
- topic-classification
paperswithcode_id: null
---


# Dataset Card for HateSpeechPl

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

- **Homepage:** http://zil.ipipan.waw.pl/HateSpeech
- **Repository:** [N/A]
- **Paper:** http://www.qualitativesociologyreview.org/PL/Volume38/PSJ_13_2_Troszynski_Wawer.pdf
- **Leaderboard:** [N/A]
- **Point of Contact:** [Marek Troszyński](mtroszynski@civitas.edu.pl), [Aleksander Wawer](axw@ipipan.waw.pl)

### Dataset Summary

The dataset was created to analyze the possibility of automating the recognition of hate speech in Polish. It was collected from the Polish forums and represents various types and degrees of offensive language, expressed towards minorities.

The original dataset is provided as an export of MySQL tables, what makes it hard to load. Due to that, it was converted to CSV and put to a Github repository. 

### Supported Tasks and Leaderboards

- `text-classification`: The dataset might be used to perform the text classification on different target fields, like the presence of irony/sarcasm, minority it describes or a topic. 
- `text-scoring`: The sentiment analysis is another task which might be solved on a dataset.

### Languages

Polish, collected from public forums, including the HTML formatting of the text.

## Dataset Structure

### Data Instances

The dataset consists of three collections, originally provided as separate MySQL tables. Here represented as three CSV files.

```
{
  'id': 1,
  'text_id': 121713,
  'annotator_id': 1,
  'minority_id': 72,
  'negative_emotions': false,
  'call_to_action': false,
  'source_of_knowledge': 2,
  'irony_sarcasm': false,
  'topic': 18,
  'text': ' <font color=\"blue\"> Niemiec</font> mówi co innego',
  'rating': 0
}
```

### Data Fields

List and describe the fields present in the dataset. Mention their data type, and whether they are used as input or output in any of the tasks the dataset currently supports. If the data has span indices, describe their attributes, such as whether they are at the character level or word level, whether they are contiguous or not, etc. If the datasets contains example IDs, state whether they have an inherent meaning, such as a mapping to other datasets or pointing to relationships between data points.

- `id`: unique identifier of the entry
- `text_id`: text identifier, useful when a single text is rated several times by different annotators
- `annotator_id`: identifier of the person who annotated the text
- `minority_id`: the internal identifier of the minority described in the text
- `negative_emotions`: boolean indicator of the presence of negative emotions in the text
- `call_to_action`: boolean indicator set to true, if the text calls the audience to perform any action, typically with a negative emotions
- `source_of_knowledge`: categorical variable, describing the source of knowledge for the post rating - 0, 1 or 2 (direct, lexical or contextual, but the description of the meaning for different values couldn't be found)
- `irony_sarcasm`: boolean indicator of the present of irony or sarcasm
- `topic`: internal identifier of the topic the text is about
- `text`: post text content
- `rating`: integer value, from 0 to 4 - the higher the value, the more negative the text content is

### Data Splits

The dataset was not originally split at all.

## Dataset Creation

### Curation Rationale

[More Information Needed]

### Source Data

The dataset was collected from the public forums.

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

The dataset doesn't contain any personal or sensitive information.

## Considerations for Using the Data

### Social Impact of Dataset

The automated hate speech recognition is the main beneficial outcome of using the dataset. 

### Discussion of Biases

The dataset contains negative posts only and due to that might underrepresent the whole language.

### Other Known Limitations

[More Information Needed]

## Additional Information

### Dataset Curators

The dataset was created by Marek Troszyński and Aleksander Wawer, during work done at [IPI PAN](https://www.ipipan.waw.pl/).

### Licensing Information

According to [Metashare](http://metashare.nlp.ipipan.waw.pl/metashare/repository/browse/polish-hatespeech-corpus/21b7e2366b0011e284b6000423bfd61cbc7616f601724f09bafc8a62c42d56de/), the dataset is licensed under CC-BY-NC-SA, but the version is not mentioned.

### Citation Information

```
@article{troszynski2017czy,
  title={Czy komputer rozpozna hejtera? Wykorzystanie uczenia maszynowego (ML) w jako{\'s}ciowej analizie danych},
  author={Troszy{\'n}ski, Marek and Wawer, Aleksandra},
  journal={Przegl{\k{a}}d Socjologii Jako{\'s}ciowej},
  volume={13},
  number={2},
  pages={62--80},
  year={2017},
  publisher={Uniwersytet {\L}{\'o}dzki, Wydzia{\l} Ekonomiczno-Socjologiczny, Katedra Socjologii~…}
}
```


### Contributions

Thanks to [@kacperlukawski](https://github.com/kacperlukawski) for adding this dataset.