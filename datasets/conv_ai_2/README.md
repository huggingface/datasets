---
annotations_creators:
- crowdsourced
language_creators:
- crowdsourced
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
- text-scoring
task_ids:
- text-scoring-other-evaluating-dialogue-systems
paperswithcode_id: convai2
---

# Dataset Card for conv_ai_2

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

- **Homepage:** https://github.com/DeepPavlov/convai/tree/master/2018
- **Repository:** https://github.com/DeepPavlov/convai/tree/master/2018
- **Paper:** https://arxiv.org/abs/1902.00098
- **Leaderboard:** [More Information Needed]
- **Point of Contact:** [More Information Needed]

### Dataset Summary

ConvAI is a dataset of human-to-bot conversations labeled for quality. This data can be used to train a metric for evaluating dialogue systems. Moreover, it can be used in the development of chatbots themselves: it contains information on the quality of utterances and entire dialogues, that can guide a dialogue system in search of better answers.

### Supported Tasks and Leaderboards

[More Information Needed]

### Languages

[More Information Needed]

## Dataset Structure

### Data Instances

```
{
        "dialog_id": "0x648cc5b7",
        "dialog": [
            {
                "id": 0,
                "sender": "participant2",
                "text": "Hi! How is your day? \ud83d\ude09",
                "sender_class": "Bot"
            },
            {
                "id": 1,
                "sender": "participant1",
                "text": "Hi! Great!",
                "sender_class": "Human"
            },
            {
                "id": 2,
                "sender": "participant2",
                "text": "I am good thanks for asking are you currently in high school?",
                "sender_class": "Bot"
            }
        ],
        "bot_profile": [
            "my current goal is to run a k.",
            "when i grow up i want to be a physical therapist.",
            "i'm currently in high school.",
            "i make straight as in school.",
            "i won homecoming queen this year."
        ],
        "user_profile": [
            "my favorite color is red.",
            "i enjoy listening to classical music.",
            "i'm a christian.",
            "i can drive a tractor."
        ],
        "eval_score": 4,
        "profile_match": 1
    }
```

### Data Fields

- dialog_id : specifies the unique ID for the dialogs.
- dialog : Array of dialogs.
- bot_profile : Bot annotated response that will be used for evaluation.
- user_profile : user annoted response that will be used for evaluation.
- eval_score : (`1`,` 2`,` 3`,` 4`,` 5`) how does an user like a conversation. The missing values are replaced with` -1`
- profile_match : (`0`,` 1`) an user is given by two profile descriptions (4 sentences each), one of them is the one given to the bot it had been talking to, the other one is random; the user needs to choose one of them.The missing values are replaced with` -1`

### Data Splits

[More Information Needed]

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

[More Information Needed]

### Citation Information

@article{DBLP:journals/corr/abs-1902-00098,
  author    = {Emily Dinan and
               Varvara Logacheva and
               Valentin Malykh and
               Alexander H. Miller and
               Kurt Shuster and
               Jack Urbanek and
               Douwe Kiela and
               Arthur Szlam and
               Iulian Serban and
               Ryan Lowe and
               Shrimai Prabhumoye and
               Alan W. Black and
               Alexander I. Rudnicky and
               Jason Williams and
               Joelle Pineau and
               Mikhail S. Burtsev and
               Jason Weston},
  title     = {The Second Conversational Intelligence Challenge (ConvAI2)},
  journal   = {CoRR},
  volume    = {abs/1902.00098},
  year      = {2019},
  url       = {http://arxiv.org/abs/1902.00098},
  archivePrefix = {arXiv},
  eprint    = {1902.00098},
  timestamp = {Wed, 07 Oct 2020 11:09:41 +0200},
  biburl    = {https://dblp.org/rec/journals/corr/abs-1902-00098.bib},
  bibsource = {dblp computer science bibliography, https://dblp.org}
}
### Contributions

Thanks to [@rkc007](https://github.com/rkc007) for adding this dataset.