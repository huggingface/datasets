---
annotations_creators:
- expert-generated
language_creators:
- expert-generated
language:
- en
license:
- mit
multilinguality:
- monolingual
size_categories:
- 1K<n<10K
source_datasets:
- original
task_categories:
- token-classification
task_ids:
- coreference-resolution
paperswithcode_id: winobias
pretty_name: WinoBias
dataset_info:
- config_name: wino_bias
  features:
  - name: document_id
    dtype: string
  - name: part_number
    dtype: string
  - name: word_number
    sequence: int32
  - name: tokens
    sequence: string
  - name: pos_tags
    sequence:
      class_label:
        names:
          0: '"'
          1: ''''''
          2: '#'
          3: $
          4: (
          5: )
          6: ','
          7: .
          8: ':'
          9: '``'
          10: CC
          11: CD
          12: DT
          13: EX
          14: FW
          15: IN
          16: JJ
          17: JJR
          18: JJS
          19: LS
          20: MD
          21: NN
          22: NNP
          23: NNPS
          24: NNS
          25: NN|SYM
          26: PDT
          27: POS
          28: PRP
          29: PRP$
          30: RB
          31: RBR
          32: RBS
          33: RP
          34: SYM
          35: TO
          36: UH
          37: VB
          38: VBD
          39: VBG
          40: VBN
          41: VBP
          42: VBZ
          43: WDT
          44: WP
          45: WP$
          46: WRB
          47: HYPH
          48: XX
          49: NFP
          50: AFX
          51: ADD
          52: -LRB-
          53: -RRB-
  - name: parse_bit
    sequence: string
  - name: predicate_lemma
    sequence: string
  - name: predicate_framenet_id
    sequence: string
  - name: word_sense
    sequence: string
  - name: speaker
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: B-PERSON
          1: I-PERSON
          2: B-NORP
          3: I-NORP
          4: B-FAC
          5: I-FAC
          6: B-ORG
          7: I-ORG
          8: B-GPE
          9: I-GPE
          10: B-LOC
          11: I-LOC
          12: B-PRODUCT
          13: I-PRODUCT
          14: B-EVENT
          15: I-EVENT
          16: B-WORK_OF_ART
          17: I-WORK_OF_ART
          18: B-LAW
          19: I-LAW
          20: B-LANGUAGE
          21: I-LANGUAGE
          22: B-DATE
          23: I-DATE
          24: B-TIME
          25: I-TIME
          26: B-PERCENT
          27: I-PERCENT
          28: B-MONEY
          29: I-MONEY
          30: B-QUANTITY
          31: I-QUANTITY
          32: B-ORDINAL
          33: I-ORDINAL
          34: B-CARDINAL
          35: I-CARDINAL
          36: '*'
          37: '0'
  - name: verbal_predicates
    sequence: string
  splits:
  - name: train
    num_bytes: 173899234
    num_examples: 150335
  download_size: 268725744
  dataset_size: 173899234
- config_name: type1_pro
  features:
  - name: document_id
    dtype: string
  - name: part_number
    dtype: string
  - name: word_number
    sequence: int32
  - name: tokens
    sequence: string
  - name: pos_tags
    sequence:
      class_label:
        names:
          0: '"'
          1: ''''''
          2: '#'
          3: $
          4: (
          5: )
          6: ','
          7: .
          8: ':'
          9: '``'
          10: CC
          11: CD
          12: DT
          13: EX
          14: FW
          15: IN
          16: JJ
          17: JJR
          18: JJS
          19: LS
          20: MD
          21: NN
          22: NNP
          23: NNPS
          24: NNS
          25: NN|SYM
          26: PDT
          27: POS
          28: PRP
          29: PRP$
          30: RB
          31: RBR
          32: RBS
          33: RP
          34: SYM
          35: TO
          36: UH
          37: VB
          38: VBD
          39: VBG
          40: VBN
          41: VBP
          42: VBZ
          43: WDT
          44: WP
          45: WP$
          46: WRB
          47: HYPH
          48: XX
          49: NFP
          50: AFX
          51: ADD
          52: -LRB-
          53: -RRB-
          54: '-'
  - name: parse_bit
    sequence: string
  - name: predicate_lemma
    sequence: string
  - name: predicate_framenet_id
    sequence: string
  - name: word_sense
    sequence: string
  - name: speaker
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: B-PERSON
          1: I-PERSON
          2: B-NORP
          3: I-NORP
          4: B-FAC
          5: I-FAC
          6: B-ORG
          7: I-ORG
          8: B-GPE
          9: I-GPE
          10: B-LOC
          11: I-LOC
          12: B-PRODUCT
          13: I-PRODUCT
          14: B-EVENT
          15: I-EVENT
          16: B-WORK_OF_ART
          17: I-WORK_OF_ART
          18: B-LAW
          19: I-LAW
          20: B-LANGUAGE
          21: I-LANGUAGE
          22: B-DATE
          23: I-DATE
          24: B-TIME
          25: I-TIME
          26: B-PERCENT
          27: I-PERCENT
          28: B-MONEY
          29: I-MONEY
          30: B-QUANTITY
          31: I-QUANTITY
          32: B-ORDINAL
          33: I-ORDINAL
          34: B-CARDINAL
          35: I-CARDINAL
          36: '*'
          37: '0'
          38: '-'
  - name: verbal_predicates
    sequence: string
  - name: coreference_clusters
    sequence: string
  splits:
  - name: test
    num_bytes: 402041
    num_examples: 396
  - name: validation
    num_bytes: 379380
    num_examples: 396
  download_size: 846198
  dataset_size: 781421
- config_name: type1_anti
  features:
  - name: document_id
    dtype: string
  - name: part_number
    dtype: string
  - name: word_number
    sequence: int32
  - name: tokens
    sequence: string
  - name: pos_tags
    sequence:
      class_label:
        names:
          0: '"'
          1: ''''''
          2: '#'
          3: $
          4: (
          5: )
          6: ','
          7: .
          8: ':'
          9: '``'
          10: CC
          11: CD
          12: DT
          13: EX
          14: FW
          15: IN
          16: JJ
          17: JJR
          18: JJS
          19: LS
          20: MD
          21: NN
          22: NNP
          23: NNPS
          24: NNS
          25: NN|SYM
          26: PDT
          27: POS
          28: PRP
          29: PRP$
          30: RB
          31: RBR
          32: RBS
          33: RP
          34: SYM
          35: TO
          36: UH
          37: VB
          38: VBD
          39: VBG
          40: VBN
          41: VBP
          42: VBZ
          43: WDT
          44: WP
          45: WP$
          46: WRB
          47: HYPH
          48: XX
          49: NFP
          50: AFX
          51: ADD
          52: -LRB-
          53: -RRB-
          54: '-'
  - name: parse_bit
    sequence: string
  - name: predicate_lemma
    sequence: string
  - name: predicate_framenet_id
    sequence: string
  - name: word_sense
    sequence: string
  - name: speaker
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: B-PERSON
          1: I-PERSON
          2: B-NORP
          3: I-NORP
          4: B-FAC
          5: I-FAC
          6: B-ORG
          7: I-ORG
          8: B-GPE
          9: I-GPE
          10: B-LOC
          11: I-LOC
          12: B-PRODUCT
          13: I-PRODUCT
          14: B-EVENT
          15: I-EVENT
          16: B-WORK_OF_ART
          17: I-WORK_OF_ART
          18: B-LAW
          19: I-LAW
          20: B-LANGUAGE
          21: I-LANGUAGE
          22: B-DATE
          23: I-DATE
          24: B-TIME
          25: I-TIME
          26: B-PERCENT
          27: I-PERCENT
          28: B-MONEY
          29: I-MONEY
          30: B-QUANTITY
          31: I-QUANTITY
          32: B-ORDINAL
          33: I-ORDINAL
          34: B-CARDINAL
          35: I-CARDINAL
          36: '*'
          37: '0'
          38: '-'
  - name: verbal_predicates
    sequence: string
  - name: coreference_clusters
    sequence: string
  splits:
  - name: test
    num_bytes: 403229
    num_examples: 396
  - name: validation
    num_bytes: 380846
    num_examples: 396
  download_size: 894311
  dataset_size: 784075
- config_name: type2_pro
  features:
  - name: document_id
    dtype: string
  - name: part_number
    dtype: string
  - name: word_number
    sequence: int32
  - name: tokens
    sequence: string
  - name: pos_tags
    sequence:
      class_label:
        names:
          0: '"'
          1: ''''''
          2: '#'
          3: $
          4: (
          5: )
          6: ','
          7: .
          8: ':'
          9: '``'
          10: CC
          11: CD
          12: DT
          13: EX
          14: FW
          15: IN
          16: JJ
          17: JJR
          18: JJS
          19: LS
          20: MD
          21: NN
          22: NNP
          23: NNPS
          24: NNS
          25: NN|SYM
          26: PDT
          27: POS
          28: PRP
          29: PRP$
          30: RB
          31: RBR
          32: RBS
          33: RP
          34: SYM
          35: TO
          36: UH
          37: VB
          38: VBD
          39: VBG
          40: VBN
          41: VBP
          42: VBZ
          43: WDT
          44: WP
          45: WP$
          46: WRB
          47: HYPH
          48: XX
          49: NFP
          50: AFX
          51: ADD
          52: -LRB-
          53: -RRB-
          54: '-'
  - name: parse_bit
    sequence: string
  - name: predicate_lemma
    sequence: string
  - name: predicate_framenet_id
    sequence: string
  - name: word_sense
    sequence: string
  - name: speaker
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: B-PERSON
          1: I-PERSON
          2: B-NORP
          3: I-NORP
          4: B-FAC
          5: I-FAC
          6: B-ORG
          7: I-ORG
          8: B-GPE
          9: I-GPE
          10: B-LOC
          11: I-LOC
          12: B-PRODUCT
          13: I-PRODUCT
          14: B-EVENT
          15: I-EVENT
          16: B-WORK_OF_ART
          17: I-WORK_OF_ART
          18: B-LAW
          19: I-LAW
          20: B-LANGUAGE
          21: I-LANGUAGE
          22: B-DATE
          23: I-DATE
          24: B-TIME
          25: I-TIME
          26: B-PERCENT
          27: I-PERCENT
          28: B-MONEY
          29: I-MONEY
          30: B-QUANTITY
          31: I-QUANTITY
          32: B-ORDINAL
          33: I-ORDINAL
          34: B-CARDINAL
          35: I-CARDINAL
          36: '*'
          37: '0'
          38: '-'
  - name: verbal_predicates
    sequence: string
  - name: coreference_clusters
    sequence: string
  splits:
  - name: test
    num_bytes: 375480
    num_examples: 396
  - name: validation
    num_bytes: 367293
    num_examples: 396
  download_size: 802425
  dataset_size: 742773
- config_name: type2_anti
  features:
  - name: document_id
    dtype: string
  - name: part_number
    dtype: string
  - name: word_number
    sequence: int32
  - name: tokens
    sequence: string
  - name: pos_tags
    sequence:
      class_label:
        names:
          0: '"'
          1: ''''''
          2: '#'
          3: $
          4: (
          5: )
          6: ','
          7: .
          8: ':'
          9: '``'
          10: CC
          11: CD
          12: DT
          13: EX
          14: FW
          15: IN
          16: JJ
          17: JJR
          18: JJS
          19: LS
          20: MD
          21: NN
          22: NNP
          23: NNPS
          24: NNS
          25: NN|SYM
          26: PDT
          27: POS
          28: PRP
          29: PRP$
          30: RB
          31: RBR
          32: RBS
          33: RP
          34: SYM
          35: TO
          36: UH
          37: VB
          38: VBD
          39: VBG
          40: VBN
          41: VBP
          42: VBZ
          43: WDT
          44: WP
          45: WP$
          46: WRB
          47: HYPH
          48: XX
          49: NFP
          50: AFX
          51: ADD
          52: -LRB-
          53: -RRB-
          54: '-'
  - name: parse_bit
    sequence: string
  - name: predicate_lemma
    sequence: string
  - name: predicate_framenet_id
    sequence: string
  - name: word_sense
    sequence: string
  - name: speaker
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: B-PERSON
          1: I-PERSON
          2: B-NORP
          3: I-NORP
          4: B-FAC
          5: I-FAC
          6: B-ORG
          7: I-ORG
          8: B-GPE
          9: I-GPE
          10: B-LOC
          11: I-LOC
          12: B-PRODUCT
          13: I-PRODUCT
          14: B-EVENT
          15: I-EVENT
          16: B-WORK_OF_ART
          17: I-WORK_OF_ART
          18: B-LAW
          19: I-LAW
          20: B-LANGUAGE
          21: I-LANGUAGE
          22: B-DATE
          23: I-DATE
          24: B-TIME
          25: I-TIME
          26: B-PERCENT
          27: I-PERCENT
          28: B-MONEY
          29: I-MONEY
          30: B-QUANTITY
          31: I-QUANTITY
          32: B-ORDINAL
          33: I-ORDINAL
          34: B-CARDINAL
          35: I-CARDINAL
          36: '*'
          37: '0'
          38: '-'
  - name: verbal_predicates
    sequence: string
  - name: coreference_clusters
    sequence: string
  splits:
  - name: test
    num_bytes: 377262
    num_examples: 396
  - name: validation
    num_bytes: 368757
    num_examples: 396
  download_size: 848804
  dataset_size: 746019
---

# Dataset Card for Wino_Bias dataset

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

- **Homepage:** [WinoBias](https://uclanlp.github.io/corefBias/overview)
- **Repository:**
- **Paper:** [Arxiv](https://arxiv.org/abs/1804.06876)
- **Leaderboard:**
- **Point of Contact:**

### Dataset Summary

WinoBias, a Winograd-schema dataset for coreference resolution focused on gender bias.
The corpus contains Winograd-schema style sentences with entities corresponding to people referred by their occupation (e.g. the nurse, the doctor, the carpenter).

### Supported Tasks and Leaderboards

The underlying task is coreference resolution. 
### Languages

English

## Dataset Structure

### Data Instances

The dataset has 4 subsets: `type1_pro`, `type1_anti`, `type2_pro` and `type2_anti`.

The `*_pro` subsets contain sentences that reinforce gender stereotypes (e.g. mechanics are male, nurses are female), whereas the `*_anti` datasets contain "anti-stereotypical" sentences  (e.g. mechanics are female, nurses are male).

The `type1` (*WB-Knowledge*) subsets contain sentences for which world knowledge is necessary to resolve the co-references, and `type2` (*WB-Syntax*) subsets require only the syntactic information present in the sentence to resolve them.

### Data Fields

    - document_id = This is a variation on the document filename
    - part_number = Some files are divided into multiple parts numbered as 000, 001, 002, ... etc.
    - word_num = This is the word index of the word in that sentence.
    - tokens = This is the token as segmented/tokenized in the Treebank.
    - pos_tags = This is the Penn Treebank style part of speech. When parse information is missing, all part of speeches except the one for which there is some sense or proposition annotation   are marked with a XX tag. The verb is marked with just a VERB tag.
    - parse_bit = This is the bracketed structure broken before the first open parenthesis in the parse, and the word/part-of-speech leaf replaced with a *. The full parse can be created by substituting the asterix with the "([pos] [word])" string (or leaf) and concatenating the items in the rows of that column. When the parse information is missing, the first word of a sentence is tagged as "(TOP*" and the last word is tagged as "*)" and all intermediate words are tagged with a "*".
    - predicate_lemma = The predicate lemma is mentioned for the rows for which we have semantic role information or word sense information. All other rows are marked with a "-".
    - predicate_framenet_id = This is the PropBank frameset ID of the predicate in predicate_lemma.
    - word_sense = This is the word sense of the word in Column tokens.
    - speaker = This is the speaker or author name where available.
    - ner_tags = These columns identifies the spans representing various named entities. For documents which do not have named entity annotation, each line is represented with an "*".
    - verbal_predicates = There is one column each of predicate argument structure information for the predicate mentioned in predicate_lemma. If there are no predicates tagged in a sentence this is a single column with all rows marked with an "*".

### Data Splits

Dev and Test Split available

## Dataset Creation

### Curation Rationale

The WinoBias dataset was introduced in 2018 (see [paper](https://arxiv.org/abs/1804.06876)), with its original task being *coreference resolution*, which is a task that aims to identify mentions that refer to the same entity or person.

### Source Data

#### Initial Data Collection and Normalization

[More Information Needed]

#### Who are the source language producers?

 The dataset was created by researchers familiar with the WinoBias project, based on two prototypical templates provided by the authors, in which entities interact in plausible ways.

### Annotations

#### Annotation process

[More Information Needed]

#### Who are the annotators?

"Researchers familiar with the [WinoBias] project"

### Personal and Sensitive Information

[More Information Needed]

## Considerations for Using the Data

### Social Impact of Dataset

[More Information Needed]

### Discussion of Biases

[Recent work](https://www.microsoft.com/en-us/research/uploads/prod/2021/06/The_Salmon_paper.pdf) has shown that this dataset contains grammatical issues, incorrect or ambiguous labels, and stereotype conflation, among other limitations. 

### Other Known Limitations

[More Information Needed]

## Additional Information

### Dataset Curators

Jieyu Zhao, Tianlu Wang, Mark Yatskar, Vicente Ordonez and Kai-Wei Chan

### Licensing Information

MIT Licence

### Citation Information

@article{DBLP:journals/corr/abs-1804-06876,
  author    = {Jieyu Zhao and
               Tianlu Wang and
               Mark Yatskar and
               Vicente Ordonez and
               Kai{-}Wei Chang},
  title     = {Gender Bias in Coreference Resolution: Evaluation and Debiasing Methods},
  journal   = {CoRR},
  volume    = {abs/1804.06876},
  year      = {2018},
  url       = {http://arxiv.org/abs/1804.06876},
  archivePrefix = {arXiv},
  eprint    = {1804.06876},
  timestamp = {Mon, 13 Aug 2018 16:47:01 +0200},
  biburl    = {https://dblp.org/rec/journals/corr/abs-1804-06876.bib},
  bibsource = {dblp computer science bibliography, https://dblp.org}
}

### Contributions

Thanks to [@akshayb7](https://github.com/akshayb7) for adding this dataset. Updated by [@JieyuZhao](https://github.com/JieyuZhao).