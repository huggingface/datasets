---
annotations_creators:
- expert-generated
language_creators:
- expert-generated
languages:
- en
- id
licenses:
- unknown
multilinguality:
- translation
size_categories:
- 10K<n<100K
source_datasets:
- original
task_categories:
- conditional-text-generation
task_ids:
- machine-translation
paperswithcode_id: null
---

# Dataset Card for [Dataset Name]

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

- **Homepage:** [PANL BPPT](http://digilib.bppt.go.id/sampul/p92-budiono.pdf)
- **Repository:** [PANL BPPT Repository](https://github.com/cahya-wirawan/indonesian-language-models/raw/master/data/BPPTIndToEngCorpusHalfM.zip)
- **Paper:** [Resource Report: Building Parallel Text Corpora for Multi-Domain Translation System](http://digilib.bppt.go.id/sampul/p92-budiono.pdf)
- **Leaderboard:**
- **Point of Contact:**

### Dataset Summary
Parallel Text Corpora for Multi-Domain Translation System created by BPPT (Indonesian Agency for the Assessment and 
Application of Technology) for PAN Localization Project (A Regional Initiative to Develop Local Language Computing 
Capacity in Asia). The dataset contains around 24K sentences divided in 4 difference topics (Economic, international,
Science and Technology and Sport).
### Supported Tasks and Leaderboards

[More Information Needed]

### Languages

Indonesian

## Dataset Structure

[More Information Needed]

### Data Instances

An example of the dataset:
```
{ 
  'id': '0',
  'topic': 0,
  'translation':
    { 
      'en': 'Minister of Finance Sri Mulyani Indrawati said that a sharp correction of the composite
inde x by up to 4 pct in Wedenesday?s trading was a mere temporary effect of regional factors like
decline in plantation commodity prices and the financial crisis in Thailand.',
      'id': 'Menteri Keuangan Sri Mulyani mengatakan koreksi tajam pada Indeks Harga Saham Gabungan
IHSG hingga sekitar 4 persen dalam perdagangan Rabu 10/1 hanya efek sesaat dari faktor-faktor regional
seperti penurunan harga komoditi perkebunan dan krisis finansial di Thailand.'
    }
}
```

### Data Fields
- `id`: id of the sample
- `translation`: the parallel sentence english-indonesian
- `topic`: the topic of the sentence. It could be one of the following:
  - Economic
  - International
  - Science and Technology
  - Sport


### Data Splits

The dataset is splitted in to train, validation and test sets.

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

[More Information Needed]

### Contributions

Thanks to [@cahya-wirawan](https://github.com/cahya-wirawan) for adding this dataset.