<div itemscope itemtype="http://schema.org/Dataset">
  <div itemscope itemprop="includedInDataCatalog" itemtype="http://schema.org/DataCatalog">
    <meta itemprop="name" content="TensorFlow Datasets" />
  </div>
  <meta itemprop="name" content="blimp" />
  <meta itemprop="description" content="&#10;BLiMP is a challenge set for evaluating what language models (LMs) know about&#10;major grammatical phenomena in English. BLiMP consists of 67 sub-datasets, each&#10;containing 1000 minimal pairs isolating specific contrasts in syntax,&#10;morphology, or semantics. The data is automatically generated according to&#10;expert-crafted grammars.&#10;&#10;&#10;To use this dataset:&#10;&#10;```python&#10;import tensorflow_datasets as tfds&#10;&#10;ds = tfds.load(&#x27;blimp&#x27;, split=&#x27;train&#x27;)&#10;for ex in ds.take(4):&#10;  print(ex)&#10;```&#10;&#10;See [the guide](https://www.tensorflow.org/datasets/overview) for more&#10;informations on [tensorflow_datasets](https://www.tensorflow.org/datasets).&#10;&#10;" />
  <meta itemprop="url" content="https://www.tensorflow.org/datasets/catalog/blimp" />
  <meta itemprop="sameAs" content="https://github.com/alexwarstadt/blimp/tree/master/" />
  <meta itemprop="citation" content="&#10;@article{warstadt2019blimp,&#10;  title={BLiMP: A Benchmark of Linguistic Minimal Pairs for English},&#10;  author={Warstadt, Alex and Parrish, Alicia and Liu, Haokun and Mohananey, Anhad and Peng, Wei, and Wang, Sheng-Fu and Bowman, Samuel R},&#10;  journal={arXiv preprint arXiv:1912.00582},&#10;  year={2019}&#10;}&#10;" />
</div>
# `blimp`

*   **Description**:

BLiMP is a challenge set for evaluating what language models (LMs) know about
major grammatical phenomena in English. BLiMP consists of 67 sub-datasets, each
containing 1000 minimal pairs isolating specific contrasts in syntax,
morphology, or semantics. The data is automatically generated according to
expert-crafted grammars.

*   **Homepage**:
    [https://github.com/alexwarstadt/blimp/tree/master/](https://github.com/alexwarstadt/blimp/tree/master/)
*   **Source code**:
    [`tfds.text.blimp.Blimp`](https://github.com/tensorflow/datasets/tree/master/tensorflow_datasets/text/blimp.py)
*   **Versions**:
    *   **`0.1.0`** (default): No release notes.
*   **Auto-cached**
    ([documentation](https://www.tensorflow.org/datasets/performances#auto-caching)):
    Yes
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 1,000

*   **Features**:

```python
FeaturesDict({
    'UID': Text(shape=(), dtype=tf.string),
    'field': Text(shape=(), dtype=tf.string),
    'lexically_identical': tf.bool,
    'linguistics_term': Text(shape=(), dtype=tf.string),
    'one_prefix_method': tf.bool,
    'pair_id': tf.int32,
    'sentence_bad': Text(shape=(), dtype=tf.string),
    'sentence_good': Text(shape=(), dtype=tf.string),
    'simple_LM_method': tf.bool,
    'two_prefix_method': tf.bool,
})
```
*   **Supervised keys** (See
    [`as_supervised` doc](https://www.tensorflow.org/datasets/api_docs/python/tfds/load#args)):
    `None`
*   **Citation**:

```
@article{warstadt2019blimp,
  title={BLiMP: A Benchmark of Linguistic Minimal Pairs for English},
  author={Warstadt, Alex and Parrish, Alicia and Liu, Haokun and Mohananey, Anhad and Peng, Wei, and Wang, Sheng-Fu and Bowman, Samuel R},
  journal={arXiv preprint arXiv:1912.00582},
  year={2019}
}
```

## blimp/adjunct_island (default config)

*   **Config description**: BLiMP is a challenge set for evaluating what
    language models (LMs) know about major grammatical phenomena in English.
    BLiMP consists of 67 sub-datasets, each containing 1000 minimal pairs
    isolating specific contrasts in syntax, morphology, or semantics. The data
    is automatically generated according to expert-crafted grammars. This
    configuration includes the paradigm adjunct_island.
*   **Download size**: `350.86 KiB`
*   **Dataset size**: `366.47 KiB`

## blimp/anaphor_gender_agreement

*   **Config description**: BLiMP is a challenge set for evaluating what
    language models (LMs) know about major grammatical phenomena in English.
    BLiMP consists of 67 sub-datasets, each containing 1000 minimal pairs
    isolating specific contrasts in syntax, morphology, or semantics. The data
    is automatically generated according to expert-crafted grammars. This
    configuration includes the paradigm anaphor_gender_agreement.
*   **Download size**: `426.51 KiB`
*   **Dataset size**: `332.31 KiB`

## blimp/anaphor_number_agreement

*   **Config description**: BLiMP is a challenge set for evaluating what
    language models (LMs) know about major grammatical phenomena in English.
    BLiMP consists of 67 sub-datasets, each containing 1000 minimal pairs
    isolating specific contrasts in syntax, morphology, or semantics. The data
    is automatically generated according to expert-crafted grammars. This
    configuration includes the paradigm anaphor_number_agreement.
*   **Download size**: `440.29 KiB`
*   **Dataset size**: `341.07 KiB`

## blimp/animate_subject_passive

*   **Config description**: BLiMP is a challenge set for evaluating what
    language models (LMs) know about major grammatical phenomena in English.
    BLiMP consists of 67 sub-datasets, each containing 1000 minimal pairs
    isolating specific contrasts in syntax, morphology, or semantics. The data
    is automatically generated according to expert-crafted grammars. This
    configuration includes the paradigm animate_subject_passive.
*   **Download size**: `451.46 KiB`
*   **Dataset size**: `345.50 KiB`

## blimp/animate_subject_trans

*   **Config description**: BLiMP is a challenge set for evaluating what
    language models (LMs) know about major grammatical phenomena in English.
    BLiMP consists of 67 sub-datasets, each containing 1000 minimal pairs
    isolating specific contrasts in syntax, morphology, or semantics. The data
    is automatically generated according to expert-crafted grammars. This
    configuration includes the paradigm animate_subject_trans.
*   **Download size**: `422.95 KiB`
*   **Dataset size**: `329.27 KiB`

## blimp/causative

*   **Config description**: BLiMP is a challenge set for evaluating what
    language models (LMs) know about major grammatical phenomena in English.
    BLiMP consists of 67 sub-datasets, each containing 1000 minimal pairs
    isolating specific contrasts in syntax, morphology, or semantics. The data
    is automatically generated according to expert-crafted grammars. This
    configuration includes the paradigm causative.
*   **Download size**: `309.73 KiB`
*   **Dataset size**: `324.36 KiB`

## blimp/complex_NP_island

*   **Config description**: BLiMP is a challenge set for evaluating what
    language models (LMs) know about major grammatical phenomena in English.
    BLiMP consists of 67 sub-datasets, each containing 1000 minimal pairs
    isolating specific contrasts in syntax, morphology, or semantics. The data
    is automatically generated according to expert-crafted grammars. This
    configuration includes the paradigm complex_NP_island.
*   **Download size**: `383.17 KiB`
*   **Dataset size**: `398.78 KiB`

## blimp/coordinate_structure_constraint_complex_left_branch

*   **Config description**: BLiMP is a challenge set for evaluating what
    language models (LMs) know about major grammatical phenomena in English.
    BLiMP consists of 67 sub-datasets, each containing 1000 minimal pairs
    isolating specific contrasts in syntax, morphology, or semantics. The data
    is automatically generated according to expert-crafted grammars. This
    configuration includes the paradigm
    coordinate_structure_constraint_complex_left_branch.
*   **Download size**: `558.30 KiB`
*   **Dataset size**: `410.43 KiB`

## blimp/coordinate_structure_constraint_object_extraction

*   **Config description**: BLiMP is a challenge set for evaluating what
    language models (LMs) know about major grammatical phenomena in English.
    BLiMP consists of 67 sub-datasets, each containing 1000 minimal pairs
    isolating specific contrasts in syntax, morphology, or semantics. The data
    is automatically generated according to expert-crafted grammars. This
    configuration includes the paradigm
    coordinate_structure_constraint_object_extraction.
*   **Download size**: `357.47 KiB`
*   **Dataset size**: `372.10 KiB`

## blimp/determiner_noun_agreement_1

*   **Config description**: BLiMP is a challenge set for evaluating what
    language models (LMs) know about major grammatical phenomena in English.
    BLiMP consists of 67 sub-datasets, each containing 1000 minimal pairs
    isolating specific contrasts in syntax, morphology, or semantics. The data
    is automatically generated according to expert-crafted grammars. This
    configuration includes the paradigm determiner_noun_agreement_1.
*   **Download size**: `457.66 KiB`
*   **Dataset size**: `356.93 KiB`

## blimp/determiner_noun_agreement_2

*   **Config description**: BLiMP is a challenge set for evaluating what
    language models (LMs) know about major grammatical phenomena in English.
    BLiMP consists of 67 sub-datasets, each containing 1000 minimal pairs
    isolating specific contrasts in syntax, morphology, or semantics. The data
    is automatically generated according to expert-crafted grammars. This
    configuration includes the paradigm determiner_noun_agreement_2.
*   **Download size**: `477.40 KiB`
*   **Dataset size**: `357.01 KiB`

## blimp/determiner_noun_agreement_irregular_1

*   **Config description**: BLiMP is a challenge set for evaluating what
    language models (LMs) know about major grammatical phenomena in English.
    BLiMP consists of 67 sub-datasets, each containing 1000 minimal pairs
    isolating specific contrasts in syntax, morphology, or semantics. The data
    is automatically generated according to expert-crafted grammars. This
    configuration includes the paradigm determiner_noun_agreement_irregular_1.
*   **Download size**: `463.80 KiB`
*   **Dataset size**: `365.08 KiB`

## blimp/determiner_noun_agreement_irregular_2

*   **Config description**: BLiMP is a challenge set for evaluating what
    language models (LMs) know about major grammatical phenomena in English.
    BLiMP consists of 67 sub-datasets, each containing 1000 minimal pairs
    isolating specific contrasts in syntax, morphology, or semantics. The data
    is automatically generated according to expert-crafted grammars. This
    configuration includes the paradigm determiner_noun_agreement_irregular_2.
*   **Download size**: `479.35 KiB`
*   **Dataset size**: `361.76 KiB`

## blimp/determiner_noun_agreement_with_adj_2

*   **Config description**: BLiMP is a challenge set for evaluating what
    language models (LMs) know about major grammatical phenomena in English.
    BLiMP consists of 67 sub-datasets, each containing 1000 minimal pairs
    isolating specific contrasts in syntax, morphology, or semantics. The data
    is automatically generated according to expert-crafted grammars. This
    configuration includes the paradigm determiner_noun_agreement_with_adj_2.
*   **Download size**: `514.46 KiB`
*   **Dataset size**: `379.92 KiB`

## blimp/determiner_noun_agreement_with_adj_irregular_1

*   **Config description**: BLiMP is a challenge set for evaluating what
    language models (LMs) know about major grammatical phenomena in English.
    BLiMP consists of 67 sub-datasets, each containing 1000 minimal pairs
    isolating specific contrasts in syntax, morphology, or semantics. The data
    is automatically generated according to expert-crafted grammars. This
    configuration includes the paradigm
    determiner_noun_agreement_with_adj_irregular_1.
*   **Download size**: `487.95 KiB`
*   **Dataset size**: `384.67 KiB`

## blimp/determiner_noun_agreement_with_adj_irregular_2

*   **Config description**: BLiMP is a challenge set for evaluating what
    language models (LMs) know about major grammatical phenomena in English.
    BLiMP consists of 67 sub-datasets, each containing 1000 minimal pairs
    isolating specific contrasts in syntax, morphology, or semantics. The data
    is automatically generated according to expert-crafted grammars. This
    configuration includes the paradigm
    determiner_noun_agreement_with_adj_irregular_2.
*   **Download size**: `516.14 KiB`
*   **Dataset size**: `384.54 KiB`

## blimp/determiner_noun_agreement_with_adjective_1

*   **Config description**: BLiMP is a challenge set for evaluating what
    language models (LMs) know about major grammatical phenomena in English.
    BLiMP consists of 67 sub-datasets, each containing 1000 minimal pairs
    isolating specific contrasts in syntax, morphology, or semantics. The data
    is automatically generated according to expert-crafted grammars. This
    configuration includes the paradigm
    determiner_noun_agreement_with_adjective_1.
*   **Download size**: `492.85 KiB`
*   **Dataset size**: `385.25 KiB`

## blimp/distractor_agreement_relational_noun

*   **Config description**: BLiMP is a challenge set for evaluating what
    language models (LMs) know about major grammatical phenomena in English.
    BLiMP consists of 67 sub-datasets, each containing 1000 minimal pairs
    isolating specific contrasts in syntax, morphology, or semantics. The data
    is automatically generated according to expert-crafted grammars. This
    configuration includes the paradigm distractor_agreement_relational_noun.
*   **Download size**: `513.33 KiB`
*   **Dataset size**: `391.45 KiB`

## blimp/distractor_agreement_relative_clause

*   **Config description**: BLiMP is a challenge set for evaluating what
    language models (LMs) know about major grammatical phenomena in English.
    BLiMP consists of 67 sub-datasets, each containing 1000 minimal pairs
    isolating specific contrasts in syntax, morphology, or semantics. The data
    is automatically generated according to expert-crafted grammars. This
    configuration includes the paradigm distractor_agreement_relative_clause.
*   **Download size**: `551.53 KiB`
*   **Dataset size**: `416.14 KiB`

## blimp/drop_argument

*   **Config description**: BLiMP is a challenge set for evaluating what
    language models (LMs) know about major grammatical phenomena in English.
    BLiMP consists of 67 sub-datasets, each containing 1000 minimal pairs
    isolating specific contrasts in syntax, morphology, or semantics. The data
    is automatically generated according to expert-crafted grammars. This
    configuration includes the paradigm drop_argument.
*   **Download size**: `297.07 KiB`
*   **Dataset size**: `311.70 KiB`

## blimp/ellipsis_n_bar_1

*   **Config description**: BLiMP is a challenge set for evaluating what
    language models (LMs) know about major grammatical phenomena in English.
    BLiMP consists of 67 sub-datasets, each containing 1000 minimal pairs
    isolating specific contrasts in syntax, morphology, or semantics. The data
    is automatically generated according to expert-crafted grammars. This
    configuration includes the paradigm ellipsis_n_bar_1.
*   **Download size**: `402.32 KiB`
*   **Dataset size**: `417.06 KiB`

## blimp/ellipsis_n_bar_2

*   **Config description**: BLiMP is a challenge set for evaluating what
    language models (LMs) know about major grammatical phenomena in English.
    BLiMP consists of 67 sub-datasets, each containing 1000 minimal pairs
    isolating specific contrasts in syntax, morphology, or semantics. The data
    is automatically generated according to expert-crafted grammars. This
    configuration includes the paradigm ellipsis_n_bar_2.
*   **Download size**: `417.53 KiB`
*   **Dataset size**: `432.47 KiB`

## blimp/existential_there_object_raising

*   **Config description**: BLiMP is a challenge set for evaluating what
    language models (LMs) know about major grammatical phenomena in English.
    BLiMP consists of 67 sub-datasets, each containing 1000 minimal pairs
    isolating specific contrasts in syntax, morphology, or semantics. The data
    is automatically generated according to expert-crafted grammars. This
    configuration includes the paradigm existential_there_object_raising.
*   **Download size**: `537.77 KiB`
*   **Dataset size**: `423.00 KiB`

## blimp/existential_there_quantifiers_1

*   **Config description**: BLiMP is a challenge set for evaluating what
    language models (LMs) know about major grammatical phenomena in English.
    BLiMP consists of 67 sub-datasets, each containing 1000 minimal pairs
    isolating specific contrasts in syntax, morphology, or semantics. The data
    is automatically generated according to expert-crafted grammars. This
    configuration includes the paradigm existential_there_quantifiers_1.
*   **Download size**: `348.95 KiB`
*   **Dataset size**: `363.58 KiB`

## blimp/existential_there_quantifiers_2

*   **Config description**: BLiMP is a challenge set for evaluating what
    language models (LMs) know about major grammatical phenomena in English.
    BLiMP consists of 67 sub-datasets, each containing 1000 minimal pairs
    isolating specific contrasts in syntax, morphology, or semantics. The data
    is automatically generated according to expert-crafted grammars. This
    configuration includes the paradigm existential_there_quantifiers_2.
*   **Download size**: `350.80 KiB`
*   **Dataset size**: `365.43 KiB`

## blimp/existential_there_subject_raising

*   **Config description**: BLiMP is a challenge set for evaluating what
    language models (LMs) know about major grammatical phenomena in English.
    BLiMP consists of 67 sub-datasets, each containing 1000 minimal pairs
    isolating specific contrasts in syntax, morphology, or semantics. The data
    is automatically generated according to expert-crafted grammars. This
    configuration includes the paradigm existential_there_subject_raising.
*   **Download size**: `385.21 KiB`
*   **Dataset size**: `399.84 KiB`

## blimp/expletive_it_object_raising

*   **Config description**: BLiMP is a challenge set for evaluating what
    language models (LMs) know about major grammatical phenomena in English.
    BLiMP consists of 67 sub-datasets, each containing 1000 minimal pairs
    isolating specific contrasts in syntax, morphology, or semantics. The data
    is automatically generated according to expert-crafted grammars. This
    configuration includes the paradigm expletive_it_object_raising.
*   **Download size**: `573.88 KiB`
*   **Dataset size**: `437.58 KiB`

## blimp/inchoative

*   **Config description**: BLiMP is a challenge set for evaluating what
    language models (LMs) know about major grammatical phenomena in English.
    BLiMP consists of 67 sub-datasets, each containing 1000 minimal pairs
    isolating specific contrasts in syntax, morphology, or semantics. The data
    is automatically generated according to expert-crafted grammars. This
    configuration includes the paradigm inchoative.
*   **Download size**: `291.71 KiB`
*   **Dataset size**: `306.34 KiB`

## blimp/intransitive

*   **Config description**: BLiMP is a challenge set for evaluating what
    language models (LMs) know about major grammatical phenomena in English.
    BLiMP consists of 67 sub-datasets, each containing 1000 minimal pairs
    isolating specific contrasts in syntax, morphology, or semantics. The data
    is automatically generated according to expert-crafted grammars. This
    configuration includes the paradigm intransitive.
*   **Download size**: `298.33 KiB`
*   **Dataset size**: `312.96 KiB`

## blimp/irregular_past_participle_adjectives

*   **Config description**: BLiMP is a challenge set for evaluating what
    language models (LMs) know about major grammatical phenomena in English.
    BLiMP consists of 67 sub-datasets, each containing 1000 minimal pairs
    isolating specific contrasts in syntax, morphology, or semantics. The data
    is automatically generated according to expert-crafted grammars. This
    configuration includes the paradigm irregular_past_participle_adjectives.
*   **Download size**: `434.10 KiB`
*   **Dataset size**: `345.74 KiB`

## blimp/irregular_past_participle_verbs

*   **Config description**: BLiMP is a challenge set for evaluating what
    language models (LMs) know about major grammatical phenomena in English.
    BLiMP consists of 67 sub-datasets, each containing 1000 minimal pairs
    isolating specific contrasts in syntax, morphology, or semantics. The data
    is automatically generated according to expert-crafted grammars. This
    configuration includes the paradigm irregular_past_participle_verbs.
*   **Download size**: `410.27 KiB`
*   **Dataset size**: `327.21 KiB`

## blimp/irregular_plural_subject_verb_agreement_1

*   **Config description**: BLiMP is a challenge set for evaluating what
    language models (LMs) know about major grammatical phenomena in English.
    BLiMP consists of 67 sub-datasets, each containing 1000 minimal pairs
    isolating specific contrasts in syntax, morphology, or semantics. The data
    is automatically generated according to expert-crafted grammars. This
    configuration includes the paradigm
    irregular_plural_subject_verb_agreement_1.
*   **Download size**: `449.91 KiB`
*   **Dataset size**: `366.17 KiB`

## blimp/irregular_plural_subject_verb_agreement_2

*   **Config description**: BLiMP is a challenge set for evaluating what
    language models (LMs) know about major grammatical phenomena in English.
    BLiMP consists of 67 sub-datasets, each containing 1000 minimal pairs
    isolating specific contrasts in syntax, morphology, or semantics. The data
    is automatically generated according to expert-crafted grammars. This
    configuration includes the paradigm
    irregular_plural_subject_verb_agreement_2.
*   **Download size**: `442.75 KiB`
*   **Dataset size**: `354.70 KiB`

## blimp/left_branch_island_echo_question

*   **Config description**: BLiMP is a challenge set for evaluating what
    language models (LMs) know about major grammatical phenomena in English.
    BLiMP consists of 67 sub-datasets, each containing 1000 minimal pairs
    isolating specific contrasts in syntax, morphology, or semantics. The data
    is automatically generated according to expert-crafted grammars. This
    configuration includes the paradigm left_branch_island_echo_question.
*   **Download size**: `471.31 KiB`
*   **Dataset size**: `348.84 KiB`

## blimp/left_branch_island_simple_question

*   **Config description**: BLiMP is a challenge set for evaluating what
    language models (LMs) know about major grammatical phenomena in English.
    BLiMP consists of 67 sub-datasets, each containing 1000 minimal pairs
    isolating specific contrasts in syntax, morphology, or semantics. The data
    is automatically generated according to expert-crafted grammars. This
    configuration includes the paradigm left_branch_island_simple_question.
*   **Download size**: `335.40 KiB`
*   **Dataset size**: `351.01 KiB`

## blimp/matrix_question_npi_licensor_present

*   **Config description**: BLiMP is a challenge set for evaluating what
    language models (LMs) know about major grammatical phenomena in English.
    BLiMP consists of 67 sub-datasets, each containing 1000 minimal pairs
    isolating specific contrasts in syntax, morphology, or semantics. The data
    is automatically generated according to expert-crafted grammars. This
    configuration includes the paradigm matrix_question_npi_licensor_present.
*   **Download size**: `447.08 KiB`
*   **Dataset size**: `354.14 KiB`

## blimp/npi_present_1

*   **Config description**: BLiMP is a challenge set for evaluating what
    language models (LMs) know about major grammatical phenomena in English.
    BLiMP consists of 67 sub-datasets, each containing 1000 minimal pairs
    isolating specific contrasts in syntax, morphology, or semantics. The data
    is automatically generated according to expert-crafted grammars. This
    configuration includes the paradigm npi_present_1.
*   **Download size**: `427.75 KiB`
*   **Dataset size**: `339.68 KiB`

## blimp/npi_present_2

*   **Config description**: BLiMP is a challenge set for evaluating what
    language models (LMs) know about major grammatical phenomena in English.
    BLiMP consists of 67 sub-datasets, each containing 1000 minimal pairs
    isolating specific contrasts in syntax, morphology, or semantics. The data
    is automatically generated according to expert-crafted grammars. This
    configuration includes the paradigm npi_present_2.
*   **Download size**: `412.24 KiB`
*   **Dataset size**: `329.11 KiB`

## blimp/only_npi_licensor_present

*   **Config description**: BLiMP is a challenge set for evaluating what
    language models (LMs) know about major grammatical phenomena in English.
    BLiMP consists of 67 sub-datasets, each containing 1000 minimal pairs
    isolating specific contrasts in syntax, morphology, or semantics. The data
    is automatically generated according to expert-crafted grammars. This
    configuration includes the paradigm only_npi_licensor_present.
*   **Download size**: `448.41 KiB`
*   **Dataset size**: `349.50 KiB`

## blimp/only_npi_scope

*   **Config description**: BLiMP is a challenge set for evaluating what
    language models (LMs) know about major grammatical phenomena in English.
    BLiMP consists of 67 sub-datasets, each containing 1000 minimal pairs
    isolating specific contrasts in syntax, morphology, or semantics. The data
    is automatically generated according to expert-crafted grammars. This
    configuration includes the paradigm only_npi_scope.
*   **Download size**: `570.04 KiB`
*   **Dataset size**: `408.52 KiB`

## blimp/passive_1

*   **Config description**: BLiMP is a challenge set for evaluating what
    language models (LMs) know about major grammatical phenomena in English.
    BLiMP consists of 67 sub-datasets, each containing 1000 minimal pairs
    isolating specific contrasts in syntax, morphology, or semantics. The data
    is automatically generated according to expert-crafted grammars. This
    configuration includes the paradigm passive_1.
*   **Download size**: `332.30 KiB`
*   **Dataset size**: `346.93 KiB`

## blimp/passive_2

*   **Config description**: BLiMP is a challenge set for evaluating what
    language models (LMs) know about major grammatical phenomena in English.
    BLiMP consists of 67 sub-datasets, each containing 1000 minimal pairs
    isolating specific contrasts in syntax, morphology, or semantics. The data
    is automatically generated according to expert-crafted grammars. This
    configuration includes the paradigm passive_2.
*   **Download size**: `301.12 KiB`
*   **Dataset size**: `315.75 KiB`

## blimp/principle_A_c_command

*   **Config description**: BLiMP is a challenge set for evaluating what
    language models (LMs) know about major grammatical phenomena in English.
    BLiMP consists of 67 sub-datasets, each containing 1000 minimal pairs
    isolating specific contrasts in syntax, morphology, or semantics. The data
    is automatically generated according to expert-crafted grammars. This
    configuration includes the paradigm principle_A_c_command.
*   **Download size**: `515.32 KiB`
*   **Dataset size**: `388.54 KiB`

## blimp/principle_A_case_1

*   **Config description**: BLiMP is a challenge set for evaluating what
    language models (LMs) know about major grammatical phenomena in English.
    BLiMP consists of 67 sub-datasets, each containing 1000 minimal pairs
    isolating specific contrasts in syntax, morphology, or semantics. The data
    is automatically generated according to expert-crafted grammars. This
    configuration includes the paradigm principle_A_case_1.
*   **Download size**: `466.05 KiB`
*   **Dataset size**: `370.87 KiB`

## blimp/principle_A_case_2

*   **Config description**: BLiMP is a challenge set for evaluating what
    language models (LMs) know about major grammatical phenomena in English.
    BLiMP consists of 67 sub-datasets, each containing 1000 minimal pairs
    isolating specific contrasts in syntax, morphology, or semantics. The data
    is automatically generated according to expert-crafted grammars. This
    configuration includes the paradigm principle_A_case_2.
*   **Download size**: `481.42 KiB`
*   **Dataset size**: `370.88 KiB`

## blimp/principle_A_domain_1

*   **Config description**: BLiMP is a challenge set for evaluating what
    language models (LMs) know about major grammatical phenomena in English.
    BLiMP consists of 67 sub-datasets, each containing 1000 minimal pairs
    isolating specific contrasts in syntax, morphology, or semantics. The data
    is automatically generated according to expert-crafted grammars. This
    configuration includes the paradigm principle_A_domain_1.
*   **Download size**: `488.15 KiB`
*   **Dataset size**: `371.62 KiB`

## blimp/principle_A_domain_2

*   **Config description**: BLiMP is a challenge set for evaluating what
    language models (LMs) know about major grammatical phenomena in English.
    BLiMP consists of 67 sub-datasets, each containing 1000 minimal pairs
    isolating specific contrasts in syntax, morphology, or semantics. The data
    is automatically generated according to expert-crafted grammars. This
    configuration includes the paradigm principle_A_domain_2.
*   **Download size**: `481.63 KiB`
*   **Dataset size**: `365.92 KiB`

## blimp/principle_A_domain_3

*   **Config description**: BLiMP is a challenge set for evaluating what
    language models (LMs) know about major grammatical phenomena in English.
    BLiMP consists of 67 sub-datasets, each containing 1000 minimal pairs
    isolating specific contrasts in syntax, morphology, or semantics. The data
    is automatically generated according to expert-crafted grammars. This
    configuration includes the paradigm principle_A_domain_3.
*   **Download size**: `501.84 KiB`
*   **Dataset size**: `359.74 KiB`

## blimp/principle_A_reconstruction

*   **Config description**: BLiMP is a challenge set for evaluating what
    language models (LMs) know about major grammatical phenomena in English.
    BLiMP consists of 67 sub-datasets, each containing 1000 minimal pairs
    isolating specific contrasts in syntax, morphology, or semantics. The data
    is automatically generated according to expert-crafted grammars. This
    configuration includes the paradigm principle_A_reconstruction.
*   **Download size**: `337.40 KiB`
*   **Dataset size**: `353.00 KiB`

## blimp/regular_plural_subject_verb_agreement_1

*   **Config description**: BLiMP is a challenge set for evaluating what
    language models (LMs) know about major grammatical phenomena in English.
    BLiMP consists of 67 sub-datasets, each containing 1000 minimal pairs
    isolating specific contrasts in syntax, morphology, or semantics. The data
    is automatically generated according to expert-crafted grammars. This
    configuration includes the paradigm regular_plural_subject_verb_agreement_1.
*   **Download size**: `441.26 KiB`
*   **Dataset size**: `359.56 KiB`

## blimp/regular_plural_subject_verb_agreement_2

*   **Config description**: BLiMP is a challenge set for evaluating what
    language models (LMs) know about major grammatical phenomena in English.
    BLiMP consists of 67 sub-datasets, each containing 1000 minimal pairs
    isolating specific contrasts in syntax, morphology, or semantics. The data
    is automatically generated according to expert-crafted grammars. This
    configuration includes the paradigm regular_plural_subject_verb_agreement_2.
*   **Download size**: `445.78 KiB`
*   **Dataset size**: `354.47 KiB`

## blimp/sentential_negation_npi_licensor_present

*   **Config description**: BLiMP is a challenge set for evaluating what
    language models (LMs) know about major grammatical phenomena in English.
    BLiMP consists of 67 sub-datasets, each containing 1000 minimal pairs
    isolating specific contrasts in syntax, morphology, or semantics. The data
    is automatically generated according to expert-crafted grammars. This
    configuration includes the paradigm
    sentential_negation_npi_licensor_present.
*   **Download size**: `479.49 KiB`
*   **Dataset size**: `372.30 KiB`

## blimp/sentential_negation_npi_scope

*   **Config description**: BLiMP is a challenge set for evaluating what
    language models (LMs) know about major grammatical phenomena in English.
    BLiMP consists of 67 sub-datasets, each containing 1000 minimal pairs
    isolating specific contrasts in syntax, morphology, or semantics. The data
    is automatically generated according to expert-crafted grammars. This
    configuration includes the paradigm sentential_negation_npi_scope.
*   **Download size**: `600.52 KiB`
*   **Dataset size**: `431.18 KiB`

## blimp/sentential_subject_island

*   **Config description**: BLiMP is a challenge set for evaluating what
    language models (LMs) know about major grammatical phenomena in English.
    BLiMP consists of 67 sub-datasets, each containing 1000 minimal pairs
    isolating specific contrasts in syntax, morphology, or semantics. The data
    is automatically generated according to expert-crafted grammars. This
    configuration includes the paradigm sentential_subject_island.
*   **Download size**: `357.25 KiB`
*   **Dataset size**: `372.86 KiB`

## blimp/superlative_quantifiers_1

*   **Config description**: BLiMP is a challenge set for evaluating what
    language models (LMs) know about major grammatical phenomena in English.
    BLiMP consists of 67 sub-datasets, each containing 1000 minimal pairs
    isolating specific contrasts in syntax, morphology, or semantics. The data
    is automatically generated according to expert-crafted grammars. This
    configuration includes the paradigm superlative_quantifiers_1.
*   **Download size**: `372.25 KiB`
*   **Dataset size**: `360.02 KiB`

## blimp/superlative_quantifiers_2

*   **Config description**: BLiMP is a challenge set for evaluating what
    language models (LMs) know about major grammatical phenomena in English.
    BLiMP consists of 67 sub-datasets, each containing 1000 minimal pairs
    isolating specific contrasts in syntax, morphology, or semantics. The data
    is automatically generated according to expert-crafted grammars. This
    configuration includes the paradigm superlative_quantifiers_2.
*   **Download size**: `504.02 KiB`
*   **Dataset size**: `360.07 KiB`

## blimp/tough_vs_raising_1

*   **Config description**: BLiMP is a challenge set for evaluating what
    language models (LMs) know about major grammatical phenomena in English.
    BLiMP consists of 67 sub-datasets, each containing 1000 minimal pairs
    isolating specific contrasts in syntax, morphology, or semantics. The data
    is automatically generated according to expert-crafted grammars. This
    configuration includes the paradigm tough_vs_raising_1.
*   **Download size**: `334.99 KiB`
*   **Dataset size**: `349.62 KiB`

## blimp/tough_vs_raising_2

*   **Config description**: BLiMP is a challenge set for evaluating what
    language models (LMs) know about major grammatical phenomena in English.
    BLiMP consists of 67 sub-datasets, each containing 1000 minimal pairs
    isolating specific contrasts in syntax, morphology, or semantics. The data
    is automatically generated according to expert-crafted grammars. This
    configuration includes the paradigm tough_vs_raising_2.
*   **Download size**: `355.54 KiB`
*   **Dataset size**: `370.17 KiB`

## blimp/transitive

*   **Config description**: BLiMP is a challenge set for evaluating what
    language models (LMs) know about major grammatical phenomena in English.
    BLiMP consists of 67 sub-datasets, each containing 1000 minimal pairs
    isolating specific contrasts in syntax, morphology, or semantics. The data
    is automatically generated according to expert-crafted grammars. This
    configuration includes the paradigm transitive.
*   **Download size**: `449.50 KiB`
*   **Dataset size**: `334.45 KiB`

## blimp/wh_island

*   **Config description**: BLiMP is a challenge set for evaluating what
    language models (LMs) know about major grammatical phenomena in English.
    BLiMP consists of 67 sub-datasets, each containing 1000 minimal pairs
    isolating specific contrasts in syntax, morphology, or semantics. The data
    is automatically generated according to expert-crafted grammars. This
    configuration includes the paradigm wh_island.
*   **Download size**: `438.12 KiB`
*   **Dataset size**: `343.47 KiB`

## blimp/wh_questions_object_gap

*   **Config description**: BLiMP is a challenge set for evaluating what
    language models (LMs) know about major grammatical phenomena in English.
    BLiMP consists of 67 sub-datasets, each containing 1000 minimal pairs
    isolating specific contrasts in syntax, morphology, or semantics. The data
    is automatically generated according to expert-crafted grammars. This
    configuration includes the paradigm wh_questions_object_gap.
*   **Download size**: `378.35 KiB`
*   **Dataset size**: `392.99 KiB`

## blimp/wh_questions_subject_gap

*   **Config description**: BLiMP is a challenge set for evaluating what
    language models (LMs) know about major grammatical phenomena in English.
    BLiMP consists of 67 sub-datasets, each containing 1000 minimal pairs
    isolating specific contrasts in syntax, morphology, or semantics. The data
    is automatically generated according to expert-crafted grammars. This
    configuration includes the paradigm wh_questions_subject_gap.
*   **Download size**: `380.84 KiB`
*   **Dataset size**: `395.47 KiB`

## blimp/wh_questions_subject_gap_long_distance

*   **Config description**: BLiMP is a challenge set for evaluating what
    language models (LMs) know about major grammatical phenomena in English.
    BLiMP consists of 67 sub-datasets, each containing 1000 minimal pairs
    isolating specific contrasts in syntax, morphology, or semantics. The data
    is automatically generated according to expert-crafted grammars. This
    configuration includes the paradigm wh_questions_subject_gap_long_distance.
*   **Download size**: `451.82 KiB`
*   **Dataset size**: `466.53 KiB`

## blimp/wh_vs_that_no_gap

*   **Config description**: BLiMP is a challenge set for evaluating what
    language models (LMs) know about major grammatical phenomena in English.
    BLiMP consists of 67 sub-datasets, each containing 1000 minimal pairs
    isolating specific contrasts in syntax, morphology, or semantics. The data
    is automatically generated according to expert-crafted grammars. This
    configuration includes the paradigm wh_vs_that_no_gap.
*   **Download size**: `374.28 KiB`
*   **Dataset size**: `388.91 KiB`

## blimp/wh_vs_that_no_gap_long_distance

*   **Config description**: BLiMP is a challenge set for evaluating what
    language models (LMs) know about major grammatical phenomena in English.
    BLiMP consists of 67 sub-datasets, each containing 1000 minimal pairs
    isolating specific contrasts in syntax, morphology, or semantics. The data
    is automatically generated according to expert-crafted grammars. This
    configuration includes the paradigm wh_vs_that_no_gap_long_distance.
*   **Download size**: `431.08 KiB`
*   **Dataset size**: `445.74 KiB`

## blimp/wh_vs_that_with_gap

*   **Config description**: BLiMP is a challenge set for evaluating what
    language models (LMs) know about major grammatical phenomena in English.
    BLiMP consists of 67 sub-datasets, each containing 1000 minimal pairs
    isolating specific contrasts in syntax, morphology, or semantics. The data
    is automatically generated according to expert-crafted grammars. This
    configuration includes the paradigm wh_vs_that_with_gap.
*   **Download size**: `359.16 KiB`
*   **Dataset size**: `373.79 KiB`

## blimp/wh_vs_that_with_gap_long_distance

*   **Config description**: BLiMP is a challenge set for evaluating what
    language models (LMs) know about major grammatical phenomena in English.
    BLiMP consists of 67 sub-datasets, each containing 1000 minimal pairs
    isolating specific contrasts in syntax, morphology, or semantics. The data
    is automatically generated according to expert-crafted grammars. This
    configuration includes the paradigm wh_vs_that_with_gap_long_distance.
*   **Download size**: `416.00 KiB`
*   **Dataset size**: `430.63 KiB`
