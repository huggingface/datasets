---
annotations_creators:
- expert-generated
language_creators:
- crowdsourced
language:
- en
license:
- cc-by-4.0
multilinguality:
- monolingual
size_categories:
- 1K<n<10K
source_datasets:
- original
task_categories:
- conversational
- text-generation
- fill-mask
task_ids:
- dialogue-modeling
pretty_name: Campsite Negotiation Dialogues
paperswithcode_id: casino

---


# Dataset Card for Casino

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

- **Repository:** [Github: Kushal Chawla CaSiNo](https://github.com/kushalchawla/CaSiNo)
- **Paper:** [CaSiNo: A Corpus of Campsite Negotiation Dialogues for Automatic Negotiation Systems](https://aclanthology.org/2021.naacl-main.254.pdf)
- **Point of Contact:** [Kushal Chawla](kchawla@usc.edu)

### Dataset Summary

We provide a novel dataset (referred to as CaSiNo) of 1030 negotiation dialogues. Two participants take the role of campsite neighbors and negotiate for Food, Water, and Firewood packages, based on their individual preferences and requirements. This design keeps the task tractable, while still facilitating linguistically rich and personal conversations. This helps to overcome the limitations of prior negotiation datasets such as Deal or No Deal and Craigslist Bargain. Each dialogue consists of rich meta-data including participant demographics, personality, and their subjective evaluation of the negotiation in terms of satisfaction and opponent likeness.

### Supported Tasks and Leaderboards

Train end-to-end models for negotiation

### Languages

English

## Dataset Structure

### Data Instances

```
{
    "chat_logs": [
        {
            "text": "Hello! \ud83d\ude42 Let's work together on a deal for these packages, shall we? What are you most interested in?",
            "task_data": {}, 
            "id": "mturk_agent_1"
        },
        ...
    ],
    "participant_info": {
        "mturk_agent_1":
            {
                "value2issue": ...
                "value2reason": ...
                "outcomes": ...
                "demographics": ...
                "personality": ...
            }, 
        "mturk_agent_2": ...
    },
    "annotations": [
        ["Hello! \ud83d\ude42 Let's work together on a deal for these packages, shall we? What are you most interested in?", "promote-coordination,elicit-pref"],
        ...
    ]
}
```

### Data Fields

- `chat_logs`: The negotiation dialogue between two participants
  - `text`: The dialogue utterance
  - `task_data`: Meta-data associated with the utterance such as the deal submitted by a participant
  - `id`: The ID of the participant who typed this utterance
- `participant_info`: Meta-data about the two participants in this conversation
  - `mturk_agent_1`: For the first participant (Note that 'first' is just for reference. There is no order between the participants and any participant can start the conversation)
      - `value2issue`: The priority order of this participant among Food, Water, Firewood
      - `value2reason`: The personal arguments given by the participants themselves, consistent with the above preference order. This preference order and these arguments were submitted before the negotiation began. 
      - `outcomes`: The negotiation outcomes for this participant including objective and subjective assessment.
      - `demographics`: Demographic attributes of the participant in terms of age, gender, ethnicity, and education.
      - `personality`: Personality attributes for this participant, in terms of Big-5 and Social Value Orientation
  - `mturk_agent_2`: For the second participant; follows the same structure as above
- `annotations`: Strategy annotations for each utterance in the dialogue, wherever available. The first element represents the utterance and the second represents a comma-separated list of all strategies present in that utterance.

### Data Splits

No default data split has been provided. Hence, all 1030 data points are under the 'train' split.

|                     | Train |
|       -----         | ----- |
| total dialogues     |  1030 |
| annotated dialogues |   396 |

## Dataset Creation

### Curation Rationale

The dataset was collected to address the limitations in prior negotiation datasets from the perspective of downstream applications in pedagogy and conversational AI. Please refer to the original paper published at NAACL 2021 for details about the rationale and data curation steps ([source paper](https://aclanthology.org/2021.naacl-main.254.pdf)).

### Source Data

#### Initial Data Collection and Normalization

The dialogues were crowdsourced on Amazon Mechanical Turk. The strategy annotations were performed by expert annotators (first three authors of the paper). Please refer to the original dataset paper published at NAACL 2021 for more details ([source paper](https://aclanthology.org/2021.naacl-main.254.pdf)).

#### Who are the source language producers?

The primary producers are Turkers on Amazon Mechanical Turk platform. Two turkers were randomly paired with each other to engage in a negotiation via a chat interface. Please refer to the original dataset paper published at NAACL 2021 for more details ([source paper](https://aclanthology.org/2021.naacl-main.254.pdf)).

### Annotations

#### Annotation process

From the [source paper](https://aclanthology.org/2021.naacl-main.254.pdf) for this dataset: 

>Three expert annotators independently annotated 396 dialogues containing 4615 utterances. The annotation guidelines were iterated over a subset of 5 dialogues, while the reliability scores were computed on a different subset of 10 dialogues. We use the nominal form of Krippendorff’s alpha (Krippendorff, 2018) to measure the inter-annotator agreement. We provide the annotation statistics in Table 2. Although we release all the annotations, we skip Coordination and Empathy for our analysis in this work, due to higher subjectivity resulting in relatively lower reliability scores.

#### Who are the annotators?

Three expert annotators (first three authors of the paper).

### Personal and Sensitive Information

All personally identifiable information about the participants such as MTurk Ids or HIT Ids was removed before releasing the data.

## Considerations for Using the Data

### Social Impact of Dataset

Please refer to Section 8.2 in the [source paper](https://aclanthology.org/2021.naacl-main.254.pdf).

### Discussion of Biases

Please refer to Section 8.2 in the [source paper](https://aclanthology.org/2021.naacl-main.254.pdf).

### Other Known Limitations

Please refer to Section 7 in the [source paper](https://aclanthology.org/2021.naacl-main.254.pdf).

## Additional Information

### Dataset Curators

Corresponding Author: Kushal Chawla (`kchawla@usc.edu`)\
Affiliation: University of Southern California\
Please refer to the [source paper](https://aclanthology.org/2021.naacl-main.254.pdf) for the complete author list.

### Licensing Information

The project is licensed under CC-by-4.0

### Citation Information
```
@inproceedings{chawla2021casino,
  title={CaSiNo: A Corpus of Campsite Negotiation Dialogues for Automatic Negotiation Systems},
  author={Chawla, Kushal and Ramirez, Jaysa and Clever, Rene and Lucas, Gale and May, Jonathan and Gratch, Jonathan},
  booktitle={Proceedings of the 2021 Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies},
  pages={3167--3185},
  year={2021}
}
```

### Contributions

Thanks to [Kushal Chawla](https://kushalchawla.github.io/) for adding this dataset.