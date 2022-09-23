---
annotations_creators:
- machine-generated
language_creators:
- crowdsourced
language:
- ace
- af
- als
- am
- an
- ang
- ar
- arc
- arz
- as
- ast
- ay
- az
- ba
- bar
- be
- bg
- bh
- bn
- bo
- br
- bs
- ca
- cbk
- cdo
- ce
- ceb
- ckb
- co
- crh
- cs
- csb
- cv
- cy
- da
- de
- diq
- dv
- el
- eml
- en
- eo
- es
- et
- eu
- ext
- fa
- fi
- fo
- fr
- frr
- fur
- fy
- ga
- gan
- gd
- gl
- gn
- gu
- hak
- he
- hi
- hr
- hsb
- hu
- hy
- ia
- id
- ig
- ilo
- io
- is
- it
- ja
- jbo
- jv
- ka
- kk
- km
- kn
- ko
- ksh
- ku
- ky
- la
- lb
- li
- lij
- lmo
- ln
- lt
- lv
- lzh
- mg
- mhr
- mi
- min
- mk
- ml
- mn
- mr
- ms
- mt
- mwl
- my
- mzn
- nan
- nap
- nds
- ne
- nl
- nn
- 'no'
- nov
- oc
- or
- os
- pa
- pdc
- pl
- pms
- pnb
- ps
- pt
- qu
- rm
- ro
- ru
- rw
- sa
- sah
- scn
- sco
- sd
- sgs
- sh
- si
- sk
- sl
- so
- sq
- sr
- su
- sv
- sw
- szl
- ta
- te
- tg
- th
- tk
- tl
- tr
- tt
- ug
- uk
- ur
- uz
- vec
- vep
- vi
- vls
- vo
- vro
- wa
- war
- wuu
- xmf
- yi
- yo
- yue
- zea
- zh
language_bcp47:
- be-tarask
- en-basiceng
- jv-x-bms
license:
- unknown
multilinguality:
- multilingual
size_categories:
- n<1K
source_datasets:
- original
task_categories:
- token-classification
task_ids:
- named-entity-recognition
paperswithcode_id: wikiann-1
pretty_name: WikiANN
configs:
- 'no'
- ace
- af
- als
- am
- an
- ang
- ar
- arc
- arz
- as
- ast
- ay
- az
- ba
- bar
- be
- bg
- bh
- bn
- bo
- br
- bs
- ca
- cdo
- ce
- ceb
- ckb
- co
- crh
- cs
- csb
- cv
- cy
- da
- de
- diq
- dv
- el
- en
- eo
- es
- et
- eu
- ext
- fa
- fi
- fo
- fr
- frr
- fur
- fy
- ga
- gan
- gd
- gl
- gn
- gu
- hak
- he
- hi
- hr
- hsb
- hu
- hy
- ia
- id
- ig
- ilo
- io
- is
- it
- ja
- jbo
- jv
- ka
- kk
- km
- kn
- ko
- ksh
- ku
- ky
- la
- lb
- li
- lij
- lmo
- ln
- lt
- lv
- mg
- mhr
- mi
- min
- mk
- ml
- mn
- mr
- ms
- mt
- mwl
- my
- mzn
- nap
- nds
- ne
- nl
- nn
- nov
- oc
- or
- os
- other-bat-smg
- other-be-x-old
- other-cbk-zam
- other-eml
- other-fiu-vro
- other-map-bms
- other-simple
- other-zh-classical
- other-zh-min-nan
- other-zh-yue
- pa
- pdc
- pl
- pms
- pnb
- ps
- pt
- qu
- rm
- ro
- ru
- rw
- sa
- sah
- scn
- sco
- sd
- sh
- si
- sk
- sl
- so
- sq
- sr
- su
- sv
- sw
- szl
- ta
- te
- tg
- th
- tk
- tl
- tr
- tt
- ug
- uk
- ur
- uz
- vec
- vep
- vi
- vls
- vo
- wa
- war
- wuu
- xmf
- yi
- yo
- zea
- zh
dataset_info:
- config_name: ace
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-PER
          2: I-PER
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
  - name: langs
    sequence: string
  - name: spans
    sequence: string
  splits:
  - name: test
    num_bytes: 25752
    num_examples: 100
  - name: train
    num_bytes: 23231
    num_examples: 100
  - name: validation
    num_bytes: 22453
    num_examples: 100
  download_size: 234008884
  dataset_size: 71436
- config_name: af
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-PER
          2: I-PER
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
  - name: langs
    sequence: string
  - name: spans
    sequence: string
  splits:
  - name: test
    num_bytes: 295849
    num_examples: 1000
  - name: train
    num_bytes: 1521604
    num_examples: 5000
  - name: validation
    num_bytes: 299137
    num_examples: 1000
  download_size: 234008884
  dataset_size: 2116590
- config_name: als
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-PER
          2: I-PER
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
  - name: langs
    sequence: string
  - name: spans
    sequence: string
  splits:
  - name: test
    num_bytes: 36345
    num_examples: 100
  - name: train
    num_bytes: 34968
    num_examples: 100
  - name: validation
    num_bytes: 34318
    num_examples: 100
  download_size: 234008884
  dataset_size: 105631
- config_name: am
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-PER
          2: I-PER
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
  - name: langs
    sequence: string
  - name: spans
    sequence: string
  splits:
  - name: test
    num_bytes: 23811
    num_examples: 100
  - name: train
    num_bytes: 22214
    num_examples: 100
  - name: validation
    num_bytes: 21429
    num_examples: 100
  download_size: 234008884
  dataset_size: 67454
- config_name: an
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-PER
          2: I-PER
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
  - name: langs
    sequence: string
  - name: spans
    sequence: string
  splits:
  - name: test
    num_bytes: 174992
    num_examples: 1000
  - name: train
    num_bytes: 180967
    num_examples: 1000
  - name: validation
    num_bytes: 180609
    num_examples: 1000
  download_size: 234008884
  dataset_size: 536568
- config_name: ang
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-PER
          2: I-PER
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
  - name: langs
    sequence: string
  - name: spans
    sequence: string
  splits:
  - name: test
    num_bytes: 24523
    num_examples: 100
  - name: train
    num_bytes: 23296
    num_examples: 100
  - name: validation
    num_bytes: 21925
    num_examples: 100
  download_size: 234008884
  dataset_size: 69744
- config_name: ar
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-PER
          2: I-PER
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
  - name: langs
    sequence: string
  - name: spans
    sequence: string
  splits:
  - name: test
    num_bytes: 2334664
    num_examples: 10000
  - name: train
    num_bytes: 4671669
    num_examples: 20000
  - name: validation
    num_bytes: 2325688
    num_examples: 10000
  download_size: 234008884
  dataset_size: 9332021
- config_name: arc
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-PER
          2: I-PER
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
  - name: langs
    sequence: string
  - name: spans
    sequence: string
  splits:
  - name: test
    num_bytes: 16641
    num_examples: 100
  - name: train
    num_bytes: 18536
    num_examples: 100
  - name: validation
    num_bytes: 15726
    num_examples: 100
  download_size: 234008884
  dataset_size: 50903
- config_name: arz
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-PER
          2: I-PER
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
  - name: langs
    sequence: string
  - name: spans
    sequence: string
  splits:
  - name: test
    num_bytes: 25663
    num_examples: 100
  - name: train
    num_bytes: 26375
    num_examples: 100
  - name: validation
    num_bytes: 26609
    num_examples: 100
  download_size: 234008884
  dataset_size: 78647
- config_name: as
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-PER
          2: I-PER
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
  - name: langs
    sequence: string
  - name: spans
    sequence: string
  splits:
  - name: test
    num_bytes: 23350
    num_examples: 100
  - name: train
    num_bytes: 24984
    num_examples: 100
  - name: validation
    num_bytes: 25736
    num_examples: 100
  download_size: 234008884
  dataset_size: 74070
- config_name: ast
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-PER
          2: I-PER
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
  - name: langs
    sequence: string
  - name: spans
    sequence: string
  splits:
  - name: test
    num_bytes: 220874
    num_examples: 1000
  - name: train
    num_bytes: 228238
    num_examples: 1000
  - name: validation
    num_bytes: 217477
    num_examples: 1000
  download_size: 234008884
  dataset_size: 666589
- config_name: ay
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-PER
          2: I-PER
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
  - name: langs
    sequence: string
  - name: spans
    sequence: string
  splits:
  - name: test
    num_bytes: 13379
    num_examples: 100
  - name: train
    num_bytes: 12596
    num_examples: 100
  - name: validation
    num_bytes: 11684
    num_examples: 100
  download_size: 234008884
  dataset_size: 37659
- config_name: az
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-PER
          2: I-PER
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
  - name: langs
    sequence: string
  - name: spans
    sequence: string
  splits:
  - name: test
    num_bytes: 267935
    num_examples: 1000
  - name: train
    num_bytes: 2645552
    num_examples: 10000
  - name: validation
    num_bytes: 272066
    num_examples: 1000
  download_size: 234008884
  dataset_size: 3185553
- config_name: ba
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-PER
          2: I-PER
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
  - name: langs
    sequence: string
  - name: spans
    sequence: string
  splits:
  - name: test
    num_bytes: 30502
    num_examples: 100
  - name: train
    num_bytes: 31123
    num_examples: 100
  - name: validation
    num_bytes: 29262
    num_examples: 100
  download_size: 234008884
  dataset_size: 90887
- config_name: bar
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-PER
          2: I-PER
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
  - name: langs
    sequence: string
  - name: spans
    sequence: string
  splits:
  - name: test
    num_bytes: 17839
    num_examples: 100
  - name: train
    num_bytes: 16796
    num_examples: 100
  - name: validation
    num_bytes: 17374
    num_examples: 100
  download_size: 234008884
  dataset_size: 52009
- config_name: bat-smg
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-PER
          2: I-PER
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
  - name: langs
    sequence: string
  - name: spans
    sequence: string
  splits:
  - name: test
    num_bytes: 26093
    num_examples: 100
  - name: train
    num_bytes: 24677
    num_examples: 100
  - name: validation
    num_bytes: 26496
    num_examples: 100
  download_size: 234008884
  dataset_size: 77266
- config_name: be
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-PER
          2: I-PER
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
  - name: langs
    sequence: string
  - name: spans
    sequence: string
  splits:
  - name: test
    num_bytes: 266104
    num_examples: 1000
  - name: train
    num_bytes: 3983322
    num_examples: 15000
  - name: validation
    num_bytes: 262042
    num_examples: 1000
  download_size: 234008884
  dataset_size: 4511468
- config_name: be-x-old
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-PER
          2: I-PER
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
  - name: langs
    sequence: string
  - name: spans
    sequence: string
  splits:
  - name: test
    num_bytes: 337599
    num_examples: 1000
  - name: train
    num_bytes: 1704256
    num_examples: 5000
  - name: validation
    num_bytes: 342654
    num_examples: 1000
  download_size: 234008884
  dataset_size: 2384509
- config_name: bg
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-PER
          2: I-PER
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
  - name: langs
    sequence: string
  - name: spans
    sequence: string
  splits:
  - name: test
    num_bytes: 2830213
    num_examples: 10000
  - name: train
    num_bytes: 5665063
    num_examples: 20000
  - name: validation
    num_bytes: 2840907
    num_examples: 10000
  download_size: 234008884
  dataset_size: 11336183
- config_name: bh
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-PER
          2: I-PER
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
  - name: langs
    sequence: string
  - name: spans
    sequence: string
  splits:
  - name: test
    num_bytes: 30692
    num_examples: 100
  - name: train
    num_bytes: 36374
    num_examples: 100
  - name: validation
    num_bytes: 33682
    num_examples: 100
  download_size: 234008884
  dataset_size: 100748
- config_name: bn
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-PER
          2: I-PER
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
  - name: langs
    sequence: string
  - name: spans
    sequence: string
  splits:
  - name: test
    num_bytes: 237218
    num_examples: 1000
  - name: train
    num_bytes: 2351591
    num_examples: 10000
  - name: validation
    num_bytes: 238446
    num_examples: 1000
  download_size: 234008884
  dataset_size: 2827255
- config_name: bo
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-PER
          2: I-PER
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
  - name: langs
    sequence: string
  - name: spans
    sequence: string
  splits:
  - name: test
    num_bytes: 15437
    num_examples: 100
  - name: train
    num_bytes: 14085
    num_examples: 100
  - name: validation
    num_bytes: 22688
    num_examples: 100
  download_size: 234008884
  dataset_size: 52210
- config_name: br
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-PER
          2: I-PER
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
  - name: langs
    sequence: string
  - name: spans
    sequence: string
  splits:
  - name: test
    num_bytes: 222083
    num_examples: 1000
  - name: train
    num_bytes: 221495
    num_examples: 1000
  - name: validation
    num_bytes: 206839
    num_examples: 1000
  download_size: 234008884
  dataset_size: 650417
- config_name: bs
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-PER
          2: I-PER
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
  - name: langs
    sequence: string
  - name: spans
    sequence: string
  splits:
  - name: test
    num_bytes: 247331
    num_examples: 1000
  - name: train
    num_bytes: 3669346
    num_examples: 15000
  - name: validation
    num_bytes: 246378
    num_examples: 1000
  download_size: 234008884
  dataset_size: 4163055
- config_name: ca
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-PER
          2: I-PER
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
  - name: langs
    sequence: string
  - name: spans
    sequence: string
  splits:
  - name: test
    num_bytes: 1847746
    num_examples: 10000
  - name: train
    num_bytes: 3689342
    num_examples: 20000
  - name: validation
    num_bytes: 1836319
    num_examples: 10000
  download_size: 234008884
  dataset_size: 7373407
- config_name: cbk-zam
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-PER
          2: I-PER
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
  - name: langs
    sequence: string
  - name: spans
    sequence: string
  splits:
  - name: test
    num_bytes: 47277
    num_examples: 100
  - name: train
    num_bytes: 52545
    num_examples: 100
  - name: validation
    num_bytes: 47060
    num_examples: 100
  download_size: 234008884
  dataset_size: 146882
- config_name: cdo
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-PER
          2: I-PER
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
  - name: langs
    sequence: string
  - name: spans
    sequence: string
  splits:
  - name: test
    num_bytes: 34319
    num_examples: 100
  - name: train
    num_bytes: 36204
    num_examples: 100
  - name: validation
    num_bytes: 37479
    num_examples: 100
  download_size: 234008884
  dataset_size: 108002
- config_name: ce
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-PER
          2: I-PER
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
  - name: langs
    sequence: string
  - name: spans
    sequence: string
  splits:
  - name: test
    num_bytes: 38640
    num_examples: 100
  - name: train
    num_bytes: 38284
    num_examples: 100
  - name: validation
    num_bytes: 40303
    num_examples: 100
  download_size: 234008884
  dataset_size: 117227
- config_name: ceb
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-PER
          2: I-PER
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
  - name: langs
    sequence: string
  - name: spans
    sequence: string
  splits:
  - name: test
    num_bytes: 23950
    num_examples: 100
  - name: train
    num_bytes: 21365
    num_examples: 100
  - name: validation
    num_bytes: 22789
    num_examples: 100
  download_size: 234008884
  dataset_size: 68104
- config_name: ckb
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-PER
          2: I-PER
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
  - name: langs
    sequence: string
  - name: spans
    sequence: string
  splits:
  - name: test
    num_bytes: 211988
    num_examples: 1000
  - name: train
    num_bytes: 217066
    num_examples: 1000
  - name: validation
    num_bytes: 214231
    num_examples: 1000
  download_size: 234008884
  dataset_size: 643285
- config_name: co
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-PER
          2: I-PER
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
  - name: langs
    sequence: string
  - name: spans
    sequence: string
  splits:
  - name: test
    num_bytes: 15880
    num_examples: 100
  - name: train
    num_bytes: 18032
    num_examples: 100
  - name: validation
    num_bytes: 15968
    num_examples: 100
  download_size: 234008884
  dataset_size: 49880
- config_name: crh
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-PER
          2: I-PER
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
  - name: langs
    sequence: string
  - name: spans
    sequence: string
  splits:
  - name: test
    num_bytes: 23879
    num_examples: 100
  - name: train
    num_bytes: 23336
    num_examples: 100
  - name: validation
    num_bytes: 20230
    num_examples: 100
  download_size: 234008884
  dataset_size: 67445
- config_name: cs
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-PER
          2: I-PER
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
  - name: langs
    sequence: string
  - name: spans
    sequence: string
  splits:
  - name: test
    num_bytes: 2458155
    num_examples: 10000
  - name: train
    num_bytes: 4944758
    num_examples: 20000
  - name: validation
    num_bytes: 2456654
    num_examples: 10000
  download_size: 234008884
  dataset_size: 9859567
- config_name: csb
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-PER
          2: I-PER
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
  - name: langs
    sequence: string
  - name: spans
    sequence: string
  splits:
  - name: test
    num_bytes: 27840
    num_examples: 100
  - name: train
    num_bytes: 31640
    num_examples: 100
  - name: validation
    num_bytes: 28841
    num_examples: 100
  download_size: 234008884
  dataset_size: 88321
- config_name: cv
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-PER
          2: I-PER
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
  - name: langs
    sequence: string
  - name: spans
    sequence: string
  splits:
  - name: test
    num_bytes: 26403
    num_examples: 100
  - name: train
    num_bytes: 26956
    num_examples: 100
  - name: validation
    num_bytes: 24787
    num_examples: 100
  download_size: 234008884
  dataset_size: 78146
- config_name: cy
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-PER
          2: I-PER
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
  - name: langs
    sequence: string
  - name: spans
    sequence: string
  splits:
  - name: test
    num_bytes: 233869
    num_examples: 1000
  - name: train
    num_bytes: 2337116
    num_examples: 10000
  - name: validation
    num_bytes: 228586
    num_examples: 1000
  download_size: 234008884
  dataset_size: 2799571
- config_name: da
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-PER
          2: I-PER
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
  - name: langs
    sequence: string
  - name: spans
    sequence: string
  splits:
  - name: test
    num_bytes: 2432324
    num_examples: 10000
  - name: train
    num_bytes: 4882222
    num_examples: 20000
  - name: validation
    num_bytes: 2422976
    num_examples: 10000
  download_size: 234008884
  dataset_size: 9737522
- config_name: de
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-PER
          2: I-PER
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
  - name: langs
    sequence: string
  - name: spans
    sequence: string
  splits:
  - name: test
    num_bytes: 2750996
    num_examples: 10000
  - name: train
    num_bytes: 5510641
    num_examples: 20000
  - name: validation
    num_bytes: 2754550
    num_examples: 10000
  download_size: 234008884
  dataset_size: 11016187
- config_name: diq
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-PER
          2: I-PER
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
  - name: langs
    sequence: string
  - name: spans
    sequence: string
  splits:
  - name: test
    num_bytes: 22476
    num_examples: 100
  - name: train
    num_bytes: 24131
    num_examples: 100
  - name: validation
    num_bytes: 24147
    num_examples: 100
  download_size: 234008884
  dataset_size: 70754
- config_name: dv
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-PER
          2: I-PER
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
  - name: langs
    sequence: string
  - name: spans
    sequence: string
  splits:
  - name: test
    num_bytes: 27279
    num_examples: 100
  - name: train
    num_bytes: 31033
    num_examples: 100
  - name: validation
    num_bytes: 30322
    num_examples: 100
  download_size: 234008884
  dataset_size: 88634
- config_name: el
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-PER
          2: I-PER
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
  - name: langs
    sequence: string
  - name: spans
    sequence: string
  splits:
  - name: test
    num_bytes: 3034329
    num_examples: 10000
  - name: train
    num_bytes: 6046638
    num_examples: 20000
  - name: validation
    num_bytes: 3027962
    num_examples: 10000
  download_size: 234008884
  dataset_size: 12108929
- config_name: eml
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-PER
          2: I-PER
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
  - name: langs
    sequence: string
  - name: spans
    sequence: string
  splits:
  - name: test
    num_bytes: 35880
    num_examples: 100
  - name: train
    num_bytes: 30792
    num_examples: 100
  - name: validation
    num_bytes: 30050
    num_examples: 100
  download_size: 234008884
  dataset_size: 96722
- config_name: en
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-PER
          2: I-PER
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
  - name: langs
    sequence: string
  - name: spans
    sequence: string
  splits:
  - name: test
    num_bytes: 2330245
    num_examples: 10000
  - name: train
    num_bytes: 4649601
    num_examples: 20000
  - name: validation
    num_bytes: 2336353
    num_examples: 10000
  download_size: 234008884
  dataset_size: 9316199
- config_name: eo
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-PER
          2: I-PER
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
  - name: langs
    sequence: string
  - name: spans
    sequence: string
  splits:
  - name: test
    num_bytes: 1961486
    num_examples: 10000
  - name: train
    num_bytes: 2952610
    num_examples: 15000
  - name: validation
    num_bytes: 1968690
    num_examples: 10000
  download_size: 234008884
  dataset_size: 6882786
- config_name: es
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-PER
          2: I-PER
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
  - name: langs
    sequence: string
  - name: spans
    sequence: string
  splits:
  - name: test
    num_bytes: 1986664
    num_examples: 10000
  - name: train
    num_bytes: 3972292
    num_examples: 20000
  - name: validation
    num_bytes: 1976935
    num_examples: 10000
  download_size: 234008884
  dataset_size: 7935891
- config_name: et
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-PER
          2: I-PER
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
  - name: langs
    sequence: string
  - name: spans
    sequence: string
  splits:
  - name: test
    num_bytes: 2392424
    num_examples: 10000
  - name: train
    num_bytes: 3579264
    num_examples: 15000
  - name: validation
    num_bytes: 2403361
    num_examples: 10000
  download_size: 234008884
  dataset_size: 8375049
- config_name: eu
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-PER
          2: I-PER
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
  - name: langs
    sequence: string
  - name: spans
    sequence: string
  splits:
  - name: test
    num_bytes: 2628951
    num_examples: 10000
  - name: train
    num_bytes: 2672353
    num_examples: 10000
  - name: validation
    num_bytes: 2677036
    num_examples: 10000
  download_size: 234008884
  dataset_size: 7978340
- config_name: ext
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-PER
          2: I-PER
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
  - name: langs
    sequence: string
  - name: spans
    sequence: string
  splits:
  - name: test
    num_bytes: 29483
    num_examples: 100
  - name: train
    num_bytes: 23110
    num_examples: 100
  - name: validation
    num_bytes: 30821
    num_examples: 100
  download_size: 234008884
  dataset_size: 83414
- config_name: fa
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-PER
          2: I-PER
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
  - name: langs
    sequence: string
  - name: spans
    sequence: string
  splits:
  - name: test
    num_bytes: 2314687
    num_examples: 10000
  - name: train
    num_bytes: 4618098
    num_examples: 20000
  - name: validation
    num_bytes: 2328640
    num_examples: 10000
  download_size: 234008884
  dataset_size: 9261425
- config_name: fi
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-PER
          2: I-PER
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
  - name: langs
    sequence: string
  - name: spans
    sequence: string
  splits:
  - name: test
    num_bytes: 2505161
    num_examples: 10000
  - name: train
    num_bytes: 5020655
    num_examples: 20000
  - name: validation
    num_bytes: 2500586
    num_examples: 10000
  download_size: 234008884
  dataset_size: 10026402
- config_name: fiu-vro
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-PER
          2: I-PER
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
  - name: langs
    sequence: string
  - name: spans
    sequence: string
  splits:
  - name: test
    num_bytes: 27728
    num_examples: 100
  - name: train
    num_bytes: 28689
    num_examples: 100
  - name: validation
    num_bytes: 27672
    num_examples: 100
  download_size: 234008884
  dataset_size: 84089
- config_name: fo
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-PER
          2: I-PER
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
  - name: langs
    sequence: string
  - name: spans
    sequence: string
  splits:
  - name: test
    num_bytes: 23531
    num_examples: 100
  - name: train
    num_bytes: 26178
    num_examples: 100
  - name: validation
    num_bytes: 26094
    num_examples: 100
  download_size: 234008884
  dataset_size: 75803
- config_name: fr
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-PER
          2: I-PER
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
  - name: langs
    sequence: string
  - name: spans
    sequence: string
  splits:
  - name: test
    num_bytes: 2073593
    num_examples: 10000
  - name: train
    num_bytes: 4123995
    num_examples: 20000
  - name: validation
    num_bytes: 2058004
    num_examples: 10000
  download_size: 234008884
  dataset_size: 8255592
- config_name: frr
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-PER
          2: I-PER
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
  - name: langs
    sequence: string
  - name: spans
    sequence: string
  splits:
  - name: test
    num_bytes: 15736
    num_examples: 100
  - name: train
    num_bytes: 16654
    num_examples: 100
  - name: validation
    num_bytes: 15883
    num_examples: 100
  download_size: 234008884
  dataset_size: 48273
- config_name: fur
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-PER
          2: I-PER
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
  - name: langs
    sequence: string
  - name: spans
    sequence: string
  splits:
  - name: test
    num_bytes: 30562
    num_examples: 100
  - name: train
    num_bytes: 33654
    num_examples: 100
  - name: validation
    num_bytes: 25264
    num_examples: 100
  download_size: 234008884
  dataset_size: 89480
- config_name: fy
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-PER
          2: I-PER
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
  - name: langs
    sequence: string
  - name: spans
    sequence: string
  splits:
  - name: test
    num_bytes: 229700
    num_examples: 1000
  - name: train
    num_bytes: 223013
    num_examples: 1000
  - name: validation
    num_bytes: 226436
    num_examples: 1000
  download_size: 234008884
  dataset_size: 679149
- config_name: ga
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-PER
          2: I-PER
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
  - name: langs
    sequence: string
  - name: spans
    sequence: string
  splits:
  - name: test
    num_bytes: 235083
    num_examples: 1000
  - name: train
    num_bytes: 238047
    num_examples: 1000
  - name: validation
    num_bytes: 234092
    num_examples: 1000
  download_size: 234008884
  dataset_size: 707222
- config_name: gan
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-PER
          2: I-PER
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
  - name: langs
    sequence: string
  - name: spans
    sequence: string
  splits:
  - name: test
    num_bytes: 13879
    num_examples: 100
  - name: train
    num_bytes: 14398
    num_examples: 100
  - name: validation
    num_bytes: 17533
    num_examples: 100
  download_size: 234008884
  dataset_size: 45810
- config_name: gd
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-PER
          2: I-PER
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
  - name: langs
    sequence: string
  - name: spans
    sequence: string
  splits:
  - name: test
    num_bytes: 20308
    num_examples: 100
  - name: train
    num_bytes: 20154
    num_examples: 100
  - name: validation
    num_bytes: 23230
    num_examples: 100
  download_size: 234008884
  dataset_size: 63692
- config_name: gl
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-PER
          2: I-PER
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
  - name: langs
    sequence: string
  - name: spans
    sequence: string
  splits:
  - name: test
    num_bytes: 2031150
    num_examples: 10000
  - name: train
    num_bytes: 3030993
    num_examples: 15000
  - name: validation
    num_bytes: 2029683
    num_examples: 10000
  download_size: 234008884
  dataset_size: 7091826
- config_name: gn
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-PER
          2: I-PER
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
  - name: langs
    sequence: string
  - name: spans
    sequence: string
  splits:
  - name: test
    num_bytes: 24263
    num_examples: 100
  - name: train
    num_bytes: 28220
    num_examples: 100
  - name: validation
    num_bytes: 29132
    num_examples: 100
  download_size: 234008884
  dataset_size: 81615
- config_name: gu
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-PER
          2: I-PER
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
  - name: langs
    sequence: string
  - name: spans
    sequence: string
  splits:
  - name: test
    num_bytes: 45417
    num_examples: 100
  - name: train
    num_bytes: 42625
    num_examples: 100
  - name: validation
    num_bytes: 48009
    num_examples: 100
  download_size: 234008884
  dataset_size: 136051
- config_name: hak
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-PER
          2: I-PER
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
  - name: langs
    sequence: string
  - name: spans
    sequence: string
  splits:
  - name: test
    num_bytes: 18155
    num_examples: 100
  - name: train
    num_bytes: 16208
    num_examples: 100
  - name: validation
    num_bytes: 17977
    num_examples: 100
  download_size: 234008884
  dataset_size: 52340
- config_name: he
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-PER
          2: I-PER
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
  - name: langs
    sequence: string
  - name: spans
    sequence: string
  splits:
  - name: test
    num_bytes: 2785474
    num_examples: 10000
  - name: train
    num_bytes: 5600488
    num_examples: 20000
  - name: validation
    num_bytes: 2801392
    num_examples: 10000
  download_size: 234008884
  dataset_size: 11187354
- config_name: hi
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-PER
          2: I-PER
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
  - name: langs
    sequence: string
  - name: spans
    sequence: string
  splits:
  - name: test
    num_bytes: 267255
    num_examples: 1000
  - name: train
    num_bytes: 1315829
    num_examples: 5000
  - name: validation
    num_bytes: 261207
    num_examples: 1000
  download_size: 234008884
  dataset_size: 1844291
- config_name: hr
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-PER
          2: I-PER
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
  - name: langs
    sequence: string
  - name: spans
    sequence: string
  splits:
  - name: test
    num_bytes: 2430440
    num_examples: 10000
  - name: train
    num_bytes: 4877331
    num_examples: 20000
  - name: validation
    num_bytes: 2417450
    num_examples: 10000
  download_size: 234008884
  dataset_size: 9725221
- config_name: hsb
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-PER
          2: I-PER
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
  - name: langs
    sequence: string
  - name: spans
    sequence: string
  splits:
  - name: test
    num_bytes: 24348
    num_examples: 100
  - name: train
    num_bytes: 24228
    num_examples: 100
  - name: validation
    num_bytes: 24695
    num_examples: 100
  download_size: 234008884
  dataset_size: 73271
- config_name: hu
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-PER
          2: I-PER
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
  - name: langs
    sequence: string
  - name: spans
    sequence: string
  splits:
  - name: test
    num_bytes: 2626771
    num_examples: 10000
  - name: train
    num_bytes: 5263122
    num_examples: 20000
  - name: validation
    num_bytes: 2590116
    num_examples: 10000
  download_size: 234008884
  dataset_size: 10480009
- config_name: hy
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-PER
          2: I-PER
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
  - name: langs
    sequence: string
  - name: spans
    sequence: string
  splits:
  - name: test
    num_bytes: 237121
    num_examples: 1000
  - name: train
    num_bytes: 3634065
    num_examples: 15000
  - name: validation
    num_bytes: 237560
    num_examples: 1000
  download_size: 234008884
  dataset_size: 4108746
- config_name: ia
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-PER
          2: I-PER
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
  - name: langs
    sequence: string
  - name: spans
    sequence: string
  splits:
  - name: test
    num_bytes: 37617
    num_examples: 100
  - name: train
    num_bytes: 32928
    num_examples: 100
  - name: validation
    num_bytes: 32064
    num_examples: 100
  download_size: 234008884
  dataset_size: 102609
- config_name: id
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-PER
          2: I-PER
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
  - name: langs
    sequence: string
  - name: spans
    sequence: string
  splits:
  - name: test
    num_bytes: 1902732
    num_examples: 10000
  - name: train
    num_bytes: 3814047
    num_examples: 20000
  - name: validation
    num_bytes: 1901625
    num_examples: 10000
  download_size: 234008884
  dataset_size: 7618404
- config_name: ig
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-PER
          2: I-PER
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
  - name: langs
    sequence: string
  - name: spans
    sequence: string
  splits:
  - name: test
    num_bytes: 18432
    num_examples: 100
  - name: train
    num_bytes: 15988
    num_examples: 100
  - name: validation
    num_bytes: 17721
    num_examples: 100
  download_size: 234008884
  dataset_size: 52141
- config_name: ilo
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-PER
          2: I-PER
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
  - name: langs
    sequence: string
  - name: spans
    sequence: string
  splits:
  - name: test
    num_bytes: 17245
    num_examples: 100
  - name: train
    num_bytes: 17152
    num_examples: 100
  - name: validation
    num_bytes: 16675
    num_examples: 100
  download_size: 234008884
  dataset_size: 51072
- config_name: io
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-PER
          2: I-PER
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
  - name: langs
    sequence: string
  - name: spans
    sequence: string
  splits:
  - name: test
    num_bytes: 17231
    num_examples: 100
  - name: train
    num_bytes: 20781
    num_examples: 100
  - name: validation
    num_bytes: 19026
    num_examples: 100
  download_size: 234008884
  dataset_size: 57038
- config_name: is
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-PER
          2: I-PER
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
  - name: langs
    sequence: string
  - name: spans
    sequence: string
  splits:
  - name: test
    num_bytes: 235946
    num_examples: 1000
  - name: train
    num_bytes: 243465
    num_examples: 1000
  - name: validation
    num_bytes: 243667
    num_examples: 1000
  download_size: 234008884
  dataset_size: 723078
- config_name: it
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-PER
          2: I-PER
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
  - name: langs
    sequence: string
  - name: spans
    sequence: string
  splits:
  - name: test
    num_bytes: 2307618
    num_examples: 10000
  - name: train
    num_bytes: 4633575
    num_examples: 20000
  - name: validation
    num_bytes: 2282947
    num_examples: 10000
  download_size: 234008884
  dataset_size: 9224140
- config_name: ja
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-PER
          2: I-PER
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
  - name: langs
    sequence: string
  - name: spans
    sequence: string
  splits:
  - name: test
    num_bytes: 6898538
    num_examples: 10000
  - name: train
    num_bytes: 13578325
    num_examples: 20000
  - name: validation
    num_bytes: 6775608
    num_examples: 10000
  download_size: 234008884
  dataset_size: 27252471
- config_name: jbo
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-PER
          2: I-PER
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
  - name: langs
    sequence: string
  - name: spans
    sequence: string
  splits:
  - name: test
    num_bytes: 19586
    num_examples: 100
  - name: train
    num_bytes: 15070
    num_examples: 100
  - name: validation
    num_bytes: 15618
    num_examples: 100
  download_size: 234008884
  dataset_size: 50274
- config_name: jv
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-PER
          2: I-PER
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
  - name: langs
    sequence: string
  - name: spans
    sequence: string
  splits:
  - name: test
    num_bytes: 20203
    num_examples: 100
  - name: train
    num_bytes: 19409
    num_examples: 100
  - name: validation
    num_bytes: 17691
    num_examples: 100
  download_size: 234008884
  dataset_size: 57303
- config_name: ka
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-PER
          2: I-PER
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
  - name: langs
    sequence: string
  - name: spans
    sequence: string
  splits:
  - name: test
    num_bytes: 3480870
    num_examples: 10000
  - name: train
    num_bytes: 3428008
    num_examples: 10000
  - name: validation
    num_bytes: 3454381
    num_examples: 10000
  download_size: 234008884
  dataset_size: 10363259
- config_name: kk
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-PER
          2: I-PER
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
  - name: langs
    sequence: string
  - name: spans
    sequence: string
  splits:
  - name: test
    num_bytes: 284503
    num_examples: 1000
  - name: train
    num_bytes: 287952
    num_examples: 1000
  - name: validation
    num_bytes: 286502
    num_examples: 1000
  download_size: 234008884
  dataset_size: 858957
- config_name: km
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-PER
          2: I-PER
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
  - name: langs
    sequence: string
  - name: spans
    sequence: string
  splits:
  - name: test
    num_bytes: 36101
    num_examples: 100
  - name: train
    num_bytes: 31938
    num_examples: 100
  - name: validation
    num_bytes: 29310
    num_examples: 100
  download_size: 234008884
  dataset_size: 97349
- config_name: kn
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-PER
          2: I-PER
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
  - name: langs
    sequence: string
  - name: spans
    sequence: string
  splits:
  - name: test
    num_bytes: 32278
    num_examples: 100
  - name: train
    num_bytes: 34346
    num_examples: 100
  - name: validation
    num_bytes: 36853
    num_examples: 100
  download_size: 234008884
  dataset_size: 103477
- config_name: ko
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-PER
          2: I-PER
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
  - name: langs
    sequence: string
  - name: spans
    sequence: string
  splits:
  - name: test
    num_bytes: 2547800
    num_examples: 10000
  - name: train
    num_bytes: 5107090
    num_examples: 20000
  - name: validation
    num_bytes: 2553068
    num_examples: 10000
  download_size: 234008884
  dataset_size: 10207958
- config_name: ksh
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-PER
          2: I-PER
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
  - name: langs
    sequence: string
  - name: spans
    sequence: string
  splits:
  - name: test
    num_bytes: 25249
    num_examples: 100
  - name: train
    num_bytes: 25941
    num_examples: 100
  - name: validation
    num_bytes: 26338
    num_examples: 100
  download_size: 234008884
  dataset_size: 77528
- config_name: ku
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-PER
          2: I-PER
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
  - name: langs
    sequence: string
  - name: spans
    sequence: string
  splits:
  - name: test
    num_bytes: 20795
    num_examples: 100
  - name: train
    num_bytes: 22669
    num_examples: 100
  - name: validation
    num_bytes: 22597
    num_examples: 100
  download_size: 234008884
  dataset_size: 66061
- config_name: ky
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-PER
          2: I-PER
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
  - name: langs
    sequence: string
  - name: spans
    sequence: string
  splits:
  - name: test
    num_bytes: 31896
    num_examples: 100
  - name: train
    num_bytes: 32768
    num_examples: 100
  - name: validation
    num_bytes: 31010
    num_examples: 100
  download_size: 234008884
  dataset_size: 95674
- config_name: la
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-PER
          2: I-PER
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
  - name: langs
    sequence: string
  - name: spans
    sequence: string
  splits:
  - name: test
    num_bytes: 198910
    num_examples: 1000
  - name: train
    num_bytes: 999050
    num_examples: 5000
  - name: validation
    num_bytes: 207205
    num_examples: 1000
  download_size: 234008884
  dataset_size: 1405165
- config_name: lb
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-PER
          2: I-PER
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
  - name: langs
    sequence: string
  - name: spans
    sequence: string
  splits:
  - name: test
    num_bytes: 249989
    num_examples: 1000
  - name: train
    num_bytes: 1260939
    num_examples: 5000
  - name: validation
    num_bytes: 253774
    num_examples: 1000
  download_size: 234008884
  dataset_size: 1764702
- config_name: li
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-PER
          2: I-PER
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
  - name: langs
    sequence: string
  - name: spans
    sequence: string
  splits:
  - name: test
    num_bytes: 18817
    num_examples: 100
  - name: train
    num_bytes: 20211
    num_examples: 100
  - name: validation
    num_bytes: 20201
    num_examples: 100
  download_size: 234008884
  dataset_size: 59229
- config_name: lij
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-PER
          2: I-PER
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
  - name: langs
    sequence: string
  - name: spans
    sequence: string
  splits:
  - name: test
    num_bytes: 27882
    num_examples: 100
  - name: train
    num_bytes: 30581
    num_examples: 100
  - name: validation
    num_bytes: 28005
    num_examples: 100
  download_size: 234008884
  dataset_size: 86468
- config_name: lmo
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-PER
          2: I-PER
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
  - name: langs
    sequence: string
  - name: spans
    sequence: string
  splits:
  - name: test
    num_bytes: 29453
    num_examples: 100
  - name: train
    num_bytes: 24161
    num_examples: 100
  - name: validation
    num_bytes: 26575
    num_examples: 100
  download_size: 234008884
  dataset_size: 80189
- config_name: ln
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-PER
          2: I-PER
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
  - name: langs
    sequence: string
  - name: spans
    sequence: string
  splits:
  - name: test
    num_bytes: 27003
    num_examples: 100
  - name: train
    num_bytes: 22227
    num_examples: 100
  - name: validation
    num_bytes: 21709
    num_examples: 100
  download_size: 234008884
  dataset_size: 70939
- config_name: lt
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-PER
          2: I-PER
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
  - name: langs
    sequence: string
  - name: spans
    sequence: string
  splits:
  - name: test
    num_bytes: 2191269
    num_examples: 10000
  - name: train
    num_bytes: 2199946
    num_examples: 10000
  - name: validation
    num_bytes: 2192874
    num_examples: 10000
  download_size: 234008884
  dataset_size: 6584089
- config_name: lv
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-PER
          2: I-PER
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
  - name: langs
    sequence: string
  - name: spans
    sequence: string
  splits:
  - name: test
    num_bytes: 2190458
    num_examples: 10000
  - name: train
    num_bytes: 2206943
    num_examples: 10000
  - name: validation
    num_bytes: 2173420
    num_examples: 10000
  download_size: 234008884
  dataset_size: 6570821
- config_name: map-bms
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-PER
          2: I-PER
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
  - name: langs
    sequence: string
  - name: spans
    sequence: string
  splits:
  - name: test
    num_bytes: 20558
    num_examples: 100
  - name: train
    num_bytes: 21639
    num_examples: 100
  - name: validation
    num_bytes: 19780
    num_examples: 100
  download_size: 234008884
  dataset_size: 61977
- config_name: mg
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-PER
          2: I-PER
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
  - name: langs
    sequence: string
  - name: spans
    sequence: string
  splits:
  - name: test
    num_bytes: 22570
    num_examples: 100
  - name: train
    num_bytes: 25739
    num_examples: 100
  - name: validation
    num_bytes: 24861
    num_examples: 100
  download_size: 234008884
  dataset_size: 73170
- config_name: mhr
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-PER
          2: I-PER
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
  - name: langs
    sequence: string
  - name: spans
    sequence: string
  splits:
  - name: test
    num_bytes: 23639
    num_examples: 100
  - name: train
    num_bytes: 18648
    num_examples: 100
  - name: validation
    num_bytes: 23263
    num_examples: 100
  download_size: 234008884
  dataset_size: 65550
- config_name: mi
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-PER
          2: I-PER
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
  - name: langs
    sequence: string
  - name: spans
    sequence: string
  splits:
  - name: test
    num_bytes: 40147
    num_examples: 100
  - name: train
    num_bytes: 37896
    num_examples: 100
  - name: validation
    num_bytes: 39399
    num_examples: 100
  download_size: 234008884
  dataset_size: 117442
- config_name: min
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-PER
          2: I-PER
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
  - name: langs
    sequence: string
  - name: spans
    sequence: string
  splits:
  - name: test
    num_bytes: 24741
    num_examples: 100
  - name: train
    num_bytes: 26620
    num_examples: 100
  - name: validation
    num_bytes: 28719
    num_examples: 100
  download_size: 234008884
  dataset_size: 80080
- config_name: mk
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-PER
          2: I-PER
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
  - name: langs
    sequence: string
  - name: spans
    sequence: string
  splits:
  - name: test
    num_bytes: 337757
    num_examples: 1000
  - name: train
    num_bytes: 3355936
    num_examples: 10000
  - name: validation
    num_bytes: 333193
    num_examples: 1000
  download_size: 234008884
  dataset_size: 4026886
- config_name: ml
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-PER
          2: I-PER
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
  - name: langs
    sequence: string
  - name: spans
    sequence: string
  splits:
  - name: test
    num_bytes: 349383
    num_examples: 1000
  - name: train
    num_bytes: 3582066
    num_examples: 10000
  - name: validation
    num_bytes: 363008
    num_examples: 1000
  download_size: 234008884
  dataset_size: 4294457
- config_name: mn
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-PER
          2: I-PER
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
  - name: langs
    sequence: string
  - name: spans
    sequence: string
  splits:
  - name: test
    num_bytes: 23538
    num_examples: 100
  - name: train
    num_bytes: 23244
    num_examples: 100
  - name: validation
    num_bytes: 22006
    num_examples: 100
  download_size: 234008884
  dataset_size: 68788
- config_name: mr
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-PER
          2: I-PER
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
  - name: langs
    sequence: string
  - name: spans
    sequence: string
  splits:
  - name: test
    num_bytes: 326290
    num_examples: 1000
  - name: train
    num_bytes: 1598804
    num_examples: 5000
  - name: validation
    num_bytes: 314858
    num_examples: 1000
  download_size: 234008884
  dataset_size: 2239952
- config_name: ms
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-PER
          2: I-PER
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
  - name: langs
    sequence: string
  - name: spans
    sequence: string
  splits:
  - name: test
    num_bytes: 183539
    num_examples: 1000
  - name: train
    num_bytes: 3699238
    num_examples: 20000
  - name: validation
    num_bytes: 183944
    num_examples: 1000
  download_size: 234008884
  dataset_size: 4066721
- config_name: mt
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-PER
          2: I-PER
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
  - name: langs
    sequence: string
  - name: spans
    sequence: string
  splits:
  - name: test
    num_bytes: 24662
    num_examples: 100
  - name: train
    num_bytes: 24956
    num_examples: 100
  - name: validation
    num_bytes: 24571
    num_examples: 100
  download_size: 234008884
  dataset_size: 74189
- config_name: mwl
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-PER
          2: I-PER
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
  - name: langs
    sequence: string
  - name: spans
    sequence: string
  splits:
  - name: test
    num_bytes: 43008
    num_examples: 100
  - name: train
    num_bytes: 44605
    num_examples: 100
  - name: validation
    num_bytes: 51987
    num_examples: 100
  download_size: 234008884
  dataset_size: 139600
- config_name: my
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-PER
          2: I-PER
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
  - name: langs
    sequence: string
  - name: spans
    sequence: string
  splits:
  - name: test
    num_bytes: 45956
    num_examples: 100
  - name: train
    num_bytes: 41371
    num_examples: 100
  - name: validation
    num_bytes: 48953
    num_examples: 100
  download_size: 234008884
  dataset_size: 136280
- config_name: mzn
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-PER
          2: I-PER
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
  - name: langs
    sequence: string
  - name: spans
    sequence: string
  splits:
  - name: test
    num_bytes: 25947
    num_examples: 100
  - name: train
    num_bytes: 24841
    num_examples: 100
  - name: validation
    num_bytes: 25304
    num_examples: 100
  download_size: 234008884
  dataset_size: 76092
- config_name: nap
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-PER
          2: I-PER
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
  - name: langs
    sequence: string
  - name: spans
    sequence: string
  splits:
  - name: test
    num_bytes: 24194
    num_examples: 100
  - name: train
    num_bytes: 26596
    num_examples: 100
  - name: validation
    num_bytes: 21546
    num_examples: 100
  download_size: 234008884
  dataset_size: 72336
- config_name: nds
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-PER
          2: I-PER
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
  - name: langs
    sequence: string
  - name: spans
    sequence: string
  splits:
  - name: test
    num_bytes: 26571
    num_examples: 100
  - name: train
    num_bytes: 24679
    num_examples: 100
  - name: validation
    num_bytes: 28388
    num_examples: 100
  download_size: 234008884
  dataset_size: 79638
- config_name: ne
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-PER
          2: I-PER
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
  - name: langs
    sequence: string
  - name: spans
    sequence: string
  splits:
  - name: test
    num_bytes: 33227
    num_examples: 100
  - name: train
    num_bytes: 36173
    num_examples: 100
  - name: validation
    num_bytes: 33932
    num_examples: 100
  download_size: 234008884
  dataset_size: 103332
- config_name: nl
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-PER
          2: I-PER
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
  - name: langs
    sequence: string
  - name: spans
    sequence: string
  splits:
  - name: test
    num_bytes: 2403076
    num_examples: 10000
  - name: train
    num_bytes: 4784289
    num_examples: 20000
  - name: validation
    num_bytes: 2378080
    num_examples: 10000
  download_size: 234008884
  dataset_size: 9565445
- config_name: nn
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-PER
          2: I-PER
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
  - name: langs
    sequence: string
  - name: spans
    sequence: string
  splits:
  - name: test
    num_bytes: 269631
    num_examples: 1000
  - name: train
    num_bytes: 5436185
    num_examples: 20000
  - name: validation
    num_bytes: 274140
    num_examples: 1000
  download_size: 234008884
  dataset_size: 5979956
- config_name: 'no'
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-PER
          2: I-PER
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
  - name: langs
    sequence: string
  - name: spans
    sequence: string
  splits:
  - name: test
    num_bytes: 2563559
    num_examples: 10000
  - name: train
    num_bytes: 5139548
    num_examples: 20000
  - name: validation
    num_bytes: 2576669
    num_examples: 10000
  download_size: 234008884
  dataset_size: 10279776
- config_name: nov
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-PER
          2: I-PER
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
  - name: langs
    sequence: string
  - name: spans
    sequence: string
  splits:
  - name: test
    num_bytes: 14830
    num_examples: 100
  - name: train
    num_bytes: 17270
    num_examples: 100
  - name: validation
    num_bytes: 14856
    num_examples: 100
  download_size: 234008884
  dataset_size: 46956
- config_name: oc
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-PER
          2: I-PER
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
  - name: langs
    sequence: string
  - name: spans
    sequence: string
  splits:
  - name: test
    num_bytes: 18600
    num_examples: 100
  - name: train
    num_bytes: 19319
    num_examples: 100
  - name: validation
    num_bytes: 20428
    num_examples: 100
  download_size: 234008884
  dataset_size: 58347
- config_name: or
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-PER
          2: I-PER
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
  - name: langs
    sequence: string
  - name: spans
    sequence: string
  splits:
  - name: test
    num_bytes: 29508
    num_examples: 100
  - name: train
    num_bytes: 27822
    num_examples: 100
  - name: validation
    num_bytes: 32131
    num_examples: 100
  download_size: 234008884
  dataset_size: 89461
- config_name: os
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-PER
          2: I-PER
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
  - name: langs
    sequence: string
  - name: spans
    sequence: string
  splits:
  - name: test
    num_bytes: 25995
    num_examples: 100
  - name: train
    num_bytes: 26033
    num_examples: 100
  - name: validation
    num_bytes: 26779
    num_examples: 100
  download_size: 234008884
  dataset_size: 78807
- config_name: pa
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-PER
          2: I-PER
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
  - name: langs
    sequence: string
  - name: spans
    sequence: string
  splits:
  - name: test
    num_bytes: 23708
    num_examples: 100
  - name: train
    num_bytes: 24171
    num_examples: 100
  - name: validation
    num_bytes: 25230
    num_examples: 100
  download_size: 234008884
  dataset_size: 73109
- config_name: pdc
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-PER
          2: I-PER
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
  - name: langs
    sequence: string
  - name: spans
    sequence: string
  splits:
  - name: test
    num_bytes: 24674
    num_examples: 100
  - name: train
    num_bytes: 23991
    num_examples: 100
  - name: validation
    num_bytes: 24419
    num_examples: 100
  download_size: 234008884
  dataset_size: 73084
- config_name: pl
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-PER
          2: I-PER
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
  - name: langs
    sequence: string
  - name: spans
    sequence: string
  splits:
  - name: test
    num_bytes: 2463783
    num_examples: 10000
  - name: train
    num_bytes: 4851527
    num_examples: 20000
  - name: validation
    num_bytes: 2448324
    num_examples: 10000
  download_size: 234008884
  dataset_size: 9763634
- config_name: pms
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-PER
          2: I-PER
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
  - name: langs
    sequence: string
  - name: spans
    sequence: string
  splits:
  - name: test
    num_bytes: 24015
    num_examples: 100
  - name: train
    num_bytes: 27429
    num_examples: 100
  - name: validation
    num_bytes: 28369
    num_examples: 100
  download_size: 234008884
  dataset_size: 79813
- config_name: pnb
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-PER
          2: I-PER
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
  - name: langs
    sequence: string
  - name: spans
    sequence: string
  splits:
  - name: test
    num_bytes: 21206
    num_examples: 100
  - name: train
    num_bytes: 19504
    num_examples: 100
  - name: validation
    num_bytes: 19070
    num_examples: 100
  download_size: 234008884
  dataset_size: 59780
- config_name: ps
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-PER
          2: I-PER
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
  - name: langs
    sequence: string
  - name: spans
    sequence: string
  splits:
  - name: test
    num_bytes: 43621
    num_examples: 100
  - name: train
    num_bytes: 63501
    num_examples: 100
  - name: validation
    num_bytes: 49901
    num_examples: 100
  download_size: 234008884
  dataset_size: 157023
- config_name: pt
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-PER
          2: I-PER
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
  - name: langs
    sequence: string
  - name: spans
    sequence: string
  splits:
  - name: test
    num_bytes: 1946729
    num_examples: 10000
  - name: train
    num_bytes: 3917453
    num_examples: 20000
  - name: validation
    num_bytes: 1962145
    num_examples: 10000
  download_size: 234008884
  dataset_size: 7826327
- config_name: qu
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-PER
          2: I-PER
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
  - name: langs
    sequence: string
  - name: spans
    sequence: string
  splits:
  - name: test
    num_bytes: 17675
    num_examples: 100
  - name: train
    num_bytes: 16989
    num_examples: 100
  - name: validation
    num_bytes: 18231
    num_examples: 100
  download_size: 234008884
  dataset_size: 52895
- config_name: rm
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-PER
          2: I-PER
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
  - name: langs
    sequence: string
  - name: spans
    sequence: string
  splits:
  - name: test
    num_bytes: 35880
    num_examples: 100
  - name: train
    num_bytes: 30489
    num_examples: 100
  - name: validation
    num_bytes: 32776
    num_examples: 100
  download_size: 234008884
  dataset_size: 99145
- config_name: ro
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-PER
          2: I-PER
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
  - name: langs
    sequence: string
  - name: spans
    sequence: string
  splits:
  - name: test
    num_bytes: 2060933
    num_examples: 10000
  - name: train
    num_bytes: 4179869
    num_examples: 20000
  - name: validation
    num_bytes: 2063860
    num_examples: 10000
  download_size: 234008884
  dataset_size: 8304662
- config_name: ru
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-PER
          2: I-PER
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
  - name: langs
    sequence: string
  - name: spans
    sequence: string
  splits:
  - name: test
    num_bytes: 2597248
    num_examples: 10000
  - name: train
    num_bytes: 5175665
    num_examples: 20000
  - name: validation
    num_bytes: 2574546
    num_examples: 10000
  download_size: 234008884
  dataset_size: 10347459
- config_name: rw
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-PER
          2: I-PER
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
  - name: langs
    sequence: string
  - name: spans
    sequence: string
  splits:
  - name: test
    num_bytes: 14445
    num_examples: 100
  - name: train
    num_bytes: 16778
    num_examples: 100
  - name: validation
    num_bytes: 17999
    num_examples: 100
  download_size: 234008884
  dataset_size: 49222
- config_name: sa
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-PER
          2: I-PER
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
  - name: langs
    sequence: string
  - name: spans
    sequence: string
  splits:
  - name: test
    num_bytes: 49209
    num_examples: 100
  - name: train
    num_bytes: 52504
    num_examples: 100
  - name: validation
    num_bytes: 45721
    num_examples: 100
  download_size: 234008884
  dataset_size: 147434
- config_name: sah
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-PER
          2: I-PER
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
  - name: langs
    sequence: string
  - name: spans
    sequence: string
  splits:
  - name: test
    num_bytes: 26853
    num_examples: 100
  - name: train
    num_bytes: 27041
    num_examples: 100
  - name: validation
    num_bytes: 27875
    num_examples: 100
  download_size: 234008884
  dataset_size: 81769
- config_name: scn
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-PER
          2: I-PER
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
  - name: langs
    sequence: string
  - name: spans
    sequence: string
  splits:
  - name: test
    num_bytes: 17384
    num_examples: 100
  - name: train
    num_bytes: 21032
    num_examples: 100
  - name: validation
    num_bytes: 20105
    num_examples: 100
  download_size: 234008884
  dataset_size: 58521
- config_name: sco
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-PER
          2: I-PER
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
  - name: langs
    sequence: string
  - name: spans
    sequence: string
  splits:
  - name: test
    num_bytes: 21589
    num_examples: 100
  - name: train
    num_bytes: 20308
    num_examples: 100
  - name: validation
    num_bytes: 22215
    num_examples: 100
  download_size: 234008884
  dataset_size: 64112
- config_name: sd
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-PER
          2: I-PER
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
  - name: langs
    sequence: string
  - name: spans
    sequence: string
  splits:
  - name: test
    num_bytes: 38534
    num_examples: 100
  - name: train
    num_bytes: 56925
    num_examples: 100
  - name: validation
    num_bytes: 51555
    num_examples: 100
  download_size: 234008884
  dataset_size: 147014
- config_name: sh
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-PER
          2: I-PER
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
  - name: langs
    sequence: string
  - name: spans
    sequence: string
  splits:
  - name: test
    num_bytes: 1791491
    num_examples: 10000
  - name: train
    num_bytes: 3583633
    num_examples: 20000
  - name: validation
    num_bytes: 1789918
    num_examples: 10000
  download_size: 234008884
  dataset_size: 7165042
- config_name: si
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-PER
          2: I-PER
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
  - name: langs
    sequence: string
  - name: spans
    sequence: string
  splits:
  - name: test
    num_bytes: 29341
    num_examples: 100
  - name: train
    num_bytes: 31255
    num_examples: 100
  - name: validation
    num_bytes: 30845
    num_examples: 100
  download_size: 234008884
  dataset_size: 91441
- config_name: simple
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-PER
          2: I-PER
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
  - name: langs
    sequence: string
  - name: spans
    sequence: string
  splits:
  - name: test
    num_bytes: 245358
    num_examples: 1000
  - name: train
    num_bytes: 4921916
    num_examples: 20000
  - name: validation
    num_bytes: 247147
    num_examples: 1000
  download_size: 234008884
  dataset_size: 5414421
- config_name: sk
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-PER
          2: I-PER
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
  - name: langs
    sequence: string
  - name: spans
    sequence: string
  splits:
  - name: test
    num_bytes: 2335009
    num_examples: 10000
  - name: train
    num_bytes: 4701553
    num_examples: 20000
  - name: validation
    num_bytes: 2342061
    num_examples: 10000
  download_size: 234008884
  dataset_size: 9378623
- config_name: sl
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-PER
          2: I-PER
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
  - name: langs
    sequence: string
  - name: spans
    sequence: string
  splits:
  - name: test
    num_bytes: 2133491
    num_examples: 10000
  - name: train
    num_bytes: 3158676
    num_examples: 15000
  - name: validation
    num_bytes: 2090247
    num_examples: 10000
  download_size: 234008884
  dataset_size: 7382414
- config_name: so
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-PER
          2: I-PER
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
  - name: langs
    sequence: string
  - name: spans
    sequence: string
  splits:
  - name: test
    num_bytes: 17219
    num_examples: 100
  - name: train
    num_bytes: 23780
    num_examples: 100
  - name: validation
    num_bytes: 21864
    num_examples: 100
  download_size: 234008884
  dataset_size: 62863
- config_name: sq
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-PER
          2: I-PER
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
  - name: langs
    sequence: string
  - name: spans
    sequence: string
  splits:
  - name: test
    num_bytes: 209824
    num_examples: 1000
  - name: train
    num_bytes: 1052387
    num_examples: 5000
  - name: validation
    num_bytes: 210888
    num_examples: 1000
  download_size: 234008884
  dataset_size: 1473099
- config_name: sr
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-PER
          2: I-PER
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
  - name: langs
    sequence: string
  - name: spans
    sequence: string
  splits:
  - name: test
    num_bytes: 2564831
    num_examples: 10000
  - name: train
    num_bytes: 5105569
    num_examples: 20000
  - name: validation
    num_bytes: 2548390
    num_examples: 10000
  download_size: 234008884
  dataset_size: 10218790
- config_name: su
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-PER
          2: I-PER
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
  - name: langs
    sequence: string
  - name: spans
    sequence: string
  splits:
  - name: test
    num_bytes: 21861
    num_examples: 100
  - name: train
    num_bytes: 20839
    num_examples: 100
  - name: validation
    num_bytes: 22605
    num_examples: 100
  download_size: 234008884
  dataset_size: 65305
- config_name: sv
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-PER
          2: I-PER
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
  - name: langs
    sequence: string
  - name: spans
    sequence: string
  splits:
  - name: test
    num_bytes: 2719077
    num_examples: 10000
  - name: train
    num_bytes: 5395722
    num_examples: 20000
  - name: validation
    num_bytes: 2678672
    num_examples: 10000
  download_size: 234008884
  dataset_size: 10793471
- config_name: sw
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-PER
          2: I-PER
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
  - name: langs
    sequence: string
  - name: spans
    sequence: string
  splits:
  - name: test
    num_bytes: 172693
    num_examples: 1000
  - name: train
    num_bytes: 168749
    num_examples: 1000
  - name: validation
    num_bytes: 168819
    num_examples: 1000
  download_size: 234008884
  dataset_size: 510261
- config_name: szl
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-PER
          2: I-PER
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
  - name: langs
    sequence: string
  - name: spans
    sequence: string
  splits:
  - name: test
    num_bytes: 18967
    num_examples: 100
  - name: train
    num_bytes: 17646
    num_examples: 100
  - name: validation
    num_bytes: 19397
    num_examples: 100
  download_size: 234008884
  dataset_size: 56010
- config_name: ta
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-PER
          2: I-PER
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
  - name: langs
    sequence: string
  - name: spans
    sequence: string
  splits:
  - name: test
    num_bytes: 357667
    num_examples: 1000
  - name: train
    num_bytes: 5275759
    num_examples: 15000
  - name: validation
    num_bytes: 354957
    num_examples: 1000
  download_size: 234008884
  dataset_size: 5988383
- config_name: te
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-PER
          2: I-PER
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
  - name: langs
    sequence: string
  - name: spans
    sequence: string
  splits:
  - name: test
    num_bytes: 359780
    num_examples: 1000
  - name: train
    num_bytes: 358792
    num_examples: 1000
  - name: validation
    num_bytes: 356189
    num_examples: 1000
  download_size: 234008884
  dataset_size: 1074761
- config_name: tg
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-PER
          2: I-PER
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
  - name: langs
    sequence: string
  - name: spans
    sequence: string
  splits:
  - name: test
    num_bytes: 28821
    num_examples: 100
  - name: train
    num_bytes: 27200
    num_examples: 100
  - name: validation
    num_bytes: 27130
    num_examples: 100
  download_size: 234008884
  dataset_size: 83151
- config_name: th
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-PER
          2: I-PER
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
  - name: langs
    sequence: string
  - name: spans
    sequence: string
  splits:
  - name: test
    num_bytes: 14505054
    num_examples: 10000
  - name: train
    num_bytes: 28968916
    num_examples: 20000
  - name: validation
    num_bytes: 14189743
    num_examples: 10000
  download_size: 234008884
  dataset_size: 57663713
- config_name: tk
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-PER
          2: I-PER
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
  - name: langs
    sequence: string
  - name: spans
    sequence: string
  splits:
  - name: test
    num_bytes: 20302
    num_examples: 100
  - name: train
    num_bytes: 19521
    num_examples: 100
  - name: validation
    num_bytes: 21611
    num_examples: 100
  download_size: 234008884
  dataset_size: 61434
- config_name: tl
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-PER
          2: I-PER
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
  - name: langs
    sequence: string
  - name: spans
    sequence: string
  splits:
  - name: test
    num_bytes: 152964
    num_examples: 1000
  - name: train
    num_bytes: 1518784
    num_examples: 10000
  - name: validation
    num_bytes: 148682
    num_examples: 1000
  download_size: 234008884
  dataset_size: 1820430
- config_name: tr
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-PER
          2: I-PER
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
  - name: langs
    sequence: string
  - name: spans
    sequence: string
  splits:
  - name: test
    num_bytes: 2276920
    num_examples: 10000
  - name: train
    num_bytes: 4501912
    num_examples: 20000
  - name: validation
    num_bytes: 2280517
    num_examples: 10000
  download_size: 234008884
  dataset_size: 9059349
- config_name: tt
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-PER
          2: I-PER
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
  - name: langs
    sequence: string
  - name: spans
    sequence: string
  splits:
  - name: test
    num_bytes: 282691
    num_examples: 1000
  - name: train
    num_bytes: 283392
    num_examples: 1000
  - name: validation
    num_bytes: 282535
    num_examples: 1000
  download_size: 234008884
  dataset_size: 848618
- config_name: ug
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-PER
          2: I-PER
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
  - name: langs
    sequence: string
  - name: spans
    sequence: string
  splits:
  - name: test
    num_bytes: 31129
    num_examples: 100
  - name: train
    num_bytes: 26620
    num_examples: 100
  - name: validation
    num_bytes: 35219
    num_examples: 100
  download_size: 234008884
  dataset_size: 92968
- config_name: uk
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-PER
          2: I-PER
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
  - name: langs
    sequence: string
  - name: spans
    sequence: string
  splits:
  - name: test
    num_bytes: 2928200
    num_examples: 10000
  - name: train
    num_bytes: 5928026
    num_examples: 20000
  - name: validation
    num_bytes: 2934897
    num_examples: 10000
  download_size: 234008884
  dataset_size: 11791123
- config_name: ur
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-PER
          2: I-PER
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
  - name: langs
    sequence: string
  - name: spans
    sequence: string
  splits:
  - name: test
    num_bytes: 203138
    num_examples: 1000
  - name: train
    num_bytes: 4108707
    num_examples: 20000
  - name: validation
    num_bytes: 203747
    num_examples: 1000
  download_size: 234008884
  dataset_size: 4515592
- config_name: uz
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-PER
          2: I-PER
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
  - name: langs
    sequence: string
  - name: spans
    sequence: string
  splits:
  - name: test
    num_bytes: 184713
    num_examples: 1000
  - name: train
    num_bytes: 186105
    num_examples: 1000
  - name: validation
    num_bytes: 184625
    num_examples: 1000
  download_size: 234008884
  dataset_size: 555443
- config_name: vec
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-PER
          2: I-PER
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
  - name: langs
    sequence: string
  - name: spans
    sequence: string
  splits:
  - name: test
    num_bytes: 20254
    num_examples: 100
  - name: train
    num_bytes: 20437
    num_examples: 100
  - name: validation
    num_bytes: 19335
    num_examples: 100
  download_size: 234008884
  dataset_size: 60026
- config_name: vep
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-PER
          2: I-PER
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
  - name: langs
    sequence: string
  - name: spans
    sequence: string
  splits:
  - name: test
    num_bytes: 21371
    num_examples: 100
  - name: train
    num_bytes: 21387
    num_examples: 100
  - name: validation
    num_bytes: 22306
    num_examples: 100
  download_size: 234008884
  dataset_size: 65064
- config_name: vi
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-PER
          2: I-PER
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
  - name: langs
    sequence: string
  - name: spans
    sequence: string
  splits:
  - name: test
    num_bytes: 1960024
    num_examples: 10000
  - name: train
    num_bytes: 3915944
    num_examples: 20000
  - name: validation
    num_bytes: 1944856
    num_examples: 10000
  download_size: 234008884
  dataset_size: 7820824
- config_name: vls
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-PER
          2: I-PER
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
  - name: langs
    sequence: string
  - name: spans
    sequence: string
  splits:
  - name: test
    num_bytes: 26778
    num_examples: 100
  - name: train
    num_bytes: 26183
    num_examples: 100
  - name: validation
    num_bytes: 27895
    num_examples: 100
  download_size: 234008884
  dataset_size: 80856
- config_name: vo
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-PER
          2: I-PER
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
  - name: langs
    sequence: string
  - name: spans
    sequence: string
  splits:
  - name: test
    num_bytes: 14001
    num_examples: 100
  - name: train
    num_bytes: 14442
    num_examples: 100
  - name: validation
    num_bytes: 14385
    num_examples: 100
  download_size: 234008884
  dataset_size: 42828
- config_name: wa
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-PER
          2: I-PER
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
  - name: langs
    sequence: string
  - name: spans
    sequence: string
  splits:
  - name: test
    num_bytes: 21581
    num_examples: 100
  - name: train
    num_bytes: 23072
    num_examples: 100
  - name: validation
    num_bytes: 22493
    num_examples: 100
  download_size: 234008884
  dataset_size: 67146
- config_name: war
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-PER
          2: I-PER
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
  - name: langs
    sequence: string
  - name: spans
    sequence: string
  splits:
  - name: test
    num_bytes: 19912
    num_examples: 100
  - name: train
    num_bytes: 18829
    num_examples: 100
  - name: validation
    num_bytes: 16834
    num_examples: 100
  download_size: 234008884
  dataset_size: 55575
- config_name: wuu
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-PER
          2: I-PER
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
  - name: langs
    sequence: string
  - name: spans
    sequence: string
  splits:
  - name: test
    num_bytes: 15067
    num_examples: 100
  - name: train
    num_bytes: 17016
    num_examples: 100
  - name: validation
    num_bytes: 15123
    num_examples: 100
  download_size: 234008884
  dataset_size: 47206
- config_name: xmf
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-PER
          2: I-PER
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
  - name: langs
    sequence: string
  - name: spans
    sequence: string
  splits:
  - name: test
    num_bytes: 36081
    num_examples: 100
  - name: train
    num_bytes: 31796
    num_examples: 100
  - name: validation
    num_bytes: 39979
    num_examples: 100
  download_size: 234008884
  dataset_size: 107856
- config_name: yi
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-PER
          2: I-PER
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
  - name: langs
    sequence: string
  - name: spans
    sequence: string
  splits:
  - name: test
    num_bytes: 25005
    num_examples: 100
  - name: train
    num_bytes: 27303
    num_examples: 100
  - name: validation
    num_bytes: 25269
    num_examples: 100
  download_size: 234008884
  dataset_size: 77577
- config_name: yo
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-PER
          2: I-PER
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
  - name: langs
    sequence: string
  - name: spans
    sequence: string
  splits:
  - name: test
    num_bytes: 17996
    num_examples: 100
  - name: train
    num_bytes: 18984
    num_examples: 100
  - name: validation
    num_bytes: 17738
    num_examples: 100
  download_size: 234008884
  dataset_size: 54718
- config_name: zea
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-PER
          2: I-PER
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
  - name: langs
    sequence: string
  - name: spans
    sequence: string
  splits:
  - name: test
    num_bytes: 22997
    num_examples: 100
  - name: train
    num_bytes: 21252
    num_examples: 100
  - name: validation
    num_bytes: 24916
    num_examples: 100
  download_size: 234008884
  dataset_size: 69165
- config_name: zh
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-PER
          2: I-PER
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
  - name: langs
    sequence: string
  - name: spans
    sequence: string
  splits:
  - name: test
    num_bytes: 4709458
    num_examples: 10000
  - name: train
    num_bytes: 9524981
    num_examples: 20000
  - name: validation
    num_bytes: 4839728
    num_examples: 10000
  download_size: 234008884
  dataset_size: 19074167
- config_name: zh-classical
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-PER
          2: I-PER
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
  - name: langs
    sequence: string
  - name: spans
    sequence: string
  splits:
  - name: test
    num_bytes: 65885
    num_examples: 100
  - name: train
    num_bytes: 56238
    num_examples: 100
  - name: validation
    num_bytes: 59980
    num_examples: 100
  download_size: 234008884
  dataset_size: 182103
- config_name: zh-min-nan
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-PER
          2: I-PER
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
  - name: langs
    sequence: string
  - name: spans
    sequence: string
  splits:
  - name: test
    num_bytes: 24326
    num_examples: 100
  - name: train
    num_bytes: 19358
    num_examples: 100
  - name: validation
    num_bytes: 24533
    num_examples: 100
  download_size: 234008884
  dataset_size: 68217
- config_name: zh-yue
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-PER
          2: I-PER
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
  - name: langs
    sequence: string
  - name: spans
    sequence: string
  splits:
  - name: test
    num_bytes: 4964029
    num_examples: 10000
  - name: train
    num_bytes: 9950629
    num_examples: 20000
  - name: validation
    num_bytes: 4934158
    num_examples: 10000
  download_size: 234008884
  dataset_size: 19848816
---

# Dataset Card for WikiANN

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

- **Homepage:** [Massively Multilingual Transfer for NER](https://github.com/afshinrahimi/mmner)
- **Repository:** [Massively Multilingual Transfer for NER](https://github.com/afshinrahimi/mmner)
- **Paper:** The original datasets come from the _Cross-lingual name tagging and linking for 282 languages_ [paper](https://www.aclweb.org/anthology/P17-1178/) by Xiaoman Pan et al. (2018). This version corresponds to the balanced train, dev, and test splits of the original data from the _Massively Multilingual Transfer for NER_ [paper](https://arxiv.org/abs/1902.00193) by Afshin Rahimi et al. (2019).
- **Leaderboard:**
- **Point of Contact:** [Afshin Rahimi](mailto:afshinrahimi@gmail.com) or [Lewis Tunstall](mailto:lewis.c.tunstall@gmail.com) or [Albert Villanova del Moral](albert@huggingface.co)

### Dataset Summary

WikiANN (sometimes called PAN-X) is a multilingual named entity recognition dataset consisting of Wikipedia articles annotated with LOC (location), PER (person), and ORG (organisation) tags in the IOB2 format. This version corresponds to the balanced train, dev, and test splits of Rahimi et al. (2019), which supports 176 of the 282 languages from the original WikiANN corpus.

### Supported Tasks and Leaderboards

- `named-entity-recognition`: The dataset can be used to train a model for named entity recognition in many languages, or evaluate the zero-shot cross-lingual capabilities of multilingual models.

### Languages

The dataset contains 176 languages, one in each of the configuration subsets. The corresponding BCP 47 language tags
are:

|                    | Language tag   |
|:-------------------|:---------------|
| ace                | ace            |
| af                 | af             |
| als                | als            |
| am                 | am             |
| an                 | an             |
| ang                | ang            |
| ar                 | ar             |
| arc                | arc            |
| arz                | arz            |
| as                 | as             |
| ast                | ast            |
| ay                 | ay             |
| az                 | az             |
| ba                 | ba             |
| bar                | bar            |
| be                 | be             |
| bg                 | bg             |
| bh                 | bh             |
| bn                 | bn             |
| bo                 | bo             |
| br                 | br             |
| bs                 | bs             |
| ca                 | ca             |
| cdo                | cdo            |
| ce                 | ce             |
| ceb                | ceb            |
| ckb                | ckb            |
| co                 | co             |
| crh                | crh            |
| cs                 | cs             |
| csb                | csb            |
| cv                 | cv             |
| cy                 | cy             |
| da                 | da             |
| de                 | de             |
| diq                | diq            |
| dv                 | dv             |
| el                 | el             |
| en                 | en             |
| eo                 | eo             |
| es                 | es             |
| et                 | et             |
| eu                 | eu             |
| ext                | ext            |
| fa                 | fa             |
| fi                 | fi             |
| fo                 | fo             |
| fr                 | fr             |
| frr                | frr            |
| fur                | fur            |
| fy                 | fy             |
| ga                 | ga             |
| gan                | gan            |
| gd                 | gd             |
| gl                 | gl             |
| gn                 | gn             |
| gu                 | gu             |
| hak                | hak            |
| he                 | he             |
| hi                 | hi             |
| hr                 | hr             |
| hsb                | hsb            |
| hu                 | hu             |
| hy                 | hy             |
| ia                 | ia             |
| id                 | id             |
| ig                 | ig             |
| ilo                | ilo            |
| io                 | io             |
| is                 | is             |
| it                 | it             |
| ja                 | ja             |
| jbo                | jbo            |
| jv                 | jv             |
| ka                 | ka             |
| kk                 | kk             |
| km                 | km             |
| kn                 | kn             |
| ko                 | ko             |
| ksh                | ksh            |
| ku                 | ku             |
| ky                 | ky             |
| la                 | la             |
| lb                 | lb             |
| li                 | li             |
| lij                | lij            |
| lmo                | lmo            |
| ln                 | ln             |
| lt                 | lt             |
| lv                 | lv             |
| mg                 | mg             |
| mhr                | mhr            |
| mi                 | mi             |
| min                | min            |
| mk                 | mk             |
| ml                 | ml             |
| mn                 | mn             |
| mr                 | mr             |
| ms                 | ms             |
| mt                 | mt             |
| mwl                | mwl            |
| my                 | my             |
| mzn                | mzn            |
| nap                | nap            |
| nds                | nds            |
| ne                 | ne             |
| nl                 | nl             |
| nn                 | nn             |
| no                 | no             |
| nov                | nov            |
| oc                 | oc             |
| or                 | or             |
| os                 | os             |
| other-bat-smg      | sgs            |
| other-be-x-old     | be-tarask      |
| other-cbk-zam      | cbk            |
| other-eml          | eml            |
| other-fiu-vro      | vro            |
| other-map-bms      | jv-x-bms       |
| other-simple       | en-basiceng    |
| other-zh-classical | lzh            |
| other-zh-min-nan   | nan            |
| other-zh-yue       | yue            |
| pa                 | pa             |
| pdc                | pdc            |
| pl                 | pl             |
| pms                | pms            |
| pnb                | pnb            |
| ps                 | ps             |
| pt                 | pt             |
| qu                 | qu             |
| rm                 | rm             |
| ro                 | ro             |
| ru                 | ru             |
| rw                 | rw             |
| sa                 | sa             |
| sah                | sah            |
| scn                | scn            |
| sco                | sco            |
| sd                 | sd             |
| sh                 | sh             |
| si                 | si             |
| sk                 | sk             |
| sl                 | sl             |
| so                 | so             |
| sq                 | sq             |
| sr                 | sr             |
| su                 | su             |
| sv                 | sv             |
| sw                 | sw             |
| szl                | szl            |
| ta                 | ta             |
| te                 | te             |
| tg                 | tg             |
| th                 | th             |
| tk                 | tk             |
| tl                 | tl             |
| tr                 | tr             |
| tt                 | tt             |
| ug                 | ug             |
| uk                 | uk             |
| ur                 | ur             |
| uz                 | uz             |
| vec                | vec            |
| vep                | vep            |
| vi                 | vi             |
| vls                | vls            |
| vo                 | vo             |
| wa                 | wa             |
| war                | war            |
| wuu                | wuu            |
| xmf                | xmf            |
| yi                 | yi             |
| yo                 | yo             |
| zea                | zea            |
| zh                 | zh             |

## Dataset Structure

### Data Instances

This is an example in the "train" split of the "af" (Afrikaans language) configuration subset:
```python
{
  'tokens': ['Sy', 'ander', 'seun', ',', 'Swjatopolk', ',', 'was', 'die', 'resultaat', 'van', '’n', 'buite-egtelike', 'verhouding', '.'],
  'ner_tags': [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  'langs': ['af', 'af', 'af', 'af', 'af', 'af', 'af', 'af', 'af', 'af', 'af', 'af', 'af', 'af'],
  'spans': ['PER: Swjatopolk']
}
```

### Data Fields

- `tokens`: a `list` of `string` features.
- `langs`: a `list` of `string` features that correspond to the language of each token.
- `ner_tags`: a `list` of classification labels, with possible values including `O` (0), `B-PER` (1), `I-PER` (2), `B-ORG` (3), `I-ORG` (4), `B-LOC` (5), `I-LOC` (6).
- `spans`: a `list` of `string` features, that is the list of named entities in the input text formatted as ``<TAG>: <mention>``

### Data Splits

For each configuration subset, the data is split into "train", "validation" and "test" sets, each containing the
following number of examples:

|              |   Train |   Validation |   Test |
|:-------------|--------:|-------------:|-------:|
| ace          |     100 |          100 |    100 |
| af           |    5000 |         1000 |   1000 |
| als          |     100 |          100 |    100 |
| am           |     100 |          100 |    100 |
| an           |    1000 |         1000 |   1000 |
| ang          |     100 |          100 |    100 |
| ar           |   20000 |        10000 |  10000 |
| arc          |     100 |          100 |    100 |
| arz          |     100 |          100 |    100 |
| as           |     100 |          100 |    100 |
| ast          |    1000 |         1000 |   1000 |
| ay           |     100 |          100 |    100 |
| az           |   10000 |         1000 |   1000 |
| ba           |     100 |          100 |    100 |
| bar          |     100 |          100 |    100 |
| bat-smg      |     100 |          100 |    100 |
| be           |   15000 |         1000 |   1000 |
| be-x-old     |    5000 |         1000 |   1000 |
| bg           |   20000 |        10000 |  10000 |
| bh           |     100 |          100 |    100 |
| bn           |   10000 |         1000 |   1000 |
| bo           |     100 |          100 |    100 |
| br           |    1000 |         1000 |   1000 |
| bs           |   15000 |         1000 |   1000 |
| ca           |   20000 |        10000 |  10000 |
| cbk-zam      |     100 |          100 |    100 |
| cdo          |     100 |          100 |    100 |
| ce           |     100 |          100 |    100 |
| ceb          |     100 |          100 |    100 |
| ckb          |    1000 |         1000 |   1000 |
| co           |     100 |          100 |    100 |
| crh          |     100 |          100 |    100 |
| cs           |   20000 |        10000 |  10000 |
| csb          |     100 |          100 |    100 |
| cv           |     100 |          100 |    100 |
| cy           |   10000 |         1000 |   1000 |
| da           |   20000 |        10000 |  10000 |
| de           |   20000 |        10000 |  10000 |
| diq          |     100 |          100 |    100 |
| dv           |     100 |          100 |    100 |
| el           |   20000 |        10000 |  10000 |
| eml          |     100 |          100 |    100 |
| en           |   20000 |        10000 |  10000 |
| eo           |   15000 |        10000 |  10000 |
| es           |   20000 |        10000 |  10000 |
| et           |   15000 |        10000 |  10000 |
| eu           |   10000 |        10000 |  10000 |
| ext          |     100 |          100 |    100 |
| fa           |   20000 |        10000 |  10000 |
| fi           |   20000 |        10000 |  10000 |
| fiu-vro      |     100 |          100 |    100 |
| fo           |     100 |          100 |    100 |
| fr           |   20000 |        10000 |  10000 |
| frr          |     100 |          100 |    100 |
| fur          |     100 |          100 |    100 |
| fy           |    1000 |         1000 |   1000 |
| ga           |    1000 |         1000 |   1000 |
| gan          |     100 |          100 |    100 |
| gd           |     100 |          100 |    100 |
| gl           |   15000 |        10000 |  10000 |
| gn           |     100 |          100 |    100 |
| gu           |     100 |          100 |    100 |
| hak          |     100 |          100 |    100 |
| he           |   20000 |        10000 |  10000 |
| hi           |    5000 |         1000 |   1000 |
| hr           |   20000 |        10000 |  10000 |
| hsb          |     100 |          100 |    100 |
| hu           |   20000 |        10000 |  10000 |
| hy           |   15000 |         1000 |   1000 |
| ia           |     100 |          100 |    100 |
| id           |   20000 |        10000 |  10000 |
| ig           |     100 |          100 |    100 |
| ilo          |     100 |          100 |    100 |
| io           |     100 |          100 |    100 |
| is           |    1000 |         1000 |   1000 |
| it           |   20000 |        10000 |  10000 |
| ja           |   20000 |        10000 |  10000 |
| jbo          |     100 |          100 |    100 |
| jv           |     100 |          100 |    100 |
| ka           |   10000 |        10000 |  10000 |
| kk           |    1000 |         1000 |   1000 |
| km           |     100 |          100 |    100 |
| kn           |     100 |          100 |    100 |
| ko           |   20000 |        10000 |  10000 |
| ksh          |     100 |          100 |    100 |
| ku           |     100 |          100 |    100 |
| ky           |     100 |          100 |    100 |
| la           |    5000 |         1000 |   1000 |
| lb           |    5000 |         1000 |   1000 |
| li           |     100 |          100 |    100 |
| lij          |     100 |          100 |    100 |
| lmo          |     100 |          100 |    100 |
| ln           |     100 |          100 |    100 |
| lt           |   10000 |        10000 |  10000 |
| lv           |   10000 |        10000 |  10000 |
| map-bms      |     100 |          100 |    100 |
| mg           |     100 |          100 |    100 |
| mhr          |     100 |          100 |    100 |
| mi           |     100 |          100 |    100 |
| min          |     100 |          100 |    100 |
| mk           |   10000 |         1000 |   1000 |
| ml           |   10000 |         1000 |   1000 |
| mn           |     100 |          100 |    100 |
| mr           |    5000 |         1000 |   1000 |
| ms           |   20000 |         1000 |   1000 |
| mt           |     100 |          100 |    100 |
| mwl          |     100 |          100 |    100 |
| my           |     100 |          100 |    100 |
| mzn          |     100 |          100 |    100 |
| nap          |     100 |          100 |    100 |
| nds          |     100 |          100 |    100 |
| ne           |     100 |          100 |    100 |
| nl           |   20000 |        10000 |  10000 |
| nn           |   20000 |         1000 |   1000 |
| no           |   20000 |        10000 |  10000 |
| nov          |     100 |          100 |    100 |
| oc           |     100 |          100 |    100 |
| or           |     100 |          100 |    100 |
| os           |     100 |          100 |    100 |
| pa           |     100 |          100 |    100 |
| pdc          |     100 |          100 |    100 |
| pl           |   20000 |        10000 |  10000 |
| pms          |     100 |          100 |    100 |
| pnb          |     100 |          100 |    100 |
| ps           |     100 |          100 |    100 |
| pt           |   20000 |        10000 |  10000 |
| qu           |     100 |          100 |    100 |
| rm           |     100 |          100 |    100 |
| ro           |   20000 |        10000 |  10000 |
| ru           |   20000 |        10000 |  10000 |
| rw           |     100 |          100 |    100 |
| sa           |     100 |          100 |    100 |
| sah          |     100 |          100 |    100 |
| scn          |     100 |          100 |    100 |
| sco          |     100 |          100 |    100 |
| sd           |     100 |          100 |    100 |
| sh           |   20000 |        10000 |  10000 |
| si           |     100 |          100 |    100 |
| simple       |   20000 |         1000 |   1000 |
| sk           |   20000 |        10000 |  10000 |
| sl           |   15000 |        10000 |  10000 |
| so           |     100 |          100 |    100 |
| sq           |    5000 |         1000 |   1000 |
| sr           |   20000 |        10000 |  10000 |
| su           |     100 |          100 |    100 |
| sv           |   20000 |        10000 |  10000 |
| sw           |    1000 |         1000 |   1000 |
| szl          |     100 |          100 |    100 |
| ta           |   15000 |         1000 |   1000 |
| te           |    1000 |         1000 |   1000 |
| tg           |     100 |          100 |    100 |
| th           |   20000 |        10000 |  10000 |
| tk           |     100 |          100 |    100 |
| tl           |   10000 |         1000 |   1000 |
| tr           |   20000 |        10000 |  10000 |
| tt           |    1000 |         1000 |   1000 |
| ug           |     100 |          100 |    100 |
| uk           |   20000 |        10000 |  10000 |
| ur           |   20000 |         1000 |   1000 |
| uz           |    1000 |         1000 |   1000 |
| vec          |     100 |          100 |    100 |
| vep          |     100 |          100 |    100 |
| vi           |   20000 |        10000 |  10000 |
| vls          |     100 |          100 |    100 |
| vo           |     100 |          100 |    100 |
| wa           |     100 |          100 |    100 |
| war          |     100 |          100 |    100 |
| wuu          |     100 |          100 |    100 |
| xmf          |     100 |          100 |    100 |
| yi           |     100 |          100 |    100 |
| yo           |     100 |          100 |    100 |
| zea          |     100 |          100 |    100 |
| zh           |   20000 |        10000 |  10000 |
| zh-classical |     100 |          100 |    100 |
| zh-min-nan   |     100 |          100 |    100 |
| zh-yue       |   20000 |        10000 |  10000 |

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

[More Information Needed]

### Citation Information

The original 282 datasets are associated with this article

```
@inproceedings{pan-etal-2017-cross,
    title = "Cross-lingual Name Tagging and Linking for 282 Languages",
    author = "Pan, Xiaoman  and
      Zhang, Boliang  and
      May, Jonathan  and
      Nothman, Joel  and
      Knight, Kevin  and
      Ji, Heng",
    booktitle = "Proceedings of the 55th Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)",
    month = jul,
    year = "2017",
    address = "Vancouver, Canada",
    publisher = "Association for Computational Linguistics",
    url = "https://www.aclweb.org/anthology/P17-1178",
    doi = "10.18653/v1/P17-1178",
    pages = "1946--1958",
    abstract = "The ambitious goal of this work is to develop a cross-lingual name tagging and linking framework for 282 languages that exist in Wikipedia. Given a document in any of these languages, our framework is able to identify name mentions, assign a coarse-grained or fine-grained type to each mention, and link it to an English Knowledge Base (KB) if it is linkable. We achieve this goal by performing a series of new KB mining methods: generating {``}silver-standard{''} annotations by transferring annotations from English to other languages through cross-lingual links and KB properties, refining annotations through self-training and topic selection, deriving language-specific morphology features from anchor links, and mining word translation pairs from cross-lingual links. Both name tagging and linking results for 282 languages are promising on Wikipedia data and on-Wikipedia data.",
}
```

while the 176 languages supported in this version are associated with the following article

```
@inproceedings{rahimi-etal-2019-massively,
    title = "Massively Multilingual Transfer for {NER}",
    author = "Rahimi, Afshin  and
      Li, Yuan  and
      Cohn, Trevor",
    booktitle = "Proceedings of the 57th Annual Meeting of the Association for Computational Linguistics",
    month = jul,
    year = "2019",
    address = "Florence, Italy",
    publisher = "Association for Computational Linguistics",
    url = "https://www.aclweb.org/anthology/P19-1015",
    pages = "151--164",
}
```


### Contributions

Thanks to [@lewtun](https://github.com/lewtun) and [@rabeehk](https://github.com/rabeehk) for adding this dataset.