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
  release_v3.0_ru:
  - conditional-text-generation
  webnlg_challenge_2017:
  - conditional-text-generation
task_ids:
  release_v1:
  - other-structured-to-text
  release_v2:
  - other-structured-to-text
  release_v2.1:
  - other-structured-to-text
  release_v2.1_constrained:
  - other-structured-to-text
  release_v2_constrained:
  - other-structured-to-text
  release_v3.0_en:
  - other-structured-to-text
  release_v3.0_ru:
  - other-structured-to-text
  webnlg_challenge_2017:
  - other-structured-to-text
paperswithcode_id: webnlg
pretty_name: WebNLG
---

# Dataset Card for WebNLG

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

The dataset supports a Structured to Text task which requires a model takes a set of RDF (Resource Description Format) triples from a database (DBpedia) of the form (subject, property, object) as input and write out a natural language sentence expressing the information contained in the triples. The dataset has supportd two challenges: the [WebNLG2017](https://www.aclweb.org/anthology/W17-3518/) and [WebNLG2020](https://gerbil-nlg.dice-research.org/gerbil/webnlg2020results) challenge. Results were ordered by their [METEOR](https://huggingface.co/metrics/meteor) to the reference, but the leaderboards report a range of other metrics including [BLEU](https://huggingface.co/metrics/bleu), [BERTscore](https://huggingface.co/metrics/bertscore), and [BLEURT](https://huggingface.co/metrics/bleurt). The v3 release (`release_v3.0_en`, `release_v3.0_ru`) for the WebNLG2020 challenge also supports a semantic `parsing` task.

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
- `category`: the category of the DBpedia entities present in the RDF triples.
- `eid`: an example ID, only unique per split per category.
- `size`: number of RDF triples in the set.
- `shape`: (since v2) Each set of RDF-triples is a tree, which is characterised by its shape and shape type. `shape` is a string representation of the tree with nested parentheses where X is a node (see [Newick tree format](https://en.wikipedia.org/wiki/Newick_format))
- `shape_type`: (since v2) is a type of the tree shape, which can be: `chain` (the object of one triple is the subject of the other); `sibling` (triples with a shared subject); `mixed` (both chain and sibling types present).
- `test_category`: (for `webnlg_challenge_2017` and `v3`) tells whether the set of RDF triples was present in the training set or not. Several splits of the test set are available: with and without references, and for RDF-to-text generation / for semantic parsing.
- `lex`: the lexicalizations, with:
  - `text`: the text to be predicted.
  - `lid`: a lexicalization ID, unique per example.
  - `comment`: the lexicalizations were rated by crowd workers are either `good` or `bad`
  - `lang`: (for `release_v3.0_ru`) the language used because original English texts were kept in the Russian version.

Russian data has additional optional fields comparing to English:
- `dbpedialinks`: RDF triples extracted from DBpedia between English and Russian entities by means of the property `sameAs`.
- `links`: RDF triples created manually for some entities to serve as pointers to translators. There are two types of them:
    * with `sameAs` (`Spaniards | sameAs | испанцы`)
    * with `includes` (`Tomatoes, guanciale, cheese, olive oil | includes | гуанчиале`). Those were mostly created for string literals to translate some parts of them.

### Data Splits

For `v3.0` releases:

|  English (v3.0) | Train  | Dev   | Test (data-to-text) |
|-----------------|--------|-------|-------|
| **triple sets** | 13,211 | 1,667 | 1,779 |
| **texts**       | 35,426 | 4,464 | 5,150 |
|**properties**   | 372    | 290   | 220   |


|  Russian (v3.0) | Train  | Dev   | Test (data-to-text) |
|-----------------|--------|-------|---------------------|
| **triple sets** | 5,573  | 790   | 1,102 |
| **texts**       | 14,239 | 2,026 | 2,780 |
|**properties**   | 226    | 115   | 192   |

## Dataset Creation

### Curation Rationale

The WebNLG dataset was created to promote the development _(i)_ of RDF verbalisers and _(ii)_ of microplanners able to handle a wide range of linguistic constructions. The dataset aims at covering knowledge in different domains ("categories"). The same properties and entities can appear in several categories.

### Source Data

The data was compiled from raw DBpedia triples. [This paper](https://www.aclweb.org/anthology/C16-1141/) explains how the triples were selected.

#### Initial Data Collection and Normalization

Initial triples extracted from DBpedia were modified in several ways. See [official documentation](https://webnlg-challenge.loria.fr/docs/) for the most frequent changes that have been made. An original tripleset and a modified tripleset usually represent a one-to-one mapping. However, there are cases with many-to-one mappings when several original triplesets are mapped to one modified tripleset.

Entities that served as roots of RDF trees are listed in [this file](https://gitlab.com/shimorina/webnlg-dataset/-/blob/master/supplementary/entities_dict.json).

The English WebNLG 2020 dataset (v3.0) for training comprises data-text pairs for 16 distinct DBpedia categories:
- The 10 seen categories used in the 2017 version: Airport, Astronaut, Building, City, ComicsCharacter, Food, Monument, SportsTeam, University, and WrittenWork.
- The 5 unseen categories of 2017, which are now part of the seen data: Athlete, Artist, CelestialBody, MeanOfTransportation, Politician.
- 1 new category: Company.

The Russian dataset (v3.0) comprises data-text pairs for 9 distinct categories: Airport, Astronaut, Building, CelestialBody, ComicsCharacter, Food, Monument, SportsTeam, and University.

#### Who are the source language producers?

There are no source texts, all textual material was compiled during the annotation process.

### Annotations

#### Annotation process

Annotators were first asked to create sentences that verbalise single triples. In a second round, annotators were asked to combine single-triple sentences together into sentences that cover 2 triples. And so on until 7 triples. Quality checks were performed to ensure the quality of the annotations. See Section 3.3 in [the dataset paper](https://www.aclweb.org/anthology/P17-1017.pdf).

Russian data was translated from English with an MT system and then was post-edited by crowdworkers. See Section 2.2 of [this paper](https://webnlg-challenge.loria.fr/files/2020.webnlg-papers.7.pdf).

#### Who are the annotators?

All references were collected through crowdsourcing platforms (CrowdFlower/Figure 8 and Amazon Mechanical Turk). For Russian, post-editing was done using the Yandex.Toloka crowdsourcing platform.

### Personal and Sensitive Information

Neither the dataset as published or the annotation process involves the collection or sharing of any kind of personal / demographic information.

## Considerations for Using the Data

### Social Impact of Dataset

We do not foresee any negative social impact in particular from this dataset or task.

Positive outlooks: Being able to generate good quality text from RDF data would permit, e.g., making this data more accessible to lay users, enriching existing text with information drawn from knowledge bases such as DBpedia or describing, comparing and relating entities present in these knowledge bases.

### Discussion of Biases

This dataset is created using DBpedia RDF triples which naturally exhibit biases that have been found to exist in Wikipedia such as some forms of, e.g., gender bias.

The choice of [entities](https://gitlab.com/shimorina/webnlg-dataset/-/blob/master/supplementary/entities_dict.json), described by RDF trees, was not controlled. As such, they may contain gender biases; for instance, all the astronauts described by RDF triples are male. Hence, in texts, pronouns _he/him/his_ occur more often. Similarly, entities can be related to the Western culture more often than to other cultures.

### Other Known Limitations

The quality of the crowdsourced references is limited, in particular in terms of fluency/naturalness of the collected texts.

Russian data was machine-translated and then post-edited by crowdworkers, so some examples may still exhibit issues related to bad translations.

## Additional Information

### Dataset Curators

The principle curator of the dataset is Anastasia Shimorina (Université de Lorraine / LORIA, France). Throughout the WebNLG releases, several people contributed to their construction: Claire Gardent (CNRS / LORIA, France), Shashi Narayan (Google, UK), Laura Perez-Beltrachini (University of Edinburgh, UK), Elena Khasanova, and Thiago Castro Ferreira (Federal University of Minas Gerais, Brazil).
The dataset construction was funded by the French National Research Agency (ANR).

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

### Contributions

Thanks to [@Shimorina](https://github.com/Shimorina), [@yjernite](https://github.com/yjernite) for adding this dataset.