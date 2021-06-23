---
annotations_creators:
- expert-generated
- machine-generated
language_creators:
- found
- expert-generated
languages:
- th
licenses:
- cc-by-3.0
multilinguality:
- monolingual
size_categories:
- 1K<n<10K
source_datasets:
- extended|other-tirasaroj-aroonmanakun
task_categories:
- structure-prediction
task_ids:
- named-entity-recognition
- part-of-speech-tagging
paperswithcode_id: null
---

# Dataset Card for `thainer`

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

- **Homepage:** https://github.com/wannaphong/thai-ner
- **Repository:** https://github.com/wannaphong/thai-ner
- **Paper:**
- **Leaderboard:**
- **Point of Contact:** https://github.com/wannaphong/

### Dataset Summary

ThaiNER (v1.3) is a 6,456-sentence named entity recognition dataset created from expanding the 2,258-sentence [unnamed dataset](http://pioneer.chula.ac.th/~awirote/Data-Nutcha.zip) by [Tirasaroj and Aroonmanakun (2012)](http://pioneer.chula.ac.th/~awirote/publications/). It is used to train NER taggers in [PyThaiNLP](https://github.com/PyThaiNLP/pythainlp). The NER tags are annotated by [Tirasaroj and Aroonmanakun (2012)]((http://pioneer.chula.ac.th/~awirote/publications/)) for 2,258 sentences and the rest by [@wannaphong](https://github.com/wannaphong/). The POS tags are done by [PyThaiNLP](https://github.com/PyThaiNLP/pythainlp)'s `perceptron` engine trained on `orchid_ud`. [@wannaphong](https://github.com/wannaphong/) is now the only maintainer of this dataset.

### Supported Tasks and Leaderboards

- named entity recognition
- pos tagging

### Languages

Thai

## Dataset Structure

### Data Instances

```
{'id': 100, 'ner_tags': [27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27], 'pos_tags': [6, 12, 13, 1, 6, 5, 11, 7, 11, 6, 5, 13, 6, 6, 6, 11, 6, 6, 11, 6, 6, 11, 6, 6, 13, 6, 11, 11, 6, 11, 6, 11, 6, 11, 6, 11, 11, 6, 6, 11, 12, 6, 13, 5, 11, 7, 11, 6, 3, 11, 12, 3, 13, 6, 1, 6, 12, 13, 1, 6, 6, 5, 11, 3, 11, 5, 4, 6, 13, 6, 13, 6, 10, 3, 13, 13, 12, 13, 12, 0, 1, 10, 11, 6, 6, 11, 6, 11, 6, 12, 13, 5, 12, 3, 13, 13, 1, 6, 1, 6, 13], 'tokens': ['เชื้อโรค', 'ที่', 'ปรากฏ', 'ใน', 'สัตว์', 'ทั้ง', ' ', '4', ' ', 'ชนิด', 'นี้', 'เป็น', 'เชื้อ', 'โรคไข้หวัด', 'นก', ' ', 'เอช', 'พี', ' ', 'เอ', 'เวียน', ' ', 'อิน', 'ฟลู', 'เอน', 'ซา', ' ', '(', 'Hight', ' ', 'Polygenic', ' ', 'Avain', ' ', 'Influenza', ')', ' ', 'ชนิด', 'รุนแรง', ' ', 'ซึ่ง', 'การ', 'ตั้งชื่อ', 'ทั้ง', ' ', '4', ' ', 'ขึ้น', 'มา', ' ', 'เพื่อที่จะ', 'สามารถ', 'ระบุ', 'เชื้อ', 'ของ', 'ไวรัส', 'ที่', 'ทำอันตราย', 'ตาม', 'สิ่งมีชีวิต', 'ประเภท', 'ต่างๆ', ' ', 'ได้', ' ', 'อีก', 'ทั้ง', 'การ', 'ระบุ', 'สถานที่', 'คือ', 'ประเทศ', 'ไทย', 'จะ', 'ทำให้', 'รู้', 'ว่า', 'พบ', 'ที่', 'แรก', 'ใน', 'ไทย', ' ', 'ส่วน', 'วัน', ' ', 'เดือน', ' ', 'ปี', 'ที่', 'พบ', 'นั้น', 'ก็', 'จะ', 'ทำให้', 'ทราบ', 'ถึง', 'ครั้งแรก', 'ของ', 'การ', 'ค้นพบ']}
{'id': 107, 'ner_tags': [27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27], 'pos_tags': [0, 1, 6, 5, 11, 12, 3, 3, 13, 6, 13, 12, 0, 2, 12, 11, 6, 5, 13, 6, 5, 1, 6, 6, 1, 10, 11, 4, 13, 6, 11, 12, 6, 6, 10, 11, 13, 6, 1, 6, 4, 6, 1, 6, 6, 11, 4, 6, 1, 5, 6, 12, 2, 13, 6, 6, 5, 1, 11, 12, 13, 1, 6, 6, 11, 13, 11, 6, 6, 6, 11, 11, 6, 11, 11, 4, 10, 11, 11, 6, 11], 'tokens': ['ล่าสุด', 'ใน', 'เรื่อง', 'นี้', ' ', 'ทั้งนี้', 'คง', 'ต้อง', 'มี', 'การ', 'ตรวจสอบ', 'ให้', 'ชัดเจน', 'อีกครั้ง', 'ว่า', ' ', 'ไวรัส', 'นี้', 'เป็น', 'ชนิด', 'เดียว', 'กับ', 'ไข้หวัด', 'นก', 'ใน', 'ไทย', ' ', 'หรือ', 'เป็น', 'การกลายพันธุ์', ' ', 'โดยที่', 'คณะ', 'สัตวแพทย์', 'มหาวิทยาลัยเกษตรศาสตร์', ' ', 'จัด', 'ระดมสมอง', 'จาก', 'คณบดี', 'และ', 'ผู้เชี่ยวชาญ', 'จาก', 'คณะ', 'สัตวแพทย์', ' ', 'และ', 'ปศุสัตว์', 'ของ', 'หลาย', 'มหาวิทยาลัย', 'เพื่อ', 'ร่วมกัน', 'หา', 'ข้อมูล', 'เรื่อง', 'นี้', 'ด้วย', ' ', 'โดย', 'ประสาน', 'กับ', 'เจ้าหน้าที่', 'ระหว่างประเทศ', ' ', 'คือ', ' ', 'องค์การ', 'สุขภาพ', 'สัตว์โลก', ' ', '(', 'OIE', ')', ' ', 'และ', 'องค์การอนามัยโลก', ' ', '(', 'WHO', ')']}
```

### Data Fields

- `id`: sentence id
- `tokens`: word tokens by [PyThaiNLP](https://github.com/PyThaiNLP/pythainlp)'s dictionary-based tokenizer `newmm`
- `pos_tags`: POS tags tagged by [PyThaiNLP](https://github.com/PyThaiNLP/pythainlp)'s `perceptron` engine trained on `orchid_ud`
- `ner_tags`: NER tags tagged by humans

### Data Splits

No explicit split is given

## Dataset Creation

### Curation Rationale

ThaiNER (v1.3) is a 6,456-sentence named entity recognition dataset created from expanding the 2,258-sentence [unnamed dataset](http://pioneer.chula.ac.th/~awirote/Data-Nutcha.zip) by [Tirasaroj and Aroonmanakun (2012)](http://pioneer.chula.ac.th/~awirote/publications/). It is used to train NER taggers in [PyThaiNLP](https://github.com/PyThaiNLP/pythainlp). 

### Source Data

#### Initial Data Collection and Normalization

The earlier part of the dataset is all news articles, whereas the part added by [@wannaphong](https://github.com/wannaphong/) includes news articles, public announcements and [@wannaphong](https://github.com/wannaphong/)'s own chat messages with personal and sensitive information removed.

#### Who are the source language producers?

News articles and public announcements are created by their respective authors. Chat messages are created by [@wannaphong](https://github.com/wannaphong/).

### Annotations

#### Annotation process

[More Information Needed]

#### Who are the annotators?

[Tirasaroj and Aroonmanakun (2012)](http://pioneer.chula.ac.th/~awirote/publications/) for the earlier 2,258 sentences and [@wannaphong](https://github.com/wannaphong/) for the rest

### Personal and Sensitive Information

News articles and public announcements are not expected to include personal and sensitive information. [@wannaphong](https://github.com/wannaphong/) has removed such information from his own chat messages.

## Considerations for Using the Data

### Social Impact of Dataset

- named entity recognition in Thai

### Discussion of Biases

Since almost all of collection and annotation is done by [@wannaphong](https://github.com/wannaphong/), his biases are expected to be reflected in the dataset.

### Other Known Limitations

[More Information Needed]

## Additional Information

### Dataset Curators

[Tirasaroj and Aroonmanakun (2012)](http://pioneer.chula.ac.th/~awirote/publications/) for the earlier 2,258 sentences and [@wannaphong](https://github.com/wannaphong/) for the rest

### Licensing Information

CC-BY 3.0

### Citation Information

```
@misc{Wannaphong Phatthiyaphaibun_2019,
    title={wannaphongcom/thai-ner: ThaiNER 1.3},
    url={https://zenodo.org/record/3550546},
    DOI={10.5281/ZENODO.3550546},
    abstractNote={Thai Named Entity Recognition},
    publisher={Zenodo},
    author={Wannaphong Phatthiyaphaibun},
    year={2019},
    month={Nov}
}
```

Work extended from:
[Tirasaroj, N.  and Aroonmanakun, W. 2012. Thai NER using CRF model based on surface features. In Proceedings of SNLP-AOS 2011, 9-10 February, 2012, Bangkok, pages 176-180.](http://pioneer.chula.ac.th/~awirote/publications/)

### Contributions

Thanks to [@cstorm125](https://github.com/cstorm125) for adding this dataset.