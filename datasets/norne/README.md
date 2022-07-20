---
annotations_creators:
- expert-generated
language_creators:
- crowdsourced
language:
- "no"
license:
- other
multilinguality:
- monolingual
size_categories:
- 10K<n<100K
source_datasets:
- original
task_categories:
- token-classification
task_ids:
- named-entity-recognition
paperswithcode_id: null
pretty_name: 'NorNE: Norwegian Named Entities'
---

# Dataset Card for NorNE: Norwegian Named Entities

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

- **Homepage:** [NorNE](https://github.com/ltgoslo/norne/)
- **Repository:** [Github](https://github.com/ltgoslo/norne/)
- **Paper:** https://arxiv.org/abs/1911.12146
- **Leaderboard:**
- **Point of Contact:**

### Dataset Summary

NorNE is a manually annotated corpus of named entities which extends the annotation of the existing Norwegian Dependency Treebank. Comprising both of the official standards of written Norwegian (Bokmål and Nynorsk), the corpus contains around 600,000 tokens and annotates a rich set of entity types including persons,organizations, locations, geo-political entities, products, and events, in addition to a class corresponding to nominals derived from names.

There are 3 main configs in this dataset each with 3 versions of the NER tag set. When accessing the `bokmaal`, `nynorsk`, or `combined` configs the NER tag set will be comprised of 9 tags: `GPE_ORG`, `GPE_LOC`, `ORG`, `LOC`, `PER`, `PROD`, `EVT`, `DRV`, and `MISC`. The two special types `GPE_LOC` and `GPE_ORG` can easily be altered depending on the task, choosing either the more general `GPE` tag or the more specific `LOC`/`ORG` tags, conflating them with the other annotations of the same type. To access these reduced versions of the dataset, you can use the configs `bokmaal-7`, `nynorsk-7`, `combined-7` for the NER tag set with 7 tags ( **`ORG`**, **`LOC`**, `PER`, `PROD`, `EVT`, `DRV`, `MISC`), and `bokmaal-8`, `nynorsk-8`, `combined-8` for the NER tag set with 8 tags (`LOC_` and `ORG_`: **`ORG`**, **`LOC`**, **`GPE`**, `PER`, `PROD`, `EVT`, `DRV`, `MISC`). By default, the full set (9 tags) will be used. See Annotations for further details.

### Supported Tasks and Leaderboards

NorNE ads named entity annotations on top of the Norwegian Dependency Treebank.

### Languages

Both Norwegian Bokmål (`bokmaal`) and Nynorsk (`nynorsk`) are supported as different configs in this dataset. An extra config for the combined languages is also included (`combined`). See the Annotation section for details on accessing reduced tag sets for the NER feature.

## Dataset Structure

Each entry contains text sentences, their language, identifiers, tokens, lemmas, and corresponding NER and POS tag lists.

### Data Instances

An example of the `train` split of the `bokmaal` config.

```python
{'idx': '000001',
 'lang': 'bokmaal',
 'lemmas': ['lam', 'og', 'piggvar', 'på', 'bryllupsmeny'],
 'ner_tags': [0, 0, 0, 0, 0],
 'pos_tags': [0, 9, 0, 5, 0],
 'text': 'Lam og piggvar på bryllupsmenyen',
 'tokens': ['Lam', 'og', 'piggvar', 'på', 'bryllupsmenyen']}
```

### Data Fields

Each entry is annotated with the next fields:

- `idx` (`int`), text (sentence) identifier from the NorNE dataset
- `lang` (`str`), language variety, either `bokmaal`, `nynorsk` or `combined`
- `text` (`str`), plain text
- `tokens` (`List[str]`), list of tokens extracted from `text`
- `lemmas` (`List[str]`), list of lemmas extracted from `tokens`
- `ner_tags` (`List[int]`), list of numeric NER tags for each token in `tokens`
- `pos_tags` (`List[int]`), list of numeric PoS tags for each token in `tokens`

An example DataFrame obtained from the dataset:

<table class="dataframe" border="1">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>idx</th>
      <th>lang</th>
      <th>text</th>
      <th>tokens</th>
      <th>lemmas</th>
      <th>ner_tags</th>
      <th>pos_tags</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>000001</td>
      <td>bokmaal</td>
      <td>Lam og piggvar på bryllupsmenyen</td>
      <td>[Lam, og, piggvar, på, bryllupsmenyen]</td>
      <td>[lam, og, piggvar, på, bryllupsmeny]</td>
      <td>[0, 0, 0, 0, 0]</td>
      <td>[0, 9, 0, 5, 0]</td>
    </tr>
    <tr>
      <th>1</th>
      <td>000002</td>
      <td>bokmaal</td>
      <td>Kamskjell, piggvar og lammefilet sto på menyen...</td>
      <td>[Kamskjell, ,, piggvar, og, lammefilet, sto, p...</td>
      <td>[kamskjell, $,, piggvar, og, lammefilet, stå, ...</td>
      <td>[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]</td>
      <td>[0, 1, 0, 9, 0, 15, 2, 0, 2, 8, 6, 0, 1]</td>
    </tr>
    <tr>
      <th>2</th>
      <td>000003</td>
      <td>bokmaal</td>
      <td>Og til dessert: Parfait à la Mette-Marit.</td>
      <td>[Og, til, dessert, :, Parfait, à, la, Mette-Ma...</td>
      <td>[og, til, dessert, $:, Parfait, à, la, Mette-M...</td>
      <td>[0, 0, 0, 0, 7, 8, 8, 8, 0]</td>
      <td>[9, 2, 0, 1, 10, 12, 12, 10, 1]</td>
    </tr>
  </tbody>
</table>

### Data Splits

There are three splits: `train`, `validation` and `test`.

| Config    | Split        | Total  |
| :---------|-------------:|-------:|
| `bokmaal` | `train`      |  15696 |
| `bokmaal` | `validation` |   2410 |
| `bokmaal` | `test`       |   1939 |
| `nynorsk` | `train`      |  14174 |
| `nynorsk` | `validation` |   1890 |
| `nynorsk` | `test`       |   1511 |
| `combined`| `test`       |  29870 |
| `combined`| `validation` |   4300 |
| `combined`| `test`       |   3450 |

## Dataset Creation

### Curation Rationale

1. A _name_ in this context is close to [Saul Kripke's definition of a name](https://en.wikipedia.org/wiki/Saul_Kripke#Naming_and_Necessity),
in that a name has a unique reference and its meaning is constant (there are exceptions in the annotations, e.g. "Regjeringen" (en. "Government")).
2. It is the usage of a name that determines the entity type, not the default/literal sense of the name,
3. If there is an ambiguity in the type/sense of a name, then the the default/literal sense of the name is chosen
(following [Markert and Nissim, 2002](http://www.lrec-conf.org/proceedings/lrec2002/pdf/11.pdf)).

For more details, see the "Annotation Guidelines.pdf" distributed with the corpus.

### Source Data

Data was collected using blogs and newspapers in Norwegian, as well as parliament speeches and governamental reports.

#### Initial Data Collection and Normalization

The texts in the Norwegian Dependency Treebank (NDT) are manually annotated with morphological features, syntactic functions
and hierarchical structure. The formalism used for the syntactic annotation is dependency grammar.

The treebanks consists of two parts, one part in Norwegian Bokmål (`nob`) and one part in Norwegian Nynorsk (`nno`).
Both parts contain around 300.000 tokens, and are a mix of different non-fictional genres.

See the [NDT webpage](https://www.nb.no/sprakbanken/show?serial=sbr-10) for more details.

### Annotations

The following types of entities are annotated:

- **Person (`PER`):** Real or fictional characters and animals
- **Organization (`ORG`):** Any collection of people, such as firms, institutions, organizations, music groups,
 sports teams, unions, political parties etc.
- **Location (`LOC`):** Geographical places, buildings and facilities
- **Geo-political entity (`GPE`):** Geographical regions defined by political and/or social groups.
A GPE entity subsumes and does not distinguish between a nation, its region, its government, or its people
- **Product (`PROD`):** Artificially produced entities are regarded products. This may include more abstract entities, such as speeches,
radio shows, programming languages, contracts, laws and ideas.
- **Event (`EVT`):** Festivals, cultural events, sports events, weather phenomena, wars, etc. Events are bounded in time and space.
- **Derived (`DRV`):** Words (and phrases?) that are dervied from a name, but not a name in themselves. They typically contain a full name and are capitalized, but are not proper nouns. Examples (fictive) are "Brann-treneren" ("the Brann coach") or "Oslo-mannen" ("the man from Oslo").
- **Miscellaneous (`MISC`):** Names that do not belong in the other categories. Examples are animals species and names of medical conditions. Entities that are manufactured or produced are of type Products, whereas thing naturally or spontaneously occurring are of type Miscellaneous.

Furthermore, all `GPE` entities are additionally sub-categorized as being either `ORG` or `LOC`, with the two annotation levels separated by an underscore:

- `GPE_LOC`: Geo-political entity, with a locative sense (e.g. "John lives in _Spain_")
- `GPE_ORG`: Geo-political entity, with an organisation sense (e.g. "_Spain_ declined to meet with Belgium")

The two special types `GPE_LOC` and `GPE_ORG` can easily be altered depending on the task, choosing either the more general `GPE` tag or the more specific `LOC`/`ORG` tags, conflating them with the other annotations of the same type. This means that the following sets of entity types can be derived:

- 7 types, deleting `_GPE`: **`ORG`**, **`LOC`**, `PER`, `PROD`, `EVT`, `DRV`, `MISC`
- 8 types, deleting `LOC_` and `ORG_`: **`ORG`**, **`LOC`**, **`GPE`**, `PER`, `PROD`, `EVT`, `DRV`, `MISC`
- 9 types, keeping all types: **`ORG`**, **`LOC`**, **`GPE_LOC`**, **`GPE_ORG`**, `PER`, `PROD`, `EVT`, `DRV`, `MISC`

The class distribution is as follows, broken down across the data splits of the UD version of NDT, and sorted by total counts (i.e. the number of examples, not tokens within the spans of the annotatons):

| Type     | Train  | Dev    | Test   |  Total |
| :--------|-------:|-------:|-------:|-------:|
| `PER`    |   4033 |    607 |    560 |   5200 |
| `ORG`    |   2828 |    400 |    283 |   3511 |
| `GPE_LOC`|   2132 |    258 |    257 |   2647 |
| `PROD`   |    671 |    162 |     71 |    904 |
| `LOC`    |    613 |    109 |    103 |    825 |
| `GPE_ORG`|    388 |     55 |     50 |    493 |
| `DRV`    |    519 |     77 |     48 |    644 |
| `EVT`    |    131 |      9 |      5 |    145 |
| `MISC`   |      8 |      0 |      0 |      0 |

To access these reduced versions of the dataset, you can use the configs `bokmaal-7`, `nynorsk-7`, `combined-7` for the NER tag set with 7 tags ( **`ORG`**, **`LOC`**, `PER`, `PROD`, `EVT`, `DRV`, `MISC`), and `bokmaal-8`, `nynorsk-8`, `combined-8` for the NER tag set with 8 tags (`LOC_` and `ORG_`: **`ORG`**, **`LOC`**, **`GPE`**, `PER`, `PROD`, `EVT`, `DRV`, `MISC`). By default, the full set (9 tags) will be used.

## Additional Information

### Dataset Curators

NorNE was created as a collaboration between [Schibsted Media Group](https://schibsted.com/), [Språkbanken](https://www.nb.no/forskning/sprakbanken/) at the [National Library of Norway](https://www.nb.no) and the [Language Technology Group](https://www.mn.uio.no/ifi/english/research/groups/ltg/) at the University of Oslo.

NorNE was added to 🤗 Datasets by the AI-Lab at the National Library of Norway.

### Licensing Information

The NorNE corpus is published under the same [license](https://github.com/ltgoslo/norne/blob/master/LICENSE_NDT.txt) as the Norwegian Dependency Treebank

### Citation Information

This dataset is described in the paper _NorNE: Annotating Named Entities for Norwegian_ by
Fredrik Jørgensen, Tobias Aasmoe, Anne-Stine Ruud Husevåg, Lilja Øvrelid, and Erik Velldal, accepted for LREC 2020 and available as pre-print here: https://arxiv.org/abs/1911.12146.

```bibtex
@inproceedings{johansen2019ner,
  title={NorNE: Annotating Named Entities for Norwegian},
  author={Fredrik Jørgensen, Tobias Aasmoe, Anne-Stine Ruud Husevåg,
          Lilja Øvrelid, and Erik Velldal},
  booktitle={LREC 2020},
  year={2020},
  url={https://arxiv.org/abs/1911.12146}
}
```

### Contributions

Thanks to [@versae](https://github.com/versae) for adding this dataset.
