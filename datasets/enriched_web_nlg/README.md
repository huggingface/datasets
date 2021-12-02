---
annotations_creators:
- found
language_creators:
- crowdsourced
languages:
  de:
  - de
  en:
  - en
licenses:
- cc-by-sa-4.0
multilinguality:
- monolingual
size_categories:
- 1K<n<10K
source_datasets:
- extended|other-web-nlg
task_categories:
- conditional-text-generation
task_ids:
- other-structured-to-text
paperswithcode_id: null
pretty_name: Enriched WebNLG
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
- **Repository:** [Enriched WebNLG Github repository](https://github.com/ThiagoCF05/webnlg)
- **Paper:** [Enriching the WebNLG corpus](https://www.aclweb.org/anthology/W18-6521/)

### Dataset Summary

The WebNLG challenge consists in mapping data to text. The training data consists of Data/Text pairs where the data is a
set of triples extracted from DBpedia and the text is a verbalisation of these triples. For instance, given the 3
DBpedia triples shown in (a), the aim is to generate a text such as (b). It is a valuable resource and benchmark for the Natural Language Generation (NLG) community. However, as other NLG benchmarks, it only consists of a collection of parallel raw representations and their corresponding textual realizations. This work aimed to provide intermediate representations of the data for the development and evaluation of popular tasks in the NLG pipeline architecture, such as Discourse Ordering, Lexicalization, Aggregation and Referring Expression Generation.

### Supported Tasks and Leaderboards

The dataset supports a `other-structured-to-text` task which requires a model takes a set of RDF (Resource Description
Format) triples from a database (DBpedia) of the form (subject, property, object) as input and write out a natural
language sentence expressing the information contained in the triples.

### Languages

The dataset is presented in two versions: English (config `en`) and German (config `de`)

## Dataset Structure

### Data Instances

A typical example contains the original RDF triples in the set, a modified version which presented to crowd workers, and
a set of possible verbalizations for this set of triples:

```
{ 'category': 'Politician',
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
- `shape`: (for v3 only) Each set of RDF-triples is a tree, which is characterised by its shape and shape type. `shape`
  is a string representation of the tree with nested parentheses where X is a node (
  see [Newick tree format](https://en.wikipedia.org/wiki/Newick_format))
- `shape_type`: (for v3 only) is a type of the tree shape, which can be: `chain` (the object of one triple is the
  subject of the other); `sibling` (triples with a shared subject); `mixed` (both chain and sibling types present).
- `2017_test_category`: (for `webnlg_challenge_2017`) tells whether the set of RDF triples was present in the training
  set or not.
- `lex`: the lexicalizations, with:
    - `text`: the text to be predicted.
    - `lid`: a lexicalizayion ID, unique per example.
    - `comment`: the lexicalizations were rated by crowd workers are either `good` or `bad`

### Data Splits

The `en` version has `train`, `test` and `dev` splits; the `de` version, only `train` and `dev`.

## Dataset Creation

### Curation Rationale

Natural  Language  Generation  (NLG)  is  the  process  of  automatically  converting  non-linguistic data  into  a  linguistic  output  format  (Reiter  andDale,   2000;   Gatt   and   Krahmer,   2018). Recently,   the  field  has  seen  an  increase  in  the number  of  available  focused  data  resources  as E2E (Novikova et al., 2017), ROTOWIRE(Wise-man  et  al.,  2017)  and  WebNLG  (Gardent  et  al.,2017a,b) corpora. Although theses recent releases are highly valuable resources for the NLG community in general,nall  of  them  were  designed  to  work  with  end-to-end NLG models.   Hence,  they consist of a collection  of  parallel  raw  representations  and  their corresponding  textual  realizations.   No  intermediate representations are available so researchersncan straight-forwardly use them to develop or evaluate  popular tasks  in NLG  pipelines (Reiter  and Dale, 2000), such as Discourse Ordering, Lexicalization,  Aggregation,  Referring Expression Generation, among others.  Moreover, these new corpora, like many other resources in Computational Linguistics  more  in  general,  are  only  available in  English,  limiting  the  development  of  NLG-applications  to  other  languages.


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

The dataset uses the `cc-by-nc-sa-4.0` license. The source DBpedia project uses the `cc-by-sa-3.0` and `gfdl-1.1`
licenses.

### Citation Information

- If you use the Enriched WebNLG corpus, cite:

```
@InProceedings{ferreiraetal2018,
  author = 	"Castro Ferreira, Thiago
		and Moussallem, Diego
		and Wubben, Sander
		and Krahmer, Emiel",
  title = 	"Enriching the WebNLG corpus",
  booktitle = 	"Proceedings of the 11th International Conference on Natural Language Generation",
  year = 	"2018",
  series = {INLG'18},
  publisher = 	"Association for Computational Linguistics",
  address = 	"Tilburg, The Netherlands",
}

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
### Contributions

Thanks to [@TevenLeScao](https://github.com/TevenLeScao) for adding this dataset.