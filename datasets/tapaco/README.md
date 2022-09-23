---
annotations_creators:
- machine-generated
language_creators:
- crowdsourced
language:
- af
- ar
- az
- be
- ber
- bg
- bn
- br
- ca
- cbk
- cmn
- cs
- da
- de
- el
- en
- eo
- es
- et
- eu
- fi
- fr
- gl
- gos
- he
- hi
- hr
- hu
- hy
- ia
- id
- ie
- io
- is
- it
- ja
- jbo
- kab
- ko
- kw
- la
- lfn
- lt
- mk
- mr
- nb
- nds
- nl
- orv
- ota
- pes
- pl
- pt
- rn
- ro
- ru
- sl
- sr
- sv
- tk
- tl
- tlh
- tok
- tr
- tt
- ug
- uk
- ur
- vi
- vo
- war
- wuu
- yue
license:
- cc-by-2.0
multilinguality:
- multilingual
size_categories:
- 100K<n<1M
- 10K<n<100K
- 1K<n<10K
- 1M<n<10M
- n<1K
source_datasets:
- extended|other-tatoeba
task_categories:
- text2text-generation
- translation
- text-classification
task_ids:
- text2text-generation-other-paraphrase-generation
- semantic-similarity-classification
paperswithcode_id: tapaco
pretty_name: TaPaCo Corpus
configs:
- af
- all_languages
- ar
- az
- be
- ber
- bg
- bn
- br
- ca
- cbk
- cmn
- cs
- da
- de
- el
- en
- eo
- es
- et
- eu
- fi
- fr
- gl
- gos
- he
- hi
- hr
- hu
- hy
- ia
- id
- ie
- io
- is
- it
- ja
- jbo
- kab
- ko
- kw
- la
- lfn
- lt
- mk
- mr
- nb
- nds
- nl
- orv
- ota
- pes
- pl
- pt
- rn
- ro
- ru
- sl
- sr
- sv
- tk
- tl
- tlh
- tok
- tr
- tt
- ug
- uk
- ur
- vi
- vo
- war
- wuu
- yue
dataset_info:
- config_name: all_languages
  features:
  - name: paraphrase_set_id
    dtype: string
  - name: sentence_id
    dtype: string
  - name: paraphrase
    dtype: string
  - name: lists
    sequence: string
  - name: tags
    sequence: string
  - name: language
    dtype: string
  splits:
  - name: train
    num_bytes: 162802556
    num_examples: 1926192
  download_size: 32213126
  dataset_size: 162802556
- config_name: af
  features:
  - name: paraphrase_set_id
    dtype: string
  - name: sentence_id
    dtype: string
  - name: paraphrase
    dtype: string
  - name: lists
    sequence: string
  - name: tags
    sequence: string
  - name: language
    dtype: string
  splits:
  - name: train
    num_bytes: 21219
    num_examples: 307
  download_size: 32213126
  dataset_size: 21219
- config_name: ar
  features:
  - name: paraphrase_set_id
    dtype: string
  - name: sentence_id
    dtype: string
  - name: paraphrase
    dtype: string
  - name: lists
    sequence: string
  - name: tags
    sequence: string
  - name: language
    dtype: string
  splits:
  - name: train
    num_bytes: 546200
    num_examples: 6446
  download_size: 32213126
  dataset_size: 546200
- config_name: az
  features:
  - name: paraphrase_set_id
    dtype: string
  - name: sentence_id
    dtype: string
  - name: paraphrase
    dtype: string
  - name: lists
    sequence: string
  - name: tags
    sequence: string
  - name: language
    dtype: string
  splits:
  - name: train
    num_bytes: 44461
    num_examples: 624
  download_size: 32213126
  dataset_size: 44461
- config_name: be
  features:
  - name: paraphrase_set_id
    dtype: string
  - name: sentence_id
    dtype: string
  - name: paraphrase
    dtype: string
  - name: lists
    sequence: string
  - name: tags
    sequence: string
  - name: language
    dtype: string
  splits:
  - name: train
    num_bytes: 140376
    num_examples: 1512
  download_size: 32213126
  dataset_size: 140376
- config_name: ber
  features:
  - name: paraphrase_set_id
    dtype: string
  - name: sentence_id
    dtype: string
  - name: paraphrase
    dtype: string
  - name: lists
    sequence: string
  - name: tags
    sequence: string
  - name: language
    dtype: string
  splits:
  - name: train
    num_bytes: 5118620
    num_examples: 67484
  download_size: 32213126
  dataset_size: 5118620
- config_name: bg
  features:
  - name: paraphrase_set_id
    dtype: string
  - name: sentence_id
    dtype: string
  - name: paraphrase
    dtype: string
  - name: lists
    sequence: string
  - name: tags
    sequence: string
  - name: language
    dtype: string
  splits:
  - name: train
    num_bytes: 590535
    num_examples: 6324
  download_size: 32213126
  dataset_size: 590535
- config_name: bn
  features:
  - name: paraphrase_set_id
    dtype: string
  - name: sentence_id
    dtype: string
  - name: paraphrase
    dtype: string
  - name: lists
    sequence: string
  - name: tags
    sequence: string
  - name: language
    dtype: string
  splits:
  - name: train
    num_bytes: 146654
    num_examples: 1440
  download_size: 32213126
  dataset_size: 146654
- config_name: br
  features:
  - name: paraphrase_set_id
    dtype: string
  - name: sentence_id
    dtype: string
  - name: paraphrase
    dtype: string
  - name: lists
    sequence: string
  - name: tags
    sequence: string
  - name: language
    dtype: string
  splits:
  - name: train
    num_bytes: 177919
    num_examples: 2536
  download_size: 32213126
  dataset_size: 177919
- config_name: ca
  features:
  - name: paraphrase_set_id
    dtype: string
  - name: sentence_id
    dtype: string
  - name: paraphrase
    dtype: string
  - name: lists
    sequence: string
  - name: tags
    sequence: string
  - name: language
    dtype: string
  splits:
  - name: train
    num_bytes: 39404
    num_examples: 518
  download_size: 32213126
  dataset_size: 39404
- config_name: cbk
  features:
  - name: paraphrase_set_id
    dtype: string
  - name: sentence_id
    dtype: string
  - name: paraphrase
    dtype: string
  - name: lists
    sequence: string
  - name: tags
    sequence: string
  - name: language
    dtype: string
  splits:
  - name: train
    num_bytes: 19404
    num_examples: 262
  download_size: 32213126
  dataset_size: 19404
- config_name: cmn
  features:
  - name: paraphrase_set_id
    dtype: string
  - name: sentence_id
    dtype: string
  - name: paraphrase
    dtype: string
  - name: lists
    sequence: string
  - name: tags
    sequence: string
  - name: language
    dtype: string
  splits:
  - name: train
    num_bytes: 964514
    num_examples: 12549
  download_size: 32213126
  dataset_size: 964514
- config_name: cs
  features:
  - name: paraphrase_set_id
    dtype: string
  - name: sentence_id
    dtype: string
  - name: paraphrase
    dtype: string
  - name: lists
    sequence: string
  - name: tags
    sequence: string
  - name: language
    dtype: string
  splits:
  - name: train
    num_bytes: 482292
    num_examples: 6659
  download_size: 32213126
  dataset_size: 482292
- config_name: da
  features:
  - name: paraphrase_set_id
    dtype: string
  - name: sentence_id
    dtype: string
  - name: paraphrase
    dtype: string
  - name: lists
    sequence: string
  - name: tags
    sequence: string
  - name: language
    dtype: string
  splits:
  - name: train
    num_bytes: 848886
    num_examples: 11220
  download_size: 32213126
  dataset_size: 848886
- config_name: de
  features:
  - name: paraphrase_set_id
    dtype: string
  - name: sentence_id
    dtype: string
  - name: paraphrase
    dtype: string
  - name: lists
    sequence: string
  - name: tags
    sequence: string
  - name: language
    dtype: string
  splits:
  - name: train
    num_bytes: 10593377
    num_examples: 125091
  download_size: 32213126
  dataset_size: 10593377
- config_name: el
  features:
  - name: paraphrase_set_id
    dtype: string
  - name: sentence_id
    dtype: string
  - name: paraphrase
    dtype: string
  - name: lists
    sequence: string
  - name: tags
    sequence: string
  - name: language
    dtype: string
  splits:
  - name: train
    num_bytes: 926054
    num_examples: 10072
  download_size: 32213126
  dataset_size: 926054
- config_name: en
  features:
  - name: paraphrase_set_id
    dtype: string
  - name: sentence_id
    dtype: string
  - name: paraphrase
    dtype: string
  - name: lists
    sequence: string
  - name: tags
    sequence: string
  - name: language
    dtype: string
  splits:
  - name: train
    num_bytes: 15070349
    num_examples: 158053
  download_size: 32213126
  dataset_size: 15070349
- config_name: eo
  features:
  - name: paraphrase_set_id
    dtype: string
  - name: sentence_id
    dtype: string
  - name: paraphrase
    dtype: string
  - name: lists
    sequence: string
  - name: tags
    sequence: string
  - name: language
    dtype: string
  splits:
  - name: train
    num_bytes: 16810965
    num_examples: 207105
  download_size: 32213126
  dataset_size: 16810965
- config_name: es
  features:
  - name: paraphrase_set_id
    dtype: string
  - name: sentence_id
    dtype: string
  - name: paraphrase
    dtype: string
  - name: lists
    sequence: string
  - name: tags
    sequence: string
  - name: language
    dtype: string
  splits:
  - name: train
    num_bytes: 6851135
    num_examples: 85064
  download_size: 32213126
  dataset_size: 6851135
- config_name: et
  features:
  - name: paraphrase_set_id
    dtype: string
  - name: sentence_id
    dtype: string
  - name: paraphrase
    dtype: string
  - name: lists
    sequence: string
  - name: tags
    sequence: string
  - name: language
    dtype: string
  splits:
  - name: train
    num_bytes: 17127
    num_examples: 241
  download_size: 32213126
  dataset_size: 17127
- config_name: eu
  features:
  - name: paraphrase_set_id
    dtype: string
  - name: sentence_id
    dtype: string
  - name: paraphrase
    dtype: string
  - name: lists
    sequence: string
  - name: tags
    sequence: string
  - name: language
    dtype: string
  splits:
  - name: train
    num_bytes: 42702
    num_examples: 573
  download_size: 32213126
  dataset_size: 42702
- config_name: fi
  features:
  - name: paraphrase_set_id
    dtype: string
  - name: sentence_id
    dtype: string
  - name: paraphrase
    dtype: string
  - name: lists
    sequence: string
  - name: tags
    sequence: string
  - name: language
    dtype: string
  splits:
  - name: train
    num_bytes: 2520167
    num_examples: 31753
  download_size: 32213126
  dataset_size: 2520167
- config_name: fr
  features:
  - name: paraphrase_set_id
    dtype: string
  - name: sentence_id
    dtype: string
  - name: paraphrase
    dtype: string
  - name: lists
    sequence: string
  - name: tags
    sequence: string
  - name: language
    dtype: string
  splits:
  - name: train
    num_bytes: 9481426
    num_examples: 116733
  download_size: 32213126
  dataset_size: 9481426
- config_name: gl
  features:
  - name: paraphrase_set_id
    dtype: string
  - name: sentence_id
    dtype: string
  - name: paraphrase
    dtype: string
  - name: lists
    sequence: string
  - name: tags
    sequence: string
  - name: language
    dtype: string
  splits:
  - name: train
    num_bytes: 26551
    num_examples: 351
  download_size: 32213126
  dataset_size: 26551
- config_name: gos
  features:
  - name: paraphrase_set_id
    dtype: string
  - name: sentence_id
    dtype: string
  - name: paraphrase
    dtype: string
  - name: lists
    sequence: string
  - name: tags
    sequence: string
  - name: language
    dtype: string
  splits:
  - name: train
    num_bytes: 18442
    num_examples: 279
  download_size: 32213126
  dataset_size: 18442
- config_name: he
  features:
  - name: paraphrase_set_id
    dtype: string
  - name: sentence_id
    dtype: string
  - name: paraphrase
    dtype: string
  - name: lists
    sequence: string
  - name: tags
    sequence: string
  - name: language
    dtype: string
  splits:
  - name: train
    num_bytes: 6024345
    num_examples: 68350
  download_size: 32213126
  dataset_size: 6024345
- config_name: hi
  features:
  - name: paraphrase_set_id
    dtype: string
  - name: sentence_id
    dtype: string
  - name: paraphrase
    dtype: string
  - name: lists
    sequence: string
  - name: tags
    sequence: string
  - name: language
    dtype: string
  splits:
  - name: train
    num_bytes: 209382
    num_examples: 1913
  download_size: 32213126
  dataset_size: 209382
- config_name: hr
  features:
  - name: paraphrase_set_id
    dtype: string
  - name: sentence_id
    dtype: string
  - name: paraphrase
    dtype: string
  - name: lists
    sequence: string
  - name: tags
    sequence: string
  - name: language
    dtype: string
  splits:
  - name: train
    num_bytes: 36638
    num_examples: 505
  download_size: 32213126
  dataset_size: 36638
- config_name: hu
  features:
  - name: paraphrase_set_id
    dtype: string
  - name: sentence_id
    dtype: string
  - name: paraphrase
    dtype: string
  - name: lists
    sequence: string
  - name: tags
    sequence: string
  - name: language
    dtype: string
  splits:
  - name: train
    num_bytes: 5289610
    num_examples: 67964
  download_size: 32213126
  dataset_size: 5289610
- config_name: hy
  features:
  - name: paraphrase_set_id
    dtype: string
  - name: sentence_id
    dtype: string
  - name: paraphrase
    dtype: string
  - name: lists
    sequence: string
  - name: tags
    sequence: string
  - name: language
    dtype: string
  splits:
  - name: train
    num_bytes: 49230
    num_examples: 603
  download_size: 32213126
  dataset_size: 49230
- config_name: ia
  features:
  - name: paraphrase_set_id
    dtype: string
  - name: sentence_id
    dtype: string
  - name: paraphrase
    dtype: string
  - name: lists
    sequence: string
  - name: tags
    sequence: string
  - name: language
    dtype: string
  splits:
  - name: train
    num_bytes: 194035
    num_examples: 2548
  download_size: 32213126
  dataset_size: 194035
- config_name: id
  features:
  - name: paraphrase_set_id
    dtype: string
  - name: sentence_id
    dtype: string
  - name: paraphrase
    dtype: string
  - name: lists
    sequence: string
  - name: tags
    sequence: string
  - name: language
    dtype: string
  splits:
  - name: train
    num_bytes: 124568
    num_examples: 1602
  download_size: 32213126
  dataset_size: 124568
- config_name: ie
  features:
  - name: paraphrase_set_id
    dtype: string
  - name: sentence_id
    dtype: string
  - name: paraphrase
    dtype: string
  - name: lists
    sequence: string
  - name: tags
    sequence: string
  - name: language
    dtype: string
  splits:
  - name: train
    num_bytes: 31956
    num_examples: 488
  download_size: 32213126
  dataset_size: 31956
- config_name: io
  features:
  - name: paraphrase_set_id
    dtype: string
  - name: sentence_id
    dtype: string
  - name: paraphrase
    dtype: string
  - name: lists
    sequence: string
  - name: tags
    sequence: string
  - name: language
    dtype: string
  splits:
  - name: train
    num_bytes: 33892
    num_examples: 480
  download_size: 32213126
  dataset_size: 33892
- config_name: is
  features:
  - name: paraphrase_set_id
    dtype: string
  - name: sentence_id
    dtype: string
  - name: paraphrase
    dtype: string
  - name: lists
    sequence: string
  - name: tags
    sequence: string
  - name: language
    dtype: string
  splits:
  - name: train
    num_bytes: 132062
    num_examples: 1641
  download_size: 32213126
  dataset_size: 132062
- config_name: it
  features:
  - name: paraphrase_set_id
    dtype: string
  - name: sentence_id
    dtype: string
  - name: paraphrase
    dtype: string
  - name: lists
    sequence: string
  - name: tags
    sequence: string
  - name: language
    dtype: string
  splits:
  - name: train
    num_bytes: 15073750
    num_examples: 198919
  download_size: 32213126
  dataset_size: 15073750
- config_name: ja
  features:
  - name: paraphrase_set_id
    dtype: string
  - name: sentence_id
    dtype: string
  - name: paraphrase
    dtype: string
  - name: lists
    sequence: string
  - name: tags
    sequence: string
  - name: language
    dtype: string
  splits:
  - name: train
    num_bytes: 4314423
    num_examples: 44267
  download_size: 32213126
  dataset_size: 4314423
- config_name: jbo
  features:
  - name: paraphrase_set_id
    dtype: string
  - name: sentence_id
    dtype: string
  - name: paraphrase
    dtype: string
  - name: lists
    sequence: string
  - name: tags
    sequence: string
  - name: language
    dtype: string
  splits:
  - name: train
    num_bytes: 201564
    num_examples: 2704
  download_size: 32213126
  dataset_size: 201564
- config_name: kab
  features:
  - name: paraphrase_set_id
    dtype: string
  - name: sentence_id
    dtype: string
  - name: paraphrase
    dtype: string
  - name: lists
    sequence: string
  - name: tags
    sequence: string
  - name: language
    dtype: string
  splits:
  - name: train
    num_bytes: 1211051
    num_examples: 15944
  download_size: 32213126
  dataset_size: 1211051
- config_name: ko
  features:
  - name: paraphrase_set_id
    dtype: string
  - name: sentence_id
    dtype: string
  - name: paraphrase
    dtype: string
  - name: lists
    sequence: string
  - name: tags
    sequence: string
  - name: language
    dtype: string
  splits:
  - name: train
    num_bytes: 40458
    num_examples: 503
  download_size: 32213126
  dataset_size: 40458
- config_name: kw
  features:
  - name: paraphrase_set_id
    dtype: string
  - name: sentence_id
    dtype: string
  - name: paraphrase
    dtype: string
  - name: lists
    sequence: string
  - name: tags
    sequence: string
  - name: language
    dtype: string
  splits:
  - name: train
    num_bytes: 88577
    num_examples: 1328
  download_size: 32213126
  dataset_size: 88577
- config_name: la
  features:
  - name: paraphrase_set_id
    dtype: string
  - name: sentence_id
    dtype: string
  - name: paraphrase
    dtype: string
  - name: lists
    sequence: string
  - name: tags
    sequence: string
  - name: language
    dtype: string
  splits:
  - name: train
    num_bytes: 485749
    num_examples: 6889
  download_size: 32213126
  dataset_size: 485749
- config_name: lfn
  features:
  - name: paraphrase_set_id
    dtype: string
  - name: sentence_id
    dtype: string
  - name: paraphrase
    dtype: string
  - name: lists
    sequence: string
  - name: tags
    sequence: string
  - name: language
    dtype: string
  splits:
  - name: train
    num_bytes: 203383
    num_examples: 2313
  download_size: 32213126
  dataset_size: 203383
- config_name: lt
  features:
  - name: paraphrase_set_id
    dtype: string
  - name: sentence_id
    dtype: string
  - name: paraphrase
    dtype: string
  - name: lists
    sequence: string
  - name: tags
    sequence: string
  - name: language
    dtype: string
  splits:
  - name: train
    num_bytes: 599166
    num_examples: 8042
  download_size: 32213126
  dataset_size: 599166
- config_name: mk
  features:
  - name: paraphrase_set_id
    dtype: string
  - name: sentence_id
    dtype: string
  - name: paraphrase
    dtype: string
  - name: lists
    sequence: string
  - name: tags
    sequence: string
  - name: language
    dtype: string
  splits:
  - name: train
    num_bytes: 1240185
    num_examples: 14678
  download_size: 32213126
  dataset_size: 1240185
- config_name: mr
  features:
  - name: paraphrase_set_id
    dtype: string
  - name: sentence_id
    dtype: string
  - name: paraphrase
    dtype: string
  - name: lists
    sequence: string
  - name: tags
    sequence: string
  - name: language
    dtype: string
  splits:
  - name: train
    num_bytes: 1838921
    num_examples: 16413
  download_size: 32213126
  dataset_size: 1838921
- config_name: nb
  features:
  - name: paraphrase_set_id
    dtype: string
  - name: sentence_id
    dtype: string
  - name: paraphrase
    dtype: string
  - name: lists
    sequence: string
  - name: tags
    sequence: string
  - name: language
    dtype: string
  splits:
  - name: train
    num_bytes: 85371
    num_examples: 1094
  download_size: 32213126
  dataset_size: 85371
- config_name: nds
  features:
  - name: paraphrase_set_id
    dtype: string
  - name: sentence_id
    dtype: string
  - name: paraphrase
    dtype: string
  - name: lists
    sequence: string
  - name: tags
    sequence: string
  - name: language
    dtype: string
  splits:
  - name: train
    num_bytes: 195021
    num_examples: 2633
  download_size: 32213126
  dataset_size: 195021
- config_name: nl
  features:
  - name: paraphrase_set_id
    dtype: string
  - name: sentence_id
    dtype: string
  - name: paraphrase
    dtype: string
  - name: lists
    sequence: string
  - name: tags
    sequence: string
  - name: language
    dtype: string
  splits:
  - name: train
    num_bytes: 1790975
    num_examples: 23561
  download_size: 32213126
  dataset_size: 1790975
- config_name: orv
  features:
  - name: paraphrase_set_id
    dtype: string
  - name: sentence_id
    dtype: string
  - name: paraphrase
    dtype: string
  - name: lists
    sequence: string
  - name: tags
    sequence: string
  - name: language
    dtype: string
  splits:
  - name: train
    num_bytes: 40484
    num_examples: 471
  download_size: 32213126
  dataset_size: 40484
- config_name: ota
  features:
  - name: paraphrase_set_id
    dtype: string
  - name: sentence_id
    dtype: string
  - name: paraphrase
    dtype: string
  - name: lists
    sequence: string
  - name: tags
    sequence: string
  - name: language
    dtype: string
  splits:
  - name: train
    num_bytes: 44996
    num_examples: 486
  download_size: 32213126
  dataset_size: 44996
- config_name: pes
  features:
  - name: paraphrase_set_id
    dtype: string
  - name: sentence_id
    dtype: string
  - name: paraphrase
    dtype: string
  - name: lists
    sequence: string
  - name: tags
    sequence: string
  - name: language
    dtype: string
  splits:
  - name: train
    num_bytes: 433406
    num_examples: 4285
  download_size: 32213126
  dataset_size: 433406
- config_name: pl
  features:
  - name: paraphrase_set_id
    dtype: string
  - name: sentence_id
    dtype: string
  - name: paraphrase
    dtype: string
  - name: lists
    sequence: string
  - name: tags
    sequence: string
  - name: language
    dtype: string
  splits:
  - name: train
    num_bytes: 1722188
    num_examples: 22391
  download_size: 32213126
  dataset_size: 1722188
- config_name: pt
  features:
  - name: paraphrase_set_id
    dtype: string
  - name: sentence_id
    dtype: string
  - name: paraphrase
    dtype: string
  - name: lists
    sequence: string
  - name: tags
    sequence: string
  - name: language
    dtype: string
  splits:
  - name: train
    num_bytes: 6141178
    num_examples: 78430
  download_size: 32213126
  dataset_size: 6141178
- config_name: rn
  features:
  - name: paraphrase_set_id
    dtype: string
  - name: sentence_id
    dtype: string
  - name: paraphrase
    dtype: string
  - name: lists
    sequence: string
  - name: tags
    sequence: string
  - name: language
    dtype: string
  splits:
  - name: train
    num_bytes: 47387
    num_examples: 648
  download_size: 32213126
  dataset_size: 47387
- config_name: ro
  features:
  - name: paraphrase_set_id
    dtype: string
  - name: sentence_id
    dtype: string
  - name: paraphrase
    dtype: string
  - name: lists
    sequence: string
  - name: tags
    sequence: string
  - name: language
    dtype: string
  splits:
  - name: train
    num_bytes: 162955
    num_examples: 2092
  download_size: 32213126
  dataset_size: 162955
- config_name: ru
  features:
  - name: paraphrase_set_id
    dtype: string
  - name: sentence_id
    dtype: string
  - name: paraphrase
    dtype: string
  - name: lists
    sequence: string
  - name: tags
    sequence: string
  - name: language
    dtype: string
  splits:
  - name: train
    num_bytes: 24540667
    num_examples: 251263
  download_size: 32213126
  dataset_size: 24540667
- config_name: sl
  features:
  - name: paraphrase_set_id
    dtype: string
  - name: sentence_id
    dtype: string
  - name: paraphrase
    dtype: string
  - name: lists
    sequence: string
  - name: tags
    sequence: string
  - name: language
    dtype: string
  splits:
  - name: train
    num_bytes: 49610
    num_examples: 706
  download_size: 32213126
  dataset_size: 49610
- config_name: sr
  features:
  - name: paraphrase_set_id
    dtype: string
  - name: sentence_id
    dtype: string
  - name: paraphrase
    dtype: string
  - name: lists
    sequence: string
  - name: tags
    sequence: string
  - name: language
    dtype: string
  splits:
  - name: train
    num_bytes: 667308
    num_examples: 8175
  download_size: 32213126
  dataset_size: 667308
- config_name: sv
  features:
  - name: paraphrase_set_id
    dtype: string
  - name: sentence_id
    dtype: string
  - name: paraphrase
    dtype: string
  - name: lists
    sequence: string
  - name: tags
    sequence: string
  - name: language
    dtype: string
  splits:
  - name: train
    num_bytes: 509884
    num_examples: 7005
  download_size: 32213126
  dataset_size: 509884
- config_name: tk
  features:
  - name: paraphrase_set_id
    dtype: string
  - name: sentence_id
    dtype: string
  - name: paraphrase
    dtype: string
  - name: lists
    sequence: string
  - name: tags
    sequence: string
  - name: language
    dtype: string
  splits:
  - name: train
    num_bytes: 95047
    num_examples: 1165
  download_size: 32213126
  dataset_size: 95047
- config_name: tl
  features:
  - name: paraphrase_set_id
    dtype: string
  - name: sentence_id
    dtype: string
  - name: paraphrase
    dtype: string
  - name: lists
    sequence: string
  - name: tags
    sequence: string
  - name: language
    dtype: string
  splits:
  - name: train
    num_bytes: 76059
    num_examples: 1017
  download_size: 32213126
  dataset_size: 76059
- config_name: tlh
  features:
  - name: paraphrase_set_id
    dtype: string
  - name: sentence_id
    dtype: string
  - name: paraphrase
    dtype: string
  - name: lists
    sequence: string
  - name: tags
    sequence: string
  - name: language
    dtype: string
  splits:
  - name: train
    num_bytes: 185309
    num_examples: 2804
  download_size: 32213126
  dataset_size: 185309
- config_name: toki
  features:
  - name: paraphrase_set_id
    dtype: string
  - name: sentence_id
    dtype: string
  - name: paraphrase
    dtype: string
  - name: lists
    sequence: string
  - name: tags
    sequence: string
  - name: language
    dtype: string
  splits:
  - name: train
    num_bytes: 310864
    num_examples: 3738
  download_size: 32213126
  dataset_size: 310864
- config_name: tr
  features:
  - name: paraphrase_set_id
    dtype: string
  - name: sentence_id
    dtype: string
  - name: paraphrase
    dtype: string
  - name: lists
    sequence: string
  - name: tags
    sequence: string
  - name: language
    dtype: string
  splits:
  - name: train
    num_bytes: 11271158
    num_examples: 142088
  download_size: 32213126
  dataset_size: 11271158
- config_name: tt
  features:
  - name: paraphrase_set_id
    dtype: string
  - name: sentence_id
    dtype: string
  - name: paraphrase
    dtype: string
  - name: lists
    sequence: string
  - name: tags
    sequence: string
  - name: language
    dtype: string
  splits:
  - name: train
    num_bytes: 277269
    num_examples: 2398
  download_size: 32213126
  dataset_size: 277269
- config_name: ug
  features:
  - name: paraphrase_set_id
    dtype: string
  - name: sentence_id
    dtype: string
  - name: paraphrase
    dtype: string
  - name: lists
    sequence: string
  - name: tags
    sequence: string
  - name: language
    dtype: string
  splits:
  - name: train
    num_bytes: 118474
    num_examples: 1183
  download_size: 32213126
  dataset_size: 118474
- config_name: uk
  features:
  - name: paraphrase_set_id
    dtype: string
  - name: sentence_id
    dtype: string
  - name: paraphrase
    dtype: string
  - name: lists
    sequence: string
  - name: tags
    sequence: string
  - name: language
    dtype: string
  splits:
  - name: train
    num_bytes: 4885677
    num_examples: 54431
  download_size: 32213126
  dataset_size: 4885677
- config_name: ur
  features:
  - name: paraphrase_set_id
    dtype: string
  - name: sentence_id
    dtype: string
  - name: paraphrase
    dtype: string
  - name: lists
    sequence: string
  - name: tags
    sequence: string
  - name: language
    dtype: string
  splits:
  - name: train
    num_bytes: 24075
    num_examples: 252
  download_size: 32213126
  dataset_size: 24075
- config_name: vi
  features:
  - name: paraphrase_set_id
    dtype: string
  - name: sentence_id
    dtype: string
  - name: paraphrase
    dtype: string
  - name: lists
    sequence: string
  - name: tags
    sequence: string
  - name: language
    dtype: string
  splits:
  - name: train
    num_bytes: 84773
    num_examples: 962
  download_size: 32213126
  dataset_size: 84773
- config_name: vo
  features:
  - name: paraphrase_set_id
    dtype: string
  - name: sentence_id
    dtype: string
  - name: paraphrase
    dtype: string
  - name: lists
    sequence: string
  - name: tags
    sequence: string
  - name: language
    dtype: string
  splits:
  - name: train
    num_bytes: 22164
    num_examples: 328
  download_size: 32213126
  dataset_size: 22164
- config_name: war
  features:
  - name: paraphrase_set_id
    dtype: string
  - name: sentence_id
    dtype: string
  - name: paraphrase
    dtype: string
  - name: lists
    sequence: string
  - name: tags
    sequence: string
  - name: language
    dtype: string
  splits:
  - name: train
    num_bytes: 25759
    num_examples: 327
  download_size: 32213126
  dataset_size: 25759
- config_name: wuu
  features:
  - name: paraphrase_set_id
    dtype: string
  - name: sentence_id
    dtype: string
  - name: paraphrase
    dtype: string
  - name: lists
    sequence: string
  - name: tags
    sequence: string
  - name: language
    dtype: string
  splits:
  - name: train
    num_bytes: 31640
    num_examples: 408
  download_size: 32213126
  dataset_size: 31640
- config_name: yue
  features:
  - name: paraphrase_set_id
    dtype: string
  - name: sentence_id
    dtype: string
  - name: paraphrase
    dtype: string
  - name: lists
    sequence: string
  - name: tags
    sequence: string
  - name: language
    dtype: string
  splits:
  - name: train
    num_bytes: 42766
    num_examples: 561
  download_size: 32213126
  dataset_size: 42766
---

# Dataset Card for TaPaCo Corpus

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

- **Homepage:** [TaPaCo: A Corpus of Sentential Paraphrases for 73 Languages](https://zenodo.org/record/3707949#.X9Dh0cYza3I)
- **Paper:** [TaPaCo: A Corpus of Sentential Paraphrases for 73 Languages](https://www.aclweb.org/anthology/2020.lrec-1.848.pdf)
- **Point of Contact:** [Yves Scherrer](https://blogs.helsinki.fi/yvesscherrer/)

### Dataset Summary
A freely available paraphrase corpus for 73 languages extracted from the Tatoeba database. 
Tatoeba is a crowdsourcing project mainly geared towards language learners. Its aim is to provide example sentences 
and translations for particular linguistic constructions and words. The paraphrase corpus is created by populating a 
graph with Tatoeba sentences and equivalence links between sentences “meaning the same thing”. This graph is then 
traversed to extract sets of paraphrases. Several language-independent filters and pruning steps are applied to 
remove uninteresting sentences. A manual evaluation performed on three languages shows that between half and three 
quarters of inferred paraphrases are correct and that most remaining ones are either correct but trivial, 
or near-paraphrases that neutralize a morphological distinction. The corpus contains a total of 1.9 million 
sentences, with 200 – 250 000 sentences per language. It covers a range of languages for which, to our knowledge,
no other paraphrase dataset exists.

### Supported Tasks and Leaderboards
Paraphrase detection and generation have become popular tasks in NLP
and are increasingly integrated into a wide variety of common downstream tasks such as machine translation
, information retrieval, question answering, and semantic parsing. Most of the existing datasets
 cover only a single language – in most cases English – or a small number of languages. Furthermore, some paraphrase
  datasets focus on lexical and phrasal rather than sentential paraphrases, while others are created (semi
  -)automatically using machine translation.

The number of sentences per language ranges from 200 to 250 000, which makes the dataset
more suitable for fine-tuning and evaluation purposes than
for training. It is well-suited for multi-reference evaluation
of paraphrase generation models, as there is generally not a
single correct way of paraphrasing a given input sentence.

### Languages

The dataset contains paraphrases in Afrikaans, Arabic, Azerbaijani, Belarusian, Berber languages, Bulgarian, Bengali
, Breton, Catalan; Valencian, Chavacano, Mandarin, Czech, Danish, German, Greek, Modern (1453-), English, Esperanto
, Spanish; Castilian, Estonian, Basque, Finnish, French, Galician, Gronings, Hebrew, Hindi, Croatian, Hungarian
, Armenian, Interlingua (International Auxiliary Language Association), Indonesian, Interlingue; Occidental, Ido
, Icelandic, Italian, Japanese, Lojban, Kabyle, Korean, Cornish, Latin, Lingua Franca Nova\t, Lithuanian, Macedonian
, Marathi, Bokmål, Norwegian; Norwegian Bokmål, Low German; Low Saxon; German, Low; Saxon, Low, Dutch; Flemish, ]Old
 Russian, Turkish, Ottoman (1500-1928), Iranian Persian, Polish, Portuguese, Rundi, Romanian; Moldavian; Moldovan, 
 Russian, Slovenian, Serbian, Swedish, Turkmen, Tagalog, Klingon; tlhIngan-Hol, Toki Pona, Turkish, Tatar, 
 Uighur; Uyghur, Ukrainian, Urdu, Vietnamese, Volapük, Waray, Wu Chinese and Yue Chinese

## Dataset Structure

### Data Instances
Each data instance corresponds to a paraphrase, e.g.:
```
{ 
    'paraphrase_set_id': '1483',  
    'sentence_id': '5778896',
    'paraphrase': 'Ɣremt adlis-a.', 
    'lists': ['7546'], 
    'tags': [''],
    'language': 'ber'
}
```

### Data Fields
Each dialogue instance has the following fields:
- `paraphrase_set_id`:  a running number that groups together all sentences that are considered paraphrases of each
 other
- `sentence_id`: OPUS sentence id
- `paraphrase`: Sentential paraphrase in a given language for a given paraphrase_set_id
- `lists`: Contributors can add sentences to list in order to specify the original source of the data
- `tags`: Indicates morphological or phonological properties of the sentence when available
- `language`: Language identifier, one of the 73 languages that belong to this dataset.

### Data Splits

The dataset is having a single `train` split, contains a total of 1.9 million sentences, with 200 – 250 000
 sentences per language

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

Creative Commons Attribution 2.0 Generic

### Citation Information

```
@dataset{scherrer_yves_2020_3707949,
  author       = {Scherrer, Yves},
  title        = {{TaPaCo: A Corpus of Sentential Paraphrases for 73 Languages}},
  month        = mar,
  year         = 2020,
  publisher    = {Zenodo},
  version      = {1.0},
  doi          = {10.5281/zenodo.3707949},
  url          = {https://doi.org/10.5281/zenodo.3707949}
}
```

### Contributions

Thanks to [@pacman100](https://github.com/pacman100) for adding this dataset.