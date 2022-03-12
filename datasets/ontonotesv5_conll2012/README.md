---
annotations_creators:
- expert-generated
language_creators:
- found
languages:
- ar
- en
- zh
licenses:
- cc-by-nc-nd-4.0
multilinguality:
- multilingual
paperswithcode_id: ontonotes-5-0
pretty_name: CoNLL2012 shared task data based on OntoNotes 5.0
size_categories:
- 10K<n<100K
source_datasets:
- original
task_categories:
- structure-prediction
task_ids:
- named-entity-recognition
- part-of-speech-tagging
- semantic-role-labeling
- coreference-resolution
- parsing
- lemmatization
- word-sense-disambiguation
---

# Dataset Card for CoNLL2012 shared task data based on OntoNotes 5.0

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

- **Homepage:** [CoNLL-2012 Shared Task](https://conll.cemantix.org/2012/data.html), [Author's page](https://cemantix.org/data/ontonotes.html)
- **Repository:** [Mendeley](https://data.mendeley.com/datasets/zmycy7t9h9)
- **Paper:** [Towards Robust Linguistic Analysis using OntoNotes](https://aclanthology.org/W13-3516/)
- **Leaderboard:**
- **Point of Contact:**

### Dataset Summary

OntoNotes v5.0 is the final version of OntoNotes corpus, and is a large-scale, multi-genre,
multilingual corpus manually annotated with syntactic, semantic and discourse information.

This dataset is the version of OntoNotes v5.0 extended and is used in the CoNLL-2012 shared task.
It includes v4 train/dev and v9 test data for English/Chinese/Arabic and corrected version v12 train/dev/test data (English only).

The source of data is the Mendeley Data repo [ontonotes-conll2012](https://data.mendeley.com/datasets/zmycy7t9h9), which seems to be as the same as the official data, but users should use this dataset on their own responsibility.

See also summaries from paperwithcode [OntoNotes 5.0](https://paperswithcode.com/dataset/ontonotes-5-0) [CoNLL-2012](https://paperswithcode.com/dataset/conll-2012-1)

### Supported Tasks and Leaderboards

[Named Entity Recognition on Ontonotes v5 (English)](https://paperswithcode.com/sota/named-entity-recognition-ner-on-ontonotes-v5)
[Coreference Resolution on OntoNotes](https://paperswithcode.com/sota/coreference-resolution-on-ontonotes)
[Semantic Role Labeling on OntoNotes](https://paperswithcode.com/sota/semantic-role-labeling-on-ontonotes)
...

### Languages

V4 data for Arabic, Chinese, English, and V12 data for English

## Dataset Structure

### Data Instances

Notice that every entry in the dataset contains data of a single whole document, such that we can concatenate sentences easily. 

```
{
  {'document_id': 'nw/wsj/23/wsj_2311',
 'sentences': [{'part_id': 0,
                'words': ['CONCORDE', 'trans-Atlantic', 'flights', 'are', '$', '2, 'to', 'Paris', 'and', '$', '3, 'to', 'London', '.']},
                'pos_tags': ['NNP', 'JJ', 'NNS', 'VBP', '$', 'CD', 'IN', 'NNP', 'CC', '$', 'CD', 'IN', 'NNP', '.'],
                'parse_tree': '(TOP(S(NP (NNP CONCORDE)  (JJ trans-Atlantic)  (NNS flights) )(VP (VBP are) (NP(NP(NP ($ $)  (CD 2,400) )(PP (IN to) (NP (NNP Paris) ))) (CC and) (NP(NP ($ $)  (CD 3,200) )(PP (IN to) (NP (NNP London) ))))) (. .) ))',
                'predicate_lemmas': [None, None, None, 'be', None, None, None, None, None, None, None, None, None, None],
                'predicate_framenet_ids': [None, None, None, '01', None, None, None, None, None, None, None, None, None, None],
                'word_senses': [None, None, None, None, None, None, None, None, None, None, None, None, None, None],
                'speaker': None,
                'named_entities': [7, 6, 0, 0, 0, 15, 0, 5, 0, 0, 15, 0, 5, 0],
                'srl_frames': [{'frames': ['B-ARG1', 'I-ARG1', 'I-ARG1', 'B-V', 'B-ARG2', 'I-ARG2', 'I-ARG2', 'I-ARG2', 'I-ARG2', 'I-ARG2', 'I-ARG2', 'I-ARG2', 'I-ARG2', 'O'],
                                'verb': 'are'}],
                'coref_spans': [],
               {'part_id': 0,
                'words': ['In', 'a', 'Centennial', 'Journal', 'article', 'Oct.', '5', ', 'the', 'fares', 'were', 'reversed', '.']}]}
                'pos_tags': ['IN', 'DT', 'NNP', 'NNP', 'NN', 'NNP', 'CD', ', 'DT', 'NNS', 'VBD', 'VBN', '.'],
                'parse_tree': '(TOP(S(PP (IN In) (NP (DT a) (NML (NNP Centennial)  (NNP Journal) ) (NN article) ))(NP (NNP Oct.)  (CD 5) ) (, ,) (NP (DT the)  (NNS fares) )(VP (VBD were) (VP (VBN reversed) )) (. .) ))',
                'predicate_lemmas': [None, None, None, None, None, None, None, None, None, None, None, 'reverse', None],
                'predicate_framenet_ids': [None, None, None, None, None, None, None, None, None, None, None, '01', None],
                'word_senses': [None, None, None, None, None, None, None, None, None, None, None, None, None],
                'speaker': None,
                'named_entities': [0, 0, 4, 22, 0, 12, 30, 0, 0, 0, 0, 0, 0],
                'srl_frames': [{'frames': ['B-ARGM-LOC', 'I-ARGM-LOC', 'I-ARGM-LOC', 'I-ARGM-LOC', 'I-ARGM-LOC', 'B-ARGM-TMP', 'I-ARGM-TMP', 'O', 'B-ARG1', 'I-ARG1', 'O', 'B-V', 'O'],
                                'verb': 'reversed'}],
                'coref_spans': [],
}
```

Note that name entity tag is belong to
```
datasets.ClassLabel(num_classes=37, names=[
  "O",
  "B-PERSON", "B-NORP", "B-FAC", "B-ORG", "B-GPE", "B-LOC", "B-PRODUCT", "B-EVENT", "B-WORK_OF_ART", "B-LAW", "B-LANGUAGE", "B-DATE", "B-TIME", "B-PERCENT", "B-MONEY", "B-QUANTITY", "B-ORDINAL", "B-CARDINAL",
  "I-PERSON", "I-NORP", "I-FAC", "I-ORG", "I-GPE", "I-LOC", "I-PRODUCT", "I-EVENT", "I-WORK_OF_ART", "I-LAW", "I-LANGUAGE", "I-DATE", "I-TIME", "I-PERCENT", "I-MONEY", "I-QUANTITY", "I-ORDINAL", "I-CARDINAL",
])
```

### Data Fields

Every element (sentence) under the "sentences" data field of every entry, is stored in the format as same as [AllenNLP/OntonotesSentence](https://docs.allennlp.org/models/main/models/common/ontonotes/#ontonotessentence), except for the following
- `part_id`: `int`
- `parse_tree`: `str`
- `srl_frames`: `List[Dict("word":str, "frames":List[str])]`
- `speaker`: a single `str`
- `coref spans`: `List[List[int]]`, every coref span is represented by (cluster id, start index, end_index)

### Data Splits

Each dataset (arabic_v4, chinese_v4, english_v4, english_v12) has 3 splits: _train_, _validation_, and _test_

## Dataset Creation

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

[More Information Needed]

### Citation Information

```
@inproceedings{pradhan-etal-2013-towards,
    title = "Towards Robust Linguistic Analysis using {O}nto{N}otes",
    author = {Pradhan, Sameer  and
      Moschitti, Alessandro  and
      Xue, Nianwen  and
      Ng, Hwee Tou  and
      Bj{\"o}rkelund, Anders  and
      Uryupina, Olga  and
      Zhang, Yuchen  and
      Zhong, Zhi},
    booktitle = "Proceedings of the Seventeenth Conference on Computational Natural Language Learning",
    month = aug,
    year = "2013",
    address = "Sofia, Bulgaria",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/W13-3516",
    pages = "143--152",
}
```

### Contributions

Thanks to [@richarddwang](https://github.com/richarddwang) for adding this dataset.
