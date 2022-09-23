---
task_categories:
- text-generation
- fill-mask
multilinguality:
- translation
task_ids:
- language-modeling
- masked-language-modeling
language:
- bn
- en
- gu
- hi
- ml
- mr
- or
- pa
- ta
- te
- ur
annotations_creators:
- no-annotation
source_datasets:
- original
size_categories:
- 1K<n<10K
- n<1K
license:
- cc-by-4.0
paperswithcode_id: null
pretty_name: CVIT MKB
configs:
- bn-en
- bn-gu
- bn-hi
- bn-ml
- bn-mr
- bn-or
- bn-ta
- bn-te
- bn-ur
- en-gu
- en-hi
- en-ml
- en-mr
- en-or
- en-ta
- en-te
- en-ur
- gu-hi
- gu-ml
- gu-mr
- gu-or
- gu-ta
- gu-te
- gu-ur
- hi-ml
- hi-mr
- hi-or
- hi-ta
- hi-te
- hi-ur
- ml-mr
- ml-or
- ml-ta
- ml-te
- ml-ur
- mr-or
- mr-ta
- mr-te
- mr-ur
- or-ta
- or-te
- or-ur
- ta-te
- ta-ur
- te-ur
dataset_info:
- config_name: or-ur
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - or
        - ur
  splits:
  - name: train
    num_bytes: 39336
    num_examples: 98
  download_size: 52428800
  dataset_size: 39336
- config_name: ml-or
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - ml
        - or
  splits:
  - name: train
    num_bytes: 224084
    num_examples: 427
  download_size: 52428800
  dataset_size: 224084
- config_name: bn-ta
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - bn
        - ta
  splits:
  - name: train
    num_bytes: 2020506
    num_examples: 3460
  download_size: 52428800
  dataset_size: 2020506
- config_name: gu-mr
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - gu
        - mr
  splits:
  - name: train
    num_bytes: 1818018
    num_examples: 3658
  download_size: 52428800
  dataset_size: 1818018
- config_name: hi-or
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - hi
        - or
  splits:
  - name: train
    num_bytes: 188779
    num_examples: 389
  download_size: 52428800
  dataset_size: 188779
- config_name: en-or
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - en
        - or
  splits:
  - name: train
    num_bytes: 276520
    num_examples: 768
  download_size: 52428800
  dataset_size: 276520
- config_name: mr-ur
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - mr
        - ur
  splits:
  - name: train
    num_bytes: 225305
    num_examples: 490
  download_size: 52428800
  dataset_size: 225305
- config_name: en-ta
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - en
        - ta
  splits:
  - name: train
    num_bytes: 2578828
    num_examples: 5744
  download_size: 52428800
  dataset_size: 2578828
- config_name: hi-ta
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - hi
        - ta
  splits:
  - name: train
    num_bytes: 1583237
    num_examples: 2761
  download_size: 52428800
  dataset_size: 1583237
- config_name: bn-en
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - bn
        - en
  splits:
  - name: train
    num_bytes: 2001834
    num_examples: 5634
  download_size: 52428800
  dataset_size: 2001834
- config_name: bn-or
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - bn
        - or
  splits:
  - name: train
    num_bytes: 220893
    num_examples: 447
  download_size: 52428800
  dataset_size: 220893
- config_name: ml-ta
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - ml
        - ta
  splits:
  - name: train
    num_bytes: 1958818
    num_examples: 3124
  download_size: 52428800
  dataset_size: 1958818
- config_name: gu-ur
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - gu
        - ur
  splits:
  - name: train
    num_bytes: 311082
    num_examples: 749
  download_size: 52428800
  dataset_size: 311082
- config_name: bn-ml
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - bn
        - ml
  splits:
  - name: train
    num_bytes: 1587528
    num_examples: 2938
  download_size: 52428800
  dataset_size: 1587528
- config_name: bn-hi
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - bn
        - hi
  splits:
  - name: train
    num_bytes: 1298611
    num_examples: 2706
  download_size: 52428800
  dataset_size: 1298611
- config_name: gu-te
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - gu
        - te
  splits:
  - name: train
    num_bytes: 1669386
    num_examples: 3528
  download_size: 52428800
  dataset_size: 1669386
- config_name: hi-ml
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - hi
        - ml
  splits:
  - name: train
    num_bytes: 1208956
    num_examples: 2305
  download_size: 52428800
  dataset_size: 1208956
- config_name: or-te
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - or
        - te
  splits:
  - name: train
    num_bytes: 209457
    num_examples: 440
  download_size: 52428800
  dataset_size: 209457
- config_name: en-ml
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - en
        - ml
  splits:
  - name: train
    num_bytes: 2007061
    num_examples: 5017
  download_size: 52428800
  dataset_size: 2007061
- config_name: en-hi
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - en
        - hi
  splits:
  - name: train
    num_bytes: 1865430
    num_examples: 5272
  download_size: 52428800
  dataset_size: 1865430
- config_name: mr-te
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - mr
        - te
  splits:
  - name: train
    num_bytes: 1434444
    num_examples: 2839
  download_size: 52428800
  dataset_size: 1434444
- config_name: bn-te
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - bn
        - te
  splits:
  - name: train
    num_bytes: 1431096
    num_examples: 2939
  download_size: 52428800
  dataset_size: 1431096
- config_name: gu-hi
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - gu
        - hi
  splits:
  - name: train
    num_bytes: 1521174
    num_examples: 3213
  download_size: 52428800
  dataset_size: 1521174
- config_name: ta-ur
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - ta
        - ur
  splits:
  - name: train
    num_bytes: 329809
    num_examples: 637
  download_size: 52428800
  dataset_size: 329809
- config_name: te-ur
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - te
        - ur
  splits:
  - name: train
    num_bytes: 254581
    num_examples: 599
  download_size: 52428800
  dataset_size: 254581
- config_name: gu-ml
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - gu
        - ml
  splits:
  - name: train
    num_bytes: 1822865
    num_examples: 3469
  download_size: 52428800
  dataset_size: 1822865
- config_name: hi-te
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - hi
        - te
  splits:
  - name: train
    num_bytes: 1078371
    num_examples: 2289
  download_size: 52428800
  dataset_size: 1078371
- config_name: en-te
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - en
        - te
  splits:
  - name: train
    num_bytes: 1784517
    num_examples: 5177
  download_size: 52428800
  dataset_size: 1784517
- config_name: ml-te
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - ml
        - te
  splits:
  - name: train
    num_bytes: 1556164
    num_examples: 2898
  download_size: 52428800
  dataset_size: 1556164
- config_name: hi-ur
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - hi
        - ur
  splits:
  - name: train
    num_bytes: 313360
    num_examples: 742
  download_size: 52428800
  dataset_size: 313360
- config_name: mr-or
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - mr
        - or
  splits:
  - name: train
    num_bytes: 219193
    num_examples: 432
  download_size: 52428800
  dataset_size: 219193
- config_name: en-ur
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - en
        - ur
  splits:
  - name: train
    num_bytes: 289419
    num_examples: 1019
  download_size: 52428800
  dataset_size: 289419
- config_name: ml-ur
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - ml
        - ur
  splits:
  - name: train
    num_bytes: 295806
    num_examples: 624
  download_size: 52428800
  dataset_size: 295806
- config_name: bn-mr
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - bn
        - mr
  splits:
  - name: train
    num_bytes: 1554154
    num_examples: 3054
  download_size: 52428800
  dataset_size: 1554154
- config_name: gu-ta
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - gu
        - ta
  splits:
  - name: train
    num_bytes: 2284643
    num_examples: 3998
  download_size: 52428800
  dataset_size: 2284643
- config_name: bn-gu
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - bn
        - gu
  splits:
  - name: train
    num_bytes: 1840059
    num_examples: 3810
  download_size: 52428800
  dataset_size: 1840059
- config_name: bn-ur
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - bn
        - ur
  splits:
  - name: train
    num_bytes: 234561
    num_examples: 559
  download_size: 52428800
  dataset_size: 234561
- config_name: ml-mr
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - ml
        - mr
  splits:
  - name: train
    num_bytes: 1568672
    num_examples: 2803
  download_size: 52428800
  dataset_size: 1568672
- config_name: or-ta
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - or
        - ta
  splits:
  - name: train
    num_bytes: 267193
    num_examples: 470
  download_size: 52428800
  dataset_size: 267193
- config_name: ta-te
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - ta
        - te
  splits:
  - name: train
    num_bytes: 1773728
    num_examples: 3100
  download_size: 52428800
  dataset_size: 1773728
- config_name: gu-or
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - gu
        - or
  splits:
  - name: train
    num_bytes: 256362
    num_examples: 541
  download_size: 52428800
  dataset_size: 256362
- config_name: en-gu
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - en
        - gu
  splits:
  - name: train
    num_bytes: 2318080
    num_examples: 6615
  download_size: 52428800
  dataset_size: 2318080
- config_name: hi-mr
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - hi
        - mr
  splits:
  - name: train
    num_bytes: 1243583
    num_examples: 2491
  download_size: 52428800
  dataset_size: 1243583
- config_name: mr-ta
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - mr
        - ta
  splits:
  - name: train
    num_bytes: 1906073
    num_examples: 3175
  download_size: 52428800
  dataset_size: 1906073
- config_name: en-mr
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - en
        - mr
  splits:
  - name: train
    num_bytes: 2140298
    num_examples: 5867
  download_size: 52428800
  dataset_size: 2140298
---

# Dataset Card for CVIT MKB

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

- **Homepage:** [Link](http://preon.iiit.ac.in/~jerin/bhasha/) 
- **Repository:**
- **Paper:** [ARXIV](https://arxiv.org/abs/2007.07691)
- **Leaderboard:** 
- **Point of Contact:** [email](cvit-bhasha@googlegroups.com)

### Dataset Summary

Indian Prime Minister's speeches - Mann Ki Baat, on All India Radio, translated into many languages.

### Supported Tasks and Leaderboards

[MORE INFORMATION NEEDED]

### Languages

Hindi, Telugu, Tamil, Malayalam, Gujarati, Urdu, Bengali, Oriya, Marathi, Punjabi, and English

## Dataset Structure

### Data Instances

[MORE INFORMATION NEEDED]

### Data Fields

- `src_tag`: `string` text in source language
- `tgt_tag`: `string` translation of source language in target language

### Data Splits

[MORE INFORMATION NEEDED]

## Dataset Creation

### Curation Rationale

[MORE INFORMATION NEEDED]

### Source Data

[MORE INFORMATION NEEDED]

#### Initial Data Collection and Normalization

[MORE INFORMATION NEEDED]

#### Who are the source language producers?

[MORE INFORMATION NEEDED]

### Annotations

#### Annotation process

[MORE INFORMATION NEEDED]

#### Who are the annotators?

[MORE INFORMATION NEEDED]

### Personal and Sensitive Information

[MORE INFORMATION NEEDED]

## Considerations for Using the Data

### Social Impact of Dataset

[MORE INFORMATION NEEDED]

### Discussion of Biases

[MORE INFORMATION NEEDED]

### Other Known Limitations

[MORE INFORMATION NEEDED]

## Additional Information

### Dataset Curators

[MORE INFORMATION NEEDED]

### Licensing Information

The datasets and pretrained models provided here are licensed under Creative Commons Attribution-ShareAlike 4.0 International License.

### Citation Information

```
@misc{siripragada2020multilingual,
      title={A Multilingual Parallel Corpora Collection Effort for Indian Languages},
      author={Shashank Siripragada and Jerin Philip and Vinay P. Namboodiri and C V Jawahar},
      year={2020},
      eprint={2007.07691},
      archivePrefix={arXiv},
      primaryClass={cs.CL}
}
```

### Contributions

Thanks to [@vasudevgupta7](https://github.com/vasudevgupta7) for adding this dataset.