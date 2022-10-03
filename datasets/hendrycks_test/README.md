---
annotations_creators:
- no-annotation
language_creators:
- expert-generated
language:
- en
language_bcp47:
- en-US
license:
- mit
multilinguality:
- monolingual
size_categories:
- 10K<n<100K
source_datasets:
- original
task_categories:
- question-answering
task_ids:
- multiple-choice-qa
pretty_name: HendrycksTest
dataset_info:
- config_name: abstract_algebra
  features:
  - name: question
    dtype: string
  - name: choices
    sequence: string
  - name: answer
    dtype:
      class_label:
        names:
          0: A
          1: B
          2: C
          3: D
  splits:
  - name: auxiliary_train
    num_bytes: 160601377
    num_examples: 99842
  - name: dev
    num_bytes: 830
    num_examples: 5
  - name: test
    num_bytes: 19328
    num_examples: 100
  - name: validation
    num_bytes: 2024
    num_examples: 11
  download_size: 166184960
  dataset_size: 160623559
- config_name: anatomy
  features:
  - name: question
    dtype: string
  - name: choices
    sequence: string
  - name: answer
    dtype:
      class_label:
        names:
          0: A
          1: B
          2: C
          3: D
  splits:
  - name: auxiliary_train
    num_bytes: 160601377
    num_examples: 99842
  - name: dev
    num_bytes: 967
    num_examples: 5
  - name: test
    num_bytes: 33121
    num_examples: 135
  - name: validation
    num_bytes: 3140
    num_examples: 14
  download_size: 166184960
  dataset_size: 160638605
- config_name: astronomy
  features:
  - name: question
    dtype: string
  - name: choices
    sequence: string
  - name: answer
    dtype:
      class_label:
        names:
          0: A
          1: B
          2: C
          3: D
  splits:
  - name: auxiliary_train
    num_bytes: 160601377
    num_examples: 99842
  - name: dev
    num_bytes: 2076
    num_examples: 5
  - name: test
    num_bytes: 46771
    num_examples: 152
  - name: validation
    num_bytes: 5027
    num_examples: 16
  download_size: 166184960
  dataset_size: 160655251
- config_name: business_ethics
  features:
  - name: question
    dtype: string
  - name: choices
    sequence: string
  - name: answer
    dtype:
      class_label:
        names:
          0: A
          1: B
          2: C
          3: D
  splits:
  - name: auxiliary_train
    num_bytes: 160601377
    num_examples: 99842
  - name: dev
    num_bytes: 2190
    num_examples: 5
  - name: test
    num_bytes: 33252
    num_examples: 100
  - name: validation
    num_bytes: 3038
    num_examples: 11
  download_size: 166184960
  dataset_size: 160639857
- config_name: clinical_knowledge
  features:
  - name: question
    dtype: string
  - name: choices
    sequence: string
  - name: answer
    dtype:
      class_label:
        names:
          0: A
          1: B
          2: C
          3: D
  splits:
  - name: auxiliary_train
    num_bytes: 160601377
    num_examples: 99842
  - name: dev
    num_bytes: 1210
    num_examples: 5
  - name: test
    num_bytes: 62754
    num_examples: 265
  - name: validation
    num_bytes: 6664
    num_examples: 29
  download_size: 166184960
  dataset_size: 160672005
- config_name: college_biology
  features:
  - name: question
    dtype: string
  - name: choices
    sequence: string
  - name: answer
    dtype:
      class_label:
        names:
          0: A
          1: B
          2: C
          3: D
  splits:
  - name: auxiliary_train
    num_bytes: 160601377
    num_examples: 99842
  - name: dev
    num_bytes: 1532
    num_examples: 5
  - name: test
    num_bytes: 48797
    num_examples: 144
  - name: validation
    num_bytes: 4819
    num_examples: 16
  download_size: 166184960
  dataset_size: 160656525
- config_name: college_chemistry
  features:
  - name: question
    dtype: string
  - name: choices
    sequence: string
  - name: answer
    dtype:
      class_label:
        names:
          0: A
          1: B
          2: C
          3: D
  splits:
  - name: auxiliary_train
    num_bytes: 160601377
    num_examples: 99842
  - name: dev
    num_bytes: 1331
    num_examples: 5
  - name: test
    num_bytes: 24708
    num_examples: 100
  - name: validation
    num_bytes: 2328
    num_examples: 8
  download_size: 166184960
  dataset_size: 160629744
- config_name: college_computer_science
  features:
  - name: question
    dtype: string
  - name: choices
    sequence: string
  - name: answer
    dtype:
      class_label:
        names:
          0: A
          1: B
          2: C
          3: D
  splits:
  - name: auxiliary_train
    num_bytes: 160601377
    num_examples: 99842
  - name: dev
    num_bytes: 2765
    num_examples: 5
  - name: test
    num_bytes: 42641
    num_examples: 100
  - name: validation
    num_bytes: 4663
    num_examples: 11
  download_size: 166184960
  dataset_size: 160651446
- config_name: college_mathematics
  features:
  - name: question
    dtype: string
  - name: choices
    sequence: string
  - name: answer
    dtype:
      class_label:
        names:
          0: A
          1: B
          2: C
          3: D
  splits:
  - name: auxiliary_train
    num_bytes: 160601377
    num_examples: 99842
  - name: dev
    num_bytes: 1493
    num_examples: 5
  - name: test
    num_bytes: 24711
    num_examples: 100
  - name: validation
    num_bytes: 2668
    num_examples: 11
  download_size: 166184960
  dataset_size: 160630249
- config_name: college_medicine
  features:
  - name: question
    dtype: string
  - name: choices
    sequence: string
  - name: answer
    dtype:
      class_label:
        names:
          0: A
          1: B
          2: C
          3: D
  splits:
  - name: auxiliary_train
    num_bytes: 160601377
    num_examples: 99842
  - name: dev
    num_bytes: 1670
    num_examples: 5
  - name: test
    num_bytes: 82397
    num_examples: 173
  - name: validation
    num_bytes: 7909
    num_examples: 22
  download_size: 166184960
  dataset_size: 160693353
- config_name: college_physics
  features:
  - name: question
    dtype: string
  - name: choices
    sequence: string
  - name: answer
    dtype:
      class_label:
        names:
          0: A
          1: B
          2: C
          3: D
  splits:
  - name: auxiliary_train
    num_bytes: 160601377
    num_examples: 99842
  - name: dev
    num_bytes: 1412
    num_examples: 5
  - name: test
    num_bytes: 30181
    num_examples: 102
  - name: validation
    num_bytes: 3490
    num_examples: 11
  download_size: 166184960
  dataset_size: 160636460
- config_name: computer_security
  features:
  - name: question
    dtype: string
  - name: choices
    sequence: string
  - name: answer
    dtype:
      class_label:
        names:
          0: A
          1: B
          2: C
          3: D
  splits:
  - name: auxiliary_train
    num_bytes: 160601377
    num_examples: 99842
  - name: dev
    num_bytes: 1101
    num_examples: 5
  - name: test
    num_bytes: 27124
    num_examples: 100
  - name: validation
    num_bytes: 4549
    num_examples: 11
  download_size: 166184960
  dataset_size: 160634151
- config_name: conceptual_physics
  features:
  - name: question
    dtype: string
  - name: choices
    sequence: string
  - name: answer
    dtype:
      class_label:
        names:
          0: A
          1: B
          2: C
          3: D
  splits:
  - name: auxiliary_train
    num_bytes: 160601377
    num_examples: 99842
  - name: dev
    num_bytes: 934
    num_examples: 5
  - name: test
    num_bytes: 40709
    num_examples: 235
  - name: validation
    num_bytes: 4474
    num_examples: 26
  download_size: 166184960
  dataset_size: 160647494
- config_name: econometrics
  features:
  - name: question
    dtype: string
  - name: choices
    sequence: string
  - name: answer
    dtype:
      class_label:
        names:
          0: A
          1: B
          2: C
          3: D
  splits:
  - name: auxiliary_train
    num_bytes: 160601377
    num_examples: 99842
  - name: dev
    num_bytes: 1644
    num_examples: 5
  - name: test
    num_bytes: 46547
    num_examples: 114
  - name: validation
    num_bytes: 4967
    num_examples: 12
  download_size: 166184960
  dataset_size: 160654535
- config_name: electrical_engineering
  features:
  - name: question
    dtype: string
  - name: choices
    sequence: string
  - name: answer
    dtype:
      class_label:
        names:
          0: A
          1: B
          2: C
          3: D
  splits:
  - name: auxiliary_train
    num_bytes: 160601377
    num_examples: 99842
  - name: dev
    num_bytes: 972
    num_examples: 5
  - name: test
    num_bytes: 25142
    num_examples: 145
  - name: validation
    num_bytes: 2903
    num_examples: 16
  download_size: 166184960
  dataset_size: 160630394
- config_name: elementary_mathematics
  features:
  - name: question
    dtype: string
  - name: choices
    sequence: string
  - name: answer
    dtype:
      class_label:
        names:
          0: A
          1: B
          2: C
          3: D
  splits:
  - name: auxiliary_train
    num_bytes: 160601377
    num_examples: 99842
  - name: dev
    num_bytes: 1440
    num_examples: 5
  - name: test
    num_bytes: 70108
    num_examples: 378
  - name: validation
    num_bytes: 8988
    num_examples: 41
  download_size: 166184960
  dataset_size: 160681913
- config_name: formal_logic
  features:
  - name: question
    dtype: string
  - name: choices
    sequence: string
  - name: answer
    dtype:
      class_label:
        names:
          0: A
          1: B
          2: C
          3: D
  splits:
  - name: auxiliary_train
    num_bytes: 160601377
    num_examples: 99842
  - name: dev
    num_bytes: 1757
    num_examples: 5
  - name: test
    num_bytes: 49785
    num_examples: 126
  - name: validation
    num_bytes: 6252
    num_examples: 14
  download_size: 166184960
  dataset_size: 160659171
- config_name: global_facts
  features:
  - name: question
    dtype: string
  - name: choices
    sequence: string
  - name: answer
    dtype:
      class_label:
        names:
          0: A
          1: B
          2: C
          3: D
  splits:
  - name: auxiliary_train
    num_bytes: 160601377
    num_examples: 99842
  - name: dev
    num_bytes: 1229
    num_examples: 5
  - name: test
    num_bytes: 18403
    num_examples: 100
  - name: validation
    num_bytes: 1865
    num_examples: 10
  download_size: 166184960
  dataset_size: 160622874
- config_name: high_school_biology
  features:
  - name: question
    dtype: string
  - name: choices
    sequence: string
  - name: answer
    dtype:
      class_label:
        names:
          0: A
          1: B
          2: C
          3: D
  splits:
  - name: auxiliary_train
    num_bytes: 160601377
    num_examples: 99842
  - name: dev
    num_bytes: 1673
    num_examples: 5
  - name: test
    num_bytes: 109732
    num_examples: 310
  - name: validation
    num_bytes: 11022
    num_examples: 32
  download_size: 166184960
  dataset_size: 160723804
- config_name: high_school_chemistry
  features:
  - name: question
    dtype: string
  - name: choices
    sequence: string
  - name: answer
    dtype:
      class_label:
        names:
          0: A
          1: B
          2: C
          3: D
  splits:
  - name: auxiliary_train
    num_bytes: 160601377
    num_examples: 99842
  - name: dev
    num_bytes: 1220
    num_examples: 5
  - name: test
    num_bytes: 58464
    num_examples: 203
  - name: validation
    num_bytes: 7092
    num_examples: 22
  download_size: 166184960
  dataset_size: 160668153
- config_name: high_school_computer_science
  features:
  - name: question
    dtype: string
  - name: choices
    sequence: string
  - name: answer
    dtype:
      class_label:
        names:
          0: A
          1: B
          2: C
          3: D
  splits:
  - name: auxiliary_train
    num_bytes: 160601377
    num_examples: 99842
  - name: dev
    num_bytes: 2918
    num_examples: 5
  - name: test
    num_bytes: 44476
    num_examples: 100
  - name: validation
    num_bytes: 3343
    num_examples: 9
  download_size: 166184960
  dataset_size: 160652114
- config_name: high_school_european_history
  features:
  - name: question
    dtype: string
  - name: choices
    sequence: string
  - name: answer
    dtype:
      class_label:
        names:
          0: A
          1: B
          2: C
          3: D
  splits:
  - name: auxiliary_train
    num_bytes: 160601377
    num_examples: 99842
  - name: dev
    num_bytes: 11564
    num_examples: 5
  - name: test
    num_bytes: 270300
    num_examples: 165
  - name: validation
    num_bytes: 29632
    num_examples: 18
  download_size: 166184960
  dataset_size: 160912873
- config_name: high_school_geography
  features:
  - name: question
    dtype: string
  - name: choices
    sequence: string
  - name: answer
    dtype:
      class_label:
        names:
          0: A
          1: B
          2: C
          3: D
  splits:
  - name: auxiliary_train
    num_bytes: 160601377
    num_examples: 99842
  - name: dev
    num_bytes: 1403
    num_examples: 5
  - name: test
    num_bytes: 42034
    num_examples: 198
  - name: validation
    num_bytes: 4332
    num_examples: 22
  download_size: 166184960
  dataset_size: 160649146
- config_name: high_school_government_and_politics
  features:
  - name: question
    dtype: string
  - name: choices
    sequence: string
  - name: answer
    dtype:
      class_label:
        names:
          0: A
          1: B
          2: C
          3: D
  splits:
  - name: auxiliary_train
    num_bytes: 160601377
    num_examples: 99842
  - name: dev
    num_bytes: 1779
    num_examples: 5
  - name: test
    num_bytes: 66074
    num_examples: 193
  - name: validation
    num_bytes: 7063
    num_examples: 21
  download_size: 166184960
  dataset_size: 160676293
- config_name: high_school_macroeconomics
  features:
  - name: question
    dtype: string
  - name: choices
    sequence: string
  - name: answer
    dtype:
      class_label:
        names:
          0: A
          1: B
          2: C
          3: D
  splits:
  - name: auxiliary_train
    num_bytes: 160601377
    num_examples: 99842
  - name: dev
    num_bytes: 1328
    num_examples: 5
  - name: test
    num_bytes: 117687
    num_examples: 390
  - name: validation
    num_bytes: 13020
    num_examples: 43
  download_size: 166184960
  dataset_size: 160733412
- config_name: high_school_mathematics
  features:
  - name: question
    dtype: string
  - name: choices
    sequence: string
  - name: answer
    dtype:
      class_label:
        names:
          0: A
          1: B
          2: C
          3: D
  splits:
  - name: auxiliary_train
    num_bytes: 160601377
    num_examples: 99842
  - name: dev
    num_bytes: 1297
    num_examples: 5
  - name: test
    num_bytes: 54854
    num_examples: 270
  - name: validation
    num_bytes: 5765
    num_examples: 29
  download_size: 166184960
  dataset_size: 160663293
- config_name: high_school_microeconomics
  features:
  - name: question
    dtype: string
  - name: choices
    sequence: string
  - name: answer
    dtype:
      class_label:
        names:
          0: A
          1: B
          2: C
          3: D
  splits:
  - name: auxiliary_train
    num_bytes: 160601377
    num_examples: 99842
  - name: dev
    num_bytes: 1298
    num_examples: 5
  - name: test
    num_bytes: 75703
    num_examples: 238
  - name: validation
    num_bytes: 7553
    num_examples: 26
  download_size: 166184960
  dataset_size: 160685931
- config_name: high_school_physics
  features:
  - name: question
    dtype: string
  - name: choices
    sequence: string
  - name: answer
    dtype:
      class_label:
        names:
          0: A
          1: B
          2: C
          3: D
  splits:
  - name: auxiliary_train
    num_bytes: 160601377
    num_examples: 99842
  - name: dev
    num_bytes: 1489
    num_examples: 5
  - name: test
    num_bytes: 59538
    num_examples: 151
  - name: validation
    num_bytes: 6771
    num_examples: 17
  download_size: 166184960
  dataset_size: 160669175
- config_name: high_school_psychology
  features:
  - name: question
    dtype: string
  - name: choices
    sequence: string
  - name: answer
    dtype:
      class_label:
        names:
          0: A
          1: B
          2: C
          3: D
  splits:
  - name: auxiliary_train
    num_bytes: 160601377
    num_examples: 99842
  - name: dev
    num_bytes: 1905
    num_examples: 5
  - name: test
    num_bytes: 159407
    num_examples: 545
  - name: validation
    num_bytes: 17269
    num_examples: 60
  download_size: 166184960
  dataset_size: 160779958
- config_name: high_school_statistics
  features:
  - name: question
    dtype: string
  - name: choices
    sequence: string
  - name: answer
    dtype:
      class_label:
        names:
          0: A
          1: B
          2: C
          3: D
  splits:
  - name: auxiliary_train
    num_bytes: 160601377
    num_examples: 99842
  - name: dev
    num_bytes: 2528
    num_examples: 5
  - name: test
    num_bytes: 110702
    num_examples: 216
  - name: validation
    num_bytes: 9997
    num_examples: 23
  download_size: 166184960
  dataset_size: 160724604
- config_name: high_school_us_history
  features:
  - name: question
    dtype: string
  - name: choices
    sequence: string
  - name: answer
    dtype:
      class_label:
        names:
          0: A
          1: B
          2: C
          3: D
  splits:
  - name: auxiliary_train
    num_bytes: 160601377
    num_examples: 99842
  - name: dev
    num_bytes: 8864
    num_examples: 5
  - name: test
    num_bytes: 296734
    num_examples: 204
  - name: validation
    num_bytes: 31706
    num_examples: 22
  download_size: 166184960
  dataset_size: 160938681
- config_name: high_school_world_history
  features:
  - name: question
    dtype: string
  - name: choices
    sequence: string
  - name: answer
    dtype:
      class_label:
        names:
          0: A
          1: B
          2: C
          3: D
  splits:
  - name: auxiliary_train
    num_bytes: 160601377
    num_examples: 99842
  - name: dev
    num_bytes: 4882
    num_examples: 5
  - name: test
    num_bytes: 378617
    num_examples: 237
  - name: validation
    num_bytes: 45501
    num_examples: 26
  download_size: 166184960
  dataset_size: 161030377
- config_name: human_aging
  features:
  - name: question
    dtype: string
  - name: choices
    sequence: string
  - name: answer
    dtype:
      class_label:
        names:
          0: A
          1: B
          2: C
          3: D
  splits:
  - name: auxiliary_train
    num_bytes: 160601377
    num_examples: 99842
  - name: dev
    num_bytes: 1008
    num_examples: 5
  - name: test
    num_bytes: 46098
    num_examples: 223
  - name: validation
    num_bytes: 4707
    num_examples: 23
  download_size: 166184960
  dataset_size: 160653190
- config_name: human_sexuality
  features:
  - name: question
    dtype: string
  - name: choices
    sequence: string
  - name: answer
    dtype:
      class_label:
        names:
          0: A
          1: B
          2: C
          3: D
  splits:
  - name: auxiliary_train
    num_bytes: 160601377
    num_examples: 99842
  - name: dev
    num_bytes: 1077
    num_examples: 5
  - name: test
    num_bytes: 32110
    num_examples: 131
  - name: validation
    num_bytes: 2421
    num_examples: 12
  download_size: 166184960
  dataset_size: 160636985
- config_name: international_law
  features:
  - name: question
    dtype: string
  - name: choices
    sequence: string
  - name: answer
    dtype:
      class_label:
        names:
          0: A
          1: B
          2: C
          3: D
  splits:
  - name: auxiliary_train
    num_bytes: 160601377
    num_examples: 99842
  - name: dev
    num_bytes: 2418
    num_examples: 5
  - name: test
    num_bytes: 53531
    num_examples: 121
  - name: validation
    num_bytes: 6473
    num_examples: 13
  download_size: 166184960
  dataset_size: 160663799
- config_name: jurisprudence
  features:
  - name: question
    dtype: string
  - name: choices
    sequence: string
  - name: answer
    dtype:
      class_label:
        names:
          0: A
          1: B
          2: C
          3: D
  splits:
  - name: auxiliary_train
    num_bytes: 160601377
    num_examples: 99842
  - name: dev
    num_bytes: 1303
    num_examples: 5
  - name: test
    num_bytes: 33986
    num_examples: 108
  - name: validation
    num_bytes: 3729
    num_examples: 11
  download_size: 166184960
  dataset_size: 160640395
- config_name: logical_fallacies
  features:
  - name: question
    dtype: string
  - name: choices
    sequence: string
  - name: answer
    dtype:
      class_label:
        names:
          0: A
          1: B
          2: C
          3: D
  splits:
  - name: auxiliary_train
    num_bytes: 160601377
    num_examples: 99842
  - name: dev
    num_bytes: 1573
    num_examples: 5
  - name: test
    num_bytes: 50117
    num_examples: 163
  - name: validation
    num_bytes: 5103
    num_examples: 18
  download_size: 166184960
  dataset_size: 160658170
- config_name: machine_learning
  features:
  - name: question
    dtype: string
  - name: choices
    sequence: string
  - name: answer
    dtype:
      class_label:
        names:
          0: A
          1: B
          2: C
          3: D
  splits:
  - name: auxiliary_train
    num_bytes: 160601377
    num_examples: 99842
  - name: dev
    num_bytes: 2323
    num_examples: 5
  - name: test
    num_bytes: 33880
    num_examples: 112
  - name: validation
    num_bytes: 3232
    num_examples: 11
  download_size: 166184960
  dataset_size: 160640812
- config_name: management
  features:
  - name: question
    dtype: string
  - name: choices
    sequence: string
  - name: answer
    dtype:
      class_label:
        names:
          0: A
          1: B
          2: C
          3: D
  splits:
  - name: auxiliary_train
    num_bytes: 160601377
    num_examples: 99842
  - name: dev
    num_bytes: 898
    num_examples: 5
  - name: test
    num_bytes: 20002
    num_examples: 103
  - name: validation
    num_bytes: 1820
    num_examples: 11
  download_size: 166184960
  dataset_size: 160624097
- config_name: marketing
  features:
  - name: question
    dtype: string
  - name: choices
    sequence: string
  - name: answer
    dtype:
      class_label:
        names:
          0: A
          1: B
          2: C
          3: D
  splits:
  - name: auxiliary_train
    num_bytes: 160601377
    num_examples: 99842
  - name: dev
    num_bytes: 1481
    num_examples: 5
  - name: test
    num_bytes: 63025
    num_examples: 234
  - name: validation
    num_bytes: 7394
    num_examples: 25
  download_size: 166184960
  dataset_size: 160673277
- config_name: medical_genetics
  features:
  - name: question
    dtype: string
  - name: choices
    sequence: string
  - name: answer
    dtype:
      class_label:
        names:
          0: A
          1: B
          2: C
          3: D
  splits:
  - name: auxiliary_train
    num_bytes: 160601377
    num_examples: 99842
  - name: dev
    num_bytes: 1089
    num_examples: 5
  - name: test
    num_bytes: 20864
    num_examples: 100
  - name: validation
    num_bytes: 3005
    num_examples: 11
  download_size: 166184960
  dataset_size: 160626335
- config_name: miscellaneous
  features:
  - name: question
    dtype: string
  - name: choices
    sequence: string
  - name: answer
    dtype:
      class_label:
        names:
          0: A
          1: B
          2: C
          3: D
  splits:
  - name: auxiliary_train
    num_bytes: 160601377
    num_examples: 99842
  - name: dev
    num_bytes: 699
    num_examples: 5
  - name: test
    num_bytes: 147704
    num_examples: 783
  - name: validation
    num_bytes: 14330
    num_examples: 86
  download_size: 166184960
  dataset_size: 160764110
- config_name: moral_disputes
  features:
  - name: question
    dtype: string
  - name: choices
    sequence: string
  - name: answer
    dtype:
      class_label:
        names:
          0: A
          1: B
          2: C
          3: D
  splits:
  - name: auxiliary_train
    num_bytes: 160601377
    num_examples: 99842
  - name: dev
    num_bytes: 1755
    num_examples: 5
  - name: test
    num_bytes: 107818
    num_examples: 346
  - name: validation
    num_bytes: 12420
    num_examples: 38
  download_size: 166184960
  dataset_size: 160723370
- config_name: moral_scenarios
  features:
  - name: question
    dtype: string
  - name: choices
    sequence: string
  - name: answer
    dtype:
      class_label:
        names:
          0: A
          1: B
          2: C
          3: D
  splits:
  - name: auxiliary_train
    num_bytes: 160601377
    num_examples: 99842
  - name: dev
    num_bytes: 2058
    num_examples: 5
  - name: test
    num_bytes: 374026
    num_examples: 895
  - name: validation
    num_bytes: 42338
    num_examples: 100
  download_size: 166184960
  dataset_size: 161019799
- config_name: nutrition
  features:
  - name: question
    dtype: string
  - name: choices
    sequence: string
  - name: answer
    dtype:
      class_label:
        names:
          0: A
          1: B
          2: C
          3: D
  splits:
  - name: auxiliary_train
    num_bytes: 160601377
    num_examples: 99842
  - name: dev
    num_bytes: 2085
    num_examples: 5
  - name: test
    num_bytes: 92410
    num_examples: 306
  - name: validation
    num_bytes: 8436
    num_examples: 33
  download_size: 166184960
  dataset_size: 160704308
- config_name: philosophy
  features:
  - name: question
    dtype: string
  - name: choices
    sequence: string
  - name: answer
    dtype:
      class_label:
        names:
          0: A
          1: B
          2: C
          3: D
  splits:
  - name: auxiliary_train
    num_bytes: 160601377
    num_examples: 99842
  - name: dev
    num_bytes: 988
    num_examples: 5
  - name: test
    num_bytes: 80073
    num_examples: 311
  - name: validation
    num_bytes: 9184
    num_examples: 34
  download_size: 166184960
  dataset_size: 160691622
- config_name: prehistory
  features:
  - name: question
    dtype: string
  - name: choices
    sequence: string
  - name: answer
    dtype:
      class_label:
        names:
          0: A
          1: B
          2: C
          3: D
  splits:
  - name: auxiliary_train
    num_bytes: 160601377
    num_examples: 99842
  - name: dev
    num_bytes: 1878
    num_examples: 5
  - name: test
    num_bytes: 89594
    num_examples: 324
  - name: validation
    num_bytes: 10285
    num_examples: 35
  download_size: 166184960
  dataset_size: 160703134
- config_name: professional_accounting
  features:
  - name: question
    dtype: string
  - name: choices
    sequence: string
  - name: answer
    dtype:
      class_label:
        names:
          0: A
          1: B
          2: C
          3: D
  splits:
  - name: auxiliary_train
    num_bytes: 160601377
    num_examples: 99842
  - name: dev
    num_bytes: 2148
    num_examples: 5
  - name: test
    num_bytes: 124550
    num_examples: 282
  - name: validation
    num_bytes: 14372
    num_examples: 31
  download_size: 166184960
  dataset_size: 160742447
- config_name: professional_law
  features:
  - name: question
    dtype: string
  - name: choices
    sequence: string
  - name: answer
    dtype:
      class_label:
        names:
          0: A
          1: B
          2: C
          3: D
  splits:
  - name: auxiliary_train
    num_bytes: 160601377
    num_examples: 99842
  - name: dev
    num_bytes: 6610
    num_examples: 5
  - name: test
    num_bytes: 1891762
    num_examples: 1534
  - name: validation
    num_bytes: 203519
    num_examples: 170
  download_size: 166184960
  dataset_size: 162703268
- config_name: professional_medicine
  features:
  - name: question
    dtype: string
  - name: choices
    sequence: string
  - name: answer
    dtype:
      class_label:
        names:
          0: A
          1: B
          2: C
          3: D
  splits:
  - name: auxiliary_train
    num_bytes: 160601377
    num_examples: 99842
  - name: dev
    num_bytes: 3807
    num_examples: 5
  - name: test
    num_bytes: 217561
    num_examples: 272
  - name: validation
    num_bytes: 23847
    num_examples: 31
  download_size: 166184960
  dataset_size: 160846592
- config_name: professional_psychology
  features:
  - name: question
    dtype: string
  - name: choices
    sequence: string
  - name: answer
    dtype:
      class_label:
        names:
          0: A
          1: B
          2: C
          3: D
  splits:
  - name: auxiliary_train
    num_bytes: 160601377
    num_examples: 99842
  - name: dev
    num_bytes: 2267
    num_examples: 5
  - name: test
    num_bytes: 225899
    num_examples: 612
  - name: validation
    num_bytes: 29101
    num_examples: 69
  download_size: 166184960
  dataset_size: 160858644
- config_name: public_relations
  features:
  - name: question
    dtype: string
  - name: choices
    sequence: string
  - name: answer
    dtype:
      class_label:
        names:
          0: A
          1: B
          2: C
          3: D
  splits:
  - name: auxiliary_train
    num_bytes: 160601377
    num_examples: 99842
  - name: dev
    num_bytes: 1496
    num_examples: 5
  - name: test
    num_bytes: 28760
    num_examples: 110
  - name: validation
    num_bytes: 4566
    num_examples: 12
  download_size: 166184960
  dataset_size: 160636199
- config_name: security_studies
  features:
  - name: question
    dtype: string
  - name: choices
    sequence: string
  - name: answer
    dtype:
      class_label:
        names:
          0: A
          1: B
          2: C
          3: D
  splits:
  - name: auxiliary_train
    num_bytes: 160601377
    num_examples: 99842
  - name: dev
    num_bytes: 5335
    num_examples: 5
  - name: test
    num_bytes: 204844
    num_examples: 245
  - name: validation
    num_bytes: 22637
    num_examples: 27
  download_size: 166184960
  dataset_size: 160834193
- config_name: sociology
  features:
  - name: question
    dtype: string
  - name: choices
    sequence: string
  - name: answer
    dtype:
      class_label:
        names:
          0: A
          1: B
          2: C
          3: D
  splits:
  - name: auxiliary_train
    num_bytes: 160601377
    num_examples: 99842
  - name: dev
    num_bytes: 1613
    num_examples: 5
  - name: test
    num_bytes: 66243
    num_examples: 201
  - name: validation
    num_bytes: 7184
    num_examples: 22
  download_size: 166184960
  dataset_size: 160676417
- config_name: us_foreign_policy
  features:
  - name: question
    dtype: string
  - name: choices
    sequence: string
  - name: answer
    dtype:
      class_label:
        names:
          0: A
          1: B
          2: C
          3: D
  splits:
  - name: auxiliary_train
    num_bytes: 160601377
    num_examples: 99842
  - name: dev
    num_bytes: 1611
    num_examples: 5
  - name: test
    num_bytes: 28443
    num_examples: 100
  - name: validation
    num_bytes: 3264
    num_examples: 11
  download_size: 166184960
  dataset_size: 160634695
- config_name: virology
  features:
  - name: question
    dtype: string
  - name: choices
    sequence: string
  - name: answer
    dtype:
      class_label:
        names:
          0: A
          1: B
          2: C
          3: D
  splits:
  - name: auxiliary_train
    num_bytes: 160601377
    num_examples: 99842
  - name: dev
    num_bytes: 1096
    num_examples: 5
  - name: test
    num_bytes: 38759
    num_examples: 166
  - name: validation
    num_bytes: 5463
    num_examples: 18
  download_size: 166184960
  dataset_size: 160646695
- config_name: world_religions
  features:
  - name: question
    dtype: string
  - name: choices
    sequence: string
  - name: answer
    dtype:
      class_label:
        names:
          0: A
          1: B
          2: C
          3: D
  splits:
  - name: auxiliary_train
    num_bytes: 160601377
    num_examples: 99842
  - name: dev
    num_bytes: 670
    num_examples: 5
  - name: test
    num_bytes: 25274
    num_examples: 171
  - name: validation
    num_bytes: 2765
    num_examples: 19
  download_size: 166184960
  dataset_size: 160630086
---

# Dataset Card for HendrycksTest

## Table of Contents
- [Table of Contents](#table-of-contents)
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

- **Repository**: https://github.com/hendrycks/test
- **Paper**: https://arxiv.org/abs/2009.03300

### Dataset Summary

[Measuring Massive Multitask Language Understanding](https://arxiv.org/pdf/2009.03300) by [Dan Hendrycks](https://people.eecs.berkeley.edu/~hendrycks/), [Collin Burns](http://collinpburns.com), [Steven Basart](https://stevenbas.art), Andy Zou, Mantas Mazeika, [Dawn Song](https://people.eecs.berkeley.edu/~dawnsong/), and [Jacob Steinhardt](https://www.stat.berkeley.edu/~jsteinhardt/) (ICLR 2021).

This is a massive multitask test consisting of multiple-choice questions from various branches of knowledge. The test spans subjects in the humanities, social sciences, hard sciences, and other areas that are important for some people to learn. This covers 57 tasks including elementary mathematics, US history, computer science, law, and more. To attain high accuracy on this test, models must possess extensive world knowledge and problem solving ability.

A complete list of tasks: ['abstract_algebra', 'anatomy', 'astronomy', 'business_ethics', 'clinical_knowledge', 'college_biology', 'college_chemistry', 'college_computer_science', 'college_mathematics', 'college_medicine', 'college_physics', 'computer_security', 'conceptual_physics', 'econometrics', 'electrical_engineering', 'elementary_mathematics', 'formal_logic', 'global_facts', 'high_school_biology', 'high_school_chemistry', 'high_school_computer_science', 'high_school_european_history', 'high_school_geography', 'high_school_government_and_politics', 'high_school_macroeconomics', 'high_school_mathematics', 'high_school_microeconomics', 'high_school_physics', 'high_school_psychology', 'high_school_statistics', 'high_school_us_history', 'high_school_world_history', 'human_aging', 'human_sexuality', 'international_law', 'jurisprudence', 'logical_fallacies', 'machine_learning', 'management', 'marketing', 'medical_genetics', 'miscellaneous', 'moral_disputes', 'moral_scenarios', 'nutrition', 'philosophy', 'prehistory', 'professional_accounting', 'professional_law', 'professional_medicine', 'professional_psychology', 'public_relations', 'security_studies', 'sociology', 'us_foreign_policy', 'virology', 'world_religions']

### Supported Tasks and Leaderboards

|                Model               | Authors |  Humanities |  Social Science  | STEM | Other | Average |
|------------------------------------|----------|:-------:|:-------:|:-------:|:-------:|:-------:|
| [UnifiedQA](https://arxiv.org/abs/2005.00700) | Khashabi et al., 2020 | 45.6 | 56.6 | 40.2 | 54.6 | 48.9
| [GPT-3](https://arxiv.org/abs/2005.14165) (few-shot) | Brown et al., 2020 | 40.8 | 50.4 | 36.7 | 48.8 | 43.9
| [GPT-2](https://arxiv.org/abs/2005.14165) | Radford et al., 2019 | 32.8 | 33.3 | 30.2 | 33.1 | 32.4
| Random Baseline           | N/A | 25.0 | 25.0 | 25.0 | 25.0 | 25.0 | 25.0

### Languages

English

## Dataset Structure

### Data Instances

An example from anatomy subtask looks as follows:
```
{
  "question": "What is the embryological origin of the hyoid bone?",
  "choices": ["The first pharyngeal arch", "The first and second pharyngeal arches", "The second pharyngeal arch", "The second and third pharyngeal arches"],
  "answer": "D"
}
```

### Data Fields

- `question`: a string feature
- `choices`: a list of 4 string features
- `answer`: a ClassLabel feature

### Data Splits

- `auxiliary_train`: auxiliary multiple-choice training questions from ARC, MC_TEST, OBQA, RACE, etc.
- `dev`: 5 examples per subtask, meant for few-shot setting
- `test`: there are at least 100 examples per subtask

|       | auxiliary_train   | dev | val | test |
| ----- | :------: | :-----: | :-----: | :-----: |
| TOTAL | 99842 | 285 | 1531 | 14042

## Dataset Creation

### Curation Rationale

Transformer models have driven this recent progress by pretraining on massive text corpora, including all of Wikipedia, thousands of books, and numerous websites. These models consequently see extensive information about specialized topics, most of which is not assessed by existing NLP benchmarks. To bridge the gap between the wide-ranging knowledge that models see during pretraining and the existing measures of success, we introduce a new benchmark for assessing models across a diverse set of subjects that humans learn.

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

[MIT License](https://github.com/hendrycks/test/blob/master/LICENSE)

### Citation Information

If you find this useful in your research, please consider citing the test and also the [ETHICS](https://arxiv.org/abs/2008.02275) dataset it draws from:
```
    @article{hendryckstest2021,
      title={Measuring Massive Multitask Language Understanding},
      author={Dan Hendrycks and Collin Burns and Steven Basart and Andy Zou and Mantas Mazeika and Dawn Song and Jacob Steinhardt},
      journal={Proceedings of the International Conference on Learning Representations (ICLR)},
      year={2021}
    }

    @article{hendrycks2021ethics,
      title={Aligning AI With Shared Human Values},
      author={Dan Hendrycks and Collin Burns and Steven Basart and Andrew Critch and Jerry Li and Dawn Song and Jacob Steinhardt},
      journal={Proceedings of the International Conference on Learning Representations (ICLR)},
      year={2021}
    }
```
### Contributions

Thanks to [@andyzoujm](https://github.com/andyzoujm) for adding this dataset.