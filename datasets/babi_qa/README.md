---
pretty_name: BabiQa
annotations_creators:
- machine-generated
language_creators:
- machine-generated
language:
- en
license:
- cc-by-3.0
multilinguality:
- monolingual
size_categories:
- 10K<n<100K
- 1K<n<10K
- n<1K
source_datasets:
- original
task_categories:
- question-answering
task_ids:
- question-answering-other-chained-qa
paperswithcode_id: babi-1
configs:
- en-10k-qa1
- en-10k-qa10
- en-10k-qa11
- en-10k-qa12
- en-10k-qa13
- en-10k-qa14
- en-10k-qa15
- en-10k-qa16
- en-10k-qa17
- en-10k-qa18
- en-10k-qa19
- en-10k-qa2
- en-10k-qa20
- en-10k-qa3
- en-10k-qa4
- en-10k-qa5
- en-10k-qa6
- en-10k-qa7
- en-10k-qa8
- en-10k-qa9
- en-qa1
- en-qa10
- en-qa11
- en-qa12
- en-qa13
- en-qa14
- en-qa15
- en-qa16
- en-qa17
- en-qa18
- en-qa19
- en-qa2
- en-qa20
- en-qa3
- en-qa4
- en-qa5
- en-qa6
- en-qa7
- en-qa8
- en-qa9
- en-valid-10k-qa1
- en-valid-10k-qa10
- en-valid-10k-qa11
- en-valid-10k-qa12
- en-valid-10k-qa13
- en-valid-10k-qa14
- en-valid-10k-qa15
- en-valid-10k-qa16
- en-valid-10k-qa17
- en-valid-10k-qa18
- en-valid-10k-qa19
- en-valid-10k-qa2
- en-valid-10k-qa20
- en-valid-10k-qa3
- en-valid-10k-qa4
- en-valid-10k-qa5
- en-valid-10k-qa6
- en-valid-10k-qa7
- en-valid-10k-qa8
- en-valid-10k-qa9
- en-valid-qa1
- en-valid-qa10
- en-valid-qa11
- en-valid-qa12
- en-valid-qa13
- en-valid-qa14
- en-valid-qa15
- en-valid-qa16
- en-valid-qa17
- en-valid-qa18
- en-valid-qa19
- en-valid-qa2
- en-valid-qa20
- en-valid-qa3
- en-valid-qa4
- en-valid-qa5
- en-valid-qa6
- en-valid-qa7
- en-valid-qa8
- en-valid-qa9
- hn-10k-qa1
- hn-10k-qa10
- hn-10k-qa11
- hn-10k-qa12
- hn-10k-qa13
- hn-10k-qa14
- hn-10k-qa15
- hn-10k-qa16
- hn-10k-qa17
- hn-10k-qa18
- hn-10k-qa19
- hn-10k-qa2
- hn-10k-qa20
- hn-10k-qa3
- hn-10k-qa4
- hn-10k-qa5
- hn-10k-qa6
- hn-10k-qa7
- hn-10k-qa8
- hn-10k-qa9
- hn-qa1
- hn-qa10
- hn-qa11
- hn-qa12
- hn-qa13
- hn-qa14
- hn-qa15
- hn-qa16
- hn-qa17
- hn-qa18
- hn-qa19
- hn-qa2
- hn-qa20
- hn-qa3
- hn-qa4
- hn-qa5
- hn-qa6
- hn-qa7
- hn-qa8
- hn-qa9
- shuffled-10k-qa1
- shuffled-10k-qa10
- shuffled-10k-qa11
- shuffled-10k-qa12
- shuffled-10k-qa13
- shuffled-10k-qa14
- shuffled-10k-qa15
- shuffled-10k-qa16
- shuffled-10k-qa17
- shuffled-10k-qa18
- shuffled-10k-qa19
- shuffled-10k-qa2
- shuffled-10k-qa20
- shuffled-10k-qa3
- shuffled-10k-qa4
- shuffled-10k-qa5
- shuffled-10k-qa6
- shuffled-10k-qa7
- shuffled-10k-qa8
- shuffled-10k-qa9
- shuffled-qa1
- shuffled-qa10
- shuffled-qa11
- shuffled-qa12
- shuffled-qa13
- shuffled-qa14
- shuffled-qa15
- shuffled-qa16
- shuffled-qa17
- shuffled-qa18
- shuffled-qa19
- shuffled-qa2
- shuffled-qa20
- shuffled-qa3
- shuffled-qa4
- shuffled-qa5
- shuffled-qa6
- shuffled-qa7
- shuffled-qa8
- shuffled-qa9
dataset_info:
- config_name: en-qa1
  features:
  - name: story
    sequence:
    - name: id
      dtype: string
    - name: type
      dtype:
        class_label:
          names:
            0: context
            1: question
    - name: text
      dtype: string
    - name: supporting_ids
      sequence: string
    - name: answer
      dtype: string
  splits:
  - name: test
    num_bytes: 165517
    num_examples: 200
  - name: train
    num_bytes: 165386
    num_examples: 200
  download_size: 15719851
  dataset_size: 330903
- config_name: en-qa2
  features:
  - name: story
    sequence:
    - name: id
      dtype: string
    - name: type
      dtype:
        class_label:
          names:
            0: context
            1: question
    - name: text
      dtype: string
    - name: supporting_ids
      sequence: string
    - name: answer
      dtype: string
  splits:
  - name: test
    num_bytes: 306631
    num_examples: 200
  - name: train
    num_bytes: 302888
    num_examples: 200
  download_size: 15719851
  dataset_size: 609519
- config_name: en-qa3
  features:
  - name: story
    sequence:
    - name: id
      dtype: string
    - name: type
      dtype:
        class_label:
          names:
            0: context
            1: question
    - name: text
      dtype: string
    - name: supporting_ids
      sequence: string
    - name: answer
      dtype: string
  splits:
  - name: test
    num_bytes: 883187
    num_examples: 200
  - name: train
    num_bytes: 887756
    num_examples: 200
  download_size: 15719851
  dataset_size: 1770943
- config_name: en-qa4
  features:
  - name: story
    sequence:
    - name: id
      dtype: string
    - name: type
      dtype:
        class_label:
          names:
            0: context
            1: question
    - name: text
      dtype: string
    - name: supporting_ids
      sequence: string
    - name: answer
      dtype: string
  splits:
  - name: test
    num_bytes: 205434
    num_examples: 1000
  - name: train
    num_bytes: 205510
    num_examples: 1000
  download_size: 15719851
  dataset_size: 410944
- config_name: en-qa5
  features:
  - name: story
    sequence:
    - name: id
      dtype: string
    - name: type
      dtype:
        class_label:
          names:
            0: context
            1: question
    - name: text
      dtype: string
    - name: supporting_ids
      sequence: string
    - name: answer
      dtype: string
  splits:
  - name: test
    num_bytes: 350457
    num_examples: 200
  - name: train
    num_bytes: 337349
    num_examples: 200
  download_size: 15719851
  dataset_size: 687806
- config_name: en-qa6
  features:
  - name: story
    sequence:
    - name: id
      dtype: string
    - name: type
      dtype:
        class_label:
          names:
            0: context
            1: question
    - name: text
      dtype: string
    - name: supporting_ids
      sequence: string
    - name: answer
      dtype: string
  splits:
  - name: test
    num_bytes: 172249
    num_examples: 200
  - name: train
    num_bytes: 173053
    num_examples: 200
  download_size: 15719851
  dataset_size: 345302
- config_name: en-qa7
  features:
  - name: story
    sequence:
    - name: id
      dtype: string
    - name: type
      dtype:
        class_label:
          names:
            0: context
            1: question
    - name: text
      dtype: string
    - name: supporting_ids
      sequence: string
    - name: answer
      dtype: string
  splits:
  - name: test
    num_bytes: 215512
    num_examples: 200
  - name: train
    num_bytes: 224778
    num_examples: 200
  download_size: 15719851
  dataset_size: 440290
- config_name: en-qa8
  features:
  - name: story
    sequence:
    - name: id
      dtype: string
    - name: type
      dtype:
        class_label:
          names:
            0: context
            1: question
    - name: text
      dtype: string
    - name: supporting_ids
      sequence: string
    - name: answer
      dtype: string
  splits:
  - name: test
    num_bytes: 216244
    num_examples: 200
  - name: train
    num_bytes: 212517
    num_examples: 200
  download_size: 15719851
  dataset_size: 428761
- config_name: en-qa9
  features:
  - name: story
    sequence:
    - name: id
      dtype: string
    - name: type
      dtype:
        class_label:
          names:
            0: context
            1: question
    - name: text
      dtype: string
    - name: supporting_ids
      sequence: string
    - name: answer
      dtype: string
  splits:
  - name: test
    num_bytes: 168248
    num_examples: 200
  - name: train
    num_bytes: 168350
    num_examples: 200
  download_size: 15719851
  dataset_size: 336598
- config_name: en-qa10
  features:
  - name: story
    sequence:
    - name: id
      dtype: string
    - name: type
      dtype:
        class_label:
          names:
            0: context
            1: question
    - name: text
      dtype: string
    - name: supporting_ids
      sequence: string
    - name: answer
      dtype: string
  splits:
  - name: test
    num_bytes: 170672
    num_examples: 200
  - name: train
    num_bytes: 170257
    num_examples: 200
  download_size: 15719851
  dataset_size: 340929
- config_name: en-qa11
  features:
  - name: story
    sequence:
    - name: id
      dtype: string
    - name: type
      dtype:
        class_label:
          names:
            0: context
            1: question
    - name: text
      dtype: string
    - name: supporting_ids
      sequence: string
    - name: answer
      dtype: string
  splits:
  - name: test
    num_bytes: 178840
    num_examples: 200
  - name: train
    num_bytes: 178560
    num_examples: 200
  download_size: 15719851
  dataset_size: 357400
- config_name: en-qa12
  features:
  - name: story
    sequence:
    - name: id
      dtype: string
    - name: type
      dtype:
        class_label:
          names:
            0: context
            1: question
    - name: text
      dtype: string
    - name: supporting_ids
      sequence: string
    - name: answer
      dtype: string
  splits:
  - name: test
    num_bytes: 185529
    num_examples: 200
  - name: train
    num_bytes: 185600
    num_examples: 200
  download_size: 15719851
  dataset_size: 371129
- config_name: en-qa13
  features:
  - name: story
    sequence:
    - name: id
      dtype: string
    - name: type
      dtype:
        class_label:
          names:
            0: context
            1: question
    - name: text
      dtype: string
    - name: supporting_ids
      sequence: string
    - name: answer
      dtype: string
  splits:
  - name: test
    num_bytes: 190484
    num_examples: 200
  - name: train
    num_bytes: 190556
    num_examples: 200
  download_size: 15719851
  dataset_size: 381040
- config_name: en-qa14
  features:
  - name: story
    sequence:
    - name: id
      dtype: string
    - name: type
      dtype:
        class_label:
          names:
            0: context
            1: question
    - name: text
      dtype: string
    - name: supporting_ids
      sequence: string
    - name: answer
      dtype: string
  splits:
  - name: test
    num_bytes: 233204
    num_examples: 200
  - name: train
    num_bytes: 234355
    num_examples: 200
  download_size: 15719851
  dataset_size: 467559
- config_name: en-qa15
  features:
  - name: story
    sequence:
    - name: id
      dtype: string
    - name: type
      dtype:
        class_label:
          names:
            0: context
            1: question
    - name: text
      dtype: string
    - name: supporting_ids
      sequence: string
    - name: answer
      dtype: string
  splits:
  - name: test
    num_bytes: 163809
    num_examples: 250
  - name: train
    num_bytes: 163728
    num_examples: 250
  download_size: 15719851
  dataset_size: 327537
- config_name: en-qa16
  features:
  - name: story
    sequence:
    - name: id
      dtype: string
    - name: type
      dtype:
        class_label:
          names:
            0: context
            1: question
    - name: text
      dtype: string
    - name: supporting_ids
      sequence: string
    - name: answer
      dtype: string
  splits:
  - name: test
    num_bytes: 456248
    num_examples: 1000
  - name: train
    num_bytes: 456374
    num_examples: 1000
  download_size: 15719851
  dataset_size: 912622
- config_name: en-qa17
  features:
  - name: story
    sequence:
    - name: id
      dtype: string
    - name: type
      dtype:
        class_label:
          names:
            0: context
            1: question
    - name: text
      dtype: string
    - name: supporting_ids
      sequence: string
    - name: answer
      dtype: string
  splits:
  - name: test
    num_bytes: 103618
    num_examples: 125
  - name: train
    num_bytes: 103636
    num_examples: 125
  download_size: 15719851
  dataset_size: 207254
- config_name: en-qa18
  features:
  - name: story
    sequence:
    - name: id
      dtype: string
    - name: type
      dtype:
        class_label:
          names:
            0: context
            1: question
    - name: text
      dtype: string
    - name: supporting_ids
      sequence: string
    - name: answer
      dtype: string
  splits:
  - name: test
    num_bytes: 161266
    num_examples: 199
  - name: train
    num_bytes: 162875
    num_examples: 198
  download_size: 15719851
  dataset_size: 324141
- config_name: en-qa19
  features:
  - name: story
    sequence:
    - name: id
      dtype: string
    - name: type
      dtype:
        class_label:
          names:
            0: context
            1: question
    - name: text
      dtype: string
    - name: supporting_ids
      sequence: string
    - name: answer
      dtype: string
  splits:
  - name: test
    num_bytes: 404489
    num_examples: 1000
  - name: train
    num_bytes: 404536
    num_examples: 1000
  download_size: 15719851
  dataset_size: 809025
- config_name: en-qa20
  features:
  - name: story
    sequence:
    - name: id
      dtype: string
    - name: type
      dtype:
        class_label:
          names:
            0: context
            1: question
    - name: text
      dtype: string
    - name: supporting_ids
      sequence: string
    - name: answer
      dtype: string
  splits:
  - name: test
    num_bytes: 115863
    num_examples: 93
  - name: train
    num_bytes: 115812
    num_examples: 94
  download_size: 15719851
  dataset_size: 231675
- config_name: hn-qa1
  features:
  - name: story
    sequence:
    - name: id
      dtype: string
    - name: type
      dtype:
        class_label:
          names:
            0: context
            1: question
    - name: text
      dtype: string
    - name: supporting_ids
      sequence: string
    - name: answer
      dtype: string
  splits:
  - name: test
    num_bytes: 168572
    num_examples: 200
  - name: train
    num_bytes: 168605
    num_examples: 200
  download_size: 15719851
  dataset_size: 337177
- config_name: hn-qa2
  features:
  - name: story
    sequence:
    - name: id
      dtype: string
    - name: type
      dtype:
        class_label:
          names:
            0: context
            1: question
    - name: text
      dtype: string
    - name: supporting_ids
      sequence: string
    - name: answer
      dtype: string
  splits:
  - name: test
    num_bytes: 288429
    num_examples: 200
  - name: train
    num_bytes: 296391
    num_examples: 200
  download_size: 15719851
  dataset_size: 584820
- config_name: hn-qa3
  features:
  - name: story
    sequence:
    - name: id
      dtype: string
    - name: type
      dtype:
        class_label:
          names:
            0: context
            1: question
    - name: text
      dtype: string
    - name: supporting_ids
      sequence: string
    - name: answer
      dtype: string
  splits:
  - name: test
    num_bytes: 808460
    num_examples: 167
  - name: train
    num_bytes: 842184
    num_examples: 167
  download_size: 15719851
  dataset_size: 1650644
- config_name: hn-qa4
  features:
  - name: story
    sequence:
    - name: id
      dtype: string
    - name: type
      dtype:
        class_label:
          names:
            0: context
            1: question
    - name: text
      dtype: string
    - name: supporting_ids
      sequence: string
    - name: answer
      dtype: string
  splits:
  - name: test
    num_bytes: 231230
    num_examples: 1000
  - name: train
    num_bytes: 231303
    num_examples: 1000
  download_size: 15719851
  dataset_size: 462533
- config_name: hn-qa5
  features:
  - name: story
    sequence:
    - name: id
      dtype: string
    - name: type
      dtype:
        class_label:
          names:
            0: context
            1: question
    - name: text
      dtype: string
    - name: supporting_ids
      sequence: string
    - name: answer
      dtype: string
  splits:
  - name: test
    num_bytes: 315396
    num_examples: 200
  - name: train
    num_bytes: 320859
    num_examples: 200
  download_size: 15719851
  dataset_size: 636255
- config_name: hn-qa6
  features:
  - name: story
    sequence:
    - name: id
      dtype: string
    - name: type
      dtype:
        class_label:
          names:
            0: context
            1: question
    - name: text
      dtype: string
    - name: supporting_ids
      sequence: string
    - name: answer
      dtype: string
  splits:
  - name: test
    num_bytes: 171360
    num_examples: 200
  - name: train
    num_bytes: 170796
    num_examples: 200
  download_size: 15719851
  dataset_size: 342156
- config_name: hn-qa7
  features:
  - name: story
    sequence:
    - name: id
      dtype: string
    - name: type
      dtype:
        class_label:
          names:
            0: context
            1: question
    - name: text
      dtype: string
    - name: supporting_ids
      sequence: string
    - name: answer
      dtype: string
  splits:
  - name: test
    num_bytes: 208080
    num_examples: 200
  - name: train
    num_bytes: 206981
    num_examples: 200
  download_size: 15719851
  dataset_size: 415061
- config_name: hn-qa8
  features:
  - name: story
    sequence:
    - name: id
      dtype: string
    - name: type
      dtype:
        class_label:
          names:
            0: context
            1: question
    - name: text
      dtype: string
    - name: supporting_ids
      sequence: string
    - name: answer
      dtype: string
  splits:
  - name: test
    num_bytes: 222232
    num_examples: 200
  - name: train
    num_bytes: 211584
    num_examples: 200
  download_size: 15719851
  dataset_size: 433816
- config_name: hn-qa9
  features:
  - name: story
    sequence:
    - name: id
      dtype: string
    - name: type
      dtype:
        class_label:
          names:
            0: context
            1: question
    - name: text
      dtype: string
    - name: supporting_ids
      sequence: string
    - name: answer
      dtype: string
  splits:
  - name: test
    num_bytes: 187341
    num_examples: 200
  - name: train
    num_bytes: 187718
    num_examples: 200
  download_size: 15719851
  dataset_size: 375059
- config_name: hn-qa10
  features:
  - name: story
    sequence:
    - name: id
      dtype: string
    - name: type
      dtype:
        class_label:
          names:
            0: context
            1: question
    - name: text
      dtype: string
    - name: supporting_ids
      sequence: string
    - name: answer
      dtype: string
  splits:
  - name: test
    num_bytes: 182932
    num_examples: 200
  - name: train
    num_bytes: 183583
    num_examples: 200
  download_size: 15719851
  dataset_size: 366515
- config_name: hn-qa11
  features:
  - name: story
    sequence:
    - name: id
      dtype: string
    - name: type
      dtype:
        class_label:
          names:
            0: context
            1: question
    - name: text
      dtype: string
    - name: supporting_ids
      sequence: string
    - name: answer
      dtype: string
  splits:
  - name: test
    num_bytes: 180461
    num_examples: 200
  - name: train
    num_bytes: 179698
    num_examples: 200
  download_size: 15719851
  dataset_size: 360159
- config_name: hn-qa12
  features:
  - name: story
    sequence:
    - name: id
      dtype: string
    - name: type
      dtype:
        class_label:
          names:
            0: context
            1: question
    - name: text
      dtype: string
    - name: supporting_ids
      sequence: string
    - name: answer
      dtype: string
  splits:
  - name: test
    num_bytes: 187954
    num_examples: 200
  - name: train
    num_bytes: 187731
    num_examples: 200
  download_size: 15719851
  dataset_size: 375685
- config_name: hn-qa13
  features:
  - name: story
    sequence:
    - name: id
      dtype: string
    - name: type
      dtype:
        class_label:
          names:
            0: context
            1: question
    - name: text
      dtype: string
    - name: supporting_ids
      sequence: string
    - name: answer
      dtype: string
  splits:
  - name: test
    num_bytes: 191747
    num_examples: 125
  - name: train
    num_bytes: 191395
    num_examples: 125
  download_size: 15719851
  dataset_size: 383142
- config_name: hn-qa14
  features:
  - name: story
    sequence:
    - name: id
      dtype: string
    - name: type
      dtype:
        class_label:
          names:
            0: context
            1: question
    - name: text
      dtype: string
    - name: supporting_ids
      sequence: string
    - name: answer
      dtype: string
  splits:
  - name: test
    num_bytes: 240436
    num_examples: 200
  - name: train
    num_bytes: 240659
    num_examples: 200
  download_size: 15719851
  dataset_size: 481095
- config_name: hn-qa15
  features:
  - name: story
    sequence:
    - name: id
      dtype: string
    - name: type
      dtype:
        class_label:
          names:
            0: context
            1: question
    - name: text
      dtype: string
    - name: supporting_ids
      sequence: string
    - name: answer
      dtype: string
  splits:
  - name: test
    num_bytes: 170259
    num_examples: 250
  - name: train
    num_bytes: 170358
    num_examples: 250
  download_size: 15719851
  dataset_size: 340617
- config_name: hn-qa16
  features:
  - name: story
    sequence:
    - name: id
      dtype: string
    - name: type
      dtype:
        class_label:
          names:
            0: context
            1: question
    - name: text
      dtype: string
    - name: supporting_ids
      sequence: string
    - name: answer
      dtype: string
  splits:
  - name: test
    num_bytes: 523032
    num_examples: 1000
  - name: train
    num_bytes: 523093
    num_examples: 1000
  download_size: 15719851
  dataset_size: 1046125
- config_name: hn-qa17
  features:
  - name: story
    sequence:
    - name: id
      dtype: string
    - name: type
      dtype:
        class_label:
          names:
            0: context
            1: question
    - name: text
      dtype: string
    - name: supporting_ids
      sequence: string
    - name: answer
      dtype: string
  splits:
  - name: test
    num_bytes: 104061
    num_examples: 125
  - name: train
    num_bytes: 103878
    num_examples: 125
  download_size: 15719851
  dataset_size: 207939
- config_name: hn-qa18
  features:
  - name: story
    sequence:
    - name: id
      dtype: string
    - name: type
      dtype:
        class_label:
          names:
            0: context
            1: question
    - name: text
      dtype: string
    - name: supporting_ids
      sequence: string
    - name: answer
      dtype: string
  splits:
  - name: test
    num_bytes: 176824
    num_examples: 198
  - name: train
    num_bytes: 173056
    num_examples: 198
  download_size: 15719851
  dataset_size: 349880
- config_name: hn-qa19
  features:
  - name: story
    sequence:
    - name: id
      dtype: string
    - name: type
      dtype:
        class_label:
          names:
            0: context
            1: question
    - name: text
      dtype: string
    - name: supporting_ids
      sequence: string
    - name: answer
      dtype: string
  splits:
  - name: test
    num_bytes: 470479
    num_examples: 1000
  - name: train
    num_bytes: 470225
    num_examples: 1000
  download_size: 15719851
  dataset_size: 940704
- config_name: hn-qa20
  features:
  - name: story
    sequence:
    - name: id
      dtype: string
    - name: type
      dtype:
        class_label:
          names:
            0: context
            1: question
    - name: text
      dtype: string
    - name: supporting_ids
      sequence: string
    - name: answer
      dtype: string
  splits:
  - name: test
    num_bytes: 115088
    num_examples: 94
  - name: train
    num_bytes: 115021
    num_examples: 93
  download_size: 15719851
  dataset_size: 230109
- config_name: en-10k-qa1
  features:
  - name: story
    sequence:
    - name: id
      dtype: string
    - name: type
      dtype:
        class_label:
          names:
            0: context
            1: question
    - name: text
      dtype: string
    - name: supporting_ids
      sequence: string
    - name: answer
      dtype: string
  splits:
  - name: test
    num_bytes: 165517
    num_examples: 200
  - name: train
    num_bytes: 1654288
    num_examples: 2000
  download_size: 15719851
  dataset_size: 1819805
- config_name: en-10k-qa2
  features:
  - name: story
    sequence:
    - name: id
      dtype: string
    - name: type
      dtype:
        class_label:
          names:
            0: context
            1: question
    - name: text
      dtype: string
    - name: supporting_ids
      sequence: string
    - name: answer
      dtype: string
  splits:
  - name: test
    num_bytes: 306631
    num_examples: 200
  - name: train
    num_bytes: 3062580
    num_examples: 2000
  download_size: 15719851
  dataset_size: 3369211
- config_name: en-10k-qa3
  features:
  - name: story
    sequence:
    - name: id
      dtype: string
    - name: type
      dtype:
        class_label:
          names:
            0: context
            1: question
    - name: text
      dtype: string
    - name: supporting_ids
      sequence: string
    - name: answer
      dtype: string
  splits:
  - name: test
    num_bytes: 883187
    num_examples: 200
  - name: train
    num_bytes: 8921215
    num_examples: 2000
  download_size: 15719851
  dataset_size: 9804402
- config_name: en-10k-qa4
  features:
  - name: story
    sequence:
    - name: id
      dtype: string
    - name: type
      dtype:
        class_label:
          names:
            0: context
            1: question
    - name: text
      dtype: string
    - name: supporting_ids
      sequence: string
    - name: answer
      dtype: string
  splits:
  - name: test
    num_bytes: 205434
    num_examples: 1000
  - name: train
    num_bytes: 2055105
    num_examples: 10000
  download_size: 15719851
  dataset_size: 2260539
- config_name: en-10k-qa5
  features:
  - name: story
    sequence:
    - name: id
      dtype: string
    - name: type
      dtype:
        class_label:
          names:
            0: context
            1: question
    - name: text
      dtype: string
    - name: supporting_ids
      sequence: string
    - name: answer
      dtype: string
  splits:
  - name: test
    num_bytes: 350457
    num_examples: 200
  - name: train
    num_bytes: 3592157
    num_examples: 2000
  download_size: 15719851
  dataset_size: 3942614
- config_name: en-10k-qa6
  features:
  - name: story
    sequence:
    - name: id
      dtype: string
    - name: type
      dtype:
        class_label:
          names:
            0: context
            1: question
    - name: text
      dtype: string
    - name: supporting_ids
      sequence: string
    - name: answer
      dtype: string
  splits:
  - name: test
    num_bytes: 172249
    num_examples: 200
  - name: train
    num_bytes: 1726716
    num_examples: 2000
  download_size: 15719851
  dataset_size: 1898965
- config_name: en-10k-qa7
  features:
  - name: story
    sequence:
    - name: id
      dtype: string
    - name: type
      dtype:
        class_label:
          names:
            0: context
            1: question
    - name: text
      dtype: string
    - name: supporting_ids
      sequence: string
    - name: answer
      dtype: string
  splits:
  - name: test
    num_bytes: 215512
    num_examples: 200
  - name: train
    num_bytes: 2228087
    num_examples: 2000
  download_size: 15719851
  dataset_size: 2443599
- config_name: en-10k-qa8
  features:
  - name: story
    sequence:
    - name: id
      dtype: string
    - name: type
      dtype:
        class_label:
          names:
            0: context
            1: question
    - name: text
      dtype: string
    - name: supporting_ids
      sequence: string
    - name: answer
      dtype: string
  splits:
  - name: test
    num_bytes: 216244
    num_examples: 200
  - name: train
    num_bytes: 2141880
    num_examples: 2000
  download_size: 15719851
  dataset_size: 2358124
- config_name: en-10k-qa9
  features:
  - name: story
    sequence:
    - name: id
      dtype: string
    - name: type
      dtype:
        class_label:
          names:
            0: context
            1: question
    - name: text
      dtype: string
    - name: supporting_ids
      sequence: string
    - name: answer
      dtype: string
  splits:
  - name: test
    num_bytes: 168248
    num_examples: 200
  - name: train
    num_bytes: 1681213
    num_examples: 2000
  download_size: 15719851
  dataset_size: 1849461
- config_name: en-10k-qa10
  features:
  - name: story
    sequence:
    - name: id
      dtype: string
    - name: type
      dtype:
        class_label:
          names:
            0: context
            1: question
    - name: text
      dtype: string
    - name: supporting_ids
      sequence: string
    - name: answer
      dtype: string
  splits:
  - name: test
    num_bytes: 170672
    num_examples: 200
  - name: train
    num_bytes: 1707675
    num_examples: 2000
  download_size: 15719851
  dataset_size: 1878347
- config_name: en-10k-qa11
  features:
  - name: story
    sequence:
    - name: id
      dtype: string
    - name: type
      dtype:
        class_label:
          names:
            0: context
            1: question
    - name: text
      dtype: string
    - name: supporting_ids
      sequence: string
    - name: answer
      dtype: string
  splits:
  - name: test
    num_bytes: 178840
    num_examples: 200
  - name: train
    num_bytes: 1786179
    num_examples: 2000
  download_size: 15719851
  dataset_size: 1965019
- config_name: en-10k-qa12
  features:
  - name: story
    sequence:
    - name: id
      dtype: string
    - name: type
      dtype:
        class_label:
          names:
            0: context
            1: question
    - name: text
      dtype: string
    - name: supporting_ids
      sequence: string
    - name: answer
      dtype: string
  splits:
  - name: test
    num_bytes: 185529
    num_examples: 200
  - name: train
    num_bytes: 1854745
    num_examples: 2000
  download_size: 15719851
  dataset_size: 2040274
- config_name: en-10k-qa13
  features:
  - name: story
    sequence:
    - name: id
      dtype: string
    - name: type
      dtype:
        class_label:
          names:
            0: context
            1: question
    - name: text
      dtype: string
    - name: supporting_ids
      sequence: string
    - name: answer
      dtype: string
  splits:
  - name: test
    num_bytes: 190484
    num_examples: 200
  - name: train
    num_bytes: 1903149
    num_examples: 2000
  download_size: 15719851
  dataset_size: 2093633
- config_name: en-10k-qa14
  features:
  - name: story
    sequence:
    - name: id
      dtype: string
    - name: type
      dtype:
        class_label:
          names:
            0: context
            1: question
    - name: text
      dtype: string
    - name: supporting_ids
      sequence: string
    - name: answer
      dtype: string
  splits:
  - name: test
    num_bytes: 233204
    num_examples: 200
  - name: train
    num_bytes: 2321511
    num_examples: 2000
  download_size: 15719851
  dataset_size: 2554715
- config_name: en-10k-qa15
  features:
  - name: story
    sequence:
    - name: id
      dtype: string
    - name: type
      dtype:
        class_label:
          names:
            0: context
            1: question
    - name: text
      dtype: string
    - name: supporting_ids
      sequence: string
    - name: answer
      dtype: string
  splits:
  - name: test
    num_bytes: 163809
    num_examples: 250
  - name: train
    num_bytes: 1637398
    num_examples: 2500
  download_size: 15719851
  dataset_size: 1801207
- config_name: en-10k-qa16
  features:
  - name: story
    sequence:
    - name: id
      dtype: string
    - name: type
      dtype:
        class_label:
          names:
            0: context
            1: question
    - name: text
      dtype: string
    - name: supporting_ids
      sequence: string
    - name: answer
      dtype: string
  splits:
  - name: test
    num_bytes: 456248
    num_examples: 1000
  - name: train
    num_bytes: 4562844
    num_examples: 10000
  download_size: 15719851
  dataset_size: 5019092
- config_name: en-10k-qa17
  features:
  - name: story
    sequence:
    - name: id
      dtype: string
    - name: type
      dtype:
        class_label:
          names:
            0: context
            1: question
    - name: text
      dtype: string
    - name: supporting_ids
      sequence: string
    - name: answer
      dtype: string
  splits:
  - name: test
    num_bytes: 103618
    num_examples: 125
  - name: train
    num_bytes: 1034333
    num_examples: 1250
  download_size: 15719851
  dataset_size: 1137951
- config_name: en-10k-qa18
  features:
  - name: story
    sequence:
    - name: id
      dtype: string
    - name: type
      dtype:
        class_label:
          names:
            0: context
            1: question
    - name: text
      dtype: string
    - name: supporting_ids
      sequence: string
    - name: answer
      dtype: string
  splits:
  - name: test
    num_bytes: 161266
    num_examples: 199
  - name: train
    num_bytes: 1641650
    num_examples: 1978
  download_size: 15719851
  dataset_size: 1802916
- config_name: en-10k-qa19
  features:
  - name: story
    sequence:
    - name: id
      dtype: string
    - name: type
      dtype:
        class_label:
          names:
            0: context
            1: question
    - name: text
      dtype: string
    - name: supporting_ids
      sequence: string
    - name: answer
      dtype: string
  splits:
  - name: test
    num_bytes: 404489
    num_examples: 1000
  - name: train
    num_bytes: 4045086
    num_examples: 10000
  download_size: 15719851
  dataset_size: 4449575
- config_name: en-10k-qa20
  features:
  - name: story
    sequence:
    - name: id
      dtype: string
    - name: type
      dtype:
        class_label:
          names:
            0: context
            1: question
    - name: text
      dtype: string
    - name: supporting_ids
      sequence: string
    - name: answer
      dtype: string
  splits:
  - name: test
    num_bytes: 115863
    num_examples: 93
  - name: train
    num_bytes: 1157351
    num_examples: 933
  download_size: 15719851
  dataset_size: 1273214
- config_name: en-valid-qa1
  features:
  - name: story
    sequence:
    - name: id
      dtype: string
    - name: type
      dtype:
        class_label:
          names:
            0: context
            1: question
    - name: text
      dtype: string
    - name: supporting_ids
      sequence: string
    - name: answer
      dtype: string
  splits:
  - name: test
    num_bytes: 165517
    num_examples: 200
  - name: train
    num_bytes: 148887
    num_examples: 180
  - name: validation
    num_bytes: 16539
    num_examples: 20
  download_size: 15719851
  dataset_size: 330943
- config_name: en-valid-qa2
  features:
  - name: story
    sequence:
    - name: id
      dtype: string
    - name: type
      dtype:
        class_label:
          names:
            0: context
            1: question
    - name: text
      dtype: string
    - name: supporting_ids
      sequence: string
    - name: answer
      dtype: string
  splits:
  - name: test
    num_bytes: 306631
    num_examples: 200
  - name: train
    num_bytes: 275106
    num_examples: 180
  - name: validation
    num_bytes: 27822
    num_examples: 20
  download_size: 15719851
  dataset_size: 609559
- config_name: en-valid-qa3
  features:
  - name: story
    sequence:
    - name: id
      dtype: string
    - name: type
      dtype:
        class_label:
          names:
            0: context
            1: question
    - name: text
      dtype: string
    - name: supporting_ids
      sequence: string
    - name: answer
      dtype: string
  splits:
  - name: test
    num_bytes: 883187
    num_examples: 200
  - name: train
    num_bytes: 794565
    num_examples: 180
  - name: validation
    num_bytes: 93231
    num_examples: 20
  download_size: 15719851
  dataset_size: 1770983
- config_name: en-valid-qa4
  features:
  - name: story
    sequence:
    - name: id
      dtype: string
    - name: type
      dtype:
        class_label:
          names:
            0: context
            1: question
    - name: text
      dtype: string
    - name: supporting_ids
      sequence: string
    - name: answer
      dtype: string
  splits:
  - name: test
    num_bytes: 205434
    num_examples: 1000
  - name: train
    num_bytes: 184992
    num_examples: 900
  - name: validation
    num_bytes: 20558
    num_examples: 100
  download_size: 15719851
  dataset_size: 410984
- config_name: en-valid-qa5
  features:
  - name: story
    sequence:
    - name: id
      dtype: string
    - name: type
      dtype:
        class_label:
          names:
            0: context
            1: question
    - name: text
      dtype: string
    - name: supporting_ids
      sequence: string
    - name: answer
      dtype: string
  splits:
  - name: test
    num_bytes: 350457
    num_examples: 200
  - name: train
    num_bytes: 305472
    num_examples: 180
  - name: validation
    num_bytes: 31917
    num_examples: 20
  download_size: 15719851
  dataset_size: 687846
- config_name: en-valid-qa6
  features:
  - name: story
    sequence:
    - name: id
      dtype: string
    - name: type
      dtype:
        class_label:
          names:
            0: context
            1: question
    - name: text
      dtype: string
    - name: supporting_ids
      sequence: string
    - name: answer
      dtype: string
  splits:
  - name: test
    num_bytes: 172249
    num_examples: 200
  - name: train
    num_bytes: 155845
    num_examples: 180
  - name: validation
    num_bytes: 17248
    num_examples: 20
  download_size: 15719851
  dataset_size: 345342
- config_name: en-valid-qa7
  features:
  - name: story
    sequence:
    - name: id
      dtype: string
    - name: type
      dtype:
        class_label:
          names:
            0: context
            1: question
    - name: text
      dtype: string
    - name: supporting_ids
      sequence: string
    - name: answer
      dtype: string
  splits:
  - name: test
    num_bytes: 215512
    num_examples: 200
  - name: train
    num_bytes: 203642
    num_examples: 180
  - name: validation
    num_bytes: 21176
    num_examples: 20
  download_size: 15719851
  dataset_size: 440330
- config_name: en-valid-qa8
  features:
  - name: story
    sequence:
    - name: id
      dtype: string
    - name: type
      dtype:
        class_label:
          names:
            0: context
            1: question
    - name: text
      dtype: string
    - name: supporting_ids
      sequence: string
    - name: answer
      dtype: string
  splits:
  - name: test
    num_bytes: 216244
    num_examples: 200
  - name: train
    num_bytes: 191599
    num_examples: 180
  - name: validation
    num_bytes: 20958
    num_examples: 20
  download_size: 15719851
  dataset_size: 428801
- config_name: en-valid-qa9
  features:
  - name: story
    sequence:
    - name: id
      dtype: string
    - name: type
      dtype:
        class_label:
          names:
            0: context
            1: question
    - name: text
      dtype: string
    - name: supporting_ids
      sequence: string
    - name: answer
      dtype: string
  splits:
  - name: test
    num_bytes: 168248
    num_examples: 200
  - name: train
    num_bytes: 151458
    num_examples: 180
  - name: validation
    num_bytes: 16932
    num_examples: 20
  download_size: 15719851
  dataset_size: 336638
- config_name: en-valid-qa10
  features:
  - name: story
    sequence:
    - name: id
      dtype: string
    - name: type
      dtype:
        class_label:
          names:
            0: context
            1: question
    - name: text
      dtype: string
    - name: supporting_ids
      sequence: string
    - name: answer
      dtype: string
  splits:
  - name: test
    num_bytes: 170672
    num_examples: 200
  - name: train
    num_bytes: 153240
    num_examples: 180
  - name: validation
    num_bytes: 17057
    num_examples: 20
  download_size: 15719851
  dataset_size: 340969
- config_name: en-valid-qa11
  features:
  - name: story
    sequence:
    - name: id
      dtype: string
    - name: type
      dtype:
        class_label:
          names:
            0: context
            1: question
    - name: text
      dtype: string
    - name: supporting_ids
      sequence: string
    - name: answer
      dtype: string
  splits:
  - name: test
    num_bytes: 178840
    num_examples: 200
  - name: train
    num_bytes: 160701
    num_examples: 180
  - name: validation
    num_bytes: 17899
    num_examples: 20
  download_size: 15719851
  dataset_size: 357440
- config_name: en-valid-qa12
  features:
  - name: story
    sequence:
    - name: id
      dtype: string
    - name: type
      dtype:
        class_label:
          names:
            0: context
            1: question
    - name: text
      dtype: string
    - name: supporting_ids
      sequence: string
    - name: answer
      dtype: string
  splits:
  - name: test
    num_bytes: 185529
    num_examples: 200
  - name: train
    num_bytes: 167031
    num_examples: 180
  - name: validation
    num_bytes: 18609
    num_examples: 20
  download_size: 15719851
  dataset_size: 371169
- config_name: en-valid-qa13
  features:
  - name: story
    sequence:
    - name: id
      dtype: string
    - name: type
      dtype:
        class_label:
          names:
            0: context
            1: question
    - name: text
      dtype: string
    - name: supporting_ids
      sequence: string
    - name: answer
      dtype: string
  splits:
  - name: test
    num_bytes: 190484
    num_examples: 200
  - name: train
    num_bytes: 171527
    num_examples: 180
  - name: validation
    num_bytes: 19069
    num_examples: 20
  download_size: 15719851
  dataset_size: 381080
- config_name: en-valid-qa14
  features:
  - name: story
    sequence:
    - name: id
      dtype: string
    - name: type
      dtype:
        class_label:
          names:
            0: context
            1: question
    - name: text
      dtype: string
    - name: supporting_ids
      sequence: string
    - name: answer
      dtype: string
  splits:
  - name: test
    num_bytes: 233204
    num_examples: 200
  - name: train
    num_bytes: 210650
    num_examples: 180
  - name: validation
    num_bytes: 23745
    num_examples: 20
  download_size: 15719851
  dataset_size: 467599
- config_name: en-valid-qa15
  features:
  - name: story
    sequence:
    - name: id
      dtype: string
    - name: type
      dtype:
        class_label:
          names:
            0: context
            1: question
    - name: text
      dtype: string
    - name: supporting_ids
      sequence: string
    - name: answer
      dtype: string
  splits:
  - name: test
    num_bytes: 163809
    num_examples: 250
  - name: train
    num_bytes: 147356
    num_examples: 225
  - name: validation
    num_bytes: 16412
    num_examples: 25
  download_size: 15719851
  dataset_size: 327577
- config_name: en-valid-qa16
  features:
  - name: story
    sequence:
    - name: id
      dtype: string
    - name: type
      dtype:
        class_label:
          names:
            0: context
            1: question
    - name: text
      dtype: string
    - name: supporting_ids
      sequence: string
    - name: answer
      dtype: string
  splits:
  - name: test
    num_bytes: 456248
    num_examples: 1000
  - name: train
    num_bytes: 410711
    num_examples: 900
  - name: validation
    num_bytes: 45703
    num_examples: 100
  download_size: 15719851
  dataset_size: 912662
- config_name: en-valid-qa17
  features:
  - name: story
    sequence:
    - name: id
      dtype: string
    - name: type
      dtype:
        class_label:
          names:
            0: context
            1: question
    - name: text
      dtype: string
    - name: supporting_ids
      sequence: string
    - name: answer
      dtype: string
  splits:
  - name: test
    num_bytes: 103618
    num_examples: 125
  - name: train
    num_bytes: 93596
    num_examples: 113
  - name: validation
    num_bytes: 10080
    num_examples: 12
  download_size: 15719851
  dataset_size: 207294
- config_name: en-valid-qa18
  features:
  - name: story
    sequence:
    - name: id
      dtype: string
    - name: type
      dtype:
        class_label:
          names:
            0: context
            1: question
    - name: text
      dtype: string
    - name: supporting_ids
      sequence: string
    - name: answer
      dtype: string
  splits:
  - name: test
    num_bytes: 161266
    num_examples: 199
  - name: train
    num_bytes: 147338
    num_examples: 179
  - name: validation
    num_bytes: 15577
    num_examples: 19
  download_size: 15719851
  dataset_size: 324181
- config_name: en-valid-qa19
  features:
  - name: story
    sequence:
    - name: id
      dtype: string
    - name: type
      dtype:
        class_label:
          names:
            0: context
            1: question
    - name: text
      dtype: string
    - name: supporting_ids
      sequence: string
    - name: answer
      dtype: string
  splits:
  - name: test
    num_bytes: 404489
    num_examples: 1000
  - name: train
    num_bytes: 364090
    num_examples: 900
  - name: validation
    num_bytes: 40486
    num_examples: 100
  download_size: 15719851
  dataset_size: 809065
- config_name: en-valid-qa20
  features:
  - name: story
    sequence:
    - name: id
      dtype: string
    - name: type
      dtype:
        class_label:
          names:
            0: context
            1: question
    - name: text
      dtype: string
    - name: supporting_ids
      sequence: string
    - name: answer
      dtype: string
  splits:
  - name: test
    num_bytes: 115863
    num_examples: 93
  - name: train
    num_bytes: 104706
    num_examples: 85
  - name: validation
    num_bytes: 11146
    num_examples: 9
  download_size: 15719851
  dataset_size: 231715
- config_name: en-valid-10k-qa1
  features:
  - name: story
    sequence:
    - name: id
      dtype: string
    - name: type
      dtype:
        class_label:
          names:
            0: context
            1: question
    - name: text
      dtype: string
    - name: supporting_ids
      sequence: string
    - name: answer
      dtype: string
  splits:
  - name: test
    num_bytes: 165517
    num_examples: 200
  - name: train
    num_bytes: 1488751
    num_examples: 1800
  - name: validation
    num_bytes: 165577
    num_examples: 200
  download_size: 15719851
  dataset_size: 1819845
- config_name: en-valid-10k-qa2
  features:
  - name: story
    sequence:
    - name: id
      dtype: string
    - name: type
      dtype:
        class_label:
          names:
            0: context
            1: question
    - name: text
      dtype: string
    - name: supporting_ids
      sequence: string
    - name: answer
      dtype: string
  splits:
  - name: test
    num_bytes: 306631
    num_examples: 200
  - name: train
    num_bytes: 2746462
    num_examples: 1800
  - name: validation
    num_bytes: 316158
    num_examples: 200
  download_size: 15719851
  dataset_size: 3369251
- config_name: en-valid-10k-qa3
  features:
  - name: story
    sequence:
    - name: id
      dtype: string
    - name: type
      dtype:
        class_label:
          names:
            0: context
            1: question
    - name: text
      dtype: string
    - name: supporting_ids
      sequence: string
    - name: answer
      dtype: string
  splits:
  - name: test
    num_bytes: 883187
    num_examples: 200
  - name: train
    num_bytes: 8021847
    num_examples: 1800
  - name: validation
    num_bytes: 899408
    num_examples: 200
  download_size: 15719851
  dataset_size: 9804442
- config_name: en-valid-10k-qa4
  features:
  - name: story
    sequence:
    - name: id
      dtype: string
    - name: type
      dtype:
        class_label:
          names:
            0: context
            1: question
    - name: text
      dtype: string
    - name: supporting_ids
      sequence: string
    - name: answer
      dtype: string
  splits:
  - name: test
    num_bytes: 205434
    num_examples: 1000
  - name: train
    num_bytes: 1849497
    num_examples: 9000
  - name: validation
    num_bytes: 205648
    num_examples: 1000
  download_size: 15719851
  dataset_size: 2260579
- config_name: en-valid-10k-qa5
  features:
  - name: story
    sequence:
    - name: id
      dtype: string
    - name: type
      dtype:
        class_label:
          names:
            0: context
            1: question
    - name: text
      dtype: string
    - name: supporting_ids
      sequence: string
    - name: answer
      dtype: string
  splits:
  - name: test
    num_bytes: 350457
    num_examples: 200
  - name: train
    num_bytes: 3234186
    num_examples: 1800
  - name: validation
    num_bytes: 358011
    num_examples: 200
  download_size: 15719851
  dataset_size: 3942654
- config_name: en-valid-10k-qa6
  features:
  - name: story
    sequence:
    - name: id
      dtype: string
    - name: type
      dtype:
        class_label:
          names:
            0: context
            1: question
    - name: text
      dtype: string
    - name: supporting_ids
      sequence: string
    - name: answer
      dtype: string
  splits:
  - name: test
    num_bytes: 172249
    num_examples: 200
  - name: train
    num_bytes: 1553957
    num_examples: 1800
  - name: validation
    num_bytes: 172799
    num_examples: 200
  download_size: 15719851
  dataset_size: 1899005
- config_name: en-valid-10k-qa7
  features:
  - name: story
    sequence:
    - name: id
      dtype: string
    - name: type
      dtype:
        class_label:
          names:
            0: context
            1: question
    - name: text
      dtype: string
    - name: supporting_ids
      sequence: string
    - name: answer
      dtype: string
  splits:
  - name: test
    num_bytes: 215512
    num_examples: 200
  - name: train
    num_bytes: 2003820
    num_examples: 1800
  - name: validation
    num_bytes: 224307
    num_examples: 200
  download_size: 15719851
  dataset_size: 2443639
- config_name: en-valid-10k-qa8
  features:
  - name: story
    sequence:
    - name: id
      dtype: string
    - name: type
      dtype:
        class_label:
          names:
            0: context
            1: question
    - name: text
      dtype: string
    - name: supporting_ids
      sequence: string
    - name: answer
      dtype: string
  splits:
  - name: test
    num_bytes: 216244
    num_examples: 200
  - name: train
    num_bytes: 1926339
    num_examples: 1800
  - name: validation
    num_bytes: 215581
    num_examples: 200
  download_size: 15719851
  dataset_size: 2358164
- config_name: en-valid-10k-qa9
  features:
  - name: story
    sequence:
    - name: id
      dtype: string
    - name: type
      dtype:
        class_label:
          names:
            0: context
            1: question
    - name: text
      dtype: string
    - name: supporting_ids
      sequence: string
    - name: answer
      dtype: string
  splits:
  - name: test
    num_bytes: 168248
    num_examples: 200
  - name: train
    num_bytes: 1512917
    num_examples: 1800
  - name: validation
    num_bytes: 168336
    num_examples: 200
  download_size: 15719851
  dataset_size: 1849501
- config_name: en-valid-10k-qa10
  features:
  - name: story
    sequence:
    - name: id
      dtype: string
    - name: type
      dtype:
        class_label:
          names:
            0: context
            1: question
    - name: text
      dtype: string
    - name: supporting_ids
      sequence: string
    - name: answer
      dtype: string
  splits:
  - name: test
    num_bytes: 170672
    num_examples: 200
  - name: train
    num_bytes: 1536416
    num_examples: 1800
  - name: validation
    num_bytes: 171299
    num_examples: 200
  download_size: 15719851
  dataset_size: 1878387
- config_name: en-valid-10k-qa11
  features:
  - name: story
    sequence:
    - name: id
      dtype: string
    - name: type
      dtype:
        class_label:
          names:
            0: context
            1: question
    - name: text
      dtype: string
    - name: supporting_ids
      sequence: string
    - name: answer
      dtype: string
  splits:
  - name: test
    num_bytes: 178840
    num_examples: 200
  - name: train
    num_bytes: 1607505
    num_examples: 1800
  - name: validation
    num_bytes: 178714
    num_examples: 200
  download_size: 15719851
  dataset_size: 1965059
- config_name: en-valid-10k-qa12
  features:
  - name: story
    sequence:
    - name: id
      dtype: string
    - name: type
      dtype:
        class_label:
          names:
            0: context
            1: question
    - name: text
      dtype: string
    - name: supporting_ids
      sequence: string
    - name: answer
      dtype: string
  splits:
  - name: test
    num_bytes: 185529
    num_examples: 200
  - name: train
    num_bytes: 1669198
    num_examples: 1800
  - name: validation
    num_bytes: 185587
    num_examples: 200
  download_size: 15719851
  dataset_size: 2040314
- config_name: en-valid-10k-qa13
  features:
  - name: story
    sequence:
    - name: id
      dtype: string
    - name: type
      dtype:
        class_label:
          names:
            0: context
            1: question
    - name: text
      dtype: string
    - name: supporting_ids
      sequence: string
    - name: answer
      dtype: string
  splits:
  - name: test
    num_bytes: 190484
    num_examples: 200
  - name: train
    num_bytes: 1712558
    num_examples: 1800
  - name: validation
    num_bytes: 190631
    num_examples: 200
  download_size: 15719851
  dataset_size: 2093673
- config_name: en-valid-10k-qa14
  features:
  - name: story
    sequence:
    - name: id
      dtype: string
    - name: type
      dtype:
        class_label:
          names:
            0: context
            1: question
    - name: text
      dtype: string
    - name: supporting_ids
      sequence: string
    - name: answer
      dtype: string
  splits:
  - name: test
    num_bytes: 233204
    num_examples: 200
  - name: train
    num_bytes: 2091491
    num_examples: 1800
  - name: validation
    num_bytes: 230060
    num_examples: 200
  download_size: 15719851
  dataset_size: 2554755
- config_name: en-valid-10k-qa15
  features:
  - name: story
    sequence:
    - name: id
      dtype: string
    - name: type
      dtype:
        class_label:
          names:
            0: context
            1: question
    - name: text
      dtype: string
    - name: supporting_ids
      sequence: string
    - name: answer
      dtype: string
  splits:
  - name: test
    num_bytes: 163809
    num_examples: 250
  - name: train
    num_bytes: 1473615
    num_examples: 2250
  - name: validation
    num_bytes: 163823
    num_examples: 250
  download_size: 15719851
  dataset_size: 1801247
- config_name: en-valid-10k-qa16
  features:
  - name: story
    sequence:
    - name: id
      dtype: string
    - name: type
      dtype:
        class_label:
          names:
            0: context
            1: question
    - name: text
      dtype: string
    - name: supporting_ids
      sequence: string
    - name: answer
      dtype: string
  splits:
  - name: test
    num_bytes: 456248
    num_examples: 1000
  - name: train
    num_bytes: 4106444
    num_examples: 9000
  - name: validation
    num_bytes: 456440
    num_examples: 1000
  download_size: 15719851
  dataset_size: 5019132
- config_name: en-valid-10k-qa17
  features:
  - name: story
    sequence:
    - name: id
      dtype: string
    - name: type
      dtype:
        class_label:
          names:
            0: context
            1: question
    - name: text
      dtype: string
    - name: supporting_ids
      sequence: string
    - name: answer
      dtype: string
  splits:
  - name: test
    num_bytes: 103618
    num_examples: 125
  - name: train
    num_bytes: 930465
    num_examples: 1125
  - name: validation
    num_bytes: 103908
    num_examples: 125
  download_size: 15719851
  dataset_size: 1137991
- config_name: en-valid-10k-qa18
  features:
  - name: story
    sequence:
    - name: id
      dtype: string
    - name: type
      dtype:
        class_label:
          names:
            0: context
            1: question
    - name: text
      dtype: string
    - name: supporting_ids
      sequence: string
    - name: answer
      dtype: string
  splits:
  - name: test
    num_bytes: 161266
    num_examples: 199
  - name: train
    num_bytes: 1477467
    num_examples: 1781
  - name: validation
    num_bytes: 164223
    num_examples: 197
  download_size: 15719851
  dataset_size: 1802956
- config_name: en-valid-10k-qa19
  features:
  - name: story
    sequence:
    - name: id
      dtype: string
    - name: type
      dtype:
        class_label:
          names:
            0: context
            1: question
    - name: text
      dtype: string
    - name: supporting_ids
      sequence: string
    - name: answer
      dtype: string
  splits:
  - name: test
    num_bytes: 404489
    num_examples: 1000
  - name: train
    num_bytes: 3640527
    num_examples: 9000
  - name: validation
    num_bytes: 404599
    num_examples: 1000
  download_size: 15719851
  dataset_size: 4449615
- config_name: en-valid-10k-qa20
  features:
  - name: story
    sequence:
    - name: id
      dtype: string
    - name: type
      dtype:
        class_label:
          names:
            0: context
            1: question
    - name: text
      dtype: string
    - name: supporting_ids
      sequence: string
    - name: answer
      dtype: string
  splits:
  - name: test
    num_bytes: 115863
    num_examples: 93
  - name: train
    num_bytes: 1041856
    num_examples: 840
  - name: validation
    num_bytes: 115535
    num_examples: 93
  download_size: 15719851
  dataset_size: 1273254
- config_name: hn-10k-qa1
  features:
  - name: story
    sequence:
    - name: id
      dtype: string
    - name: type
      dtype:
        class_label:
          names:
            0: context
            1: question
    - name: text
      dtype: string
    - name: supporting_ids
      sequence: string
    - name: answer
      dtype: string
  splits:
  - name: test
    num_bytes: 168572
    num_examples: 200
  - name: train
    num_bytes: 1684003
    num_examples: 2000
  download_size: 15719851
  dataset_size: 1852575
- config_name: hn-10k-qa2
  features:
  - name: story
    sequence:
    - name: id
      dtype: string
    - name: type
      dtype:
        class_label:
          names:
            0: context
            1: question
    - name: text
      dtype: string
    - name: supporting_ids
      sequence: string
    - name: answer
      dtype: string
  splits:
  - name: test
    num_bytes: 288429
    num_examples: 200
  - name: train
    num_bytes: 2934642
    num_examples: 2000
  download_size: 15719851
  dataset_size: 3223071
- config_name: hn-10k-qa3
  features:
  - name: story
    sequence:
    - name: id
      dtype: string
    - name: type
      dtype:
        class_label:
          names:
            0: context
            1: question
    - name: text
      dtype: string
    - name: supporting_ids
      sequence: string
    - name: answer
      dtype: string
  splits:
  - name: test
    num_bytes: 808460
    num_examples: 167
  - name: train
    num_bytes: 8440008
    num_examples: 1667
  download_size: 15719851
  dataset_size: 9248468
- config_name: hn-10k-qa4
  features:
  - name: story
    sequence:
    - name: id
      dtype: string
    - name: type
      dtype:
        class_label:
          names:
            0: context
            1: question
    - name: text
      dtype: string
    - name: supporting_ids
      sequence: string
    - name: answer
      dtype: string
  splits:
  - name: test
    num_bytes: 231230
    num_examples: 1000
  - name: train
    num_bytes: 2312075
    num_examples: 10000
  download_size: 15719851
  dataset_size: 2543305
- config_name: hn-10k-qa5
  features:
  - name: story
    sequence:
    - name: id
      dtype: string
    - name: type
      dtype:
        class_label:
          names:
            0: context
            1: question
    - name: text
      dtype: string
    - name: supporting_ids
      sequence: string
    - name: answer
      dtype: string
  splits:
  - name: test
    num_bytes: 315396
    num_examples: 200
  - name: train
    num_bytes: 3301271
    num_examples: 2000
  download_size: 15719851
  dataset_size: 3616667
- config_name: hn-10k-qa6
  features:
  - name: story
    sequence:
    - name: id
      dtype: string
    - name: type
      dtype:
        class_label:
          names:
            0: context
            1: question
    - name: text
      dtype: string
    - name: supporting_ids
      sequence: string
    - name: answer
      dtype: string
  splits:
  - name: test
    num_bytes: 171360
    num_examples: 200
  - name: train
    num_bytes: 1703863
    num_examples: 2000
  download_size: 15719851
  dataset_size: 1875223
- config_name: hn-10k-qa7
  features:
  - name: story
    sequence:
    - name: id
      dtype: string
    - name: type
      dtype:
        class_label:
          names:
            0: context
            1: question
    - name: text
      dtype: string
    - name: supporting_ids
      sequence: string
    - name: answer
      dtype: string
  splits:
  - name: test
    num_bytes: 208080
    num_examples: 200
  - name: train
    num_bytes: 2091460
    num_examples: 2000
  download_size: 15719851
  dataset_size: 2299540
- config_name: hn-10k-qa8
  features:
  - name: story
    sequence:
    - name: id
      dtype: string
    - name: type
      dtype:
        class_label:
          names:
            0: context
            1: question
    - name: text
      dtype: string
    - name: supporting_ids
      sequence: string
    - name: answer
      dtype: string
  splits:
  - name: test
    num_bytes: 222232
    num_examples: 200
  - name: train
    num_bytes: 2178277
    num_examples: 2000
  download_size: 15719851
  dataset_size: 2400509
- config_name: hn-10k-qa9
  features:
  - name: story
    sequence:
    - name: id
      dtype: string
    - name: type
      dtype:
        class_label:
          names:
            0: context
            1: question
    - name: text
      dtype: string
    - name: supporting_ids
      sequence: string
    - name: answer
      dtype: string
  splits:
  - name: test
    num_bytes: 187341
    num_examples: 200
  - name: train
    num_bytes: 1874753
    num_examples: 2000
  download_size: 15719851
  dataset_size: 2062094
- config_name: hn-10k-qa10
  features:
  - name: story
    sequence:
    - name: id
      dtype: string
    - name: type
      dtype:
        class_label:
          names:
            0: context
            1: question
    - name: text
      dtype: string
    - name: supporting_ids
      sequence: string
    - name: answer
      dtype: string
  splits:
  - name: test
    num_bytes: 182932
    num_examples: 200
  - name: train
    num_bytes: 1830698
    num_examples: 2000
  download_size: 15719851
  dataset_size: 2013630
- config_name: hn-10k-qa11
  features:
  - name: story
    sequence:
    - name: id
      dtype: string
    - name: type
      dtype:
        class_label:
          names:
            0: context
            1: question
    - name: text
      dtype: string
    - name: supporting_ids
      sequence: string
    - name: answer
      dtype: string
  splits:
  - name: test
    num_bytes: 180461
    num_examples: 200
  - name: train
    num_bytes: 1798057
    num_examples: 2000
  download_size: 15719851
  dataset_size: 1978518
- config_name: hn-10k-qa12
  features:
  - name: story
    sequence:
    - name: id
      dtype: string
    - name: type
      dtype:
        class_label:
          names:
            0: context
            1: question
    - name: text
      dtype: string
    - name: supporting_ids
      sequence: string
    - name: answer
      dtype: string
  splits:
  - name: test
    num_bytes: 187954
    num_examples: 200
  - name: train
    num_bytes: 1879776
    num_examples: 2000
  download_size: 15719851
  dataset_size: 2067730
- config_name: hn-10k-qa13
  features:
  - name: story
    sequence:
    - name: id
      dtype: string
    - name: type
      dtype:
        class_label:
          names:
            0: context
            1: question
    - name: text
      dtype: string
    - name: supporting_ids
      sequence: string
    - name: answer
      dtype: string
  splits:
  - name: test
    num_bytes: 191747
    num_examples: 125
  - name: train
    num_bytes: 1915482
    num_examples: 1250
  download_size: 15719851
  dataset_size: 2107229
- config_name: hn-10k-qa14
  features:
  - name: story
    sequence:
    - name: id
      dtype: string
    - name: type
      dtype:
        class_label:
          names:
            0: context
            1: question
    - name: text
      dtype: string
    - name: supporting_ids
      sequence: string
    - name: answer
      dtype: string
  splits:
  - name: test
    num_bytes: 240436
    num_examples: 200
  - name: train
    num_bytes: 2392212
    num_examples: 2000
  download_size: 15719851
  dataset_size: 2632648
- config_name: hn-10k-qa15
  features:
  - name: story
    sequence:
    - name: id
      dtype: string
    - name: type
      dtype:
        class_label:
          names:
            0: context
            1: question
    - name: text
      dtype: string
    - name: supporting_ids
      sequence: string
    - name: answer
      dtype: string
  splits:
  - name: test
    num_bytes: 170259
    num_examples: 250
  - name: train
    num_bytes: 1702512
    num_examples: 2500
  download_size: 15719851
  dataset_size: 1872771
- config_name: hn-10k-qa16
  features:
  - name: story
    sequence:
    - name: id
      dtype: string
    - name: type
      dtype:
        class_label:
          names:
            0: context
            1: question
    - name: text
      dtype: string
    - name: supporting_ids
      sequence: string
    - name: answer
      dtype: string
  splits:
  - name: test
    num_bytes: 523032
    num_examples: 1000
  - name: train
    num_bytes: 5229983
    num_examples: 10000
  download_size: 15719851
  dataset_size: 5753015
- config_name: hn-10k-qa17
  features:
  - name: story
    sequence:
    - name: id
      dtype: string
    - name: type
      dtype:
        class_label:
          names:
            0: context
            1: question
    - name: text
      dtype: string
    - name: supporting_ids
      sequence: string
    - name: answer
      dtype: string
  splits:
  - name: test
    num_bytes: 104061
    num_examples: 125
  - name: train
    num_bytes: 1039729
    num_examples: 1250
  download_size: 15719851
  dataset_size: 1143790
- config_name: hn-10k-qa18
  features:
  - name: story
    sequence:
    - name: id
      dtype: string
    - name: type
      dtype:
        class_label:
          names:
            0: context
            1: question
    - name: text
      dtype: string
    - name: supporting_ids
      sequence: string
    - name: answer
      dtype: string
  splits:
  - name: test
    num_bytes: 176824
    num_examples: 198
  - name: train
    num_bytes: 1738458
    num_examples: 1977
  download_size: 15719851
  dataset_size: 1915282
- config_name: hn-10k-qa19
  features:
  - name: story
    sequence:
    - name: id
      dtype: string
    - name: type
      dtype:
        class_label:
          names:
            0: context
            1: question
    - name: text
      dtype: string
    - name: supporting_ids
      sequence: string
    - name: answer
      dtype: string
  splits:
  - name: test
    num_bytes: 470479
    num_examples: 1000
  - name: train
    num_bytes: 4702044
    num_examples: 10000
  download_size: 15719851
  dataset_size: 5172523
- config_name: hn-10k-qa20
  features:
  - name: story
    sequence:
    - name: id
      dtype: string
    - name: type
      dtype:
        class_label:
          names:
            0: context
            1: question
    - name: text
      dtype: string
    - name: supporting_ids
      sequence: string
    - name: answer
      dtype: string
  splits:
  - name: test
    num_bytes: 115088
    num_examples: 94
  - name: train
    num_bytes: 1147599
    num_examples: 934
  download_size: 15719851
  dataset_size: 1262687
- config_name: shuffled-qa1
  features:
  - name: story
    sequence:
    - name: id
      dtype: string
    - name: type
      dtype:
        class_label:
          names:
            0: context
            1: question
    - name: text
      dtype: string
    - name: supporting_ids
      sequence: string
    - name: answer
      dtype: string
  splits:
  - name: test
    num_bytes: 165517
    num_examples: 200
  - name: train
    num_bytes: 165386
    num_examples: 200
  download_size: 15719851
  dataset_size: 330903
- config_name: shuffled-qa2
  features:
  - name: story
    sequence:
    - name: id
      dtype: string
    - name: type
      dtype:
        class_label:
          names:
            0: context
            1: question
    - name: text
      dtype: string
    - name: supporting_ids
      sequence: string
    - name: answer
      dtype: string
  splits:
  - name: test
    num_bytes: 306631
    num_examples: 200
  - name: train
    num_bytes: 302888
    num_examples: 200
  download_size: 15719851
  dataset_size: 609519
- config_name: shuffled-qa3
  features:
  - name: story
    sequence:
    - name: id
      dtype: string
    - name: type
      dtype:
        class_label:
          names:
            0: context
            1: question
    - name: text
      dtype: string
    - name: supporting_ids
      sequence: string
    - name: answer
      dtype: string
  splits:
  - name: test
    num_bytes: 883187
    num_examples: 200
  - name: train
    num_bytes: 887756
    num_examples: 200
  download_size: 15719851
  dataset_size: 1770943
- config_name: shuffled-qa4
  features:
  - name: story
    sequence:
    - name: id
      dtype: string
    - name: type
      dtype:
        class_label:
          names:
            0: context
            1: question
    - name: text
      dtype: string
    - name: supporting_ids
      sequence: string
    - name: answer
      dtype: string
  splits:
  - name: test
    num_bytes: 205434
    num_examples: 1000
  - name: train
    num_bytes: 205510
    num_examples: 1000
  download_size: 15719851
  dataset_size: 410944
- config_name: shuffled-qa5
  features:
  - name: story
    sequence:
    - name: id
      dtype: string
    - name: type
      dtype:
        class_label:
          names:
            0: context
            1: question
    - name: text
      dtype: string
    - name: supporting_ids
      sequence: string
    - name: answer
      dtype: string
  splits:
  - name: test
    num_bytes: 350457
    num_examples: 200
  - name: train
    num_bytes: 337349
    num_examples: 200
  download_size: 15719851
  dataset_size: 687806
- config_name: shuffled-qa6
  features:
  - name: story
    sequence:
    - name: id
      dtype: string
    - name: type
      dtype:
        class_label:
          names:
            0: context
            1: question
    - name: text
      dtype: string
    - name: supporting_ids
      sequence: string
    - name: answer
      dtype: string
  splits:
  - name: test
    num_bytes: 172249
    num_examples: 200
  - name: train
    num_bytes: 173053
    num_examples: 200
  download_size: 15719851
  dataset_size: 345302
- config_name: shuffled-qa7
  features:
  - name: story
    sequence:
    - name: id
      dtype: string
    - name: type
      dtype:
        class_label:
          names:
            0: context
            1: question
    - name: text
      dtype: string
    - name: supporting_ids
      sequence: string
    - name: answer
      dtype: string
  splits:
  - name: test
    num_bytes: 215512
    num_examples: 200
  - name: train
    num_bytes: 224778
    num_examples: 200
  download_size: 15719851
  dataset_size: 440290
- config_name: shuffled-qa8
  features:
  - name: story
    sequence:
    - name: id
      dtype: string
    - name: type
      dtype:
        class_label:
          names:
            0: context
            1: question
    - name: text
      dtype: string
    - name: supporting_ids
      sequence: string
    - name: answer
      dtype: string
  splits:
  - name: test
    num_bytes: 216244
    num_examples: 200
  - name: train
    num_bytes: 212517
    num_examples: 200
  download_size: 15719851
  dataset_size: 428761
- config_name: shuffled-qa9
  features:
  - name: story
    sequence:
    - name: id
      dtype: string
    - name: type
      dtype:
        class_label:
          names:
            0: context
            1: question
    - name: text
      dtype: string
    - name: supporting_ids
      sequence: string
    - name: answer
      dtype: string
  splits:
  - name: test
    num_bytes: 168248
    num_examples: 200
  - name: train
    num_bytes: 168350
    num_examples: 200
  download_size: 15719851
  dataset_size: 336598
- config_name: shuffled-qa10
  features:
  - name: story
    sequence:
    - name: id
      dtype: string
    - name: type
      dtype:
        class_label:
          names:
            0: context
            1: question
    - name: text
      dtype: string
    - name: supporting_ids
      sequence: string
    - name: answer
      dtype: string
  splits:
  - name: test
    num_bytes: 170672
    num_examples: 200
  - name: train
    num_bytes: 170257
    num_examples: 200
  download_size: 15719851
  dataset_size: 340929
- config_name: shuffled-qa11
  features:
  - name: story
    sequence:
    - name: id
      dtype: string
    - name: type
      dtype:
        class_label:
          names:
            0: context
            1: question
    - name: text
      dtype: string
    - name: supporting_ids
      sequence: string
    - name: answer
      dtype: string
  splits:
  - name: test
    num_bytes: 178313
    num_examples: 200
  - name: train
    num_bytes: 178083
    num_examples: 200
  download_size: 15719851
  dataset_size: 356396
- config_name: shuffled-qa12
  features:
  - name: story
    sequence:
    - name: id
      dtype: string
    - name: type
      dtype:
        class_label:
          names:
            0: context
            1: question
    - name: text
      dtype: string
    - name: supporting_ids
      sequence: string
    - name: answer
      dtype: string
  splits:
  - name: test
    num_bytes: 185529
    num_examples: 200
  - name: train
    num_bytes: 185600
    num_examples: 200
  download_size: 15719851
  dataset_size: 371129
- config_name: shuffled-qa13
  features:
  - name: story
    sequence:
    - name: id
      dtype: string
    - name: type
      dtype:
        class_label:
          names:
            0: context
            1: question
    - name: text
      dtype: string
    - name: supporting_ids
      sequence: string
    - name: answer
      dtype: string
  splits:
  - name: test
    num_bytes: 190484
    num_examples: 200
  - name: train
    num_bytes: 190556
    num_examples: 200
  download_size: 15719851
  dataset_size: 381040
- config_name: shuffled-qa14
  features:
  - name: story
    sequence:
    - name: id
      dtype: string
    - name: type
      dtype:
        class_label:
          names:
            0: context
            1: question
    - name: text
      dtype: string
    - name: supporting_ids
      sequence: string
    - name: answer
      dtype: string
  splits:
  - name: test
    num_bytes: 233204
    num_examples: 200
  - name: train
    num_bytes: 234355
    num_examples: 200
  download_size: 15719851
  dataset_size: 467559
- config_name: shuffled-qa15
  features:
  - name: story
    sequence:
    - name: id
      dtype: string
    - name: type
      dtype:
        class_label:
          names:
            0: context
            1: question
    - name: text
      dtype: string
    - name: supporting_ids
      sequence: string
    - name: answer
      dtype: string
  splits:
  - name: test
    num_bytes: 163809
    num_examples: 250
  - name: train
    num_bytes: 163728
    num_examples: 250
  download_size: 15719851
  dataset_size: 327537
- config_name: shuffled-qa16
  features:
  - name: story
    sequence:
    - name: id
      dtype: string
    - name: type
      dtype:
        class_label:
          names:
            0: context
            1: question
    - name: text
      dtype: string
    - name: supporting_ids
      sequence: string
    - name: answer
      dtype: string
  splits:
  - name: test
    num_bytes: 456248
    num_examples: 1000
  - name: train
    num_bytes: 456374
    num_examples: 1000
  download_size: 15719851
  dataset_size: 912622
- config_name: shuffled-qa17
  features:
  - name: story
    sequence:
    - name: id
      dtype: string
    - name: type
      dtype:
        class_label:
          names:
            0: context
            1: question
    - name: text
      dtype: string
    - name: supporting_ids
      sequence: string
    - name: answer
      dtype: string
  splits:
  - name: test
    num_bytes: 103618
    num_examples: 125
  - name: train
    num_bytes: 103636
    num_examples: 125
  download_size: 15719851
  dataset_size: 207254
- config_name: shuffled-qa18
  features:
  - name: story
    sequence:
    - name: id
      dtype: string
    - name: type
      dtype:
        class_label:
          names:
            0: context
            1: question
    - name: text
      dtype: string
    - name: supporting_ids
      sequence: string
    - name: answer
      dtype: string
  splits:
  - name: test
    num_bytes: 161266
    num_examples: 199
  - name: train
    num_bytes: 162875
    num_examples: 198
  download_size: 15719851
  dataset_size: 324141
- config_name: shuffled-qa19
  features:
  - name: story
    sequence:
    - name: id
      dtype: string
    - name: type
      dtype:
        class_label:
          names:
            0: context
            1: question
    - name: text
      dtype: string
    - name: supporting_ids
      sequence: string
    - name: answer
      dtype: string
  splits:
  - name: test
    num_bytes: 404489
    num_examples: 1000
  - name: train
    num_bytes: 404536
    num_examples: 1000
  download_size: 15719851
  dataset_size: 809025
- config_name: shuffled-qa20
  features:
  - name: story
    sequence:
    - name: id
      dtype: string
    - name: type
      dtype:
        class_label:
          names:
            0: context
            1: question
    - name: text
      dtype: string
    - name: supporting_ids
      sequence: string
    - name: answer
      dtype: string
  splits:
  - name: test
    num_bytes: 115863
    num_examples: 93
  - name: train
    num_bytes: 115812
    num_examples: 94
  download_size: 15719851
  dataset_size: 231675
- config_name: shuffled-10k-qa1
  features:
  - name: story
    sequence:
    - name: id
      dtype: string
    - name: type
      dtype:
        class_label:
          names:
            0: context
            1: question
    - name: text
      dtype: string
    - name: supporting_ids
      sequence: string
    - name: answer
      dtype: string
  splits:
  - name: test
    num_bytes: 165517
    num_examples: 200
  - name: train
    num_bytes: 1654288
    num_examples: 2000
  download_size: 15719851
  dataset_size: 1819805
- config_name: shuffled-10k-qa2
  features:
  - name: story
    sequence:
    - name: id
      dtype: string
    - name: type
      dtype:
        class_label:
          names:
            0: context
            1: question
    - name: text
      dtype: string
    - name: supporting_ids
      sequence: string
    - name: answer
      dtype: string
  splits:
  - name: test
    num_bytes: 306631
    num_examples: 200
  - name: train
    num_bytes: 3062580
    num_examples: 2000
  download_size: 15719851
  dataset_size: 3369211
- config_name: shuffled-10k-qa3
  features:
  - name: story
    sequence:
    - name: id
      dtype: string
    - name: type
      dtype:
        class_label:
          names:
            0: context
            1: question
    - name: text
      dtype: string
    - name: supporting_ids
      sequence: string
    - name: answer
      dtype: string
  splits:
  - name: test
    num_bytes: 883187
    num_examples: 200
  - name: train
    num_bytes: 8921215
    num_examples: 2000
  download_size: 15719851
  dataset_size: 9804402
- config_name: shuffled-10k-qa4
  features:
  - name: story
    sequence:
    - name: id
      dtype: string
    - name: type
      dtype:
        class_label:
          names:
            0: context
            1: question
    - name: text
      dtype: string
    - name: supporting_ids
      sequence: string
    - name: answer
      dtype: string
  splits:
  - name: test
    num_bytes: 205434
    num_examples: 1000
  - name: train
    num_bytes: 2055105
    num_examples: 10000
  download_size: 15719851
  dataset_size: 2260539
- config_name: shuffled-10k-qa5
  features:
  - name: story
    sequence:
    - name: id
      dtype: string
    - name: type
      dtype:
        class_label:
          names:
            0: context
            1: question
    - name: text
      dtype: string
    - name: supporting_ids
      sequence: string
    - name: answer
      dtype: string
  splits:
  - name: test
    num_bytes: 350457
    num_examples: 200
  - name: train
    num_bytes: 3592157
    num_examples: 2000
  download_size: 15719851
  dataset_size: 3942614
- config_name: shuffled-10k-qa6
  features:
  - name: story
    sequence:
    - name: id
      dtype: string
    - name: type
      dtype:
        class_label:
          names:
            0: context
            1: question
    - name: text
      dtype: string
    - name: supporting_ids
      sequence: string
    - name: answer
      dtype: string
  splits:
  - name: test
    num_bytes: 172249
    num_examples: 200
  - name: train
    num_bytes: 1726716
    num_examples: 2000
  download_size: 15719851
  dataset_size: 1898965
- config_name: shuffled-10k-qa7
  features:
  - name: story
    sequence:
    - name: id
      dtype: string
    - name: type
      dtype:
        class_label:
          names:
            0: context
            1: question
    - name: text
      dtype: string
    - name: supporting_ids
      sequence: string
    - name: answer
      dtype: string
  splits:
  - name: test
    num_bytes: 215512
    num_examples: 200
  - name: train
    num_bytes: 2228087
    num_examples: 2000
  download_size: 15719851
  dataset_size: 2443599
- config_name: shuffled-10k-qa8
  features:
  - name: story
    sequence:
    - name: id
      dtype: string
    - name: type
      dtype:
        class_label:
          names:
            0: context
            1: question
    - name: text
      dtype: string
    - name: supporting_ids
      sequence: string
    - name: answer
      dtype: string
  splits:
  - name: test
    num_bytes: 216244
    num_examples: 200
  - name: train
    num_bytes: 2141880
    num_examples: 2000
  download_size: 15719851
  dataset_size: 2358124
- config_name: shuffled-10k-qa9
  features:
  - name: story
    sequence:
    - name: id
      dtype: string
    - name: type
      dtype:
        class_label:
          names:
            0: context
            1: question
    - name: text
      dtype: string
    - name: supporting_ids
      sequence: string
    - name: answer
      dtype: string
  splits:
  - name: test
    num_bytes: 168248
    num_examples: 200
  - name: train
    num_bytes: 1681213
    num_examples: 2000
  download_size: 15719851
  dataset_size: 1849461
- config_name: shuffled-10k-qa10
  features:
  - name: story
    sequence:
    - name: id
      dtype: string
    - name: type
      dtype:
        class_label:
          names:
            0: context
            1: question
    - name: text
      dtype: string
    - name: supporting_ids
      sequence: string
    - name: answer
      dtype: string
  splits:
  - name: test
    num_bytes: 170672
    num_examples: 200
  - name: train
    num_bytes: 1707675
    num_examples: 2000
  download_size: 15719851
  dataset_size: 1878347
- config_name: shuffled-10k-qa11
  features:
  - name: story
    sequence:
    - name: id
      dtype: string
    - name: type
      dtype:
        class_label:
          names:
            0: context
            1: question
    - name: text
      dtype: string
    - name: supporting_ids
      sequence: string
    - name: answer
      dtype: string
  splits:
  - name: test
    num_bytes: 178313
    num_examples: 200
  - name: train
    num_bytes: 1781176
    num_examples: 2000
  download_size: 15719851
  dataset_size: 1959489
- config_name: shuffled-10k-qa12
  features:
  - name: story
    sequence:
    - name: id
      dtype: string
    - name: type
      dtype:
        class_label:
          names:
            0: context
            1: question
    - name: text
      dtype: string
    - name: supporting_ids
      sequence: string
    - name: answer
      dtype: string
  splits:
  - name: test
    num_bytes: 185529
    num_examples: 200
  - name: train
    num_bytes: 1854745
    num_examples: 2000
  download_size: 15719851
  dataset_size: 2040274
- config_name: shuffled-10k-qa13
  features:
  - name: story
    sequence:
    - name: id
      dtype: string
    - name: type
      dtype:
        class_label:
          names:
            0: context
            1: question
    - name: text
      dtype: string
    - name: supporting_ids
      sequence: string
    - name: answer
      dtype: string
  splits:
  - name: test
    num_bytes: 190484
    num_examples: 200
  - name: train
    num_bytes: 1903149
    num_examples: 2000
  download_size: 15719851
  dataset_size: 2093633
- config_name: shuffled-10k-qa14
  features:
  - name: story
    sequence:
    - name: id
      dtype: string
    - name: type
      dtype:
        class_label:
          names:
            0: context
            1: question
    - name: text
      dtype: string
    - name: supporting_ids
      sequence: string
    - name: answer
      dtype: string
  splits:
  - name: test
    num_bytes: 233204
    num_examples: 200
  - name: train
    num_bytes: 2321511
    num_examples: 2000
  download_size: 15719851
  dataset_size: 2554715
- config_name: shuffled-10k-qa15
  features:
  - name: story
    sequence:
    - name: id
      dtype: string
    - name: type
      dtype:
        class_label:
          names:
            0: context
            1: question
    - name: text
      dtype: string
    - name: supporting_ids
      sequence: string
    - name: answer
      dtype: string
  splits:
  - name: test
    num_bytes: 163809
    num_examples: 250
  - name: train
    num_bytes: 1637398
    num_examples: 2500
  download_size: 15719851
  dataset_size: 1801207
- config_name: shuffled-10k-qa16
  features:
  - name: story
    sequence:
    - name: id
      dtype: string
    - name: type
      dtype:
        class_label:
          names:
            0: context
            1: question
    - name: text
      dtype: string
    - name: supporting_ids
      sequence: string
    - name: answer
      dtype: string
  splits:
  - name: test
    num_bytes: 456248
    num_examples: 1000
  - name: train
    num_bytes: 4562844
    num_examples: 10000
  download_size: 15719851
  dataset_size: 5019092
- config_name: shuffled-10k-qa17
  features:
  - name: story
    sequence:
    - name: id
      dtype: string
    - name: type
      dtype:
        class_label:
          names:
            0: context
            1: question
    - name: text
      dtype: string
    - name: supporting_ids
      sequence: string
    - name: answer
      dtype: string
  splits:
  - name: test
    num_bytes: 103618
    num_examples: 125
  - name: train
    num_bytes: 1034333
    num_examples: 1250
  download_size: 15719851
  dataset_size: 1137951
- config_name: shuffled-10k-qa18
  features:
  - name: story
    sequence:
    - name: id
      dtype: string
    - name: type
      dtype:
        class_label:
          names:
            0: context
            1: question
    - name: text
      dtype: string
    - name: supporting_ids
      sequence: string
    - name: answer
      dtype: string
  splits:
  - name: test
    num_bytes: 161266
    num_examples: 199
  - name: train
    num_bytes: 1641650
    num_examples: 1978
  download_size: 15719851
  dataset_size: 1802916
- config_name: shuffled-10k-qa19
  features:
  - name: story
    sequence:
    - name: id
      dtype: string
    - name: type
      dtype:
        class_label:
          names:
            0: context
            1: question
    - name: text
      dtype: string
    - name: supporting_ids
      sequence: string
    - name: answer
      dtype: string
  splits:
  - name: test
    num_bytes: 404489
    num_examples: 1000
  - name: train
    num_bytes: 4045086
    num_examples: 10000
  download_size: 15719851
  dataset_size: 4449575
- config_name: shuffled-10k-qa20
  features:
  - name: story
    sequence:
    - name: id
      dtype: string
    - name: type
      dtype:
        class_label:
          names:
            0: context
            1: question
    - name: text
      dtype: string
    - name: supporting_ids
      sequence: string
    - name: answer
      dtype: string
  splits:
  - name: test
    num_bytes: 115863
    num_examples: 93
  - name: train
    num_bytes: 1157351
    num_examples: 933
  download_size: 15719851
  dataset_size: 1273214
---


# Dataset Card for bAbi QA

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

- **Homepage:**[The bAbI project](https://research.fb.com/downloads/babi/)
- **Repository:**
- **Paper:** [arXiv Paper](https://arxiv.org/pdf/1502.05698.pdf)
- **Leaderboard:**
- **Point of Contact:** 
### Dataset Summary

The (20) QA bAbI tasks are a set of proxy tasks that evaluate reading comprehension via question answering. Our tasks measure understanding in several ways: whether a system is able to answer questions via chaining facts, simple induction, deduction and many more. The tasks are designed to be prerequisites for any system that aims to be capable of conversing with a human. The aim is to classify these tasks into skill sets,so that researchers can identify (and then rectify) the failings of their systems.

### Supported Tasks and Leaderboards

The dataset supports a set of 20 proxy story-based question answering tasks for various "types" in English and Hindi. The tasks are:

|task_no|task_name|
|----|------------|
|qa1 |single-supporting-fact|
|qa2 |two-supporting-facts|
|qa3 |three-supporting-facts|
|qa4 |two-arg-relations|
|qa5 |three-arg-relations|
|qa6 |yes-no-questions|
|qa7 |counting|
|qa8 |lists-sets|
|qa9 |simple-negation|
|qa10| indefinite-knowledge|
|qa11| basic-coreference|
|qa12| conjunction|
|qa13| compound-coreference|
|qa14| time-reasoning|
|qa15| basic-deduction|
|qa16| basic-induction|
|qa17| positional-reasoning|
|qa18| size-reasoning|
|qa19| path-finding|
|qa20| agents-motivations|


The "types" are are:

- `en`
   - the tasks in English, readable by humans.

- `hn`
   - the tasks in Hindi, readable by humans.
- `shuffled` 
   - the same tasks with shuffled letters so they are not readable by humans, and for existing parsers and taggers cannot be used in a straight-forward fashion to leverage extra resources-- in this case the learner is more forced to rely on the given training data. This mimics a learner being first presented a language and having to learn from scratch.
- `en-10k`, `shuffled-10k` and `hn-10k`  
   - the same tasks in the three formats, but with 10,000 training examples, rather than 1000 training examples.
- `en-valid` and `en-valid-10k`
   - are the same as `en` and `en10k` except the train sets have been conveniently split into train and valid portions (90% and 10% split).

To get a particular dataset, use `load_dataset('babi_qa',type=f'{type}',task_no=f'{task_no}')` where `type` is one of the types, and `task_no` is one of the task numbers. For example, `load_dataset('babi_qa', type='en', task_no='qa1')`.
### Languages



## Dataset Structure

### Data Instances
An instance from the `en-qa1` config's `train` split:

```
{'story': {'answer': ['', '', 'bathroom', '', '', 'hallway', '', '', 'hallway', '', '', 'office', '', '', 'bathroom'], 'id': ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15'], 'supporting_ids': [[], [], ['1'], [], [], ['4'], [], [], ['4'], [], [], ['11'], [], [], ['8']], 'text': ['Mary moved to the bathroom.', 'John went to the hallway.', 'Where is Mary?', 'Daniel went back to the hallway.', 'Sandra moved to the garden.', 'Where is Daniel?', 'John moved to the office.', 'Sandra journeyed to the bathroom.', 'Where is Daniel?', 'Mary moved to the hallway.', 'Daniel travelled to the office.', 'Where is Daniel?', 'John went back to the garden.', 'John moved to the bedroom.', 'Where is Sandra?'], 'type': [0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1]}}
```

### Data Fields

- `story`: a dictionary feature containing:
  - `id`: a `string` feature, which denotes the line number in the example.
  - `type`: a classification label, with possible values including `context`, `question`, denoting whether the text is context or a question.
  - `text`: a `string` feature the text present, whether it is a question or context.
  - `supporting_ids`: a `list` of `string` features containing the line numbers of the lines in the example which support the answer.
  - `answer`: a `string` feature containing the answer to the question, or an empty string if the `type`s is not `question`.

### Data Splits

The splits and corresponding sizes are:

|                   |   train |   test |   validation |
|-------------------|---------|--------|--------------|
| en-qa1            |     200 |    200 |          -   |
| en-qa2            |     200 |    200 |          -   |
| en-qa3            |     200 |    200 |          -   |
| en-qa4            |    1000 |   1000 |          -   |
| en-qa5            |     200 |    200 |          -   |
| en-qa6            |     200 |    200 |          -   |
| en-qa7            |     200 |    200 |          -   |
| en-qa8            |     200 |    200 |          -   |
| en-qa9            |     200 |    200 |          -   |
| en-qa10           |     200 |    200 |          -   |
| en-qa11           |     200 |    200 |          -   |
| en-qa12           |     200 |    200 |          -   |
| en-qa13           |     200 |    200 |          -   |
| en-qa14           |     200 |    200 |          -   |
| en-qa15           |     250 |    250 |          -   |
| en-qa16           |    1000 |   1000 |          -   |
| en-qa17           |     125 |    125 |          -   |
| en-qa18           |     198 |    199 |          -   |
| en-qa19           |    1000 |   1000 |          -   |
| en-qa20           |      94 |     93 |          -   |
| en-10k-qa1        |    2000 |    200 |          -   |
| en-10k-qa2        |    2000 |    200 |          -   |
| en-10k-qa3        |    2000 |    200 |          -   |
| en-10k-qa4        |   10000 |   1000 |          -   |
| en-10k-qa5        |    2000 |    200 |          -   |
| en-10k-qa6        |    2000 |    200 |          -   |
| en-10k-qa7        |    2000 |    200 |          -   |
| en-10k-qa8        |    2000 |    200 |          -   |
| en-10k-qa9        |    2000 |    200 |          -   |
| en-10k-qa10       |    2000 |    200 |          -   |
| en-10k-qa11       |    2000 |    200 |          -   |
| en-10k-qa12       |    2000 |    200 |          -   |
| en-10k-qa13       |    2000 |    200 |          -   |
| en-10k-qa14       |    2000 |    200 |          -   |
| en-10k-qa15       |    2500 |    250 |          -   |
| en-10k-qa16       |   10000 |   1000 |          -   |
| en-10k-qa17       |    1250 |    125 |          -   |
| en-10k-qa18       |    1978 |    199 |          -   |
| en-10k-qa19       |   10000 |   1000 |          -   |
| en-10k-qa20       |     933 |     93 |          -   |
| en-valid-qa1      |     180 |    200 |           20 |
| en-valid-qa2      |     180 |    200 |           20 |
| en-valid-qa3      |     180 |    200 |           20 |
| en-valid-qa4      |     900 |   1000 |          100 |
| en-valid-qa5      |     180 |    200 |           20 |
| en-valid-qa6      |     180 |    200 |           20 |
| en-valid-qa7      |     180 |    200 |           20 |
| en-valid-qa8      |     180 |    200 |           20 |
| en-valid-qa9      |     180 |    200 |           20 |
| en-valid-qa10     |     180 |    200 |           20 |
| en-valid-qa11     |     180 |    200 |           20 |
| en-valid-qa12     |     180 |    200 |           20 |
| en-valid-qa13     |     180 |    200 |           20 |
| en-valid-qa14     |     180 |    200 |           20 |
| en-valid-qa15     |     225 |    250 |           25 |
| en-valid-qa16     |     900 |   1000 |          100 |
| en-valid-qa17     |     113 |    125 |           12 |
| en-valid-qa18     |     179 |    199 |           19 |
| en-valid-qa19     |     900 |   1000 |          100 |
| en-valid-qa20     |      85 |     93 |            9 |
| en-valid-10k-qa1  |    1800 |    200 |          200 |
| en-valid-10k-qa2  |    1800 |    200 |          200 |
| en-valid-10k-qa3  |    1800 |    200 |          200 |
| en-valid-10k-qa4  |    9000 |   1000 |         1000 |
| en-valid-10k-qa5  |    1800 |    200 |          200 |
| en-valid-10k-qa6  |    1800 |    200 |          200 |
| en-valid-10k-qa7  |    1800 |    200 |          200 |
| en-valid-10k-qa8  |    1800 |    200 |          200 |
| en-valid-10k-qa9  |    1800 |    200 |          200 |
| en-valid-10k-qa10 |    1800 |    200 |          200 |
| en-valid-10k-qa11 |    1800 |    200 |          200 |
| en-valid-10k-qa12 |    1800 |    200 |          200 |
| en-valid-10k-qa13 |    1800 |    200 |          200 |
| en-valid-10k-qa14 |    1800 |    200 |          200 |
| en-valid-10k-qa15 |    2250 |    250 |          250 |
| en-valid-10k-qa16 |    9000 |   1000 |         1000 |
| en-valid-10k-qa17 |    1125 |    125 |          125 |
| en-valid-10k-qa18 |    1781 |    199 |          197 |
| en-valid-10k-qa19 |    9000 |   1000 |         1000 |
| en-valid-10k-qa20 |     840 |     93 |           93 |
| hn-qa1            |     200 |    200 |          -   |
| hn-qa2            |     200 |    200 |          -   |
| hn-qa3            |     167 |    167 |          -   |
| hn-qa4            |    1000 |   1000 |          -   |
| hn-qa5            |     200 |    200 |          -   |
| hn-qa6            |     200 |    200 |          -   |
| hn-qa7            |     200 |    200 |          -   |
| hn-qa8            |     200 |    200 |          -   |
| hn-qa9            |     200 |    200 |          -   |
| hn-qa10           |     200 |    200 |          -   |
| hn-qa11           |     200 |    200 |          -   |
| hn-qa12           |     200 |    200 |          -   |
| hn-qa13           |     125 |    125 |          -   |
| hn-qa14           |     200 |    200 |          -   |
| hn-qa15           |     250 |    250 |          -   |
| hn-qa16           |    1000 |   1000 |          -   |
| hn-qa17           |     125 |    125 |          -   |
| hn-qa18           |     198 |    198 |          -   |
| hn-qa19           |    1000 |   1000 |          -   |
| hn-qa20           |      93 |     94 |          -   |
| hn-10k-qa1        |    2000 |    200 |          -   |
| hn-10k-qa2        |    2000 |    200 |          -   |
| hn-10k-qa3        |    1667 |    167 |          -   |
| hn-10k-qa4        |   10000 |   1000 |          -   |
| hn-10k-qa5        |    2000 |    200 |          -   |
| hn-10k-qa6        |    2000 |    200 |          -   |
| hn-10k-qa7        |    2000 |    200 |          -   |
| hn-10k-qa8        |    2000 |    200 |          -   |
| hn-10k-qa9        |    2000 |    200 |          -   |
| hn-10k-qa10       |    2000 |    200 |          -   |
| hn-10k-qa11       |    2000 |    200 |          -   |
| hn-10k-qa12       |    2000 |    200 |          -   |
| hn-10k-qa13       |    1250 |    125 |          -   |
| hn-10k-qa14       |    2000 |    200 |          -   |
| hn-10k-qa15       |    2500 |    250 |          -   |
| hn-10k-qa16       |   10000 |   1000 |          -   |
| hn-10k-qa17       |    1250 |    125 |          -   |
| hn-10k-qa18       |    1977 |    198 |          -   |
| hn-10k-qa19       |   10000 |   1000 |          -   |
| hn-10k-qa20       |     934 |     94 |          -   |
| shuffled-qa1      |     200 |    200 |          -   |
| shuffled-qa2      |     200 |    200 |          -   |
| shuffled-qa3      |     200 |    200 |          -   |
| shuffled-qa4      |    1000 |   1000 |          -   |
| shuffled-qa5      |     200 |    200 |          -   |
| shuffled-qa6      |     200 |    200 |          -   |
| shuffled-qa7      |     200 |    200 |          -   |
| shuffled-qa8      |     200 |    200 |          -   |
| shuffled-qa9      |     200 |    200 |          -   |
| shuffled-qa10     |     200 |    200 |          -   |
| shuffled-qa11     |     200 |    200 |          -   |
| shuffled-qa12     |     200 |    200 |          -   |
| shuffled-qa13     |     200 |    200 |          -   |
| shuffled-qa14     |     200 |    200 |          -   |
| shuffled-qa15     |     250 |    250 |          -   |
| shuffled-qa16     |    1000 |   1000 |          -   |
| shuffled-qa17     |     125 |    125 |          -   |
| shuffled-qa18     |     198 |    199 |          -   |
| shuffled-qa19     |    1000 |   1000 |          -   |
| shuffled-qa20     |      94 |     93 |          -   |
| shuffled-10k-qa1  |    2000 |    200 |          -   |
| shuffled-10k-qa2  |    2000 |    200 |          -   |
| shuffled-10k-qa3  |    2000 |    200 |          -   |
| shuffled-10k-qa4  |   10000 |   1000 |          -   |
| shuffled-10k-qa5  |    2000 |    200 |          -   |
| shuffled-10k-qa6  |    2000 |    200 |          -   |
| shuffled-10k-qa7  |    2000 |    200 |          -   |
| shuffled-10k-qa8  |    2000 |    200 |          -   |
| shuffled-10k-qa9  |    2000 |    200 |          -   |
| shuffled-10k-qa10 |    2000 |    200 |          -   |
| shuffled-10k-qa11 |    2000 |    200 |          -   |
| shuffled-10k-qa12 |    2000 |    200 |          -   |
| shuffled-10k-qa13 |    2000 |    200 |          -   |
| shuffled-10k-qa14 |    2000 |    200 |          -   |
| shuffled-10k-qa15 |    2500 |    250 |          -   |
| shuffled-10k-qa16 |   10000 |   1000 |          -   |
| shuffled-10k-qa17 |    1250 |    125 |          -   |
| shuffled-10k-qa18 |    1978 |    199 |          -   |
| shuffled-10k-qa19 |   10000 |   1000 |          -   |
| shuffled-10k-qa20 |     933 |     93 |          -   |


## Dataset Creation

### Curation Rationale

[More Information Needed]

### Source Data

#### Initial Data Collection and Normalization

Code to generate tasks is available on [github](https://github.com/facebook/bAbI-tasks)

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

Jesse Dodge and Andreea Gane and Xiang Zhang and Antoine Bordes and Sumit Chopra and Alexander Miller and Arthur Szlam and Jason Weston, at Facebook Research.

### Licensing Information

```
Creative Commons Attribution 3.0 License
```

### Citation Information

```
@misc{dodge2016evaluating,
      title={Evaluating Prerequisite Qualities for Learning End-to-End Dialog Systems}, 
      author={Jesse Dodge and Andreea Gane and Xiang Zhang and Antoine Bordes and Sumit Chopra and Alexander Miller and Arthur Szlam and Jason Weston},
      year={2016},
      eprint={1511.06931},
      archivePrefix={arXiv},
      primaryClass={cs.CL}
}
```


### Contributions

Thanks to [@gchhablani](https://github.com/gchhablani) for adding this dataset.