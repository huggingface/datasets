---
annotations_creators:
- found
language_creators:
- found
language:
- ar
- cs
- de
- en
- es
- fr
- it
- ja
- nl
- pt
- ru
- zh
license:
- unknown
multilinguality:
- multilingual
size_categories:
- 10K<n<100K
source_datasets:
- original
task_categories:
- translation
task_ids: []
paperswithcode_id: null
pretty_name: NewsCommentary
dataset_info:
- config_name: ar-cs
  features:
  - name: id
    dtype: string
  - name: translation
    dtype:
      translation:
        languages:
        - ar
        - cs
  splits:
  - name: train
    num_bytes: 51546460
    num_examples: 52128
  download_size: 16242918
  dataset_size: 51546460
- config_name: ar-de
  features:
  - name: id
    dtype: string
  - name: translation
    dtype:
      translation:
        languages:
        - ar
        - de
  splits:
  - name: train
    num_bytes: 69681419
    num_examples: 68916
  download_size: 21446768
  dataset_size: 69681419
- config_name: cs-de
  features:
  - name: id
    dtype: string
  - name: translation
    dtype:
      translation:
        languages:
        - cs
        - de
  splits:
  - name: train
    num_bytes: 57470799
    num_examples: 172706
  download_size: 21623462
  dataset_size: 57470799
- config_name: ar-en
  features:
  - name: id
    dtype: string
  - name: translation
    dtype:
      translation:
        languages:
        - ar
        - en
  splits:
  - name: train
    num_bytes: 80655273
    num_examples: 83187
  download_size: 24714354
  dataset_size: 80655273
- config_name: cs-en
  features:
  - name: id
    dtype: string
  - name: translation
    dtype:
      translation:
        languages:
        - cs
        - en
  splits:
  - name: train
    num_bytes: 54487874
    num_examples: 177278
  download_size: 20636368
  dataset_size: 54487874
- config_name: de-en
  features:
  - name: id
    dtype: string
  - name: translation
    dtype:
      translation:
        languages:
        - de
        - en
  splits:
  - name: train
    num_bytes: 73085451
    num_examples: 223153
  download_size: 26694093
  dataset_size: 73085451
- config_name: ar-es
  features:
  - name: id
    dtype: string
  - name: translation
    dtype:
      translation:
        languages:
        - ar
        - es
  splits:
  - name: train
    num_bytes: 79255985
    num_examples: 78074
  download_size: 24027435
  dataset_size: 79255985
- config_name: cs-es
  features:
  - name: id
    dtype: string
  - name: translation
    dtype:
      translation:
        languages:
        - cs
        - es
  splits:
  - name: train
    num_bytes: 56794825
    num_examples: 170489
  download_size: 20994380
  dataset_size: 56794825
- config_name: de-es
  features:
  - name: id
    dtype: string
  - name: translation
    dtype:
      translation:
        languages:
        - de
        - es
  splits:
  - name: train
    num_bytes: 74708740
    num_examples: 209839
  download_size: 26653320
  dataset_size: 74708740
- config_name: en-es
  features:
  - name: id
    dtype: string
  - name: translation
    dtype:
      translation:
        languages:
        - en
        - es
  splits:
  - name: train
    num_bytes: 78600789
    num_examples: 238872
  download_size: 28106064
  dataset_size: 78600789
- config_name: ar-fr
  features:
  - name: id
    dtype: string
  - name: translation
    dtype:
      translation:
        languages:
        - ar
        - fr
  splits:
  - name: train
    num_bytes: 71035061
    num_examples: 69157
  download_size: 21465481
  dataset_size: 71035061
- config_name: cs-fr
  features:
  - name: id
    dtype: string
  - name: translation
    dtype:
      translation:
        languages:
        - cs
        - fr
  splits:
  - name: train
    num_bytes: 50364837
    num_examples: 148578
  download_size: 18483528
  dataset_size: 50364837
- config_name: de-fr
  features:
  - name: id
    dtype: string
  - name: translation
    dtype:
      translation:
        languages:
        - de
        - fr
  splits:
  - name: train
    num_bytes: 67083899
    num_examples: 185442
  download_size: 23779967
  dataset_size: 67083899
- config_name: en-fr
  features:
  - name: id
    dtype: string
  - name: translation
    dtype:
      translation:
        languages:
        - en
        - fr
  splits:
  - name: train
    num_bytes: 70340014
    num_examples: 209479
  download_size: 24982452
  dataset_size: 70340014
- config_name: es-fr
  features:
  - name: id
    dtype: string
  - name: translation
    dtype:
      translation:
        languages:
        - es
        - fr
  splits:
  - name: train
    num_bytes: 71025933
    num_examples: 195241
  download_size: 24693126
  dataset_size: 71025933
- config_name: ar-it
  features:
  - name: id
    dtype: string
  - name: translation
    dtype:
      translation:
        languages:
        - ar
        - it
  splits:
  - name: train
    num_bytes: 17413450
    num_examples: 17227
  download_size: 5186438
  dataset_size: 17413450
- config_name: cs-it
  features:
  - name: id
    dtype: string
  - name: translation
    dtype:
      translation:
        languages:
        - cs
        - it
  splits:
  - name: train
    num_bytes: 10441845
    num_examples: 30547
  download_size: 3813656
  dataset_size: 10441845
- config_name: de-it
  features:
  - name: id
    dtype: string
  - name: translation
    dtype:
      translation:
        languages:
        - de
        - it
  splits:
  - name: train
    num_bytes: 13993454
    num_examples: 38961
  download_size: 4933419
  dataset_size: 13993454
- config_name: en-it
  features:
  - name: id
    dtype: string
  - name: translation
    dtype:
      translation:
        languages:
        - en
        - it
  splits:
  - name: train
    num_bytes: 14213972
    num_examples: 40009
  download_size: 4960768
  dataset_size: 14213972
- config_name: es-it
  features:
  - name: id
    dtype: string
  - name: translation
    dtype:
      translation:
        languages:
        - es
        - it
  splits:
  - name: train
    num_bytes: 15139636
    num_examples: 41497
  download_size: 5215173
  dataset_size: 15139636
- config_name: fr-it
  features:
  - name: id
    dtype: string
  - name: translation
    dtype:
      translation:
        languages:
        - fr
        - it
  splits:
  - name: train
    num_bytes: 14216079
    num_examples: 38485
  download_size: 4867267
  dataset_size: 14216079
- config_name: ar-ja
  features:
  - name: id
    dtype: string
  - name: translation
    dtype:
      translation:
        languages:
        - ar
        - ja
  splits:
  - name: train
    num_bytes: 661992
    num_examples: 569
  download_size: 206664
  dataset_size: 661992
- config_name: cs-ja
  features:
  - name: id
    dtype: string
  - name: translation
    dtype:
      translation:
        languages:
        - cs
        - ja
  splits:
  - name: train
    num_bytes: 487902
    num_examples: 622
  download_size: 184374
  dataset_size: 487902
- config_name: de-ja
  features:
  - name: id
    dtype: string
  - name: translation
    dtype:
      translation:
        languages:
        - de
        - ja
  splits:
  - name: train
    num_bytes: 465575
    num_examples: 582
  download_size: 171371
  dataset_size: 465575
- config_name: en-ja
  features:
  - name: id
    dtype: string
  - name: translation
    dtype:
      translation:
        languages:
        - en
        - ja
  splits:
  - name: train
    num_bytes: 485484
    num_examples: 637
  download_size: 178451
  dataset_size: 485484
- config_name: es-ja
  features:
  - name: id
    dtype: string
  - name: translation
    dtype:
      translation:
        languages:
        - es
        - ja
  splits:
  - name: train
    num_bytes: 484463
    num_examples: 602
  download_size: 175281
  dataset_size: 484463
- config_name: fr-ja
  features:
  - name: id
    dtype: string
  - name: translation
    dtype:
      translation:
        languages:
        - fr
        - ja
  splits:
  - name: train
    num_bytes: 418188
    num_examples: 519
  download_size: 151400
  dataset_size: 418188
- config_name: ar-nl
  features:
  - name: id
    dtype: string
  - name: translation
    dtype:
      translation:
        languages:
        - ar
        - nl
  splits:
  - name: train
    num_bytes: 9054134
    num_examples: 9047
  download_size: 2765542
  dataset_size: 9054134
- config_name: cs-nl
  features:
  - name: id
    dtype: string
  - name: translation
    dtype:
      translation:
        languages:
        - cs
        - nl
  splits:
  - name: train
    num_bytes: 5860976
    num_examples: 17358
  download_size: 2174494
  dataset_size: 5860976
- config_name: de-nl
  features:
  - name: id
    dtype: string
  - name: translation
    dtype:
      translation:
        languages:
        - de
        - nl
  splits:
  - name: train
    num_bytes: 7645565
    num_examples: 21439
  download_size: 2757414
  dataset_size: 7645565
- config_name: en-nl
  features:
  - name: id
    dtype: string
  - name: translation
    dtype:
      translation:
        languages:
        - en
        - nl
  splits:
  - name: train
    num_bytes: 7316599
    num_examples: 19399
  download_size: 2575916
  dataset_size: 7316599
- config_name: es-nl
  features:
  - name: id
    dtype: string
  - name: translation
    dtype:
      translation:
        languages:
        - es
        - nl
  splits:
  - name: train
    num_bytes: 7560123
    num_examples: 21012
  download_size: 2674557
  dataset_size: 7560123
- config_name: fr-nl
  features:
  - name: id
    dtype: string
  - name: translation
    dtype:
      translation:
        languages:
        - fr
        - nl
  splits:
  - name: train
    num_bytes: 7603503
    num_examples: 20898
  download_size: 2659946
  dataset_size: 7603503
- config_name: it-nl
  features:
  - name: id
    dtype: string
  - name: translation
    dtype:
      translation:
        languages:
        - it
        - nl
  splits:
  - name: train
    num_bytes: 5380912
    num_examples: 15428
  download_size: 1899094
  dataset_size: 5380912
- config_name: ar-pt
  features:
  - name: id
    dtype: string
  - name: translation
    dtype:
      translation:
        languages:
        - ar
        - pt
  splits:
  - name: train
    num_bytes: 11340074
    num_examples: 11433
  download_size: 3504173
  dataset_size: 11340074
- config_name: cs-pt
  features:
  - name: id
    dtype: string
  - name: translation
    dtype:
      translation:
        languages:
        - cs
        - pt
  splits:
  - name: train
    num_bytes: 6183725
    num_examples: 18356
  download_size: 2310039
  dataset_size: 6183725
- config_name: de-pt
  features:
  - name: id
    dtype: string
  - name: translation
    dtype:
      translation:
        languages:
        - de
        - pt
  splits:
  - name: train
    num_bytes: 7699083
    num_examples: 21884
  download_size: 2794173
  dataset_size: 7699083
- config_name: en-pt
  features:
  - name: id
    dtype: string
  - name: translation
    dtype:
      translation:
        languages:
        - en
        - pt
  splits:
  - name: train
    num_bytes: 9238819
    num_examples: 25929
  download_size: 3310748
  dataset_size: 9238819
- config_name: es-pt
  features:
  - name: id
    dtype: string
  - name: translation
    dtype:
      translation:
        languages:
        - es
        - pt
  splits:
  - name: train
    num_bytes: 9195685
    num_examples: 25551
  download_size: 3278814
  dataset_size: 9195685
- config_name: fr-pt
  features:
  - name: id
    dtype: string
  - name: translation
    dtype:
      translation:
        languages:
        - fr
        - pt
  splits:
  - name: train
    num_bytes: 9261169
    num_examples: 25642
  download_size: 3254925
  dataset_size: 9261169
- config_name: it-pt
  features:
  - name: id
    dtype: string
  - name: translation
    dtype:
      translation:
        languages:
        - it
        - pt
  splits:
  - name: train
    num_bytes: 3988570
    num_examples: 11407
  download_size: 1397344
  dataset_size: 3988570
- config_name: nl-pt
  features:
  - name: id
    dtype: string
  - name: translation
    dtype:
      translation:
        languages:
        - nl
        - pt
  splits:
  - name: train
    num_bytes: 3612339
    num_examples: 10598
  download_size: 1290715
  dataset_size: 3612339
- config_name: ar-ru
  features:
  - name: id
    dtype: string
  - name: translation
    dtype:
      translation:
        languages:
        - ar
        - ru
  splits:
  - name: train
    num_bytes: 105804303
    num_examples: 84455
  download_size: 28643600
  dataset_size: 105804303
- config_name: cs-ru
  features:
  - name: id
    dtype: string
  - name: translation
    dtype:
      translation:
        languages:
        - cs
        - ru
  splits:
  - name: train
    num_bytes: 71185695
    num_examples: 161133
  download_size: 21917168
  dataset_size: 71185695
- config_name: de-ru
  features:
  - name: id
    dtype: string
  - name: translation
    dtype:
      translation:
        languages:
        - de
        - ru
  splits:
  - name: train
    num_bytes: 81812014
    num_examples: 175905
  download_size: 24610973
  dataset_size: 81812014
- config_name: en-ru
  features:
  - name: id
    dtype: string
  - name: translation
    dtype:
      translation:
        languages:
        - en
        - ru
  splits:
  - name: train
    num_bytes: 83282480
    num_examples: 190104
  download_size: 24849511
  dataset_size: 83282480
- config_name: es-ru
  features:
  - name: id
    dtype: string
  - name: translation
    dtype:
      translation:
        languages:
        - es
        - ru
  splits:
  - name: train
    num_bytes: 84345850
    num_examples: 180217
  download_size: 24883942
  dataset_size: 84345850
- config_name: fr-ru
  features:
  - name: id
    dtype: string
  - name: translation
    dtype:
      translation:
        languages:
        - fr
        - ru
  splits:
  - name: train
    num_bytes: 75967253
    num_examples: 160740
  download_size: 22385777
  dataset_size: 75967253
- config_name: it-ru
  features:
  - name: id
    dtype: string
  - name: translation
    dtype:
      translation:
        languages:
        - it
        - ru
  splits:
  - name: train
    num_bytes: 12915073
    num_examples: 27267
  download_size: 3781318
  dataset_size: 12915073
- config_name: ja-ru
  features:
  - name: id
    dtype: string
  - name: translation
    dtype:
      translation:
        languages:
        - ja
        - ru
  splits:
  - name: train
    num_bytes: 596166
    num_examples: 586
  download_size: 184791
  dataset_size: 596166
- config_name: nl-ru
  features:
  - name: id
    dtype: string
  - name: translation
    dtype:
      translation:
        languages:
        - nl
        - ru
  splits:
  - name: train
    num_bytes: 8933805
    num_examples: 19112
  download_size: 2662250
  dataset_size: 8933805
- config_name: pt-ru
  features:
  - name: id
    dtype: string
  - name: translation
    dtype:
      translation:
        languages:
        - pt
        - ru
  splits:
  - name: train
    num_bytes: 8645475
    num_examples: 18458
  download_size: 2584012
  dataset_size: 8645475
- config_name: ar-zh
  features:
  - name: id
    dtype: string
  - name: translation
    dtype:
      translation:
        languages:
        - ar
        - zh
  splits:
  - name: train
    num_bytes: 65483204
    num_examples: 66021
  download_size: 21625859
  dataset_size: 65483204
- config_name: cs-zh
  features:
  - name: id
    dtype: string
  - name: translation
    dtype:
      translation:
        languages:
        - cs
        - zh
  splits:
  - name: train
    num_bytes: 29971192
    num_examples: 45424
  download_size: 12495392
  dataset_size: 29971192
- config_name: de-zh
  features:
  - name: id
    dtype: string
  - name: translation
    dtype:
      translation:
        languages:
        - de
        - zh
  splits:
  - name: train
    num_bytes: 39044704
    num_examples: 59020
  download_size: 15773631
  dataset_size: 39044704
- config_name: en-zh
  features:
  - name: id
    dtype: string
  - name: translation
    dtype:
      translation:
        languages:
        - en
        - zh
  splits:
  - name: train
    num_bytes: 44596087
    num_examples: 69206
  download_size: 18101984
  dataset_size: 44596087
- config_name: es-zh
  features:
  - name: id
    dtype: string
  - name: translation
    dtype:
      translation:
        languages:
        - es
        - zh
  splits:
  - name: train
    num_bytes: 43940013
    num_examples: 65424
  download_size: 17424938
  dataset_size: 43940013
- config_name: fr-zh
  features:
  - name: id
    dtype: string
  - name: translation
    dtype:
      translation:
        languages:
        - fr
        - zh
  splits:
  - name: train
    num_bytes: 40144071
    num_examples: 59060
  download_size: 15817862
  dataset_size: 40144071
- config_name: it-zh
  features:
  - name: id
    dtype: string
  - name: translation
    dtype:
      translation:
        languages:
        - it
        - zh
  splits:
  - name: train
    num_bytes: 9676756
    num_examples: 14652
  download_size: 3799012
  dataset_size: 9676756
- config_name: ja-zh
  features:
  - name: id
    dtype: string
  - name: translation
    dtype:
      translation:
        languages:
        - ja
        - zh
  splits:
  - name: train
    num_bytes: 462685
    num_examples: 570
  download_size: 181924
  dataset_size: 462685
- config_name: nl-zh
  features:
  - name: id
    dtype: string
  - name: translation
    dtype:
      translation:
        languages:
        - nl
        - zh
  splits:
  - name: train
    num_bytes: 5509070
    num_examples: 8433
  download_size: 2218937
  dataset_size: 5509070
- config_name: pt-zh
  features:
  - name: id
    dtype: string
  - name: translation
    dtype:
      translation:
        languages:
        - pt
        - zh
  splits:
  - name: train
    num_bytes: 7152774
    num_examples: 10873
  download_size: 2889296
  dataset_size: 7152774
- config_name: ru-zh
  features:
  - name: id
    dtype: string
  - name: translation
    dtype:
      translation:
        languages:
        - ru
        - zh
  splits:
  - name: train
    num_bytes: 43112824
    num_examples: 47687
  download_size: 14225498
  dataset_size: 43112824
---

# Dataset Card for NewsCommentary

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

- **Homepage:** http://opus.nlpl.eu/News-Commentary.php
- **Repository:** None
- **Paper:** http://www.lrec-conf.org/proceedings/lrec2012/pdf/463_Paper.pdf
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

[More Information Needed]

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