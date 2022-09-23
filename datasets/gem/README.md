---
annotations_creators:
- crowdsourced
- found
language_creators:
- crowdsourced
- found
- machine-generated
language:
- cs
- de
- en
- es
- ru
- tr
- vi
license:
- other
multilinguality:
- monolingual
- multilingual
size_categories:
- 100K<n<1M
- 10K<n<100K
- 1K<n<10K
source_datasets:
- extended|other-vision-datasets
- original
task_categories:
- fill-mask
- summarization
- table-to-text
- tabular-to-text
- text-generation
- text2text-generation
task_ids:
- dialogue-modeling
- other-concepts-to-text
- other-intent-to-text
- rdf-to-text
- news-articles-summarization
- text-simplification
- text2text-generation-other-meaning-representation-to-text
paperswithcode_id: gem
pretty_name: GEM
configs:
- common_gen
- cs_restaurants
- dart
- e2e_nlg
- mlsum_de
- mlsum_es
- schema_guided_dialog
- totto
- web_nlg_en
- web_nlg_ru
- wiki_auto_asset_turk
- wiki_lingua_es_en
- wiki_lingua_ru_en
- wiki_lingua_tr_en
- wiki_lingua_vi_en
- xsum
dataset_info:
- config_name: mlsum_de
  features:
  - name: gem_id
    dtype: string
  - name: gem_parent_id
    dtype: string
  - name: text
    dtype: string
  - name: topic
    dtype: string
  - name: url
    dtype: string
  - name: title
    dtype: string
  - name: date
    dtype: string
  - name: target
    dtype: string
  - name: references
    list: string
  splits:
  - name: challenge_test_covid
    num_bytes: 19771285
    num_examples: 5058
  - name: challenge_train_sample
    num_bytes: 1894220
    num_examples: 500
  - name: challenge_validation_sample
    num_bytes: 2202723
    num_examples: 500
  - name: test
    num_bytes: 49146354
    num_examples: 10695
  - name: train
    num_bytes: 858060337
    num_examples: 220748
  - name: validation
    num_bytes: 49712791
    num_examples: 11392
  download_size: 362783528
  dataset_size: 980787710
- config_name: mlsum_es
  features:
  - name: gem_id
    dtype: string
  - name: gem_parent_id
    dtype: string
  - name: text
    dtype: string
  - name: topic
    dtype: string
  - name: url
    dtype: string
  - name: title
    dtype: string
  - name: date
    dtype: string
  - name: target
    dtype: string
  - name: references
    list: string
  splits:
  - name: challenge_test_covid
    num_bytes: 13576624
    num_examples: 1938
  - name: challenge_train_sample
    num_bytes: 2366443
    num_examples: 500
  - name: challenge_validation_sample
    num_bytes: 2658596
    num_examples: 500
  - name: test
    num_bytes: 72117564
    num_examples: 13366
  - name: train
    num_bytes: 1211240956
    num_examples: 259888
  - name: validation
    num_bytes: 51611723
    num_examples: 9977
  download_size: 525621426
  dataset_size: 1353571906
- config_name: wiki_lingua_es_en_v0
  features:
  - name: gem_id
    dtype: string
  - name: gem_parent_id
    dtype: string
  - name: source
    dtype: string
  - name: target
    dtype: string
  - name: references
    list: string
  splits:
  - name: test
    num_bytes: 50195305
    num_examples: 19797
  - name: train
    num_bytes: 215665468
    num_examples: 79515
  - name: validation
    num_bytes: 25891008
    num_examples: 8835
  download_size: 169406387
  dataset_size: 291751781
- config_name: wiki_lingua_ru_en_v0
  features:
  - name: gem_id
    dtype: string
  - name: gem_parent_id
    dtype: string
  - name: source
    dtype: string
  - name: target
    dtype: string
  - name: references
    list: string
  splits:
  - name: test
    num_bytes: 34865311
    num_examples: 9094
  - name: train
    num_bytes: 159631205
    num_examples: 36898
  - name: validation
    num_bytes: 18626973
    num_examples: 4100
  download_size: 169406387
  dataset_size: 213123489
- config_name: wiki_lingua_tr_en_v0
  features:
  - name: gem_id
    dtype: string
  - name: gem_parent_id
    dtype: string
  - name: source
    dtype: string
  - name: target
    dtype: string
  - name: references
    list: string
  splits:
  - name: test
    num_bytes: 1875110
    num_examples: 808
  - name: train
    num_bytes: 7689845
    num_examples: 3193
  - name: validation
    num_bytes: 942122
    num_examples: 355
  download_size: 169406387
  dataset_size: 10507077
- config_name: wiki_lingua_vi_en_v0
  features:
  - name: gem_id
    dtype: string
  - name: gem_parent_id
    dtype: string
  - name: source
    dtype: string
  - name: target
    dtype: string
  - name: references
    list: string
  splits:
  - name: test
    num_bytes: 6267359
    num_examples: 2167
  - name: train
    num_bytes: 31599580
    num_examples: 9206
  - name: validation
    num_bytes: 3618660
    num_examples: 1023
  download_size: 169406387
  dataset_size: 41485599
- config_name: wiki_lingua_arabic_ar
  features:
  - name: gem_id
    dtype: string
  - name: gem_parent_id
    dtype: string
  - name: source_aligned
    dtype:
      translation:
        languages:
        - ar
        - en
  - name: target_aligned
    dtype:
      translation:
        languages:
        - ar
        - en
  - name: source
    dtype: string
  - name: target
    dtype: string
  - name: references
    list: string
  splits:
  - name: test
    num_bytes: 60915220
    num_examples: 5841
  - name: train
    num_bytes: 208106335
    num_examples: 20441
  - name: validation
    num_bytes: 31126187
    num_examples: 2919
  download_size: 58984103
  dataset_size: 300147742
- config_name: wiki_lingua_chinese_zh
  features:
  - name: gem_id
    dtype: string
  - name: gem_parent_id
    dtype: string
  - name: source_aligned
    dtype:
      translation:
        languages:
        - zh
        - en
  - name: target_aligned
    dtype:
      translation:
        languages:
        - zh
        - en
  - name: source
    dtype: string
  - name: target
    dtype: string
  - name: references
    list: string
  splits:
  - name: test
    num_bytes: 25310021
    num_examples: 3775
  - name: train
    num_bytes: 86130302
    num_examples: 13211
  - name: validation
    num_bytes: 13060918
    num_examples: 1886
  download_size: 32899156
  dataset_size: 124501241
- config_name: wiki_lingua_czech_cs
  features:
  - name: gem_id
    dtype: string
  - name: gem_parent_id
    dtype: string
  - name: source_aligned
    dtype:
      translation:
        languages:
        - cs
        - en
  - name: target_aligned
    dtype:
      translation:
        languages:
        - cs
        - en
  - name: source
    dtype: string
  - name: target
    dtype: string
  - name: references
    list: string
  splits:
  - name: test
    num_bytes: 12124770
    num_examples: 1438
  - name: train
    num_bytes: 41107318
    num_examples: 5033
  - name: validation
    num_bytes: 6305328
    num_examples: 718
  download_size: 14515534
  dataset_size: 59537416
- config_name: wiki_lingua_dutch_nl
  features:
  - name: gem_id
    dtype: string
  - name: gem_parent_id
    dtype: string
  - name: source_aligned
    dtype:
      translation:
        languages:
        - nl
        - en
  - name: target_aligned
    dtype:
      translation:
        languages:
        - nl
        - en
  - name: source
    dtype: string
  - name: target
    dtype: string
  - name: references
    list: string
  splits:
  - name: test
    num_bytes: 49165151
    num_examples: 6248
  - name: train
    num_bytes: 169067454
    num_examples: 21866
  - name: validation
    num_bytes: 25521003
    num_examples: 3123
  download_size: 56492150
  dataset_size: 243753608
- config_name: wiki_lingua_english_en
  features:
  - name: gem_id
    dtype: string
  - name: gem_parent_id
    dtype: string
  - name: source_aligned
    dtype:
      translation:
        languages:
        - en
        - en
  - name: target_aligned
    dtype:
      translation:
        languages:
        - en
        - en
  - name: source
    dtype: string
  - name: target
    dtype: string
  - name: references
    list: string
  splits:
  - name: test
    num_bytes: 138944243
    num_examples: 28614
  - name: train
    num_bytes: 464171624
    num_examples: 99020
  - name: validation
    num_bytes: 67652281
    num_examples: 13823
  download_size: 118031903
  dataset_size: 670768148
- config_name: wiki_lingua_french_fr
  features:
  - name: gem_id
    dtype: string
  - name: gem_parent_id
    dtype: string
  - name: source_aligned
    dtype:
      translation:
        languages:
        - fr
        - en
  - name: target_aligned
    dtype:
      translation:
        languages:
        - fr
        - en
  - name: source
    dtype: string
  - name: target
    dtype: string
  - name: references
    list: string
  splits:
  - name: test
    num_bytes: 108831855
    num_examples: 12731
  - name: train
    num_bytes: 372039357
    num_examples: 44556
  - name: validation
    num_bytes: 54992250
    num_examples: 6364
  download_size: 118758047
  dataset_size: 535863462
- config_name: wiki_lingua_german_de
  features:
  - name: gem_id
    dtype: string
  - name: gem_parent_id
    dtype: string
  - name: source_aligned
    dtype:
      translation:
        languages:
        - de
        - en
  - name: target_aligned
    dtype:
      translation:
        languages:
        - de
        - en
  - name: source
    dtype: string
  - name: target
    dtype: string
  - name: references
    list: string
  splits:
  - name: test
    num_bytes: 93715331
    num_examples: 11669
  - name: train
    num_bytes: 322276536
    num_examples: 40839
  - name: validation
    num_bytes: 47631883
    num_examples: 5833
  download_size: 107638803
  dataset_size: 463623750
- config_name: wiki_lingua_hindi_hi
  features:
  - name: gem_id
    dtype: string
  - name: gem_parent_id
    dtype: string
  - name: source_aligned
    dtype:
      translation:
        languages:
        - hi
        - en
  - name: target_aligned
    dtype:
      translation:
        languages:
        - hi
        - en
  - name: source
    dtype: string
  - name: target
    dtype: string
  - name: references
    list: string
  splits:
  - name: test
    num_bytes: 28543048
    num_examples: 1984
  - name: train
    num_bytes: 99672133
    num_examples: 6942
  - name: validation
    num_bytes: 14706378
    num_examples: 991
  download_size: 21042040
  dataset_size: 142921559
- config_name: wiki_lingua_indonesian_id
  features:
  - name: gem_id
    dtype: string
  - name: gem_parent_id
    dtype: string
  - name: source_aligned
    dtype:
      translation:
        languages:
        - id
        - en
  - name: target_aligned
    dtype:
      translation:
        languages:
        - id
        - en
  - name: source
    dtype: string
  - name: target
    dtype: string
  - name: references
    list: string
  splits:
  - name: test
    num_bytes: 76567819
    num_examples: 9497
  - name: train
    num_bytes: 263974954
    num_examples: 33237
  - name: validation
    num_bytes: 39297987
    num_examples: 4747
  download_size: 83968162
  dataset_size: 379840760
- config_name: wiki_lingua_italian_it
  features:
  - name: gem_id
    dtype: string
  - name: gem_parent_id
    dtype: string
  - name: source_aligned
    dtype:
      translation:
        languages:
        - it
        - en
  - name: target_aligned
    dtype:
      translation:
        languages:
        - it
        - en
  - name: source
    dtype: string
  - name: target
    dtype: string
  - name: references
    list: string
  splits:
  - name: test
    num_bytes: 76840429
    num_examples: 10189
  - name: train
    num_bytes: 267090482
    num_examples: 35661
  - name: validation
    num_bytes: 39227425
    num_examples: 5093
  download_size: 88921209
  dataset_size: 383158336
- config_name: wiki_lingua_japanese_ja
  features:
  - name: gem_id
    dtype: string
  - name: gem_parent_id
    dtype: string
  - name: source_aligned
    dtype:
      translation:
        languages:
        - ja
        - en
  - name: target_aligned
    dtype:
      translation:
        languages:
        - ja
        - en
  - name: source
    dtype: string
  - name: target
    dtype: string
  - name: references
    list: string
  splits:
  - name: test
    num_bytes: 21175951
    num_examples: 2530
  - name: train
    num_bytes: 73871019
    num_examples: 8853
  - name: validation
    num_bytes: 10807006
    num_examples: 1264
  download_size: 22803299
  dataset_size: 105853976
- config_name: wiki_lingua_korean_ko
  features:
  - name: gem_id
    dtype: string
  - name: gem_parent_id
    dtype: string
  - name: source_aligned
    dtype:
      translation:
        languages:
        - ko
        - en
  - name: target_aligned
    dtype:
      translation:
        languages:
        - ko
        - en
  - name: source
    dtype: string
  - name: target
    dtype: string
  - name: references
    list: string
  splits:
  - name: test
    num_bytes: 21172641
    num_examples: 2436
  - name: train
    num_bytes: 73106687
    num_examples: 8524
  - name: validation
    num_bytes: 10788276
    num_examples: 1216
  download_size: 23336917
  dataset_size: 105067604
- config_name: wiki_lingua_portuguese_pt
  features:
  - name: gem_id
    dtype: string
  - name: gem_parent_id
    dtype: string
  - name: source_aligned
    dtype:
      translation:
        languages:
        - pt
        - en
  - name: target_aligned
    dtype:
      translation:
        languages:
        - pt
        - en
  - name: source
    dtype: string
  - name: target
    dtype: string
  - name: references
    list: string
  splits:
  - name: test
    num_bytes: 117775356
    num_examples: 16331
  - name: train
    num_bytes: 405546332
    num_examples: 57159
  - name: validation
    num_bytes: 59729210
    num_examples: 8165
  download_size: 137542940
  dataset_size: 583050898
- config_name: wiki_lingua_russian_ru
  features:
  - name: gem_id
    dtype: string
  - name: gem_parent_id
    dtype: string
  - name: source_aligned
    dtype:
      translation:
        languages:
        - ru
        - en
  - name: target_aligned
    dtype:
      translation:
        languages:
        - ru
        - en
  - name: source
    dtype: string
  - name: target
    dtype: string
  - name: references
    list: string
  splits:
  - name: test
    num_bytes: 116330937
    num_examples: 10580
  - name: train
    num_bytes: 406299624
    num_examples: 37028
  - name: validation
    num_bytes: 59651340
    num_examples: 5288
  download_size: 106281321
  dataset_size: 582281901
- config_name: wiki_lingua_spanish_es
  features:
  - name: gem_id
    dtype: string
  - name: gem_parent_id
    dtype: string
  - name: source_aligned
    dtype:
      translation:
        languages:
        - es
        - en
  - name: target_aligned
    dtype:
      translation:
        languages:
        - es
        - en
  - name: source
    dtype: string
  - name: target
    dtype: string
  - name: references
    list: string
  splits:
  - name: test
    num_bytes: 177096288
    num_examples: 22632
  - name: train
    num_bytes: 604276564
    num_examples: 79212
  - name: validation
    num_bytes: 88677656
    num_examples: 11316
  download_size: 198247534
  dataset_size: 870050508
- config_name: wiki_lingua_thai_th
  features:
  - name: gem_id
    dtype: string
  - name: gem_parent_id
    dtype: string
  - name: source_aligned
    dtype:
      translation:
        languages:
        - th
        - en
  - name: target_aligned
    dtype:
      translation:
        languages:
        - th
        - en
  - name: source
    dtype: string
  - name: target
    dtype: string
  - name: references
    list: string
  splits:
  - name: test
    num_bytes: 40049968
    num_examples: 2950
  - name: train
    num_bytes: 139287649
    num_examples: 10325
  - name: validation
    num_bytes: 21097845
    num_examples: 1475
  download_size: 29988180
  dataset_size: 200435462
- config_name: wiki_lingua_turkish_tr
  features:
  - name: gem_id
    dtype: string
  - name: gem_parent_id
    dtype: string
  - name: source_aligned
    dtype:
      translation:
        languages:
        - tr
        - en
  - name: target_aligned
    dtype:
      translation:
        languages:
        - tr
        - en
  - name: source
    dtype: string
  - name: target
    dtype: string
  - name: references
    list: string
  splits:
  - name: test
    num_bytes: 6197850
    num_examples: 900
  - name: train
    num_bytes: 21987247
    num_examples: 3148
  - name: validation
    num_bytes: 3229714
    num_examples: 449
  download_size: 7055820
  dataset_size: 31414811
- config_name: wiki_lingua_vietnamese_vi
  features:
  - name: gem_id
    dtype: string
  - name: gem_parent_id
    dtype: string
  - name: source_aligned
    dtype:
      translation:
        languages:
        - vi
        - en
  - name: target_aligned
    dtype:
      translation:
        languages:
        - vi
        - en
  - name: source
    dtype: string
  - name: target
    dtype: string
  - name: references
    list: string
  splits:
  - name: test
    num_bytes: 37430208
    num_examples: 3917
  - name: train
    num_bytes: 128025008
    num_examples: 13707
  - name: validation
    num_bytes: 19414734
    num_examples: 1957
  download_size: 38035490
  dataset_size: 184869950
- config_name: xsum
  features:
  - name: gem_id
    dtype: string
  - name: gem_parent_id
    dtype: string
  - name: xsum_id
    dtype: string
  - name: document
    dtype: string
  - name: target
    dtype: string
  - name: references
    list: string
  splits:
  - name: challenge_test_backtranslation
    num_bytes: 1262047
    num_examples: 500
  - name: challenge_test_bfp_02
    num_bytes: 1090364
    num_examples: 500
  - name: challenge_test_bfp_05
    num_bytes: 1078076
    num_examples: 500
  - name: challenge_test_covid
    num_bytes: 1867180
    num_examples: 401
  - name: challenge_test_nopunc
    num_bytes: 1127796
    num_examples: 500
  - name: challenge_train_sample
    num_bytes: 1429145
    num_examples: 500
  - name: challenge_validation_sample
    num_bytes: 1012689
    num_examples: 500
  - name: test
    num_bytes: 2598509
    num_examples: 1166
  - name: train
    num_bytes: 66299136
    num_examples: 23206
  - name: validation
    num_bytes: 2270306
    num_examples: 1117
  download_size: 258277147
  dataset_size: 80035248
- config_name: common_gen
  features:
  - name: gem_id
    dtype: string
  - name: gem_parent_id
    dtype: string
  - name: concept_set_id
    dtype: int32
  - name: concepts
    list: string
  - name: target
    dtype: string
  - name: references
    list: string
  splits:
  - name: challenge_test_scramble
    num_bytes: 60411
    num_examples: 500
  - name: challenge_train_sample
    num_bytes: 85413
    num_examples: 500
  - name: challenge_validation_sample
    num_bytes: 215192
    num_examples: 500
  - name: test
    num_bytes: 153170
    num_examples: 1497
  - name: train
    num_bytes: 10475926
    num_examples: 67389
  - name: validation
    num_bytes: 405872
    num_examples: 993
  download_size: 1933517
  dataset_size: 11395984
- config_name: cs_restaurants
  features:
  - name: gem_id
    dtype: string
  - name: gem_parent_id
    dtype: string
  - name: dialog_act
    dtype: string
  - name: dialog_act_delexicalized
    dtype: string
  - name: target_delexicalized
    dtype: string
  - name: target
    dtype: string
  - name: references
    list: string
  splits:
  - name: challenge_test_scramble
    num_bytes: 185574
    num_examples: 500
  - name: challenge_train_sample
    num_bytes: 127869
    num_examples: 500
  - name: challenge_validation_sample
    num_bytes: 193239
    num_examples: 500
  - name: test
    num_bytes: 295696
    num_examples: 842
  - name: train
    num_bytes: 873145
    num_examples: 3569
  - name: validation
    num_bytes: 288222
    num_examples: 781
  download_size: 1531111
  dataset_size: 1963745
- config_name: dart
  features:
  - name: gem_id
    dtype: string
  - name: gem_parent_id
    dtype: string
  - name: dart_id
    dtype: int32
  - name: tripleset
    list:
      list: string
  - name: subtree_was_extended
    dtype: bool
  - name: target_sources
    list: string
  - name: target
    dtype: string
  - name: references
    list: string
  splits:
  - name: test
    num_bytes: 3476953
    num_examples: 5097
  - name: train
    num_bytes: 23047610
    num_examples: 62659
  - name: validation
    num_bytes: 1934054
    num_examples: 2768
  download_size: 29939366
  dataset_size: 28458617
- config_name: e2e_nlg
  features:
  - name: gem_id
    dtype: string
  - name: gem_parent_id
    dtype: string
  - name: meaning_representation
    dtype: string
  - name: target
    dtype: string
  - name: references
    list: string
  splits:
  - name: challenge_test_scramble
    num_bytes: 236199
    num_examples: 500
  - name: challenge_train_sample
    num_bytes: 145319
    num_examples: 500
  - name: challenge_validation_sample
    num_bytes: 226525
    num_examples: 500
  - name: test
    num_bytes: 2133695
    num_examples: 4693
  - name: train
    num_bytes: 9129030
    num_examples: 33525
  - name: validation
    num_bytes: 1856097
    num_examples: 4299
  download_size: 14668048
  dataset_size: 13726865
- config_name: totto
  features:
  - name: gem_id
    dtype: string
  - name: gem_parent_id
    dtype: string
  - name: totto_id
    dtype: int32
  - name: table_page_title
    dtype: string
  - name: table_webpage_url
    dtype: string
  - name: table_section_title
    dtype: string
  - name: table_section_text
    dtype: string
  - name: table
    list:
      list:
      - name: column_span
        dtype: int32
      - name: is_header
        dtype: bool
      - name: row_span
        dtype: int32
      - name: value
        dtype: string
  - name: highlighted_cells
    list:
      list: int32
  - name: example_id
    dtype: string
  - name: sentence_annotations
    list:
    - name: original_sentence
      dtype: string
    - name: sentence_after_deletion
      dtype: string
    - name: sentence_after_ambiguity
      dtype: string
    - name: final_sentence
      dtype: string
  - name: overlap_subset
    dtype: string
  - name: target
    dtype: string
  - name: references
    list: string
  splits:
  - name: challenge_test_scramble
    num_bytes: 2638966
    num_examples: 500
  - name: challenge_train_sample
    num_bytes: 2283076
    num_examples: 500
  - name: challenge_validation_sample
    num_bytes: 3398639
    num_examples: 500
  - name: test
    num_bytes: 41330062
    num_examples: 7700
  - name: train
    num_bytes: 676032144
    num_examples: 121153
  - name: validation
    num_bytes: 50736204
    num_examples: 7700
  download_size: 189534609
  dataset_size: 776419091
- config_name: web_nlg_en
  features:
  - name: gem_id
    dtype: string
  - name: gem_parent_id
    dtype: string
  - name: input
    list: string
  - name: target
    dtype: string
  - name: references
    list: string
  - name: category
    dtype: string
  - name: webnlg_id
    dtype: string
  splits:
  - name: challenge_test_numbers
    num_bytes: 409213
    num_examples: 500
  - name: challenge_test_scramble
    num_bytes: 402407
    num_examples: 500
  - name: challenge_train_sample
    num_bytes: 193198
    num_examples: 502
  - name: challenge_validation_sample
    num_bytes: 359868
    num_examples: 499
  - name: test
    num_bytes: 1403601
    num_examples: 1779
  - name: train
    num_bytes: 13067615
    num_examples: 35426
  - name: validation
    num_bytes: 1153995
    num_examples: 1667
  download_size: 13181969
  dataset_size: 16989897
- config_name: web_nlg_ru
  features:
  - name: gem_id
    dtype: string
  - name: gem_parent_id
    dtype: string
  - name: input
    list: string
  - name: target
    dtype: string
  - name: references
    list: string
  - name: category
    dtype: string
  - name: webnlg_id
    dtype: string
  splits:
  - name: challenge_test_scramble
    num_bytes: 521625
    num_examples: 500
  - name: challenge_train_sample
    num_bytes: 247089
    num_examples: 501
  - name: challenge_validation_sample
    num_bytes: 514117
    num_examples: 500
  - name: test
    num_bytes: 1145282
    num_examples: 1102
  - name: train
    num_bytes: 6888009
    num_examples: 14630
  - name: validation
    num_bytes: 795998
    num_examples: 790
  download_size: 7854845
  dataset_size: 10112120
- config_name: wiki_auto_asset_turk
  features:
  - name: gem_id
    dtype: string
  - name: gem_parent_id
    dtype: string
  - name: source
    dtype: string
  - name: target
    dtype: string
  - name: references
    list: string
  splits:
  - name: challenge_test_asset_backtranslation
    num_bytes: 436820
    num_examples: 359
  - name: challenge_test_asset_bfp02
    num_bytes: 432742
    num_examples: 359
  - name: challenge_test_asset_bfp05
    num_bytes: 432742
    num_examples: 359
  - name: challenge_test_asset_nopunc
    num_bytes: 432735
    num_examples: 359
  - name: challenge_test_turk_backtranslation
    num_bytes: 417204
    num_examples: 359
  - name: challenge_test_turk_bfp02
    num_bytes: 414381
    num_examples: 359
  - name: challenge_test_turk_bfp05
    num_bytes: 414383
    num_examples: 359
  - name: challenge_test_turk_nopunc
    num_bytes: 414388
    num_examples: 359
  - name: challenge_train_sample
    num_bytes: 219542
    num_examples: 500
  - name: challenge_validation_sample
    num_bytes: 213048
    num_examples: 500
  - name: test_asset
    num_bytes: 475336
    num_examples: 359
  - name: test_turk
    num_bytes: 406842
    num_examples: 359
  - name: train
    num_bytes: 161095379
    num_examples: 483801
  - name: validation
    num_bytes: 8211308
    num_examples: 20000
  download_size: 126927527
  dataset_size: 174016850
- config_name: schema_guided_dialog
  features:
  - name: gem_id
    dtype: string
  - name: gem_parent_id
    dtype: string
  - name: dialog_acts
    list:
    - name: act
      dtype:
        class_label:
          names:
            0: AFFIRM
            1: AFFIRM_INTENT
            2: CONFIRM
            3: GOODBYE
            4: INFORM
            5: INFORM_COUNT
            6: INFORM_INTENT
            7: NEGATE
            8: NEGATE_INTENT
            9: NOTIFY_FAILURE
            10: NOTIFY_SUCCESS
            11: OFFER
            12: OFFER_INTENT
            13: REQUEST
            14: REQUEST_ALTS
            15: REQ_MORE
            16: SELECT
            17: THANK_YOU
    - name: slot
      dtype: string
    - name: values
      list: string
  - name: context
    list: string
  - name: dialog_id
    dtype: string
  - name: service
    dtype: string
  - name: turn_id
    dtype: int32
  - name: prompt
    dtype: string
  - name: target
    dtype: string
  - name: references
    list: string
  splits:
  - name: challenge_test_backtranslation
    num_bytes: 512834
    num_examples: 500
  - name: challenge_test_bfp02
    num_bytes: 529404
    num_examples: 500
  - name: challenge_test_bfp05
    num_bytes: 515151
    num_examples: 500
  - name: challenge_test_nopunc
    num_bytes: 509332
    num_examples: 500
  - name: challenge_test_scramble
    num_bytes: 514644
    num_examples: 500
  - name: challenge_train_sample
    num_bytes: 441326
    num_examples: 500
  - name: challenge_validation_sample
    num_bytes: 491492
    num_examples: 500
  - name: test
    num_bytes: 10160596
    num_examples: 10000
  - name: train
    num_bytes: 146648117
    num_examples: 164982
  - name: validation
    num_bytes: 9376504
    num_examples: 10000
  download_size: 17826468
  dataset_size: 169699400
---

# Dataset Card for GEM

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

- **Homepage:** [https://gem-benchmark.github.io/](https://gem-benchmark.github.io/)
- **Repository:**
- **Paper:** [The GEM Benchmark: Natural Language Generation, its Evaluation and Metrics](https://arxiv.org/abs/2102.01672)
- **Point of Contact:** [Sebastian Gehrman](gehrmann@google.com)
- **Size of downloaded dataset files:** 2084.23 MB
- **Size of the generated dataset:** 3734.73 MB
- **Total amount of disk used:** 5818.96 MB

### Dataset Summary

GEM is a benchmark environment for Natural Language Generation with a focus on its Evaluation,
both through human annotations and automated Metrics.

GEM aims to:
- measure NLG progress across 13 datasets spanning many NLG tasks and languages.
- provide an in-depth analysis of data and models presented via data statements and challenge sets.
- develop standards for evaluation of generated text using both automated and human metrics.

It is our goal to regularly update GEM and to encourage toward more inclusive practices in dataset development
by extending existing data or developing datasets for additional languages.

You can find more complete information in the dataset cards for each of the subsets:
- [CommonGen](https://gem-benchmark.github.io/data_cards/CommonGen)
- [Czech Restaurant](https://gem-benchmark.github.io/data_cards/Czech%20Restaurant)
- [DART](https://gem-benchmark.github.io/data_cards/DART)
- [E2E](https://gem-benchmark.github.io/data_cards/E2E)
- [MLSum](https://gem-benchmark.github.io/data_cards/MLSum)
- [Schema-Guided Dialog](https://gem-benchmark.github.io/data_cards/Schema-Guided%20DIalog)
- [WebNLG](https://gem-benchmark.github.io/data_cards/WebNLG)
- [Wiki-Auto](https://gem-benchmark.github.io/data_cards/Wiki-Auto)/[ASSET](https://gem-benchmark.github.io/data_cards/ASSET)/[TURK](https://gem-benchmark.github.io/data_cards/TURK)
- [WikiLingua](https://gem-benchmark.github.io/data_cards/WikiLingua)
- [XSum](https://gem-benchmark.github.io/data_cards/XSum)

The subsets are organized by task:
```
{
    "summarization": {
        "mlsum": ["mlsum_de", "mlsum_es"],
        "wiki_lingua": ["wiki_lingua_es_en", "wiki_lingua_ru_en", "wiki_lingua_tr_en", "wiki_lingua_vi_en"],
        "xsum": ["xsum"],
    },
    "struct2text": {
        "common_gen": ["common_gen"],
        "cs_restaurants": ["cs_restaurants"],
        "dart": ["dart"],
        "e2e": ["e2e_nlg"],
        "totto": ["totto"],
        "web_nlg": ["web_nlg_en", "web_nlg_ru"],
    },
    "simplification": {
        "wiki_auto_asset_turk": ["wiki_auto_asset_turk"],
    },
    "dialog": {
        "schema_guided_dialog": ["schema_guided_dialog"],
    },
}
```

Each example has one `target` per example in its training set, and a set of `references` (with one or more items) in its validation and test set.

### Supported Tasks and Leaderboards

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Languages

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

## Dataset Structure

### Data Instances

#### common_gen

- **Size of downloaded dataset files:** 1.76 MB
- **Size of the generated dataset:** 8.80 MB
- **Total amount of disk used:** 10.56 MB

An example of `validation` looks as follows.
```
{'concept_set_id': 0,
 'concepts': ['field', 'look', 'stand'],
 'gem_id': 'common_gen-validation-0',
 'references': ['The player stood in the field looking at the batter.',
                'The coach stands along the field, looking at the goalkeeper.',
                'I stood and looked across the field, peacefully.',
                'Someone stands, looking around the empty field.'],
 'target': 'The player stood in the field looking at the batter.'}
```

#### cs_restaurants

- **Size of downloaded dataset files:** 1.40 MB
- **Size of the generated dataset:** 1.25 MB
- **Total amount of disk used:** 2.64 MB

An example of `validation` looks as follows.
```
{'dialog_act': '?request(area)',
 'dialog_act_delexicalized': '?request(area)',
 'gem_id': 'cs_restaurants-validation-0',
 'references': ['Jakou lokalitu hledáte ?'],
 'target': 'Jakou lokalitu hledáte ?',
 'target_delexicalized': 'Jakou lokalitu hledáte ?'}
```

#### dart

- **Size of downloaded dataset files:** 28.01 MB
- **Size of the generated dataset:** 26.17 MB
- **Total amount of disk used:** 54.18 MB

An example of `validation` looks as follows.
```
{'dart_id': 0,
 'gem_id': 'dart-validation-0',
 'references': ['A school from Mars Hill, North Carolina, joined in 1973.'],
 'subtree_was_extended': True,
 'target': 'A school from Mars Hill, North Carolina, joined in 1973.',
 'target_sources': ['WikiSQL_decl_sents'],
 'tripleset': [['Mars Hill College', 'JOINED', '1973'], ['Mars Hill College', 'LOCATION', 'Mars Hill, North Carolina']]}
```

#### e2e_nlg

- **Size of downloaded dataset files:** 13.92 MB
- **Size of the generated dataset:** 11.58 MB
- **Total amount of disk used:** 25.50 MB

An example of `validation` looks as follows.
```
{'gem_id': 'e2e_nlg-validation-0',
 'meaning_representation': 'name[Alimentum], area[city centre], familyFriendly[no]',
 'references': ['There is a place in the city centre, Alimentum, that is not family-friendly.'],
 'target': 'There is a place in the city centre, Alimentum, that is not family-friendly.'}
```

#### mlsum_de

- **Size of downloaded dataset files:** 331.27 MB
- **Size of the generated dataset:** 907.00 MB
- **Total amount of disk used:** 1238.27 MB

An example of `validation` looks as follows.
```
{'date': '00/04/2019',
 'gem_id': 'mlsum_de-validation-0',
 'references': ['In einer Kleinstadt auf der Insel Usedom war eine junge Frau tot in ihrer Wohnung gefunden worden. Nun stehen zwei Bekannte unter Verdacht.'],
 'target': 'In einer Kleinstadt auf der Insel Usedom war eine junge Frau tot in ihrer Wohnung gefunden worden. Nun stehen zwei Bekannte unter Verdacht.',
 'text': 'Kerzen und Blumen stehen vor dem Eingang eines Hauses, in dem eine 18-jährige Frau tot aufgefunden wurde. In einer Kleinstadt auf der Insel Usedom war eine junge Frau tot in ...',
 'title': 'Tod von 18-Jähriger auf Usedom: Zwei Festnahmen',
 'topic': 'panorama',
 'url': 'https://www.sueddeutsche.de/panorama/usedom-frau-tot-festnahme-verdaechtige-1.4412256'}
```

#### mlsum_es

- **Size of downloaded dataset files:** 490.29 MB
- **Size of the generated dataset:** 1253.63 MB
- **Total amount of disk used:** 1743.92 MB

An example of `validation` looks as follows.
```
{'date': '05/01/2019',
 'gem_id': 'mlsum_es-validation-0',
 'references': ['El diseñador que dio carta de naturaleza al estilo genuinamente americano celebra el medio siglo de su marca entre grandes fastos y problemas financieros. Conectar con las nuevas generaciones es el regalo que precisa más que nunca'],
 'target': 'El diseñador que dio carta de naturaleza al estilo genuinamente americano celebra el medio siglo de su marca entre grandes fastos y problemas financieros. Conectar con las nuevas generaciones es el regalo que precisa más que nunca',
 'text': 'Un oso de peluche marcándose un heelflip de monopatín es todo lo que Ralph Lauren necesitaba esta Navidad. Estampado en un jersey de lana azul marino, supone la guinda que corona ...',
 'title': 'Ralph Lauren busca el secreto de la eterna juventud',
 'topic': 'elpais estilo',
 'url': 'http://elpais.com/elpais/2019/01/04/estilo/1546617396_933318.html'}
```

#### schema_guided_dialog

- **Size of downloaded dataset files:** 8.24 MB
- **Size of the generated dataset:** 43.66 MB
- **Total amount of disk used:** 51.91 MB

An example of `validation` looks as follows.
```
{'dialog_acts': [{'act': 2, 'slot': 'song_name', 'values': ['Carnivore']}, {'act': 2, 'slot': 'playback_device', 'values': ['TV']}],
 'dialog_id': '10_00054',
 'gem_id': 'schema_guided_dialog-validation-0',
 'prompt': 'Yes, I would.',
 'references': ['Please confirm the song Carnivore on tv.'],
 'target': 'Please confirm the song Carnivore on tv.',
 'turn_id': 15}
```

#### totto

- **Size of downloaded dataset files:** 179.03 MB
- **Size of the generated dataset:** 722.88 MB
- **Total amount of disk used:** 901.91 MB

An example of `validation` looks as follows.
```
{'example_id': '7391450717765563190',
 'gem_id': 'totto-validation-0',
 'highlighted_cells': [[3, 0], [3, 2], [3, 3]],
 'overlap_subset': 'True',
 'references': ['Daniel Henry Chamberlain was the 76th Governor of South Carolina from 1874.',
                'Daniel Henry Chamberlain was the 76th Governor of South Carolina, beginning in 1874.',
                'Daniel Henry Chamberlain was the 76th Governor of South Carolina who took office in 1874.'],
 'sentence_annotations': [{'final_sentence': 'Daniel Henry Chamberlain was the 76th Governor of South Carolina from 1874.',
                           'original_sentence': 'Daniel Henry Chamberlain (June 23, 1835 – April 13, 1907) was an American planter, lawyer, author and the 76th Governor of South Carolina '
                                                'from 1874 until 1877.',
                           'sentence_after_ambiguity': 'Daniel Henry Chamberlain was the 76th Governor of South Carolina from 1874.',
                           'sentence_after_deletion': 'Daniel Henry Chamberlain was the 76th Governor of South Carolina from 1874.'},
                          ...
                          ],
 'table': [[{'column_span': 1, 'is_header': True, 'row_span': 1, 'value': '#'},
            {'column_span': 2, 'is_header': True, 'row_span': 1, 'value': 'Governor'},
            {'column_span': 1, 'is_header': True, 'row_span': 1, 'value': 'Took Office'},
            {'column_span': 1, 'is_header': True, 'row_span': 1, 'value': 'Left Office'}],
           [{'column_span': 1, 'is_header': True, 'row_span': 1, 'value': '74'},
            {'column_span': 1, 'is_header': False, 'row_span': 1, 'value': '-'},
            {'column_span': 1, 'is_header': False, 'row_span': 1, 'value': 'Robert Kingston Scott'},
            {'column_span': 1, 'is_header': False, 'row_span': 1, 'value': 'July 6, 1868'}],
           ...
          ],
 'table_page_title': 'List of Governors of South Carolina',
 'table_section_text': 'Parties Democratic Republican',
 'table_section_title': 'Governors under the Constitution of 1868',
 'table_webpage_url': 'http://en.wikipedia.org/wiki/List_of_Governors_of_South_Carolina',
 'target': 'Daniel Henry Chamberlain was the 76th Governor of South Carolina from 1874.',
 'totto_id': 0}
```

#### web_nlg_en

- **Size of downloaded dataset files:** 12.35 MB
- **Size of the generated dataset:** 13.95 MB
- **Total amount of disk used:** 26.29 MB

An example of `validation` looks as follows.
```
{'category': 'Airport',
 'gem_id': 'web_nlg_en-validation-0',
 'input': ['Aarhus | leader | Jacob_Bundsgaard'],
 'references': ['The leader of Aarhus is Jacob Bundsgaard.'],
 'target': 'The leader of Aarhus is Jacob Bundsgaard.',
 'webnlg_id': 'dev/Airport/1/Id1'}
```

#### web_nlg_ru

- **Size of downloaded dataset files:** 7.28 MB
- **Size of the generated dataset:** 8.02 MB
- **Total amount of disk used:** 15.30 MB

An example of `validation` looks as follows.
```
{'category': 'Airport',
 'gem_id': 'web_nlg_ru-validation-0',
 'input': ['Punjab,_Pakistan | leaderTitle | Provincial_Assembly_of_the_Punjab'],
 'references': ['Пенджаб, Пакистан, возглавляется Провинциальной ассамблеей Пенджаба.', 'Пенджаб, Пакистан возглавляется Провинциальной ассамблеей Пенджаба.'],
 'target': 'Пенджаб, Пакистан, возглавляется Провинциальной ассамблеей Пенджаба.',
 'webnlg_id': 'dev/Airport/1/Id1'}
```

#### wiki_auto_asset_turk

- **Size of downloaded dataset files:** 121.37 MB
- **Size of the generated dataset:** 145.69 MB
- **Total amount of disk used:** 267.07 MB

An example of `validation` looks as follows.
```
{'gem_id': 'wiki_auto_asset_turk-validation-0',
 'references': ['The Gandalf Awards honor excellent writing in in fantasy literature.'],
 'source': 'The Gandalf Awards, honoring achievement in fantasy literature, were conferred by the World Science Fiction Society annually from 1974 to 1981.',
 'source_id': '350_691837-1-0-0',
 'target': 'The Gandalf Awards honor excellent writing in in fantasy literature.',
 'target_id': '350_691837-0-0-0'}
```

#### wiki_lingua_es_en

- **Size of downloaded dataset files:** 161.56 MB
- **Size of the generated dataset:** 274.28 MB
- **Total amount of disk used:** 435.84 MB

An example of `validation` looks as follows.
```
'references': ["Practice matted hair prevention from early in your cat's life. Make sure that your cat is grooming itself effectively. Keep a close eye on cats with long hair."],
'source': 'Muchas personas presentan problemas porque no cepillaron el pelaje de sus gatos en una etapa temprana de su vida, ya que no lo consideraban necesario. Sin embargo, a medida que...',
'target': "Practice matted hair prevention from early in your cat's life. Make sure that your cat is grooming itself effectively. Keep a close eye on cats with long hair."}
```

#### wiki_lingua_ru_en

- **Size of downloaded dataset files:** 161.56 MB
- **Size of the generated dataset:** 201.43 MB
- **Total amount of disk used:** 362.99 MB

An example of `validation` looks as follows.
```
{'gem_id': 'wiki_lingua_ru_en-val-0',
 'references': ['Get immediate medical care if you notice signs of a complication. Undergo diagnostic tests to check for gallstones and complications. Ask your doctor about your treatment '
                'options.'],
 'source': 'И хотя, скорее всего, вам не о чем волноваться, следует незамедлительно обратиться к врачу, если вы подозреваете, что у вас возникло осложнение желчекаменной болезни. Это ...',
 'target': 'Get immediate medical care if you notice signs of a complication. Undergo diagnostic tests to check for gallstones and complications. Ask your doctor about your treatment '
           'options.'}
```

#### wiki_lingua_tr_en

- **Size of downloaded dataset files:** 161.56 MB
- **Size of the generated dataset:** 9.87 MB
- **Total amount of disk used:** 171.42 MB

An example of `validation` looks as follows.
```
{'gem_id': 'wiki_lingua_tr_en-val-0',
 'references': ['Open Instagram. Go to the video you want to download. Tap ⋮. Tap Copy Link. Open  Google Chrome. Tap the address bar. Go to the SaveFromWeb site. Tap the "Paste Instagram Video" text box. Tap and hold the text box. Tap PASTE. Tap Download. Download the video. Find the video on your Android.'],
 'source': 'Instagram uygulamasının çok renkli kamera şeklindeki simgesine dokun. Daha önce giriş yaptıysan Instagram haber kaynağı açılır. Giriş yapmadıysan istendiğinde e-posta adresini ...',
 'target': 'Open Instagram. Go to the video you want to download. Tap ⋮. Tap Copy Link. Open  Google Chrome. Tap the address bar. Go to the SaveFromWeb site. Tap the "Paste Instagram Video" text box. Tap and hold the text box. Tap PASTE. Tap Download. Download the video. Find the video on your Android.'}
```

#### wiki_lingua_vi_en

- **Size of downloaded dataset files:** 161.56 MB
- **Size of the generated dataset:** 39.12 MB
- **Total amount of disk used:** 200.68 MB

An example of `validation` looks as follows.
```
{'gem_id': 'wiki_lingua_vi_en-val-0',
 'references': ['Select the right time of year for planting the tree. You will usually want to plant your tree when it is dormant, or not flowering, during cooler or colder times of year.'],
 'source': 'Bạn muốn cung cấp cho cây cơ hội tốt nhất để phát triển và sinh tồn. Trồng cây đúng thời điểm trong năm chính là yếu tố then chốt. Thời điểm sẽ thay đổi phụ thuộc vào loài cây ...',
 'target': 'Select the right time of year for planting the tree. You will usually want to plant your tree when it is dormant, or not flowering, during cooler or colder times of year.'}
```

#### xsum

- **Size of downloaded dataset files:** 243.08 MB
- **Size of the generated dataset:** 67.40 MB
- **Total amount of disk used:** 310.48 MB

An example of `validation` looks as follows.
```
{'document': 'Burberry reported pre-tax profits of £166m for the year to March. A year ago it made a loss of £16.1m, hit by charges at its Spanish operations.\n'
             'In the past year it has opened 21 new stores and closed nine. It plans to open 20-30 stores this year worldwide.\n'
             'The group has also focused on promoting the Burberry brand online...',
 'gem_id': 'xsum-validation-0',
 'references': ['Luxury fashion designer Burberry has returned to profit after opening new stores and spending more on online marketing'],
 'target': 'Luxury fashion designer Burberry has returned to profit after opening new stores and spending more on online marketing',
 'xsum_id': '10162122'}
```

### Data Fields

The data fields are the same among all splits.

#### common_gen
- `gem_id`: a `string` feature.
- `concept_set_id`: a `int32` feature.
- `concepts`: a `list` of `string` features.
- `target`: a `string` feature.
- `references`: a `list` of `string` features.

#### cs_restaurants
- `gem_id`: a `string` feature.
- `dialog_act`: a `string` feature.
- `dialog_act_delexicalized`: a `string` feature.
- `target_delexicalized`: a `string` feature.
- `target`: a `string` feature.
- `references`: a `list` of `string` features.

#### dart
- `gem_id`: a `string` feature.
- `dart_id`: a `int32` feature.
- `tripleset`: a `list` of `string` features.
- `subtree_was_extended`: a `bool` feature.
- `target_sources`: a `list` of `string` features.
- `target`: a `string` feature.
- `references`: a `list` of `string` features.

#### e2e_nlg
- `gem_id`: a `string` feature.
- `meaning_representation`: a `string` feature.
- `target`: a `string` feature.
- `references`: a `list` of `string` features.

#### mlsum_de
- `gem_id`: a `string` feature.
- `text`: a `string` feature.
- `topic`: a `string` feature.
- `url`: a `string` feature.
- `title`: a `string` feature.
- `date`: a `string` feature.
- `target`: a `string` feature.
- `references`: a `list` of `string` features.

#### mlsum_es
- `gem_id`: a `string` feature.
- `text`: a `string` feature.
- `topic`: a `string` feature.
- `url`: a `string` feature.
- `title`: a `string` feature.
- `date`: a `string` feature.
- `target`: a `string` feature.
- `references`: a `list` of `string` features.

#### schema_guided_dialog
- `gem_id`: a `string` feature.
- `act`: a classification label, with possible values including `AFFIRM` (0), `AFFIRM_INTENT` (1), `CONFIRM` (2), `GOODBYE` (3), `INFORM` (4).
- `slot`: a `string` feature.
- `values`: a `list` of `string` features.
- `dialog_id`: a `string` feature.
- `turn_id`: a `int32` feature.
- `prompt`: a `string` feature.
- `target`: a `string` feature.
- `references`: a `list` of `string` features.

#### totto
- `gem_id`: a `string` feature.
- `totto_id`: a `int32` feature.
- `table_page_title`: a `string` feature.
- `table_webpage_url`: a `string` feature.
- `table_section_title`: a `string` feature.
- `table_section_text`: a `string` feature.
- `column_span`: a `int32` feature.
- `is_header`: a `bool` feature.
- `row_span`: a `int32` feature.
- `value`: a `string` feature.
- `highlighted_cells`: a `list` of `int32` features.
- `example_id`: a `string` feature.
- `original_sentence`: a `string` feature.
- `sentence_after_deletion`: a `string` feature.
- `sentence_after_ambiguity`: a `string` feature.
- `final_sentence`: a `string` feature.
- `overlap_subset`: a `string` feature.
- `target`: a `string` feature.
- `references`: a `list` of `string` features.

#### web_nlg_en
- `gem_id`: a `string` feature.
- `input`: a `list` of `string` features.
- `target`: a `string` feature.
- `references`: a `list` of `string` features.
- `category`: a `string` feature.
- `webnlg_id`: a `string` feature.

#### web_nlg_ru
- `gem_id`: a `string` feature.
- `input`: a `list` of `string` features.
- `target`: a `string` feature.
- `references`: a `list` of `string` features.
- `category`: a `string` feature.
- `webnlg_id`: a `string` feature.

#### wiki_auto_asset_turk
- `gem_id`: a `string` feature.
- `source_id`: a `string` feature.
- `target_id`: a `string` feature.
- `source`: a `string` feature.
- `target`: a `string` feature.
- `references`: a `list` of `string` features.

#### wiki_lingua_es_en
- `gem_id`: a `string` feature.
- `source`: a `string` feature.
- `target`: a `string` feature.
- `references`: a `list` of `string` features.

#### wiki_lingua_ru_en
- `gem_id`: a `string` feature.
- `source`: a `string` feature.
- `target`: a `string` feature.
- `references`: a `list` of `string` features.

#### wiki_lingua_tr_en
- `gem_id`: a `string` feature.
- `source`: a `string` feature.
- `target`: a `string` feature.
- `references`: a `list` of `string` features.

#### wiki_lingua_vi_en
- `gem_id`: a `string` feature.
- `source`: a `string` feature.
- `target`: a `string` feature.
- `references`: a `list` of `string` features.

#### xsum
- `gem_id`: a `string` feature.
- `xsum_id`: a `string` feature.
- `document`: a `string` feature.
- `target`: a `string` feature.
- `references`: a `list` of `string` features.

### Data Splits

#### common_gen

|          |train|validation|test|
|----------|----:|---------:|---:|
|common_gen|67389|       993|1497|

#### cs_restaurants

|              |train|validation|test|
|--------------|----:|---------:|---:|
|cs_restaurants| 3569|       781| 842|

#### dart

|    |train|validation|test|
|----|----:|---------:|---:|
|dart|62659|      2768|6959|

#### e2e_nlg

|       |train|validation|test|
|-------|----:|---------:|---:|
|e2e_nlg|33525|      4299|4693|

#### mlsum_de

|        |train |validation|test |
|--------|-----:|---------:|----:|
|mlsum_de|220748|     11392|10695|

#### mlsum_es

|        |train |validation|test |
|--------|-----:|---------:|----:|
|mlsum_es|259886|      9977|13365|

#### schema_guided_dialog

|                    |train |validation|test |
|--------------------|-----:|---------:|----:|
|schema_guided_dialog|164982|     10000|10000|

#### totto

|     |train |validation|test|
|-----|-----:|---------:|---:|
|totto|121153|      7700|7700|

#### web_nlg_en

|          |train|validation|test|
|----------|----:|---------:|---:|
|web_nlg_en|35426|      1667|1779|

#### web_nlg_ru

|          |train|validation|test|
|----------|----:|---------:|---:|
|web_nlg_ru|14630|       790|1102|

#### wiki_auto_asset_turk

|                    |train |validation|test_asset|test_turk|
|--------------------|-----:|---------:|---------:|--------:|
|wiki_auto_asset_turk|373801|     73249|       359|      359|

#### wiki_lingua_es_en

|                 |train|validation|test |
|-----------------|----:|---------:|----:|
|wiki_lingua_es_en|79515|      8835|19797|

#### wiki_lingua_ru_en

|                 |train|validation|test|
|-----------------|----:|---------:|---:|
|wiki_lingua_ru_en|36898|      4100|9094|

#### wiki_lingua_tr_en

|                 |train|validation|test|
|-----------------|----:|---------:|---:|
|wiki_lingua_tr_en| 3193|       355| 808|

#### wiki_lingua_vi_en

|                 |train|validation|test|
|-----------------|----:|---------:|---:|
|wiki_lingua_vi_en| 9206|      1023|2167|

#### xsum

|    |train|validation|test|
|----|----:|---------:|---:|
|xsum|23206|      1117|1166|

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

CC-BY-SA-4.0

### Citation Information

```
@article{gem_benchmark,
  author    = {Sebastian Gehrmann and
               Tosin P. Adewumi and
               Karmanya Aggarwal and
               Pawan Sasanka Ammanamanchi and
               Aremu Anuoluwapo and
               Antoine Bosselut and
               Khyathi Raghavi Chandu and
               Miruna{-}Adriana Clinciu and
               Dipanjan Das and
               Kaustubh D. Dhole and
               Wanyu Du and
               Esin Durmus and
               Ondrej Dusek and
               Chris Emezue and
               Varun Gangal and
               Cristina Garbacea and
               Tatsunori Hashimoto and
               Yufang Hou and
               Yacine Jernite and
               Harsh Jhamtani and
               Yangfeng Ji and
               Shailza Jolly and
               Dhruv Kumar and
               Faisal Ladhak and
               Aman Madaan and
               Mounica Maddela and
               Khyati Mahajan and
               Saad Mahamood and
               Bodhisattwa Prasad Majumder and
               Pedro Henrique Martins and
               Angelina McMillan{-}Major and
               Simon Mille and
               Emiel van Miltenburg and
               Moin Nadeem and
               Shashi Narayan and
               Vitaly Nikolaev and
               Rubungo Andre Niyongabo and
               Salomey Osei and
               Ankur P. Parikh and
               Laura Perez{-}Beltrachini and
               Niranjan Ramesh Rao and
               Vikas Raunak and
               Juan Diego Rodriguez and
               Sashank Santhanam and
               Jo{\~{a}}o Sedoc and
               Thibault Sellam and
               Samira Shaikh and
               Anastasia Shimorina and
               Marco Antonio Sobrevilla Cabezudo and
               Hendrik Strobelt and
               Nishant Subramani and
               Wei Xu and
               Diyi Yang and
               Akhila Yerukola and
               Jiawei Zhou},
  title     = {The {GEM} Benchmark: Natural Language Generation, its Evaluation and
               Metrics},
  journal   = {CoRR},
  volume    = {abs/2102.01672},
  year      = {2021},
  url       = {https://arxiv.org/abs/2102.01672},
  archivePrefix = {arXiv},
  eprint    = {2102.01672}
}
```

### Contributions

Thanks to [@yjernite](https://github.com/yjernite) for adding this dataset.