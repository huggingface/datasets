---
annotations_creators:
- machine-generated
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
- sequence-modeling
task_ids:
- dialogue-modeling
paperswithcode_id: craigslistbargains
---

# Dataset Card Creation Guide

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

- **Homepage:** [Decoupling Strategy and Generation in Negotiation Dialogues](https://worksheets.codalab.org/worksheets/0x453913e76b65495d8b9730d41c7e0a0c/)
- **Repository:** [Github: Stanford NLP Cocoa](https://github.com/stanfordnlp/cocoa/tree/master)
- **Paper:** [Decoupling Strategy and Generation in Negotiation Dialogues](https://arxiv.org/abs/1808.09637)
- **Leaderboard:** []()
- **Point of Contact:** [He He](hehe@cs.nyu.edu)

### Dataset Summary

We study negotiation dialogues where two agents, a buyer and a seller, negotiate over the price of an time for sale. We collected a dataset of more than 6K negotiation dialogues over multiple categories of products scraped from Craigslist. Our goal is to develop an agent that negotiates with humans through such conversations. The challenge is to handle both the negotiation strategy and the rich language for bargaining. To this end, we develop a modular framework which separates strategy learning from language generation. Specifically, we learn strategies in a coarse dialogue act space and instantiate that into utterances conditioned on dialogue history. 

### Supported Tasks and Leaderboards



### Languages

This dataset is English

## Dataset Structure

### Data Instances

```
{
  'agent_info': {
    'Bottomline': 
      [
        'None', 
        'None'
      ],
    'Role': 
      [
        'buyer', 
        'seller'
      ],
    'Target': 
      [
        7.0, 
        10.0
      ]
  },
  'agent_turn': 
    [
      0, 
      1, 
      ...
    ],
  'dialogue_acts': {
    'intent': 
      [
        'init-price',
        'unknown',
        ...
      ],
    'price': 
      [
        5.0, 
        -1.0, 
        ...
        ]
    },
  'items': {
    'Category': 
      [
        'phone', 
        'phone'
      ],
    'Description': 
      [
        'Charge two devices simultaneously on the go..., 
        ...
      ],
    'Images': 
      [
        'phone/6149527852_0.jpg', 
        'phone/6149527852_0.jpg'
      ],
    'Price': 
      [
        10.0, 
        10.0
      ],
    'Title': 
      [
        'Verizon Car Charger with Dual Output Micro USB and ...', 
        ...
      ]
    },
  'utterance': 
    [
      'Hi, not sure if the charger would work for my car...'
      'It will work...',
      ...
    ]
}

```

### Data Fields


- `agent_info`: Information about each of the agents taking part in the dialogue
  - `Bottomline`: TBD
  - `Role`: Whether the agent is buyer or seller
  - `Target`: Target price that the buyer/seller wants to hit in the negotiation
- `agent_turn`: Agent taking the current turn in the dialogue (`int` index corresponding to `Role` above)
- `dialogue_acts`: Rules-based information about the strategy of each agent for each turn
  - `intent`: The intent of the agent at the particular turn (offer, accept, etc.)
  - `price`: The current item price associated with the intent and turn in the bargaining process. Default value for missing: (`-1`)
- `items`: Information about the item the agents are bargaining for. **Note that there is an elembet for each of the fields below for each agent**
  - `Category`: Category of the item
  - `Description`: Description(s) of the item
  - `Images`: (comma delimited) strings of image names of the item
  - `Price`: Price(s) of the item. Default value for missing: (`-1`)
  - `Title`: Title(s) of the item
- `utterance`: Utterance for each turn in the dialogue, corresponding to the agent in `agent_turns`. The utterance may be an empty string (`''`) for some turns if multiple dialogue acts take place after an utterance (e.g. there are often multiple dialogue acts associated with the closing of the bargaining process after all utterances have completed to describe the conclusion of the bargaining).

### Data Splits

This dataset contains three splits, `train`, `validation` and `test`. Note that `test` is not provided with `dialogue_acts` information as described above. To ensure schema consistency across dataset splits, the `dialogue_acts` field in the `test` split is populated with the default values: `{"price": -1.0, "intent": ""}`

The counts of examples in each split are as follows:

|                            | Train  | Valid | Test |
| Input Examples             | 5247   | 597   | 838  |
| Average Dialogue Length    | 9.14   | 9.17  | 9.24 |

Note that 

## Dataset Creation

From the [source paper](https://arxiv.org/pdf/1808.09637.pdf) for this dataset: 

> To generate the negotiation scenarios, we
> scraped postings on sfbay.craigslist.org
> from the 6 most popular categories (housing, furniture, cars, bikes, phones, and electronics). Each
> posting produces three scenarios with the buyer’s
> target prices at 0.5x, 0.7x and 0.9x of the listing
> price. Statistics of the scenarios are shown in Table 2.
> We collected 6682 human-human dialogues on
> AMT using the interface shown in Appendix A
> Figure 2. The dataset statistics in Table 3 show
> that CRAIGSLISTBARGAIN has longer dialogues
> and more diverse utterances compared to prior
> datasets. Furthermore, workers were encouraged
> to embellish the item and negotiate side offers
> such as free delivery or pick-up. This highly relatable scenario leads to richer dialogues such as
> the one shown in Table 1. We also observed various persuasion techniques listed in Table 4 such as
> embellishment,

### Curation Rationale

See **Dataset Creation**

### Source Data

See **Dataset Creation**

#### Initial Data Collection and Normalization

See **Dataset Creation**

#### Who are the source language producers?

See **Dataset Creation**

### Annotations

If the dataset contains annotations which are not part of the initial data collection, describe them in the following paragraphs.

#### Annotation process

Annotations for the `dialogue_acts` in `train` and `test` were generated via a rules-based system which can be found in [this script](https://github.com/stanfordnlp/cocoa/blob/master/craigslistbargain/parse_dialogue.py)

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

He He and Derek Chen and Anusha Balakrishnan and Percy Liang
Computer Science Department, Stanford University
`{hehe,derekchen14,anusha,pliang}@cs.stanford.edu`

The work through which this data was produced was supported by
DARPA Communicating with Computers (CwC)
program under ARO prime contract no. W911NF15-1-0462

### Licensing Information

[More Information Needed]

### Citation Information

```
@misc{he2018decoupling,
    title={Decoupling Strategy and Generation in Negotiation Dialogues},
    author={He He and Derek Chen and Anusha Balakrishnan and Percy Liang},
    year={2018},
    eprint={1808.09637},
    archivePrefix={arXiv},
    primaryClass={cs.CL}
}
```


### Contributions

Thanks to [@ZacharySBrown](https://github.com/ZacharySBrown) for adding this dataset.