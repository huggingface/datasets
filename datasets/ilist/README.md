---
task_categories:
- text-classification
multilinguality:
- multilingual
task_ids:
- text-classification-other-language-identification
language:
- awa
- bho
- bra
- hi
- mag
language_creators:
- found
annotations_creators:
- no-annotation
source_datasets:
- original
size_categories:
- 10K<n<100K
license:
- cc-by-4.0
paperswithcode_id: null
pretty_name: ilist
dataset_info:
  features:
  - name: language_id
    dtype:
      class_label:
        names:
          0: AWA
          1: BRA
          2: MAG
          3: BHO
          4: HIN
  - name: text
    dtype: string
  splits:
  - name: test
    num_bytes: 2146857
    num_examples: 9692
  - name: train
    num_bytes: 14362998
    num_examples: 70351
  - name: validation
    num_bytes: 2407643
    num_examples: 10329
  download_size: 18284850
  dataset_size: 18917498
---

# Dataset Card for ilist

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

- **Homepage:**
- **Repository:** https://github.com/kmi-linguistics/vardial2018
- **Paper:** [Language Identification and Morphosyntactic Tagging: The Second VarDial Evaluation Campaign](https://aclanthology.org/W18-3901/)
- **Leaderboard:**
- **Point of Contact:** linguistics.kmi@gmail.com

### Dataset Summary

This dataset is introduced in a task which aimed at identifying 5 closely-related languages of Indo-Aryan language family: Hindi (also known as Khari Boli), Braj Bhasha, Awadhi, Bhojpuri and Magahi. These languages form part of a continuum starting from Western Uttar Pradesh (Hindi and Braj Bhasha) to Eastern Uttar Pradesh (Awadhi and Bhojpuri) and the neighbouring Eastern state of Bihar (Bhojpuri and Magahi).

For this task, participants were provided with a dataset of approximately 15,000 sentences in each language, mainly from the domain of literature, published over the web as well as in print.

### Supported Tasks and Leaderboards

[More Information Needed]

### Languages

 Hindi, Braj Bhasha, Awadhi, Bhojpuri and Magahi

## Dataset Structure

### Data Instances

```
{
    "language_id": 4,
    "text": 'तभी बारिश हुई थी जिसका गीलापन इन मूर्तियों को इन तस्वीरों में एक अलग रूप देता है .'
}
```

### Data Fields

- `text`: text which you want to classify
- `language_id`: label for the text as an integer from 0 to 4
The language ids correspond to the following languages: "AWA", "BRA", "MAG", "BHO", "HIN".

### Data Splits

|                      | train | valid | test  |
|----------------------|-------|-------|-------|
| # of input sentences | 70351 | 9692  | 10329 |

## Dataset Creation

### Curation Rationale

[More Information Needed]

### Source Data

The data for this task was collected from both hard printed and digital sources. Printed materials were
obtained from different institutions that promote these languages. We also gathered data from libraries,
as well as from local literary and cultural groups. We collected printed stories, novels and essays in
books, magazines, and newspapers.

#### Initial Data Collection and Normalization

We scanned the printed materials, then we performed OCR, and
finally we asked native speakers of the respective languages to correct the OCR output. Since there are
no specific OCR models available for these languages, we used the Google OCR for Hindi, part of the
Drive API. Since all the languages used the Devanagari script, we expected the OCR to work reasonably
well, and overall it did. We further managed to get some blogs in Magahi and Bhojpuri.

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

This work is licensed under a Creative Commons Attribution 4.0 International License: http://creativecommons.org/licenses/by/4.0/

### Citation Information

```
@inproceedings{zampieri-etal-2018-language,
    title = "Language Identification and Morphosyntactic Tagging: The Second {V}ar{D}ial Evaluation Campaign",
    author = {Zampieri, Marcos  and
      Malmasi, Shervin  and
      Nakov, Preslav  and
      Ali, Ahmed  and
      Shon, Suwon  and
      Glass, James  and
      Scherrer, Yves  and
      Samard{\v{z}}i{\'c}, Tanja  and
      Ljube{\v{s}}i{\'c}, Nikola  and
      Tiedemann, J{\"o}rg  and
      van der Lee, Chris  and
      Grondelaers, Stefan  and
      Oostdijk, Nelleke  and
      Speelman, Dirk  and
      van den Bosch, Antal  and
      Kumar, Ritesh  and
      Lahiri, Bornini  and
      Jain, Mayank},
    booktitle = "Proceedings of the Fifth Workshop on {NLP} for Similar Languages, Varieties and Dialects ({V}ar{D}ial 2018)",
    month = aug,
    year = "2018",
    address = "Santa Fe, New Mexico, USA",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/W18-3901",
    pages = "1--17",
}
```

### Contributions

Thanks to [@vasudevgupta7](https://github.com/vasudevgupta7) for adding this dataset.