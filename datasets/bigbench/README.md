---
annotations_creators:
- crowdsourced
- expert-generated
- machine-generated
language_creators:
- crowdsourced
- expert-generated
- machine-generated
- other
language:
- en
license:
- apache-2.0
multilinguality:
- multilingual
- monolingual
pretty_name: bigbench
size_categories:
- unknown
source_datasets:
- original
task_categories:
- multiple-choice
- question-answering
- text-classification
- text-generation
- zero-shot-classification
- other
task_ids:
- multiple-choice-qa
- extractive-qa
- open-domain-qa
- closed-domain-qa
- fact-checking
- acceptability-classification
- intent-classification
- multi-class-classification
- multi-label-classification
- text-scoring
- hate-speech-detection
- language-modeling
dataset_info:
- config_name: abstract_narrative_understanding
  features:
  - name: idx
    dtype: int32
  - name: inputs
    dtype: string
  - name: targets
    sequence: string
  - name: multiple_choice_targets
    sequence: string
  - name: multiple_choice_scores
    sequence: int32
  splits:
  - name: default
    num_bytes: 6574843
    num_examples: 3000
  - name: train
    num_bytes: 5261643
    num_examples: 2400
  - name: validation
    num_bytes: 1313224
    num_examples: 600
  download_size: 0
  dataset_size: 13149710
- config_name: anachronisms
  features:
  - name: idx
    dtype: int32
  - name: inputs
    dtype: string
  - name: targets
    sequence: string
  - name: multiple_choice_targets
    sequence: string
  - name: multiple_choice_scores
    sequence: int32
  splits:
  - name: default
    num_bytes: 48937
    num_examples: 230
  - name: train
    num_bytes: 39209
    num_examples: 184
  - name: validation
    num_bytes: 9752
    num_examples: 46
  download_size: 0
  dataset_size: 97898
- config_name: analogical_similarity
  features:
  - name: idx
    dtype: int32
  - name: inputs
    dtype: string
  - name: targets
    sequence: string
  - name: multiple_choice_targets
    sequence: string
  - name: multiple_choice_scores
    sequence: int32
  splits:
  - name: default
    num_bytes: 1374163
    num_examples: 323
  - name: train
    num_bytes: 1101796
    num_examples: 259
  - name: validation
    num_bytes: 272391
    num_examples: 64
  download_size: 0
  dataset_size: 2748350
- config_name: analytic_entailment
  features:
  - name: idx
    dtype: int32
  - name: inputs
    dtype: string
  - name: targets
    sequence: string
  - name: multiple_choice_targets
    sequence: string
  - name: multiple_choice_scores
    sequence: int32
  splits:
  - name: default
    num_bytes: 17367
    num_examples: 70
  - name: train
    num_bytes: 13413
    num_examples: 54
  - name: validation
    num_bytes: 3978
    num_examples: 16
  download_size: 0
  dataset_size: 34758
- config_name: arithmetic
  features:
  - name: idx
    dtype: int32
  - name: inputs
    dtype: string
  - name: targets
    sequence: string
  - name: multiple_choice_targets
    sequence: string
  - name: multiple_choice_scores
    sequence: int32
  splits:
  - name: default
    num_bytes: 3848183
    num_examples: 15023
  - name: train
    num_bytes: 3078715
    num_examples: 12019
  - name: validation
    num_bytes: 769493
    num_examples: 3004
  download_size: 0
  dataset_size: 7696391
- config_name: ascii_word_recognition
  features:
  - name: idx
    dtype: int32
  - name: inputs
    dtype: string
  - name: targets
    sequence: string
  - name: multiple_choice_targets
    sequence: string
  - name: multiple_choice_scores
    sequence: int32
  splits:
  - name: default
    num_bytes: 4985315
    num_examples: 5000
  - name: train
    num_bytes: 3997801
    num_examples: 4000
  - name: validation
    num_bytes: 987542
    num_examples: 1000
  download_size: 0
  dataset_size: 9970658
- config_name: authorship_verification
  features:
  - name: idx
    dtype: int32
  - name: inputs
    dtype: string
  - name: targets
    sequence: string
  - name: multiple_choice_targets
    sequence: string
  - name: multiple_choice_scores
    sequence: int32
  splits:
  - name: default
    num_bytes: 14118946
    num_examples: 880
  - name: train
    num_bytes: 11288769
    num_examples: 704
  - name: validation
    num_bytes: 2830201
    num_examples: 176
  download_size: 0
  dataset_size: 28237916
- config_name: auto_categorization
  features:
  - name: idx
    dtype: int32
  - name: inputs
    dtype: string
  - name: targets
    sequence: string
  - name: multiple_choice_targets
    sequence: string
  - name: multiple_choice_scores
    sequence: int32
  splits:
  - name: default
    num_bytes: 40618
    num_examples: 328
  - name: train
    num_bytes: 33053
    num_examples: 263
  - name: validation
    num_bytes: 7594
    num_examples: 65
  download_size: 0
  dataset_size: 81265
- config_name: auto_debugging
  features:
  - name: idx
    dtype: int32
  - name: inputs
    dtype: string
  - name: targets
    sequence: string
  - name: multiple_choice_targets
    sequence: string
  - name: multiple_choice_scores
    sequence: int32
  splits:
  - name: default
    num_bytes: 5145
    num_examples: 34
  - name: train
    num_bytes: 2682
    num_examples: 18
  - name: validation
    num_bytes: 2491
    num_examples: 16
  download_size: 0
  dataset_size: 10318
- config_name: bbq_lite_json
  features:
  - name: idx
    dtype: int32
  - name: inputs
    dtype: string
  - name: targets
    sequence: string
  - name: multiple_choice_targets
    sequence: string
  - name: multiple_choice_scores
    sequence: int32
  splits:
  - name: default
    num_bytes: 6898580
    num_examples: 16076
  - name: train
    num_bytes: 5515066
    num_examples: 12866
  - name: validation
    num_bytes: 1383539
    num_examples: 3210
  download_size: 0
  dataset_size: 13797185
- config_name: bridging_anaphora_resolution_barqa
  features:
  - name: idx
    dtype: int32
  - name: inputs
    dtype: string
  - name: targets
    sequence: string
  - name: multiple_choice_targets
    sequence: string
  - name: multiple_choice_scores
    sequence: int32
  splits:
  - name: default
    num_bytes: 1971124
    num_examples: 648
  - name: train
    num_bytes: 1537357
    num_examples: 519
  - name: validation
    num_bytes: 433796
    num_examples: 129
  download_size: 0
  dataset_size: 3942277
- config_name: causal_judgment
  features:
  - name: idx
    dtype: int32
  - name: inputs
    dtype: string
  - name: targets
    sequence: string
  - name: multiple_choice_targets
    sequence: string
  - name: multiple_choice_scores
    sequence: int32
  splits:
  - name: default
    num_bytes: 204974
    num_examples: 190
  - name: train
    num_bytes: 165021
    num_examples: 152
  - name: validation
    num_bytes: 39977
    num_examples: 38
  download_size: 0
  dataset_size: 409972
- config_name: cause_and_effect
  features:
  - name: idx
    dtype: int32
  - name: inputs
    dtype: string
  - name: targets
    sequence: string
  - name: multiple_choice_targets
    sequence: string
  - name: multiple_choice_scores
    sequence: int32
  splits:
  - name: default
    num_bytes: 49397
    num_examples: 153
  - name: train
    num_bytes: 39691
    num_examples: 123
  - name: validation
    num_bytes: 9730
    num_examples: 30
  download_size: 0
  dataset_size: 98818
- config_name: checkmate_in_one
  features:
  - name: idx
    dtype: int32
  - name: inputs
    dtype: string
  - name: targets
    sequence: string
  - name: multiple_choice_targets
    sequence: string
  - name: multiple_choice_scores
    sequence: int32
  splits:
  - name: default
    num_bytes: 3140634
    num_examples: 3498
  - name: train
    num_bytes: 2516239
    num_examples: 2799
  - name: validation
    num_bytes: 624419
    num_examples: 699
  download_size: 0
  dataset_size: 6281292
- config_name: chess_state_tracking
  features:
  - name: idx
    dtype: int32
  - name: inputs
    dtype: string
  - name: targets
    sequence: string
  - name: multiple_choice_targets
    sequence: string
  - name: multiple_choice_scores
    sequence: int32
  splits:
  - name: default
    num_bytes: 3270710
    num_examples: 6000
  - name: train
    num_bytes: 2616922
    num_examples: 4800
  - name: validation
    num_bytes: 653816
    num_examples: 1200
  download_size: 0
  dataset_size: 6541448
- config_name: chinese_remainder_theorem
  features:
  - name: idx
    dtype: int32
  - name: inputs
    dtype: string
  - name: targets
    sequence: string
  - name: multiple_choice_targets
    sequence: string
  - name: multiple_choice_scores
    sequence: int32
  splits:
  - name: default
    num_bytes: 153313
    num_examples: 500
  - name: train
    num_bytes: 122679
    num_examples: 400
  - name: validation
    num_bytes: 30662
    num_examples: 100
  download_size: 0
  dataset_size: 306654
- config_name: cifar10_classification
  features:
  - name: idx
    dtype: int32
  - name: inputs
    dtype: string
  - name: targets
    sequence: string
  - name: multiple_choice_targets
    sequence: string
  - name: multiple_choice_scores
    sequence: int32
  splits:
  - name: default
    num_bytes: 111049748
    num_examples: 20000
  - name: train
    num_bytes: 88804772
    num_examples: 16000
  - name: validation
    num_bytes: 22245000
    num_examples: 4000
  download_size: 0
  dataset_size: 222099520
- config_name: code_line_description
  features:
  - name: idx
    dtype: int32
  - name: inputs
    dtype: string
  - name: targets
    sequence: string
  - name: multiple_choice_targets
    sequence: string
  - name: multiple_choice_scores
    sequence: int32
  splits:
  - name: default
    num_bytes: 33733
    num_examples: 60
  - name: train
    num_bytes: 25583
    num_examples: 44
  - name: validation
    num_bytes: 8174
    num_examples: 16
  download_size: 0
  dataset_size: 67490
- config_name: codenames
  features:
  - name: idx
    dtype: int32
  - name: inputs
    dtype: string
  - name: targets
    sequence: string
  - name: multiple_choice_targets
    sequence: string
  - name: multiple_choice_scores
    sequence: int32
  splits:
  - name: default
    num_bytes: 25234
    num_examples: 85
  - name: train
    num_bytes: 20001
    num_examples: 68
  - name: validation
    num_bytes: 5262
    num_examples: 17
  download_size: 0
  dataset_size: 50497
- config_name: color
  features:
  - name: idx
    dtype: int32
  - name: inputs
    dtype: string
  - name: targets
    sequence: string
  - name: multiple_choice_targets
    sequence: string
  - name: multiple_choice_scores
    sequence: int32
  splits:
  - name: default
    num_bytes: 1638787
    num_examples: 4000
  - name: train
    num_bytes: 1311087
    num_examples: 3200
  - name: validation
    num_bytes: 327724
    num_examples: 800
  download_size: 0
  dataset_size: 3277598
- config_name: common_morpheme
  features:
  - name: idx
    dtype: int32
  - name: inputs
    dtype: string
  - name: targets
    sequence: string
  - name: multiple_choice_targets
    sequence: string
  - name: multiple_choice_scores
    sequence: int32
  splits:
  - name: default
    num_bytes: 12444
    num_examples: 50
  - name: train
    num_bytes: 8490
    num_examples: 34
  - name: validation
    num_bytes: 3978
    num_examples: 16
  download_size: 0
  dataset_size: 24912
- config_name: conceptual_combinations
  features:
  - name: idx
    dtype: int32
  - name: inputs
    dtype: string
  - name: targets
    sequence: string
  - name: multiple_choice_targets
    sequence: string
  - name: multiple_choice_scores
    sequence: int32
  splits:
  - name: default
    num_bytes: 58948
    num_examples: 103
  - name: train
    num_bytes: 48087
    num_examples: 84
  - name: validation
    num_bytes: 10886
    num_examples: 19
  download_size: 0
  dataset_size: 117921
- config_name: conlang_translation
  features:
  - name: idx
    dtype: int32
  - name: inputs
    dtype: string
  - name: targets
    sequence: string
  - name: multiple_choice_targets
    sequence: string
  - name: multiple_choice_scores
    sequence: int32
  splits:
  - name: default
    num_bytes: 215239
    num_examples: 164
  - name: train
    num_bytes: 173069
    num_examples: 132
  - name: validation
    num_bytes: 42198
    num_examples: 32
  download_size: 0
  dataset_size: 430506
- config_name: contextual_parametric_knowledge_conflicts
  features:
  - name: idx
    dtype: int32
  - name: inputs
    dtype: string
  - name: targets
    sequence: string
  - name: multiple_choice_targets
    sequence: string
  - name: multiple_choice_scores
    sequence: int32
  splits:
  - name: default
    num_bytes: 14594175
    num_examples: 17528
  - name: train
    num_bytes: 11671543
    num_examples: 14023
  - name: validation
    num_bytes: 2922658
    num_examples: 3505
  download_size: 0
  dataset_size: 29188376
- config_name: crash_blossom
  features:
  - name: idx
    dtype: int32
  - name: inputs
    dtype: string
  - name: targets
    sequence: string
  - name: multiple_choice_targets
    sequence: string
  - name: multiple_choice_scores
    sequence: int32
  splits:
  - name: default
    num_bytes: 12242
    num_examples: 38
  - name: train
    num_bytes: 7037
    num_examples: 22
  - name: validation
    num_bytes: 5229
    num_examples: 16
  download_size: 0
  dataset_size: 24508
- config_name: crass_ai
  features:
  - name: idx
    dtype: int32
  - name: inputs
    dtype: string
  - name: targets
    sequence: string
  - name: multiple_choice_targets
    sequence: string
  - name: multiple_choice_scores
    sequence: int32
  splits:
  - name: default
    num_bytes: 22922
    num_examples: 44
  - name: train
    num_bytes: 14172
    num_examples: 28
  - name: validation
    num_bytes: 8774
    num_examples: 16
  download_size: 0
  dataset_size: 45868
- config_name: cryobiology_spanish
  features:
  - name: idx
    dtype: int32
  - name: inputs
    dtype: string
  - name: targets
    sequence: string
  - name: multiple_choice_targets
    sequence: string
  - name: multiple_choice_scores
    sequence: int32
  splits:
  - name: default
    num_bytes: 38754
    num_examples: 146
  - name: train
    num_bytes: 31198
    num_examples: 117
  - name: validation
    num_bytes: 7581
    num_examples: 29
  download_size: 0
  dataset_size: 77533
- config_name: cryptonite
  features:
  - name: idx
    dtype: int32
  - name: inputs
    dtype: string
  - name: targets
    sequence: string
  - name: multiple_choice_targets
    sequence: string
  - name: multiple_choice_scores
    sequence: int32
  splits:
  - name: default
    num_bytes: 2847756
    num_examples: 26157
  - name: train
    num_bytes: 2278424
    num_examples: 20926
  - name: validation
    num_bytes: 569360
    num_examples: 5231
  download_size: 0
  dataset_size: 5695540
- config_name: cs_algorithms
  features:
  - name: idx
    dtype: int32
  - name: inputs
    dtype: string
  - name: targets
    sequence: string
  - name: multiple_choice_targets
    sequence: string
  - name: multiple_choice_scores
    sequence: int32
  splits:
  - name: default
    num_bytes: 273274
    num_examples: 1320
  - name: train
    num_bytes: 218868
    num_examples: 1056
  - name: validation
    num_bytes: 54430
    num_examples: 264
  download_size: 0
  dataset_size: 546572
- config_name: dark_humor_detection
  features:
  - name: idx
    dtype: int32
  - name: inputs
    dtype: string
  - name: targets
    sequence: string
  - name: multiple_choice_targets
    sequence: string
  - name: multiple_choice_scores
    sequence: int32
  splits:
  - name: default
    num_bytes: 26610
    num_examples: 80
  - name: train
    num_bytes: 21315
    num_examples: 64
  - name: validation
    num_bytes: 5319
    num_examples: 16
  download_size: 0
  dataset_size: 53244
- config_name: date_understanding
  features:
  - name: idx
    dtype: int32
  - name: inputs
    dtype: string
  - name: targets
    sequence: string
  - name: multiple_choice_targets
    sequence: string
  - name: multiple_choice_scores
    sequence: int32
  splits:
  - name: default
    num_bytes: 95249
    num_examples: 369
  - name: train
    num_bytes: 76443
    num_examples: 296
  - name: validation
    num_bytes: 18831
    num_examples: 73
  download_size: 0
  dataset_size: 190523
- config_name: disambiguation_qa
  features:
  - name: idx
    dtype: int32
  - name: inputs
    dtype: string
  - name: targets
    sequence: string
  - name: multiple_choice_targets
    sequence: string
  - name: multiple_choice_scores
    sequence: int32
  splits:
  - name: default
    num_bytes: 122626
    num_examples: 258
  - name: train
    num_bytes: 98815
    num_examples: 207
  - name: validation
    num_bytes: 23835
    num_examples: 51
  download_size: 0
  dataset_size: 245276
- config_name: discourse_marker_prediction
  features:
  - name: idx
    dtype: int32
  - name: inputs
    dtype: string
  - name: targets
    sequence: string
  - name: multiple_choice_targets
    sequence: string
  - name: multiple_choice_scores
    sequence: int32
  splits:
  - name: default
    num_bytes: 2091888
    num_examples: 857
  - name: train
    num_bytes: 1667020
    num_examples: 686
  - name: validation
    num_bytes: 424892
    num_examples: 171
  download_size: 0
  dataset_size: 4183800
- config_name: disfl_qa
  features:
  - name: idx
    dtype: int32
  - name: inputs
    dtype: string
  - name: targets
    sequence: string
  - name: multiple_choice_targets
    sequence: string
  - name: multiple_choice_scores
    sequence: int32
  splits:
  - name: default
    num_bytes: 7965803
    num_examples: 8000
  - name: train
    num_bytes: 6377339
    num_examples: 6400
  - name: validation
    num_bytes: 1588492
    num_examples: 1600
  download_size: 0
  dataset_size: 15931634
- config_name: dyck_languages
  features:
  - name: idx
    dtype: int32
  - name: inputs
    dtype: string
  - name: targets
    sequence: string
  - name: multiple_choice_targets
    sequence: string
  - name: multiple_choice_scores
    sequence: int32
  splits:
  - name: default
    num_bytes: 1238565
    num_examples: 1000
  - name: train
    num_bytes: 991204
    num_examples: 800
  - name: validation
    num_bytes: 247385
    num_examples: 200
  download_size: 0
  dataset_size: 2477154
- config_name: elementary_math_qa
  features:
  - name: idx
    dtype: int32
  - name: inputs
    dtype: string
  - name: targets
    sequence: string
  - name: multiple_choice_targets
    sequence: string
  - name: multiple_choice_scores
    sequence: int32
  splits:
  - name: default
    num_bytes: 13471291
    num_examples: 38160
  - name: train
    num_bytes: 10789985
    num_examples: 30531
  - name: validation
    num_bytes: 2681331
    num_examples: 7629
  download_size: 0
  dataset_size: 26942607
- config_name: emoji_movie
  features:
  - name: idx
    dtype: int32
  - name: inputs
    dtype: string
  - name: targets
    sequence: string
  - name: multiple_choice_targets
    sequence: string
  - name: multiple_choice_scores
    sequence: int32
  splits:
  - name: default
    num_bytes: 33767
    num_examples: 100
  - name: train
    num_bytes: 27071
    num_examples: 80
  - name: validation
    num_bytes: 6720
    num_examples: 20
  download_size: 0
  dataset_size: 67558
- config_name: emojis_emotion_prediction
  features:
  - name: idx
    dtype: int32
  - name: inputs
    dtype: string
  - name: targets
    sequence: string
  - name: multiple_choice_targets
    sequence: string
  - name: multiple_choice_scores
    sequence: int32
  splits:
  - name: default
    num_bytes: 48155
    num_examples: 131
  - name: train
    num_bytes: 38601
    num_examples: 105
  - name: validation
    num_bytes: 9579
    num_examples: 26
  download_size: 0
  dataset_size: 96335
- config_name: empirical_judgments
  features:
  - name: idx
    dtype: int32
  - name: inputs
    dtype: string
  - name: targets
    sequence: string
  - name: multiple_choice_targets
    sequence: string
  - name: multiple_choice_scores
    sequence: int32
  splits:
  - name: default
    num_bytes: 47574
    num_examples: 99
  - name: train
    num_bytes: 38410
    num_examples: 80
  - name: validation
    num_bytes: 9188
    num_examples: 19
  download_size: 0
  dataset_size: 95172
- config_name: english_proverbs
  features:
  - name: idx
    dtype: int32
  - name: inputs
    dtype: string
  - name: targets
    sequence: string
  - name: multiple_choice_targets
    sequence: string
  - name: multiple_choice_scores
    sequence: int32
  splits:
  - name: default
    num_bytes: 22577
    num_examples: 34
  - name: train
    num_bytes: 12103
    num_examples: 18
  - name: validation
    num_bytes: 10499
    num_examples: 16
  download_size: 0
  dataset_size: 45179
- config_name: english_russian_proverbs
  features:
  - name: idx
    dtype: int32
  - name: inputs
    dtype: string
  - name: targets
    sequence: string
  - name: multiple_choice_targets
    sequence: string
  - name: multiple_choice_scores
    sequence: int32
  splits:
  - name: default
    num_bytes: 59974
    num_examples: 80
  - name: train
    num_bytes: 48115
    num_examples: 64
  - name: validation
    num_bytes: 11883
    num_examples: 16
  download_size: 0
  dataset_size: 119972
- config_name: entailed_polarity
  features:
  - name: idx
    dtype: int32
  - name: inputs
    dtype: string
  - name: targets
    sequence: string
  - name: multiple_choice_targets
    sequence: string
  - name: multiple_choice_scores
    sequence: int32
  splits:
  - name: default
    num_bytes: 25501
    num_examples: 148
  - name: train
    num_bytes: 20419
    num_examples: 119
  - name: validation
    num_bytes: 5107
    num_examples: 29
  download_size: 0
  dataset_size: 51027
- config_name: entailed_polarity_hindi
  features:
  - name: idx
    dtype: int32
  - name: inputs
    dtype: string
  - name: targets
    sequence: string
  - name: multiple_choice_targets
    sequence: string
  - name: multiple_choice_scores
    sequence: int32
  splits:
  - name: default
    num_bytes: 57129
    num_examples: 138
  - name: train
    num_bytes: 45895
    num_examples: 111
  - name: validation
    num_bytes: 11258
    num_examples: 27
  download_size: 0
  dataset_size: 114282
- config_name: epistemic_reasoning
  features:
  - name: idx
    dtype: int32
  - name: inputs
    dtype: string
  - name: targets
    sequence: string
  - name: multiple_choice_targets
    sequence: string
  - name: multiple_choice_scores
    sequence: int32
  splits:
  - name: default
    num_bytes: 887932
    num_examples: 2000
  - name: train
    num_bytes: 710731
    num_examples: 1600
  - name: validation
    num_bytes: 177225
    num_examples: 400
  download_size: 0
  dataset_size: 1775888
- config_name: evaluating_information_essentiality
  features:
  - name: idx
    dtype: int32
  - name: inputs
    dtype: string
  - name: targets
    sequence: string
  - name: multiple_choice_targets
    sequence: string
  - name: multiple_choice_scores
    sequence: int32
  splits:
  - name: default
    num_bytes: 77564
    num_examples: 68
  - name: train
    num_bytes: 59660
    num_examples: 52
  - name: validation
    num_bytes: 17928
    num_examples: 16
  download_size: 0
  dataset_size: 155152
- config_name: fact_checker
  features:
  - name: idx
    dtype: int32
  - name: inputs
    dtype: string
  - name: targets
    sequence: string
  - name: multiple_choice_targets
    sequence: string
  - name: multiple_choice_scores
    sequence: int32
  splits:
  - name: default
    num_bytes: 1340092
    num_examples: 7154
  - name: train
    num_bytes: 1072921
    num_examples: 5724
  - name: validation
    num_bytes: 267195
    num_examples: 1430
  download_size: 0
  dataset_size: 2680208
- config_name: fantasy_reasoning
  features:
  - name: idx
    dtype: int32
  - name: inputs
    dtype: string
  - name: targets
    sequence: string
  - name: multiple_choice_targets
    sequence: string
  - name: multiple_choice_scores
    sequence: int32
  splits:
  - name: default
    num_bytes: 75987
    num_examples: 201
  - name: train
    num_bytes: 61484
    num_examples: 161
  - name: validation
    num_bytes: 14527
    num_examples: 40
  download_size: 0
  dataset_size: 151998
- config_name: few_shot_nlg
  features:
  - name: idx
    dtype: int32
  - name: inputs
    dtype: string
  - name: targets
    sequence: string
  - name: multiple_choice_targets
    sequence: string
  - name: multiple_choice_scores
    sequence: int32
  splits:
  - name: default
    num_bytes: 75985
    num_examples: 153
  - name: train
    num_bytes: 61906
    num_examples: 123
  - name: validation
    num_bytes: 14107
    num_examples: 30
  download_size: 0
  dataset_size: 151998
- config_name: figure_of_speech_detection
  features:
  - name: idx
    dtype: int32
  - name: inputs
    dtype: string
  - name: targets
    sequence: string
  - name: multiple_choice_targets
    sequence: string
  - name: multiple_choice_scores
    sequence: int32
  splits:
  - name: default
    num_bytes: 21823
    num_examples: 59
  - name: train
    num_bytes: 16046
    num_examples: 43
  - name: validation
    num_bytes: 5801
    num_examples: 16
  download_size: 0
  dataset_size: 43670
- config_name: formal_fallacies_syllogisms_negation
  features:
  - name: idx
    dtype: int32
  - name: inputs
    dtype: string
  - name: targets
    sequence: string
  - name: multiple_choice_targets
    sequence: string
  - name: multiple_choice_scores
    sequence: int32
  splits:
  - name: default
    num_bytes: 8320026
    num_examples: 14200
  - name: train
    num_bytes: 6657263
    num_examples: 11360
  - name: validation
    num_bytes: 1662787
    num_examples: 2840
  download_size: 0
  dataset_size: 16640076
- config_name: gem
  features:
  - name: idx
    dtype: int32
  - name: inputs
    dtype: string
  - name: targets
    sequence: string
  - name: multiple_choice_targets
    sequence: string
  - name: multiple_choice_scores
    sequence: int32
  splits:
  - name: default
    num_bytes: 36067188
    num_examples: 14802
  - name: train
    num_bytes: 28821034
    num_examples: 11845
  - name: validation
    num_bytes: 7246182
    num_examples: 2957
  download_size: 0
  dataset_size: 72134404
- config_name: gender_inclusive_sentences_german
  features:
  - name: idx
    dtype: int32
  - name: inputs
    dtype: string
  - name: targets
    sequence: string
  - name: multiple_choice_targets
    sequence: string
  - name: multiple_choice_scores
    sequence: int32
  splits:
  - name: default
    num_bytes: 126934
    num_examples: 200
  - name: train
    num_bytes: 100676
    num_examples: 160
  - name: validation
    num_bytes: 26286
    num_examples: 40
  download_size: 0
  dataset_size: 253896
- config_name: general_knowledge
  features:
  - name: idx
    dtype: int32
  - name: inputs
    dtype: string
  - name: targets
    sequence: string
  - name: multiple_choice_targets
    sequence: string
  - name: multiple_choice_scores
    sequence: int32
  splits:
  - name: default
    num_bytes: 21928
    num_examples: 70
  - name: train
    num_bytes: 16900
    num_examples: 54
  - name: validation
    num_bytes: 5052
    num_examples: 16
  download_size: 0
  dataset_size: 43880
- config_name: geometric_shapes
  features:
  - name: idx
    dtype: int32
  - name: inputs
    dtype: string
  - name: targets
    sequence: string
  - name: multiple_choice_targets
    sequence: string
  - name: multiple_choice_scores
    sequence: int32
  splits:
  - name: default
    num_bytes: 180621
    num_examples: 359
  - name: train
    num_bytes: 145030
    num_examples: 288
  - name: validation
    num_bytes: 35616
    num_examples: 71
  download_size: 0
  dataset_size: 361267
- config_name: goal_step_wikihow
  features:
  - name: idx
    dtype: int32
  - name: inputs
    dtype: string
  - name: targets
    sequence: string
  - name: multiple_choice_targets
    sequence: string
  - name: multiple_choice_scores
    sequence: int32
  splits:
  - name: default
    num_bytes: 3571273
    num_examples: 7053
  - name: train
    num_bytes: 2856803
    num_examples: 5643
  - name: validation
    num_bytes: 714495
    num_examples: 1410
  download_size: 0
  dataset_size: 7142571
- config_name: gre_reading_comprehension
  features:
  - name: idx
    dtype: int32
  - name: inputs
    dtype: string
  - name: targets
    sequence: string
  - name: multiple_choice_targets
    sequence: string
  - name: multiple_choice_scores
    sequence: int32
  splits:
  - name: default
    num_bytes: 94319
    num_examples: 31
  - name: train
    num_bytes: 44493
    num_examples: 15
  - name: validation
    num_bytes: 49850
    num_examples: 16
  download_size: 0
  dataset_size: 188662
- config_name: hhh_alignment
  features:
  - name: idx
    dtype: int32
  - name: inputs
    dtype: string
  - name: targets
    sequence: string
  - name: multiple_choice_targets
    sequence: string
  - name: multiple_choice_scores
    sequence: int32
  splits:
  - name: default
    num_bytes: 273006
    num_examples: 221
  - name: train
    num_bytes: 212580
    num_examples: 179
  - name: validation
    num_bytes: 60451
    num_examples: 42
  download_size: 0
  dataset_size: 546037
- config_name: hindi_question_answering
  features:
  - name: idx
    dtype: int32
  - name: inputs
    dtype: string
  - name: targets
    sequence: string
  - name: multiple_choice_targets
    sequence: string
  - name: multiple_choice_scores
    sequence: int32
  splits:
  - name: default
    num_bytes: 15155809
    num_examples: 6610
  - name: train
    num_bytes: 11984526
    num_examples: 5288
  - name: validation
    num_bytes: 3171311
    num_examples: 1322
  download_size: 0
  dataset_size: 30311646
- config_name: hindu_knowledge
  features:
  - name: idx
    dtype: int32
  - name: inputs
    dtype: string
  - name: targets
    sequence: string
  - name: multiple_choice_targets
    sequence: string
  - name: multiple_choice_scores
    sequence: int32
  splits:
  - name: default
    num_bytes: 44227
    num_examples: 175
  - name: train
    num_bytes: 35505
    num_examples: 140
  - name: validation
    num_bytes: 8747
    num_examples: 35
  download_size: 0
  dataset_size: 88479
- config_name: hinglish_toxicity
  features:
  - name: idx
    dtype: int32
  - name: inputs
    dtype: string
  - name: targets
    sequence: string
  - name: multiple_choice_targets
    sequence: string
  - name: multiple_choice_scores
    sequence: int32
  splits:
  - name: default
    num_bytes: 60712
    num_examples: 200
  - name: train
    num_bytes: 50081
    num_examples: 160
  - name: validation
    num_bytes: 10655
    num_examples: 40
  download_size: 0
  dataset_size: 121448
- config_name: human_organs_senses
  features:
  - name: idx
    dtype: int32
  - name: inputs
    dtype: string
  - name: targets
    sequence: string
  - name: multiple_choice_targets
    sequence: string
  - name: multiple_choice_scores
    sequence: int32
  splits:
  - name: default
    num_bytes: 7995
    num_examples: 42
  - name: train
    num_bytes: 4914
    num_examples: 26
  - name: validation
    num_bytes: 3105
    num_examples: 16
  download_size: 0
  dataset_size: 16014
- config_name: hyperbaton
  features:
  - name: idx
    dtype: int32
  - name: inputs
    dtype: string
  - name: targets
    sequence: string
  - name: multiple_choice_targets
    sequence: string
  - name: multiple_choice_scores
    sequence: int32
  splits:
  - name: default
    num_bytes: 9402856
    num_examples: 50000
  - name: train
    num_bytes: 7524430
    num_examples: 40000
  - name: validation
    num_bytes: 1878426
    num_examples: 10000
  download_size: 0
  dataset_size: 18805712
- config_name: identify_math_theorems
  features:
  - name: idx
    dtype: int32
  - name: inputs
    dtype: string
  - name: targets
    sequence: string
  - name: multiple_choice_targets
    sequence: string
  - name: multiple_choice_scores
    sequence: int32
  splits:
  - name: default
    num_bytes: 104899
    num_examples: 53
  - name: train
    num_bytes: 70343
    num_examples: 37
  - name: validation
    num_bytes: 34581
    num_examples: 16
  download_size: 0
  dataset_size: 209823
- config_name: identify_odd_metaphor
  features:
  - name: idx
    dtype: int32
  - name: inputs
    dtype: string
  - name: targets
    sequence: string
  - name: multiple_choice_targets
    sequence: string
  - name: multiple_choice_scores
    sequence: int32
  splits:
  - name: default
    num_bytes: 27658
    num_examples: 47
  - name: train
    num_bytes: 18183
    num_examples: 31
  - name: validation
    num_bytes: 9499
    num_examples: 16
  download_size: 0
  dataset_size: 55340
- config_name: implicatures
  features:
  - name: idx
    dtype: int32
  - name: inputs
    dtype: string
  - name: targets
    sequence: string
  - name: multiple_choice_targets
    sequence: string
  - name: multiple_choice_scores
    sequence: int32
  splits:
  - name: default
    num_bytes: 91892
    num_examples: 492
  - name: train
    num_bytes: 73589
    num_examples: 394
  - name: validation
    num_bytes: 18329
    num_examples: 98
  download_size: 0
  dataset_size: 183810
- config_name: implicit_relations
  features:
  - name: idx
    dtype: int32
  - name: inputs
    dtype: string
  - name: targets
    sequence: string
  - name: multiple_choice_targets
    sequence: string
  - name: multiple_choice_scores
    sequence: int32
  splits:
  - name: default
    num_bytes: 80011
    num_examples: 85
  - name: train
    num_bytes: 64592
    num_examples: 68
  - name: validation
    num_bytes: 15445
    num_examples: 17
  download_size: 0
  dataset_size: 160048
- config_name: intent_recognition
  features:
  - name: idx
    dtype: int32
  - name: inputs
    dtype: string
  - name: targets
    sequence: string
  - name: multiple_choice_targets
    sequence: string
  - name: multiple_choice_scores
    sequence: int32
  splits:
  - name: default
    num_bytes: 323089
    num_examples: 693
  - name: train
    num_bytes: 258444
    num_examples: 555
  - name: validation
    num_bytes: 64670
    num_examples: 138
  download_size: 0
  dataset_size: 646203
- config_name: international_phonetic_alphabet_nli
  features:
  - name: idx
    dtype: int32
  - name: inputs
    dtype: string
  - name: targets
    sequence: string
  - name: multiple_choice_targets
    sequence: string
  - name: multiple_choice_scores
    sequence: int32
  splits:
  - name: default
    num_bytes: 79408
    num_examples: 126
  - name: train
    num_bytes: 63363
    num_examples: 101
  - name: validation
    num_bytes: 16070
    num_examples: 25
  download_size: 0
  dataset_size: 158841
- config_name: international_phonetic_alphabet_transliterate
  features:
  - name: idx
    dtype: int32
  - name: inputs
    dtype: string
  - name: targets
    sequence: string
  - name: multiple_choice_targets
    sequence: string
  - name: multiple_choice_scores
    sequence: int32
  splits:
  - name: default
    num_bytes: 276092
    num_examples: 1003
  - name: train
    num_bytes: 220913
    num_examples: 803
  - name: validation
    num_bytes: 55207
    num_examples: 200
  download_size: 0
  dataset_size: 552212
- config_name: intersect_geometry
  features:
  - name: idx
    dtype: int32
  - name: inputs
    dtype: string
  - name: targets
    sequence: string
  - name: multiple_choice_targets
    sequence: string
  - name: multiple_choice_scores
    sequence: int32
  splits:
  - name: default
    num_bytes: 212987847
    num_examples: 249999
  - name: train
    num_bytes: 170383378
    num_examples: 200000
  - name: validation
    num_bytes: 42604469
    num_examples: 49999
  download_size: 0
  dataset_size: 425975694
- config_name: irony_identification
  features:
  - name: idx
    dtype: int32
  - name: inputs
    dtype: string
  - name: targets
    sequence: string
  - name: multiple_choice_targets
    sequence: string
  - name: multiple_choice_scores
    sequence: int32
  splits:
  - name: default
    num_bytes: 28240
    num_examples: 99
  - name: train
    num_bytes: 22972
    num_examples: 80
  - name: validation
    num_bytes: 5292
    num_examples: 19
  download_size: 0
  dataset_size: 56504
- config_name: kanji_ascii
  features:
  - name: idx
    dtype: int32
  - name: inputs
    dtype: string
  - name: targets
    sequence: string
  - name: multiple_choice_targets
    sequence: string
  - name: multiple_choice_scores
    sequence: int32
  splits:
  - name: default
    num_bytes: 367225
    num_examples: 1092
  - name: train
    num_bytes: 294162
    num_examples: 875
  - name: validation
    num_bytes: 73089
    num_examples: 217
  download_size: 0
  dataset_size: 734476
- config_name: kannada
  features:
  - name: idx
    dtype: int32
  - name: inputs
    dtype: string
  - name: targets
    sequence: string
  - name: multiple_choice_targets
    sequence: string
  - name: multiple_choice_scores
    sequence: int32
  splits:
  - name: default
    num_bytes: 140859
    num_examples: 316
  - name: train
    num_bytes: 112047
    num_examples: 253
  - name: validation
    num_bytes: 28836
    num_examples: 63
  download_size: 0
  dataset_size: 281742
- config_name: key_value_maps
  features:
  - name: idx
    dtype: int32
  - name: inputs
    dtype: string
  - name: targets
    sequence: string
  - name: multiple_choice_targets
    sequence: string
  - name: multiple_choice_scores
    sequence: int32
  splits:
  - name: default
    num_bytes: 105199
    num_examples: 101
  - name: train
    num_bytes: 84371
    num_examples: 80
  - name: validation
    num_bytes: 20852
    num_examples: 21
  download_size: 0
  dataset_size: 210422
- config_name: known_unknowns
  features:
  - name: idx
    dtype: int32
  - name: inputs
    dtype: string
  - name: targets
    sequence: string
  - name: multiple_choice_targets
    sequence: string
  - name: multiple_choice_scores
    sequence: int32
  splits:
  - name: default
    num_bytes: 8002
    num_examples: 46
  - name: train
    num_bytes: 5166
    num_examples: 30
  - name: validation
    num_bytes: 2860
    num_examples: 16
  download_size: 0
  dataset_size: 16028
- config_name: language_games
  features:
  - name: idx
    dtype: int32
  - name: inputs
    dtype: string
  - name: targets
    sequence: string
  - name: multiple_choice_targets
    sequence: string
  - name: multiple_choice_scores
    sequence: int32
  splits:
  - name: default
    num_bytes: 979913
    num_examples: 2128
  - name: train
    num_bytes: 783352
    num_examples: 1704
  - name: validation
    num_bytes: 196589
    num_examples: 424
  download_size: 0
  dataset_size: 1959854
- config_name: language_identification
  features:
  - name: idx
    dtype: int32
  - name: inputs
    dtype: string
  - name: targets
    sequence: string
  - name: multiple_choice_targets
    sequence: string
  - name: multiple_choice_scores
    sequence: int32
  splits:
  - name: default
    num_bytes: 7391247
    num_examples: 10000
  - name: train
    num_bytes: 5920832
    num_examples: 8000
  - name: validation
    num_bytes: 1470439
    num_examples: 2000
  download_size: 0
  dataset_size: 14782518
- config_name: linguistic_mappings
  features:
  - name: idx
    dtype: int32
  - name: inputs
    dtype: string
  - name: targets
    sequence: string
  - name: multiple_choice_targets
    sequence: string
  - name: multiple_choice_scores
    sequence: int32
  splits:
  - name: default
    num_bytes: 1327183
    num_examples: 15527
  - name: train
    num_bytes: 1061698
    num_examples: 12426
  - name: validation
    num_bytes: 265514
    num_examples: 3101
  download_size: 0
  dataset_size: 2654395
- config_name: linguistics_puzzles
  features:
  - name: idx
    dtype: int32
  - name: inputs
    dtype: string
  - name: targets
    sequence: string
  - name: multiple_choice_targets
    sequence: string
  - name: multiple_choice_scores
    sequence: int32
  splits:
  - name: default
    num_bytes: 1746302
    num_examples: 2000
  - name: train
    num_bytes: 1398341
    num_examples: 1600
  - name: validation
    num_bytes: 347989
    num_examples: 400
  download_size: 0
  dataset_size: 3492632
- config_name: list_functions
  features:
  - name: idx
    dtype: int32
  - name: inputs
    dtype: string
  - name: targets
    sequence: string
  - name: multiple_choice_targets
    sequence: string
  - name: multiple_choice_scores
    sequence: int32
  splits:
  - name: default
    num_bytes: 2679536
    num_examples: 10750
  - name: train
    num_bytes: 2162181
    num_examples: 8700
  - name: validation
    num_bytes: 517356
    num_examples: 2050
  download_size: 0
  dataset_size: 5359073
- config_name: logic_grid_puzzle
  features:
  - name: idx
    dtype: int32
  - name: inputs
    dtype: string
  - name: targets
    sequence: string
  - name: multiple_choice_targets
    sequence: string
  - name: multiple_choice_scores
    sequence: int32
  splits:
  - name: default
    num_bytes: 1456816
    num_examples: 1000
  - name: train
    num_bytes: 1160620
    num_examples: 800
  - name: validation
    num_bytes: 296220
    num_examples: 200
  download_size: 0
  dataset_size: 2913656
- config_name: logical_args
  features:
  - name: idx
    dtype: int32
  - name: inputs
    dtype: string
  - name: targets
    sequence: string
  - name: multiple_choice_targets
    sequence: string
  - name: multiple_choice_scores
    sequence: int32
  splits:
  - name: default
    num_bytes: 43630
    num_examples: 32
  - name: train
    num_bytes: 21108
    num_examples: 16
  - name: validation
    num_bytes: 22546
    num_examples: 16
  download_size: 0
  dataset_size: 87284
- config_name: logical_deduction
  features:
  - name: idx
    dtype: int32
  - name: inputs
    dtype: string
  - name: targets
    sequence: string
  - name: multiple_choice_targets
    sequence: string
  - name: multiple_choice_scores
    sequence: int32
  splits:
  - name: default
    num_bytes: 1057966
    num_examples: 1500
  - name: train
    num_bytes: 842792
    num_examples: 1200
  - name: validation
    num_bytes: 215198
    num_examples: 300
  download_size: 0
  dataset_size: 2115956
- config_name: logical_fallacy_detection
  features:
  - name: idx
    dtype: int32
  - name: inputs
    dtype: string
  - name: targets
    sequence: string
  - name: multiple_choice_targets
    sequence: string
  - name: multiple_choice_scores
    sequence: int32
  splits:
  - name: default
    num_bytes: 721360
    num_examples: 2800
  - name: train
    num_bytes: 577159
    num_examples: 2240
  - name: validation
    num_bytes: 144225
    num_examples: 560
  download_size: 0
  dataset_size: 1442744
- config_name: logical_sequence
  features:
  - name: idx
    dtype: int32
  - name: inputs
    dtype: string
  - name: targets
    sequence: string
  - name: multiple_choice_targets
    sequence: string
  - name: multiple_choice_scores
    sequence: int32
  splits:
  - name: default
    num_bytes: 22771
    num_examples: 39
  - name: train
    num_bytes: 12687
    num_examples: 23
  - name: validation
    num_bytes: 10108
    num_examples: 16
  download_size: 0
  dataset_size: 45566
- config_name: mathematical_induction
  features:
  - name: idx
    dtype: int32
  - name: inputs
    dtype: string
  - name: targets
    sequence: string
  - name: multiple_choice_targets
    sequence: string
  - name: multiple_choice_scores
    sequence: int32
  splits:
  - name: default
    num_bytes: 19069
    num_examples: 69
  - name: train
    num_bytes: 15028
    num_examples: 53
  - name: validation
    num_bytes: 4065
    num_examples: 16
  download_size: 0
  dataset_size: 38162
- config_name: matrixshapes
  features:
  - name: idx
    dtype: int32
  - name: inputs
    dtype: string
  - name: targets
    sequence: string
  - name: multiple_choice_targets
    sequence: string
  - name: multiple_choice_scores
    sequence: int32
  splits:
  - name: default
    num_bytes: 1131160
    num_examples: 4462
  - name: train
    num_bytes: 906536
    num_examples: 3570
  - name: validation
    num_bytes: 224653
    num_examples: 892
  download_size: 0
  dataset_size: 2262349
- config_name: metaphor_boolean
  features:
  - name: idx
    dtype: int32
  - name: inputs
    dtype: string
  - name: targets
    sequence: string
  - name: multiple_choice_targets
    sequence: string
  - name: multiple_choice_scores
    sequence: int32
  splits:
  - name: default
    num_bytes: 214127
    num_examples: 680
  - name: train
    num_bytes: 170993
    num_examples: 544
  - name: validation
    num_bytes: 43158
    num_examples: 136
  download_size: 0
  dataset_size: 428278
- config_name: metaphor_understanding
  features:
  - name: idx
    dtype: int32
  - name: inputs
    dtype: string
  - name: targets
    sequence: string
  - name: multiple_choice_targets
    sequence: string
  - name: multiple_choice_scores
    sequence: int32
  splits:
  - name: default
    num_bytes: 201033
    num_examples: 234
  - name: train
    num_bytes: 162243
    num_examples: 188
  - name: validation
    num_bytes: 38814
    num_examples: 46
  download_size: 0
  dataset_size: 402090
- config_name: minute_mysteries_qa
  features:
  - name: idx
    dtype: int32
  - name: inputs
    dtype: string
  - name: targets
    sequence: string
  - name: multiple_choice_targets
    sequence: string
  - name: multiple_choice_scores
    sequence: int32
  splits:
  - name: default
    num_bytes: 3245380
    num_examples: 477
  - name: train
    num_bytes: 2623861
    num_examples: 383
  - name: validation
    num_bytes: 621544
    num_examples: 94
  download_size: 0
  dataset_size: 6490785
- config_name: misconceptions
  features:
  - name: idx
    dtype: int32
  - name: inputs
    dtype: string
  - name: targets
    sequence: string
  - name: multiple_choice_targets
    sequence: string
  - name: multiple_choice_scores
    sequence: int32
  splits:
  - name: default
    num_bytes: 45923
    num_examples: 219
  - name: train
    num_bytes: 37336
    num_examples: 176
  - name: validation
    num_bytes: 8611
    num_examples: 43
  download_size: 0
  dataset_size: 91870
- config_name: misconceptions_russian
  features:
  - name: idx
    dtype: int32
  - name: inputs
    dtype: string
  - name: targets
    sequence: string
  - name: multiple_choice_targets
    sequence: string
  - name: multiple_choice_scores
    sequence: int32
  splits:
  - name: default
    num_bytes: 17035
    num_examples: 49
  - name: train
    num_bytes: 11008
    num_examples: 33
  - name: validation
    num_bytes: 6051
    num_examples: 16
  download_size: 0
  dataset_size: 34094
- config_name: mnist_ascii
  features:
  - name: idx
    dtype: int32
  - name: inputs
    dtype: string
  - name: targets
    sequence: string
  - name: multiple_choice_targets
    sequence: string
  - name: multiple_choice_scores
    sequence: int32
  splits:
  - name: default
    num_bytes: 61836204
    num_examples: 69984
  - name: train
    num_bytes: 49497056
    num_examples: 55988
  - name: validation
    num_bytes: 12339173
    num_examples: 13996
  download_size: 0
  dataset_size: 123672433
- config_name: modified_arithmetic
  features:
  - name: idx
    dtype: int32
  - name: inputs
    dtype: string
  - name: targets
    sequence: string
  - name: multiple_choice_targets
    sequence: string
  - name: multiple_choice_scores
    sequence: int32
  splits:
  - name: default
    num_bytes: 1221771
    num_examples: 6000
  - name: train
    num_bytes: 977487
    num_examples: 4800
  - name: validation
    num_bytes: 244312
    num_examples: 1200
  download_size: 0
  dataset_size: 2443570
- config_name: moral_permissibility
  features:
  - name: idx
    dtype: int32
  - name: inputs
    dtype: string
  - name: targets
    sequence: string
  - name: multiple_choice_targets
    sequence: string
  - name: multiple_choice_scores
    sequence: int32
  splits:
  - name: default
    num_bytes: 162221
    num_examples: 342
  - name: train
    num_bytes: 128918
    num_examples: 274
  - name: validation
    num_bytes: 33328
    num_examples: 68
  download_size: 0
  dataset_size: 324467
- config_name: movie_dialog_same_or_different
  features:
  - name: idx
    dtype: int32
  - name: inputs
    dtype: string
  - name: targets
    sequence: string
  - name: multiple_choice_targets
    sequence: string
  - name: multiple_choice_scores
    sequence: int32
  splits:
  - name: default
    num_bytes: 28664867
    num_examples: 50000
  - name: train
    num_bytes: 22904157
    num_examples: 40000
  - name: validation
    num_bytes: 5760710
    num_examples: 10000
  download_size: 0
  dataset_size: 57329734
- config_name: movie_recommendation
  features:
  - name: idx
    dtype: int32
  - name: inputs
    dtype: string
  - name: targets
    sequence: string
  - name: multiple_choice_targets
    sequence: string
  - name: multiple_choice_scores
    sequence: int32
  splits:
  - name: default
    num_bytes: 173894
    num_examples: 500
  - name: train
    num_bytes: 139210
    num_examples: 400
  - name: validation
    num_bytes: 34708
    num_examples: 100
  download_size: 0
  dataset_size: 347812
- config_name: mult_data_wrangling
  features:
  - name: idx
    dtype: int32
  - name: inputs
    dtype: string
  - name: targets
    sequence: string
  - name: multiple_choice_targets
    sequence: string
  - name: multiple_choice_scores
    sequence: int32
  splits:
  - name: default
    num_bytes: 626432
    num_examples: 7854
  - name: train
    num_bytes: 508664
    num_examples: 6380
  - name: validation
    num_bytes: 117797
    num_examples: 1474
  download_size: 0
  dataset_size: 1252893
- config_name: multiemo
  features:
  - name: idx
    dtype: int32
  - name: inputs
    dtype: string
  - name: targets
    sequence: string
  - name: multiple_choice_targets
    sequence: string
  - name: multiple_choice_scores
    sequence: int32
  splits:
  - name: default
    num_bytes: 651075683
    num_examples: 1437281
  - name: train
    num_bytes: 520893617
    num_examples: 1149873
  - name: validation
    num_bytes: 130182066
    num_examples: 287408
  download_size: 0
  dataset_size: 1302151366
- config_name: natural_instructions
  features:
  - name: idx
    dtype: int32
  - name: inputs
    dtype: string
  - name: targets
    sequence: string
  - name: multiple_choice_targets
    sequence: string
  - name: multiple_choice_scores
    sequence: int32
  splits:
  - name: default
    num_bytes: 355963087
    num_examples: 193250
  - name: train
    num_bytes: 284939871
    num_examples: 154615
  - name: validation
    num_bytes: 71023216
    num_examples: 38635
  download_size: 0
  dataset_size: 711926174
- config_name: navigate
  features:
  - name: idx
    dtype: int32
  - name: inputs
    dtype: string
  - name: targets
    sequence: string
  - name: multiple_choice_targets
    sequence: string
  - name: multiple_choice_scores
    sequence: int32
  splits:
  - name: default
    num_bytes: 226212
    num_examples: 1000
  - name: train
    num_bytes: 181282
    num_examples: 800
  - name: validation
    num_bytes: 44954
    num_examples: 200
  download_size: 0
  dataset_size: 452448
- config_name: nonsense_words_grammar
  features:
  - name: idx
    dtype: int32
  - name: inputs
    dtype: string
  - name: targets
    sequence: string
  - name: multiple_choice_targets
    sequence: string
  - name: multiple_choice_scores
    sequence: int32
  splits:
  - name: default
    num_bytes: 11164
    num_examples: 50
  - name: train
    num_bytes: 7632
    num_examples: 34
  - name: validation
    num_bytes: 3556
    num_examples: 16
  download_size: 0
  dataset_size: 22352
- config_name: novel_concepts
  features:
  - name: idx
    dtype: int32
  - name: inputs
    dtype: string
  - name: targets
    sequence: string
  - name: multiple_choice_targets
    sequence: string
  - name: multiple_choice_scores
    sequence: int32
  splits:
  - name: default
    num_bytes: 16115
    num_examples: 32
  - name: train
    num_bytes: 8165
    num_examples: 16
  - name: validation
    num_bytes: 7974
    num_examples: 16
  download_size: 0
  dataset_size: 32254
- config_name: object_counting
  features:
  - name: idx
    dtype: int32
  - name: inputs
    dtype: string
  - name: targets
    sequence: string
  - name: multiple_choice_targets
    sequence: string
  - name: multiple_choice_scores
    sequence: int32
  splits:
  - name: default
    num_bytes: 149708
    num_examples: 1000
  - name: train
    num_bytes: 119737
    num_examples: 800
  - name: validation
    num_bytes: 29999
    num_examples: 200
  download_size: 0
  dataset_size: 299444
- config_name: odd_one_out
  features:
  - name: idx
    dtype: int32
  - name: inputs
    dtype: string
  - name: targets
    sequence: string
  - name: multiple_choice_targets
    sequence: string
  - name: multiple_choice_scores
    sequence: int32
  splits:
  - name: default
    num_bytes: 13932
    num_examples: 86
  - name: train
    num_bytes: 11293
    num_examples: 69
  - name: validation
    num_bytes: 2664
    num_examples: 17
  download_size: 0
  dataset_size: 27889
- config_name: operators
  features:
  - name: idx
    dtype: int32
  - name: inputs
    dtype: string
  - name: targets
    sequence: string
  - name: multiple_choice_targets
    sequence: string
  - name: multiple_choice_scores
    sequence: int32
  splits:
  - name: default
    num_bytes: 32490
    num_examples: 210
  - name: train
    num_bytes: 25986
    num_examples: 168
  - name: validation
    num_bytes: 6532
    num_examples: 42
  download_size: 0
  dataset_size: 65008
- config_name: paragraph_segmentation
  features:
  - name: idx
    dtype: int32
  - name: inputs
    dtype: string
  - name: targets
    sequence: string
  - name: multiple_choice_targets
    sequence: string
  - name: multiple_choice_scores
    sequence: int32
  splits:
  - name: default
    num_bytes: 56847660
    num_examples: 9000
  - name: train
    num_bytes: 45675248
    num_examples: 7200
  - name: validation
    num_bytes: 11172440
    num_examples: 1800
  download_size: 0
  dataset_size: 113695348
- config_name: parsinlu_qa
  features:
  - name: idx
    dtype: int32
  - name: inputs
    dtype: string
  - name: targets
    sequence: string
  - name: multiple_choice_targets
    sequence: string
  - name: multiple_choice_scores
    sequence: int32
  splits:
  - name: default
    num_bytes: 456870
    num_examples: 1050
  - name: train
    num_bytes: 367126
    num_examples: 840
  - name: validation
    num_bytes: 89768
    num_examples: 210
  download_size: 0
  dataset_size: 913764
- config_name: parsinlu_reading_comprehension
  features:
  - name: idx
    dtype: int32
  - name: inputs
    dtype: string
  - name: targets
    sequence: string
  - name: multiple_choice_targets
    sequence: string
  - name: multiple_choice_scores
    sequence: int32
  splits:
  - name: default
    num_bytes: 573891
    num_examples: 518
  - name: train
    num_bytes: 455908
    num_examples: 415
  - name: validation
    num_bytes: 118011
    num_examples: 103
  download_size: 0
  dataset_size: 1147810
- config_name: penguins_in_a_table
  features:
  - name: idx
    dtype: int32
  - name: inputs
    dtype: string
  - name: targets
    sequence: string
  - name: multiple_choice_targets
    sequence: string
  - name: multiple_choice_scores
    sequence: int32
  splits:
  - name: default
    num_bytes: 76121
    num_examples: 149
  - name: train
    num_bytes: 61435
    num_examples: 120
  - name: validation
    num_bytes: 14711
    num_examples: 29
  download_size: 0
  dataset_size: 152267
- config_name: periodic_elements
  features:
  - name: idx
    dtype: int32
  - name: inputs
    dtype: string
  - name: targets
    sequence: string
  - name: multiple_choice_targets
    sequence: string
  - name: multiple_choice_scores
    sequence: int32
  splits:
  - name: default
    num_bytes: 287051
    num_examples: 654
  - name: train
    num_bytes: 230973
    num_examples: 524
  - name: validation
    num_bytes: 56104
    num_examples: 130
  download_size: 0
  dataset_size: 574128
- config_name: persian_idioms
  features:
  - name: idx
    dtype: int32
  - name: inputs
    dtype: string
  - name: targets
    sequence: string
  - name: multiple_choice_targets
    sequence: string
  - name: multiple_choice_scores
    sequence: int32
  splits:
  - name: default
    num_bytes: 28658
    num_examples: 66
  - name: train
    num_bytes: 21740
    num_examples: 50
  - name: validation
    num_bytes: 6942
    num_examples: 16
  download_size: 0
  dataset_size: 57340
- config_name: phrase_relatedness
  features:
  - name: idx
    dtype: int32
  - name: inputs
    dtype: string
  - name: targets
    sequence: string
  - name: multiple_choice_targets
    sequence: string
  - name: multiple_choice_scores
    sequence: int32
  splits:
  - name: default
    num_bytes: 30277
    num_examples: 100
  - name: train
    num_bytes: 23847
    num_examples: 80
  - name: validation
    num_bytes: 6454
    num_examples: 20
  download_size: 0
  dataset_size: 60578
- config_name: physical_intuition
  features:
  - name: idx
    dtype: int32
  - name: inputs
    dtype: string
  - name: targets
    sequence: string
  - name: multiple_choice_targets
    sequence: string
  - name: multiple_choice_scores
    sequence: int32
  splits:
  - name: default
    num_bytes: 23810
    num_examples: 81
  - name: train
    num_bytes: 19373
    num_examples: 65
  - name: validation
    num_bytes: 4461
    num_examples: 16
  download_size: 0
  dataset_size: 47644
- config_name: physics
  features:
  - name: idx
    dtype: int32
  - name: inputs
    dtype: string
  - name: targets
    sequence: string
  - name: multiple_choice_targets
    sequence: string
  - name: multiple_choice_scores
    sequence: int32
  splits:
  - name: default
    num_bytes: 120407
    num_examples: 229
  - name: train
    num_bytes: 96261
    num_examples: 184
  - name: validation
    num_bytes: 24170
    num_examples: 45
  download_size: 0
  dataset_size: 240838
- config_name: physics_questions
  features:
  - name: idx
    dtype: int32
  - name: inputs
    dtype: string
  - name: targets
    sequence: string
  - name: multiple_choice_targets
    sequence: string
  - name: multiple_choice_scores
    sequence: int32
  splits:
  - name: default
    num_bytes: 18407
    num_examples: 54
  - name: train
    num_bytes: 13435
    num_examples: 38
  - name: validation
    num_bytes: 5000
    num_examples: 16
  download_size: 0
  dataset_size: 36842
- config_name: play_dialog_same_or_different
  features:
  - name: idx
    dtype: int32
  - name: inputs
    dtype: string
  - name: targets
    sequence: string
  - name: multiple_choice_targets
    sequence: string
  - name: multiple_choice_scores
    sequence: int32
  splits:
  - name: default
    num_bytes: 3143716
    num_examples: 3264
  - name: train
    num_bytes: 2517056
    num_examples: 2612
  - name: validation
    num_bytes: 626685
    num_examples: 652
  download_size: 0
  dataset_size: 6287457
- config_name: polish_sequence_labeling
  features:
  - name: idx
    dtype: int32
  - name: inputs
    dtype: string
  - name: targets
    sequence: string
  - name: multiple_choice_targets
    sequence: string
  - name: multiple_choice_scores
    sequence: int32
  splits:
  - name: default
    num_bytes: 18082770
    num_examples: 12812
  - name: train
    num_bytes: 14472058
    num_examples: 10250
  - name: validation
    num_bytes: 3610741
    num_examples: 2562
  download_size: 0
  dataset_size: 36165569
- config_name: presuppositions_as_nli
  features:
  - name: idx
    dtype: int32
  - name: inputs
    dtype: string
  - name: targets
    sequence: string
  - name: multiple_choice_targets
    sequence: string
  - name: multiple_choice_scores
    sequence: int32
  splits:
  - name: default
    num_bytes: 502914
    num_examples: 735
  - name: train
    num_bytes: 401080
    num_examples: 588
  - name: validation
    num_bytes: 101860
    num_examples: 147
  download_size: 0
  dataset_size: 1005854
- config_name: qa_wikidata
  features:
  - name: idx
    dtype: int32
  - name: inputs
    dtype: string
  - name: targets
    sequence: string
  - name: multiple_choice_targets
    sequence: string
  - name: multiple_choice_scores
    sequence: int32
  splits:
  - name: default
    num_bytes: 1421667
    num_examples: 20321
  - name: train
    num_bytes: 1137007
    num_examples: 16257
  - name: validation
    num_bytes: 284660
    num_examples: 4064
  download_size: 0
  dataset_size: 2843334
- config_name: question_selection
  features:
  - name: idx
    dtype: int32
  - name: inputs
    dtype: string
  - name: targets
    sequence: string
  - name: multiple_choice_targets
    sequence: string
  - name: multiple_choice_scores
    sequence: int32
  splits:
  - name: default
    num_bytes: 2487986
    num_examples: 1582
  - name: train
    num_bytes: 1990739
    num_examples: 1266
  - name: validation
    num_bytes: 497272
    num_examples: 316
  download_size: 0
  dataset_size: 4975997
- config_name: real_or_fake_text
  features:
  - name: idx
    dtype: int32
  - name: inputs
    dtype: string
  - name: targets
    sequence: string
  - name: multiple_choice_targets
    sequence: string
  - name: multiple_choice_scores
    sequence: int32
  splits:
  - name: default
    num_bytes: 53684101
    num_examples: 15088
  - name: train
    num_bytes: 42896484
    num_examples: 12072
  - name: validation
    num_bytes: 10787642
    num_examples: 3016
  download_size: 0
  dataset_size: 107368227
- config_name: reasoning_about_colored_objects
  features:
  - name: idx
    dtype: int32
  - name: inputs
    dtype: string
  - name: targets
    sequence: string
  - name: multiple_choice_targets
    sequence: string
  - name: multiple_choice_scores
    sequence: int32
  splits:
  - name: default
    num_bytes: 912440
    num_examples: 2000
  - name: train
    num_bytes: 733608
    num_examples: 1600
  - name: validation
    num_bytes: 178857
    num_examples: 400
  download_size: 0
  dataset_size: 1824905
- config_name: repeat_copy_logic
  features:
  - name: idx
    dtype: int32
  - name: inputs
    dtype: string
  - name: targets
    sequence: string
  - name: multiple_choice_targets
    sequence: string
  - name: multiple_choice_scores
    sequence: int32
  splits:
  - name: default
    num_bytes: 6710
    num_examples: 32
  - name: train
    num_bytes: 3357
    num_examples: 16
  - name: validation
    num_bytes: 3381
    num_examples: 16
  download_size: 0
  dataset_size: 13448
- config_name: rephrase
  features:
  - name: idx
    dtype: int32
  - name: inputs
    dtype: string
  - name: targets
    sequence: string
  - name: multiple_choice_targets
    sequence: string
  - name: multiple_choice_scores
    sequence: int32
  splits:
  - name: default
    num_bytes: 34260
    num_examples: 78
  - name: train
    num_bytes: 27396
    num_examples: 62
  - name: validation
    num_bytes: 6892
    num_examples: 16
  download_size: 0
  dataset_size: 68548
- config_name: riddle_sense
  features:
  - name: idx
    dtype: int32
  - name: inputs
    dtype: string
  - name: targets
    sequence: string
  - name: multiple_choice_targets
    sequence: string
  - name: multiple_choice_scores
    sequence: int32
  splits:
  - name: default
    num_bytes: 15569
    num_examples: 49
  - name: train
    num_bytes: 10791
    num_examples: 33
  - name: validation
    num_bytes: 4802
    num_examples: 16
  download_size: 0
  dataset_size: 31162
- config_name: ruin_names
  features:
  - name: idx
    dtype: int32
  - name: inputs
    dtype: string
  - name: targets
    sequence: string
  - name: multiple_choice_targets
    sequence: string
  - name: multiple_choice_scores
    sequence: int32
  splits:
  - name: default
    num_bytes: 144391
    num_examples: 448
  - name: train
    num_bytes: 115420
    num_examples: 359
  - name: validation
    num_bytes: 28997
    num_examples: 89
  download_size: 0
  dataset_size: 288808
- config_name: salient_translation_error_detection
  features:
  - name: idx
    dtype: int32
  - name: inputs
    dtype: string
  - name: targets
    sequence: string
  - name: multiple_choice_targets
    sequence: string
  - name: multiple_choice_scores
    sequence: int32
  splits:
  - name: default
    num_bytes: 1142524
    num_examples: 998
  - name: train
    num_bytes: 913543
    num_examples: 799
  - name: validation
    num_bytes: 229006
    num_examples: 199
  download_size: 0
  dataset_size: 2285073
- config_name: scientific_press_release
  features:
  - name: idx
    dtype: int32
  - name: inputs
    dtype: string
  - name: targets
    sequence: string
  - name: multiple_choice_targets
    sequence: string
  - name: multiple_choice_scores
    sequence: int32
  splits:
  - name: default
    num_bytes: 13725
    num_examples: 50
  - name: train
    num_bytes: 9287
    num_examples: 34
  - name: validation
    num_bytes: 4466
    num_examples: 16
  download_size: 0
  dataset_size: 27478
- config_name: semantic_parsing_in_context_sparc
  features:
  - name: idx
    dtype: int32
  - name: inputs
    dtype: string
  - name: targets
    sequence: string
  - name: multiple_choice_targets
    sequence: string
  - name: multiple_choice_scores
    sequence: int32
  splits:
  - name: default
    num_bytes: 1525025
    num_examples: 1155
  - name: train
    num_bytes: 1248535
    num_examples: 924
  - name: validation
    num_bytes: 276518
    num_examples: 231
  download_size: 0
  dataset_size: 3050078
- config_name: semantic_parsing_spider
  features:
  - name: idx
    dtype: int32
  - name: inputs
    dtype: string
  - name: targets
    sequence: string
  - name: multiple_choice_targets
    sequence: string
  - name: multiple_choice_scores
    sequence: int32
  splits:
  - name: default
    num_bytes: 1265902
    num_examples: 1034
  - name: train
    num_bytes: 973996
    num_examples: 828
  - name: validation
    num_bytes: 291934
    num_examples: 206
  download_size: 0
  dataset_size: 2531832
- config_name: sentence_ambiguity
  features:
  - name: idx
    dtype: int32
  - name: inputs
    dtype: string
  - name: targets
    sequence: string
  - name: multiple_choice_targets
    sequence: string
  - name: multiple_choice_scores
    sequence: int32
  splits:
  - name: default
    num_bytes: 8215
    num_examples: 60
  - name: train
    num_bytes: 6017
    num_examples: 44
  - name: validation
    num_bytes: 2222
    num_examples: 16
  download_size: 0
  dataset_size: 16454
- config_name: similarities_abstraction
  features:
  - name: idx
    dtype: int32
  - name: inputs
    dtype: string
  - name: targets
    sequence: string
  - name: multiple_choice_targets
    sequence: string
  - name: multiple_choice_scores
    sequence: int32
  splits:
  - name: default
    num_bytes: 23490
    num_examples: 76
  - name: train
    num_bytes: 18609
    num_examples: 60
  - name: validation
    num_bytes: 4906
    num_examples: 16
  download_size: 0
  dataset_size: 47005
- config_name: simp_turing_concept
  features:
  - name: idx
    dtype: int32
  - name: inputs
    dtype: string
  - name: targets
    sequence: string
  - name: multiple_choice_targets
    sequence: string
  - name: multiple_choice_scores
    sequence: int32
  splits:
  - name: default
    num_bytes: 1018473
    num_examples: 6390
  - name: train
    num_bytes: 813887
    num_examples: 5112
  - name: validation
    num_bytes: 204614
    num_examples: 1278
  download_size: 0
  dataset_size: 2036974
- config_name: simple_arithmetic_json
  features:
  - name: idx
    dtype: int32
  - name: inputs
    dtype: string
  - name: targets
    sequence: string
  - name: multiple_choice_targets
    sequence: string
  - name: multiple_choice_scores
    sequence: int32
  splits:
  - name: default
    num_bytes: 1177
    num_examples: 30
  - name: train
    num_bytes: 570
    num_examples: 14
  - name: validation
    num_bytes: 635
    num_examples: 16
  download_size: 0
  dataset_size: 2382
- config_name: simple_arithmetic_json_multiple_choice
  features:
  - name: idx
    dtype: int32
  - name: inputs
    dtype: string
  - name: targets
    sequence: string
  - name: multiple_choice_targets
    sequence: string
  - name: multiple_choice_scores
    sequence: int32
  splits:
  - name: default
    num_bytes: 953
    num_examples: 8
  - name: train
  - name: validation
  download_size: 0
  dataset_size: 953
- config_name: simple_arithmetic_json_subtasks
  features:
  - name: idx
    dtype: int32
  - name: inputs
    dtype: string
  - name: targets
    sequence: string
  - name: multiple_choice_targets
    sequence: string
  - name: multiple_choice_scores
    sequence: int32
  splits:
  - name: default
    num_bytes: 1177
    num_examples: 30
  - name: train
    num_bytes: 601
    num_examples: 15
  - name: validation
    num_bytes: 604
    num_examples: 15
  download_size: 0
  dataset_size: 2382
- config_name: simple_arithmetic_multiple_targets_json
  features:
  - name: idx
    dtype: int32
  - name: inputs
    dtype: string
  - name: targets
    sequence: string
  - name: multiple_choice_targets
    sequence: string
  - name: multiple_choice_scores
    sequence: int32
  splits:
  - name: default
    num_bytes: 444
    num_examples: 10
  - name: train
  - name: validation
  download_size: 0
  dataset_size: 444
- config_name: simple_ethical_questions
  features:
  - name: idx
    dtype: int32
  - name: inputs
    dtype: string
  - name: targets
    sequence: string
  - name: multiple_choice_targets
    sequence: string
  - name: multiple_choice_scores
    sequence: int32
  splits:
  - name: default
    num_bytes: 76615
    num_examples: 115
  - name: train
    num_bytes: 60357
    num_examples: 92
  - name: validation
    num_bytes: 16282
    num_examples: 23
  download_size: 0
  dataset_size: 153254
- config_name: simple_text_editing
  features:
  - name: idx
    dtype: int32
  - name: inputs
    dtype: string
  - name: targets
    sequence: string
  - name: multiple_choice_targets
    sequence: string
  - name: multiple_choice_scores
    sequence: int32
  splits:
  - name: default
    num_bytes: 27899
    num_examples: 47
  - name: train
    num_bytes: 18501
    num_examples: 31
  - name: validation
    num_bytes: 9426
    num_examples: 16
  download_size: 0
  dataset_size: 55826
- config_name: snarks
  features:
  - name: idx
    dtype: int32
  - name: inputs
    dtype: string
  - name: targets
    sequence: string
  - name: multiple_choice_targets
    sequence: string
  - name: multiple_choice_scores
    sequence: int32
  splits:
  - name: default
    num_bytes: 45810
    num_examples: 181
  - name: train
    num_bytes: 37069
    num_examples: 145
  - name: validation
    num_bytes: 8766
    num_examples: 36
  download_size: 0
  dataset_size: 91645
- config_name: social_iqa
  features:
  - name: idx
    dtype: int32
  - name: inputs
    dtype: string
  - name: targets
    sequence: string
  - name: multiple_choice_targets
    sequence: string
  - name: multiple_choice_scores
    sequence: int32
  splits:
  - name: default
    num_bytes: 644154
    num_examples: 1935
  - name: train
    num_bytes: 516485
    num_examples: 1548
  - name: validation
    num_bytes: 127694
    num_examples: 387
  download_size: 0
  dataset_size: 1288333
- config_name: social_support
  features:
  - name: idx
    dtype: int32
  - name: inputs
    dtype: string
  - name: targets
    sequence: string
  - name: multiple_choice_targets
    sequence: string
  - name: multiple_choice_scores
    sequence: int32
  splits:
  - name: default
    num_bytes: 367179
    num_examples: 897
  - name: train
    num_bytes: 295177
    num_examples: 718
  - name: validation
    num_bytes: 72027
    num_examples: 179
  download_size: 0
  dataset_size: 734383
- config_name: sports_understanding
  features:
  - name: idx
    dtype: int32
  - name: inputs
    dtype: string
  - name: targets
    sequence: string
  - name: multiple_choice_targets
    sequence: string
  - name: multiple_choice_scores
    sequence: int32
  splits:
  - name: default
    num_bytes: 227049
    num_examples: 986
  - name: train
    num_bytes: 181649
    num_examples: 789
  - name: validation
    num_bytes: 45425
    num_examples: 197
  download_size: 0
  dataset_size: 454123
- config_name: strange_stories
  features:
  - name: idx
    dtype: int32
  - name: inputs
    dtype: string
  - name: targets
    sequence: string
  - name: multiple_choice_targets
    sequence: string
  - name: multiple_choice_scores
    sequence: int32
  splits:
  - name: default
    num_bytes: 120620
    num_examples: 174
  - name: train
    num_bytes: 98157
    num_examples: 140
  - name: validation
    num_bytes: 22489
    num_examples: 34
  download_size: 0
  dataset_size: 241266
- config_name: strategyqa
  features:
  - name: idx
    dtype: int32
  - name: inputs
    dtype: string
  - name: targets
    sequence: string
  - name: multiple_choice_targets
    sequence: string
  - name: multiple_choice_scores
    sequence: int32
  splits:
  - name: default
    num_bytes: 660851
    num_examples: 2289
  - name: train
    num_bytes: 528381
    num_examples: 1832
  - name: validation
    num_bytes: 132494
    num_examples: 457
  download_size: 0
  dataset_size: 1321726
- config_name: sufficient_information
  features:
  - name: idx
    dtype: int32
  - name: inputs
    dtype: string
  - name: targets
    sequence: string
  - name: multiple_choice_targets
    sequence: string
  - name: multiple_choice_scores
    sequence: int32
  splits:
  - name: default
    num_bytes: 9458
    num_examples: 39
  - name: train
    num_bytes: 5625
    num_examples: 23
  - name: validation
    num_bytes: 3861
    num_examples: 16
  download_size: 0
  dataset_size: 18944
- config_name: suicide_risk
  features:
  - name: idx
    dtype: int32
  - name: inputs
    dtype: string
  - name: targets
    sequence: string
  - name: multiple_choice_targets
    sequence: string
  - name: multiple_choice_scores
    sequence: int32
  splits:
  - name: default
    num_bytes: 38001
    num_examples: 40
  - name: train
    num_bytes: 23106
    num_examples: 24
  - name: validation
    num_bytes: 14919
    num_examples: 16
  download_size: 0
  dataset_size: 76026
- config_name: swahili_english_proverbs
  features:
  - name: idx
    dtype: int32
  - name: inputs
    dtype: string
  - name: targets
    sequence: string
  - name: multiple_choice_targets
    sequence: string
  - name: multiple_choice_scores
    sequence: int32
  splits:
  - name: default
    num_bytes: 90367
    num_examples: 153
  - name: train
    num_bytes: 72569
    num_examples: 123
  - name: validation
    num_bytes: 17822
    num_examples: 30
  download_size: 0
  dataset_size: 180758
- config_name: swedish_to_german_proverbs
  features:
  - name: idx
    dtype: int32
  - name: inputs
    dtype: string
  - name: targets
    sequence: string
  - name: multiple_choice_targets
    sequence: string
  - name: multiple_choice_scores
    sequence: int32
  splits:
  - name: default
    num_bytes: 35273
    num_examples: 72
  - name: train
    num_bytes: 27325
    num_examples: 56
  - name: validation
    num_bytes: 7972
    num_examples: 16
  download_size: 0
  dataset_size: 70570
- config_name: symbol_interpretation
  features:
  - name: idx
    dtype: int32
  - name: inputs
    dtype: string
  - name: targets
    sequence: string
  - name: multiple_choice_targets
    sequence: string
  - name: multiple_choice_scores
    sequence: int32
  splits:
  - name: default
    num_bytes: 1149725
    num_examples: 990
  - name: train
    num_bytes: 927947
    num_examples: 795
  - name: validation
    num_bytes: 221803
    num_examples: 195
  download_size: 0
  dataset_size: 2299475
- config_name: temporal_sequences
  features:
  - name: idx
    dtype: int32
  - name: inputs
    dtype: string
  - name: targets
    sequence: string
  - name: multiple_choice_targets
    sequence: string
  - name: multiple_choice_scores
    sequence: int32
  splits:
  - name: default
    num_bytes: 687735
    num_examples: 1000
  - name: train
    num_bytes: 550332
    num_examples: 800
  - name: validation
    num_bytes: 137427
    num_examples: 200
  download_size: 0
  dataset_size: 1375494
- config_name: tense
  features:
  - name: idx
    dtype: int32
  - name: inputs
    dtype: string
  - name: targets
    sequence: string
  - name: multiple_choice_targets
    sequence: string
  - name: multiple_choice_scores
    sequence: int32
  splits:
  - name: default
    num_bytes: 43946
    num_examples: 286
  - name: train
    num_bytes: 35523
    num_examples: 229
  - name: validation
    num_bytes: 8452
    num_examples: 57
  download_size: 0
  dataset_size: 87921
- config_name: timedial
  features:
  - name: idx
    dtype: int32
  - name: inputs
    dtype: string
  - name: targets
    sequence: string
  - name: multiple_choice_targets
    sequence: string
  - name: multiple_choice_scores
    sequence: int32
  splits:
  - name: default
    num_bytes: 2764478
    num_examples: 2550
  - name: train
    num_bytes: 2218234
    num_examples: 2040
  - name: validation
    num_bytes: 546268
    num_examples: 510
  download_size: 0
  dataset_size: 5528980
- config_name: topical_chat
  features:
  - name: idx
    dtype: int32
  - name: inputs
    dtype: string
  - name: targets
    sequence: string
  - name: multiple_choice_targets
    sequence: string
  - name: multiple_choice_scores
    sequence: int32
  splits:
  - name: default
    num_bytes: 30930629
    num_examples: 22295
  - name: train
    num_bytes: 24829540
    num_examples: 17836
  - name: validation
    num_bytes: 6101090
    num_examples: 4459
  download_size: 0
  dataset_size: 61861259
- config_name: tracking_shuffled_objects
  features:
  - name: idx
    dtype: int32
  - name: inputs
    dtype: string
  - name: targets
    sequence: string
  - name: multiple_choice_targets
    sequence: string
  - name: multiple_choice_scores
    sequence: int32
  splits:
  - name: default
    num_bytes: 2779059
    num_examples: 3750
  - name: train
    num_bytes: 2226511
    num_examples: 3000
  - name: validation
    num_bytes: 552572
    num_examples: 750
  download_size: 0
  dataset_size: 5558142
- config_name: understanding_fables
  features:
  - name: idx
    dtype: int32
  - name: inputs
    dtype: string
  - name: targets
    sequence: string
  - name: multiple_choice_targets
    sequence: string
  - name: multiple_choice_scores
    sequence: int32
  splits:
  - name: default
    num_bytes: 227915
    num_examples: 189
  - name: train
    num_bytes: 181138
    num_examples: 152
  - name: validation
    num_bytes: 46801
    num_examples: 37
  download_size: 0
  dataset_size: 455854
- config_name: undo_permutation
  features:
  - name: idx
    dtype: int32
  - name: inputs
    dtype: string
  - name: targets
    sequence: string
  - name: multiple_choice_targets
    sequence: string
  - name: multiple_choice_scores
    sequence: int32
  splits:
  - name: default
    num_bytes: 196443
    num_examples: 300
  - name: train
    num_bytes: 158827
    num_examples: 240
  - name: validation
    num_bytes: 37641
    num_examples: 60
  download_size: 0
  dataset_size: 392911
- config_name: unit_conversion
  features:
  - name: idx
    dtype: int32
  - name: inputs
    dtype: string
  - name: targets
    sequence: string
  - name: multiple_choice_targets
    sequence: string
  - name: multiple_choice_scores
    sequence: int32
  splits:
  - name: default
    num_bytes: 4040317
    num_examples: 23936
  - name: train
    num_bytes: 3239699
    num_examples: 19151
  - name: validation
    num_bytes: 800619
    num_examples: 4785
  download_size: 0
  dataset_size: 8080635
- config_name: unit_interpretation
  features:
  - name: idx
    dtype: int32
  - name: inputs
    dtype: string
  - name: targets
    sequence: string
  - name: multiple_choice_targets
    sequence: string
  - name: multiple_choice_scores
    sequence: int32
  splits:
  - name: default
    num_bytes: 37463
    num_examples: 100
  - name: train
    num_bytes: 30023
    num_examples: 80
  - name: validation
    num_bytes: 7464
    num_examples: 20
  download_size: 0
  dataset_size: 74950
- config_name: unnatural_in_context_learning
  features:
  - name: idx
    dtype: int32
  - name: inputs
    dtype: string
  - name: targets
    sequence: string
  - name: multiple_choice_targets
    sequence: string
  - name: multiple_choice_scores
    sequence: int32
  splits:
  - name: default
    num_bytes: 4609162
    num_examples: 73420
  - name: train
    num_bytes: 3687332
    num_examples: 58736
  - name: validation
    num_bytes: 921830
    num_examples: 14684
  download_size: 0
  dataset_size: 9218324
- config_name: vitaminc_fact_verification
  features:
  - name: idx
    dtype: int32
  - name: inputs
    dtype: string
  - name: targets
    sequence: string
  - name: multiple_choice_targets
    sequence: string
  - name: multiple_choice_scores
    sequence: int32
  splits:
  - name: default
    num_bytes: 32389297
    num_examples: 54668
  - name: train
    num_bytes: 25911838
    num_examples: 43735
  - name: validation
    num_bytes: 6477483
    num_examples: 10933
  download_size: 0
  dataset_size: 64778618
- config_name: what_is_the_tao
  features:
  - name: idx
    dtype: int32
  - name: inputs
    dtype: string
  - name: targets
    sequence: string
  - name: multiple_choice_targets
    sequence: string
  - name: multiple_choice_scores
    sequence: int32
  splits:
  - name: default
    num_bytes: 13306
    num_examples: 36
  - name: train
    num_bytes: 7467
    num_examples: 20
  - name: validation
    num_bytes: 5863
    num_examples: 16
  download_size: 0
  dataset_size: 26636
- config_name: which_wiki_edit
  features:
  - name: idx
    dtype: int32
  - name: inputs
    dtype: string
  - name: targets
    sequence: string
  - name: multiple_choice_targets
    sequence: string
  - name: multiple_choice_scores
    sequence: int32
  splits:
  - name: default
    num_bytes: 6332065
    num_examples: 571
  - name: train
    num_bytes: 5234181
    num_examples: 457
  - name: validation
    num_bytes: 1097909
    num_examples: 114
  download_size: 0
  dataset_size: 12664155
- config_name: winowhy
  features:
  - name: idx
    dtype: int32
  - name: inputs
    dtype: string
  - name: targets
    sequence: string
  - name: multiple_choice_targets
    sequence: string
  - name: multiple_choice_scores
    sequence: int32
  splits:
  - name: default
    num_bytes: 1003532
    num_examples: 2862
  - name: train
    num_bytes: 801404
    num_examples: 2290
  - name: validation
    num_bytes: 202153
    num_examples: 572
  download_size: 0
  dataset_size: 2007089
- config_name: word_sorting
  features:
  - name: idx
    dtype: int32
  - name: inputs
    dtype: string
  - name: targets
    sequence: string
  - name: multiple_choice_targets
    sequence: string
  - name: multiple_choice_scores
    sequence: int32
  splits:
  - name: default
    num_bytes: 491320
    num_examples: 1900
  - name: train
    num_bytes: 392956
    num_examples: 1520
  - name: validation
    num_bytes: 98392
    num_examples: 380
  download_size: 0
  dataset_size: 982668
- config_name: word_unscrambling
  features:
  - name: idx
    dtype: int32
  - name: inputs
    dtype: string
  - name: targets
    sequence: string
  - name: multiple_choice_targets
    sequence: string
  - name: multiple_choice_scores
    sequence: int32
  splits:
  - name: default
    num_bytes: 883507
    num_examples: 8917
  - name: train
    num_bytes: 706675
    num_examples: 7134
  - name: validation
    num_bytes: 176860
    num_examples: 1783
  download_size: 0
  dataset_size: 1767042
---

# Dataset Card for BIG-bench

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

- **Homepage/Repository:** [https://github.com/google/BIG-bench](https://github.com/google/BIG-bench)
- **Paper:** In progress
- **Leaderboard:**
- **Point of Contact:** [bigbench@googlegroups.com](mailto:bigbench@googlegroups.com)


### Dataset Summary

The Beyond the Imitation Game Benchmark (BIG-bench) is a collaborative benchmark intended to probe large language models and extrapolate their future capabilities. Tasks included in BIG-bench are summarized by keyword [here](https://github.com/google/BIG-bench/blob/main/bigbench/benchmark_tasks/keywords_to_tasks.md), and by task name [here](https://github.com/google/BIG-bench/blob/main/bigbench/benchmark_tasks/README.md). A paper introducing the benchmark, including evaluation results on large language models, is currently in preparation.

### Supported Tasks and Leaderboards

BIG-Bench consists of both json and programmatic tasks.
This implementation in HuggingFace datasets implements

  - 24 BIG-bench Lite tasks

  - 167 BIG-bench json tasks (includes BIG-bench Lite)
   
To study the remaining programmatic tasks, please see the [BIG-bench GitHub repo](https://github.com/google/BIG-bench)

### Languages

Although predominantly English, BIG-bench contains tasks in over 1000 written languages, as well as some synthetic and programming languages. 
See [BIG-bench organized by keywords](https://github.com/google/BIG-bench/blob/main/bigbench/benchmark_tasks/keywords_to_tasks.md). Relevant keywords include `multilingual`, `non-english`, `low-resource-language`, `translation`.

For tasks specifically targeting low-resource languages, see the table below:

Task Name | Languages |
--|--|
Conlang Translation Problems | English, German, Finnish, Abma, Apinayé, Inapuri, Ndebele, Palauan|
Kannada Riddles | Kannada|
Language Identification | 1000 languages |
Swahili English Proverbs | Swahili |
Which Wiki Edit | English, Russian, Spanish, German, French, Turkish, Japanese, Vietnamese, Chinese, Arabic, Norwegian, Tagalog|




## Dataset Structure

### Data Instances

Each dataset contains 5 features. For example an instance from the `emoji_movie` task is:

```
{
  "idx": 0,
  "inputs": "Q: What movie does this emoji describe? 👦👓⚡️\n  choice: harry potter\n. choice: shutter island\n. choice: inglourious basterds\n. choice: die hard\n. choice: moonlight\nA:"
  "targets": ["harry potter"],
  "multiple_choice_targets":["harry potter", "shutter island", "die hard", "inglourious basterds", "moonlight"],
  "multiple_choice_scores": [1, 0, 0, 0, 0]
}
```
      
For tasks that do not have multiple choice targets, the lists are empty.


### Data Fields

Every example has the following fields
  - `idx`: an `int` feature
  - `inputs`: a `string` feature
  - `targets`: a sequence of `string` feature
  - `multiple_choice_targets`: a sequence of `string` features
  - `multiple_choice_scores`: a sequence of `int` features

### Data Splits

Each task has a `default`, `train` and `validation` split.
The split `default` uses all the samples for each task (and it's the same as `all` used in the `bigbench.bbseqio` implementation.)
For standard evaluation on BIG-bench, we recommend using the `default` split, and the `train` and `validation` split is to be used if one wants to train a model on BIG-bench.

## Dataset Creation

BIG-bench tasks were collaboratively submitted through GitHub pull requests. 

Each task went through a review and meta-review process with criteria outlined in the [BIG-bench repository documentation](https://github.com/google/BIG-bench/blob/main/docs/doc.md#submission-review-process).
Each task was required to describe the data source and curation methods on the task README page. 

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

BIG-bench contains a wide range of tasks, some of which are sensitive and should be used with care.

Some tasks are specifically designed to test biases and failures common to large language models, and so may elicit inappropriate or harmful responses.
For a more thorough discussion see the [BIG-bench paper](in progress). 

To view tasks designed to probe pro-social behavior, including alignment, social, racial, gender, religious or political bias; toxicity; inclusion; and other issues please see tasks under the [pro-social behavior keywords](https://github.com/google/BIG-bench/blob/main/bigbench/benchmark_tasks/keywords_to_tasks.md#pro-social-behavior) on the BIG-bench repository.


### Social Impact of Dataset

[More Information Needed]


### Discussion of Biases

[More Information Needed]


### Other Known Limitations

[More Information Needed]


## Additional Information

For a more thorough discussion of all aspects of BIG-bench including dataset creation and evaluations see the BIG-bench repository [https://github.com/google/BIG-bench](https://github.com/google/BIG-bench) and paper []

### Dataset Curators

[More Information Needed]


### Licensing Information

[Apache License 2.0](https://github.com/google/BIG-bench/blob/main/LICENSE)

### Citation Information

To be added soon !

### Contributions
For a full list of contributors to the BIG-bench dataset, see the paper.

Thanks to [@andersjohanandreassen](https://github.com/andersjohanandreassen) and [@ethansdyer](https://github.com/ethansdyer) for adding this dataset to HuggingFace.