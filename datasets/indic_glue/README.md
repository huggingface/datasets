---
annotations_creators:
- other
language:
- as
- bn
- en
- gu
- hi
- kn
- ml
- mr
- or
- pa
- ta
- te
language_creators:
- found
license:
- other
multilinguality:
- multilingual
pretty_name: IndicGLUE
size_categories:
- 100K<n<1M
source_datasets:
- extended|other
task_categories:
- text-classification
- token-classification
- multiple-choice
task_ids:
- topic-classification
- natural-language-inference
- sentiment-analysis
- semantic-similarity-scoring
- text-classification-other-headline-classification
- text-classification-other-paraphrase-identification
- text-classification-other-cross-lingual-similarity
- text-classification-other-discourse-mode-classification
- named-entity-recognition
- multiple-choice-qa
paperswithcode_id: null
dataset_info:
- config_name: wnli.en
  features:
  - name: hypothesis
    dtype: string
  - name: premise
    dtype: string
  - name: label
    dtype:
      class_label:
        names:
          0: not_entailment
          1: entailment
          2: None
  splits:
  - name: test
    num_bytes: 37305
    num_examples: 146
  - name: train
    num_bytes: 104577
    num_examples: 635
  - name: validation
    num_bytes: 11886
    num_examples: 71
  download_size: 591249
  dataset_size: 153768
- config_name: wnli.hi
  features:
  - name: hypothesis
    dtype: string
  - name: premise
    dtype: string
  - name: label
    dtype:
      class_label:
        names:
          0: not_entailment
          1: entailment
          2: None
  splits:
  - name: test
    num_bytes: 90831
    num_examples: 146
  - name: train
    num_bytes: 253342
    num_examples: 635
  - name: validation
    num_bytes: 28684
    num_examples: 71
  download_size: 591249
  dataset_size: 372857
- config_name: wnli.gu
  features:
  - name: hypothesis
    dtype: string
  - name: premise
    dtype: string
  - name: label
    dtype:
      class_label:
        names:
          0: not_entailment
          1: entailment
          2: None
  splits:
  - name: test
    num_bytes: 94586
    num_examples: 146
  - name: train
    num_bytes: 251562
    num_examples: 635
  - name: validation
    num_bytes: 28183
    num_examples: 71
  download_size: 591249
  dataset_size: 374331
- config_name: wnli.mr
  features:
  - name: hypothesis
    dtype: string
  - name: premise
    dtype: string
  - name: label
    dtype:
      class_label:
        names:
          0: not_entailment
          1: entailment
          2: None
  splits:
  - name: test
    num_bytes: 97136
    num_examples: 146
  - name: train
    num_bytes: 256657
    num_examples: 635
  - name: validation
    num_bytes: 29226
    num_examples: 71
  download_size: 591249
  dataset_size: 383019
- config_name: copa.en
  features:
  - name: premise
    dtype: string
  - name: choice1
    dtype: string
  - name: choice2
    dtype: string
  - name: question
    dtype: string
  - name: label
    dtype: int32
  splits:
  - name: test
    num_bytes: 55862
    num_examples: 500
  - name: train
    num_bytes: 46049
    num_examples: 400
  - name: validation
    num_bytes: 11695
    num_examples: 100
  download_size: 757679
  dataset_size: 113606
- config_name: copa.hi
  features:
  - name: premise
    dtype: string
  - name: choice1
    dtype: string
  - name: choice2
    dtype: string
  - name: question
    dtype: string
  - name: label
    dtype: int32
  splits:
  - name: test
    num_bytes: 112846
    num_examples: 449
  - name: train
    num_bytes: 93392
    num_examples: 362
  - name: validation
    num_bytes: 23575
    num_examples: 88
  download_size: 757679
  dataset_size: 229813
- config_name: copa.gu
  features:
  - name: premise
    dtype: string
  - name: choice1
    dtype: string
  - name: choice2
    dtype: string
  - name: question
    dtype: string
  - name: label
    dtype: int32
  splits:
  - name: test
    num_bytes: 110013
    num_examples: 448
  - name: train
    num_bytes: 92113
    num_examples: 362
  - name: validation
    num_bytes: 23466
    num_examples: 88
  download_size: 757679
  dataset_size: 225592
- config_name: copa.mr
  features:
  - name: premise
    dtype: string
  - name: choice1
    dtype: string
  - name: choice2
    dtype: string
  - name: question
    dtype: string
  - name: label
    dtype: int32
  splits:
  - name: test
    num_bytes: 112071
    num_examples: 449
  - name: train
    num_bytes: 93457
    num_examples: 362
  - name: validation
    num_bytes: 23890
    num_examples: 88
  download_size: 757679
  dataset_size: 229418
- config_name: sna.bn
  features:
  - name: text
    dtype: string
  - name: label
    dtype:
      class_label:
        names:
          0: kolkata
          1: state
          2: national
          3: sports
          4: entertainment
          5: international
  splits:
  - name: test
    num_bytes: 5799983
    num_examples: 1411
  - name: train
    num_bytes: 46070054
    num_examples: 11284
  - name: validation
    num_bytes: 5648130
    num_examples: 1411
  download_size: 11803096
  dataset_size: 57518167
- config_name: csqa.as
  features:
  - name: question
    dtype: string
  - name: answer
    dtype: string
  - name: category
    dtype: string
  - name: title
    dtype: string
  - name: options
    sequence: string
  - name: out_of_context_options
    sequence: string
  splits:
  - name: test
    num_bytes: 3800555
    num_examples: 2942
  download_size: 65099316
  dataset_size: 3800555
- config_name: csqa.bn
  features:
  - name: question
    dtype: string
  - name: answer
    dtype: string
  - name: category
    dtype: string
  - name: title
    dtype: string
  - name: options
    sequence: string
  - name: out_of_context_options
    sequence: string
  splits:
  - name: test
    num_bytes: 54671146
    num_examples: 38845
  download_size: 65099316
  dataset_size: 54671146
- config_name: csqa.gu
  features:
  - name: question
    dtype: string
  - name: answer
    dtype: string
  - name: category
    dtype: string
  - name: title
    dtype: string
  - name: options
    sequence: string
  - name: out_of_context_options
    sequence: string
  splits:
  - name: test
    num_bytes: 29131703
    num_examples: 22861
  download_size: 65099316
  dataset_size: 29131703
- config_name: csqa.hi
  features:
  - name: question
    dtype: string
  - name: answer
    dtype: string
  - name: category
    dtype: string
  - name: title
    dtype: string
  - name: options
    sequence: string
  - name: out_of_context_options
    sequence: string
  splits:
  - name: test
    num_bytes: 40409475
    num_examples: 35140
  download_size: 65099316
  dataset_size: 40409475
- config_name: csqa.kn
  features:
  - name: question
    dtype: string
  - name: answer
    dtype: string
  - name: category
    dtype: string
  - name: title
    dtype: string
  - name: options
    sequence: string
  - name: out_of_context_options
    sequence: string
  splits:
  - name: test
    num_bytes: 21199880
    num_examples: 13666
  download_size: 65099316
  dataset_size: 21199880
- config_name: csqa.ml
  features:
  - name: question
    dtype: string
  - name: answer
    dtype: string
  - name: category
    dtype: string
  - name: title
    dtype: string
  - name: options
    sequence: string
  - name: out_of_context_options
    sequence: string
  splits:
  - name: test
    num_bytes: 47220932
    num_examples: 26537
  download_size: 65099316
  dataset_size: 47220932
- config_name: csqa.mr
  features:
  - name: question
    dtype: string
  - name: answer
    dtype: string
  - name: category
    dtype: string
  - name: title
    dtype: string
  - name: options
    sequence: string
  - name: out_of_context_options
    sequence: string
  splits:
  - name: test
    num_bytes: 13667238
    num_examples: 11370
  download_size: 65099316
  dataset_size: 13667238
- config_name: csqa.or
  features:
  - name: question
    dtype: string
  - name: answer
    dtype: string
  - name: category
    dtype: string
  - name: title
    dtype: string
  - name: options
    sequence: string
  - name: out_of_context_options
    sequence: string
  splits:
  - name: test
    num_bytes: 2562397
    num_examples: 1975
  download_size: 65099316
  dataset_size: 2562397
- config_name: csqa.pa
  features:
  - name: question
    dtype: string
  - name: answer
    dtype: string
  - name: category
    dtype: string
  - name: title
    dtype: string
  - name: options
    sequence: string
  - name: out_of_context_options
    sequence: string
  splits:
  - name: test
    num_bytes: 5806129
    num_examples: 5667
  download_size: 65099316
  dataset_size: 5806129
- config_name: csqa.ta
  features:
  - name: question
    dtype: string
  - name: answer
    dtype: string
  - name: category
    dtype: string
  - name: title
    dtype: string
  - name: options
    sequence: string
  - name: out_of_context_options
    sequence: string
  splits:
  - name: test
    num_bytes: 61868609
    num_examples: 38590
  download_size: 65099316
  dataset_size: 61868609
- config_name: csqa.te
  features:
  - name: question
    dtype: string
  - name: answer
    dtype: string
  - name: category
    dtype: string
  - name: title
    dtype: string
  - name: options
    sequence: string
  - name: out_of_context_options
    sequence: string
  splits:
  - name: test
    num_bytes: 58785157
    num_examples: 41338
  download_size: 65099316
  dataset_size: 58785157
- config_name: wstp.as
  features:
  - name: sectionText
    dtype: string
  - name: correctTitle
    dtype: string
  - name: titleA
    dtype: string
  - name: titleB
    dtype: string
  - name: titleC
    dtype: string
  - name: titleD
    dtype: string
  - name: url
    dtype: string
  splits:
  - name: test
    num_bytes: 1697678
    num_examples: 626
  - name: train
    num_bytes: 13581364
    num_examples: 5000
  - name: validation
    num_bytes: 1698996
    num_examples: 625
  download_size: 242008091
  dataset_size: 16978038
- config_name: wstp.bn
  features:
  - name: sectionText
    dtype: string
  - name: correctTitle
    dtype: string
  - name: titleA
    dtype: string
  - name: titleB
    dtype: string
  - name: titleC
    dtype: string
  - name: titleD
    dtype: string
  - name: url
    dtype: string
  splits:
  - name: test
    num_bytes: 17633893
    num_examples: 5948
  - name: train
    num_bytes: 143340597
    num_examples: 47580
  - name: validation
    num_bytes: 17759264
    num_examples: 5947
  download_size: 242008091
  dataset_size: 178733754
- config_name: wstp.gu
  features:
  - name: sectionText
    dtype: string
  - name: correctTitle
    dtype: string
  - name: titleA
    dtype: string
  - name: titleB
    dtype: string
  - name: titleC
    dtype: string
  - name: titleD
    dtype: string
  - name: url
    dtype: string
  splits:
  - name: test
    num_bytes: 4699186
    num_examples: 1251
  - name: train
    num_bytes: 39353520
    num_examples: 10004
  - name: validation
    num_bytes: 4887780
    num_examples: 1251
  download_size: 242008091
  dataset_size: 48940486
- config_name: wstp.hi
  features:
  - name: sectionText
    dtype: string
  - name: correctTitle
    dtype: string
  - name: titleA
    dtype: string
  - name: titleB
    dtype: string
  - name: titleC
    dtype: string
  - name: titleD
    dtype: string
  - name: url
    dtype: string
  splits:
  - name: test
    num_bytes: 19593029
    num_examples: 5509
  - name: train
    num_bytes: 158529718
    num_examples: 44069
  - name: validation
    num_bytes: 19371932
    num_examples: 5509
  download_size: 242008091
  dataset_size: 197494679
- config_name: wstp.kn
  features:
  - name: sectionText
    dtype: string
  - name: correctTitle
    dtype: string
  - name: titleA
    dtype: string
  - name: titleB
    dtype: string
  - name: titleC
    dtype: string
  - name: titleD
    dtype: string
  - name: url
    dtype: string
  splits:
  - name: test
    num_bytes: 17897059
    num_examples: 4423
  - name: train
    num_bytes: 139950425
    num_examples: 35379
  - name: validation
    num_bytes: 17789810
    num_examples: 4422
  download_size: 242008091
  dataset_size: 175637294
- config_name: wstp.ml
  features:
  - name: sectionText
    dtype: string
  - name: correctTitle
    dtype: string
  - name: titleA
    dtype: string
  - name: titleB
    dtype: string
  - name: titleC
    dtype: string
  - name: titleD
    dtype: string
  - name: url
    dtype: string
  splits:
  - name: test
    num_bytes: 11150942
    num_examples: 3441
  - name: train
    num_bytes: 88360588
    num_examples: 27527
  - name: validation
    num_bytes: 11193368
    num_examples: 3441
  download_size: 242008091
  dataset_size: 110704898
- config_name: wstp.mr
  features:
  - name: sectionText
    dtype: string
  - name: correctTitle
    dtype: string
  - name: titleA
    dtype: string
  - name: titleB
    dtype: string
  - name: titleC
    dtype: string
  - name: titleD
    dtype: string
  - name: url
    dtype: string
  splits:
  - name: test
    num_bytes: 3631712
    num_examples: 1306
  - name: train
    num_bytes: 28302397
    num_examples: 10446
  - name: validation
    num_bytes: 3328826
    num_examples: 1306
  download_size: 242008091
  dataset_size: 35262935
- config_name: wstp.or
  features:
  - name: sectionText
    dtype: string
  - name: correctTitle
    dtype: string
  - name: titleA
    dtype: string
  - name: titleB
    dtype: string
  - name: titleC
    dtype: string
  - name: titleD
    dtype: string
  - name: url
    dtype: string
  splits:
  - name: test
    num_bytes: 1344680
    num_examples: 502
  - name: train
    num_bytes: 10900034
    num_examples: 4015
  - name: validation
    num_bytes: 1264963
    num_examples: 502
  download_size: 242008091
  dataset_size: 13509677
- config_name: wstp.pa
  features:
  - name: sectionText
    dtype: string
  - name: correctTitle
    dtype: string
  - name: titleA
    dtype: string
  - name: titleB
    dtype: string
  - name: titleC
    dtype: string
  - name: titleD
    dtype: string
  - name: url
    dtype: string
  splits:
  - name: test
    num_bytes: 2685795
    num_examples: 1097
  - name: train
    num_bytes: 22189758
    num_examples: 8772
  - name: validation
    num_bytes: 2789214
    num_examples: 1097
  download_size: 242008091
  dataset_size: 27664767
- config_name: wstp.ta
  features:
  - name: sectionText
    dtype: string
  - name: correctTitle
    dtype: string
  - name: titleA
    dtype: string
  - name: titleB
    dtype: string
  - name: titleC
    dtype: string
  - name: titleD
    dtype: string
  - name: url
    dtype: string
  splits:
  - name: test
    num_bytes: 18815099
    num_examples: 6118
  - name: train
    num_bytes: 151929358
    num_examples: 48940
  - name: validation
    num_bytes: 18817195
    num_examples: 6117
  download_size: 242008091
  dataset_size: 189561652
- config_name: wstp.te
  features:
  - name: sectionText
    dtype: string
  - name: correctTitle
    dtype: string
  - name: titleA
    dtype: string
  - name: titleB
    dtype: string
  - name: titleC
    dtype: string
  - name: titleD
    dtype: string
  - name: url
    dtype: string
  splits:
  - name: test
    num_bytes: 18991941
    num_examples: 10000
  - name: train
    num_bytes: 151696915
    num_examples: 80000
  - name: validation
    num_bytes: 19003197
    num_examples: 10000
  download_size: 242008091
  dataset_size: 189692053
- config_name: inltkh.gu
  features:
  - name: text
    dtype: string
  - name: label
    dtype:
      class_label:
        names:
          0: entertainment
          1: business
          2: tech
          3: sports
          4: state
          5: spirituality
          6: tamil-cinema
          7: positive
          8: negative
          9: neutral
  splits:
  - name: test
    num_bytes: 110761
    num_examples: 659
  - name: train
    num_bytes: 883067
    num_examples: 5269
  - name: validation
    num_bytes: 111205
    num_examples: 659
  download_size: 2054771
  dataset_size: 1105033
- config_name: inltkh.ml
  features:
  - name: text
    dtype: string
  - name: label
    dtype:
      class_label:
        names:
          0: entertainment
          1: business
          2: tech
          3: sports
          4: state
          5: spirituality
          6: tamil-cinema
          7: positive
          8: negative
          9: neutral
  splits:
  - name: test
    num_bytes: 138851
    num_examples: 630
  - name: train
    num_bytes: 1108149
    num_examples: 5036
  - name: validation
    num_bytes: 140059
    num_examples: 630
  download_size: 2054771
  dataset_size: 1387059
- config_name: inltkh.mr
  features:
  - name: text
    dtype: string
  - name: label
    dtype:
      class_label:
        names:
          0: entertainment
          1: business
          2: tech
          3: sports
          4: state
          5: spirituality
          6: tamil-cinema
          7: positive
          8: negative
          9: neutral
  splits:
  - name: test
    num_bytes: 180562
    num_examples: 1210
  - name: train
    num_bytes: 1462618
    num_examples: 9672
  - name: validation
    num_bytes: 180310
    num_examples: 1210
  download_size: 2054771
  dataset_size: 1823490
- config_name: inltkh.ta
  features:
  - name: text
    dtype: string
  - name: label
    dtype:
      class_label:
        names:
          0: entertainment
          1: business
          2: tech
          3: sports
          4: state
          5: spirituality
          6: tamil-cinema
          7: positive
          8: negative
          9: neutral
  splits:
  - name: test
    num_bytes: 320469
    num_examples: 669
  - name: train
    num_bytes: 2659573
    num_examples: 5346
  - name: validation
    num_bytes: 316087
    num_examples: 669
  download_size: 2054771
  dataset_size: 3296129
- config_name: inltkh.te
  features:
  - name: text
    dtype: string
  - name: label
    dtype:
      class_label:
        names:
          0: entertainment
          1: business
          2: tech
          3: sports
          4: state
          5: spirituality
          6: tamil-cinema
          7: positive
          8: negative
          9: neutral
  splits:
  - name: test
    num_bytes: 173153
    num_examples: 541
  - name: train
    num_bytes: 1361671
    num_examples: 4328
  - name: validation
    num_bytes: 170475
    num_examples: 541
  download_size: 2054771
  dataset_size: 1705299
- config_name: bbca.hi
  features:
  - name: label
    dtype: string
  - name: text
    dtype: string
  splits:
  - name: test
    num_bytes: 5501156
    num_examples: 866
  - name: train
    num_bytes: 22126213
    num_examples: 3467
  download_size: 5770136
  dataset_size: 27627369
- config_name: cvit-mkb-clsr.en-bn
  features:
  - name: sentence1
    dtype: string
  - name: sentence2
    dtype: string
  splits:
  - name: test
    num_bytes: 2002009
    num_examples: 5522
  download_size: 3702442
  dataset_size: 2002009
- config_name: cvit-mkb-clsr.en-gu
  features:
  - name: sentence1
    dtype: string
  - name: sentence2
    dtype: string
  splits:
  - name: test
    num_bytes: 2316311
    num_examples: 6463
  download_size: 3702442
  dataset_size: 2316311
- config_name: cvit-mkb-clsr.en-hi
  features:
  - name: sentence1
    dtype: string
  - name: sentence2
    dtype: string
  splits:
  - name: test
    num_bytes: 1866335
    num_examples: 5169
  download_size: 3702442
  dataset_size: 1866335
- config_name: cvit-mkb-clsr.en-ml
  features:
  - name: sentence1
    dtype: string
  - name: sentence2
    dtype: string
  splits:
  - name: test
    num_bytes: 1999869
    num_examples: 4886
  download_size: 3702442
  dataset_size: 1999869
- config_name: cvit-mkb-clsr.en-mr
  features:
  - name: sentence1
    dtype: string
  - name: sentence2
    dtype: string
  splits:
  - name: test
    num_bytes: 2142129
    num_examples: 5760
  download_size: 3702442
  dataset_size: 2142129
- config_name: cvit-mkb-clsr.en-or
  features:
  - name: sentence1
    dtype: string
  - name: sentence2
    dtype: string
  splits:
  - name: test
    num_bytes: 276385
    num_examples: 752
  download_size: 3702442
  dataset_size: 276385
- config_name: cvit-mkb-clsr.en-ta
  features:
  - name: sentence1
    dtype: string
  - name: sentence2
    dtype: string
  splits:
  - name: test
    num_bytes: 2576460
    num_examples: 5637
  download_size: 3702442
  dataset_size: 2576460
- config_name: cvit-mkb-clsr.en-te
  features:
  - name: sentence1
    dtype: string
  - name: sentence2
    dtype: string
  splits:
  - name: test
    num_bytes: 1781235
    num_examples: 5049
  download_size: 3702442
  dataset_size: 1781235
- config_name: cvit-mkb-clsr.en-ur
  features:
  - name: sentence1
    dtype: string
  - name: sentence2
    dtype: string
  splits:
  - name: test
    num_bytes: 290450
    num_examples: 1006
  download_size: 3702442
  dataset_size: 290450
- config_name: iitp-mr.hi
  features:
  - name: text
    dtype: string
  - name: label
    dtype:
      class_label:
        names:
          0: negative
          1: neutral
          2: positive
  splits:
  - name: test
    num_bytes: 702377
    num_examples: 310
  - name: train
    num_bytes: 6704909
    num_examples: 2480
  - name: validation
    num_bytes: 822222
    num_examples: 310
  download_size: 1742048
  dataset_size: 8229508
- config_name: iitp-pr.hi
  features:
  - name: text
    dtype: string
  - name: label
    dtype:
      class_label:
        names:
          0: negative
          1: neutral
          2: positive
  splits:
  - name: test
    num_bytes: 121914
    num_examples: 523
  - name: train
    num_bytes: 945593
    num_examples: 4182
  - name: validation
    num_bytes: 120104
    num_examples: 523
  download_size: 266545
  dataset_size: 1187611
- config_name: actsa-sc.te
  features:
  - name: text
    dtype: string
  - name: label
    dtype:
      class_label:
        names:
          0: positive
          1: negative
  splits:
  - name: test
    num_bytes: 168295
    num_examples: 541
  - name: train
    num_bytes: 1370911
    num_examples: 4328
  - name: validation
    num_bytes: 166093
    num_examples: 541
  download_size: 378882
  dataset_size: 1705299
- config_name: md.hi
  features:
  - name: sentence
    dtype: string
  - name: discourse_mode
    dtype: string
  - name: story_number
    dtype: int32
  - name: id
    dtype: int32
  splits:
  - name: test
    num_bytes: 210183
    num_examples: 997
  - name: train
    num_bytes: 1672117
    num_examples: 7974
  - name: validation
    num_bytes: 211195
    num_examples: 997
  download_size: 1048441
  dataset_size: 2093495
- config_name: wiki-ner.as
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: B-LOC
          1: B-ORG
          2: B-PER
          3: I-LOC
          4: I-ORG
          5: I-PER
          6: O
  - name: additional_info
    sequence:
      sequence: string
  splits:
  - name: test
    num_bytes: 50480
    num_examples: 160
  - name: train
    num_bytes: 375007
    num_examples: 1021
  - name: validation
    num_bytes: 49336
    num_examples: 157
  download_size: 5980272
  dataset_size: 474823
- config_name: wiki-ner.bn
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: B-LOC
          1: B-ORG
          2: B-PER
          3: I-LOC
          4: I-ORG
          5: I-PER
          6: O
  - name: additional_info
    sequence:
      sequence: string
  splits:
  - name: test
    num_bytes: 985965
    num_examples: 2690
  - name: train
    num_bytes: 7502896
    num_examples: 20223
  - name: validation
    num_bytes: 988707
    num_examples: 2985
  download_size: 5980272
  dataset_size: 9477568
- config_name: wiki-ner.gu
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: B-LOC
          1: B-ORG
          2: B-PER
          3: I-LOC
          4: I-ORG
          5: I-PER
          6: O
  - name: additional_info
    sequence:
      sequence: string
  splits:
  - name: test
    num_bytes: 197901
    num_examples: 255
  - name: train
    num_bytes: 1571612
    num_examples: 2343
  - name: validation
    num_bytes: 192828
    num_examples: 297
  download_size: 5980272
  dataset_size: 1962341
- config_name: wiki-ner.hi
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: B-LOC
          1: B-ORG
          2: B-PER
          3: I-LOC
          4: I-ORG
          5: I-PER
          6: O
  - name: additional_info
    sequence:
      sequence: string
  splits:
  - name: test
    num_bytes: 475277
    num_examples: 1256
  - name: train
    num_bytes: 3762529
    num_examples: 9463
  - name: validation
    num_bytes: 468702
    num_examples: 1114
  download_size: 5980272
  dataset_size: 4706508
- config_name: wiki-ner.kn
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: B-LOC
          1: B-ORG
          2: B-PER
          3: I-LOC
          4: I-ORG
          5: I-PER
          6: O
  - name: additional_info
    sequence:
      sequence: string
  splits:
  - name: test
    num_bytes: 180815
    num_examples: 476
  - name: train
    num_bytes: 1352051
    num_examples: 2679
  - name: validation
    num_bytes: 179562
    num_examples: 412
  download_size: 5980272
  dataset_size: 1712428
- config_name: wiki-ner.ml
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: B-LOC
          1: B-ORG
          2: B-PER
          3: I-LOC
          4: I-ORG
          5: I-PER
          6: O
  - name: additional_info
    sequence:
      sequence: string
  splits:
  - name: test
    num_bytes: 991126
    num_examples: 2042
  - name: train
    num_bytes: 7678935
    num_examples: 15620
  - name: validation
    num_bytes: 969971
    num_examples: 2067
  download_size: 5980272
  dataset_size: 9640032
- config_name: wiki-ner.mr
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: B-LOC
          1: B-ORG
          2: B-PER
          3: I-LOC
          4: I-ORG
          5: I-PER
          6: O
  - name: additional_info
    sequence:
      sequence: string
  splits:
  - name: test
    num_bytes: 655706
    num_examples: 1329
  - name: train
    num_bytes: 5431537
    num_examples: 12151
  - name: validation
    num_bytes: 701661
    num_examples: 1498
  download_size: 5980272
  dataset_size: 6788904
- config_name: wiki-ner.or
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: B-LOC
          1: B-ORG
          2: B-PER
          3: I-LOC
          4: I-ORG
          5: I-PER
          6: O
  - name: additional_info
    sequence:
      sequence: string
  splits:
  - name: test
    num_bytes: 62235
    num_examples: 153
  - name: train
    num_bytes: 493782
    num_examples: 1077
  - name: validation
    num_bytes: 58592
    num_examples: 132
  download_size: 5980272
  dataset_size: 614609
- config_name: wiki-ner.pa
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: B-LOC
          1: B-ORG
          2: B-PER
          3: I-LOC
          4: I-ORG
          5: I-PER
          6: O
  - name: additional_info
    sequence:
      sequence: string
  splits:
  - name: test
    num_bytes: 61812
    num_examples: 179
  - name: train
    num_bytes: 520268
    num_examples: 1408
  - name: validation
    num_bytes: 61194
    num_examples: 186
  download_size: 5980272
  dataset_size: 643274
- config_name: wiki-ner.ta
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: B-LOC
          1: B-ORG
          2: B-PER
          3: I-LOC
          4: I-ORG
          5: I-PER
          6: O
  - name: additional_info
    sequence:
      sequence: string
  splits:
  - name: test
    num_bytes: 1321650
    num_examples: 2611
  - name: train
    num_bytes: 10117152
    num_examples: 20466
  - name: validation
    num_bytes: 1267212
    num_examples: 2586
  download_size: 5980272
  dataset_size: 12706014
- config_name: wiki-ner.te
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: B-LOC
          1: B-ORG
          2: B-PER
          3: I-LOC
          4: I-ORG
          5: I-PER
          6: O
  - name: additional_info
    sequence:
      sequence: string
  splits:
  - name: test
    num_bytes: 507830
    num_examples: 1110
  - name: train
    num_bytes: 3881235
    num_examples: 7978
  - name: validation
    num_bytes: 458533
    num_examples: 841
  download_size: 5980272
  dataset_size: 4847598
---

# Dataset Card for "indic_glue"

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

- **Homepage:** https://ai4bharat.iitm.ac.in/indic-glue
- **Repository:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Paper:** [IndicNLPSuite: Monolingual Corpora, Evaluation Benchmarks and Pre-trained Multilingual Language Models for Indian Languages](https://aclanthology.org/2020.findings-emnlp.445/)
- **Point of Contact:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Size of downloaded dataset files:** 3351.18 MB
- **Size of the generated dataset:** 1573.33 MB
- **Total amount of disk used:** 4924.51 MB

### Dataset Summary

IndicGLUE is a natural language understanding benchmark for Indian languages. It contains a wide
variety of tasks and covers 11 major Indian languages - as, bn, gu, hi, kn, ml, mr, or, pa, ta, te.

The Winograd Schema Challenge (Levesque et al., 2011) is a reading comprehension task
in which a system must read a sentence with a pronoun and select the referent of that pronoun from
a list of choices. The examples are manually constructed to foil simple statistical methods: Each
one is contingent on contextual information provided by a single word or phrase in the sentence.
To convert the problem into sentence pair classification, we construct sentence pairs by replacing
the ambiguous pronoun with each possible referent. The task is to predict if the sentence with the
pronoun substituted is entailed by the original sentence. We use a small evaluation set consisting of
new examples derived from fiction books that was shared privately by the authors of the original
corpus. While the included training set is balanced between two classes, the test set is imbalanced
between them (65% not entailment). Also, due to a data quirk, the development set is adversarial:
hypotheses are sometimes shared between training and development examples, so if a model memorizes the
training examples, they will predict the wrong label on corresponding development set
example. As with QNLI, each example is evaluated separately, so there is not a systematic correspondence
between a model's score on this task and its score on the unconverted original task. We
call converted dataset WNLI (Winograd NLI). This dataset is translated and publicly released for 3
Indian languages by AI4Bharat.

### Supported Tasks and Leaderboards

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Languages

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

## Dataset Structure

### Data Instances

#### actsa-sc.te

- **Size of downloaded dataset files:** 0.36 MB
- **Size of the generated dataset:** 1.63 MB
- **Total amount of disk used:** 1.99 MB

An example of 'validation' looks as follows.
```
This example was too long and was cropped:

{
    "label": 0,
    "text": "\"ప్రయాణాల్లో ఉన్నవారికోసం బస్ స్టేషన్లు, రైల్వే స్టేషన్లలో పల్స్పోలియో బూతులను ఏర్పాటు చేసి చిన్నారులకు పోలియో చుక్కలు వేసేలా ఏర..."
}
```

#### bbca.hi

- **Size of downloaded dataset files:** 5.50 MB
- **Size of the generated dataset:** 26.35 MB
- **Total amount of disk used:** 31.85 MB

An example of 'train' looks as follows.
```
This example was too long and was cropped:

{
    "label": "pakistan",
    "text": "\"नेटिजन यानि इंटरनेट पर सक्रिय नागरिक अब ट्विटर पर सरकार द्वारा लगाए प्रतिबंधों के समर्थन या विरोध में अपने विचार व्यक्त करते है..."
}
```

#### copa.en

- **Size of downloaded dataset files:** 0.72 MB
- **Size of the generated dataset:** 0.11 MB
- **Total amount of disk used:** 0.83 MB

An example of 'validation' looks as follows.
```
{
    "choice1": "I swept the floor in the unoccupied room.",
    "choice2": "I shut off the light in the unoccupied room.",
    "label": 1,
    "premise": "I wanted to conserve energy.",
    "question": "effect"
}
```

#### copa.gu

- **Size of downloaded dataset files:** 0.72 MB
- **Size of the generated dataset:** 0.22 MB
- **Total amount of disk used:** 0.94 MB

An example of 'train' looks as follows.
```
This example was too long and was cropped:

{
    "choice1": "\"સ્ત્રી જાણતી હતી કે તેનો મિત્ર મુશ્કેલ સમયમાંથી પસાર થઈ રહ્યો છે.\"...",
    "choice2": "\"મહિલાને લાગ્યું કે તેના મિત્રએ તેની દયાળુ લાભ લીધો છે.\"...",
    "label": 0,
    "premise": "મહિલાએ તેના મિત્રની મુશ્કેલ વર્તન સહન કરી.",
    "question": "cause"
}
```

#### copa.hi

- **Size of downloaded dataset files:** 0.72 MB
- **Size of the generated dataset:** 0.22 MB
- **Total amount of disk used:** 0.94 MB

An example of 'validation' looks as follows.
```
{
    "choice1": "मैंने उसका प्रस्ताव ठुकरा दिया।",
    "choice2": "उन्होंने मुझे उत्पाद खरीदने के लिए राजी किया।",
    "label": 0,
    "premise": "मैंने सेल्समैन की पिच पर शक किया।",
    "question": "effect"
}
```

### Data Fields

The data fields are the same among all splits.

#### actsa-sc.te
- `text`: a `string` feature.
- `label`: a classification label, with possible values including `positive` (0), `negative` (1).

#### bbca.hi
- `label`: a `string` feature.
- `text`: a `string` feature.

#### copa.en
- `premise`: a `string` feature.
- `choice1`: a `string` feature.
- `choice2`: a `string` feature.
- `question`: a `string` feature.
- `label`: a `int32` feature.

#### copa.gu
- `premise`: a `string` feature.
- `choice1`: a `string` feature.
- `choice2`: a `string` feature.
- `question`: a `string` feature.
- `label`: a `int32` feature.

#### copa.hi
- `premise`: a `string` feature.
- `choice1`: a `string` feature.
- `choice2`: a `string` feature.
- `question`: a `string` feature.
- `label`: a `int32` feature.

### Data Splits

#### actsa-sc.te

|           |train|validation|test|
|-----------|----:|---------:|---:|
|actsa-sc.te| 4328|       541| 541|

#### bbca.hi

|       |train|test|
|-------|----:|---:|
|bbca.hi| 3467| 866|

#### copa.en

|       |train|validation|test|
|-------|----:|---------:|---:|
|copa.en|  400|       100| 500|

#### copa.gu

|       |train|validation|test|
|-------|----:|---------:|---:|
|copa.gu|  362|        88| 448|

#### copa.hi

|       |train|validation|test|
|-------|----:|---------:|---:|
|copa.hi|  362|        88| 449|

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
@inproceedings{kakwani-etal-2020-indicnlpsuite,
    title = "{I}ndic{NLPS}uite: Monolingual Corpora, Evaluation Benchmarks and Pre-trained Multilingual Language Models for {I}ndian Languages",
    author = "Kakwani, Divyanshu  and
      Kunchukuttan, Anoop  and
      Golla, Satish  and
      N.C., Gokul  and
      Bhattacharyya, Avik  and
      Khapra, Mitesh M.  and
      Kumar, Pratyush",
    booktitle = "Findings of the Association for Computational Linguistics: EMNLP 2020",
    month = nov,
    year = "2020",
    address = "Online",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/2020.findings-emnlp.445",
    doi = "10.18653/v1/2020.findings-emnlp.445",
    pages = "4948--4961",
}

@inproceedings{Levesque2011TheWS,
title={The Winograd Schema Challenge},
author={H. Levesque and E. Davis and L. Morgenstern},
booktitle={KR},
year={2011}
}
```

### Contributions

Thanks to [@sumanthd17](https://github.com/sumanthd17) for adding this dataset.