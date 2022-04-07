---
pretty_name: ASSIN
annotations_creators:
- expert-generated
language_creators:
- found
languages:
- pt
licenses:
- unknown
multilinguality:
- monolingual
size_categories:
- 10K<n<100K
source_datasets:
- original
task_categories:
- text-classification
- text-scoring
task_ids:
- natural-language-inference
- semantic-similarity-scoring
paperswithcode_id: assin
---

# Dataset Card for ASSIN

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

- **Homepage:** [ASSIN homepage](http://nilc.icmc.usp.br/assin/)
- **Repository:** [ASSIN repository](http://nilc.icmc.usp.br/assin/)
- **Paper:** [ASSIN: Evaluation of Semantic Similarity and Textual Inference](http://propor2016.di.fc.ul.pt/wp-content/uploads/2015/10/assin-overview.pdf)
- **Point of Contact:** [Erick Rocha Fonseca](mailto:erickrf@icmc.usp.br)

### Dataset Summary

The ASSIN (Avaliação de Similaridade Semântica e INferência textual) corpus is a corpus annotated with pairs of sentences written in 
Portuguese that is suitable for the  exploration of textual entailment and paraphrasing classifiers. The corpus contains pairs of sentences 
extracted from news articles written in European Portuguese (EP) and Brazilian Portuguese (BP), obtained from Google News Portugal 
and Brazil, respectively. To create the corpus, the authors started by collecting a set of news articles describing the 
same event (one news article from Google News Portugal and another from Google News Brazil) from Google News. 
Then, they employed Latent Dirichlet Allocation (LDA) models to retrieve pairs of similar sentences between sets of news 
articles that were grouped together around the same topic. For that, two LDA models were trained (for EP and for BP) 
on external and large-scale collections of unannotated news articles from Portuguese and Brazilian news providers, respectively. 
Then, the authors defined a lower and upper threshold for the sentence similarity score of the retrieved pairs of sentences, 
taking into account that high similarity scores correspond to sentences that contain almost the same content (paraphrase candidates), 
and low similarity scores correspond to sentences that are very different in content from each other (no-relation candidates).
From the collection of pairs of sentences obtained at this stage, the authors performed some manual grammatical corrections 
and discarded some of the pairs wrongly retrieved. Furthermore, from a preliminary analysis made to the retrieved sentence pairs 
the authors noticed that the number of contradictions retrieved during the previous stage was very low. Additionally, they also 
noticed that event though paraphrases are not very frequent, they occur with some frequency in news articles. Consequently, 
in contrast with the majority of the currently available corpora for other languages, which consider as labels “neutral”, “entailment” 
and “contradiction” for the task of RTE, the authors of the ASSIN corpus decided to use as labels “none”, “entailment” and “paraphrase”.
Finally, the manual annotation of pairs of sentences was performed by human annotators. At least four annotators were randomly 
selected to annotate each pair of sentences, which is done in two steps: (i) assigning a semantic similarity label (a score between 1 and 5, 
from unrelated to very similar); and (ii) providing an entailment label (one sentence entails the other, sentences are paraphrases, 
or no relation). Sentence pairs where at least three annotators do not agree on the entailment label were considered controversial 
and thus discarded from the gold standard annotations. The full dataset has 10,000 sentence pairs, half of which in Brazilian Portuguese (ptbr) 
and half in European Portuguese (ptpt). Either language variant has 2,500 pairs for training, 500 for validation and 2,000 for testing.

### Supported Tasks and Leaderboards

[More Information Needed]

### Languages

The language supported is Portuguese.

## Dataset Structure

### Data Instances

An example from the ASSIN dataset looks as follows:

```
{
  "entailment_judgment": 0,
  "hypothesis": "André Gomes entra em campo quatro meses depois de uma lesão na perna esquerda o ter afastado dos relvados.",
  "premise": "Relembre-se que o atleta estava afastado dos relvados desde maio, altura em que contraiu uma lesão na perna esquerda.",
  "relatedness_score": 3.5,
  "sentence_pair_id": 1
}
```

### Data Fields

- `sentence_pair_id`: a `int64` feature.
- `premise`: a `string` feature.
- `hypothesis`: a `string` feature.
- `relatedness_score`: a `float32` feature.
- `entailment_judgment`: a classification label, with possible values including `NONE`, `ENTAILMENT`, `PARAPHRASE`.

### Data Splits

The data is split into train, validation and test set. The split sizes are as follow:

|         | Train  | Val   | Test |
| -----   | ------ | ----- | ---- |
| full    | 5000   | 1000  | 4000 |
| ptbr    | 2500   | 500   | 2000 |
| ptpt    | 2500   | 500   | 2000 |

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
@inproceedings{fonseca2016assin,
  title={ASSIN: Avaliacao de similaridade semantica e inferencia textual},
  author={Fonseca, E and Santos, L and Criscuolo, Marcelo and Aluisio, S},
  booktitle={Computational Processing of the Portuguese Language-12th International Conference, Tomar, Portugal},
  pages={13--15},
  year={2016}
}
```

### Contributions

Thanks to [@jonatasgrosman](https://github.com/jonatasgrosman) for adding this dataset.