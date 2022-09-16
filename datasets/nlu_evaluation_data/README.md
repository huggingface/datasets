---
annotations_creators:
- expert-generated
language_creators:
- expert-generated
language:
- en
license:
- cc-by-4.0
multilinguality:
- monolingual
size_categories:
- 10K<n<100K
source_datasets:
- original
task_categories:
- text-classification
task_ids:
- intent-classification
- multi-class-classification
paperswithcode_id: null
pretty_name: NLU Evaluation Data
---

# Dataset Card for NLU Evaluation Data

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

- **Homepage:** [Github](https://github.com/xliuhw/NLU-Evaluation-Data)
- **Repository:** [Github](https://github.com/xliuhw/NLU-Evaluation-Data)
- **Paper:** [ArXiv](https://arxiv.org/abs/1903.05566)
- **Leaderboard:**
- **Point of Contact:** [x.liu@hw.ac.uk](mailto:x.liu@hw.ac.uk)

### Dataset Summary

Dataset with short utterances from conversational domain annotated with their corresponding intents and scenarios.

It has 25 715 non-zero examples (original dataset has 25716 examples) belonging to 18 scenarios and 68 intents.
Originally, the dataset was crowd-sourced and annotated with both intents and named entities 
in order to evaluate commercial NLU systems such as RASA, IBM's Watson, Microsoft's LUIS and Google's Dialogflow.  
**This version of the dataset only includes intent annotations!**

In contrast to paper claims, released data contains 68 unique intents. This is due to the fact, that NLU systems were 
evaluated on more curated part of this dataset which only included 64 most important intents. Read more in [github issue](https://github.com/xliuhw/NLU-Evaluation-Data/issues/5).

### Supported Tasks and Leaderboards

Intent classification, intent detection

### Languages

English

## Dataset Structure

### Data Instances

An example of 'train' looks as follows:
```
{
  'label': 2, # integer label corresponding to "alarm_set" intent
  'scenario': 'alarm', 
  'text': 'wake me up at five am this week'
}
```

### Data Fields

- `text`: a string feature.
- `label`: one of classification labels (0-67) corresponding to unique intents.
- `scenario`: a string with one of unique scenarios (18).

Intent names are mapped to `label` in the following way:

|   label | intent                   |
|--------:|:-------------------------|
|       0 | alarm_query              |
|       1 | alarm_remove             |
|       2 | alarm_set                |
|       3 | audio_volume_down        |
|       4 | audio_volume_mute        |
|       5 | audio_volume_other       |
|       6 | audio_volume_up          |
|       7 | calendar_query           |
|       8 | calendar_remove          |
|       9 | calendar_set             |
|      10 | cooking_query            |
|      11 | cooking_recipe           |
|      12 | datetime_convert         |
|      13 | datetime_query           |
|      14 | email_addcontact         |
|      15 | email_query              |
|      16 | email_querycontact       |
|      17 | email_sendemail          |
|      18 | general_affirm           |
|      19 | general_commandstop      |
|      20 | general_confirm          |
|      21 | general_dontcare         |
|      22 | general_explain          |
|      23 | general_greet            |
|      24 | general_joke             |
|      25 | general_negate           |
|      26 | general_praise           |
|      27 | general_quirky           |
|      28 | general_repeat           |
|      29 | iot_cleaning             |
|      30 | iot_coffee               |
|      31 | iot_hue_lightchange      |
|      32 | iot_hue_lightdim         |
|      33 | iot_hue_lightoff         |
|      34 | iot_hue_lighton          |
|      35 | iot_hue_lightup          |
|      36 | iot_wemo_off             |
|      37 | iot_wemo_on              |
|      38 | lists_createoradd        |
|      39 | lists_query              |
|      40 | lists_remove             |
|      41 | music_dislikeness        |
|      42 | music_likeness           |
|      43 | music_query              |
|      44 | music_settings           |
|      45 | news_query               |
|      46 | play_audiobook           |
|      47 | play_game                |
|      48 | play_music               |
|      49 | play_podcasts            |
|      50 | play_radio               |
|      51 | qa_currency              |
|      52 | qa_definition            |
|      53 | qa_factoid               |
|      54 | qa_maths                 |
|      55 | qa_stock                 |
|      56 | recommendation_events    |
|      57 | recommendation_locations |
|      58 | recommendation_movies    |
|      59 | social_post              |
|      60 | social_query             |
|      61 | takeaway_order           |
|      62 | takeaway_query           |
|      63 | transport_query          |
|      64 | transport_taxi           |
|      65 | transport_ticket         |
|      66 | transport_traffic        |
|      67 | weather_query            |

### Data Splits

| Dataset statistics | Train |
| --- | --- |
| Number of examples | 25 715 |
| Average character length | 34.32 |
| Number of intents | 68 |
| Number of scenarios | 18 |

## Dataset Creation

### Curation Rationale

The dataset was prepared for a wide coverage evaluation and comparison of some of the most popular NLU services. 
At that time, previous benchmarks were done with few intents and spawning limited number of domains. Here, the dataset
is much larger and contains 68 intents from 18 scenarios, which is much larger that any previous evaluation. For more discussion see the paper. 

### Source Data

#### Initial Data Collection and Normalization

[More Information Needed]

#### Who are the source language producers?

[More Information Needed]

### Annotations

#### Annotation process

> To build the NLU component we collected real user data via Amazon Mechanical Turk (AMT). We designed tasks where the Turker’s goal was to answer questions about how people would interact with the home robot, in a wide range of scenarios designed in advance, namely: alarm, audio, audiobook, calendar, cooking, datetime, email, game, general, IoT, lists, music, news, podcasts, general Q&A, radio, recommendations, social, food takeaway, transport, and weather.
The questions put to Turkers were designed to capture the different requests within each given scenario. 
In the ‘calendar’ scenario, for example, these pre-designed intents were included: ‘set event’, ‘delete event’ and ‘query event’. 
An example question for intent ‘set event’ is: “How would you ask your PDA to schedule a meeting with someone?” for which a user’s answer example was “Schedule a chat with Adam on Thursday afternoon”. 
The Turkers would then type in their answers to these questions and select possible entities from the pre-designed suggested entities list for each of their answers.The Turkers didn’t always follow the instructions fully, e.g. for the specified ‘delete event’ Intent, an answer was: “PDA what is my next event?”; which clearly belongs to ‘query event’ Intent. 
We have manually corrected all such errors either during post-processing or the subsequent annotations.

#### Who are the annotators?

[More Information Needed]

### Personal and Sensitive Information

[More Information Needed]

## Considerations for Using the Data

### Social Impact of Dataset

The purpose of this dataset it to help develop better intent detection systems.

### Discussion of Biases

[More Information Needed]

### Other Known Limitations

[More Information Needed]

## Additional Information

### Dataset Curators

[More Information Needed]

### Licensing Information

Creative Commons Attribution 4.0 International License (CC BY 4.0)

### Citation Information
```
@InProceedings{XLiu.etal:IWSDS2019,
  author    = {Xingkun Liu, Arash Eshghi, Pawel Swietojanski and Verena Rieser},
  title     = {Benchmarking Natural Language Understanding Services for building Conversational Agents},
  booktitle = {Proceedings of the Tenth International Workshop on Spoken Dialogue Systems Technology (IWSDS)},
  month     = {April},
  year      = {2019},
  address   = {Ortigia, Siracusa (SR), Italy},
  publisher = {Springer},
  pages     = {xxx--xxx},
  url       = {http://www.xx.xx/xx/}
}
```
### Contributions

Thanks to [@dkajtoch](https://github.com/dkajtoch) for adding this dataset.
