---
pretty_name: Common Voice
annotations_creators:
- crowdsourced
language_creators:
- crowdsourced
language:
- ab
- ar
- as
- br
- ca
- cnh
- cs
- cv
- cy
- de
- dv
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
- hi
- hsb
- hu
- ia
- id
- it
- ja
- ka
- kab
- ky
- lg
- lt
- lv
- mn
- mt
- nl
- or
- pa
- pl
- pt
- rm
- ro
- ru
- rw
- sah
- sl
- sv
- ta
- th
- tr
- tt
- uk
- vi
- vot
- zh
language_bcp47:
- fy-NL
- ga-IE
- pa-IN
- rm-sursilv
- rm-vallader
- sv-SE
- zh-CN
- zh-HK
- zh-TW
license:
- cc0-1.0
multilinguality:
- multilingual
size_categories:
- 100K<n<1M
- 10K<n<100K
- 1K<n<10K
- n<1K
source_datasets:
- extended|common_voice
task_categories:
- automatic-speech-recognition
task_ids: []
paperswithcode_id: common-voice
configs:
- ab
- ar
- as
- br
- ca
- cnh
- cs
- cv
- cy
- de
- dv
- el
- en
- eo
- es
- et
- eu
- fa
- fi
- fr
- fy-NL
- ga-IE
- hi
- hsb
- hu
- ia
- id
- it
- ja
- ka
- kab
- ky
- lg
- lt
- lv
- mn
- mt
- nl
- or
- pa-IN
- pl
- pt
- rm-sursilv
- rm-vallader
- ro
- ru
- rw
- sah
- sl
- sv-SE
- ta
- th
- tr
- tt
- uk
- vi
- vot
- zh-CN
- zh-HK
- zh-TW
dataset_info:
- config_name: ab
  features:
  - name: client_id
    dtype: string
  - name: path
    dtype: string
  - name: audio
    dtype:
      audio:
        sampling_rate: 48000
  - name: sentence
    dtype: string
  - name: up_votes
    dtype: int64
  - name: down_votes
    dtype: int64
  - name: age
    dtype: string
  - name: gender
    dtype: string
  - name: accent
    dtype: string
  - name: locale
    dtype: string
  - name: segment
    dtype: string
  splits:
  - name: invalidated
    num_bytes: 361626
    num_examples: 8
  - name: other
    num_bytes: 40023390
    num_examples: 752
  - name: test
    num_bytes: 411844
    num_examples: 9
  - name: train
    num_bytes: 1295622
    num_examples: 22
  - name: validated
    num_bytes: 1707426
    num_examples: 31
  - name: validation
  download_size: 41038412
  dataset_size: 43799908
- config_name: ar
  features:
  - name: client_id
    dtype: string
  - name: path
    dtype: string
  - name: audio
    dtype:
      audio:
        sampling_rate: 48000
  - name: sentence
    dtype: string
  - name: up_votes
    dtype: int64
  - name: down_votes
    dtype: int64
  - name: age
    dtype: string
  - name: gender
    dtype: string
  - name: accent
    dtype: string
  - name: locale
    dtype: string
  - name: segment
    dtype: string
  splits:
  - name: invalidated
    num_bytes: 194805036
    num_examples: 6333
  - name: other
    num_bytes: 515822404
    num_examples: 18283
  - name: test
    num_bytes: 237546641
    num_examples: 7622
  - name: train
    num_bytes: 359335168
    num_examples: 14227
  - name: validated
    num_bytes: 1182522872
    num_examples: 43291
  - name: validation
    num_bytes: 209606861
    num_examples: 7517
  download_size: 1756264615
  dataset_size: 2699638982
- config_name: as
  features:
  - name: client_id
    dtype: string
  - name: path
    dtype: string
  - name: audio
    dtype:
      audio:
        sampling_rate: 48000
  - name: sentence
    dtype: string
  - name: up_votes
    dtype: int64
  - name: down_votes
    dtype: int64
  - name: age
    dtype: string
  - name: gender
    dtype: string
  - name: accent
    dtype: string
  - name: locale
    dtype: string
  - name: segment
    dtype: string
  splits:
  - name: invalidated
    num_bytes: 886145
    num_examples: 31
  - name: other
  - name: test
    num_bytes: 5071343
    num_examples: 110
  - name: train
    num_bytes: 11442279
    num_examples: 270
  - name: validated
    num_bytes: 21993698
    num_examples: 504
  - name: validation
    num_bytes: 5480156
    num_examples: 124
  download_size: 22226465
  dataset_size: 44873621
- config_name: br
  features:
  - name: client_id
    dtype: string
  - name: path
    dtype: string
  - name: audio
    dtype:
      audio:
        sampling_rate: 48000
  - name: sentence
    dtype: string
  - name: up_votes
    dtype: int64
  - name: down_votes
    dtype: int64
  - name: age
    dtype: string
  - name: gender
    dtype: string
  - name: accent
    dtype: string
  - name: locale
    dtype: string
  - name: segment
    dtype: string
  splits:
  - name: invalidated
    num_bytes: 20861017
    num_examples: 623
  - name: other
    num_bytes: 269858143
    num_examples: 10912
  - name: test
    num_bytes: 54461339
    num_examples: 2087
  - name: train
    num_bytes: 62238289
    num_examples: 2780
  - name: validated
    num_bytes: 203503622
    num_examples: 8560
  - name: validation
    num_bytes: 46995570
    num_examples: 1997
  download_size: 465276982
  dataset_size: 657917980
- config_name: ca
  features:
  - name: client_id
    dtype: string
  - name: path
    dtype: string
  - name: audio
    dtype:
      audio:
        sampling_rate: 48000
  - name: sentence
    dtype: string
  - name: up_votes
    dtype: int64
  - name: down_votes
    dtype: int64
  - name: age
    dtype: string
  - name: gender
    dtype: string
  - name: accent
    dtype: string
  - name: locale
    dtype: string
  - name: segment
    dtype: string
  splits:
  - name: invalidated
    num_bytes: 850402888
    num_examples: 18846
  - name: other
    num_bytes: 2693542910
    num_examples: 64446
  - name: test
    num_bytes: 745761890
    num_examples: 15724
  - name: train
    num_bytes: 12966939466
    num_examples: 285584
  - name: validated
    num_bytes: 18115833966
    num_examples: 416701
  - name: validation
    num_bytes: 716442038
    num_examples: 15724
  download_size: 20743110341
  dataset_size: 36088923158
- config_name: cnh
  features:
  - name: client_id
    dtype: string
  - name: path
    dtype: string
  - name: audio
    dtype:
      audio:
        sampling_rate: 48000
  - name: sentence
    dtype: string
  - name: up_votes
    dtype: int64
  - name: down_votes
    dtype: int64
  - name: age
    dtype: string
  - name: gender
    dtype: string
  - name: accent
    dtype: string
  - name: locale
    dtype: string
  - name: segment
    dtype: string
  splits:
  - name: invalidated
    num_bytes: 13642724
    num_examples: 433
  - name: other
    num_bytes: 84878963
    num_examples: 2934
  - name: test
    num_bytes: 24675321
    num_examples: 752
  - name: train
    num_bytes: 18866674
    num_examples: 807
  - name: validated
    num_bytes: 69330148
    num_examples: 2432
  - name: validation
    num_bytes: 22162315
    num_examples: 756
  download_size: 161331331
  dataset_size: 233556145
- config_name: cs
  features:
  - name: client_id
    dtype: string
  - name: path
    dtype: string
  - name: audio
    dtype:
      audio:
        sampling_rate: 48000
  - name: sentence
    dtype: string
  - name: up_votes
    dtype: int64
  - name: down_votes
    dtype: int64
  - name: age
    dtype: string
  - name: gender
    dtype: string
  - name: accent
    dtype: string
  - name: locale
    dtype: string
  - name: segment
    dtype: string
  splits:
  - name: invalidated
    num_bytes: 24717823
    num_examples: 685
  - name: other
    num_bytes: 282225475
    num_examples: 7475
  - name: test
    num_bytes: 148499476
    num_examples: 4144
  - name: train
    num_bytes: 215205282
    num_examples: 5655
  - name: validated
    num_bytes: 1019817024
    num_examples: 30431
  - name: validation
    num_bytes: 148312130
    num_examples: 4118
  download_size: 1271909933
  dataset_size: 1838777210
- config_name: cv
  features:
  - name: client_id
    dtype: string
  - name: path
    dtype: string
  - name: audio
    dtype:
      audio:
        sampling_rate: 48000
  - name: sentence
    dtype: string
  - name: up_votes
    dtype: int64
  - name: down_votes
    dtype: int64
  - name: age
    dtype: string
  - name: gender
    dtype: string
  - name: accent
    dtype: string
  - name: locale
    dtype: string
  - name: segment
    dtype: string
  splits:
  - name: invalidated
    num_bytes: 57923138
    num_examples: 1282
  - name: other
    num_bytes: 288294623
    num_examples: 6927
  - name: test
    num_bytes: 32513061
    num_examples: 788
  - name: train
    num_bytes: 31649510
    num_examples: 931
  - name: validated
    num_bytes: 126717875
    num_examples: 3496
  - name: validation
    num_bytes: 28429779
    num_examples: 818
  download_size: 439329081
  dataset_size: 565527986
- config_name: cy
  features:
  - name: client_id
    dtype: string
  - name: path
    dtype: string
  - name: audio
    dtype:
      audio:
        sampling_rate: 48000
  - name: sentence
    dtype: string
  - name: up_votes
    dtype: int64
  - name: down_votes
    dtype: int64
  - name: age
    dtype: string
  - name: gender
    dtype: string
  - name: accent
    dtype: string
  - name: locale
    dtype: string
  - name: segment
    dtype: string
  splits:
  - name: invalidated
    num_bytes: 146874576
    num_examples: 3648
  - name: other
    num_bytes: 688469886
    num_examples: 17919
  - name: test
    num_bytes: 206865596
    num_examples: 4820
  - name: train
    num_bytes: 271642649
    num_examples: 6839
  - name: validated
    num_bytes: 2763112391
    num_examples: 72984
  - name: validation
    num_bytes: 201813388
    num_examples: 4776
  download_size: 3434474658
  dataset_size: 4278778486
- config_name: de
  features:
  - name: client_id
    dtype: string
  - name: path
    dtype: string
  - name: audio
    dtype:
      audio:
        sampling_rate: 48000
  - name: sentence
    dtype: string
  - name: up_votes
    dtype: int64
  - name: down_votes
    dtype: int64
  - name: age
    dtype: string
  - name: gender
    dtype: string
  - name: accent
    dtype: string
  - name: locale
    dtype: string
  - name: segment
    dtype: string
  splits:
  - name: invalidated
    num_bytes: 1440604803
    num_examples: 32789
  - name: other
    num_bytes: 464513461
    num_examples: 10095
  - name: test
    num_bytes: 744617681
    num_examples: 15588
  - name: train
    num_bytes: 11463160619
    num_examples: 246525
  - name: validated
    num_bytes: 22402489041
    num_examples: 565186
  - name: validation
    num_bytes: 729559862
    num_examples: 15588
  download_size: 23283812097
  dataset_size: 37244945467
- config_name: dv
  features:
  - name: client_id
    dtype: string
  - name: path
    dtype: string
  - name: audio
    dtype:
      audio:
        sampling_rate: 48000
  - name: sentence
    dtype: string
  - name: up_votes
    dtype: int64
  - name: down_votes
    dtype: int64
  - name: age
    dtype: string
  - name: gender
    dtype: string
  - name: accent
    dtype: string
  - name: locale
    dtype: string
  - name: segment
    dtype: string
  splits:
  - name: invalidated
    num_bytes: 37694847
    num_examples: 840
  - name: other
  - name: test
    num_bytes: 94281409
    num_examples: 2202
  - name: train
    num_bytes: 118576140
    num_examples: 2680
  - name: validated
    num_bytes: 528571107
    num_examples: 11866
  - name: validation
    num_bytes: 94117088
    num_examples: 2077
  download_size: 540488041
  dataset_size: 873240591
- config_name: el
  features:
  - name: client_id
    dtype: string
  - name: path
    dtype: string
  - name: audio
    dtype:
      audio:
        sampling_rate: 48000
  - name: sentence
    dtype: string
  - name: up_votes
    dtype: int64
  - name: down_votes
    dtype: int64
  - name: age
    dtype: string
  - name: gender
    dtype: string
  - name: accent
    dtype: string
  - name: locale
    dtype: string
  - name: segment
    dtype: string
  splits:
  - name: invalidated
    num_bytes: 6023769
    num_examples: 185
  - name: other
    num_bytes: 186861175
    num_examples: 5659
  - name: test
    num_bytes: 53820491
    num_examples: 1522
  - name: train
    num_bytes: 80759076
    num_examples: 2316
  - name: validated
    num_bytes: 204446790
    num_examples: 5996
  - name: validation
    num_bytes: 44818565
    num_examples: 1401
  download_size: 381570611
  dataset_size: 576729866
- config_name: en
  features:
  - name: client_id
    dtype: string
  - name: path
    dtype: string
  - name: audio
    dtype:
      audio:
        sampling_rate: 48000
  - name: sentence
    dtype: string
  - name: up_votes
    dtype: int64
  - name: down_votes
    dtype: int64
  - name: age
    dtype: string
  - name: gender
    dtype: string
  - name: accent
    dtype: string
  - name: locale
    dtype: string
  - name: segment
    dtype: string
  splits:
  - name: invalidated
    num_bytes: 9122973965
    num_examples: 189562
  - name: other
    num_bytes: 5796244022
    num_examples: 169895
  - name: test
    num_bytes: 758718688
    num_examples: 16164
  - name: train
    num_bytes: 26088826658
    num_examples: 564337
  - name: validated
    num_bytes: 48425872575
    num_examples: 1224864
  - name: validation
    num_bytes: 795638801
    num_examples: 16164
  download_size: 60613063630
  dataset_size: 90988274709
- config_name: eo
  features:
  - name: client_id
    dtype: string
  - name: path
    dtype: string
  - name: audio
    dtype:
      audio:
        sampling_rate: 48000
  - name: sentence
    dtype: string
  - name: up_votes
    dtype: int64
  - name: down_votes
    dtype: int64
  - name: age
    dtype: string
  - name: gender
    dtype: string
  - name: accent
    dtype: string
  - name: locale
    dtype: string
  - name: segment
    dtype: string
  splits:
  - name: invalidated
    num_bytes: 238105462
    num_examples: 4736
  - name: other
    num_bytes: 142476819
    num_examples: 2946
  - name: test
    num_bytes: 420153812
    num_examples: 8969
  - name: train
    num_bytes: 993655930
    num_examples: 19587
  - name: validated
    num_bytes: 2603249289
    num_examples: 58094
  - name: validation
    num_bytes: 391427586
    num_examples: 8987
  download_size: 2883560869
  dataset_size: 4789068898
- config_name: es
  features:
  - name: client_id
    dtype: string
  - name: path
    dtype: string
  - name: audio
    dtype:
      audio:
        sampling_rate: 48000
  - name: sentence
    dtype: string
  - name: up_votes
    dtype: int64
  - name: down_votes
    dtype: int64
  - name: age
    dtype: string
  - name: gender
    dtype: string
  - name: accent
    dtype: string
  - name: locale
    dtype: string
  - name: segment
    dtype: string
  splits:
  - name: invalidated
    num_bytes: 1664876264
    num_examples: 40640
  - name: other
    num_bytes: 5528972205
    num_examples: 144791
  - name: test
    num_bytes: 754049291
    num_examples: 15089
  - name: train
    num_bytes: 6918333205
    num_examples: 161813
  - name: validated
    num_bytes: 9623788388
    num_examples: 236314
  - name: validation
    num_bytes: 735558084
    num_examples: 15089
  download_size: 16188844718
  dataset_size: 25225577437
- config_name: et
  features:
  - name: client_id
    dtype: string
  - name: path
    dtype: string
  - name: audio
    dtype:
      audio:
        sampling_rate: 48000
  - name: sentence
    dtype: string
  - name: up_votes
    dtype: int64
  - name: down_votes
    dtype: int64
  - name: age
    dtype: string
  - name: gender
    dtype: string
  - name: accent
    dtype: string
  - name: locale
    dtype: string
  - name: segment
    dtype: string
  splits:
  - name: invalidated
    num_bytes: 193019544
    num_examples: 3557
  - name: other
    num_bytes: 30339130
    num_examples: 569
  - name: test
    num_bytes: 133183135
    num_examples: 2509
  - name: train
    num_bytes: 161124199
    num_examples: 2966
  - name: validated
    num_bytes: 573417188
    num_examples: 10683
  - name: validation
    num_bytes: 137604813
    num_examples: 2507
  download_size: 767174465
  dataset_size: 1228688009
- config_name: eu
  features:
  - name: client_id
    dtype: string
  - name: path
    dtype: string
  - name: audio
    dtype:
      audio:
        sampling_rate: 48000
  - name: sentence
    dtype: string
  - name: up_votes
    dtype: int64
  - name: down_votes
    dtype: int64
  - name: age
    dtype: string
  - name: gender
    dtype: string
  - name: accent
    dtype: string
  - name: locale
    dtype: string
  - name: segment
    dtype: string
  splits:
  - name: invalidated
    num_bytes: 208553909
    num_examples: 5387
  - name: other
    num_bytes: 988079897
    num_examples: 23570
  - name: test
    num_bytes: 238866501
    num_examples: 5172
  - name: train
    num_bytes: 317322801
    num_examples: 7505
  - name: validated
    num_bytes: 2621488299
    num_examples: 63009
  - name: validation
    num_bytes: 228150083
    num_examples: 5172
  download_size: 3664586106
  dataset_size: 4602461490
- config_name: fa
  features:
  - name: client_id
    dtype: string
  - name: path
    dtype: string
  - name: audio
    dtype:
      audio:
        sampling_rate: 48000
  - name: sentence
    dtype: string
  - name: up_votes
    dtype: int64
  - name: down_votes
    dtype: int64
  - name: age
    dtype: string
  - name: gender
    dtype: string
  - name: accent
    dtype: string
  - name: locale
    dtype: string
  - name: segment
    dtype: string
  splits:
  - name: invalidated
    num_bytes: 499570226
    num_examples: 11698
  - name: other
    num_bytes: 737017546
    num_examples: 22510
  - name: test
    num_bytes: 217939210
    num_examples: 5213
  - name: train
    num_bytes: 239255087
    num_examples: 7593
  - name: validated
    num_bytes: 8120181903
    num_examples: 251659
  - name: validation
    num_bytes: 196558067
    num_examples: 5213
  download_size: 8884585819
  dataset_size: 10010522039
- config_name: fi
  features:
  - name: client_id
    dtype: string
  - name: path
    dtype: string
  - name: audio
    dtype:
      audio:
        sampling_rate: 48000
  - name: sentence
    dtype: string
  - name: up_votes
    dtype: int64
  - name: down_votes
    dtype: int64
  - name: age
    dtype: string
  - name: gender
    dtype: string
  - name: accent
    dtype: string
  - name: locale
    dtype: string
  - name: segment
    dtype: string
  splits:
  - name: invalidated
    num_bytes: 2228215
    num_examples: 59
  - name: other
    num_bytes: 5836400
    num_examples: 149
  - name: test
    num_bytes: 16117529
    num_examples: 428
  - name: train
    num_bytes: 16017393
    num_examples: 460
  - name: validated
    num_bytes: 47669391
    num_examples: 1305
  - name: validation
    num_bytes: 15471757
    num_examples: 415
  download_size: 49882909
  dataset_size: 103340685
- config_name: fr
  features:
  - name: client_id
    dtype: string
  - name: path
    dtype: string
  - name: audio
    dtype:
      audio:
        sampling_rate: 48000
  - name: sentence
    dtype: string
  - name: up_votes
    dtype: int64
  - name: down_votes
    dtype: int64
  - name: age
    dtype: string
  - name: gender
    dtype: string
  - name: accent
    dtype: string
  - name: locale
    dtype: string
  - name: segment
    dtype: string
  splits:
  - name: invalidated
    num_bytes: 1794149368
    num_examples: 40351
  - name: other
    num_bytes: 117998889
    num_examples: 3222
  - name: test
    num_bytes: 733943163
    num_examples: 15763
  - name: train
    num_bytes: 12439892070
    num_examples: 298982
  - name: validated
    num_bytes: 17921836252
    num_examples: 461004
  - name: validation
    num_bytes: 703801114
    num_examples: 15763
  download_size: 19130141984
  dataset_size: 33711620856
- config_name: fy-NL
  features:
  - name: client_id
    dtype: string
  - name: path
    dtype: string
  - name: audio
    dtype:
      audio:
        sampling_rate: 48000
  - name: sentence
    dtype: string
  - name: up_votes
    dtype: int64
  - name: down_votes
    dtype: int64
  - name: age
    dtype: string
  - name: gender
    dtype: string
  - name: accent
    dtype: string
  - name: locale
    dtype: string
  - name: segment
    dtype: string
  splits:
  - name: invalidated
    num_bytes: 38985422
    num_examples: 1031
  - name: other
    num_bytes: 893887467
    num_examples: 21569
  - name: test
    num_bytes: 126913262
    num_examples: 3020
  - name: train
    num_bytes: 159116360
    num_examples: 3927
  - name: validated
    num_bytes: 429651922
    num_examples: 10495
  - name: validation
    num_bytes: 112288554
    num_examples: 2790
  download_size: 1237743070
  dataset_size: 1760842987
- config_name: ga-IE
  features:
  - name: client_id
    dtype: string
  - name: path
    dtype: string
  - name: audio
    dtype:
      audio:
        sampling_rate: 48000
  - name: sentence
    dtype: string
  - name: up_votes
    dtype: int64
  - name: down_votes
    dtype: int64
  - name: age
    dtype: string
  - name: gender
    dtype: string
  - name: accent
    dtype: string
  - name: locale
    dtype: string
  - name: segment
    dtype: string
  splits:
  - name: invalidated
    num_bytes: 10993268
    num_examples: 409
  - name: other
    num_bytes: 61948768
    num_examples: 2130
  - name: test
    num_bytes: 16611739
    num_examples: 506
  - name: train
    num_bytes: 15396820
    num_examples: 541
  - name: validated
    num_bytes: 93371649
    num_examples: 3352
  - name: validation
    num_bytes: 14897739
    num_examples: 497
  download_size: 156553447
  dataset_size: 213219983
- config_name: hi
  features:
  - name: client_id
    dtype: string
  - name: path
    dtype: string
  - name: audio
    dtype:
      audio:
        sampling_rate: 48000
  - name: sentence
    dtype: string
  - name: up_votes
    dtype: int64
  - name: down_votes
    dtype: int64
  - name: age
    dtype: string
  - name: gender
    dtype: string
  - name: accent
    dtype: string
  - name: locale
    dtype: string
  - name: segment
    dtype: string
  splits:
  - name: invalidated
    num_bytes: 2801051
    num_examples: 60
  - name: other
    num_bytes: 4176110
    num_examples: 139
  - name: test
    num_bytes: 4728043
    num_examples: 127
  - name: train
    num_bytes: 4860737
    num_examples: 157
  - name: validated
    num_bytes: 15158052
    num_examples: 419
  - name: validation
    num_bytes: 5569352
    num_examples: 135
  download_size: 21424045
  dataset_size: 37293345
- config_name: hsb
  features:
  - name: client_id
    dtype: string
  - name: path
    dtype: string
  - name: audio
    dtype:
      audio:
        sampling_rate: 48000
  - name: sentence
    dtype: string
  - name: up_votes
    dtype: int64
  - name: down_votes
    dtype: int64
  - name: age
    dtype: string
  - name: gender
    dtype: string
  - name: accent
    dtype: string
  - name: locale
    dtype: string
  - name: segment
    dtype: string
  splits:
  - name: invalidated
    num_bytes: 5589972
    num_examples: 227
  - name: other
    num_bytes: 3173841
    num_examples: 62
  - name: test
    num_bytes: 20929094
    num_examples: 387
  - name: train
    num_bytes: 43049910
    num_examples: 808
  - name: validated
    num_bytes: 72748422
    num_examples: 1367
  - name: validation
    num_bytes: 8769458
    num_examples: 172
  download_size: 79362060
  dataset_size: 154260697
- config_name: hu
  features:
  - name: client_id
    dtype: string
  - name: path
    dtype: string
  - name: audio
    dtype:
      audio:
        sampling_rate: 48000
  - name: sentence
    dtype: string
  - name: up_votes
    dtype: int64
  - name: down_votes
    dtype: int64
  - name: age
    dtype: string
  - name: gender
    dtype: string
  - name: accent
    dtype: string
  - name: locale
    dtype: string
  - name: segment
    dtype: string
  splits:
  - name: invalidated
    num_bytes: 5881521
    num_examples: 169
  - name: other
    num_bytes: 12051094
    num_examples: 295
  - name: test
    num_bytes: 57056435
    num_examples: 1649
  - name: train
    num_bytes: 126163153
    num_examples: 3348
  - name: validated
    num_bytes: 234307671
    num_examples: 6457
  - name: validation
    num_bytes: 50306925
    num_examples: 1434
  download_size: 242758708
  dataset_size: 485766799
- config_name: ia
  features:
  - name: client_id
    dtype: string
  - name: path
    dtype: string
  - name: audio
    dtype:
      audio:
        sampling_rate: 48000
  - name: sentence
    dtype: string
  - name: up_votes
    dtype: int64
  - name: down_votes
    dtype: int64
  - name: age
    dtype: string
  - name: gender
    dtype: string
  - name: accent
    dtype: string
  - name: locale
    dtype: string
  - name: segment
    dtype: string
  splits:
  - name: invalidated
    num_bytes: 6769573
    num_examples: 192
  - name: other
    num_bytes: 30937041
    num_examples: 1095
  - name: test
    num_bytes: 33204678
    num_examples: 899
  - name: train
    num_bytes: 96577153
    num_examples: 3477
  - name: validated
    num_bytes: 197248304
    num_examples: 5978
  - name: validation
    num_bytes: 67436779
    num_examples: 1601
  download_size: 226499645
  dataset_size: 432173528
- config_name: id
  features:
  - name: client_id
    dtype: string
  - name: path
    dtype: string
  - name: audio
    dtype:
      audio:
        sampling_rate: 48000
  - name: sentence
    dtype: string
  - name: up_votes
    dtype: int64
  - name: down_votes
    dtype: int64
  - name: age
    dtype: string
  - name: gender
    dtype: string
  - name: accent
    dtype: string
  - name: locale
    dtype: string
  - name: segment
    dtype: string
  splits:
  - name: invalidated
    num_bytes: 16566129
    num_examples: 470
  - name: other
    num_bytes: 206578628
    num_examples: 6782
  - name: test
    num_bytes: 60711104
    num_examples: 1844
  - name: train
    num_bytes: 63515863
    num_examples: 2130
  - name: validated
    num_bytes: 272570942
    num_examples: 8696
  - name: validation
    num_bytes: 56963520
    num_examples: 1835
  download_size: 475918233
  dataset_size: 676906186
- config_name: it
  features:
  - name: client_id
    dtype: string
  - name: path
    dtype: string
  - name: audio
    dtype:
      audio:
        sampling_rate: 48000
  - name: sentence
    dtype: string
  - name: up_votes
    dtype: int64
  - name: down_votes
    dtype: int64
  - name: age
    dtype: string
  - name: gender
    dtype: string
  - name: accent
    dtype: string
  - name: locale
    dtype: string
  - name: segment
    dtype: string
  splits:
  - name: invalidated
    num_bytes: 564610354
    num_examples: 12189
  - name: other
    num_bytes: 671213467
    num_examples: 14549
  - name: test
    num_bytes: 656285877
    num_examples: 12928
  - name: train
    num_bytes: 2555546829
    num_examples: 58015
  - name: validated
    num_bytes: 4552252754
    num_examples: 102579
  - name: validation
    num_bytes: 621955330
    num_examples: 12928
  download_size: 5585781573
  dataset_size: 9621864611
- config_name: ja
  features:
  - name: client_id
    dtype: string
  - name: path
    dtype: string
  - name: audio
    dtype:
      audio:
        sampling_rate: 48000
  - name: sentence
    dtype: string
  - name: up_votes
    dtype: int64
  - name: down_votes
    dtype: int64
  - name: age
    dtype: string
  - name: gender
    dtype: string
  - name: accent
    dtype: string
  - name: locale
    dtype: string
  - name: segment
    dtype: string
  splits:
  - name: invalidated
    num_bytes: 17819020
    num_examples: 504
  - name: other
    num_bytes: 34588931
    num_examples: 885
  - name: test
    num_bytes: 26475556
    num_examples: 632
  - name: train
    num_bytes: 27600264
    num_examples: 722
  - name: validated
    num_bytes: 106916400
    num_examples: 3072
  - name: validation
    num_bytes: 22098940
    num_examples: 586
  download_size: 152879796
  dataset_size: 235499111
- config_name: ka
  features:
  - name: client_id
    dtype: string
  - name: path
    dtype: string
  - name: audio
    dtype:
      audio:
        sampling_rate: 48000
  - name: sentence
    dtype: string
  - name: up_votes
    dtype: int64
  - name: down_votes
    dtype: int64
  - name: age
    dtype: string
  - name: gender
    dtype: string
  - name: accent
    dtype: string
  - name: locale
    dtype: string
  - name: segment
    dtype: string
  splits:
  - name: invalidated
    num_bytes: 7004160
    num_examples: 139
  - name: other
    num_bytes: 2144603
    num_examples: 44
  - name: test
    num_bytes: 30301524
    num_examples: 656
  - name: train
    num_bytes: 47790695
    num_examples: 1058
  - name: validated
    num_bytes: 104135978
    num_examples: 2275
  - name: validation
    num_bytes: 24951079
    num_examples: 527
  download_size: 104280554
  dataset_size: 216328039
- config_name: kab
  features:
  - name: client_id
    dtype: string
  - name: path
    dtype: string
  - name: audio
    dtype:
      audio:
        sampling_rate: 48000
  - name: sentence
    dtype: string
  - name: up_votes
    dtype: int64
  - name: down_votes
    dtype: int64
  - name: age
    dtype: string
  - name: gender
    dtype: string
  - name: accent
    dtype: string
  - name: locale
    dtype: string
  - name: segment
    dtype: string
  splits:
  - name: invalidated
    num_bytes: 581587104
    num_examples: 18134
  - name: other
    num_bytes: 2282481767
    num_examples: 88021
  - name: test
    num_bytes: 446453041
    num_examples: 14622
  - name: train
    num_bytes: 3219289101
    num_examples: 120530
  - name: validated
    num_bytes: 15310455176
    num_examples: 573718
  - name: validation
    num_bytes: 414159937
    num_examples: 14622
  download_size: 17171606918
  dataset_size: 22254426126
- config_name: ky
  features:
  - name: client_id
    dtype: string
  - name: path
    dtype: string
  - name: audio
    dtype:
      audio:
        sampling_rate: 48000
  - name: sentence
    dtype: string
  - name: up_votes
    dtype: int64
  - name: down_votes
    dtype: int64
  - name: age
    dtype: string
  - name: gender
    dtype: string
  - name: accent
    dtype: string
  - name: locale
    dtype: string
  - name: segment
    dtype: string
  splits:
  - name: invalidated
    num_bytes: 41007711
    num_examples: 926
  - name: other
    num_bytes: 258081579
    num_examples: 7223
  - name: test
    num_bytes: 57116561
    num_examples: 1503
  - name: train
    num_bytes: 75460488
    num_examples: 1955
  - name: validated
    num_bytes: 355742823
    num_examples: 9236
  - name: validation
    num_bytes: 61393867
    num_examples: 1511
  download_size: 579440853
  dataset_size: 848803029
- config_name: lg
  features:
  - name: client_id
    dtype: string
  - name: path
    dtype: string
  - name: audio
    dtype:
      audio:
        sampling_rate: 48000
  - name: sentence
    dtype: string
  - name: up_votes
    dtype: int64
  - name: down_votes
    dtype: int64
  - name: age
    dtype: string
  - name: gender
    dtype: string
  - name: accent
    dtype: string
  - name: locale
    dtype: string
  - name: segment
    dtype: string
  splits:
  - name: invalidated
    num_bytes: 14069959
    num_examples: 290
  - name: other
    num_bytes: 111180838
    num_examples: 3110
  - name: test
    num_bytes: 26951803
    num_examples: 584
  - name: train
    num_bytes: 46910479
    num_examples: 1250
  - name: validated
    num_bytes: 90606863
    num_examples: 2220
  - name: validation
    num_bytes: 16709367
    num_examples: 384
  download_size: 208197149
  dataset_size: 306429309
- config_name: lt
  features:
  - name: client_id
    dtype: string
  - name: path
    dtype: string
  - name: audio
    dtype:
      audio:
        sampling_rate: 48000
  - name: sentence
    dtype: string
  - name: up_votes
    dtype: int64
  - name: down_votes
    dtype: int64
  - name: age
    dtype: string
  - name: gender
    dtype: string
  - name: accent
    dtype: string
  - name: locale
    dtype: string
  - name: segment
    dtype: string
  splits:
  - name: invalidated
    num_bytes: 4414780
    num_examples: 102
  - name: other
    num_bytes: 71150206
    num_examples: 1629
  - name: test
    num_bytes: 19940391
    num_examples: 466
  - name: train
    num_bytes: 34605356
    num_examples: 931
  - name: validated
    num_bytes: 65138550
    num_examples: 1644
  - name: validation
    num_bytes: 10462851
    num_examples: 244
  download_size: 135299706
  dataset_size: 205712134
- config_name: lv
  features:
  - name: client_id
    dtype: string
  - name: path
    dtype: string
  - name: audio
    dtype:
      audio:
        sampling_rate: 48000
  - name: sentence
    dtype: string
  - name: up_votes
    dtype: int64
  - name: down_votes
    dtype: int64
  - name: age
    dtype: string
  - name: gender
    dtype: string
  - name: accent
    dtype: string
  - name: locale
    dtype: string
  - name: segment
    dtype: string
  splits:
  - name: invalidated
    num_bytes: 4383319
    num_examples: 143
  - name: other
    num_bytes: 40259801
    num_examples: 1560
  - name: test
    num_bytes: 56937435
    num_examples: 1882
  - name: train
    num_bytes: 67269173
    num_examples: 2552
  - name: validated
    num_bytes: 179726893
    num_examples: 6444
  - name: validation
    num_bytes: 55289058
    num_examples: 2002
  download_size: 208307691
  dataset_size: 403865679
- config_name: mn
  features:
  - name: client_id
    dtype: string
  - name: path
    dtype: string
  - name: audio
    dtype:
      audio:
        sampling_rate: 48000
  - name: sentence
    dtype: string
  - name: up_votes
    dtype: int64
  - name: down_votes
    dtype: int64
  - name: age
    dtype: string
  - name: gender
    dtype: string
  - name: accent
    dtype: string
  - name: locale
    dtype: string
  - name: segment
    dtype: string
  splits:
  - name: invalidated
    num_bytes: 31764232
    num_examples: 667
  - name: other
    num_bytes: 146365394
    num_examples: 3272
  - name: test
    num_bytes: 86737041
    num_examples: 1862
  - name: train
    num_bytes: 89913910
    num_examples: 2183
  - name: validated
    num_bytes: 327264827
    num_examples: 7487
  - name: validation
    num_bytes: 82343275
    num_examples: 1837
  download_size: 486369317
  dataset_size: 764388679
- config_name: mt
  features:
  - name: client_id
    dtype: string
  - name: path
    dtype: string
  - name: audio
    dtype:
      audio:
        sampling_rate: 48000
  - name: sentence
    dtype: string
  - name: up_votes
    dtype: int64
  - name: down_votes
    dtype: int64
  - name: age
    dtype: string
  - name: gender
    dtype: string
  - name: accent
    dtype: string
  - name: locale
    dtype: string
  - name: segment
    dtype: string
  splits:
  - name: invalidated
    num_bytes: 12328068
    num_examples: 314
  - name: other
    num_bytes: 220666971
    num_examples: 5714
  - name: test
    num_bytes: 66520195
    num_examples: 1617
  - name: train
    num_bytes: 73850815
    num_examples: 2036
  - name: validated
    num_bytes: 218212969
    num_examples: 5747
  - name: validation
    num_bytes: 56412066
    num_examples: 1516
  download_size: 425114242
  dataset_size: 647991084
- config_name: nl
  features:
  - name: client_id
    dtype: string
  - name: path
    dtype: string
  - name: audio
    dtype:
      audio:
        sampling_rate: 48000
  - name: sentence
    dtype: string
  - name: up_votes
    dtype: int64
  - name: down_votes
    dtype: int64
  - name: age
    dtype: string
  - name: gender
    dtype: string
  - name: accent
    dtype: string
  - name: locale
    dtype: string
  - name: segment
    dtype: string
  splits:
  - name: invalidated
    num_bytes: 115133112
    num_examples: 3308
  - name: other
    num_bytes: 801418
    num_examples: 27
  - name: test
    num_bytes: 205287443
    num_examples: 5708
  - name: train
    num_bytes: 321946148
    num_examples: 9460
  - name: validated
    num_bytes: 1710636990
    num_examples: 52488
  - name: validation
    num_bytes: 186095353
    num_examples: 4938
  download_size: 1741827548
  dataset_size: 2539900464
- config_name: or
  features:
  - name: client_id
    dtype: string
  - name: path
    dtype: string
  - name: audio
    dtype:
      audio:
        sampling_rate: 48000
  - name: sentence
    dtype: string
  - name: up_votes
    dtype: int64
  - name: down_votes
    dtype: int64
  - name: age
    dtype: string
  - name: gender
    dtype: string
  - name: accent
    dtype: string
  - name: locale
    dtype: string
  - name: segment
    dtype: string
  splits:
  - name: invalidated
    num_bytes: 2701922
    num_examples: 62
  - name: other
    num_bytes: 177775963
    num_examples: 4302
  - name: test
    num_bytes: 4270651
    num_examples: 98
  - name: train
    num_bytes: 16067910
    num_examples: 388
  - name: validated
    num_bytes: 25824418
    num_examples: 615
  - name: validation
    num_bytes: 5485937
    num_examples: 129
  download_size: 199077358
  dataset_size: 232126801
- config_name: pa-IN
  features:
  - name: client_id
    dtype: string
  - name: path
    dtype: string
  - name: audio
    dtype:
      audio:
        sampling_rate: 48000
  - name: sentence
    dtype: string
  - name: up_votes
    dtype: int64
  - name: down_votes
    dtype: int64
  - name: age
    dtype: string
  - name: gender
    dtype: string
  - name: accent
    dtype: string
  - name: locale
    dtype: string
  - name: segment
    dtype: string
  splits:
  - name: invalidated
    num_bytes: 1690766
    num_examples: 43
  - name: other
    num_bytes: 56683312
    num_examples: 1411
  - name: test
    num_bytes: 4375532
    num_examples: 116
  - name: train
    num_bytes: 7572499
    num_examples: 211
  - name: validated
    num_bytes: 13650443
    num_examples: 371
  - name: validation
    num_bytes: 1702492
    num_examples: 44
  download_size: 69748265
  dataset_size: 85675044
- config_name: pl
  features:
  - name: client_id
    dtype: string
  - name: path
    dtype: string
  - name: audio
    dtype:
      audio:
        sampling_rate: 48000
  - name: sentence
    dtype: string
  - name: up_votes
    dtype: int64
  - name: down_votes
    dtype: int64
  - name: age
    dtype: string
  - name: gender
    dtype: string
  - name: accent
    dtype: string
  - name: locale
    dtype: string
  - name: segment
    dtype: string
  splits:
  - name: invalidated
    num_bytes: 180801918
    num_examples: 4601
  - name: other
    num_bytes: 442144781
    num_examples: 12848
  - name: test
    num_bytes: 205047541
    num_examples: 5153
  - name: train
    num_bytes: 273394509
    num_examples: 7468
  - name: validated
    num_bytes: 3150860197
    num_examples: 90791
  - name: validation
    num_bytes: 195917307
    num_examples: 5153
  download_size: 3537012341
  dataset_size: 4448166253
- config_name: pt
  features:
  - name: client_id
    dtype: string
  - name: path
    dtype: string
  - name: audio
    dtype:
      audio:
        sampling_rate: 48000
  - name: sentence
    dtype: string
  - name: up_votes
    dtype: int64
  - name: down_votes
    dtype: int64
  - name: age
    dtype: string
  - name: gender
    dtype: string
  - name: accent
    dtype: string
  - name: locale
    dtype: string
  - name: segment
    dtype: string
  splits:
  - name: invalidated
    num_bytes: 67948392
    num_examples: 1740
  - name: other
    num_bytes: 283497435
    num_examples: 8390
  - name: test
    num_bytes: 180108694
    num_examples: 4641
  - name: train
    num_bytes: 231451724
    num_examples: 6514
  - name: validated
    num_bytes: 1480529669
    num_examples: 41584
  - name: validation
    num_bytes: 165966139
    num_examples: 4592
  download_size: 1704252567
  dataset_size: 2409502053
- config_name: rm-sursilv
  features:
  - name: client_id
    dtype: string
  - name: path
    dtype: string
  - name: audio
    dtype:
      audio:
        sampling_rate: 48000
  - name: sentence
    dtype: string
  - name: up_votes
    dtype: int64
  - name: down_votes
    dtype: int64
  - name: age
    dtype: string
  - name: gender
    dtype: string
  - name: accent
    dtype: string
  - name: locale
    dtype: string
  - name: segment
    dtype: string
  splits:
  - name: invalidated
    num_bytes: 30593270
    num_examples: 639
  - name: other
    num_bytes: 93351293
    num_examples: 2102
  - name: test
    num_bytes: 51707733
    num_examples: 1194
  - name: train
    num_bytes: 62396326
    num_examples: 1384
  - name: validated
    num_bytes: 166218231
    num_examples: 3783
  - name: validation
    num_bytes: 52114252
    num_examples: 1205
  download_size: 275950479
  dataset_size: 456381105
- config_name: rm-vallader
  features:
  - name: client_id
    dtype: string
  - name: path
    dtype: string
  - name: audio
    dtype:
      audio:
        sampling_rate: 48000
  - name: sentence
    dtype: string
  - name: up_votes
    dtype: int64
  - name: down_votes
    dtype: int64
  - name: age
    dtype: string
  - name: gender
    dtype: string
  - name: accent
    dtype: string
  - name: locale
    dtype: string
  - name: segment
    dtype: string
  splits:
  - name: invalidated
    num_bytes: 9356204
    num_examples: 374
  - name: other
    num_bytes: 36890435
    num_examples: 727
  - name: test
    num_bytes: 18805466
    num_examples: 378
  - name: train
    num_bytes: 29528457
    num_examples: 574
  - name: validated
    num_bytes: 65711922
    num_examples: 1316
  - name: validation
    num_bytes: 17012341
    num_examples: 357
  download_size: 108113989
  dataset_size: 177304825
- config_name: ro
  features:
  - name: client_id
    dtype: string
  - name: path
    dtype: string
  - name: audio
    dtype:
      audio:
        sampling_rate: 48000
  - name: sentence
    dtype: string
  - name: up_votes
    dtype: int64
  - name: down_votes
    dtype: int64
  - name: age
    dtype: string
  - name: gender
    dtype: string
  - name: accent
    dtype: string
  - name: locale
    dtype: string
  - name: segment
    dtype: string
  splits:
  - name: invalidated
    num_bytes: 11108104
    num_examples: 485
  - name: other
    num_bytes: 65805210
    num_examples: 1945
  - name: test
    num_bytes: 60106568
    num_examples: 1778
  - name: train
    num_bytes: 107235430
    num_examples: 3399
  - name: validated
    num_bytes: 197820619
    num_examples: 6039
  - name: validation
    num_bytes: 30358457
    num_examples: 858
  download_size: 261978702
  dataset_size: 472434388
- config_name: ru
  features:
  - name: client_id
    dtype: string
  - name: path
    dtype: string
  - name: audio
    dtype:
      audio:
        sampling_rate: 48000
  - name: sentence
    dtype: string
  - name: up_votes
    dtype: int64
  - name: down_votes
    dtype: int64
  - name: age
    dtype: string
  - name: gender
    dtype: string
  - name: accent
    dtype: string
  - name: locale
    dtype: string
  - name: segment
    dtype: string
  splits:
  - name: invalidated
    num_bytes: 145739451
    num_examples: 3056
  - name: other
    num_bytes: 450644862
    num_examples: 10247
  - name: test
    num_bytes: 385349488
    num_examples: 8007
  - name: train
    num_bytes: 686168722
    num_examples: 15481
  - name: validated
    num_bytes: 3212213931
    num_examples: 74256
  - name: validation
    num_bytes: 361164462
    num_examples: 7963
  download_size: 3655676916
  dataset_size: 5241280916
- config_name: rw
  features:
  - name: client_id
    dtype: string
  - name: path
    dtype: string
  - name: audio
    dtype:
      audio:
        sampling_rate: 48000
  - name: sentence
    dtype: string
  - name: up_votes
    dtype: int64
  - name: down_votes
    dtype: int64
  - name: age
    dtype: string
  - name: gender
    dtype: string
  - name: accent
    dtype: string
  - name: locale
    dtype: string
  - name: segment
    dtype: string
  splits:
  - name: invalidated
    num_bytes: 7969286423
    num_examples: 206790
  - name: other
    num_bytes: 923146896
    num_examples: 22923
  - name: test
    num_bytes: 707959382
    num_examples: 15724
  - name: train
    num_bytes: 21645788973
    num_examples: 515197
  - name: validated
    num_bytes: 35011249432
    num_examples: 832929
  - name: validation
    num_bytes: 698662384
    num_examples: 15032
  download_size: 42545189583
  dataset_size: 66956093490
- config_name: sah
  features:
  - name: client_id
    dtype: string
  - name: path
    dtype: string
  - name: audio
    dtype:
      audio:
        sampling_rate: 48000
  - name: sentence
    dtype: string
  - name: up_votes
    dtype: int64
  - name: down_votes
    dtype: int64
  - name: age
    dtype: string
  - name: gender
    dtype: string
  - name: accent
    dtype: string
  - name: locale
    dtype: string
  - name: segment
    dtype: string
  splits:
  - name: invalidated
    num_bytes: 3594160
    num_examples: 66
  - name: other
    num_bytes: 62594222
    num_examples: 1275
  - name: test
    num_bytes: 38534020
    num_examples: 757
  - name: train
    num_bytes: 68286985
    num_examples: 1442
  - name: validated
    num_bytes: 124800352
    num_examples: 2606
  - name: validation
    num_bytes: 17900397
    num_examples: 405
  download_size: 181245626
  dataset_size: 315710136
- config_name: sl
  features:
  - name: client_id
    dtype: string
  - name: path
    dtype: string
  - name: audio
    dtype:
      audio:
        sampling_rate: 48000
  - name: sentence
    dtype: string
  - name: up_votes
    dtype: int64
  - name: down_votes
    dtype: int64
  - name: age
    dtype: string
  - name: gender
    dtype: string
  - name: accent
    dtype: string
  - name: locale
    dtype: string
  - name: segment
    dtype: string
  splits:
  - name: invalidated
    num_bytes: 3048301
    num_examples: 92
  - name: other
    num_bytes: 79268518
    num_examples: 2502
  - name: test
    num_bytes: 26872195
    num_examples: 881
  - name: train
    num_bytes: 66122967
    num_examples: 2038
  - name: validated
    num_bytes: 148371273
    num_examples: 4669
  - name: validation
    num_bytes: 16353097
    num_examples: 556
  download_size: 222751292
  dataset_size: 340036351
- config_name: sv-SE
  features:
  - name: client_id
    dtype: string
  - name: path
    dtype: string
  - name: audio
    dtype:
      audio:
        sampling_rate: 48000
  - name: sentence
    dtype: string
  - name: up_votes
    dtype: int64
  - name: down_votes
    dtype: int64
  - name: age
    dtype: string
  - name: gender
    dtype: string
  - name: accent
    dtype: string
  - name: locale
    dtype: string
  - name: segment
    dtype: string
  splits:
  - name: invalidated
    num_bytes: 13462567
    num_examples: 462
  - name: other
    num_bytes: 109970049
    num_examples: 3043
  - name: test
    num_bytes: 59127381
    num_examples: 2027
  - name: train
    num_bytes: 62727263
    num_examples: 2331
  - name: validated
    num_bytes: 327049001
    num_examples: 12552
  - name: validation
    num_bytes: 53846355
    num_examples: 2019
  download_size: 421434184
  dataset_size: 626182616
- config_name: ta
  features:
  - name: client_id
    dtype: string
  - name: path
    dtype: string
  - name: audio
    dtype:
      audio:
        sampling_rate: 48000
  - name: sentence
    dtype: string
  - name: up_votes
    dtype: int64
  - name: down_votes
    dtype: int64
  - name: age
    dtype: string
  - name: gender
    dtype: string
  - name: accent
    dtype: string
  - name: locale
    dtype: string
  - name: segment
    dtype: string
  splits:
  - name: invalidated
    num_bytes: 23587453
    num_examples: 594
  - name: other
    num_bytes: 246650792
    num_examples: 7428
  - name: test
    num_bytes: 67616865
    num_examples: 1781
  - name: train
    num_bytes: 69052658
    num_examples: 2009
  - name: validated
    num_bytes: 438961956
    num_examples: 12652
  - name: validation
    num_bytes: 63248009
    num_examples: 1779
  download_size: 679766097
  dataset_size: 909117733
- config_name: th
  features:
  - name: client_id
    dtype: string
  - name: path
    dtype: string
  - name: audio
    dtype:
      audio:
        sampling_rate: 48000
  - name: sentence
    dtype: string
  - name: up_votes
    dtype: int64
  - name: down_votes
    dtype: int64
  - name: age
    dtype: string
  - name: gender
    dtype: string
  - name: accent
    dtype: string
  - name: locale
    dtype: string
  - name: segment
    dtype: string
  splits:
  - name: invalidated
    num_bytes: 18247080
    num_examples: 467
  - name: other
    num_bytes: 95235301
    num_examples: 2671
  - name: test
    num_bytes: 82030679
    num_examples: 2188
  - name: train
    num_bytes: 100435725
    num_examples: 2917
  - name: validated
    num_bytes: 245734783
    num_examples: 7028
  - name: validation
    num_bytes: 63237632
    num_examples: 1922
  download_size: 341305736
  dataset_size: 604921200
- config_name: tr
  features:
  - name: client_id
    dtype: string
  - name: path
    dtype: string
  - name: audio
    dtype:
      audio:
        sampling_rate: 48000
  - name: sentence
    dtype: string
  - name: up_votes
    dtype: int64
  - name: down_votes
    dtype: int64
  - name: age
    dtype: string
  - name: gender
    dtype: string
  - name: accent
    dtype: string
  - name: locale
    dtype: string
  - name: segment
    dtype: string
  splits:
  - name: invalidated
    num_bytes: 59288266
    num_examples: 1726
  - name: other
    num_bytes: 10954154
    num_examples: 325
  - name: test
    num_bytes: 60268059
    num_examples: 1647
  - name: train
    num_bytes: 57879052
    num_examples: 1831
  - name: validated
    num_bytes: 585777527
    num_examples: 18685
  - name: validation
    num_bytes: 54914798
    num_examples: 1647
  download_size: 620848700
  dataset_size: 829081856
- config_name: tt
  features:
  - name: client_id
    dtype: string
  - name: path
    dtype: string
  - name: audio
    dtype:
      audio:
        sampling_rate: 48000
  - name: sentence
    dtype: string
  - name: up_votes
    dtype: int64
  - name: down_votes
    dtype: int64
  - name: age
    dtype: string
  - name: gender
    dtype: string
  - name: accent
    dtype: string
  - name: locale
    dtype: string
  - name: segment
    dtype: string
  splits:
  - name: invalidated
    num_bytes: 10403128
    num_examples: 287
  - name: other
    num_bytes: 62158038
    num_examples: 1798
  - name: test
    num_bytes: 135120057
    num_examples: 4485
  - name: train
    num_bytes: 348132697
    num_examples: 11211
  - name: validated
    num_bytes: 767791517
    num_examples: 25781
  - name: validation
    num_bytes: 61690964
    num_examples: 2127
  download_size: 777153207
  dataset_size: 1385296401
- config_name: uk
  features:
  - name: client_id
    dtype: string
  - name: path
    dtype: string
  - name: audio
    dtype:
      audio:
        sampling_rate: 48000
  - name: sentence
    dtype: string
  - name: up_votes
    dtype: int64
  - name: down_votes
    dtype: int64
  - name: age
    dtype: string
  - name: gender
    dtype: string
  - name: accent
    dtype: string
  - name: locale
    dtype: string
  - name: segment
    dtype: string
  splits:
  - name: invalidated
    num_bytes: 55745301
    num_examples: 1255
  - name: other
    num_bytes: 327979131
    num_examples: 8161
  - name: test
    num_bytes: 138422211
    num_examples: 3235
  - name: train
    num_bytes: 161925063
    num_examples: 4035
  - name: validated
    num_bytes: 889863965
    num_examples: 22337
  - name: validation
    num_bytes: 135483169
    num_examples: 3236
  download_size: 1218559031
  dataset_size: 1709418840
- config_name: vi
  features:
  - name: client_id
    dtype: string
  - name: path
    dtype: string
  - name: audio
    dtype:
      audio:
        sampling_rate: 48000
  - name: sentence
    dtype: string
  - name: up_votes
    dtype: int64
  - name: down_votes
    dtype: int64
  - name: age
    dtype: string
  - name: gender
    dtype: string
  - name: accent
    dtype: string
  - name: locale
    dtype: string
  - name: segment
    dtype: string
  splits:
  - name: invalidated
    num_bytes: 2981661
    num_examples: 78
  - name: other
    num_bytes: 31315434
    num_examples: 870
  - name: test
    num_bytes: 6656365
    num_examples: 198
  - name: train
    num_bytes: 6244454
    num_examples: 221
  - name: validated
    num_bytes: 19432595
    num_examples: 619
  - name: validation
    num_bytes: 6531856
    num_examples: 200
  download_size: 51929480
  dataset_size: 73162365
- config_name: vot
  features:
  - name: client_id
    dtype: string
  - name: path
    dtype: string
  - name: audio
    dtype:
      audio:
        sampling_rate: 48000
  - name: sentence
    dtype: string
  - name: up_votes
    dtype: int64
  - name: down_votes
    dtype: int64
  - name: age
    dtype: string
  - name: gender
    dtype: string
  - name: accent
    dtype: string
  - name: locale
    dtype: string
  - name: segment
    dtype: string
  splits:
  - name: invalidated
    num_bytes: 107949
    num_examples: 6
  - name: other
    num_bytes: 7963322
    num_examples: 411
  - name: test
  - name: train
    num_bytes: 146467
    num_examples: 3
  - name: validated
    num_bytes: 146467
    num_examples: 3
  - name: validation
  download_size: 7792602
  dataset_size: 8364205
- config_name: zh-CN
  features:
  - name: client_id
    dtype: string
  - name: path
    dtype: string
  - name: audio
    dtype:
      audio:
        sampling_rate: 48000
  - name: sentence
    dtype: string
  - name: up_votes
    dtype: int64
  - name: down_votes
    dtype: int64
  - name: age
    dtype: string
  - name: gender
    dtype: string
  - name: accent
    dtype: string
  - name: locale
    dtype: string
  - name: segment
    dtype: string
  splits:
  - name: invalidated
    num_bytes: 266234479
    num_examples: 5305
  - name: other
    num_bytes: 381264783
    num_examples: 8948
  - name: test
    num_bytes: 420202544
    num_examples: 8760
  - name: train
    num_bytes: 793667379
    num_examples: 18541
  - name: validated
    num_bytes: 1618113625
    num_examples: 36405
  - name: validation
    num_bytes: 396096323
    num_examples: 8743
  download_size: 2184602350
  dataset_size: 3875579133
- config_name: zh-HK
  features:
  - name: client_id
    dtype: string
  - name: path
    dtype: string
  - name: audio
    dtype:
      audio:
        sampling_rate: 48000
  - name: sentence
    dtype: string
  - name: up_votes
    dtype: int64
  - name: down_votes
    dtype: int64
  - name: age
    dtype: string
  - name: gender
    dtype: string
  - name: accent
    dtype: string
  - name: locale
    dtype: string
  - name: segment
    dtype: string
  splits:
  - name: invalidated
    num_bytes: 124170969
    num_examples: 2999
  - name: other
    num_bytes: 1319233252
    num_examples: 38830
  - name: test
    num_bytes: 217627041
    num_examples: 5172
  - name: train
    num_bytes: 221459521
    num_examples: 7506
  - name: validated
    num_bytes: 1482087591
    num_examples: 41835
  - name: validation
    num_bytes: 196071110
    num_examples: 5172
  download_size: 2774145806
  dataset_size: 3560649484
- config_name: zh-TW
  features:
  - name: client_id
    dtype: string
  - name: path
    dtype: string
  - name: audio
    dtype:
      audio:
        sampling_rate: 48000
  - name: sentence
    dtype: string
  - name: up_votes
    dtype: int64
  - name: down_votes
    dtype: int64
  - name: age
    dtype: string
  - name: gender
    dtype: string
  - name: accent
    dtype: string
  - name: locale
    dtype: string
  - name: segment
    dtype: string
  splits:
  - name: invalidated
    num_bytes: 100241443
    num_examples: 3584
  - name: other
    num_bytes: 623801957
    num_examples: 22477
  - name: test
    num_bytes: 85512325
    num_examples: 2895
  - name: train
    num_bytes: 97323787
    num_examples: 3507
  - name: validated
    num_bytes: 1568842090
    num_examples: 61232
  - name: validation
    num_bytes: 80402637
    num_examples: 2895
  download_size: 2182836295
  dataset_size: 2556124239
---

# Dataset Card for common_voice

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

- **Homepage:** https://commonvoice.mozilla.org/en/datasets
- **Repository:** https://github.com/common-voice/common-voice
- **Paper:** https://commonvoice.mozilla.org/en/datasets
- **Leaderboard:** [Needs More Information]
- **Point of Contact:** [Needs More Information]

### Dataset Summary

The Common Voice dataset consists of a unique MP3 and corresponding text file. Many of the 9,283 recorded hours in the dataset also include demographic metadata like age, sex, and accent that can help train the accuracy of speech recognition engines.

The dataset currently consists of 7,335 validated hours in 60 languages, but were always adding more voices and languages. Take a look at our Languages page to request a language or start contributing.

### Supported Tasks and Leaderboards

[Needs More Information]

### Languages

English

## Dataset Structure

### Data Instances

A typical data point comprises the path to the audio file, called path and its sentence. Additional fields include accent, age, client_id, up_votes down_votes, gender, locale and segment.

`
{'accent': 'netherlands', 'age': 'fourties', 'client_id': 'bbbcb732e0f422150c30ff3654bbab572e2a617da107bca22ff8b89ab2e4f124d03b6a92c48322862f60bd0179ae07baf0f9b4f9c4e11d581e0cec70f703ba54', 'down_votes': 0, 'gender': 'male', 'locale': 'nl', 'path': 'nl/clips/common_voice_nl_23522441.mp3', 'segment': "''", 'sentence': 'Ik vind dat een dubieuze procedure.', 'up_votes': 2, 'audio': {'path': `nl/clips/common_voice_nl_23522441.mp3', 'array': array([-0.00048828, -0.00018311, -0.00137329, ...,  0.00079346, 0.00091553,  0.00085449], dtype=float32), 'sampling_rate': 48000}
`

### Data Fields

client_id: An id for which client (voice) made the recording

path: The path to the audio file

audio: A dictionary containing the path to the downloaded audio file, the decoded audio array, and the sampling rate. Note that when accessing the audio column: `dataset[0]["audio"]` the audio file is automatically decoded and resampled to `dataset.features["audio"].sampling_rate`. Decoding and resampling of a large number of audio files might take a significant amount of time. Thus it is important to first query the sample index before the `"audio"` column, *i.e.* `dataset[0]["audio"]` should **always** be preferred over `dataset["audio"][0]`.

sentence: The sentence the user was prompted to speak

up_votes: How many upvotes the audio file has received from reviewers

down_votes: How many downvotes the audio file has received from reviewers

age: The age of the speaker.

gender: The gender of the speaker

accent: Accent of the speaker

locale: The locale of the speaker

segment: Usually empty field

### Data Splits

The speech material has been subdivided into portions for dev, train, test, validated, invalidated, reported and other.

The validated data is data that has been validated with reviewers and recieved upvotes that the data is of high quality.

The invalidated data is data has been invalidated by reviewers
and recieved downvotes that the data is of low quality.

The reported data is data that has been reported, for different reasons.

The other data is data that has not yet been reviewed.

The dev, test, train are all data that has been reviewed, deemed of high quality and split into dev, test and train.

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

The dataset consists of people who have donated their voice online.  You agree to not attempt to determine the identity of speakers in the Common Voice dataset.

## Considerations for Using the Data

### Social Impact of Dataset

The dataset consists of people who have donated their voice online.  You agree to not attempt to determine the identity of speakers in the Common Voice dataset.

### Discussion of Biases

[More Information Needed] 

### Other Known Limitations

[More Information Needed] 

## Additional Information

### Dataset Curators

[More Information Needed] 

### Licensing Information

Public Domain, [CC-0](https://creativecommons.org/share-your-work/public-domain/cc0/)

### Citation Information

```
@inproceedings{commonvoice:2020,
  author = {Ardila, R. and Branson, M. and Davis, K. and Henretty, M. and Kohler, M. and Meyer, J. and Morais, R. and Saunders, L. and Tyers, F. M. and Weber, G.},
  title = {Common Voice: A Massively-Multilingual Speech Corpus},
  booktitle = {Proceedings of the 12th Conference on Language Resources and Evaluation (LREC 2020)},
  pages = {4211--4215},
  year = 2020
}
```

### Contributions

Thanks to [@BirgerMoell](https://github.com/BirgerMoell) for adding this dataset.