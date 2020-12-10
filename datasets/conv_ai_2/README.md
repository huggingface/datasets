[Needs More Information]

# Dataset Card for conv_ai_2

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

## Dataset Description

- **Homepage:** https://github.com/DeepPavlov/convai/tree/master/2018
- **Repository:** https://github.com/DeepPavlov/convai/tree/master/2018
- **Paper:** https://arxiv.org/abs/1902.00098
- **Leaderboard:** [Needs More Information]
- **Point of Contact:** [Needs More Information]

### Dataset Summary

ConvAI is a dataset of human-to-bot conversations labeled for quality. This data can be used to train a metric for evaluating dialogue systems. Moreover, it can be used in the development of chatbots themselves: it contains information on the quality of utterances and entire dialogues, that can guide a dialogue system in search of better answers.

### Supported Tasks and Leaderboards

[Needs More Information]

### Languages

[Needs More Information]

## Dataset Structure

### Data Instances

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

### Data Fields

[Needs More Information]

### Data Splits

[Needs More Information]

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

[Needs More Information]

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

[Needs More Information]

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