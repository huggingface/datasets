---
pretty_name: SETimes – A Parallel Corpus of English and South-East European Languages
annotations_creators:
- found
language_creators:
- found
language:
- bg
- bs
- el
- en
- hr
- mk
- ro
- sq
- sr
- tr
license:
- cc-by-sa-4.0
multilinguality:
- multilingual
size_categories:
- 100K<n<1M
source_datasets:
- original
task_categories:
- translation
task_ids: []
paperswithcode_id: null
dataset_info:
- config_name: bg-bs
  features:
  - name: id
    dtype: string
  - name: translation
    dtype:
      translation:
        languages:
        - bg
        - bs
  splits:
  - name: train
    num_bytes: 53816914
    num_examples: 136009
  download_size: 15406039
  dataset_size: 53816914
- config_name: bg-el
  features:
  - name: id
    dtype: string
  - name: translation
    dtype:
      translation:
        languages:
        - bg
        - el
  splits:
  - name: train
    num_bytes: 115127431
    num_examples: 212437
  download_size: 28338218
  dataset_size: 115127431
- config_name: bs-el
  features:
  - name: id
    dtype: string
  - name: translation
    dtype:
      translation:
        languages:
        - bs
        - el
  splits:
  - name: train
    num_bytes: 57102373
    num_examples: 137602
  download_size: 16418250
  dataset_size: 57102373
- config_name: bg-en
  features:
  - name: id
    dtype: string
  - name: translation
    dtype:
      translation:
        languages:
        - bg
        - en
  splits:
  - name: train
    num_bytes: 84421414
    num_examples: 213160
  download_size: 23509552
  dataset_size: 84421414
- config_name: bs-en
  features:
  - name: id
    dtype: string
  - name: translation
    dtype:
      translation:
        languages:
        - bs
        - en
  splits:
  - name: train
    num_bytes: 38167846
    num_examples: 138387
  download_size: 13477699
  dataset_size: 38167846
- config_name: el-en
  features:
  - name: id
    dtype: string
  - name: translation
    dtype:
      translation:
        languages:
        - el
        - en
  splits:
  - name: train
    num_bytes: 95011154
    num_examples: 227168
  download_size: 26637317
  dataset_size: 95011154
- config_name: bg-hr
  features:
  - name: id
    dtype: string
  - name: translation
    dtype:
      translation:
        languages:
        - bg
        - hr
  splits:
  - name: train
    num_bytes: 81774321
    num_examples: 203465
  download_size: 23165617
  dataset_size: 81774321
- config_name: bs-hr
  features:
  - name: id
    dtype: string
  - name: translation
    dtype:
      translation:
        languages:
        - bs
        - hr
  splits:
  - name: train
    num_bytes: 38742816
    num_examples: 138402
  download_size: 13887348
  dataset_size: 38742816
- config_name: el-hr
  features:
  - name: id
    dtype: string
  - name: translation
    dtype:
      translation:
        languages:
        - el
        - hr
  splits:
  - name: train
    num_bytes: 86642323
    num_examples: 205008
  download_size: 24662936
  dataset_size: 86642323
- config_name: en-hr
  features:
  - name: id
    dtype: string
  - name: translation
    dtype:
      translation:
        languages:
        - en
        - hr
  splits:
  - name: train
    num_bytes: 57995502
    num_examples: 205910
  download_size: 20238640
  dataset_size: 57995502
- config_name: bg-mk
  features:
  - name: id
    dtype: string
  - name: translation
    dtype:
      translation:
        languages:
        - bg
        - mk
  splits:
  - name: train
    num_bytes: 110119623
    num_examples: 207169
  download_size: 26507432
  dataset_size: 110119623
- config_name: bs-mk
  features:
  - name: id
    dtype: string
  - name: translation
    dtype:
      translation:
        languages:
        - bs
        - mk
  splits:
  - name: train
    num_bytes: 53972847
    num_examples: 132779
  download_size: 15267045
  dataset_size: 53972847
- config_name: el-mk
  features:
  - name: id
    dtype: string
  - name: translation
    dtype:
      translation:
        languages:
        - el
        - mk
  splits:
  - name: train
    num_bytes: 115285053
    num_examples: 207262
  download_size: 28103006
  dataset_size: 115285053
- config_name: en-mk
  features:
  - name: id
    dtype: string
  - name: translation
    dtype:
      translation:
        languages:
        - en
        - mk
  splits:
  - name: train
    num_bytes: 84735835
    num_examples: 207777
  download_size: 23316519
  dataset_size: 84735835
- config_name: hr-mk
  features:
  - name: id
    dtype: string
  - name: translation
    dtype:
      translation:
        languages:
        - hr
        - mk
  splits:
  - name: train
    num_bytes: 82230621
    num_examples: 198876
  download_size: 23008021
  dataset_size: 82230621
- config_name: bg-ro
  features:
  - name: id
    dtype: string
  - name: translation
    dtype:
      translation:
        languages:
        - bg
        - ro
  splits:
  - name: train
    num_bytes: 88058251
    num_examples: 210842
  download_size: 24592883
  dataset_size: 88058251
- config_name: bs-ro
  features:
  - name: id
    dtype: string
  - name: translation
    dtype:
      translation:
        languages:
        - bs
        - ro
  splits:
  - name: train
    num_bytes: 40894475
    num_examples: 137365
  download_size: 14272958
  dataset_size: 40894475
- config_name: el-ro
  features:
  - name: id
    dtype: string
  - name: translation
    dtype:
      translation:
        languages:
        - el
        - ro
  splits:
  - name: train
    num_bytes: 93167572
    num_examples: 212359
  download_size: 26164582
  dataset_size: 93167572
- config_name: en-ro
  features:
  - name: id
    dtype: string
  - name: translation
    dtype:
      translation:
        languages:
        - en
        - ro
  splits:
  - name: train
    num_bytes: 63354811
    num_examples: 213047
  download_size: 21549096
  dataset_size: 63354811
- config_name: hr-ro
  features:
  - name: id
    dtype: string
  - name: translation
    dtype:
      translation:
        languages:
        - hr
        - ro
  splits:
  - name: train
    num_bytes: 61696975
    num_examples: 203777
  download_size: 21276645
  dataset_size: 61696975
- config_name: mk-ro
  features:
  - name: id
    dtype: string
  - name: translation
    dtype:
      translation:
        languages:
        - mk
        - ro
  splits:
  - name: train
    num_bytes: 88449831
    num_examples: 206168
  download_size: 24409734
  dataset_size: 88449831
- config_name: bg-sq
  features:
  - name: id
    dtype: string
  - name: translation
    dtype:
      translation:
        languages:
        - bg
        - sq
  splits:
  - name: train
    num_bytes: 87552911
    num_examples: 211518
  download_size: 24385772
  dataset_size: 87552911
- config_name: bs-sq
  features:
  - name: id
    dtype: string
  - name: translation
    dtype:
      translation:
        languages:
        - bs
        - sq
  splits:
  - name: train
    num_bytes: 40407355
    num_examples: 137953
  download_size: 14097831
  dataset_size: 40407355
- config_name: el-sq
  features:
  - name: id
    dtype: string
  - name: translation
    dtype:
      translation:
        languages:
        - el
        - sq
  splits:
  - name: train
    num_bytes: 98779961
    num_examples: 226577
  download_size: 27676986
  dataset_size: 98779961
- config_name: en-sq
  features:
  - name: id
    dtype: string
  - name: translation
    dtype:
      translation:
        languages:
        - en
        - sq
  splits:
  - name: train
    num_bytes: 66898163
    num_examples: 227516
  download_size: 22718906
  dataset_size: 66898163
- config_name: hr-sq
  features:
  - name: id
    dtype: string
  - name: translation
    dtype:
      translation:
        languages:
        - hr
        - sq
  splits:
  - name: train
    num_bytes: 61296829
    num_examples: 205044
  download_size: 21160637
  dataset_size: 61296829
- config_name: mk-sq
  features:
  - name: id
    dtype: string
  - name: translation
    dtype:
      translation:
        languages:
        - mk
        - sq
  splits:
  - name: train
    num_bytes: 88053621
    num_examples: 206601
  download_size: 24241420
  dataset_size: 88053621
- config_name: ro-sq
  features:
  - name: id
    dtype: string
  - name: translation
    dtype:
      translation:
        languages:
        - ro
        - sq
  splits:
  - name: train
    num_bytes: 66845652
    num_examples: 212320
  download_size: 22515258
  dataset_size: 66845652
- config_name: bg-sr
  features:
  - name: id
    dtype: string
  - name: translation
    dtype:
      translation:
        languages:
        - bg
        - sr
  splits:
  - name: train
    num_bytes: 84698624
    num_examples: 211172
  download_size: 24007151
  dataset_size: 84698624
- config_name: bs-sr
  features:
  - name: id
    dtype: string
  - name: translation
    dtype:
      translation:
        languages:
        - bs
        - sr
  splits:
  - name: train
    num_bytes: 38418660
    num_examples: 135945
  download_size: 13804698
  dataset_size: 38418660
- config_name: el-sr
  features:
  - name: id
    dtype: string
  - name: translation
    dtype:
      translation:
        languages:
        - el
        - sr
  splits:
  - name: train
    num_bytes: 95035416
    num_examples: 224311
  download_size: 27108001
  dataset_size: 95035416
- config_name: en-sr
  features:
  - name: id
    dtype: string
  - name: translation
    dtype:
      translation:
        languages:
        - en
        - sr
  splits:
  - name: train
    num_bytes: 63670296
    num_examples: 225169
  download_size: 22279147
  dataset_size: 63670296
- config_name: hr-sr
  features:
  - name: id
    dtype: string
  - name: translation
    dtype:
      translation:
        languages:
        - hr
        - sr
  splits:
  - name: train
    num_bytes: 58560895
    num_examples: 203989
  download_size: 20791317
  dataset_size: 58560895
- config_name: mk-sr
  features:
  - name: id
    dtype: string
  - name: translation
    dtype:
      translation:
        languages:
        - mk
        - sr
  splits:
  - name: train
    num_bytes: 85333924
    num_examples: 207295
  download_size: 23878419
  dataset_size: 85333924
- config_name: ro-sr
  features:
  - name: id
    dtype: string
  - name: translation
    dtype:
      translation:
        languages:
        - ro
        - sr
  splits:
  - name: train
    num_bytes: 63899703
    num_examples: 210612
  download_size: 22113558
  dataset_size: 63899703
- config_name: sq-sr
  features:
  - name: id
    dtype: string
  - name: translation
    dtype:
      translation:
        languages:
        - sq
        - sr
  splits:
  - name: train
    num_bytes: 67503584
    num_examples: 224595
  download_size: 23330640
  dataset_size: 67503584
- config_name: bg-tr
  features:
  - name: id
    dtype: string
  - name: translation
    dtype:
      translation:
        languages:
        - bg
        - tr
  splits:
  - name: train
    num_bytes: 86915746
    num_examples: 206071
  download_size: 23915651
  dataset_size: 86915746
- config_name: bs-tr
  features:
  - name: id
    dtype: string
  - name: translation
    dtype:
      translation:
        languages:
        - bs
        - tr
  splits:
  - name: train
    num_bytes: 40280655
    num_examples: 133958
  download_size: 13819443
  dataset_size: 40280655
- config_name: el-tr
  features:
  - name: id
    dtype: string
  - name: translation
    dtype:
      translation:
        languages:
        - el
        - tr
  splits:
  - name: train
    num_bytes: 91637159
    num_examples: 207029
  download_size: 25396713
  dataset_size: 91637159
- config_name: en-tr
  features:
  - name: id
    dtype: string
  - name: translation
    dtype:
      translation:
        languages:
        - en
        - tr
  splits:
  - name: train
    num_bytes: 62858968
    num_examples: 207678
  download_size: 21049989
  dataset_size: 62858968
- config_name: hr-tr
  features:
  - name: id
    dtype: string
  - name: translation
    dtype:
      translation:
        languages:
        - hr
        - tr
  splits:
  - name: train
    num_bytes: 61188085
    num_examples: 199260
  download_size: 20809412
  dataset_size: 61188085
- config_name: mk-tr
  features:
  - name: id
    dtype: string
  - name: translation
    dtype:
      translation:
        languages:
        - mk
        - tr
  splits:
  - name: train
    num_bytes: 87536870
    num_examples: 203231
  download_size: 23781873
  dataset_size: 87536870
- config_name: ro-tr
  features:
  - name: id
    dtype: string
  - name: translation
    dtype:
      translation:
        languages:
        - ro
        - tr
  splits:
  - name: train
    num_bytes: 66726535
    num_examples: 206104
  download_size: 22165394
  dataset_size: 66726535
- config_name: sq-tr
  features:
  - name: id
    dtype: string
  - name: translation
    dtype:
      translation:
        languages:
        - sq
        - tr
  splits:
  - name: train
    num_bytes: 66371734
    num_examples: 207107
  download_size: 22014678
  dataset_size: 66371734
- config_name: sr-tr
  features:
  - name: id
    dtype: string
  - name: translation
    dtype:
      translation:
        languages:
        - sr
        - tr
  splits:
  - name: train
    num_bytes: 63371906
    num_examples: 205993
  download_size: 21602038
  dataset_size: 63371906
---

# Dataset Card for SETimes – A Parallel Corpus of English and South-East European Languages

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

- **Homepage:** http://nlp.ffzg.hr/resources/corpora/setimes/
- **Repository:** None
- **Paper:** None
- **Leaderboard:** [More Information Needed]
- **Point of Contact:** [More Information Needed]

### Dataset Summary

[More Information Needed]

### Supported Tasks and Leaderboards

[More Information Needed]

### Languages

[More Information Needed]

## Dataset Structure

### Data Instances

Here are some examples of questions and facts:


### Data Fields

[More Information Needed]

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

Thanks to [@abhishekkrthakur](https://github.com/abhishekkrthakur) for adding this dataset.