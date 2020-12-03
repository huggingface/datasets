---
annotations_creators:
- expert-generated
- no-annotation
language_creators:
- expert-generated
languages:
- th
licenses:
- unknown
multilinguality:
- monolingual
size_categories:
- n<1K
source_datasets:
- original
task_categories:
- sequence-modeling
task_ids:
- language-modeling
---

# Dataset Card for Thai Literature Corpora (TLC)

## Table of Contents
- [Dataset Description](#dataset-description)
  - [Dataset Summary](#dataset-summary)
  - [Supported Tasks](#supported-tasks-and-leaderboards)
  - [Languages](#languages)
- [Dataset Structure](#dataset-structure)
  - [Data Instances](#data-instances)
  - [Data Fields](#data-instances)
- [Considerations for Using the Data](#considerations-for-using-the-data)
  - [Other Known Limitations](#other-known-limitations)
- [Additional Information](#additional-information)
  - [Dataset Curators](#dataset-curators)
  - [Licensing Information](#licensing-information)
  - [Citation Information](#citation-information)

## Dataset Description

- **Homepage:** https://attapol.github.io/tlc.html
- **Leaderboard:** https://www.kaggle.com/c/wisesight-sentiment/
- **Point of Contact:**  Jitkapat Sawatphol, Attapol Rutherford; attapolrutherford at gmail.com

### Dataset Summary
Thai Literature Corpora (TLC): Corpora of machine-ingestible Thai classical literature texts.

It consists of two datasets:

## TLC set
It is texts from [Vajirayana Digital Library](https://vajirayana.org/), stored by chapters and stanzas (non-tokenized).

tlc v.2.0 (6/17/19 : a total of 34 documents, 292,270 lines, 31,790,734 characters)
tlc v.1.0 (6/11/19 : a total of 25 documents, 113,981 lines, 28,775,761 characters)

## TNHC set
It is texts from Thai National Historical Corpus, stored by lines (manually tokenized).

tnhc v.1.0 (6/25/19 : a total of 47 documents, 756,478 lines, 13,361,142 characters)

### Languages

Thai

## Dataset Structure

### Data Instances

```
{
    "ch_num": "๑",
    "title": "กากี กลอนสุภาพ",
    "text": [
      [
        "๏ จักกล่าวอดีตนิทานแต่ปางก่อน\n",
        "เมื่อครั้งองค์สมเด็จพระชินวร\tยังสัญจรแสวงหาโพธิญาณ\n",
        "เสวยชาติเป็นสกุณาพระยานก\tจึงชักเรื่องชาดกมาบรรหาร\n",
        "หวังแสดงแห่งจิตหญิงพาล\tให้ชายชาญรู้เชิงกระสัตรี ฯ\n"
      ]
}
```

### Data Fields

- `ch_num`: chapter number in Thai Numerals (๑, ๒, ๓, ๔, ๕, ๖, ๗, ๘, ๙, ๑๐, ...)  
- `title`: chapter name
- `text`: each item corresponds to one stanzas, each line is a couplet which can be seperated by `\t`

## Additional Information

### Dataset Curators

Thanks [Jitkapat Sawatphol](https://jitkapat.github.io/) (Faculty of Arts, Chulalongkorn University), and [Attapol Rutherford](https://attapol.github.io/) (Faculty of Arts, Chulalongkorn University)

### Licensing Information

Not mentioned on the source website.

### Citation Information

Please cite the following if you make use of the dataset:

Jitkapat Sawatphol, and Attapol Rutherford. 2019. **Thai Literature Corpora (TLC)**.

BibTeX:
```
@misc{
  author={Sawatphol, Jitkapat},
  title={Thai Literature Corpora},
  year={2019},
  howpublished={\\url{https://attapol.github.io/tlc.html}}
}
```
