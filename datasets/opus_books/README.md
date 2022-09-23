---
annotations_creators:
- found
language_creators:
- found
language:
- ca
- de
- el
- en
- eo
- es
- fi
- fr
- hu
- it
- nl
- 'no'
- pl
- pt
- ru
- sv
license:
- unknown
multilinguality:
- multilingual
size_categories:
- 1K<n<10K
source_datasets:
- original
task_categories:
- translation
task_ids: []
paperswithcode_id: null
pretty_name: OpusBooks
dataset_info:
- config_name: ca-de
  features:
  - name: id
    dtype: string
  - name: translation
    dtype:
      translation:
        languages:
        - ca
        - de
  splits:
  - name: train
    num_bytes: 899565
    num_examples: 4445
  download_size: 349126
  dataset_size: 899565
- config_name: ca-en
  features:
  - name: id
    dtype: string
  - name: translation
    dtype:
      translation:
        languages:
        - ca
        - en
  splits:
  - name: train
    num_bytes: 863174
    num_examples: 4605
  download_size: 336276
  dataset_size: 863174
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
    num_bytes: 13739047
    num_examples: 51467
  download_size: 5124458
  dataset_size: 13739047
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
    num_bytes: 552579
    num_examples: 1285
  download_size: 175537
  dataset_size: 552579
- config_name: de-eo
  features:
  - name: id
    dtype: string
  - name: translation
    dtype:
      translation:
        languages:
        - de
        - eo
  splits:
  - name: train
    num_bytes: 398885
    num_examples: 1363
  download_size: 150822
  dataset_size: 398885
- config_name: en-eo
  features:
  - name: id
    dtype: string
  - name: translation
    dtype:
      translation:
        languages:
        - en
        - eo
  splits:
  - name: train
    num_bytes: 386231
    num_examples: 1562
  download_size: 145339
  dataset_size: 386231
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
    num_bytes: 7592487
    num_examples: 27526
  download_size: 2802010
  dataset_size: 7592487
- config_name: el-es
  features:
  - name: id
    dtype: string
  - name: translation
    dtype:
      translation:
        languages:
        - el
        - es
  splits:
  - name: train
    num_bytes: 527991
    num_examples: 1096
  download_size: 168306
  dataset_size: 527991
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
    num_bytes: 25291783
    num_examples: 93470
  download_size: 9257150
  dataset_size: 25291783
- config_name: eo-es
  features:
  - name: id
    dtype: string
  - name: translation
    dtype:
      translation:
        languages:
        - eo
        - es
  splits:
  - name: train
    num_bytes: 409591
    num_examples: 1677
  download_size: 154950
  dataset_size: 409591
- config_name: en-fi
  features:
  - name: id
    dtype: string
  - name: translation
    dtype:
      translation:
        languages:
        - en
        - fi
  splits:
  - name: train
    num_bytes: 715039
    num_examples: 3645
  download_size: 266714
  dataset_size: 715039
- config_name: es-fi
  features:
  - name: id
    dtype: string
  - name: translation
    dtype:
      translation:
        languages:
        - es
        - fi
  splits:
  - name: train
    num_bytes: 710462
    num_examples: 3344
  download_size: 264316
  dataset_size: 710462
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
    num_bytes: 9544399
    num_examples: 34916
  download_size: 3556168
  dataset_size: 9544399
- config_name: el-fr
  features:
  - name: id
    dtype: string
  - name: translation
    dtype:
      translation:
        languages:
        - el
        - fr
  splits:
  - name: train
    num_bytes: 539933
    num_examples: 1237
  download_size: 169241
  dataset_size: 539933
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
    num_bytes: 32997199
    num_examples: 127085
  download_size: 12009501
  dataset_size: 32997199
- config_name: eo-fr
  features:
  - name: id
    dtype: string
  - name: translation
    dtype:
      translation:
        languages:
        - eo
        - fr
  splits:
  - name: train
    num_bytes: 412999
    num_examples: 1588
  download_size: 152040
  dataset_size: 412999
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
    num_bytes: 14382198
    num_examples: 56319
  download_size: 5203099
  dataset_size: 14382198
- config_name: fi-fr
  features:
  - name: id
    dtype: string
  - name: translation
    dtype:
      translation:
        languages:
        - fi
        - fr
  splits:
  - name: train
    num_bytes: 746097
    num_examples: 3537
  download_size: 276633
  dataset_size: 746097
- config_name: ca-hu
  features:
  - name: id
    dtype: string
  - name: translation
    dtype:
      translation:
        languages:
        - ca
        - hu
  splits:
  - name: train
    num_bytes: 886162
    num_examples: 4463
  download_size: 346425
  dataset_size: 886162
- config_name: de-hu
  features:
  - name: id
    dtype: string
  - name: translation
    dtype:
      translation:
        languages:
        - de
        - hu
  splits:
  - name: train
    num_bytes: 13515043
    num_examples: 51780
  download_size: 5069455
  dataset_size: 13515043
- config_name: el-hu
  features:
  - name: id
    dtype: string
  - name: translation
    dtype:
      translation:
        languages:
        - el
        - hu
  splits:
  - name: train
    num_bytes: 546290
    num_examples: 1090
  download_size: 176715
  dataset_size: 546290
- config_name: en-hu
  features:
  - name: id
    dtype: string
  - name: translation
    dtype:
      translation:
        languages:
        - en
        - hu
  splits:
  - name: train
    num_bytes: 35256934
    num_examples: 137151
  download_size: 13232578
  dataset_size: 35256934
- config_name: eo-hu
  features:
  - name: id
    dtype: string
  - name: translation
    dtype:
      translation:
        languages:
        - eo
        - hu
  splits:
  - name: train
    num_bytes: 389112
    num_examples: 1636
  download_size: 151332
  dataset_size: 389112
- config_name: fr-hu
  features:
  - name: id
    dtype: string
  - name: translation
    dtype:
      translation:
        languages:
        - fr
        - hu
  splits:
  - name: train
    num_bytes: 22483133
    num_examples: 89337
  download_size: 8328639
  dataset_size: 22483133
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
    num_bytes: 7760020
    num_examples: 27381
  download_size: 2811066
  dataset_size: 7760020
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
    num_bytes: 8993803
    num_examples: 32332
  download_size: 3295251
  dataset_size: 8993803
- config_name: eo-it
  features:
  - name: id
    dtype: string
  - name: translation
    dtype:
      translation:
        languages:
        - eo
        - it
  splits:
  - name: train
    num_bytes: 387606
    num_examples: 1453
  download_size: 146899
  dataset_size: 387606
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
    num_bytes: 7837703
    num_examples: 28868
  download_size: 2864028
  dataset_size: 7837703
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
    num_bytes: 4752171
    num_examples: 14692
  download_size: 1737670
  dataset_size: 4752171
- config_name: hu-it
  features:
  - name: id
    dtype: string
  - name: translation
    dtype:
      translation:
        languages:
        - hu
        - it
  splits:
  - name: train
    num_bytes: 8445585
    num_examples: 30949
  download_size: 3101681
  dataset_size: 8445585
- config_name: ca-nl
  features:
  - name: id
    dtype: string
  - name: translation
    dtype:
      translation:
        languages:
        - ca
        - nl
  splits:
  - name: train
    num_bytes: 884823
    num_examples: 4329
  download_size: 340308
  dataset_size: 884823
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
    num_bytes: 3561764
    num_examples: 15622
  download_size: 1325189
  dataset_size: 3561764
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
    num_bytes: 10278038
    num_examples: 38652
  download_size: 3727995
  dataset_size: 10278038
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
    num_bytes: 9062389
    num_examples: 32247
  download_size: 3245558
  dataset_size: 9062389
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
    num_bytes: 10408148
    num_examples: 40017
  download_size: 3720151
  dataset_size: 10408148
- config_name: hu-nl
  features:
  - name: id
    dtype: string
  - name: translation
    dtype:
      translation:
        languages:
        - hu
        - nl
  splits:
  - name: train
    num_bytes: 10814173
    num_examples: 43428
  download_size: 3998988
  dataset_size: 10814173
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
    num_bytes: 1328305
    num_examples: 2359
  download_size: 476875
  dataset_size: 1328305
- config_name: en-no
  features:
  - name: id
    dtype: string
  - name: translation
    dtype:
      translation:
        languages:
        - en
        - 'no'
  splits:
  - name: train
    num_bytes: 661978
    num_examples: 3499
  download_size: 246977
  dataset_size: 661978
- config_name: es-no
  features:
  - name: id
    dtype: string
  - name: translation
    dtype:
      translation:
        languages:
        - es
        - 'no'
  splits:
  - name: train
    num_bytes: 729125
    num_examples: 3585
  download_size: 270796
  dataset_size: 729125
- config_name: fi-no
  features:
  - name: id
    dtype: string
  - name: translation
    dtype:
      translation:
        languages:
        - fi
        - 'no'
  splits:
  - name: train
    num_bytes: 691181
    num_examples: 3414
  download_size: 256267
  dataset_size: 691181
- config_name: fr-no
  features:
  - name: id
    dtype: string
  - name: translation
    dtype:
      translation:
        languages:
        - fr
        - 'no'
  splits:
  - name: train
    num_bytes: 692786
    num_examples: 3449
  download_size: 256501
  dataset_size: 692786
- config_name: hu-no
  features:
  - name: id
    dtype: string
  - name: translation
    dtype:
      translation:
        languages:
        - hu
        - 'no'
  splits:
  - name: train
    num_bytes: 695497
    num_examples: 3410
  download_size: 267047
  dataset_size: 695497
- config_name: en-pl
  features:
  - name: id
    dtype: string
  - name: translation
    dtype:
      translation:
        languages:
        - en
        - pl
  splits:
  - name: train
    num_bytes: 583091
    num_examples: 2831
  download_size: 226855
  dataset_size: 583091
- config_name: fi-pl
  features:
  - name: id
    dtype: string
  - name: translation
    dtype:
      translation:
        languages:
        - fi
        - pl
  splits:
  - name: train
    num_bytes: 613791
    num_examples: 2814
  download_size: 236123
  dataset_size: 613791
- config_name: fr-pl
  features:
  - name: id
    dtype: string
  - name: translation
    dtype:
      translation:
        languages:
        - fr
        - pl
  splits:
  - name: train
    num_bytes: 614248
    num_examples: 2825
  download_size: 235905
  dataset_size: 614248
- config_name: hu-pl
  features:
  - name: id
    dtype: string
  - name: translation
    dtype:
      translation:
        languages:
        - hu
        - pl
  splits:
  - name: train
    num_bytes: 616161
    num_examples: 2859
  download_size: 245670
  dataset_size: 616161
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
    num_bytes: 317155
    num_examples: 1102
  download_size: 116319
  dataset_size: 317155
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
    num_bytes: 309689
    num_examples: 1404
  download_size: 111837
  dataset_size: 309689
- config_name: eo-pt
  features:
  - name: id
    dtype: string
  - name: translation
    dtype:
      translation:
        languages:
        - eo
        - pt
  splits:
  - name: train
    num_bytes: 311079
    num_examples: 1259
  download_size: 116157
  dataset_size: 311079
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
    num_bytes: 326884
    num_examples: 1327
  download_size: 120549
  dataset_size: 326884
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
    num_bytes: 324616
    num_examples: 1263
  download_size: 115920
  dataset_size: 324616
- config_name: hu-pt
  features:
  - name: id
    dtype: string
  - name: translation
    dtype:
      translation:
        languages:
        - hu
        - pt
  splits:
  - name: train
    num_bytes: 302972
    num_examples: 1184
  download_size: 115002
  dataset_size: 302972
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
    num_bytes: 301428
    num_examples: 1163
  download_size: 111050
  dataset_size: 301428
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
    num_bytes: 5764673
    num_examples: 17373
  download_size: 1799371
  dataset_size: 5764673
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
    num_bytes: 5190880
    num_examples: 17496
  download_size: 1613419
  dataset_size: 5190880
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
    num_bytes: 5281130
    num_examples: 16793
  download_size: 1648606
  dataset_size: 5281130
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
    num_bytes: 2474210
    num_examples: 8197
  download_size: 790541
  dataset_size: 2474210
- config_name: hu-ru
  features:
  - name: id
    dtype: string
  - name: translation
    dtype:
      translation:
        languages:
        - hu
        - ru
  splits:
  - name: train
    num_bytes: 7818688
    num_examples: 26127
  download_size: 2469765
  dataset_size: 7818688
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
    num_bytes: 5316952
    num_examples: 17906
  download_size: 1620478
  dataset_size: 5316952
- config_name: en-sv
  features:
  - name: id
    dtype: string
  - name: translation
    dtype:
      translation:
        languages:
        - en
        - sv
  splits:
  - name: train
    num_bytes: 790785
    num_examples: 3095
  download_size: 304975
  dataset_size: 790785
- config_name: fr-sv
  features:
  - name: id
    dtype: string
  - name: translation
    dtype:
      translation:
        languages:
        - fr
        - sv
  splits:
  - name: train
    num_bytes: 833553
    num_examples: 3002
  download_size: 321660
  dataset_size: 833553
- config_name: it-sv
  features:
  - name: id
    dtype: string
  - name: translation
    dtype:
      translation:
        languages:
        - it
        - sv
  splits:
  - name: train
    num_bytes: 811413
    num_examples: 2998
  download_size: 307821
  dataset_size: 811413
---

# Dataset Card for OpusBooks

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

- **Homepage:** http://opus.nlpl.eu/Books.php
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