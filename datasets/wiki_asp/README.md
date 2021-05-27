---
annotations_creators:
- crowdsourced
language_creators:
- crowdsourced
languages:
- en
licenses:
- cc-by-sa-4.0
multilinguality:
- monolingual
size_categories:
- 10K<n<100K
source_datasets:
- original
task_categories:
- conditional-text-generation
task_ids:
- summarization
paperswithcode_id: wikiasp
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

- **Homepage:** [Wiki Asp](https://github.com/neulab/wikiasp)
- **Repository:** [GitHub](https://github.com/neulab/wikiasp)
- **Paper:** [WikiAsp: A Dataset for Multi-domain Aspect-based Summarization](https://arxiv.org/abs/2011.07832)

### Dataset Summary

[More Information Needed]

### Supported Tasks and Leaderboards

[More Information Needed]

### Languages

[More Information Needed]

## Dataset Structure

### Data Instances

An example from the "plant" configuration:
```
{
    'exid': 'train-78-8',
    'inputs': ['< EOT > calcareous rocks and barrens , wooded cliff edges .',
        'plant an erect short - lived perennial ( or biennial ) herb whose slender leafy stems radiate from the base , and are 3 - 5 dm tall , giving it a bushy appearance .',
        'leaves densely hairy , grayish - green , simple and alternate on the stem .',
        'flowers are bright yellow to yellow - orange , cross - shaped , each having 4 spatula - shaped petals about 5 mm long .',
        'fruit is a nearly globe - shaped capsule , about 3 mm in diameter , with 1 or 2 seeds in each cell .',
        'flowering period : early april to late may .',
        'even though there are many members of the mustard family in the range of this species , no other plant shares this combination of characters : bright yellow flowers , grayish - green stems and foliage , globe - shaped fruits with a long style , perennial habit , and the habitat of limestone rocky cliffs .',
        'timber removal may be beneficial and even needed to maintain the open character of the habitat for this species .',
        'hand removal of trees in the vicinity of the population is necessary to avoid impacts from timber operations .',
        'southwest indiana , north central kentucky , and north central tennessee .',
        'email : naturepreserves @ ky . gov feedback naturepreserves @ ky . gov | about the agency | about this site copyright © 2003 - 2013 commonwealth of kentucky .',
        'all rights reserved .',
        '<EOS>'
    ],
    'targets': [
        ['description',
            'physaria globosa is a small plant covered with dense hairs giving it a grayish appearance . it produces yellow flowers in the spring , and its fruit is globe - shaped . its preferred habitat is dry limestone cliffs , barrens , cedar glades , steep wooded slopes , and talus areas . some have also been found in areas of deeper soil and roadsides .'
        ],
        ['conservation',
            'the population fluctuates year to year , but on average there are about 2000 living plants at any one time , divided among 33 known locations . threats include forms of habitat degradation and destruction , including road construction and grading , mowing , dumping , herbicides , alteration of waterways , livestock damage , and invasive species of plants such as japanese honeysuckle , garlic mustard , alsike clover , sweet clover , meadow fescue , and multiflora rose . all populations are considered vulnerable to extirpation .'
        ]
    ]
}
```

### Data Fields

- `exid`: a unique identifier
- `input`: the cited references and consists of tokenized sentences (with NLTK) 
- `targets`: a list of aspect-based summaries, where each element is a pair of a) the target aspect and b) the aspect-based summary

### Data Splits

[More Information Needed]
## Dataset Creation

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

[More Information Needed]

### Contributions

Thanks to [@katnoria](https://github.com/katnoria) for adding this dataset.