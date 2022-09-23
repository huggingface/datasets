---
annotations_creators:
- crowdsourced
language_creators:
- machine-generated
language:
- en
license:
- unknown
multilinguality:
- monolingual
pretty_name: BLiMP
size_categories:
- 10K<n<100K
source_datasets:
- original
task_categories:
- text-classification
task_ids:
- acceptability-classification
paperswithcode_id: blimp
dataset_info:
- config_name: adjunct_island
  features:
  - name: sentence_good
    dtype: string
  - name: sentence_bad
    dtype: string
  - name: field
    dtype: string
  - name: linguistics_term
    dtype: string
  - name: UID
    dtype: string
  - name: simple_LM_method
    dtype: bool
  - name: one_prefix_method
    dtype: bool
  - name: two_prefix_method
    dtype: bool
  - name: lexically_identical
    dtype: bool
  - name: pair_id
    dtype: int32
  splits:
  - name: train
    num_bytes: 167289
    num_examples: 1000
  download_size: 359284
  dataset_size: 167289
- config_name: anaphor_gender_agreement
  features:
  - name: sentence_good
    dtype: string
  - name: sentence_bad
    dtype: string
  - name: field
    dtype: string
  - name: linguistics_term
    dtype: string
  - name: UID
    dtype: string
  - name: simple_LM_method
    dtype: bool
  - name: one_prefix_method
    dtype: bool
  - name: two_prefix_method
    dtype: bool
  - name: lexically_identical
    dtype: bool
  - name: pair_id
    dtype: int32
  splits:
  - name: train
    num_bytes: 132313
    num_examples: 1000
  download_size: 436749
  dataset_size: 132313
- config_name: anaphor_number_agreement
  features:
  - name: sentence_good
    dtype: string
  - name: sentence_bad
    dtype: string
  - name: field
    dtype: string
  - name: linguistics_term
    dtype: string
  - name: UID
    dtype: string
  - name: simple_LM_method
    dtype: bool
  - name: one_prefix_method
    dtype: bool
  - name: two_prefix_method
    dtype: bool
  - name: lexically_identical
    dtype: bool
  - name: pair_id
    dtype: int32
  splits:
  - name: train
    num_bytes: 141274
    num_examples: 1000
  download_size: 450861
  dataset_size: 141274
- config_name: animate_subject_passive
  features:
  - name: sentence_good
    dtype: string
  - name: sentence_bad
    dtype: string
  - name: field
    dtype: string
  - name: linguistics_term
    dtype: string
  - name: UID
    dtype: string
  - name: simple_LM_method
    dtype: bool
  - name: one_prefix_method
    dtype: bool
  - name: two_prefix_method
    dtype: bool
  - name: lexically_identical
    dtype: bool
  - name: pair_id
    dtype: int32
  splits:
  - name: train
    num_bytes: 145818
    num_examples: 1000
  download_size: 462292
  dataset_size: 145818
- config_name: animate_subject_trans
  features:
  - name: sentence_good
    dtype: string
  - name: sentence_bad
    dtype: string
  - name: field
    dtype: string
  - name: linguistics_term
    dtype: string
  - name: UID
    dtype: string
  - name: simple_LM_method
    dtype: bool
  - name: one_prefix_method
    dtype: bool
  - name: two_prefix_method
    dtype: bool
  - name: lexically_identical
    dtype: bool
  - name: pair_id
    dtype: int32
  splits:
  - name: train
    num_bytes: 129193
    num_examples: 1000
  download_size: 433098
  dataset_size: 129193
- config_name: causative
  features:
  - name: sentence_good
    dtype: string
  - name: sentence_bad
    dtype: string
  - name: field
    dtype: string
  - name: linguistics_term
    dtype: string
  - name: UID
    dtype: string
  - name: simple_LM_method
    dtype: bool
  - name: one_prefix_method
    dtype: bool
  - name: two_prefix_method
    dtype: bool
  - name: lexically_identical
    dtype: bool
  - name: pair_id
    dtype: int32
  splits:
  - name: train
    num_bytes: 124167
    num_examples: 1000
  download_size: 317162
  dataset_size: 124167
- config_name: complex_NP_island
  features:
  - name: sentence_good
    dtype: string
  - name: sentence_bad
    dtype: string
  - name: field
    dtype: string
  - name: linguistics_term
    dtype: string
  - name: UID
    dtype: string
  - name: simple_LM_method
    dtype: bool
  - name: one_prefix_method
    dtype: bool
  - name: two_prefix_method
    dtype: bool
  - name: lexically_identical
    dtype: bool
  - name: pair_id
    dtype: int32
  splits:
  - name: train
    num_bytes: 200367
    num_examples: 1000
  download_size: 392362
  dataset_size: 200367
- config_name: coordinate_structure_constraint_complex_left_branch
  features:
  - name: sentence_good
    dtype: string
  - name: sentence_bad
    dtype: string
  - name: field
    dtype: string
  - name: linguistics_term
    dtype: string
  - name: UID
    dtype: string
  - name: simple_LM_method
    dtype: bool
  - name: one_prefix_method
    dtype: bool
  - name: two_prefix_method
    dtype: bool
  - name: lexically_identical
    dtype: bool
  - name: pair_id
    dtype: int32
  splits:
  - name: train
    num_bytes: 212307
    num_examples: 1000
  download_size: 571696
  dataset_size: 212307
- config_name: coordinate_structure_constraint_object_extraction
  features:
  - name: sentence_good
    dtype: string
  - name: sentence_bad
    dtype: string
  - name: field
    dtype: string
  - name: linguistics_term
    dtype: string
  - name: UID
    dtype: string
  - name: simple_LM_method
    dtype: bool
  - name: one_prefix_method
    dtype: bool
  - name: two_prefix_method
    dtype: bool
  - name: lexically_identical
    dtype: bool
  - name: pair_id
    dtype: int32
  splits:
  - name: train
    num_bytes: 173050
    num_examples: 1000
  download_size: 366045
  dataset_size: 173050
- config_name: determiner_noun_agreement_1
  features:
  - name: sentence_good
    dtype: string
  - name: sentence_bad
    dtype: string
  - name: field
    dtype: string
  - name: linguistics_term
    dtype: string
  - name: UID
    dtype: string
  - name: simple_LM_method
    dtype: bool
  - name: one_prefix_method
    dtype: bool
  - name: two_prefix_method
    dtype: bool
  - name: lexically_identical
    dtype: bool
  - name: pair_id
    dtype: int32
  splits:
  - name: train
    num_bytes: 157515
    num_examples: 1000
  download_size: 468642
  dataset_size: 157515
- config_name: determiner_noun_agreement_2
  features:
  - name: sentence_good
    dtype: string
  - name: sentence_bad
    dtype: string
  - name: field
    dtype: string
  - name: linguistics_term
    dtype: string
  - name: UID
    dtype: string
  - name: simple_LM_method
    dtype: bool
  - name: one_prefix_method
    dtype: bool
  - name: two_prefix_method
    dtype: bool
  - name: lexically_identical
    dtype: bool
  - name: pair_id
    dtype: int32
  splits:
  - name: train
    num_bytes: 157599
    num_examples: 1000
  download_size: 488856
  dataset_size: 157599
- config_name: determiner_noun_agreement_irregular_1
  features:
  - name: sentence_good
    dtype: string
  - name: sentence_bad
    dtype: string
  - name: field
    dtype: string
  - name: linguistics_term
    dtype: string
  - name: UID
    dtype: string
  - name: simple_LM_method
    dtype: bool
  - name: one_prefix_method
    dtype: bool
  - name: two_prefix_method
    dtype: bool
  - name: lexically_identical
    dtype: bool
  - name: pair_id
    dtype: int32
  splits:
  - name: train
    num_bytes: 165868
    num_examples: 1000
  download_size: 474932
  dataset_size: 165868
- config_name: determiner_noun_agreement_irregular_2
  features:
  - name: sentence_good
    dtype: string
  - name: sentence_bad
    dtype: string
  - name: field
    dtype: string
  - name: linguistics_term
    dtype: string
  - name: UID
    dtype: string
  - name: simple_LM_method
    dtype: bool
  - name: one_prefix_method
    dtype: bool
  - name: two_prefix_method
    dtype: bool
  - name: lexically_identical
    dtype: bool
  - name: pair_id
    dtype: int32
  splits:
  - name: train
    num_bytes: 162469
    num_examples: 1000
  download_size: 490854
  dataset_size: 162469
- config_name: determiner_noun_agreement_with_adj_2
  features:
  - name: sentence_good
    dtype: string
  - name: sentence_bad
    dtype: string
  - name: field
    dtype: string
  - name: linguistics_term
    dtype: string
  - name: UID
    dtype: string
  - name: simple_LM_method
    dtype: bool
  - name: one_prefix_method
    dtype: bool
  - name: two_prefix_method
    dtype: bool
  - name: lexically_identical
    dtype: bool
  - name: pair_id
    dtype: int32
  splits:
  - name: train
    num_bytes: 181061
    num_examples: 1000
  download_size: 526806
  dataset_size: 181061
- config_name: determiner_noun_agreement_with_adj_irregular_1
  features:
  - name: sentence_good
    dtype: string
  - name: sentence_bad
    dtype: string
  - name: field
    dtype: string
  - name: linguistics_term
    dtype: string
  - name: UID
    dtype: string
  - name: simple_LM_method
    dtype: bool
  - name: one_prefix_method
    dtype: bool
  - name: two_prefix_method
    dtype: bool
  - name: lexically_identical
    dtype: bool
  - name: pair_id
    dtype: int32
  splits:
  - name: train
    num_bytes: 185924
    num_examples: 1000
  download_size: 499664
  dataset_size: 185924
- config_name: determiner_noun_agreement_with_adj_irregular_2
  features:
  - name: sentence_good
    dtype: string
  - name: sentence_bad
    dtype: string
  - name: field
    dtype: string
  - name: linguistics_term
    dtype: string
  - name: UID
    dtype: string
  - name: simple_LM_method
    dtype: bool
  - name: one_prefix_method
    dtype: bool
  - name: two_prefix_method
    dtype: bool
  - name: lexically_identical
    dtype: bool
  - name: pair_id
    dtype: int32
  splits:
  - name: train
    num_bytes: 185791
    num_examples: 1000
  download_size: 528528
  dataset_size: 185791
- config_name: determiner_noun_agreement_with_adjective_1
  features:
  - name: sentence_good
    dtype: string
  - name: sentence_bad
    dtype: string
  - name: field
    dtype: string
  - name: linguistics_term
    dtype: string
  - name: UID
    dtype: string
  - name: simple_LM_method
    dtype: bool
  - name: one_prefix_method
    dtype: bool
  - name: two_prefix_method
    dtype: bool
  - name: lexically_identical
    dtype: bool
  - name: pair_id
    dtype: int32
  splits:
  - name: train
    num_bytes: 186521
    num_examples: 1000
  download_size: 504676
  dataset_size: 186521
- config_name: distractor_agreement_relational_noun
  features:
  - name: sentence_good
    dtype: string
  - name: sentence_bad
    dtype: string
  - name: field
    dtype: string
  - name: linguistics_term
    dtype: string
  - name: UID
    dtype: string
  - name: simple_LM_method
    dtype: bool
  - name: one_prefix_method
    dtype: bool
  - name: two_prefix_method
    dtype: bool
  - name: lexically_identical
    dtype: bool
  - name: pair_id
    dtype: int32
  splits:
  - name: train
    num_bytes: 192868
    num_examples: 1000
  download_size: 525650
  dataset_size: 192868
- config_name: distractor_agreement_relative_clause
  features:
  - name: sentence_good
    dtype: string
  - name: sentence_bad
    dtype: string
  - name: field
    dtype: string
  - name: linguistics_term
    dtype: string
  - name: UID
    dtype: string
  - name: simple_LM_method
    dtype: bool
  - name: one_prefix_method
    dtype: bool
  - name: two_prefix_method
    dtype: bool
  - name: lexically_identical
    dtype: bool
  - name: pair_id
    dtype: int32
  splits:
  - name: train
    num_bytes: 218151
    num_examples: 1000
  download_size: 564770
  dataset_size: 218151
- config_name: drop_argument
  features:
  - name: sentence_good
    dtype: string
  - name: sentence_bad
    dtype: string
  - name: field
    dtype: string
  - name: linguistics_term
    dtype: string
  - name: UID
    dtype: string
  - name: simple_LM_method
    dtype: bool
  - name: one_prefix_method
    dtype: bool
  - name: two_prefix_method
    dtype: bool
  - name: lexically_identical
    dtype: bool
  - name: pair_id
    dtype: int32
  splits:
  - name: train
    num_bytes: 111201
    num_examples: 1000
  download_size: 304196
  dataset_size: 111201
- config_name: ellipsis_n_bar_1
  features:
  - name: sentence_good
    dtype: string
  - name: sentence_bad
    dtype: string
  - name: field
    dtype: string
  - name: linguistics_term
    dtype: string
  - name: UID
    dtype: string
  - name: simple_LM_method
    dtype: bool
  - name: one_prefix_method
    dtype: bool
  - name: two_prefix_method
    dtype: bool
  - name: lexically_identical
    dtype: bool
  - name: pair_id
    dtype: int32
  splits:
  - name: train
    num_bytes: 218985
    num_examples: 1000
  download_size: 411980
  dataset_size: 218985
- config_name: ellipsis_n_bar_2
  features:
  - name: sentence_good
    dtype: string
  - name: sentence_bad
    dtype: string
  - name: field
    dtype: string
  - name: linguistics_term
    dtype: string
  - name: UID
    dtype: string
  - name: simple_LM_method
    dtype: bool
  - name: one_prefix_method
    dtype: bool
  - name: two_prefix_method
    dtype: bool
  - name: lexically_identical
    dtype: bool
  - name: pair_id
    dtype: int32
  splits:
  - name: train
    num_bytes: 234556
    num_examples: 1000
  download_size: 427551
  dataset_size: 234556
- config_name: existential_there_object_raising
  features:
  - name: sentence_good
    dtype: string
  - name: sentence_bad
    dtype: string
  - name: field
    dtype: string
  - name: linguistics_term
    dtype: string
  - name: UID
    dtype: string
  - name: simple_LM_method
    dtype: bool
  - name: one_prefix_method
    dtype: bool
  - name: two_prefix_method
    dtype: bool
  - name: lexically_identical
    dtype: bool
  - name: pair_id
    dtype: int32
  splits:
  - name: train
    num_bytes: 225136
    num_examples: 1000
  download_size: 550672
  dataset_size: 225136
- config_name: existential_there_quantifiers_1
  features:
  - name: sentence_good
    dtype: string
  - name: sentence_bad
    dtype: string
  - name: field
    dtype: string
  - name: linguistics_term
    dtype: string
  - name: UID
    dtype: string
  - name: simple_LM_method
    dtype: bool
  - name: one_prefix_method
    dtype: bool
  - name: two_prefix_method
    dtype: bool
  - name: lexically_identical
    dtype: bool
  - name: pair_id
    dtype: int32
  splits:
  - name: train
    num_bytes: 164326
    num_examples: 1000
  download_size: 357321
  dataset_size: 164326
- config_name: existential_there_quantifiers_2
  features:
  - name: sentence_good
    dtype: string
  - name: sentence_bad
    dtype: string
  - name: field
    dtype: string
  - name: linguistics_term
    dtype: string
  - name: UID
    dtype: string
  - name: simple_LM_method
    dtype: bool
  - name: one_prefix_method
    dtype: bool
  - name: two_prefix_method
    dtype: bool
  - name: lexically_identical
    dtype: bool
  - name: pair_id
    dtype: int32
  splits:
  - name: train
    num_bytes: 166221
    num_examples: 1000
  download_size: 359216
  dataset_size: 166221
- config_name: existential_there_subject_raising
  features:
  - name: sentence_good
    dtype: string
  - name: sentence_bad
    dtype: string
  - name: field
    dtype: string
  - name: linguistics_term
    dtype: string
  - name: UID
    dtype: string
  - name: simple_LM_method
    dtype: bool
  - name: one_prefix_method
    dtype: bool
  - name: two_prefix_method
    dtype: bool
  - name: lexically_identical
    dtype: bool
  - name: pair_id
    dtype: int32
  splits:
  - name: train
    num_bytes: 201458
    num_examples: 1000
  download_size: 394453
  dataset_size: 201458
- config_name: expletive_it_object_raising
  features:
  - name: sentence_good
    dtype: string
  - name: sentence_bad
    dtype: string
  - name: field
    dtype: string
  - name: linguistics_term
    dtype: string
  - name: UID
    dtype: string
  - name: simple_LM_method
    dtype: bool
  - name: one_prefix_method
    dtype: bool
  - name: two_prefix_method
    dtype: bool
  - name: lexically_identical
    dtype: bool
  - name: pair_id
    dtype: int32
  splits:
  - name: train
    num_bytes: 240010
    num_examples: 1000
  download_size: 587648
  dataset_size: 240010
- config_name: inchoative
  features:
  - name: sentence_good
    dtype: string
  - name: sentence_bad
    dtype: string
  - name: field
    dtype: string
  - name: linguistics_term
    dtype: string
  - name: UID
    dtype: string
  - name: simple_LM_method
    dtype: bool
  - name: one_prefix_method
    dtype: bool
  - name: two_prefix_method
    dtype: bool
  - name: lexically_identical
    dtype: bool
  - name: pair_id
    dtype: int32
  splits:
  - name: train
    num_bytes: 105714
    num_examples: 1000
  download_size: 298709
  dataset_size: 105714
- config_name: intransitive
  features:
  - name: sentence_good
    dtype: string
  - name: sentence_bad
    dtype: string
  - name: field
    dtype: string
  - name: linguistics_term
    dtype: string
  - name: UID
    dtype: string
  - name: simple_LM_method
    dtype: bool
  - name: one_prefix_method
    dtype: bool
  - name: two_prefix_method
    dtype: bool
  - name: lexically_identical
    dtype: bool
  - name: pair_id
    dtype: int32
  splits:
  - name: train
    num_bytes: 112492
    num_examples: 1000
  download_size: 305487
  dataset_size: 112492
- config_name: irregular_past_participle_adjectives
  features:
  - name: sentence_good
    dtype: string
  - name: sentence_bad
    dtype: string
  - name: field
    dtype: string
  - name: linguistics_term
    dtype: string
  - name: UID
    dtype: string
  - name: simple_LM_method
    dtype: bool
  - name: one_prefix_method
    dtype: bool
  - name: two_prefix_method
    dtype: bool
  - name: lexically_identical
    dtype: bool
  - name: pair_id
    dtype: int32
  splits:
  - name: train
    num_bytes: 146056
    num_examples: 1000
  download_size: 444520
  dataset_size: 146056
- config_name: irregular_past_participle_verbs
  features:
  - name: sentence_good
    dtype: string
  - name: sentence_bad
    dtype: string
  - name: field
    dtype: string
  - name: linguistics_term
    dtype: string
  - name: UID
    dtype: string
  - name: simple_LM_method
    dtype: bool
  - name: one_prefix_method
    dtype: bool
  - name: two_prefix_method
    dtype: bool
  - name: lexically_identical
    dtype: bool
  - name: pair_id
    dtype: int32
  splits:
  - name: train
    num_bytes: 127087
    num_examples: 1000
  download_size: 420119
  dataset_size: 127087
- config_name: irregular_plural_subject_verb_agreement_1
  features:
  - name: sentence_good
    dtype: string
  - name: sentence_bad
    dtype: string
  - name: field
    dtype: string
  - name: linguistics_term
    dtype: string
  - name: UID
    dtype: string
  - name: simple_LM_method
    dtype: bool
  - name: one_prefix_method
    dtype: bool
  - name: two_prefix_method
    dtype: bool
  - name: lexically_identical
    dtype: bool
  - name: pair_id
    dtype: int32
  splits:
  - name: train
    num_bytes: 166979
    num_examples: 1000
  download_size: 460705
  dataset_size: 166979
- config_name: irregular_plural_subject_verb_agreement_2
  features:
  - name: sentence_good
    dtype: string
  - name: sentence_bad
    dtype: string
  - name: field
    dtype: string
  - name: linguistics_term
    dtype: string
  - name: UID
    dtype: string
  - name: simple_LM_method
    dtype: bool
  - name: one_prefix_method
    dtype: bool
  - name: two_prefix_method
    dtype: bool
  - name: lexically_identical
    dtype: bool
  - name: pair_id
    dtype: int32
  splits:
  - name: train
    num_bytes: 155238
    num_examples: 1000
  download_size: 453376
  dataset_size: 155238
- config_name: left_branch_island_echo_question
  features:
  - name: sentence_good
    dtype: string
  - name: sentence_bad
    dtype: string
  - name: field
    dtype: string
  - name: linguistics_term
    dtype: string
  - name: UID
    dtype: string
  - name: simple_LM_method
    dtype: bool
  - name: one_prefix_method
    dtype: bool
  - name: two_prefix_method
    dtype: bool
  - name: lexically_identical
    dtype: bool
  - name: pair_id
    dtype: int32
  splits:
  - name: train
    num_bytes: 149235
    num_examples: 1000
  download_size: 482617
  dataset_size: 149235
- config_name: left_branch_island_simple_question
  features:
  - name: sentence_good
    dtype: string
  - name: sentence_bad
    dtype: string
  - name: field
    dtype: string
  - name: linguistics_term
    dtype: string
  - name: UID
    dtype: string
  - name: simple_LM_method
    dtype: bool
  - name: one_prefix_method
    dtype: bool
  - name: two_prefix_method
    dtype: bool
  - name: lexically_identical
    dtype: bool
  - name: pair_id
    dtype: int32
  splits:
  - name: train
    num_bytes: 151455
    num_examples: 1000
  download_size: 343450
  dataset_size: 151455
- config_name: matrix_question_npi_licensor_present
  features:
  - name: sentence_good
    dtype: string
  - name: sentence_bad
    dtype: string
  - name: field
    dtype: string
  - name: linguistics_term
    dtype: string
  - name: UID
    dtype: string
  - name: simple_LM_method
    dtype: bool
  - name: one_prefix_method
    dtype: bool
  - name: two_prefix_method
    dtype: bool
  - name: lexically_identical
    dtype: bool
  - name: pair_id
    dtype: int32
  splits:
  - name: train
    num_bytes: 154657
    num_examples: 1000
  download_size: 457806
  dataset_size: 154657
- config_name: npi_present_1
  features:
  - name: sentence_good
    dtype: string
  - name: sentence_bad
    dtype: string
  - name: field
    dtype: string
  - name: linguistics_term
    dtype: string
  - name: UID
    dtype: string
  - name: simple_LM_method
    dtype: bool
  - name: one_prefix_method
    dtype: bool
  - name: two_prefix_method
    dtype: bool
  - name: lexically_identical
    dtype: bool
  - name: pair_id
    dtype: int32
  splits:
  - name: train
    num_bytes: 139860
    num_examples: 1000
  download_size: 438013
  dataset_size: 139860
- config_name: npi_present_2
  features:
  - name: sentence_good
    dtype: string
  - name: sentence_bad
    dtype: string
  - name: field
    dtype: string
  - name: linguistics_term
    dtype: string
  - name: UID
    dtype: string
  - name: simple_LM_method
    dtype: bool
  - name: one_prefix_method
    dtype: bool
  - name: two_prefix_method
    dtype: bool
  - name: lexically_identical
    dtype: bool
  - name: pair_id
    dtype: int32
  splits:
  - name: train
    num_bytes: 129031
    num_examples: 1000
  download_size: 422136
  dataset_size: 129031
- config_name: only_npi_licensor_present
  features:
  - name: sentence_good
    dtype: string
  - name: sentence_bad
    dtype: string
  - name: field
    dtype: string
  - name: linguistics_term
    dtype: string
  - name: UID
    dtype: string
  - name: simple_LM_method
    dtype: bool
  - name: one_prefix_method
    dtype: bool
  - name: two_prefix_method
    dtype: bool
  - name: lexically_identical
    dtype: bool
  - name: pair_id
    dtype: int32
  splits:
  - name: train
    num_bytes: 149911
    num_examples: 1000
  download_size: 459170
  dataset_size: 149911
- config_name: only_npi_scope
  features:
  - name: sentence_good
    dtype: string
  - name: sentence_bad
    dtype: string
  - name: field
    dtype: string
  - name: linguistics_term
    dtype: string
  - name: UID
    dtype: string
  - name: simple_LM_method
    dtype: bool
  - name: one_prefix_method
    dtype: bool
  - name: two_prefix_method
    dtype: bool
  - name: lexically_identical
    dtype: bool
  - name: pair_id
    dtype: int32
  splits:
  - name: train
    num_bytes: 210297
    num_examples: 1000
  download_size: 583720
  dataset_size: 210297
- config_name: passive_1
  features:
  - name: sentence_good
    dtype: string
  - name: sentence_bad
    dtype: string
  - name: field
    dtype: string
  - name: linguistics_term
    dtype: string
  - name: UID
    dtype: string
  - name: simple_LM_method
    dtype: bool
  - name: one_prefix_method
    dtype: bool
  - name: two_prefix_method
    dtype: bool
  - name: lexically_identical
    dtype: bool
  - name: pair_id
    dtype: int32
  splits:
  - name: train
    num_bytes: 147277
    num_examples: 1000
  download_size: 340272
  dataset_size: 147277
- config_name: passive_2
  features:
  - name: sentence_good
    dtype: string
  - name: sentence_bad
    dtype: string
  - name: field
    dtype: string
  - name: linguistics_term
    dtype: string
  - name: UID
    dtype: string
  - name: simple_LM_method
    dtype: bool
  - name: one_prefix_method
    dtype: bool
  - name: two_prefix_method
    dtype: bool
  - name: lexically_identical
    dtype: bool
  - name: pair_id
    dtype: int32
  splits:
  - name: train
    num_bytes: 115355
    num_examples: 1000
  download_size: 308350
  dataset_size: 115355
- config_name: principle_A_c_command
  features:
  - name: sentence_good
    dtype: string
  - name: sentence_bad
    dtype: string
  - name: field
    dtype: string
  - name: linguistics_term
    dtype: string
  - name: UID
    dtype: string
  - name: simple_LM_method
    dtype: bool
  - name: one_prefix_method
    dtype: bool
  - name: two_prefix_method
    dtype: bool
  - name: lexically_identical
    dtype: bool
  - name: pair_id
    dtype: int32
  splits:
  - name: train
    num_bytes: 189885
    num_examples: 1000
  download_size: 527689
  dataset_size: 189885
- config_name: principle_A_case_1
  features:
  - name: sentence_good
    dtype: string
  - name: sentence_bad
    dtype: string
  - name: field
    dtype: string
  - name: linguistics_term
    dtype: string
  - name: UID
    dtype: string
  - name: simple_LM_method
    dtype: bool
  - name: one_prefix_method
    dtype: bool
  - name: two_prefix_method
    dtype: bool
  - name: lexically_identical
    dtype: bool
  - name: pair_id
    dtype: int32
  splits:
  - name: train
    num_bytes: 171793
    num_examples: 1000
  download_size: 477239
  dataset_size: 171793
- config_name: principle_A_case_2
  features:
  - name: sentence_good
    dtype: string
  - name: sentence_bad
    dtype: string
  - name: field
    dtype: string
  - name: linguistics_term
    dtype: string
  - name: UID
    dtype: string
  - name: simple_LM_method
    dtype: bool
  - name: one_prefix_method
    dtype: bool
  - name: two_prefix_method
    dtype: bool
  - name: lexically_identical
    dtype: bool
  - name: pair_id
    dtype: int32
  splits:
  - name: train
    num_bytes: 171807
    num_examples: 1000
  download_size: 492973
  dataset_size: 171807
- config_name: principle_A_domain_1
  features:
  - name: sentence_good
    dtype: string
  - name: sentence_bad
    dtype: string
  - name: field
    dtype: string
  - name: linguistics_term
    dtype: string
  - name: UID
    dtype: string
  - name: simple_LM_method
    dtype: bool
  - name: one_prefix_method
    dtype: bool
  - name: two_prefix_method
    dtype: bool
  - name: lexically_identical
    dtype: bool
  - name: pair_id
    dtype: int32
  splits:
  - name: train
    num_bytes: 172565
    num_examples: 1000
  download_size: 499865
  dataset_size: 172565
- config_name: principle_A_domain_2
  features:
  - name: sentence_good
    dtype: string
  - name: sentence_bad
    dtype: string
  - name: field
    dtype: string
  - name: linguistics_term
    dtype: string
  - name: UID
    dtype: string
  - name: simple_LM_method
    dtype: bool
  - name: one_prefix_method
    dtype: bool
  - name: two_prefix_method
    dtype: bool
  - name: lexically_identical
    dtype: bool
  - name: pair_id
    dtype: int32
  splits:
  - name: train
    num_bytes: 166728
    num_examples: 1000
  download_size: 493189
  dataset_size: 166728
- config_name: principle_A_domain_3
  features:
  - name: sentence_good
    dtype: string
  - name: sentence_bad
    dtype: string
  - name: field
    dtype: string
  - name: linguistics_term
    dtype: string
  - name: UID
    dtype: string
  - name: simple_LM_method
    dtype: bool
  - name: one_prefix_method
    dtype: bool
  - name: two_prefix_method
    dtype: bool
  - name: lexically_identical
    dtype: bool
  - name: pair_id
    dtype: int32
  splits:
  - name: train
    num_bytes: 160393
    num_examples: 1000
  download_size: 513886
  dataset_size: 160393
- config_name: principle_A_reconstruction
  features:
  - name: sentence_good
    dtype: string
  - name: sentence_bad
    dtype: string
  - name: field
    dtype: string
  - name: linguistics_term
    dtype: string
  - name: UID
    dtype: string
  - name: simple_LM_method
    dtype: bool
  - name: one_prefix_method
    dtype: bool
  - name: two_prefix_method
    dtype: bool
  - name: lexically_identical
    dtype: bool
  - name: pair_id
    dtype: int32
  splits:
  - name: train
    num_bytes: 153499
    num_examples: 1000
  download_size: 345494
  dataset_size: 153499
- config_name: regular_plural_subject_verb_agreement_1
  features:
  - name: sentence_good
    dtype: string
  - name: sentence_bad
    dtype: string
  - name: field
    dtype: string
  - name: linguistics_term
    dtype: string
  - name: UID
    dtype: string
  - name: simple_LM_method
    dtype: bool
  - name: one_prefix_method
    dtype: bool
  - name: two_prefix_method
    dtype: bool
  - name: lexically_identical
    dtype: bool
  - name: pair_id
    dtype: int32
  splits:
  - name: train
    num_bytes: 160214
    num_examples: 1000
  download_size: 451850
  dataset_size: 160214
- config_name: regular_plural_subject_verb_agreement_2
  features:
  - name: sentence_good
    dtype: string
  - name: sentence_bad
    dtype: string
  - name: field
    dtype: string
  - name: linguistics_term
    dtype: string
  - name: UID
    dtype: string
  - name: simple_LM_method
    dtype: bool
  - name: one_prefix_method
    dtype: bool
  - name: two_prefix_method
    dtype: bool
  - name: lexically_identical
    dtype: bool
  - name: pair_id
    dtype: int32
  splits:
  - name: train
    num_bytes: 155004
    num_examples: 1000
  download_size: 456477
  dataset_size: 155004
- config_name: sentential_negation_npi_licensor_present
  features:
  - name: sentence_good
    dtype: string
  - name: sentence_bad
    dtype: string
  - name: field
    dtype: string
  - name: linguistics_term
    dtype: string
  - name: UID
    dtype: string
  - name: simple_LM_method
    dtype: bool
  - name: one_prefix_method
    dtype: bool
  - name: two_prefix_method
    dtype: bool
  - name: lexically_identical
    dtype: bool
  - name: pair_id
    dtype: int32
  splits:
  - name: train
    num_bytes: 173259
    num_examples: 1000
  download_size: 490996
  dataset_size: 173259
- config_name: sentential_negation_npi_scope
  features:
  - name: sentence_good
    dtype: string
  - name: sentence_bad
    dtype: string
  - name: field
    dtype: string
  - name: linguistics_term
    dtype: string
  - name: UID
    dtype: string
  - name: simple_LM_method
    dtype: bool
  - name: one_prefix_method
    dtype: bool
  - name: two_prefix_method
    dtype: bool
  - name: lexically_identical
    dtype: bool
  - name: pair_id
    dtype: int32
  splits:
  - name: train
    num_bytes: 233493
    num_examples: 1000
  download_size: 614930
  dataset_size: 233493
- config_name: sentential_subject_island
  features:
  - name: sentence_good
    dtype: string
  - name: sentence_bad
    dtype: string
  - name: field
    dtype: string
  - name: linguistics_term
    dtype: string
  - name: UID
    dtype: string
  - name: simple_LM_method
    dtype: bool
  - name: one_prefix_method
    dtype: bool
  - name: two_prefix_method
    dtype: bool
  - name: lexically_identical
    dtype: bool
  - name: pair_id
    dtype: int32
  splits:
  - name: train
    num_bytes: 173827
    num_examples: 1000
  download_size: 365822
  dataset_size: 173827
- config_name: superlative_quantifiers_1
  features:
  - name: sentence_good
    dtype: string
  - name: sentence_bad
    dtype: string
  - name: field
    dtype: string
  - name: linguistics_term
    dtype: string
  - name: UID
    dtype: string
  - name: simple_LM_method
    dtype: bool
  - name: one_prefix_method
    dtype: bool
  - name: two_prefix_method
    dtype: bool
  - name: lexically_identical
    dtype: bool
  - name: pair_id
    dtype: int32
  splits:
  - name: train
    num_bytes: 160685
    num_examples: 1000
  download_size: 381189
  dataset_size: 160685
- config_name: superlative_quantifiers_2
  features:
  - name: sentence_good
    dtype: string
  - name: sentence_bad
    dtype: string
  - name: field
    dtype: string
  - name: linguistics_term
    dtype: string
  - name: UID
    dtype: string
  - name: simple_LM_method
    dtype: bool
  - name: one_prefix_method
    dtype: bool
  - name: two_prefix_method
    dtype: bool
  - name: lexically_identical
    dtype: bool
  - name: pair_id
    dtype: int32
  splits:
  - name: train
    num_bytes: 160735
    num_examples: 1000
  download_size: 516120
  dataset_size: 160735
- config_name: tough_vs_raising_1
  features:
  - name: sentence_good
    dtype: string
  - name: sentence_bad
    dtype: string
  - name: field
    dtype: string
  - name: linguistics_term
    dtype: string
  - name: UID
    dtype: string
  - name: simple_LM_method
    dtype: bool
  - name: one_prefix_method
    dtype: bool
  - name: two_prefix_method
    dtype: bool
  - name: lexically_identical
    dtype: bool
  - name: pair_id
    dtype: int32
  splits:
  - name: train
    num_bytes: 150031
    num_examples: 1000
  download_size: 343026
  dataset_size: 150031
- config_name: tough_vs_raising_2
  features:
  - name: sentence_good
    dtype: string
  - name: sentence_bad
    dtype: string
  - name: field
    dtype: string
  - name: linguistics_term
    dtype: string
  - name: UID
    dtype: string
  - name: simple_LM_method
    dtype: bool
  - name: one_prefix_method
    dtype: bool
  - name: two_prefix_method
    dtype: bool
  - name: lexically_identical
    dtype: bool
  - name: pair_id
    dtype: int32
  splits:
  - name: train
    num_bytes: 171079
    num_examples: 1000
  download_size: 364074
  dataset_size: 171079
- config_name: transitive
  features:
  - name: sentence_good
    dtype: string
  - name: sentence_bad
    dtype: string
  - name: field
    dtype: string
  - name: linguistics_term
    dtype: string
  - name: UID
    dtype: string
  - name: simple_LM_method
    dtype: bool
  - name: one_prefix_method
    dtype: bool
  - name: two_prefix_method
    dtype: bool
  - name: lexically_identical
    dtype: bool
  - name: pair_id
    dtype: int32
  splits:
  - name: train
    num_bytes: 134499
    num_examples: 1000
  download_size: 460291
  dataset_size: 134499
- config_name: wh_island
  features:
  - name: sentence_good
    dtype: string
  - name: sentence_bad
    dtype: string
  - name: field
    dtype: string
  - name: linguistics_term
    dtype: string
  - name: UID
    dtype: string
  - name: simple_LM_method
    dtype: bool
  - name: one_prefix_method
    dtype: bool
  - name: two_prefix_method
    dtype: bool
  - name: lexically_identical
    dtype: bool
  - name: pair_id
    dtype: int32
  splits:
  - name: train
    num_bytes: 143735
    num_examples: 1000
  download_size: 448630
  dataset_size: 143735
- config_name: wh_questions_object_gap
  features:
  - name: sentence_good
    dtype: string
  - name: sentence_bad
    dtype: string
  - name: field
    dtype: string
  - name: linguistics_term
    dtype: string
  - name: UID
    dtype: string
  - name: simple_LM_method
    dtype: bool
  - name: one_prefix_method
    dtype: bool
  - name: two_prefix_method
    dtype: bool
  - name: lexically_identical
    dtype: bool
  - name: pair_id
    dtype: int32
  splits:
  - name: train
    num_bytes: 194440
    num_examples: 1000
  download_size: 387435
  dataset_size: 194440
- config_name: wh_questions_subject_gap
  features:
  - name: sentence_good
    dtype: string
  - name: sentence_bad
    dtype: string
  - name: field
    dtype: string
  - name: linguistics_term
    dtype: string
  - name: UID
    dtype: string
  - name: simple_LM_method
    dtype: bool
  - name: one_prefix_method
    dtype: bool
  - name: two_prefix_method
    dtype: bool
  - name: lexically_identical
    dtype: bool
  - name: pair_id
    dtype: int32
  splits:
  - name: train
    num_bytes: 196988
    num_examples: 1000
  download_size: 389983
  dataset_size: 196988
- config_name: wh_questions_subject_gap_long_distance
  features:
  - name: sentence_good
    dtype: string
  - name: sentence_bad
    dtype: string
  - name: field
    dtype: string
  - name: linguistics_term
    dtype: string
  - name: UID
    dtype: string
  - name: simple_LM_method
    dtype: bool
  - name: one_prefix_method
    dtype: bool
  - name: two_prefix_method
    dtype: bool
  - name: lexically_identical
    dtype: bool
  - name: pair_id
    dtype: int32
  splits:
  - name: train
    num_bytes: 269665
    num_examples: 1000
  download_size: 462660
  dataset_size: 269665
- config_name: wh_vs_that_no_gap
  features:
  - name: sentence_good
    dtype: string
  - name: sentence_bad
    dtype: string
  - name: field
    dtype: string
  - name: linguistics_term
    dtype: string
  - name: UID
    dtype: string
  - name: simple_LM_method
    dtype: bool
  - name: one_prefix_method
    dtype: bool
  - name: two_prefix_method
    dtype: bool
  - name: lexically_identical
    dtype: bool
  - name: pair_id
    dtype: int32
  splits:
  - name: train
    num_bytes: 190267
    num_examples: 1000
  download_size: 383262
  dataset_size: 190267
- config_name: wh_vs_that_no_gap_long_distance
  features:
  - name: sentence_good
    dtype: string
  - name: sentence_bad
    dtype: string
  - name: field
    dtype: string
  - name: linguistics_term
    dtype: string
  - name: UID
    dtype: string
  - name: simple_LM_method
    dtype: bool
  - name: one_prefix_method
    dtype: bool
  - name: two_prefix_method
    dtype: bool
  - name: lexically_identical
    dtype: bool
  - name: pair_id
    dtype: int32
  splits:
  - name: train
    num_bytes: 248434
    num_examples: 1000
  download_size: 441429
  dataset_size: 248434
- config_name: wh_vs_that_with_gap
  features:
  - name: sentence_good
    dtype: string
  - name: sentence_bad
    dtype: string
  - name: field
    dtype: string
  - name: linguistics_term
    dtype: string
  - name: UID
    dtype: string
  - name: simple_LM_method
    dtype: bool
  - name: one_prefix_method
    dtype: bool
  - name: two_prefix_method
    dtype: bool
  - name: lexically_identical
    dtype: bool
  - name: pair_id
    dtype: int32
  splits:
  - name: train
    num_bytes: 174781
    num_examples: 1000
  download_size: 367776
  dataset_size: 174781
- config_name: wh_vs_that_with_gap_long_distance
  features:
  - name: sentence_good
    dtype: string
  - name: sentence_bad
    dtype: string
  - name: field
    dtype: string
  - name: linguistics_term
    dtype: string
  - name: UID
    dtype: string
  - name: simple_LM_method
    dtype: bool
  - name: one_prefix_method
    dtype: bool
  - name: two_prefix_method
    dtype: bool
  - name: lexically_identical
    dtype: bool
  - name: pair_id
    dtype: int32
  splits:
  - name: train
    num_bytes: 232990
    num_examples: 1000
  download_size: 425985
  dataset_size: 232990
---

# Dataset Card for "blimp"

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

- **Homepage:** [https://github.com/alexwarstadt/blimp/tree/master/](https://github.com/alexwarstadt/blimp/tree/master/)
- **Repository:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Paper:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Point of Contact:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Size of downloaded dataset files:** 28.21 MB
- **Size of the generated dataset:** 10.92 MB
- **Total amount of disk used:** 39.13 MB

### Dataset Summary

BLiMP is a challenge set for evaluating what language models (LMs) know about
major grammatical phenomena in English. BLiMP consists of 67 sub-datasets, each
containing 1000 minimal pairs isolating specific contrasts in syntax,
morphology, or semantics. The data is automatically generated according to
expert-crafted grammars.

### Supported Tasks and Leaderboards

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Languages

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

## Dataset Structure

### Data Instances

#### adjunct_island

- **Size of downloaded dataset files:** 0.34 MB
- **Size of the generated dataset:** 0.16 MB
- **Total amount of disk used:** 0.50 MB

An example of 'train' looks as follows.
```
{
    "UID": "tough_vs_raising_1",
    "field": "syntax_semantics",
    "lexically_identical": false,
    "linguistics_term": "control_raising",
    "one_prefix_method": false,
    "pair_id": 2,
    "sentence_bad": "Benjamin's tutor was certain to boast about.",
    "sentence_good": "Benjamin's tutor was easy to boast about.",
    "simple_LM_method": true,
    "two_prefix_method": false
}
```

#### anaphor_gender_agreement

- **Size of downloaded dataset files:** 0.42 MB
- **Size of the generated dataset:** 0.13 MB
- **Total amount of disk used:** 0.54 MB

An example of 'train' looks as follows.
```
{
    "UID": "tough_vs_raising_1",
    "field": "syntax_semantics",
    "lexically_identical": false,
    "linguistics_term": "control_raising",
    "one_prefix_method": false,
    "pair_id": 2,
    "sentence_bad": "Benjamin's tutor was certain to boast about.",
    "sentence_good": "Benjamin's tutor was easy to boast about.",
    "simple_LM_method": true,
    "two_prefix_method": false
}
```

#### anaphor_number_agreement

- **Size of downloaded dataset files:** 0.43 MB
- **Size of the generated dataset:** 0.13 MB
- **Total amount of disk used:** 0.56 MB

An example of 'train' looks as follows.
```
{
    "UID": "tough_vs_raising_1",
    "field": "syntax_semantics",
    "lexically_identical": false,
    "linguistics_term": "control_raising",
    "one_prefix_method": false,
    "pair_id": 2,
    "sentence_bad": "Benjamin's tutor was certain to boast about.",
    "sentence_good": "Benjamin's tutor was easy to boast about.",
    "simple_LM_method": true,
    "two_prefix_method": false
}
```

#### animate_subject_passive

- **Size of downloaded dataset files:** 0.44 MB
- **Size of the generated dataset:** 0.14 MB
- **Total amount of disk used:** 0.58 MB

An example of 'train' looks as follows.
```
{
    "UID": "tough_vs_raising_1",
    "field": "syntax_semantics",
    "lexically_identical": false,
    "linguistics_term": "control_raising",
    "one_prefix_method": false,
    "pair_id": 2,
    "sentence_bad": "Benjamin's tutor was certain to boast about.",
    "sentence_good": "Benjamin's tutor was easy to boast about.",
    "simple_LM_method": true,
    "two_prefix_method": false
}
```

#### animate_subject_trans

- **Size of downloaded dataset files:** 0.41 MB
- **Size of the generated dataset:** 0.12 MB
- **Total amount of disk used:** 0.54 MB

An example of 'train' looks as follows.
```
{
    "UID": "tough_vs_raising_1",
    "field": "syntax_semantics",
    "lexically_identical": false,
    "linguistics_term": "control_raising",
    "one_prefix_method": false,
    "pair_id": 2,
    "sentence_bad": "Benjamin's tutor was certain to boast about.",
    "sentence_good": "Benjamin's tutor was easy to boast about.",
    "simple_LM_method": true,
    "two_prefix_method": false
}
```

### Data Fields

The data fields are the same among all splits.

#### adjunct_island
- `sentence_good`: a `string` feature.
- `sentence_bad`: a `string` feature.
- `field`: a `string` feature.
- `linguistics_term`: a `string` feature.
- `UID`: a `string` feature.
- `simple_LM_method`: a `bool` feature.
- `one_prefix_method`: a `bool` feature.
- `two_prefix_method`: a `bool` feature.
- `lexically_identical`: a `bool` feature.
- `pair_id`: a `int32` feature.

#### anaphor_gender_agreement
- `sentence_good`: a `string` feature.
- `sentence_bad`: a `string` feature.
- `field`: a `string` feature.
- `linguistics_term`: a `string` feature.
- `UID`: a `string` feature.
- `simple_LM_method`: a `bool` feature.
- `one_prefix_method`: a `bool` feature.
- `two_prefix_method`: a `bool` feature.
- `lexically_identical`: a `bool` feature.
- `pair_id`: a `int32` feature.

#### anaphor_number_agreement
- `sentence_good`: a `string` feature.
- `sentence_bad`: a `string` feature.
- `field`: a `string` feature.
- `linguistics_term`: a `string` feature.
- `UID`: a `string` feature.
- `simple_LM_method`: a `bool` feature.
- `one_prefix_method`: a `bool` feature.
- `two_prefix_method`: a `bool` feature.
- `lexically_identical`: a `bool` feature.
- `pair_id`: a `int32` feature.

#### animate_subject_passive
- `sentence_good`: a `string` feature.
- `sentence_bad`: a `string` feature.
- `field`: a `string` feature.
- `linguistics_term`: a `string` feature.
- `UID`: a `string` feature.
- `simple_LM_method`: a `bool` feature.
- `one_prefix_method`: a `bool` feature.
- `two_prefix_method`: a `bool` feature.
- `lexically_identical`: a `bool` feature.
- `pair_id`: a `int32` feature.

#### animate_subject_trans
- `sentence_good`: a `string` feature.
- `sentence_bad`: a `string` feature.
- `field`: a `string` feature.
- `linguistics_term`: a `string` feature.
- `UID`: a `string` feature.
- `simple_LM_method`: a `bool` feature.
- `one_prefix_method`: a `bool` feature.
- `two_prefix_method`: a `bool` feature.
- `lexically_identical`: a `bool` feature.
- `pair_id`: a `int32` feature.

### Data Splits

|          name          |train|
|------------------------|----:|
|adjunct_island          | 1000|
|anaphor_gender_agreement| 1000|
|anaphor_number_agreement| 1000|
|animate_subject_passive | 1000|
|animate_subject_trans   | 1000|

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

@article{warstadt2019blimp,
  title={BLiMP: A Benchmark of Linguistic Minimal Pairs for English},
  author={Warstadt, Alex and Parrish, Alicia and Liu, Haokun and Mohananey, Anhad and Peng, Wei, and Wang, Sheng-Fu and Bowman, Samuel R},
  journal={arXiv preprint arXiv:1912.00582},
  year={2019}
}

```


### Contributions

Thanks to [@lhoestq](https://github.com/lhoestq), [@patrickvonplaten](https://github.com/patrickvonplaten), [@thomwolf](https://github.com/thomwolf) for adding this dataset.