---
pretty_name: Opus100
task_categories:
- text-generation
- fill-mask
multilinguality:
- translation
task_ids:
- language-modeling
- masked-language-modeling
language:
- af
- am
- an
- ar
- as
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
- dz
- el
- en
- eo
- es
- et
- eu
- fa
- fi
- fr
- fy
- ga
- gd
- gl
- gu
- ha
- he
- hi
- hr
- hu
- hy
- id
- ig
- is
- it
- ja
- ka
- kk
- km
- kn
- ko
- ku
- ky
- li
- lt
- lv
- mg
- mk
- ml
- mn
- mr
- ms
- mt
- my
- nb
- ne
- nl
- nn
- 'no'
- oc
- or
- pa
- pl
- ps
- pt
- ro
- ru
- rw
- se
- sh
- si
- sk
- sl
- sq
- sr
- sv
- ta
- te
- tg
- th
- tk
- tr
- tt
- ug
- uk
- ur
- uz
- vi
- wa
- xh
- yi
- yo
- zh
- zu
annotations_creators:
- no-annotation
language_creators:
- found
source_datasets:
- extended
size_categories:
- 100K<n<1M
- 10K<n<100K
- 1K<n<10K
- 1M<n<10M
- n<1K
license:
- unknown
paperswithcode_id: opus-100
configs:
- af-en
- am-en
- an-en
- ar-de
- ar-en
- ar-fr
- ar-nl
- ar-ru
- ar-zh
- as-en
- az-en
- be-en
- bg-en
- bn-en
- br-en
- bs-en
- ca-en
- cs-en
- cy-en
- da-en
- de-en
- de-fr
- de-nl
- de-ru
- de-zh
- dz-en
- el-en
- en-eo
- en-es
- en-et
- en-eu
- en-fa
- en-fi
- en-fr
- en-fy
- en-ga
- en-gd
- en-gl
- en-gu
- en-ha
- en-he
- en-hi
- en-hr
- en-hu
- en-hy
- en-id
- en-ig
- en-is
- en-it
- en-ja
- en-ka
- en-kk
- en-km
- en-kn
- en-ko
- en-ku
- en-ky
- en-li
- en-lt
- en-lv
- en-mg
- en-mk
- en-ml
- en-mn
- en-mr
- en-ms
- en-mt
- en-my
- en-nb
- en-ne
- en-nl
- en-nn
- en-no
- en-oc
- en-or
- en-pa
- en-pl
- en-ps
- en-pt
- en-ro
- en-ru
- en-rw
- en-se
- en-sh
- en-si
- en-sk
- en-sl
- en-sq
- en-sr
- en-sv
- en-ta
- en-te
- en-tg
- en-th
- en-tk
- en-tr
- en-tt
- en-ug
- en-uk
- en-ur
- en-uz
- en-vi
- en-wa
- en-xh
- en-yi
- en-yo
- en-zh
- en-zu
- fr-nl
- fr-ru
- fr-zh
- nl-ru
- nl-zh
- ru-zh
dataset_info:
- config_name: af-en
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - af
        - en
  splits:
  - name: test
    num_bytes: 135916
    num_examples: 2000
  - name: train
    num_bytes: 18726471
    num_examples: 275512
  - name: validation
    num_bytes: 132777
    num_examples: 2000
  download_size: 7505036
  dataset_size: 18995164
- config_name: am-en
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - am
        - en
  splits:
  - name: test
    num_bytes: 588029
    num_examples: 2000
  - name: train
    num_bytes: 21950644
    num_examples: 89027
  - name: validation
    num_bytes: 566077
    num_examples: 2000
  download_size: 7004193
  dataset_size: 23104750
- config_name: an-en
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - an
        - en
  splits:
  - name: train
    num_bytes: 438332
    num_examples: 6961
  download_size: 96148
  dataset_size: 438332
- config_name: ar-en
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - ar
        - en
  splits:
  - name: test
    num_bytes: 331648
    num_examples: 2000
  - name: train
    num_bytes: 152766484
    num_examples: 1000000
  - name: validation
    num_bytes: 2272106
    num_examples: 2000
  download_size: 55286865
  dataset_size: 155370238
- config_name: as-en
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - as
        - en
  splits:
  - name: test
    num_bytes: 261466
    num_examples: 2000
  - name: train
    num_bytes: 15634648
    num_examples: 138479
  - name: validation
    num_bytes: 248139
    num_examples: 2000
  download_size: 4183517
  dataset_size: 16144253
- config_name: az-en
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - az
        - en
  splits:
  - name: test
    num_bytes: 393109
    num_examples: 2000
  - name: train
    num_bytes: 56431259
    num_examples: 262089
  - name: validation
    num_bytes: 407109
    num_examples: 2000
  download_size: 18897341
  dataset_size: 57231477
- config_name: be-en
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - be
        - en
  splits:
  - name: test
    num_bytes: 166858
    num_examples: 2000
  - name: train
    num_bytes: 5298500
    num_examples: 67312
  - name: validation
    num_bytes: 175205
    num_examples: 2000
  download_size: 1906088
  dataset_size: 5640563
- config_name: bg-en
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - bg
        - en
  splits:
  - name: test
    num_bytes: 243751
    num_examples: 2000
  - name: train
    num_bytes: 108930347
    num_examples: 1000000
  - name: validation
    num_bytes: 234848
    num_examples: 2000
  download_size: 36980744
  dataset_size: 109408946
- config_name: bn-en
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - bn
        - en
  splits:
  - name: test
    num_bytes: 510101
    num_examples: 2000
  - name: train
    num_bytes: 249906846
    num_examples: 1000000
  - name: validation
    num_bytes: 498414
    num_examples: 2000
  download_size: 72999655
  dataset_size: 250915361
- config_name: br-en
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - br
        - en
  splits:
  - name: test
    num_bytes: 127925
    num_examples: 2000
  - name: train
    num_bytes: 8539006
    num_examples: 153447
  - name: validation
    num_bytes: 133772
    num_examples: 2000
  download_size: 3323458
  dataset_size: 8800703
- config_name: bs-en
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - bs
        - en
  splits:
  - name: test
    num_bytes: 168622
    num_examples: 2000
  - name: train
    num_bytes: 75082948
    num_examples: 1000000
  - name: validation
    num_bytes: 172481
    num_examples: 2000
  download_size: 30746956
  dataset_size: 75424051
- config_name: ca-en
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - ca
        - en
  splits:
  - name: test
    num_bytes: 205666
    num_examples: 2000
  - name: train
    num_bytes: 88405510
    num_examples: 1000000
  - name: validation
    num_bytes: 212637
    num_examples: 2000
  download_size: 36267794
  dataset_size: 88823813
- config_name: cs-en
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - cs
        - en
  splits:
  - name: test
    num_bytes: 205274
    num_examples: 2000
  - name: train
    num_bytes: 91897719
    num_examples: 1000000
  - name: validation
    num_bytes: 219084
    num_examples: 2000
  download_size: 39673827
  dataset_size: 92322077
- config_name: cy-en
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - cy
        - en
  splits:
  - name: test
    num_bytes: 124289
    num_examples: 2000
  - name: train
    num_bytes: 17244980
    num_examples: 289521
  - name: validation
    num_bytes: 118856
    num_examples: 2000
  download_size: 6487005
  dataset_size: 17488125
- config_name: da-en
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - da
        - en
  splits:
  - name: test
    num_bytes: 298123
    num_examples: 2000
  - name: train
    num_bytes: 126425274
    num_examples: 1000000
  - name: validation
    num_bytes: 300624
    num_examples: 2000
  download_size: 50404122
  dataset_size: 127024021
- config_name: de-en
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - de
        - en
  splits:
  - name: test
    num_bytes: 330959
    num_examples: 2000
  - name: train
    num_bytes: 152246756
    num_examples: 1000000
  - name: validation
    num_bytes: 332350
    num_examples: 2000
  download_size: 67205361
  dataset_size: 152910065
- config_name: dz-en
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - dz
        - en
  splits:
  - name: train
    num_bytes: 81162
    num_examples: 624
  download_size: 17814
  dataset_size: 81162
- config_name: el-en
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - el
        - en
  splits:
  - name: test
    num_bytes: 302393
    num_examples: 2000
  - name: train
    num_bytes: 127964703
    num_examples: 1000000
  - name: validation
    num_bytes: 291234
    num_examples: 2000
  download_size: 43973686
  dataset_size: 128558330
- config_name: en-eo
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - en
        - eo
  splits:
  - name: test
    num_bytes: 167386
    num_examples: 2000
  - name: train
    num_bytes: 24431953
    num_examples: 337106
  - name: validation
    num_bytes: 168838
    num_examples: 2000
  download_size: 9999313
  dataset_size: 24768177
- config_name: en-es
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - en
        - es
  splits:
  - name: test
    num_bytes: 326270
    num_examples: 2000
  - name: train
    num_bytes: 136643904
    num_examples: 1000000
  - name: validation
    num_bytes: 326735
    num_examples: 2000
  download_size: 55534068
  dataset_size: 137296909
- config_name: en-et
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - en
        - et
  splits:
  - name: test
    num_bytes: 272171
    num_examples: 2000
  - name: train
    num_bytes: 112299053
    num_examples: 1000000
  - name: validation
    num_bytes: 276962
    num_examples: 2000
  download_size: 46235623
  dataset_size: 112848186
- config_name: en-eu
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - en
        - eu
  splits:
  - name: test
    num_bytes: 280885
    num_examples: 2000
  - name: train
    num_bytes: 112330085
    num_examples: 1000000
  - name: validation
    num_bytes: 281503
    num_examples: 2000
  download_size: 46389313
  dataset_size: 112892473
- config_name: en-fa
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - en
        - fa
  splits:
  - name: test
    num_bytes: 296556
    num_examples: 2000
  - name: train
    num_bytes: 125401335
    num_examples: 1000000
  - name: validation
    num_bytes: 291129
    num_examples: 2000
  download_size: 44568447
  dataset_size: 125989020
- config_name: en-fi
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - en
        - fi
  splits:
  - name: test
    num_bytes: 245822
    num_examples: 2000
  - name: train
    num_bytes: 106025790
    num_examples: 1000000
  - name: validation
    num_bytes: 247227
    num_examples: 2000
  download_size: 42563103
  dataset_size: 106518839
- config_name: en-fr
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - en
        - fr
  splits:
  - name: test
    num_bytes: 469731
    num_examples: 2000
  - name: train
    num_bytes: 201441250
    num_examples: 1000000
  - name: validation
    num_bytes: 481484
    num_examples: 2000
  download_size: 81009778
  dataset_size: 202392465
- config_name: en-fy
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - en
        - fy
  splits:
  - name: test
    num_bytes: 101246
    num_examples: 2000
  - name: train
    num_bytes: 3895688
    num_examples: 54342
  - name: validation
    num_bytes: 100129
    num_examples: 2000
  download_size: 1522187
  dataset_size: 4097063
- config_name: en-ga
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - en
        - ga
  splits:
  - name: test
    num_bytes: 503317
    num_examples: 2000
  - name: train
    num_bytes: 42132742
    num_examples: 289524
  - name: validation
    num_bytes: 503217
    num_examples: 2000
  download_size: 14998873
  dataset_size: 43139276
- config_name: en-gd
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - en
        - gd
  splits:
  - name: test
    num_bytes: 218362
    num_examples: 1606
  - name: train
    num_bytes: 1254795
    num_examples: 16316
  - name: validation
    num_bytes: 203885
    num_examples: 1605
  download_size: 564053
  dataset_size: 1677042
- config_name: en-gl
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - en
        - gl
  splits:
  - name: test
    num_bytes: 190699
    num_examples: 2000
  - name: train
    num_bytes: 43327444
    num_examples: 515344
  - name: validation
    num_bytes: 193606
    num_examples: 2000
  download_size: 18056665
  dataset_size: 43711749
- config_name: en-gu
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - en
        - gu
  splits:
  - name: test
    num_bytes: 199733
    num_examples: 2000
  - name: train
    num_bytes: 33641975
    num_examples: 318306
  - name: validation
    num_bytes: 205550
    num_examples: 2000
  download_size: 9407543
  dataset_size: 34047258
- config_name: en-ha
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - en
        - ha
  splits:
  - name: test
    num_bytes: 407352
    num_examples: 2000
  - name: train
    num_bytes: 20391964
    num_examples: 97983
  - name: validation
    num_bytes: 411526
    num_examples: 2000
  download_size: 6898482
  dataset_size: 21210842
- config_name: en-he
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - en
        - he
  splits:
  - name: test
    num_bytes: 208475
    num_examples: 2000
  - name: train
    num_bytes: 91160431
    num_examples: 1000000
  - name: validation
    num_bytes: 209446
    num_examples: 2000
  download_size: 31214136
  dataset_size: 91578352
- config_name: en-hi
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - en
        - hi
  splits:
  - name: test
    num_bytes: 496578
    num_examples: 2000
  - name: train
    num_bytes: 124923977
    num_examples: 534319
  - name: validation
    num_bytes: 474087
    num_examples: 2000
  download_size: 35993452
  dataset_size: 125894642
- config_name: en-hr
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - en
        - hr
  splits:
  - name: test
    num_bytes: 179644
    num_examples: 2000
  - name: train
    num_bytes: 75310316
    num_examples: 1000000
  - name: validation
    num_bytes: 179623
    num_examples: 2000
  download_size: 30728154
  dataset_size: 75669583
- config_name: en-hu
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - en
        - hu
  splits:
  - name: test
    num_bytes: 206047
    num_examples: 2000
  - name: train
    num_bytes: 87484262
    num_examples: 1000000
  - name: validation
    num_bytes: 208315
    num_examples: 2000
  download_size: 35696235
  dataset_size: 87898624
- config_name: en-hy
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - en
        - hy
  splits:
  - name: train
    num_bytes: 652631
    num_examples: 7059
  download_size: 215246
  dataset_size: 652631
- config_name: en-id
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - en
        - id
  splits:
  - name: test
    num_bytes: 177693
    num_examples: 2000
  - name: train
    num_bytes: 78699773
    num_examples: 1000000
  - name: validation
    num_bytes: 180032
    num_examples: 2000
  download_size: 29914089
  dataset_size: 79057498
- config_name: en-ig
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - en
        - ig
  splits:
  - name: test
    num_bytes: 137332
    num_examples: 1843
  - name: train
    num_bytes: 1612539
    num_examples: 18415
  - name: validation
    num_bytes: 135995
    num_examples: 1843
  download_size: 391849
  dataset_size: 1885866
- config_name: en-is
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - en
        - is
  splits:
  - name: test
    num_bytes: 170887
    num_examples: 2000
  - name: train
    num_bytes: 73964915
    num_examples: 1000000
  - name: validation
    num_bytes: 170640
    num_examples: 2000
  download_size: 28831218
  dataset_size: 74306442
- config_name: en-it
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - en
        - it
  splits:
  - name: test
    num_bytes: 299037
    num_examples: 2000
  - name: train
    num_bytes: 123655086
    num_examples: 1000000
  - name: validation
    num_bytes: 294362
    num_examples: 2000
  download_size: 50903618
  dataset_size: 124248485
- config_name: en-ja
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - en
        - ja
  splits:
  - name: test
    num_bytes: 190999
    num_examples: 2000
  - name: train
    num_bytes: 88349369
    num_examples: 1000000
  - name: validation
    num_bytes: 191419
    num_examples: 2000
  download_size: 34452575
  dataset_size: 88731787
- config_name: en-ka
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - en
        - ka
  splits:
  - name: test
    num_bytes: 256227
    num_examples: 2000
  - name: train
    num_bytes: 42465706
    num_examples: 377306
  - name: validation
    num_bytes: 260416
    num_examples: 2000
  download_size: 12743188
  dataset_size: 42982349
- config_name: en-kk
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - en
        - kk
  splits:
  - name: test
    num_bytes: 137664
    num_examples: 2000
  - name: train
    num_bytes: 7124378
    num_examples: 79927
  - name: validation
    num_bytes: 139665
    num_examples: 2000
  download_size: 2425372
  dataset_size: 7401707
- config_name: en-km
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - en
        - km
  splits:
  - name: test
    num_bytes: 289027
    num_examples: 2000
  - name: train
    num_bytes: 19680611
    num_examples: 111483
  - name: validation
    num_bytes: 302527
    num_examples: 2000
  download_size: 5193620
  dataset_size: 20272165
- config_name: en-ko
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - en
        - ko
  splits:
  - name: test
    num_bytes: 190696
    num_examples: 2000
  - name: train
    num_bytes: 93665332
    num_examples: 1000000
  - name: validation
    num_bytes: 189368
    num_examples: 2000
  download_size: 37602794
  dataset_size: 94045396
- config_name: en-kn
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - en
        - kn
  splits:
  - name: test
    num_bytes: 77205
    num_examples: 918
  - name: train
    num_bytes: 1833334
    num_examples: 14537
  - name: validation
    num_bytes: 77607
    num_examples: 917
  download_size: 525449
  dataset_size: 1988146
- config_name: en-ku
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - en
        - ku
  splits:
  - name: test
    num_bytes: 247847
    num_examples: 2000
  - name: train
    num_bytes: 49107864
    num_examples: 144844
  - name: validation
    num_bytes: 239325
    num_examples: 2000
  download_size: 14252198
  dataset_size: 49595036
- config_name: en-ky
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - en
        - ky
  splits:
  - name: test
    num_bytes: 142530
    num_examples: 2000
  - name: train
    num_bytes: 1879298
    num_examples: 27215
  - name: validation
    num_bytes: 138487
    num_examples: 2000
  download_size: 616902
  dataset_size: 2160315
- config_name: en-li
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - en
        - li
  splits:
  - name: test
    num_bytes: 93350
    num_examples: 2000
  - name: train
    num_bytes: 1628601
    num_examples: 25535
  - name: validation
    num_bytes: 92906
    num_examples: 2000
  download_size: 450092
  dataset_size: 1814857
- config_name: en-lt
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - en
        - lt
  splits:
  - name: test
    num_bytes: 482615
    num_examples: 2000
  - name: train
    num_bytes: 177061044
    num_examples: 1000000
  - name: validation
    num_bytes: 469117
    num_examples: 2000
  download_size: 69388131
  dataset_size: 178012776
- config_name: en-lv
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - en
        - lv
  splits:
  - name: test
    num_bytes: 536576
    num_examples: 2000
  - name: train
    num_bytes: 206051849
    num_examples: 1000000
  - name: validation
    num_bytes: 522072
    num_examples: 2000
  download_size: 78952903
  dataset_size: 207110497
- config_name: en-mg
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - en
        - mg
  splits:
  - name: test
    num_bytes: 525067
    num_examples: 2000
  - name: train
    num_bytes: 130865649
    num_examples: 590771
  - name: validation
    num_bytes: 511171
    num_examples: 2000
  download_size: 52470504
  dataset_size: 131901887
- config_name: en-mk
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - en
        - mk
  splits:
  - name: test
    num_bytes: 308934
    num_examples: 2000
  - name: train
    num_bytes: 117069489
    num_examples: 1000000
  - name: validation
    num_bytes: 305498
    num_examples: 2000
  download_size: 39517761
  dataset_size: 117683921
- config_name: en-ml
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - en
        - ml
  splits:
  - name: test
    num_bytes: 340626
    num_examples: 2000
  - name: train
    num_bytes: 199971743
    num_examples: 822746
  - name: validation
    num_bytes: 334459
    num_examples: 2000
  download_size: 48654808
  dataset_size: 200646828
- config_name: en-mn
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - en
        - mn
  splits:
  - name: train
    num_bytes: 250778
    num_examples: 4294
  download_size: 42039
  dataset_size: 250778
- config_name: en-mr
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - en
        - mr
  splits:
  - name: test
    num_bytes: 238612
    num_examples: 2000
  - name: train
    num_bytes: 2724131
    num_examples: 27007
  - name: validation
    num_bytes: 235540
    num_examples: 2000
  download_size: 910211
  dataset_size: 3198283
- config_name: en-ms
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - en
        - ms
  splits:
  - name: test
    num_bytes: 179705
    num_examples: 2000
  - name: train
    num_bytes: 76829645
    num_examples: 1000000
  - name: validation
    num_bytes: 180183
    num_examples: 2000
  download_size: 29807607
  dataset_size: 77189533
- config_name: en-mt
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - en
        - mt
  splits:
  - name: test
    num_bytes: 566134
    num_examples: 2000
  - name: train
    num_bytes: 222222396
    num_examples: 1000000
  - name: validation
    num_bytes: 594386
    num_examples: 2000
  download_size: 84757608
  dataset_size: 223382916
- config_name: en-my
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - en
        - my
  splits:
  - name: test
    num_bytes: 337351
    num_examples: 2000
  - name: train
    num_bytes: 3673501
    num_examples: 24594
  - name: validation
    num_bytes: 336155
    num_examples: 2000
  download_size: 1038600
  dataset_size: 4347007
- config_name: en-nb
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - en
        - nb
  splits:
  - name: test
    num_bytes: 334117
    num_examples: 2000
  - name: train
    num_bytes: 13611709
    num_examples: 142906
  - name: validation
    num_bytes: 324400
    num_examples: 2000
  download_size: 5706626
  dataset_size: 14270226
- config_name: en-ne
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - en
        - ne
  splits:
  - name: test
    num_bytes: 186527
    num_examples: 2000
  - name: train
    num_bytes: 44136280
    num_examples: 406381
  - name: validation
    num_bytes: 204920
    num_examples: 2000
  download_size: 11711988
  dataset_size: 44527727
- config_name: en-nl
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - en
        - nl
  splits:
  - name: test
    num_bytes: 282755
    num_examples: 2000
  - name: train
    num_bytes: 112327073
    num_examples: 1000000
  - name: validation
    num_bytes: 270940
    num_examples: 2000
  download_size: 45374708
  dataset_size: 112880768
- config_name: en-nn
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - en
        - nn
  splits:
  - name: test
    num_bytes: 179007
    num_examples: 2000
  - name: train
    num_bytes: 32924821
    num_examples: 486055
  - name: validation
    num_bytes: 187650
    num_examples: 2000
  download_size: 12742134
  dataset_size: 33291478
- config_name: en-no
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - en
        - 'no'
  splits:
  - name: test
    num_bytes: 173328
    num_examples: 2000
  - name: train
    num_bytes: 74106283
    num_examples: 1000000
  - name: validation
    num_bytes: 178013
    num_examples: 2000
  download_size: 28851262
  dataset_size: 74457624
- config_name: en-oc
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - en
        - oc
  splits:
  - name: test
    num_bytes: 82350
    num_examples: 2000
  - name: train
    num_bytes: 1627206
    num_examples: 35791
  - name: validation
    num_bytes: 81650
    num_examples: 2000
  download_size: 607192
  dataset_size: 1791206
- config_name: en-or
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - en
        - or
  splits:
  - name: test
    num_bytes: 163947
    num_examples: 1318
  - name: train
    num_bytes: 1500749
    num_examples: 14273
  - name: validation
    num_bytes: 155331
    num_examples: 1317
  download_size: 499401
  dataset_size: 1820027
- config_name: en-pa
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - en
        - pa
  splits:
  - name: test
    num_bytes: 133909
    num_examples: 2000
  - name: train
    num_bytes: 8509228
    num_examples: 107296
  - name: validation
    num_bytes: 136196
    num_examples: 2000
  download_size: 2589682
  dataset_size: 8779333
- config_name: en-pl
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - en
        - pl
  splits:
  - name: test
    num_bytes: 212503
    num_examples: 2000
  - name: train
    num_bytes: 95248523
    num_examples: 1000000
  - name: validation
    num_bytes: 218216
    num_examples: 2000
  download_size: 39320454
  dataset_size: 95679242
- config_name: en-ps
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - en
        - ps
  splits:
  - name: test
    num_bytes: 93003
    num_examples: 2000
  - name: train
    num_bytes: 4436576
    num_examples: 79127
  - name: validation
    num_bytes: 95164
    num_examples: 2000
  download_size: 1223087
  dataset_size: 4624743
- config_name: en-pt
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - en
        - pt
  splits:
  - name: test
    num_bytes: 296122
    num_examples: 2000
  - name: train
    num_bytes: 118243649
    num_examples: 1000000
  - name: validation
    num_bytes: 292082
    num_examples: 2000
  download_size: 48087550
  dataset_size: 118831853
- config_name: en-ro
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - en
        - ro
  splits:
  - name: test
    num_bytes: 198647
    num_examples: 2000
  - name: train
    num_bytes: 85249851
    num_examples: 1000000
  - name: validation
    num_bytes: 199172
    num_examples: 2000
  download_size: 35032743
  dataset_size: 85647670
- config_name: en-ru
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - en
        - ru
  splits:
  - name: test
    num_bytes: 490984
    num_examples: 2000
  - name: train
    num_bytes: 195101737
    num_examples: 1000000
  - name: validation
    num_bytes: 490246
    num_examples: 2000
  download_size: 68501634
  dataset_size: 196082967
- config_name: en-rw
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - en
        - rw
  splits:
  - name: test
    num_bytes: 136197
    num_examples: 2000
  - name: train
    num_bytes: 15286303
    num_examples: 173823
  - name: validation
    num_bytes: 134965
    num_examples: 2000
  download_size: 5233241
  dataset_size: 15557465
- config_name: en-se
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - en
        - se
  splits:
  - name: test
    num_bytes: 85705
    num_examples: 2000
  - name: train
    num_bytes: 2047412
    num_examples: 35907
  - name: validation
    num_bytes: 83672
    num_examples: 2000
  download_size: 806982
  dataset_size: 2216789
- config_name: en-sh
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - en
        - sh
  splits:
  - name: test
    num_bytes: 569487
    num_examples: 2000
  - name: train
    num_bytes: 60900239
    num_examples: 267211
  - name: validation
    num_bytes: 555602
    num_examples: 2000
  download_size: 22357505
  dataset_size: 62025328
- config_name: en-si
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - en
        - si
  splits:
  - name: test
    num_bytes: 271743
    num_examples: 2000
  - name: train
    num_bytes: 114951675
    num_examples: 979109
  - name: validation
    num_bytes: 271244
    num_examples: 2000
  download_size: 33247484
  dataset_size: 115494662
- config_name: en-sk
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - en
        - sk
  splits:
  - name: test
    num_bytes: 258042
    num_examples: 2000
  - name: train
    num_bytes: 111743868
    num_examples: 1000000
  - name: validation
    num_bytes: 255470
    num_examples: 2000
  download_size: 46618395
  dataset_size: 112257380
- config_name: en-sl
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - en
        - sl
  splits:
  - name: test
    num_bytes: 205478
    num_examples: 2000
  - name: train
    num_bytes: 90270957
    num_examples: 1000000
  - name: validation
    num_bytes: 198662
    num_examples: 2000
  download_size: 37536724
  dataset_size: 90675097
- config_name: en-sq
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - en
        - sq
  splits:
  - name: test
    num_bytes: 275379
    num_examples: 2000
  - name: train
    num_bytes: 105745981
    num_examples: 1000000
  - name: validation
    num_bytes: 267312
    num_examples: 2000
  download_size: 42697338
  dataset_size: 106288672
- config_name: en-sr
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - en
        - sr
  splits:
  - name: test
    num_bytes: 180232
    num_examples: 2000
  - name: train
    num_bytes: 75726835
    num_examples: 1000000
  - name: validation
    num_bytes: 184246
    num_examples: 2000
  download_size: 31260575
  dataset_size: 76091313
- config_name: en-sv
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - en
        - sv
  splits:
  - name: test
    num_bytes: 271014
    num_examples: 2000
  - name: train
    num_bytes: 116985953
    num_examples: 1000000
  - name: validation
    num_bytes: 279994
    num_examples: 2000
  download_size: 46694960
  dataset_size: 117536961
- config_name: en-ta
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - en
        - ta
  splits:
  - name: test
    num_bytes: 351990
    num_examples: 2000
  - name: train
    num_bytes: 74044524
    num_examples: 227014
  - name: validation
    num_bytes: 335557
    num_examples: 2000
  download_size: 17652443
  dataset_size: 74732071
- config_name: en-te
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - en
        - te
  splits:
  - name: test
    num_bytes: 190595
    num_examples: 2000
  - name: train
    num_bytes: 6688625
    num_examples: 64352
  - name: validation
    num_bytes: 193666
    num_examples: 2000
  download_size: 2011832
  dataset_size: 7072886
- config_name: en-tg
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - en
        - tg
  splits:
  - name: test
    num_bytes: 372120
    num_examples: 2000
  - name: train
    num_bytes: 35477177
    num_examples: 193882
  - name: validation
    num_bytes: 371728
    num_examples: 2000
  download_size: 11389877
  dataset_size: 36221025
- config_name: en-th
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - en
        - th
  splits:
  - name: test
    num_bytes: 290581
    num_examples: 2000
  - name: train
    num_bytes: 132821031
    num_examples: 1000000
  - name: validation
    num_bytes: 288366
    num_examples: 2000
  download_size: 38147204
  dataset_size: 133399978
- config_name: en-tk
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - en
        - tk
  splits:
  - name: test
    num_bytes: 83886
    num_examples: 1852
  - name: train
    num_bytes: 719633
    num_examples: 13110
  - name: validation
    num_bytes: 81014
    num_examples: 1852
  download_size: 157481
  dataset_size: 884533
- config_name: en-tr
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - en
        - tr
  splits:
  - name: test
    num_bytes: 183833
    num_examples: 2000
  - name: train
    num_bytes: 78946365
    num_examples: 1000000
  - name: validation
    num_bytes: 181917
    num_examples: 2000
  download_size: 30892429
  dataset_size: 79312115
- config_name: en-tt
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - en
        - tt
  splits:
  - name: test
    num_bytes: 693276
    num_examples: 2000
  - name: train
    num_bytes: 35313258
    num_examples: 100843
  - name: validation
    num_bytes: 701670
    num_examples: 2000
  download_size: 9940523
  dataset_size: 36708204
- config_name: en-ug
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - en
        - ug
  splits:
  - name: test
    num_bytes: 620881
    num_examples: 2000
  - name: train
    num_bytes: 31576580
    num_examples: 72170
  - name: validation
    num_bytes: 631236
    num_examples: 2000
  download_size: 8687743
  dataset_size: 32828697
- config_name: en-uk
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - en
        - uk
  splits:
  - name: test
    num_bytes: 249750
    num_examples: 2000
  - name: train
    num_bytes: 104230356
    num_examples: 1000000
  - name: validation
    num_bytes: 247131
    num_examples: 2000
  download_size: 37415496
  dataset_size: 104727237
- config_name: en-ur
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - en
        - ur
  splits:
  - name: test
    num_bytes: 538564
    num_examples: 2000
  - name: train
    num_bytes: 268961304
    num_examples: 753913
  - name: validation
    num_bytes: 529316
    num_examples: 2000
  download_size: 81092186
  dataset_size: 270029184
- config_name: en-uz
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - en
        - uz
  splits:
  - name: test
    num_bytes: 408683
    num_examples: 2000
  - name: train
    num_bytes: 38375434
    num_examples: 173157
  - name: validation
    num_bytes: 398861
    num_examples: 2000
  download_size: 11791643
  dataset_size: 39182978
- config_name: en-vi
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - en
        - vi
  splits:
  - name: test
    num_bytes: 192752
    num_examples: 2000
  - name: train
    num_bytes: 82615270
    num_examples: 1000000
  - name: validation
    num_bytes: 194729
    num_examples: 2000
  download_size: 30647296
  dataset_size: 83002751
- config_name: en-wa
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - en
        - wa
  splits:
  - name: test
    num_bytes: 87099
    num_examples: 2000
  - name: train
    num_bytes: 6085948
    num_examples: 104496
  - name: validation
    num_bytes: 87726
    num_examples: 2000
  download_size: 2119821
  dataset_size: 6260773
- config_name: en-xh
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - en
        - xh
  splits:
  - name: test
    num_bytes: 318660
    num_examples: 2000
  - name: train
    num_bytes: 50607248
    num_examples: 439671
  - name: validation
    num_bytes: 315839
    num_examples: 2000
  download_size: 20503199
  dataset_size: 51241747
- config_name: en-yi
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - en
        - yi
  splits:
  - name: test
    num_bytes: 96490
    num_examples: 2000
  - name: train
    num_bytes: 1275143
    num_examples: 15010
  - name: validation
    num_bytes: 99826
    num_examples: 2000
  download_size: 284031
  dataset_size: 1471459
- config_name: en-yo
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - en
        - yo
  splits:
  - name: train
    num_bytes: 979769
    num_examples: 10375
  download_size: 177540
  dataset_size: 979769
- config_name: en-zh
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - en
        - zh
  splits:
  - name: test
    num_bytes: 511372
    num_examples: 2000
  - name: train
    num_bytes: 200062983
    num_examples: 1000000
  - name: validation
    num_bytes: 512364
    num_examples: 2000
  download_size: 83265500
  dataset_size: 201086719
- config_name: en-zu
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - en
        - zu
  splits:
  - name: test
    num_bytes: 117518
    num_examples: 2000
  - name: train
    num_bytes: 2799590
    num_examples: 38616
  - name: validation
    num_bytes: 120141
    num_examples: 2000
  download_size: 889951
  dataset_size: 3037249
- config_name: ar-de
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - ar
        - de
  splits:
  - name: test
    num_bytes: 238599
    num_examples: 2000
  download_size: 2556791
  dataset_size: 238599
- config_name: ar-fr
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - ar
        - fr
  splits:
  - name: test
    num_bytes: 547382
    num_examples: 2000
  download_size: 2556791
  dataset_size: 547382
- config_name: ar-nl
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - ar
        - nl
  splits:
  - name: test
    num_bytes: 212936
    num_examples: 2000
  download_size: 2556791
  dataset_size: 212936
- config_name: ar-ru
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - ar
        - ru
  splits:
  - name: test
    num_bytes: 808270
    num_examples: 2000
  download_size: 2556791
  dataset_size: 808270
- config_name: ar-zh
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - ar
        - zh
  splits:
  - name: test
    num_bytes: 713412
    num_examples: 2000
  download_size: 2556791
  dataset_size: 713412
- config_name: de-fr
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - de
        - fr
  splits:
  - name: test
    num_bytes: 458746
    num_examples: 2000
  download_size: 2556791
  dataset_size: 458746
- config_name: de-nl
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - de
        - nl
  splits:
  - name: test
    num_bytes: 403886
    num_examples: 2000
  download_size: 2556791
  dataset_size: 403886
- config_name: de-ru
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - de
        - ru
  splits:
  - name: test
    num_bytes: 315779
    num_examples: 2000
  download_size: 2556791
  dataset_size: 315779
- config_name: de-zh
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - de
        - zh
  splits:
  - name: test
    num_bytes: 280397
    num_examples: 2000
  download_size: 2556791
  dataset_size: 280397
- config_name: fr-nl
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - fr
        - nl
  splits:
  - name: test
    num_bytes: 368646
    num_examples: 2000
  download_size: 2556791
  dataset_size: 368646
- config_name: fr-ru
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - fr
        - ru
  splits:
  - name: test
    num_bytes: 732724
    num_examples: 2000
  download_size: 2556791
  dataset_size: 732724
- config_name: fr-zh
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - fr
        - zh
  splits:
  - name: test
    num_bytes: 619394
    num_examples: 2000
  download_size: 2556791
  dataset_size: 619394
- config_name: nl-ru
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - nl
        - ru
  splits:
  - name: test
    num_bytes: 256067
    num_examples: 2000
  download_size: 2556791
  dataset_size: 256067
- config_name: nl-zh
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - nl
        - zh
  splits:
  - name: test
    num_bytes: 183641
    num_examples: 2000
  download_size: 2556791
  dataset_size: 183641
- config_name: ru-zh
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - ru
        - zh
  splits:
  - name: test
    num_bytes: 916114
    num_examples: 2000
  download_size: 2556791
  dataset_size: 916114
---

# Dataset Card for Opus100

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

- **Homepage:** [Link](http://opus.nlpl.eu/opus-100.php) 
- **Repository:** [GitHub](https://github.com/EdinburghNLP/opus-100-corpus)
- **Paper:** [ARXIV](https://arxiv.org/abs/2004.11867)
- **Leaderboard:** 
- **Point of Contact:** 

### Dataset Summary

OPUS-100 is English-centric, meaning that all training pairs include English on either the source or target side. The corpus covers 100 languages (including English). Selected the languages based on the volume of parallel data available in OPUS.

### Supported Tasks and Leaderboards

[More Information Needed]

### Languages

OPUS-100 contains approximately 55M sentence pairs. Of the 99 language pairs, 44 have 1M sentence pairs of training data, 73 have at least 100k, and 95 have at least 10k.

## Dataset Structure

### Data Instances

```
{
  "ca": "El departament de bombers té el seu propi equip d'investigació.",
  "en": "Well, the fire department has its own investigative unit."
}
```

### Data Fields

- `src_tag`: `string` text in source language
- `tgt_tag`: `string` translation of source language in target language

### Data Splits

The dataset is split into training, development, and test portions. Data was prepared by randomly sampled up to 1M sentence pairs per language pair for training and up to 2000 each for development and test. To ensure that there was no overlap (at the monolingual sentence level) between the training and development/test data, they applied a filter during sampling to exclude sentences that had already been sampled. Note that this was done cross-lingually so that, for instance, an English sentence in the Portuguese-English portion of the training data could not occur in the Hindi-English test set.

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

```
@misc{zhang2020improving,
      title={Improving Massively Multilingual Neural Machine Translation and Zero-Shot Translation}, 
      author={Biao Zhang and Philip Williams and Ivan Titov and Rico Sennrich},
      year={2020},
      eprint={2004.11867},
      archivePrefix={arXiv},
      primaryClass={cs.CL}
}
```

### Contributions

Thanks to [@vasudevgupta7](https://github.com/vasudevgupta7) for adding this dataset.