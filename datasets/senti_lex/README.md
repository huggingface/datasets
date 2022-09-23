---
annotations_creators:
- expert-generated
language_creators:
- expert-generated
language:
- af
- an
- ar
- az
- be
- bg
- bn
- br
- bs
- ca
- cs
- cy
- da
- de
- el
- eo
- es
- et
- eu
- fa
- fi
- fo
- fr
- fy
- ga
- gd
- gl
- gu
- he
- hi
- hr
- ht
- hu
- hy
- ia
- id
- io
- is
- it
- ja
- ka
- km
- kn
- ko
- ku
- ky
- la
- lb
- lt
- lv
- mk
- mr
- ms
- mt
- nl
- nn
- 'no'
- pl
- pt
- rm
- ro
- ru
- sk
- sl
- sq
- sr
- sv
- sw
- ta
- te
- th
- tk
- tl
- tr
- uk
- ur
- uz
- vi
- vo
- wa
- yi
- zh
- zhw
license:
- gpl-3.0
multilinguality:
- multilingual
size_categories:
- 1K<n<10K
- n<1K
source_datasets:
- original
task_categories:
- text-classification
task_ids:
- sentiment-classification
paperswithcode_id: null
pretty_name: SentiWS
configs:
- 'no'
- af
- an
- ar
- az
- be
- bg
- bn
- br
- bs
- ca
- cs
- cy
- da
- de
- el
- eo
- es
- et
- eu
- fa
- fi
- fo
- fr
- fy
- ga
- gd
- gl
- gu
- he
- hi
- hr
- ht
- hu
- hy
- ia
- id
- io
- is
- it
- ja
- ka
- km
- kn
- ko
- ku
- ky
- la
- lb
- lt
- lv
- mk
- mr
- ms
- mt
- nl
- nn
- pl
- pt
- rm
- ro
- ru
- sk
- sl
- sq
- sr
- sv
- sw
- ta
- te
- th
- tk
- tl
- tr
- uk
- ur
- uz
- vi
- vo
- wa
- yi
- zh
- zhw
dataset_info:
- config_name: af
  features:
  - name: word
    dtype: string
  - name: sentiment
    dtype:
      class_label:
        names:
          0: negative
          1: positive
  splits:
  - name: train
    num_bytes: 45954
    num_examples: 2299
  download_size: 0
  dataset_size: 45954
- config_name: an
  features:
  - name: word
    dtype: string
  - name: sentiment
    dtype:
      class_label:
        names:
          0: negative
          1: positive
  splits:
  - name: train
    num_bytes: 1832
    num_examples: 97
  download_size: 0
  dataset_size: 1832
- config_name: ar
  features:
  - name: word
    dtype: string
  - name: sentiment
    dtype:
      class_label:
        names:
          0: negative
          1: positive
  splits:
  - name: train
    num_bytes: 58707
    num_examples: 2794
  download_size: 0
  dataset_size: 58707
- config_name: az
  features:
  - name: word
    dtype: string
  - name: sentiment
    dtype:
      class_label:
        names:
          0: negative
          1: positive
  splits:
  - name: train
    num_bytes: 40044
    num_examples: 1979
  download_size: 0
  dataset_size: 40044
- config_name: be
  features:
  - name: word
    dtype: string
  - name: sentiment
    dtype:
      class_label:
        names:
          0: negative
          1: positive
  splits:
  - name: train
    num_bytes: 41915
    num_examples: 1526
  download_size: 0
  dataset_size: 41915
- config_name: bg
  features:
  - name: word
    dtype: string
  - name: sentiment
    dtype:
      class_label:
        names:
          0: negative
          1: positive
  splits:
  - name: train
    num_bytes: 78779
    num_examples: 2847
  download_size: 0
  dataset_size: 78779
- config_name: bn
  features:
  - name: word
    dtype: string
  - name: sentiment
    dtype:
      class_label:
        names:
          0: negative
          1: positive
  splits:
  - name: train
    num_bytes: 70928
    num_examples: 2393
  download_size: 0
  dataset_size: 70928
- config_name: br
  features:
  - name: word
    dtype: string
  - name: sentiment
    dtype:
      class_label:
        names:
          0: negative
          1: positive
  splits:
  - name: train
    num_bytes: 3234
    num_examples: 184
  download_size: 0
  dataset_size: 3234
- config_name: bs
  features:
  - name: word
    dtype: string
  - name: sentiment
    dtype:
      class_label:
        names:
          0: negative
          1: positive
  splits:
  - name: train
    num_bytes: 39890
    num_examples: 2020
  download_size: 0
  dataset_size: 39890
- config_name: ca
  features:
  - name: word
    dtype: string
  - name: sentiment
    dtype:
      class_label:
        names:
          0: negative
          1: positive
  splits:
  - name: train
    num_bytes: 64512
    num_examples: 3204
  download_size: 0
  dataset_size: 64512
- config_name: cs
  features:
  - name: word
    dtype: string
  - name: sentiment
    dtype:
      class_label:
        names:
          0: negative
          1: positive
  splits:
  - name: train
    num_bytes: 53194
    num_examples: 2599
  download_size: 0
  dataset_size: 53194
- config_name: cy
  features:
  - name: word
    dtype: string
  - name: sentiment
    dtype:
      class_label:
        names:
          0: negative
          1: positive
  splits:
  - name: train
    num_bytes: 31546
    num_examples: 1647
  download_size: 0
  dataset_size: 31546
- config_name: da
  features:
  - name: word
    dtype: string
  - name: sentiment
    dtype:
      class_label:
        names:
          0: negative
          1: positive
  splits:
  - name: train
    num_bytes: 66756
    num_examples: 3340
  download_size: 0
  dataset_size: 66756
- config_name: de
  features:
  - name: word
    dtype: string
  - name: sentiment
    dtype:
      class_label:
        names:
          0: negative
          1: positive
  splits:
  - name: train
    num_bytes: 82223
    num_examples: 3974
  download_size: 0
  dataset_size: 82223
- config_name: el
  features:
  - name: word
    dtype: string
  - name: sentiment
    dtype:
      class_label:
        names:
          0: negative
          1: positive
  splits:
  - name: train
    num_bytes: 76281
    num_examples: 2703
  download_size: 0
  dataset_size: 76281
- config_name: eo
  features:
  - name: word
    dtype: string
  - name: sentiment
    dtype:
      class_label:
        names:
          0: negative
          1: positive
  splits:
  - name: train
    num_bytes: 50271
    num_examples: 2604
  download_size: 0
  dataset_size: 50271
- config_name: es
  features:
  - name: word
    dtype: string
  - name: sentiment
    dtype:
      class_label:
        names:
          0: negative
          1: positive
  splits:
  - name: train
    num_bytes: 87157
    num_examples: 4275
  download_size: 0
  dataset_size: 87157
- config_name: et
  features:
  - name: word
    dtype: string
  - name: sentiment
    dtype:
      class_label:
        names:
          0: negative
          1: positive
  splits:
  - name: train
    num_bytes: 41964
    num_examples: 2105
  download_size: 0
  dataset_size: 41964
- config_name: eu
  features:
  - name: word
    dtype: string
  - name: sentiment
    dtype:
      class_label:
        names:
          0: negative
          1: positive
  splits:
  - name: train
    num_bytes: 39641
    num_examples: 1979
  download_size: 0
  dataset_size: 39641
- config_name: fa
  features:
  - name: word
    dtype: string
  - name: sentiment
    dtype:
      class_label:
        names:
          0: negative
          1: positive
  splits:
  - name: train
    num_bytes: 53399
    num_examples: 2477
  download_size: 0
  dataset_size: 53399
- config_name: fi
  features:
  - name: word
    dtype: string
  - name: sentiment
    dtype:
      class_label:
        names:
          0: negative
          1: positive
  splits:
  - name: train
    num_bytes: 68294
    num_examples: 3295
  download_size: 0
  dataset_size: 68294
- config_name: fo
  features:
  - name: word
    dtype: string
  - name: sentiment
    dtype:
      class_label:
        names:
          0: negative
          1: positive
  splits:
  - name: train
    num_bytes: 2213
    num_examples: 123
  download_size: 0
  dataset_size: 2213
- config_name: fr
  features:
  - name: word
    dtype: string
  - name: sentiment
    dtype:
      class_label:
        names:
          0: negative
          1: positive
  splits:
  - name: train
    num_bytes: 94832
    num_examples: 4653
  download_size: 0
  dataset_size: 94832
- config_name: fy
  features:
  - name: word
    dtype: string
  - name: sentiment
    dtype:
      class_label:
        names:
          0: negative
          1: positive
  splits:
  - name: train
    num_bytes: 3916
    num_examples: 224
  download_size: 0
  dataset_size: 3916
- config_name: ga
  features:
  - name: word
    dtype: string
  - name: sentiment
    dtype:
      class_label:
        names:
          0: negative
          1: positive
  splits:
  - name: train
    num_bytes: 21209
    num_examples: 1073
  download_size: 0
  dataset_size: 21209
- config_name: gd
  features:
  - name: word
    dtype: string
  - name: sentiment
    dtype:
      class_label:
        names:
          0: negative
          1: positive
  splits:
  - name: train
    num_bytes: 6441
    num_examples: 345
  download_size: 0
  dataset_size: 6441
- config_name: gl
  features:
  - name: word
    dtype: string
  - name: sentiment
    dtype:
      class_label:
        names:
          0: negative
          1: positive
  splits:
  - name: train
    num_bytes: 55279
    num_examples: 2714
  download_size: 0
  dataset_size: 55279
- config_name: gu
  features:
  - name: word
    dtype: string
  - name: sentiment
    dtype:
      class_label:
        names:
          0: negative
          1: positive
  splits:
  - name: train
    num_bytes: 60025
    num_examples: 2145
  download_size: 0
  dataset_size: 60025
- config_name: he
  features:
  - name: word
    dtype: string
  - name: sentiment
    dtype:
      class_label:
        names:
          0: negative
          1: positive
  splits:
  - name: train
    num_bytes: 54706
    num_examples: 2533
  download_size: 0
  dataset_size: 54706
- config_name: hi
  features:
  - name: word
    dtype: string
  - name: sentiment
    dtype:
      class_label:
        names:
          0: negative
          1: positive
  splits:
  - name: train
    num_bytes: 103800
    num_examples: 3640
  download_size: 0
  dataset_size: 103800
- config_name: hr
  features:
  - name: word
    dtype: string
  - name: sentiment
    dtype:
      class_label:
        names:
          0: negative
          1: positive
  splits:
  - name: train
    num_bytes: 43775
    num_examples: 2208
  download_size: 0
  dataset_size: 43775
- config_name: ht
  features:
  - name: word
    dtype: string
  - name: sentiment
    dtype:
      class_label:
        names:
          0: negative
          1: positive
  splits:
  - name: train
    num_bytes: 8261
    num_examples: 472
  download_size: 0
  dataset_size: 8261
- config_name: hu
  features:
  - name: word
    dtype: string
  - name: sentiment
    dtype:
      class_label:
        names:
          0: negative
          1: positive
  splits:
  - name: train
    num_bytes: 74203
    num_examples: 3522
  download_size: 0
  dataset_size: 74203
- config_name: hy
  features:
  - name: word
    dtype: string
  - name: sentiment
    dtype:
      class_label:
        names:
          0: negative
          1: positive
  splits:
  - name: train
    num_bytes: 44593
    num_examples: 1657
  download_size: 0
  dataset_size: 44593
- config_name: ia
  features:
  - name: word
    dtype: string
  - name: sentiment
    dtype:
      class_label:
        names:
          0: negative
          1: positive
  splits:
  - name: train
    num_bytes: 6401
    num_examples: 326
  download_size: 0
  dataset_size: 6401
- config_name: id
  features:
  - name: word
    dtype: string
  - name: sentiment
    dtype:
      class_label:
        names:
          0: negative
          1: positive
  splits:
  - name: train
    num_bytes: 56879
    num_examples: 2900
  download_size: 0
  dataset_size: 56879
- config_name: io
  features:
  - name: word
    dtype: string
  - name: sentiment
    dtype:
      class_label:
        names:
          0: negative
          1: positive
  splits:
  - name: train
    num_bytes: 3348
    num_examples: 183
  download_size: 0
  dataset_size: 3348
- config_name: is
  features:
  - name: word
    dtype: string
  - name: sentiment
    dtype:
      class_label:
        names:
          0: negative
          1: positive
  splits:
  - name: train
    num_bytes: 34565
    num_examples: 1770
  download_size: 0
  dataset_size: 34565
- config_name: it
  features:
  - name: word
    dtype: string
  - name: sentiment
    dtype:
      class_label:
        names:
          0: negative
          1: positive
  splits:
  - name: train
    num_bytes: 92165
    num_examples: 4491
  download_size: 0
  dataset_size: 92165
- config_name: ja
  features:
  - name: word
    dtype: string
  - name: sentiment
    dtype:
      class_label:
        names:
          0: negative
          1: positive
  splits:
  - name: train
    num_bytes: 21770
    num_examples: 1017
  download_size: 0
  dataset_size: 21770
- config_name: ka
  features:
  - name: word
    dtype: string
  - name: sentiment
    dtype:
      class_label:
        names:
          0: negative
          1: positive
  splits:
  - name: train
    num_bytes: 81286
    num_examples: 2202
  download_size: 0
  dataset_size: 81286
- config_name: km
  features:
  - name: word
    dtype: string
  - name: sentiment
    dtype:
      class_label:
        names:
          0: negative
          1: positive
  splits:
  - name: train
    num_bytes: 23133
    num_examples: 956
  download_size: 0
  dataset_size: 23133
- config_name: kn
  features:
  - name: word
    dtype: string
  - name: sentiment
    dtype:
      class_label:
        names:
          0: negative
          1: positive
  splits:
  - name: train
    num_bytes: 70449
    num_examples: 2173
  download_size: 0
  dataset_size: 70449
- config_name: ko
  features:
  - name: word
    dtype: string
  - name: sentiment
    dtype:
      class_label:
        names:
          0: negative
          1: positive
  splits:
  - name: train
    num_bytes: 41716
    num_examples: 2118
  download_size: 0
  dataset_size: 41716
- config_name: ku
  features:
  - name: word
    dtype: string
  - name: sentiment
    dtype:
      class_label:
        names:
          0: negative
          1: positive
  splits:
  - name: train
    num_bytes: 2510
    num_examples: 145
  download_size: 0
  dataset_size: 2510
- config_name: ky
  features:
  - name: word
    dtype: string
  - name: sentiment
    dtype:
      class_label:
        names:
          0: negative
          1: positive
  splits:
  - name: train
    num_bytes: 5746
    num_examples: 246
  download_size: 0
  dataset_size: 5746
- config_name: la
  features:
  - name: word
    dtype: string
  - name: sentiment
    dtype:
      class_label:
        names:
          0: negative
          1: positive
  splits:
  - name: train
    num_bytes: 39092
    num_examples: 2033
  download_size: 0
  dataset_size: 39092
- config_name: lb
  features:
  - name: word
    dtype: string
  - name: sentiment
    dtype:
      class_label:
        names:
          0: negative
          1: positive
  splits:
  - name: train
    num_bytes: 4150
    num_examples: 224
  download_size: 0
  dataset_size: 4150
- config_name: lt
  features:
  - name: word
    dtype: string
  - name: sentiment
    dtype:
      class_label:
        names:
          0: negative
          1: positive
  splits:
  - name: train
    num_bytes: 45274
    num_examples: 2190
  download_size: 0
  dataset_size: 45274
- config_name: lv
  features:
  - name: word
    dtype: string
  - name: sentiment
    dtype:
      class_label:
        names:
          0: negative
          1: positive
  splits:
  - name: train
    num_bytes: 39879
    num_examples: 1938
  download_size: 0
  dataset_size: 39879
- config_name: mk
  features:
  - name: word
    dtype: string
  - name: sentiment
    dtype:
      class_label:
        names:
          0: negative
          1: positive
  splits:
  - name: train
    num_bytes: 81619
    num_examples: 2965
  download_size: 0
  dataset_size: 81619
- config_name: mr
  features:
  - name: word
    dtype: string
  - name: sentiment
    dtype:
      class_label:
        names:
          0: negative
          1: positive
  splits:
  - name: train
    num_bytes: 48601
    num_examples: 1825
  download_size: 0
  dataset_size: 48601
- config_name: ms
  features:
  - name: word
    dtype: string
  - name: sentiment
    dtype:
      class_label:
        names:
          0: negative
          1: positive
  splits:
  - name: train
    num_bytes: 57265
    num_examples: 2934
  download_size: 0
  dataset_size: 57265
- config_name: mt
  features:
  - name: word
    dtype: string
  - name: sentiment
    dtype:
      class_label:
        names:
          0: negative
          1: positive
  splits:
  - name: train
    num_bytes: 16913
    num_examples: 863
  download_size: 0
  dataset_size: 16913
- config_name: nl
  features:
  - name: word
    dtype: string
  - name: sentiment
    dtype:
      class_label:
        names:
          0: negative
          1: positive
  splits:
  - name: train
    num_bytes: 80335
    num_examples: 3976
  download_size: 0
  dataset_size: 80335
- config_name: nn
  features:
  - name: word
    dtype: string
  - name: sentiment
    dtype:
      class_label:
        names:
          0: negative
          1: positive
  splits:
  - name: train
    num_bytes: 35835
    num_examples: 1894
  download_size: 0
  dataset_size: 35835
- config_name: 'no'
  features:
  - name: word
    dtype: string
  - name: sentiment
    dtype:
      class_label:
        names:
          0: negative
          1: positive
  splits:
  - name: train
    num_bytes: 61160
    num_examples: 3089
  download_size: 0
  dataset_size: 61160
- config_name: pl
  features:
  - name: word
    dtype: string
  - name: sentiment
    dtype:
      class_label:
        names:
          0: negative
          1: positive
  splits:
  - name: train
    num_bytes: 73213
    num_examples: 3533
  download_size: 0
  dataset_size: 73213
- config_name: pt
  features:
  - name: word
    dtype: string
  - name: sentiment
    dtype:
      class_label:
        names:
          0: negative
          1: positive
  splits:
  - name: train
    num_bytes: 80618
    num_examples: 3953
  download_size: 0
  dataset_size: 80618
- config_name: rm
  features:
  - name: word
    dtype: string
  - name: sentiment
    dtype:
      class_label:
        names:
          0: negative
          1: positive
  splits:
  - name: train
    num_bytes: 2060
    num_examples: 116
  download_size: 0
  dataset_size: 2060
- config_name: ro
  features:
  - name: word
    dtype: string
  - name: sentiment
    dtype:
      class_label:
        names:
          0: negative
          1: positive
  splits:
  - name: train
    num_bytes: 66071
    num_examples: 3329
  download_size: 0
  dataset_size: 66071
- config_name: ru
  features:
  - name: word
    dtype: string
  - name: sentiment
    dtype:
      class_label:
        names:
          0: negative
          1: positive
  splits:
  - name: train
    num_bytes: 82966
    num_examples: 2914
  download_size: 0
  dataset_size: 82966
- config_name: sk
  features:
  - name: word
    dtype: string
  - name: sentiment
    dtype:
      class_label:
        names:
          0: negative
          1: positive
  splits:
  - name: train
    num_bytes: 49751
    num_examples: 2428
  download_size: 0
  dataset_size: 49751
- config_name: sl
  features:
  - name: word
    dtype: string
  - name: sentiment
    dtype:
      class_label:
        names:
          0: negative
          1: positive
  splits:
  - name: train
    num_bytes: 44430
    num_examples: 2244
  download_size: 0
  dataset_size: 44430
- config_name: sq
  features:
  - name: word
    dtype: string
  - name: sentiment
    dtype:
      class_label:
        names:
          0: negative
          1: positive
  splits:
  - name: train
    num_bytes: 40484
    num_examples: 2076
  download_size: 0
  dataset_size: 40484
- config_name: sr
  features:
  - name: word
    dtype: string
  - name: sentiment
    dtype:
      class_label:
        names:
          0: negative
          1: positive
  splits:
  - name: train
    num_bytes: 53257
    num_examples: 2034
  download_size: 0
  dataset_size: 53257
- config_name: sv
  features:
  - name: word
    dtype: string
  - name: sentiment
    dtype:
      class_label:
        names:
          0: negative
          1: positive
  splits:
  - name: train
    num_bytes: 73939
    num_examples: 3722
  download_size: 0
  dataset_size: 73939
- config_name: sw
  features:
  - name: word
    dtype: string
  - name: sentiment
    dtype:
      class_label:
        names:
          0: negative
          1: positive
  splits:
  - name: train
    num_bytes: 24962
    num_examples: 1314
  download_size: 0
  dataset_size: 24962
- config_name: ta
  features:
  - name: word
    dtype: string
  - name: sentiment
    dtype:
      class_label:
        names:
          0: negative
          1: positive
  splits:
  - name: train
    num_bytes: 71071
    num_examples: 2057
  download_size: 0
  dataset_size: 71071
- config_name: te
  features:
  - name: word
    dtype: string
  - name: sentiment
    dtype:
      class_label:
        names:
          0: negative
          1: positive
  splits:
  - name: train
    num_bytes: 77306
    num_examples: 2523
  download_size: 0
  dataset_size: 77306
- config_name: th
  features:
  - name: word
    dtype: string
  - name: sentiment
    dtype:
      class_label:
        names:
          0: negative
          1: positive
  splits:
  - name: train
    num_bytes: 34209
    num_examples: 1279
  download_size: 0
  dataset_size: 34209
- config_name: tk
  features:
  - name: word
    dtype: string
  - name: sentiment
    dtype:
      class_label:
        names:
          0: negative
          1: positive
  splits:
  - name: train
    num_bytes: 1425
    num_examples: 78
  download_size: 0
  dataset_size: 1425
- config_name: tl
  features:
  - name: word
    dtype: string
  - name: sentiment
    dtype:
      class_label:
        names:
          0: negative
          1: positive
  splits:
  - name: train
    num_bytes: 36190
    num_examples: 1858
  download_size: 0
  dataset_size: 36190
- config_name: tr
  features:
  - name: word
    dtype: string
  - name: sentiment
    dtype:
      class_label:
        names:
          0: negative
          1: positive
  splits:
  - name: train
    num_bytes: 49295
    num_examples: 2500
  download_size: 0
  dataset_size: 49295
- config_name: uk
  features:
  - name: word
    dtype: string
  - name: sentiment
    dtype:
      class_label:
        names:
          0: negative
          1: positive
  splits:
  - name: train
    num_bytes: 80226
    num_examples: 2827
  download_size: 0
  dataset_size: 80226
- config_name: ur
  features:
  - name: word
    dtype: string
  - name: sentiment
    dtype:
      class_label:
        names:
          0: negative
          1: positive
  splits:
  - name: train
    num_bytes: 28469
    num_examples: 1347
  download_size: 0
  dataset_size: 28469
- config_name: uz
  features:
  - name: word
    dtype: string
  - name: sentiment
    dtype:
      class_label:
        names:
          0: negative
          1: positive
  splits:
  - name: train
    num_bytes: 1944
    num_examples: 111
  download_size: 0
  dataset_size: 1944
- config_name: vi
  features:
  - name: word
    dtype: string
  - name: sentiment
    dtype:
      class_label:
        names:
          0: negative
          1: positive
  splits:
  - name: train
    num_bytes: 18100
    num_examples: 1016
  download_size: 0
  dataset_size: 18100
- config_name: vo
  features:
  - name: word
    dtype: string
  - name: sentiment
    dtype:
      class_label:
        names:
          0: negative
          1: positive
  splits:
  - name: train
    num_bytes: 775
    num_examples: 43
  download_size: 0
  dataset_size: 775
- config_name: wa
  features:
  - name: word
    dtype: string
  - name: sentiment
    dtype:
      class_label:
        names:
          0: negative
          1: positive
  splits:
  - name: train
    num_bytes: 3450
    num_examples: 193
  download_size: 0
  dataset_size: 3450
- config_name: yi
  features:
  - name: word
    dtype: string
  - name: sentiment
    dtype:
      class_label:
        names:
          0: negative
          1: positive
  splits:
  - name: train
    num_bytes: 9001
    num_examples: 395
  download_size: 0
  dataset_size: 9001
- config_name: zh
  features:
  - name: word
    dtype: string
  - name: sentiment
    dtype:
      class_label:
        names:
          0: negative
          1: positive
  splits:
  - name: train
    num_bytes: 33025
    num_examples: 1879
  download_size: 0
  dataset_size: 33025
- config_name: zhw
  features:
  - name: word
    dtype: string
  - name: sentiment
    dtype:
      class_label:
        names:
          0: negative
          1: positive
  splits:
  - name: train
    num_bytes: 67675
    num_examples: 3828
  download_size: 0
  dataset_size: 67675
---

# Dataset Card for SentiWS

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

- **Homepage:** https://sites.google.com/site/datascienceslab/projects/multilingualsentiment
- **Repository:** https://www.kaggle.com/rtatman/sentiment-lexicons-for-81-languages
- **Paper:** [Needs More Information]
- **Leaderboard:** [Needs More Information]
- **Point of Contact:** [Needs More Information]

### Dataset Summary

This dataset add sentiment lexicons for 81 languages generated via graph propagation based on a knowledge graph--a graphical representation of real-world entities and the links between them

### Supported Tasks and Leaderboards

Sentiment-Classification

### Languages

Afrikaans
Aragonese
Arabic
Azerbaijani
Belarusian
Bulgarian
Bengali
Breton
Bosnian
Catalan; Valencian
Czech
Welsh
Danish
German
Greek, Modern
Esperanto
Spanish; Castilian
Estonian
Basque
Persian
Finnish
Faroese
French
Western Frisian
Irish
Scottish Gaelic; Gaelic
Galician
Gujarati
Hebrew (modern)
Hindi
Croatian
Haitian; Haitian Creole
Hungarian
Armenian
Interlingua
Indonesian
Ido
Icelandic
Italian
Japanese
Georgian
Khmer
Kannada
Korean
Kurdish
Kirghiz, Kyrgyz
Latin
Luxembourgish, Letzeburgesch
Lithuanian
Latvian
Macedonian
Marathi (Marāṭhī)
Malay
Maltese
Dutch
Norwegian Nynorsk
Norwegian
Polish
Portuguese
Romansh
Romanian, Moldavian, Moldovan
Russian
Slovak
Slovene
Albanian
Serbian
Swedish
Swahili
Tamil
Telugu
Thai
Turkmen
Tagalog
Turkish
Ukrainian
Urdu
Uzbek
Vietnamese
Volapük
Walloon
Yiddish
Chinese
Zhoa

## Dataset Structure

### Data Instances

```
{
"word":"die",
"sentiment": 0, #"negative"
}
``` 

### Data Fields

- word: one word as a string,
- sentiment-score: the sentiment classification of the word as a string either negative (0) or positive (1)

### Data Splits

[Needs More Information]

## Dataset Creation

### Curation Rationale

[Needs More Information]

### Source Data

#### Initial Data Collection and Normalization

[Needs More Information]

#### Who are the source language producers?

[Needs More Information]

### Annotations

#### Annotation process

[Needs More Information]

#### Who are the annotators?

[Needs More Information]

### Personal and Sensitive Information

[Needs More Information]

## Considerations for Using the Data

### Social Impact of Dataset

[Needs More Information]

### Discussion of Biases

[Needs More Information]

### Other Known Limitations

[Needs More Information]

## Additional Information

### Dataset Curators

[Needs More Information]

### Licensing Information

GNU General Public License v3

### Citation Information
@inproceedings{inproceedings,
author = {Chen, Yanqing and Skiena, Steven},
year = {2014},
month = {06},
pages = {383-389},
title = {Building Sentiment Lexicons for All Major Languages},
volume = {2},
journal = {52nd Annual Meeting of the Association for Computational Linguistics, ACL 2014 - Proceedings of the Conference},
doi = {10.3115/v1/P14-2063}
}
### Contributions

Thanks to [@KMFODA](https://github.com/KMFODA) for adding this dataset.