---
annotations_creators:
- found
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
task_ids:
- intent-classification
paperswithcode_id: null
---

# Dataset Card for HateOffensive

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
- **Homepage** : https://sites.google.com/view/qanta/projects/diplomacy
- **Repository** : https://github.com/DenisPeskov/2020_acl_diplomacy
- **Paper** : http://users.umiacs.umd.edu/~jbg/docs/2020_acl_diplomacy.pdf
- **Leaderboard** : 
- **Point of Contact** : 

### Dataset Summary
This dataset contains pairwise conversations annotated by the sender and the receiver for deception (and conversely truthfulness). The 17,289 messages are gathered from 12 games.

### Supported Tasks and Leaderboards
[More Information Needed]

### Languages
English

## Dataset Structure
### Data Instances
```
{
"messages": 
["Greetings Sultan!\n\nAs your neighbor I would like to propose an alliance! What are your views on the board so far?", "I think an alliance would be great! Perhaps a dmz in the Black Sea would be a good idea to solidify this alliance?\n\nAs for my views on the board, my first moves will be Western into the Balkans and Mediterranean Sea.", "Sounds good lets call a dmz in the black sea", "What's our move this year?", "I've been away from the game for a while", "Not sure yet, what are your thoughts?", "Well I'm pretty worried about Germany attacking me (and Austria to a lesser extent) so im headed west. It looks like Italy's landing a army in Syr this fall unless you can stop it", "That sounds good to me. I'll move to defend against Italy while you move west. If it's not too much too ask, I'd like to request that you withdraw your fleet from bla.", "Oh sorry missed the msg to move out of bl sea ill do that this turn. I did bring my army down into Armenia, To help you expel the Italian. It looks like Austria and Italy are working together. If we have a chance in the region you should probably use smy to protect con. We can't afford to lose con.", "I'll defend con from both ank and smy.", "Hey sorry for stabbing you earlier, it was an especially hard choice since Turkey is usually my country of choice. It's cool we got to do this study huh?"], 
"sender_labels": [false, true, false, true, true, true, true, true, true, true, true], 
"receiver_labels": [true, true, true, true, true, true, true, true, true, true, "NOANNOTATION"], 
"speakers": ["russia", "turkey", "russia", "russia", "russia", "turkey", "russia", "turkey", "russia", "turkey", "russia"], 
"receivers": ["turkey", "russia", "turkey", "turkey", "turkey", "russia", "turkey", "russia", "turkey", "russia", "turkey"], 
"absolute_message_index": [78, 107, 145, 370, 371, 374, 415, 420, 495, 497, 717], 
"relative_message_index": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 
"seasons": ["Spring", "Spring", "Spring", "Spring", "Spring", "Spring", "Fall", "Fall", "Spring", "Spring", "Fall"], 
"years": ["1901", "1901", "1901", "1902", "1902", "1902", "1902", "1902", "1903", "1903", "1905"], 
"game_score": ["4", "3", "4", "5", "5", "4", "5", "4", "5", "3", "7"],
"game_score_delta": ["1", "-1", "1", "1", "1", "-1", "1", "-1", "2", "-2", "7"], 
"players": ["russia", "turkey"], 
"game_id": 10
}
```

### Data Fields
- speakers: the sender of the message (string format. Seven possible values: russia, turkey, england, austria, germany, france, italy)
- receivers: the receiver of the message (string format. Seven possible values: russia, turkey, england, austria, germany, france, italy)
- messages: the raw message string (string format. ranges in length from one word to paragraphs in length)
- sender_labels: indicates if the sender of the message selected that the message is truthful, true, or deceptive, false. This is used for our ACTUAL_LIE calculation (true/false which can be bool or string format)
- receiver_labels: indicates if the receiver of the message selected that the message is perceived as truthful, true, or deceptive, false. In <10% of the cases, no annotation was received. This is used for our SUSPECTED_LIE calculation (string format. true/false/"NOANNOTATION" )
- game_score: the current game score---supply centers---of the sender (string format that ranges can range from 0 to 18)
- game_score_delta: the current game score---supply centers---of the sender minus the game score of the recipient (string format that ranges from -18 to 18)
- absolute_message_index: the index the message is in the entire game, across all dialogs (int format)
- relative_message_index: the index of the message in the current dialog (int format)
- seasons: the season in Diplomacy, associated with the year (string format. Spring, Fall, Winter)
- years: the year in Diplomacy, associated with the season (string format. 1901 through 1918)
- game_id: which of the 12 games the dialog comes from (int format ranging from 1 to 12)

### Data Splits
Train, Test and Validation splits

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
Unknown

### Citation Information
@inproceedings{Peskov:Cheng:Elgohary:Barrow:Danescu-Niculescu-Mizil:Boyd-Graber-2020,
Title = {It Takes Two to Lie: One to Lie and One to Listen},
Author = {Denis Peskov and Benny Cheng and Ahmed Elgohary and Joe Barrow    and Cristian Danescu-Niculescu-Mizil and Jordan Boyd-Graber},
Booktitle = {Association for Computational Linguistics},
Year = {2020},
Location = {Seattle},
}

### Contributions

Thanks to [@MisbahKhan789](https://github.com/MisbahKhan789) for adding this dataset.