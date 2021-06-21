---
annotations_creators:
- expert-generated
language_creators:
- found
languages:
- pl
licenses:
- cc-by-sa-3.0
multilinguality:
- monolingual
size_categories:
- 1K<n<10K
source_datasets:
- original
task_categories:
- text-classification
task_ids:
- semantic-similarity-classification
paperswithcode_id: null
---

# Dataset Card for wrbsc

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

- **Homepage:** https://clarin-pl.eu/dspace/handle/11321/305
- **Repository:** https://clarin-pl.eu/dspace/handle/11321/305
- **Paper:** [Needs More Information]
- **Leaderboard:** [Needs More Information]
- **Point of Contact:** [Needs More Information]

### Dataset Summary

WUT Relations Between Sentences Corpus contains 2827 pairs of related sentences. Relationships are derived from Cross-document Structure Theory (CST), which enables multi-document summarization through identification of cross-document rhetorical relationships within a cluster of related documents. Every relation was marked by at least 3 annotators.

### Supported Tasks and Leaderboards

[Needs More Information]

### Languages

Polish

## Dataset Structure

### Data Instances
An example contains two related sentences and a class representing the type of relationship between those sentences. 

```
{'relationship': 0,
 'sentence1': 'Znajdujące się w Biurze Bezpieczeństwa Narodowego akta Komisji Weryfikacyjnej WSI zostały przewiezione do siedziby Służby Kontrwywiadu Wojskowego.',
 'sentence2': '2008-07-03: Wywiezienie akt dotyczących WSI – sprawa dla prokuratury?'}
```

### Data Fields

- `sentence1`: the first sentence being compared (`string`)
- `sentence2`: the second sentence being compared (`string`)
- `relationship`: the type of relationship between those sentences. Can be one of 16 classes listed below:
  - `Krzyżowanie_się`: crossing
  - `Tło_historyczne`: historical background
  - `Źródło`: source
  - `Dalsze_informacje`: additional information
  - `Zawieranie`: inclusion
  - `Opis`: description
  - `Uszczegółowienie`: further detail 
  - `Parafraza`: paraphrase
  - `Spełnienie`: fulfillment
  - `Mowa_zależna`: passive voice
  - `Zmiana_poglądu`: change of opinion
  - `Streszczenie`: summarization
  - `Tożsamość`: identity
  - `Sprzeczność`: conflict
  - `Modalność`: modality
  - `Cytowanie`: quotation

### Data Splits

Single train split

## Dataset Creation

### Curation Rationale

[Needs More Information]

### Source Data

#### Initial Data Collection and Normalization

[Needs More Information]

#### Who are the source language producers?

[Needs More Information]

### Annotations

#### Annotation process

[Needs More Information]

#### Who are the annotators?

[Needs More Information]

### Personal and Sensitive Information

[Needs More Information]

## Considerations for Using the Data

### Social Impact of Dataset

[Needs More Information]

### Discussion of Biases

[Needs More Information]

### Other Known Limitations

[Needs More Information]

## Additional Information

### Dataset Curators

[Needs More Information]

### Licensing Information

Attribution-ShareAlike 3.0 Unported (CC BY-SA 3.0)

### Citation Information
```
@misc{11321/305,	
 title = {{WUT} Relations Between Sentences Corpus},	
 author = {Oleksy, Marcin and Fikus, Dominika and Wolski, Micha{\l} and Podbielska, Ma{\l}gorzata and Turek, Agnieszka and Kędzia, Pawe{\l}},	
 url = {http://hdl.handle.net/11321/305},	
 note = {{CLARIN}-{PL} digital repository},	
 copyright = {Attribution-{ShareAlike} 3.0 Unported ({CC} {BY}-{SA} 3.0)},	
 year = {2016}	
}
```
### Contributions

Thanks to [@kldarek](https://github.com/kldarek) for adding this dataset.