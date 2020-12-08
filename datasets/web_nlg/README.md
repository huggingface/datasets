---
annotations_creators:
- found
language_creators:
- crowdsourced
languages:
  release_v1:
  - en
  release_v2:
  - en
  release_v2.1:
  - en
  release_v2.1_constrained:
  - en
  release_v2_constrained:
  - en
  release_v3.0_en:
  - en
  release_v3.0_ru:
  - ru
  webnlg_challenge_2017:
  - en
licenses:
- cc-by-sa-3.0
- cc-by-nc-sa-4.0
- gfdl-1.1
multilinguality:
- monolingual
size_categories:
- 10K<n<100K
source_datasets:
- extended|other-db_pedia
- original
task_categories:
  release_v1:
  - conditional-text-generation
  release_v2:
  - conditional-text-generation
  release_v2.1:
  - conditional-text-generation
  release_v2.1_constrained:
  - conditional-text-generation
  release_v2_constrained:
  - conditional-text-generation
  release_v3.0_en:
  - conditional-text-generation
  - structure-prediction
  release_v3.0_ru:
  - conditional-text-generation
  - structure-prediction
  webnlg_challenge_2017:
  - conditional-text-generation
task_ids:
  release_v1:
  - other-stuctured-to-text
  release_v2:
  - other-stuctured-to-text
  release_v2.1:
  - other-stuctured-to-text
  release_v2.1_constrained:
  - other-stuctured-to-text
  release_v2_constrained:
  - other-stuctured-to-text
  release_v3.0_en:
  - conditional-text-generation
  - parsing
  release_v3.0_ru:
  - conditional-text-generation
  - parsing
  webnlg_challenge_2017:
  - other-stuctured-to-text
---

# Dataset Card for WebNLG

## Table of Contents
- [Dataset Description](#dataset-description)
  - [Dataset Summary](#dataset-summary)
  - [Supported Tasks](#supported-tasks-and-leaderboards)
  - [Languages](#languages)
- [Dataset Structure](#dataset-structure)
  - [Data Instances](#data-instances)
  - [Data Fields](#data-instances)
  - [Data Splits](#data-instances)
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

## Dataset Description

- **Homepage:** [WebNLG challenge website](https://webnlg-challenge.loria.fr/)
- **Repository:** [WebNLG GitLab repository](https://gitlab.com/shimorina/webnlg-dataset/-/tree/master/)
- **Paper:** [Creating Training Corpora for NLG Micro-Planning](https://www.aclweb.org/anthology/P17-1017.pdf)
- **Leaderboard:** [WebNLG leaderboards](https://gerbil-nlg.dice-research.org/gerbil/webnlg2020results)
- **Point of Contact:** [anastasia.shimorina@loria.fr](anastasia.shimorina@loria.fr)

### Dataset Summary

The WebNLG challenge consists in mapping data to text. The training data consists
of Data/Text pairs where the data is a set of triples extracted from DBpedia and the text is a verbalisation
of these triples. For instance, given the 3 DBpedia triples shown in (a), the aim is to generate a text such as (b).

```
a. (John_E_Blaha birthDate 1942_08_26) (John_E_Blaha birthPlace San_Antonio) (John_E_Blaha occupation Fighter_pilot)
b. John E Blaha, born in San Antonio on 1942-08-26, worked as a fighter pilot
```

As the example illustrates, the task involves specific NLG subtasks such as sentence segmentation
(how to chunk the input data into sentences), lexicalisation (of the DBpedia properties),
aggregation (how to avoid repetitions) and surface realisation
(how to build a syntactically correct and natural sounding text).

### Supported Tasks and Leaderboards

The dataset supports a `other-structured-to-text` task which requires a model takes a set of RDF (Resource Description Format) triples from a database (DBpedia) of the form (subject, property, object) as input and write out a natural language sentence expressing the information contained in the triples. The dataset has supportd two challenges: the [WebNLG2017](https://www.aclweb.org/anthology/W17-3518/) and [WebNLG2020](https://gerbil-nlg.dice-research.org/gerbil/webnlg2020results) challenge. Results were ordered by their [METEOR](https://huggingface.co/metrics/meteor) to the reference, but the leaderboards report a range of other metrics including [BLEU](https://huggingface.co/metrics/bleu), [BERTscore](https://huggingface.co/metrics/bertscore), and [BLEURT](https://huggingface.co/metrics/bleurt). The v3 release (`release_v3.0_en`, `release_v3.0_ru`) for the WebNLG2020 challenge also supports a semantic `parsing` task.

### Languages

All releases contain English (`en`) data. The v3 release (`release_v3.0_ru`) also contains Russian (`ru`) examples.

## Dataset Structure

### Data Instances

A typical example contains the original RDF triples in the set, a modified version which presented to crowd workers, and a set of possible verbalizations for this set of triples:
```
{'2017_test_category': '',
 'category': 'Politician',
 'eid': 'Id10',
 'lex': {'comment': ['good', 'good', 'good'],
         'lid': ['Id1', 'Id2', 'Id3'],
         'text': ['World War II had Chiang Kai-shek as a commander and United States Army soldier Abner W. Sibal.',
                  'Abner W. Sibal served in the United States Army during the Second World War and during that war Chiang Kai-shek was one of the commanders.',
                  'Abner W. Sibal, served in the United States Army and fought in World War II, one of the commanders of which, was Chiang Kai-shek.']},
 'modified_triple_sets': {'mtriple_set': [['Abner_W._Sibal | battle | World_War_II',
                                           'World_War_II | commander | Chiang_Kai-shek',
                                           'Abner_W._Sibal | militaryBranch | United_States_Army']]},
 'original_triple_sets': {'otriple_set': [['Abner_W._Sibal | battles | World_War_II', 'World_War_II | commander | Chiang_Kai-shek', 'Abner_W._Sibal | branch | United_States_Army'],
                                          ['Abner_W._Sibal | militaryBranch | United_States_Army',
                                           'Abner_W._Sibal | battles | World_War_II',
                                           'World_War_II | commander | Chiang_Kai-shek']]},
 'shape': '(X (X) (X (X)))',
 'shape_type': 'mixed',
 'size': 3}
```

### Data Fields

The following fields can be found in the instances:
- `category`: the category of the DBpedia entites present in the RDF triples.
- `eid`: an example ID, only unique per split per category.
- `size`: number of RDF triples in the set.
- `shape`: (for v3 only) Each set of RDF-triples is a tree, which is characterised by its shape and shape type. `shape` is a string representation of the tree with nested parentheses where X is a node (see [Newick tree format](https://en.wikipedia.org/wiki/Newick_format))
- `shape_type`: (for v3 only) is a type of the tree shape, which can be: `chain` (the object of one triple is the subject of the other); `sibling` (triples with a shared subject); `mixed` (both chain and sibling types present).
- `2017_test_category`: (for `webnlg_challenge_2017`) tells whether the set of RDF triples was present in the training set or not.
- `lex`: the lexicalizations, with:
  - `text`: the text to be predicted.
  - `lid`: a lexicalizayion ID, unique per example.
  - `comment`: the lexicalizations were rated by crowd workers are either `good` or `bad`

### Data Splits

[More Information Needed]

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

The dataset uses the `cc-by-nc-sa-4.0` license. The source DBpedia project uses the `cc-by-sa-3.0` and `gfdl-1.1` licenses.

### Citation Information

- If you use the WebNLG corpus, cite:
```
@inproceedings{web_nlg,
  author    = {Claire Gardent and
               Anastasia Shimorina and
               Shashi Narayan and
               Laura Perez{-}Beltrachini},
  editor    = {Regina Barzilay and
               Min{-}Yen Kan},
  title     = {Creating Training Corpora for {NLG} Micro-Planners},
  booktitle = {Proceedings of the 55th Annual Meeting of the Association for Computational
               Linguistics, {ACL} 2017, Vancouver, Canada, July 30 - August 4, Volume
               1: Long Papers},
  pages     = {179--188},
  publisher = {Association for Computational Linguistics},
  year      = {2017},
  url       = {https://doi.org/10.18653/v1/P17-1017},
  doi       = {10.18653/v1/P17-1017}
}
```

- If you use `release_v2_constrained` in particular, cite:
```
@InProceedings{shimorina2018handling,
  author = 	"Shimorina, Anastasia
		and Gardent, Claire",
  title = 	"Handling Rare Items in Data-to-Text Generation",
  booktitle = 	"Proceedings of the 11th International Conference on Natural Language Generation",
  year = 	"2018",
  publisher = 	"Association for Computational Linguistics",
  pages = 	"360--370",
  location = 	"Tilburg University, The Netherlands",
  url = 	"http://aclweb.org/anthology/W18-6543"
}
```
