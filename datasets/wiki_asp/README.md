---
annotations_creators:
- crowdsourced
language_creators:
- crowdsourced
language:
- en
license:
- cc-by-sa-4.0
multilinguality:
- monolingual
size_categories:
- 10K<n<100K
source_datasets:
- original
task_categories:
- summarization
task_ids:
- summarization-other-aspect-based-summarization
paperswithcode_id: wikiasp
pretty_name: WikiAsp
dataset_info:
- config_name: album
  features:
  - name: exid
    dtype: string
  - name: inputs
    sequence: string
  - name: targets
    sequence:
      sequence: string
  splits:
  - name: test
    num_bytes: 232999001
    num_examples: 3038
  - name: train
    num_bytes: 1907323642
    num_examples: 24434
  - name: validation
    num_bytes: 234990092
    num_examples: 3104
  download_size: 644173065
  dataset_size: 2375312735
- config_name: animal
  features:
  - name: exid
    dtype: string
  - name: inputs
    sequence: string
  - name: targets
    sequence:
      sequence: string
  splits:
  - name: test
    num_bytes: 61315970
    num_examples: 2007
  - name: train
    num_bytes: 497474133
    num_examples: 16540
  - name: validation
    num_bytes: 57943532
    num_examples: 2005
  download_size: 150974930
  dataset_size: 616733635
- config_name: artist
  features:
  - name: exid
    dtype: string
  - name: inputs
    sequence: string
  - name: targets
    sequence:
      sequence: string
  splits:
  - name: test
    num_bytes: 237751553
    num_examples: 3329
  - name: train
    num_bytes: 1876134255
    num_examples: 26754
  - name: validation
    num_bytes: 223240910
    num_examples: 3194
  download_size: 626686303
  dataset_size: 2337126718
- config_name: building
  features:
  - name: exid
    dtype: string
  - name: inputs
    sequence: string
  - name: targets
    sequence:
      sequence: string
  splits:
  - name: test
    num_bytes: 134357678
    num_examples: 2482
  - name: train
    num_bytes: 1100057273
    num_examples: 20449
  - name: validation
    num_bytes: 139387376
    num_examples: 2607
  download_size: 346224042
  dataset_size: 1373802327
- config_name: company
  features:
  - name: exid
    dtype: string
  - name: inputs
    sequence: string
  - name: targets
    sequence:
      sequence: string
  splits:
  - name: test
    num_bytes: 199282041
    num_examples: 3029
  - name: train
    num_bytes: 1606057076
    num_examples: 24353
  - name: validation
    num_bytes: 200498778
    num_examples: 2946
  download_size: 504194353
  dataset_size: 2005837895
- config_name: educational_institution
  features:
  - name: exid
    dtype: string
  - name: inputs
    sequence: string
  - name: targets
    sequence:
      sequence: string
  splits:
  - name: test
    num_bytes: 200476681
    num_examples: 2267
  - name: train
    num_bytes: 1623000534
    num_examples: 17634
  - name: validation
    num_bytes: 203262430
    num_examples: 2141
  download_size: 471033992
  dataset_size: 2026739645
- config_name: event
  features:
  - name: exid
    dtype: string
  - name: inputs
    sequence: string
  - name: targets
    sequence:
      sequence: string
  splits:
  - name: test
    num_bytes: 96212295
    num_examples: 828
  - name: train
    num_bytes: 748201660
    num_examples: 6475
  - name: validation
    num_bytes: 97431395
    num_examples: 807
  download_size: 240072903
  dataset_size: 941845350
- config_name: film
  features:
  - name: exid
    dtype: string
  - name: inputs
    sequence: string
  - name: targets
    sequence:
      sequence: string
  splits:
  - name: test
    num_bytes: 294918370
    num_examples: 3981
  - name: train
    num_bytes: 2370068027
    num_examples: 32129
  - name: validation
    num_bytes: 290240851
    num_examples: 4014
  download_size: 808231638
  dataset_size: 2955227248
- config_name: group
  features:
  - name: exid
    dtype: string
  - name: inputs
    sequence: string
  - name: targets
    sequence:
      sequence: string
  splits:
  - name: test
    num_bytes: 114239405
    num_examples: 1444
  - name: train
    num_bytes: 1025166800
    num_examples: 11966
  - name: validation
    num_bytes: 120863870
    num_examples: 1462
  download_size: 344498865
  dataset_size: 1260270075
- config_name: historic_place
  features:
  - name: exid
    dtype: string
  - name: inputs
    sequence: string
  - name: targets
    sequence:
      sequence: string
  splits:
  - name: test
    num_bytes: 31201154
    num_examples: 600
  - name: train
    num_bytes: 256158020
    num_examples: 4919
  - name: validation
    num_bytes: 29058067
    num_examples: 601
  download_size: 77289509
  dataset_size: 316417241
- config_name: infrastructure
  features:
  - name: exid
    dtype: string
  - name: inputs
    sequence: string
  - name: targets
    sequence:
      sequence: string
  splits:
  - name: test
    num_bytes: 134820330
    num_examples: 2091
  - name: train
    num_bytes: 1124486451
    num_examples: 17226
  - name: validation
    num_bytes: 125193140
    num_examples: 1984
  download_size: 328804337
  dataset_size: 1384499921
- config_name: mean_of_transportation
  features:
  - name: exid
    dtype: string
  - name: inputs
    sequence: string
  - name: targets
    sequence:
      sequence: string
  splits:
  - name: test
    num_bytes: 89759392
    num_examples: 1170
  - name: train
    num_bytes: 650424738
    num_examples: 9277
  - name: validation
    num_bytes: 88440901
    num_examples: 1215
  download_size: 210234418
  dataset_size: 828625031
- config_name: office_holder
  features:
  - name: exid
    dtype: string
  - name: inputs
    sequence: string
  - name: targets
    sequence:
      sequence: string
  splits:
  - name: test
    num_bytes: 207433317
    num_examples: 2333
  - name: train
    num_bytes: 1643899203
    num_examples: 18177
  - name: validation
    num_bytes: 202624275
    num_examples: 2218
  download_size: 524721727
  dataset_size: 2053956795
- config_name: plant
  features:
  - name: exid
    dtype: string
  - name: inputs
    sequence: string
  - name: targets
    sequence:
      sequence: string
  splits:
  - name: test
    num_bytes: 31340125
    num_examples: 774
  - name: train
    num_bytes: 239150885
    num_examples: 6107
  - name: validation
    num_bytes: 28752150
    num_examples: 786
  download_size: 77890632
  dataset_size: 299243160
- config_name: single
  features:
  - name: exid
    dtype: string
  - name: inputs
    sequence: string
  - name: targets
    sequence:
      sequence: string
  splits:
  - name: test
    num_bytes: 152328537
    num_examples: 1712
  - name: train
    num_bytes: 1277277277
    num_examples: 14217
  - name: validation
    num_bytes: 160312594
    num_examples: 1734
  download_size: 429214401
  dataset_size: 1589918408
- config_name: soccer_player
  features:
  - name: exid
    dtype: string
  - name: inputs
    sequence: string
  - name: targets
    sequence:
      sequence: string
  splits:
  - name: test
    num_bytes: 72820378
    num_examples: 2280
  - name: train
    num_bytes: 604502541
    num_examples: 17599
  - name: validation
    num_bytes: 76705685
    num_examples: 2150
  download_size: 193347234
  dataset_size: 754028604
- config_name: software
  features:
  - name: exid
    dtype: string
  - name: inputs
    sequence: string
  - name: targets
    sequence:
      sequence: string
  splits:
  - name: test
    num_bytes: 133717992
    num_examples: 1638
  - name: train
    num_bytes: 1122906186
    num_examples: 13516
  - name: validation
    num_bytes: 134578157
    num_examples: 1637
  download_size: 356764908
  dataset_size: 1391202335
- config_name: television_show
  features:
  - name: exid
    dtype: string
  - name: inputs
    sequence: string
  - name: targets
    sequence:
      sequence: string
  splits:
  - name: test
    num_bytes: 115155155
    num_examples: 1072
  - name: train
    num_bytes: 893325347
    num_examples: 8717
  - name: validation
    num_bytes: 119461892
    num_examples: 1128
  download_size: 302093407
  dataset_size: 1127942394
- config_name: town
  features:
  - name: exid
    dtype: string
  - name: inputs
    sequence: string
  - name: targets
    sequence:
      sequence: string
  splits:
  - name: test
    num_bytes: 100975827
    num_examples: 1831
  - name: train
    num_bytes: 772504751
    num_examples: 14818
  - name: validation
    num_bytes: 101522638
    num_examples: 1911
  download_size: 243261734
  dataset_size: 975003216
- config_name: written_work
  features:
  - name: exid
    dtype: string
  - name: inputs
    sequence: string
  - name: targets
    sequence:
      sequence: string
  splits:
  - name: test
    num_bytes: 189537205
    num_examples: 1931
  - name: train
    num_bytes: 1491395960
    num_examples: 15065
  - name: validation
    num_bytes: 185707567
    num_examples: 1843
  download_size: 498307235
  dataset_size: 1866640732
---

# Dataset Card for WikiAsp

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