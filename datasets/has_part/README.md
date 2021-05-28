---
annotations_creators:
- machine-generated
language_creators:
- found
languages:
- en
licenses:
- unknown
multilinguality:
- monolingual
size_categories:
- 10K<n<100K
source_datasets:
- extended|other-Generics-KB
task_categories:
- text-scoring
task_ids:
- text-scoring-other-Meronym-Prediction
paperswithcode_id: haspart-kb
---

# Dataset Card for [HasPart]

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

- **Homepage:** https://allenai.org/data/haspartkb
- **Repository:**
- **Paper:** https://arxiv.org/abs/2006.07510
- **Leaderboard:**
- **Point of Contact:** Peter Clark <peterc@allenai.org>

### Dataset Summary

This dataset is a new knowledge-base (KB) of hasPart relationships, extracted from a large corpus of generic statements. Complementary to other resources available, it is the first which is all three of: accurate (90% precision), salient (covers relationships a person may mention), and has high coverage of common terms (approximated as within a 10 year old’s vocabulary), as well as having several times more hasPart entries than in the popular ontologies ConceptNet and WordNet. In addition, it contains information about quantifiers, argument modifiers, and links the entities to appropriate concepts in Wikipedia and WordNet.

### Supported Tasks and Leaderboards

Text Classification / Scoring - meronyms (e.g., `plant` has part `stem`)

### Languages

English

## Dataset Structure

### Data Instances

[More Information Needed]
```
{'arg1': 'plant',
 'arg2': 'stem',
 'score': 0.9991798414303377,
 'synset': ['wn.plant.n.02', 'wn.stalk.n.02'],
 'wikipedia_primary_page': ['Plant']}

```

### Data Fields

- `arg1`, `arg2`: These are the entities of the meronym, i.e., `arg1` _has\_part_ `arg2`
- `score`: Meronymic score per the procedure described below
- `synset`: Ontological classification from WordNet for the two entities
- `wikipedia_primary_page`: Wikipedia page of the entities

**Note**: some examples contain synset / wikipedia info for only one of the entities.

### Data Splits

Single training file

## Dataset Creation

Our approach to hasPart extraction has five steps:

1. Collect generic sentences from a large corpus
2. Train and apply a RoBERTa model to identify hasPart relations in those sentences
3. Normalize the entity names
4. Aggregate and filter the entries
5. Link the hasPart arguments to Wikipedia pages and WordNet senses

Rather than extract knowledge from arbitrary text, we extract hasPart relations from generic sentences, e.g., “Dogs have tails.”, in order to bias the process towards extractions that are general (apply to most members of a category) and salient (notable enough to write down). As a source of generic sentences, we use **GenericsKB**, a large repository of 3.4M standalone generics previously harvested from a Webcrawl of 1.7B sentences.

### Annotations

#### Annotation process

For each sentence _S_ in GenericsKB, we identify all noun chunks in the sentence using a noun chunker (spaCy's Doc.noun chunks). Each chunk is a candidate whole or part. Then, for each possible pair, we use a RoBERTa model to classify whether a hasPart relationship exists between them. The input sentence is presented to RoBERTa as a sequence of wordpiece tokens, with the start and end of the candidate hasPart arguments identified using special tokens, e.g.:

> `[CLS] [ARG1-B]Some pond snails[ARG1-E] have [ARG2-B]gills[ARG2-E] to
breathe in water.`

where `[ARG1/2-B/E]` are special tokens denoting the argument boundaries. The `[CLS]` token is projected to two class labels (hasPart/notHasPart), and a softmax layer is then applied, resulting in output probabilities for the class labels. We train with cross-entropy loss. We use RoBERTa-large (24 layers), each with a hidden size of 1024, and 16 attention heads, and a total of 355M parameters. We use the pre-trained weights available with the
model and further fine-tune the model parameters by training on our labeled data for 15 epochs. To train the model, we use a hand-annotated set of ∼2k examples.

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

@misc{bhakthavatsalam2020dogs,
      title={Do Dogs have Whiskers? A New Knowledge Base of hasPart Relations}, 
      author={Sumithra Bhakthavatsalam and Kyle Richardson and Niket Tandon and Peter Clark},
      year={2020},
      eprint={2006.07510},
      archivePrefix={arXiv},
      primaryClass={cs.CL}
}

### Contributions

Thanks to [@jeromeku](https://github.com/jeromeku) for adding this dataset.