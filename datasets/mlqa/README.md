---
pretty_name: MLQA (MultiLingual Question Answering)
language:
- en
- de
- es
- ar
- zh
- vi
- hi
license:
- cc-by-sa-3.0
source_datasets:
- original
size_categories:
- 10K<n<100K
language_creators:
- crowdsourced
annotations_creators:
- crowdsourced
multilinguality:
- multilingual
task_categories:
- question-answering
task_ids:
- extractive-qa
paperswithcode_id: mlqa
dataset_info:
- config_name: mlqa-translate-train.ar
  features:
  - name: context
    dtype: string
  - name: question
    dtype: string
  - name: answers
    sequence:
    - name: answer_start
      dtype: int32
    - name: text
      dtype: string
  - name: id
    dtype: string
  splits:
  - name: train
    num_bytes: 101227245
    num_examples: 78058
  - name: validation
    num_bytes: 13144332
    num_examples: 9512
  download_size: 63364123
  dataset_size: 114371577
- config_name: mlqa-translate-train.de
  features:
  - name: context
    dtype: string
  - name: question
    dtype: string
  - name: answers
    sequence:
    - name: answer_start
      dtype: int32
    - name: text
      dtype: string
  - name: id
    dtype: string
  splits:
  - name: train
    num_bytes: 77996825
    num_examples: 80069
  - name: validation
    num_bytes: 10322113
    num_examples: 9927
  download_size: 63364123
  dataset_size: 88318938
- config_name: mlqa-translate-train.vi
  features:
  - name: context
    dtype: string
  - name: question
    dtype: string
  - name: answers
    sequence:
    - name: answer_start
      dtype: int32
    - name: text
      dtype: string
  - name: id
    dtype: string
  splits:
  - name: train
    num_bytes: 97387431
    num_examples: 84816
  - name: validation
    num_bytes: 12731112
    num_examples: 10356
  download_size: 63364123
  dataset_size: 110118543
- config_name: mlqa-translate-train.zh
  features:
  - name: context
    dtype: string
  - name: question
    dtype: string
  - name: answers
    sequence:
    - name: answer_start
      dtype: int32
    - name: text
      dtype: string
  - name: id
    dtype: string
  splits:
  - name: train
    num_bytes: 55143547
    num_examples: 76285
  - name: validation
    num_bytes: 7418070
    num_examples: 9568
  download_size: 63364123
  dataset_size: 62561617
- config_name: mlqa-translate-train.es
  features:
  - name: context
    dtype: string
  - name: question
    dtype: string
  - name: answers
    sequence:
    - name: answer_start
      dtype: int32
    - name: text
      dtype: string
  - name: id
    dtype: string
  splits:
  - name: train
    num_bytes: 80789653
    num_examples: 81810
  - name: validation
    num_bytes: 10718376
    num_examples: 10123
  download_size: 63364123
  dataset_size: 91508029
- config_name: mlqa-translate-train.hi
  features:
  - name: context
    dtype: string
  - name: question
    dtype: string
  - name: answers
    sequence:
    - name: answer_start
      dtype: int32
    - name: text
      dtype: string
  - name: id
    dtype: string
  splits:
  - name: train
    num_bytes: 168117671
    num_examples: 82451
  - name: validation
    num_bytes: 22422152
    num_examples: 10253
  download_size: 63364123
  dataset_size: 190539823
- config_name: mlqa-translate-test.ar
  features:
  - name: context
    dtype: string
  - name: question
    dtype: string
  - name: answers
    sequence:
    - name: answer_start
      dtype: int32
    - name: text
      dtype: string
  - name: id
    dtype: string
  splits:
  - name: test
    num_bytes: 5484467
    num_examples: 5335
  download_size: 10075488
  dataset_size: 5484467
- config_name: mlqa-translate-test.de
  features:
  - name: context
    dtype: string
  - name: question
    dtype: string
  - name: answers
    sequence:
    - name: answer_start
      dtype: int32
    - name: text
      dtype: string
  - name: id
    dtype: string
  splits:
  - name: test
    num_bytes: 3884332
    num_examples: 4517
  download_size: 10075488
  dataset_size: 3884332
- config_name: mlqa-translate-test.vi
  features:
  - name: context
    dtype: string
  - name: question
    dtype: string
  - name: answers
    sequence:
    - name: answer_start
      dtype: int32
    - name: text
      dtype: string
  - name: id
    dtype: string
  splits:
  - name: test
    num_bytes: 5998327
    num_examples: 5495
  download_size: 10075488
  dataset_size: 5998327
- config_name: mlqa-translate-test.zh
  features:
  - name: context
    dtype: string
  - name: question
    dtype: string
  - name: answers
    sequence:
    - name: answer_start
      dtype: int32
    - name: text
      dtype: string
  - name: id
    dtype: string
  splits:
  - name: test
    num_bytes: 4831704
    num_examples: 5137
  download_size: 10075488
  dataset_size: 4831704
- config_name: mlqa-translate-test.es
  features:
  - name: context
    dtype: string
  - name: question
    dtype: string
  - name: answers
    sequence:
    - name: answer_start
      dtype: int32
    - name: text
      dtype: string
  - name: id
    dtype: string
  splits:
  - name: test
    num_bytes: 3916758
    num_examples: 5253
  download_size: 10075488
  dataset_size: 3916758
- config_name: mlqa-translate-test.hi
  features:
  - name: context
    dtype: string
  - name: question
    dtype: string
  - name: answers
    sequence:
    - name: answer_start
      dtype: int32
    - name: text
      dtype: string
  - name: id
    dtype: string
  splits:
  - name: test
    num_bytes: 4608811
    num_examples: 4918
  download_size: 10075488
  dataset_size: 4608811
- config_name: mlqa.ar.ar
  features:
  - name: context
    dtype: string
  - name: question
    dtype: string
  - name: answers
    sequence:
    - name: answer_start
      dtype: int32
    - name: text
      dtype: string
  - name: id
    dtype: string
  splits:
  - name: test
    num_bytes: 8216837
    num_examples: 5335
  - name: validation
    num_bytes: 808830
    num_examples: 517
  download_size: 75719050
  dataset_size: 9025667
- config_name: mlqa.ar.de
  features:
  - name: context
    dtype: string
  - name: question
    dtype: string
  - name: answers
    sequence:
    - name: answer_start
      dtype: int32
    - name: text
      dtype: string
  - name: id
    dtype: string
  splits:
  - name: test
    num_bytes: 2132247
    num_examples: 1649
  - name: validation
    num_bytes: 358554
    num_examples: 207
  download_size: 75719050
  dataset_size: 2490801
- config_name: mlqa.ar.vi
  features:
  - name: context
    dtype: string
  - name: question
    dtype: string
  - name: answers
    sequence:
    - name: answer_start
      dtype: int32
    - name: text
      dtype: string
  - name: id
    dtype: string
  splits:
  - name: test
    num_bytes: 3235363
    num_examples: 2047
  - name: validation
    num_bytes: 283834
    num_examples: 163
  download_size: 75719050
  dataset_size: 3519197
- config_name: mlqa.ar.zh
  features:
  - name: context
    dtype: string
  - name: question
    dtype: string
  - name: answers
    sequence:
    - name: answer_start
      dtype: int32
    - name: text
      dtype: string
  - name: id
    dtype: string
  splits:
  - name: test
    num_bytes: 3175660
    num_examples: 1912
  - name: validation
    num_bytes: 334016
    num_examples: 188
  download_size: 75719050
  dataset_size: 3509676
- config_name: mlqa.ar.en
  features:
  - name: context
    dtype: string
  - name: question
    dtype: string
  - name: answers
    sequence:
    - name: answer_start
      dtype: int32
    - name: text
      dtype: string
  - name: id
    dtype: string
  splits:
  - name: test
    num_bytes: 8074057
    num_examples: 5335
  - name: validation
    num_bytes: 794775
    num_examples: 517
  download_size: 75719050
  dataset_size: 8868832
- config_name: mlqa.ar.es
  features:
  - name: context
    dtype: string
  - name: question
    dtype: string
  - name: answers
    sequence:
    - name: answer_start
      dtype: int32
    - name: text
      dtype: string
  - name: id
    dtype: string
  splits:
  - name: test
    num_bytes: 2981237
    num_examples: 1978
  - name: validation
    num_bytes: 223188
    num_examples: 161
  download_size: 75719050
  dataset_size: 3204425
- config_name: mlqa.ar.hi
  features:
  - name: context
    dtype: string
  - name: question
    dtype: string
  - name: answers
    sequence:
    - name: answer_start
      dtype: int32
    - name: text
      dtype: string
  - name: id
    dtype: string
  splits:
  - name: test
    num_bytes: 2993225
    num_examples: 1831
  - name: validation
    num_bytes: 276727
    num_examples: 186
  download_size: 75719050
  dataset_size: 3269952
- config_name: mlqa.de.ar
  features:
  - name: context
    dtype: string
  - name: question
    dtype: string
  - name: answers
    sequence:
    - name: answer_start
      dtype: int32
    - name: text
      dtype: string
  - name: id
    dtype: string
  splits:
  - name: test
    num_bytes: 1587005
    num_examples: 1649
  - name: validation
    num_bytes: 195822
    num_examples: 207
  download_size: 75719050
  dataset_size: 1782827
- config_name: mlqa.de.de
  features:
  - name: context
    dtype: string
  - name: question
    dtype: string
  - name: answers
    sequence:
    - name: answer_start
      dtype: int32
    - name: text
      dtype: string
  - name: id
    dtype: string
  splits:
  - name: test
    num_bytes: 4274496
    num_examples: 4517
  - name: validation
    num_bytes: 477366
    num_examples: 512
  download_size: 75719050
  dataset_size: 4751862
- config_name: mlqa.de.vi
  features:
  - name: context
    dtype: string
  - name: question
    dtype: string
  - name: answers
    sequence:
    - name: answer_start
      dtype: int32
    - name: text
      dtype: string
  - name: id
    dtype: string
  splits:
  - name: test
    num_bytes: 1654540
    num_examples: 1675
  - name: validation
    num_bytes: 211985
    num_examples: 182
  download_size: 75719050
  dataset_size: 1866525
- config_name: mlqa.de.zh
  features:
  - name: context
    dtype: string
  - name: question
    dtype: string
  - name: answers
    sequence:
    - name: answer_start
      dtype: int32
    - name: text
      dtype: string
  - name: id
    dtype: string
  splits:
  - name: test
    num_bytes: 1645937
    num_examples: 1621
  - name: validation
    num_bytes: 180114
    num_examples: 190
  download_size: 75719050
  dataset_size: 1826051
- config_name: mlqa.de.en
  features:
  - name: context
    dtype: string
  - name: question
    dtype: string
  - name: answers
    sequence:
    - name: answer_start
      dtype: int32
    - name: text
      dtype: string
  - name: id
    dtype: string
  splits:
  - name: test
    num_bytes: 4251153
    num_examples: 4517
  - name: validation
    num_bytes: 474863
    num_examples: 512
  download_size: 75719050
  dataset_size: 4726016
- config_name: mlqa.de.es
  features:
  - name: context
    dtype: string
  - name: question
    dtype: string
  - name: answers
    sequence:
    - name: answer_start
      dtype: int32
    - name: text
      dtype: string
  - name: id
    dtype: string
  splits:
  - name: test
    num_bytes: 1678176
    num_examples: 1776
  - name: validation
    num_bytes: 166193
    num_examples: 196
  download_size: 75719050
  dataset_size: 1844369
- config_name: mlqa.de.hi
  features:
  - name: context
    dtype: string
  - name: question
    dtype: string
  - name: answers
    sequence:
    - name: answer_start
      dtype: int32
    - name: text
      dtype: string
  - name: id
    dtype: string
  splits:
  - name: test
    num_bytes: 1343983
    num_examples: 1430
  - name: validation
    num_bytes: 150679
    num_examples: 163
  download_size: 75719050
  dataset_size: 1494662
- config_name: mlqa.vi.ar
  features:
  - name: context
    dtype: string
  - name: question
    dtype: string
  - name: answers
    sequence:
    - name: answer_start
      dtype: int32
    - name: text
      dtype: string
  - name: id
    dtype: string
  splits:
  - name: test
    num_bytes: 3164094
    num_examples: 2047
  - name: validation
    num_bytes: 226724
    num_examples: 163
  download_size: 75719050
  dataset_size: 3390818
- config_name: mlqa.vi.de
  features:
  - name: context
    dtype: string
  - name: question
    dtype: string
  - name: answers
    sequence:
    - name: answer_start
      dtype: int32
    - name: text
      dtype: string
  - name: id
    dtype: string
  splits:
  - name: test
    num_bytes: 2189315
    num_examples: 1675
  - name: validation
    num_bytes: 272794
    num_examples: 182
  download_size: 75719050
  dataset_size: 2462109
- config_name: mlqa.vi.vi
  features:
  - name: context
    dtype: string
  - name: question
    dtype: string
  - name: answers
    sequence:
    - name: answer_start
      dtype: int32
    - name: text
      dtype: string
  - name: id
    dtype: string
  splits:
  - name: test
    num_bytes: 7807045
    num_examples: 5495
  - name: validation
    num_bytes: 715291
    num_examples: 511
  download_size: 75719050
  dataset_size: 8522336
- config_name: mlqa.vi.zh
  features:
  - name: context
    dtype: string
  - name: question
    dtype: string
  - name: answers
    sequence:
    - name: answer_start
      dtype: int32
    - name: text
      dtype: string
  - name: id
    dtype: string
  splits:
  - name: test
    num_bytes: 2947458
    num_examples: 1943
  - name: validation
    num_bytes: 265154
    num_examples: 184
  download_size: 75719050
  dataset_size: 3212612
- config_name: mlqa.vi.en
  features:
  - name: context
    dtype: string
  - name: question
    dtype: string
  - name: answers
    sequence:
    - name: answer_start
      dtype: int32
    - name: text
      dtype: string
  - name: id
    dtype: string
  splits:
  - name: test
    num_bytes: 7727204
    num_examples: 5495
  - name: validation
    num_bytes: 707925
    num_examples: 511
  download_size: 75719050
  dataset_size: 8435129
- config_name: mlqa.vi.es
  features:
  - name: context
    dtype: string
  - name: question
    dtype: string
  - name: answers
    sequence:
    - name: answer_start
      dtype: int32
    - name: text
      dtype: string
  - name: id
    dtype: string
  splits:
  - name: test
    num_bytes: 2822481
    num_examples: 2018
  - name: validation
    num_bytes: 279235
    num_examples: 189
  download_size: 75719050
  dataset_size: 3101716
- config_name: mlqa.vi.hi
  features:
  - name: context
    dtype: string
  - name: question
    dtype: string
  - name: answers
    sequence:
    - name: answer_start
      dtype: int32
    - name: text
      dtype: string
  - name: id
    dtype: string
  splits:
  - name: test
    num_bytes: 2738045
    num_examples: 1947
  - name: validation
    num_bytes: 251470
    num_examples: 177
  download_size: 75719050
  dataset_size: 2989515
- config_name: mlqa.zh.ar
  features:
  - name: context
    dtype: string
  - name: question
    dtype: string
  - name: answers
    sequence:
    - name: answer_start
      dtype: int32
    - name: text
      dtype: string
  - name: id
    dtype: string
  splits:
  - name: test
    num_bytes: 1697005
    num_examples: 1912
  - name: validation
    num_bytes: 171743
    num_examples: 188
  download_size: 75719050
  dataset_size: 1868748
- config_name: mlqa.zh.de
  features:
  - name: context
    dtype: string
  - name: question
    dtype: string
  - name: answers
    sequence:
    - name: answer_start
      dtype: int32
    - name: text
      dtype: string
  - name: id
    dtype: string
  splits:
  - name: test
    num_bytes: 1356268
    num_examples: 1621
  - name: validation
    num_bytes: 170686
    num_examples: 190
  download_size: 75719050
  dataset_size: 1526954
- config_name: mlqa.zh.vi
  features:
  - name: context
    dtype: string
  - name: question
    dtype: string
  - name: answers
    sequence:
    - name: answer_start
      dtype: int32
    - name: text
      dtype: string
  - name: id
    dtype: string
  splits:
  - name: test
    num_bytes: 1770535
    num_examples: 1943
  - name: validation
    num_bytes: 169651
    num_examples: 184
  download_size: 75719050
  dataset_size: 1940186
- config_name: mlqa.zh.zh
  features:
  - name: context
    dtype: string
  - name: question
    dtype: string
  - name: answers
    sequence:
    - name: answer_start
      dtype: int32
    - name: text
      dtype: string
  - name: id
    dtype: string
  splits:
  - name: test
    num_bytes: 4324740
    num_examples: 5137
  - name: validation
    num_bytes: 433960
    num_examples: 504
  download_size: 75719050
  dataset_size: 4758700
- config_name: mlqa.zh.en
  features:
  - name: context
    dtype: string
  - name: question
    dtype: string
  - name: answers
    sequence:
    - name: answer_start
      dtype: int32
    - name: text
      dtype: string
  - name: id
    dtype: string
  splits:
  - name: test
    num_bytes: 4353361
    num_examples: 5137
  - name: validation
    num_bytes: 437016
    num_examples: 504
  download_size: 75719050
  dataset_size: 4790377
- config_name: mlqa.zh.es
  features:
  - name: context
    dtype: string
  - name: question
    dtype: string
  - name: answers
    sequence:
    - name: answer_start
      dtype: int32
    - name: text
      dtype: string
  - name: id
    dtype: string
  splits:
  - name: test
    num_bytes: 1697983
    num_examples: 1947
  - name: validation
    num_bytes: 134693
    num_examples: 161
  download_size: 75719050
  dataset_size: 1832676
- config_name: mlqa.zh.hi
  features:
  - name: context
    dtype: string
  - name: question
    dtype: string
  - name: answers
    sequence:
    - name: answer_start
      dtype: int32
    - name: text
      dtype: string
  - name: id
    dtype: string
  splits:
  - name: test
    num_bytes: 1547159
    num_examples: 1767
  - name: validation
    num_bytes: 180928
    num_examples: 189
  download_size: 75719050
  dataset_size: 1728087
- config_name: mlqa.en.ar
  features:
  - name: context
    dtype: string
  - name: question
    dtype: string
  - name: answers
    sequence:
    - name: answer_start
      dtype: int32
    - name: text
      dtype: string
  - name: id
    dtype: string
  splits:
  - name: test
    num_bytes: 6641971
    num_examples: 5335
  - name: validation
    num_bytes: 621075
    num_examples: 517
  download_size: 75719050
  dataset_size: 7263046
- config_name: mlqa.en.de
  features:
  - name: context
    dtype: string
  - name: question
    dtype: string
  - name: answers
    sequence:
    - name: answer_start
      dtype: int32
    - name: text
      dtype: string
  - name: id
    dtype: string
  splits:
  - name: test
    num_bytes: 4966262
    num_examples: 4517
  - name: validation
    num_bytes: 584725
    num_examples: 512
  download_size: 75719050
  dataset_size: 5550987
- config_name: mlqa.en.vi
  features:
  - name: context
    dtype: string
  - name: question
    dtype: string
  - name: answers
    sequence:
    - name: answer_start
      dtype: int32
    - name: text
      dtype: string
  - name: id
    dtype: string
  splits:
  - name: test
    num_bytes: 6958087
    num_examples: 5495
  - name: validation
    num_bytes: 631268
    num_examples: 511
  download_size: 75719050
  dataset_size: 7589355
- config_name: mlqa.en.zh
  features:
  - name: context
    dtype: string
  - name: question
    dtype: string
  - name: answers
    sequence:
    - name: answer_start
      dtype: int32
    - name: text
      dtype: string
  - name: id
    dtype: string
  splits:
  - name: test
    num_bytes: 6441614
    num_examples: 5137
  - name: validation
    num_bytes: 598772
    num_examples: 504
  download_size: 75719050
  dataset_size: 7040386
- config_name: mlqa.en.en
  features:
  - name: context
    dtype: string
  - name: question
    dtype: string
  - name: answers
    sequence:
    - name: answer_start
      dtype: int32
    - name: text
      dtype: string
  - name: id
    dtype: string
  splits:
  - name: test
    num_bytes: 13787522
    num_examples: 11590
  - name: validation
    num_bytes: 1307399
    num_examples: 1148
  download_size: 75719050
  dataset_size: 15094921
- config_name: mlqa.en.es
  features:
  - name: context
    dtype: string
  - name: question
    dtype: string
  - name: answers
    sequence:
    - name: answer_start
      dtype: int32
    - name: text
      dtype: string
  - name: id
    dtype: string
  splits:
  - name: test
    num_bytes: 6074990
    num_examples: 5253
  - name: validation
    num_bytes: 545657
    num_examples: 500
  download_size: 75719050
  dataset_size: 6620647
- config_name: mlqa.en.hi
  features:
  - name: context
    dtype: string
  - name: question
    dtype: string
  - name: answers
    sequence:
    - name: answer_start
      dtype: int32
    - name: text
      dtype: string
  - name: id
    dtype: string
  splits:
  - name: test
    num_bytes: 6293785
    num_examples: 4918
  - name: validation
    num_bytes: 614223
    num_examples: 507
  download_size: 75719050
  dataset_size: 6908008
- config_name: mlqa.es.ar
  features:
  - name: context
    dtype: string
  - name: question
    dtype: string
  - name: answers
    sequence:
    - name: answer_start
      dtype: int32
    - name: text
      dtype: string
  - name: id
    dtype: string
  splits:
  - name: test
    num_bytes: 1696778
    num_examples: 1978
  - name: validation
    num_bytes: 145105
    num_examples: 161
  download_size: 75719050
  dataset_size: 1841883
- config_name: mlqa.es.de
  features:
  - name: context
    dtype: string
  - name: question
    dtype: string
  - name: answers
    sequence:
    - name: answer_start
      dtype: int32
    - name: text
      dtype: string
  - name: id
    dtype: string
  splits:
  - name: test
    num_bytes: 1361983
    num_examples: 1776
  - name: validation
    num_bytes: 139968
    num_examples: 196
  download_size: 75719050
  dataset_size: 1501951
- config_name: mlqa.es.vi
  features:
  - name: context
    dtype: string
  - name: question
    dtype: string
  - name: answers
    sequence:
    - name: answer_start
      dtype: int32
    - name: text
      dtype: string
  - name: id
    dtype: string
  splits:
  - name: test
    num_bytes: 1707141
    num_examples: 2018
  - name: validation
    num_bytes: 172801
    num_examples: 189
  download_size: 75719050
  dataset_size: 1879942
- config_name: mlqa.es.zh
  features:
  - name: context
    dtype: string
  - name: question
    dtype: string
  - name: answers
    sequence:
    - name: answer_start
      dtype: int32
    - name: text
      dtype: string
  - name: id
    dtype: string
  splits:
  - name: test
    num_bytes: 1635294
    num_examples: 1947
  - name: validation
    num_bytes: 122829
    num_examples: 161
  download_size: 75719050
  dataset_size: 1758123
- config_name: mlqa.es.en
  features:
  - name: context
    dtype: string
  - name: question
    dtype: string
  - name: answers
    sequence:
    - name: answer_start
      dtype: int32
    - name: text
      dtype: string
  - name: id
    dtype: string
  splits:
  - name: test
    num_bytes: 4249431
    num_examples: 5253
  - name: validation
    num_bytes: 408169
    num_examples: 500
  download_size: 75719050
  dataset_size: 4657600
- config_name: mlqa.es.es
  features:
  - name: context
    dtype: string
  - name: question
    dtype: string
  - name: answers
    sequence:
    - name: answer_start
      dtype: int32
    - name: text
      dtype: string
  - name: id
    dtype: string
  splits:
  - name: test
    num_bytes: 4281273
    num_examples: 5253
  - name: validation
    num_bytes: 411196
    num_examples: 500
  download_size: 75719050
  dataset_size: 4692469
- config_name: mlqa.es.hi
  features:
  - name: context
    dtype: string
  - name: question
    dtype: string
  - name: answers
    sequence:
    - name: answer_start
      dtype: int32
    - name: text
      dtype: string
  - name: id
    dtype: string
  splits:
  - name: test
    num_bytes: 1489611
    num_examples: 1723
  - name: validation
    num_bytes: 178003
    num_examples: 187
  download_size: 75719050
  dataset_size: 1667614
- config_name: mlqa.hi.ar
  features:
  - name: context
    dtype: string
  - name: question
    dtype: string
  - name: answers
    sequence:
    - name: answer_start
      dtype: int32
    - name: text
      dtype: string
  - name: id
    dtype: string
  splits:
  - name: test
    num_bytes: 4374373
    num_examples: 1831
  - name: validation
    num_bytes: 402817
    num_examples: 186
  download_size: 75719050
  dataset_size: 4777190
- config_name: mlqa.hi.de
  features:
  - name: context
    dtype: string
  - name: question
    dtype: string
  - name: answers
    sequence:
    - name: answer_start
      dtype: int32
    - name: text
      dtype: string
  - name: id
    dtype: string
  splits:
  - name: test
    num_bytes: 2961556
    num_examples: 1430
  - name: validation
    num_bytes: 294325
    num_examples: 163
  download_size: 75719050
  dataset_size: 3255881
- config_name: mlqa.hi.vi
  features:
  - name: context
    dtype: string
  - name: question
    dtype: string
  - name: answers
    sequence:
    - name: answer_start
      dtype: int32
    - name: text
      dtype: string
  - name: id
    dtype: string
  splits:
  - name: test
    num_bytes: 4664436
    num_examples: 1947
  - name: validation
    num_bytes: 411654
    num_examples: 177
  download_size: 75719050
  dataset_size: 5076090
- config_name: mlqa.hi.zh
  features:
  - name: context
    dtype: string
  - name: question
    dtype: string
  - name: answers
    sequence:
    - name: answer_start
      dtype: int32
    - name: text
      dtype: string
  - name: id
    dtype: string
  splits:
  - name: test
    num_bytes: 4281309
    num_examples: 1767
  - name: validation
    num_bytes: 416192
    num_examples: 189
  download_size: 75719050
  dataset_size: 4697501
- config_name: mlqa.hi.en
  features:
  - name: context
    dtype: string
  - name: question
    dtype: string
  - name: answers
    sequence:
    - name: answer_start
      dtype: int32
    - name: text
      dtype: string
  - name: id
    dtype: string
  splits:
  - name: test
    num_bytes: 11245629
    num_examples: 4918
  - name: validation
    num_bytes: 1076115
    num_examples: 507
  download_size: 75719050
  dataset_size: 12321744
- config_name: mlqa.hi.es
  features:
  - name: context
    dtype: string
  - name: question
    dtype: string
  - name: answers
    sequence:
    - name: answer_start
      dtype: int32
    - name: text
      dtype: string
  - name: id
    dtype: string
  splits:
  - name: test
    num_bytes: 3789337
    num_examples: 1723
  - name: validation
    num_bytes: 412469
    num_examples: 187
  download_size: 75719050
  dataset_size: 4201806
- config_name: mlqa.hi.hi
  features:
  - name: context
    dtype: string
  - name: question
    dtype: string
  - name: answers
    sequence:
    - name: answer_start
      dtype: int32
    - name: text
      dtype: string
  - name: id
    dtype: string
  splits:
  - name: test
    num_bytes: 11606982
    num_examples: 4918
  - name: validation
    num_bytes: 1115055
    num_examples: 507
  download_size: 75719050
  dataset_size: 12722037
---

# Dataset Card for "mlqa"

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

- **Homepage:** [https://github.com/facebookresearch/MLQA](https://github.com/facebookresearch/MLQA)
- **Repository:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Paper:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Point of Contact:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Size of downloaded dataset files:** 3958.58 MB
- **Size of the generated dataset:** 867.85 MB
- **Total amount of disk used:** 4826.43 MB

### Dataset Summary

    MLQA (MultiLingual Question Answering) is a benchmark dataset for evaluating cross-lingual question answering performance.
    MLQA consists of over 5K extractive QA instances (12K in English) in SQuAD format in seven languages - English, Arabic,
    German, Spanish, Hindi, Vietnamese and Simplified Chinese. MLQA is highly parallel, with QA instances parallel between
    4 different languages on average.

### Supported Tasks and Leaderboards

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Languages

MLQA contains QA instances in 7 languages, English, Arabic, German, Spanish, Hindi, Vietnamese and Simplified Chinese.

## Dataset Structure

### Data Instances

#### mlqa-translate-test.ar

- **Size of downloaded dataset files:** 9.61 MB
- **Size of the generated dataset:** 5.23 MB
- **Total amount of disk used:** 14.84 MB

An example of 'test' looks as follows.
```

```

#### mlqa-translate-test.de

- **Size of downloaded dataset files:** 9.61 MB
- **Size of the generated dataset:** 3.70 MB
- **Total amount of disk used:** 13.31 MB

An example of 'test' looks as follows.
```

```

#### mlqa-translate-test.es

- **Size of downloaded dataset files:** 9.61 MB
- **Size of the generated dataset:** 3.74 MB
- **Total amount of disk used:** 13.34 MB

An example of 'test' looks as follows.
```

```

#### mlqa-translate-test.hi

- **Size of downloaded dataset files:** 9.61 MB
- **Size of the generated dataset:** 4.40 MB
- **Total amount of disk used:** 14.00 MB

An example of 'test' looks as follows.
```

```

#### mlqa-translate-test.vi

- **Size of downloaded dataset files:** 9.61 MB
- **Size of the generated dataset:** 5.72 MB
- **Total amount of disk used:** 15.33 MB

An example of 'test' looks as follows.
```

```

### Data Fields

The data fields are the same among all splits.

#### mlqa-translate-test.ar
- `context`: a `string` feature.
- `question`: a `string` feature.
- `answers`: a dictionary feature containing:
  - `answer_start`: a `int32` feature.
  - `text`: a `string` feature.
- `id`: a `string` feature.

#### mlqa-translate-test.de
- `context`: a `string` feature.
- `question`: a `string` feature.
- `answers`: a dictionary feature containing:
  - `answer_start`: a `int32` feature.
  - `text`: a `string` feature.
- `id`: a `string` feature.

#### mlqa-translate-test.es
- `context`: a `string` feature.
- `question`: a `string` feature.
- `answers`: a dictionary feature containing:
  - `answer_start`: a `int32` feature.
  - `text`: a `string` feature.
- `id`: a `string` feature.

#### mlqa-translate-test.hi
- `context`: a `string` feature.
- `question`: a `string` feature.
- `answers`: a dictionary feature containing:
  - `answer_start`: a `int32` feature.
  - `text`: a `string` feature.
- `id`: a `string` feature.

#### mlqa-translate-test.vi
- `context`: a `string` feature.
- `question`: a `string` feature.
- `answers`: a dictionary feature containing:
  - `answer_start`: a `int32` feature.
  - `text`: a `string` feature.
- `id`: a `string` feature.

### Data Splits

|         name         |test|
|----------------------|---:|
|mlqa-translate-test.ar|5335|
|mlqa-translate-test.de|4517|
|mlqa-translate-test.es|5253|
|mlqa-translate-test.hi|4918|
|mlqa-translate-test.vi|5495|

## Dataset Creation

### Curation Rationale

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Source Data

#### Initial Data Collection and Normalization

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

#### Who are the source language producers?

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Annotations

#### Annotation process

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

#### Who are the annotators?

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Personal and Sensitive Information

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

## Considerations for Using the Data

### Social Impact of Dataset

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Discussion of Biases

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Other Known Limitations

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

## Additional Information

### Dataset Curators

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Licensing Information

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Citation Information

```
@article{lewis2019mlqa,
  title = {MLQA: Evaluating Cross-lingual Extractive Question Answering},
  author = {Lewis, Patrick and Oguz, Barlas and Rinott, Ruty and Riedel, Sebastian and Schwenk, Holger},
  journal = {arXiv preprint arXiv:1910.07475},
  year = 2019,
  eid = {arXiv: 1910.07475}
}

```


### Contributions

Thanks to [@patrickvonplaten](https://github.com/patrickvonplaten), [@M-Salti](https://github.com/M-Salti), [@lewtun](https://github.com/lewtun), [@thomwolf](https://github.com/thomwolf), [@mariamabarham](https://github.com/mariamabarham), [@lhoestq](https://github.com/lhoestq) for adding this dataset.