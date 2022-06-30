---
annotations_creators:
- expert-generated
language_creators:
- found
language:
- ar
- en
- zh
license:
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
- token-classification
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

See also summaries from paperwithcode, [OntoNotes 5.0](https://paperswithcode.com/dataset/ontonotes-5-0) and [CoNLL-2012](https://paperswithcode.com/dataset/conll-2012-1)

For more detailed info of the dataset like annotation, tag set, etc., you can refer to the documents in the Mendeley repo mentioned above. 

### Supported Tasks and Leaderboards

- [Named Entity Recognition on Ontonotes v5 (English)](https://paperswithcode.com/sota/named-entity-recognition-ner-on-ontonotes-v5)
- [Coreference Resolution on OntoNotes](https://paperswithcode.com/sota/coreference-resolution-on-ontonotes)
- [Semantic Role Labeling on OntoNotes](https://paperswithcode.com/sota/semantic-role-labeling-on-ontonotes)
- ...

### Languages

V4 data for Arabic, Chinese, English, and V12 data for English

## Dataset Structure

### Data Instances

```
{
  {'document_id': 'nw/wsj/23/wsj_2311',
 'sentences': [{'part_id': 0,
                'words': ['CONCORDE', 'trans-Atlantic', 'flights', 'are', '$', '2, 'to', 'Paris', 'and', '$', '3, 'to', 'London', '.']},
                'pos_tags': [25, 18, 27, 43, 2, 12, 17, 25, 11, 2, 12, 17, 25, 7],
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
                'words': ['In', 'a', 'Centennial', 'Journal', 'article', 'Oct.', '5', ',', 'the', 'fares', 'were', 'reversed', '.']}]}
                'pos_tags': [17, 13, 25, 25, 24, 25, 12, 4, 13, 27, 40, 42, 7],
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

### Data Fields

- **`document_id`** (*`str`*): This is a variation on the document filename
- **`sentences`** (*`List[Dict]`*): All sentences of the same document are in a single example for the convenience of concatenating sentences.

Every element in `sentences` is a *`Dict`* composed of the following data fields:
- **`part_id`** (*`int`*) : Some files are divided into multiple parts numbered as 000, 001, 002, ... etc.
- **`words`** (*`List[str]`*) :
- **`pos_tags`** (*`List[ClassLabel]` or `List[str]`*) : This is the Penn-Treebank-style part of speech. When parse information is missing, all parts of speech except the one for which there is some sense or proposition annotation are marked with a XX tag. The verb is marked with just a VERB tag.
  - tag set : Note tag sets below are founded by scanning all the data, and I found it seems to be a little bit different from officially stated tag sets. See official documents in the [Mendeley repo](https://data.mendeley.com/datasets/zmycy7t9h9) 
    - arabic : str. Because pos tag in Arabic is compounded and complex, hard to represent it by `ClassLabel`
    - chinese v4 : `datasets.ClassLabel(num_classes=36, names=["X", "AD", "AS", "BA", "CC", "CD", "CS", "DEC", "DEG", "DER", "DEV", "DT", "ETC", "FW", "IJ", "INF", "JJ", "LB", "LC", "M", "MSP", "NN", "NR", "NT", "OD", "ON", "P", "PN", "PU", "SB", "SP", "URL", "VA", "VC", "VE", "VV",])`, where `X` is for pos tag missing
    - english v4 : `datasets.ClassLabel(num_classes=49, names=["XX", "``", "$", "''", ",", "-LRB-", "-RRB-", ".", ":", "ADD", "AFX", "CC", "CD", "DT", "EX", "FW", "HYPH", "IN", "JJ", "JJR", "JJS", "LS", "MD", "NFP", "NN", "NNP", "NNPS", "NNS", "PDT", "POS", "PRP", "PRP$", "RB", "RBR", "RBS", "RP", "SYM", "TO", "UH", "VB", "VBD", "VBG", "VBN", "VBP", "VBZ", "WDT", "WP", "WP$", "WRB",])`, where `XX` is for pos tag missing, and `-LRB-`/`-RRB-` is "`(`" / "`)`".
    - english v12 : `datasets.ClassLabel(num_classes=51, names="english_v12": ["XX", "``", "$", "''", "*", ",", "-LRB-", "-RRB-", ".", ":", "ADD", "AFX", "CC", "CD", "DT", "EX", "FW", "HYPH", "IN", "JJ", "JJR", "JJS", "LS", "MD", "NFP", "NN", "NNP", "NNPS", "NNS", "PDT", "POS", "PRP", "PRP$", "RB", "RBR", "RBS", "RP", "SYM", "TO", "UH", "VB", "VBD", "VBG", "VBN", "VBP", "VBZ", "VERB", "WDT", "WP", "WP$", "WRB",])`, where `XX` is for pos tag missing, and `-LRB-`/`-RRB-` is "`(`" / "`)`".
- **`parse_tree`** (*`Optional[str]`*) : An serialized NLTK Tree representing the parse. It includes POS tags as pre-terminal nodes. When the parse information is missing, the parse will be `None`.
- **`predicate_lemmas`** (*`List[Optional[str]]`*) : The predicate lemma of the words for which we have semantic role information or word sense information. All other indices are `None`.
- **`predicate_framenet_ids`** (*`List[Optional[int]]`*) : The PropBank frameset ID of the lemmas in predicate_lemmas, or `None`.
- **`word_senses`** (*`List[Optional[float]]`*) : The word senses for the words in the sentence, or None. These are floats because the word sense can have values after the decimal, like 1.1.
- **`speaker`** (*`Optional[str]`*) : This is the speaker or author name where available. Mostly in Broadcast Conversation and Web Log data. When it is not available, it will be `None`.
- **`named_entities`** (*`List[ClassLabel]`*) : The BIO tags for named entities in the sentence. 
  - tag set : `datasets.ClassLabel(num_classes=37, names=["O", "B-PERSON", "I-PERSON", "B-NORP", "I-NORP", "B-FAC", "I-FAC", "B-ORG", "I-ORG", "B-GPE", "I-GPE", "B-LOC", "I-LOC", "B-PRODUCT", "I-PRODUCT", "B-DATE", "I-DATE", "B-TIME", "I-TIME", "B-PERCENT", "I-PERCENT", "B-MONEY", "I-MONEY", "B-QUANTITY", "I-QUANTITY", "B-ORDINAL", "I-ORDINAL", "B-CARDINAL", "I-CARDINAL", "B-EVENT", "I-EVENT", "B-WORK_OF_ART", "I-WORK_OF_ART", "B-LAW", "I-LAW", "B-LANGUAGE", "I-LANGUAGE",])`
- **`srl_frames`** (*`List[{"word":str, "frames":List[str]}]`*) : A dictionary keyed by the verb in the sentence for the given Propbank frame labels, in a BIO format.
- **`coref spans`** (*`List[List[int]]`*) : The spans for entity mentions involved in coreference resolution within the sentence. Each element is a tuple composed of (cluster_id, start_index, end_index). Indices are inclusive.

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
