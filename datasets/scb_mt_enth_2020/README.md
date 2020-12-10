---
annotations_creators:
- crowdsourced
- expert-generated
- found
- machine-generated
language_creators:
- expert-generated
- found
- machine-generated
languages:
- en
- th
licenses:
- cc-by-sa-4.0
multilinguality:
- translation
size_categories:
- n>1M
source_datasets:
- original
task_categories:
- conditional-text-generation
task_ids:
- machine-translation
---

# Dataset Card for `scb_mt_enth_2020`

## Table of Contents
- [Dataset Description](#dataset-description)
  - [Dataset Summary](#dataset-summary)
  - [Supported Tasks](#supported-tasks-and-leaderboards)
  - [Languages](#languages)
- [Dataset Structure](#dataset-structure)
  - [Data Instances](#data-instances)
  - [Data Fields](#data-instances)
  - [Data Splits](#data-instances)
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

## Dataset Description

- **Homepage:** https://airesearch.in.th/
- **Repository:** https://github.com/vistec-AI/thai2nmt
- **Paper:** https://arxiv.org/abs/2007.03541
- **Leaderboard:** 
- **Point of Contact:** https://airesearch.in.th/

### Dataset Summary

scb-mt-en-th-2020: A Large English-Thai Parallel Corpus
The primary objective of our work is to build a large-scale English-Thai dataset for machine translation.
We construct an English-Thai machine translation dataset with over 1 million segment pairs, curated from various sources,
namely news, Wikipedia articles, SMS messages, task-based dialogs, web-crawled data and government documents.
Methodology for gathering data, building parallel texts and removing noisy sentence pairs are presented in a reproducible manner.
We train machine translation models based on this dataset. Our models' performance are comparable to that of
Google Translation API (as of May 2020) for Thai-English and outperform Google when the Open Parallel Corpus (OPUS) is
included in the training data for both Thai-English and English-Thai translation.
The dataset, pre-trained models, and source code to reproduce our work are available for public use.

### Supported Tasks and Leaderboards

machine translation

### Languages

English, Thai

## Dataset Structure

### Data Instances

```
{'subdataset': 'aqdf', 'translation': {'en': 'FAR LEFT: Indonesian National Police Chief Tito Karnavian, from left, Philippine National Police Chief Ronald Dela Rosa and Royal Malaysian Police Inspector General Khalid Abu Bakar link arms before the Trilateral Security Meeting in Pasay city, southeast of Manila, Philippines, in June 2017. [THE ASSOCIATED PRESS]', 'th': '(ซ้ายสุด) นายติโต คาร์นาเวียน ผู้บัญชาการตํารวจแห่งชาติอินโดนีเซีย (จากซ้าย) นายโรนัลด์ เดลา โรซา ผู้บัญชาการตํารวจแห่งชาติฟิลิปปินส์ และนายคาลิด อาบู บาการ์ ผู้บัญชาการตํารวจแห่งชาติมาเลเซีย ไขว้แขนกันก่อนเริ่มการประชุมความมั่นคงไตรภาคีในเมืองปาเซย์ ซึ่งอยู่ทางตะวันออกเฉียงใต้ของกรุงมะนิลา ประเทศฟิลิปปินส์ ในเดือนมิถุนายน พ.ศ. 2560 ดิแอสโซซิเอทเต็ด เพรส'}}
{'subdataset': 'thai_websites', 'translation': {'en': "*Applicants from certain countries may be required to pay a visa issuance fee after their application is approved. The Department of State's website has more information about visa issuance fees and can help you determine if an issuance fee applies to your nationality.", 'th': 'ประเภทวีซ่า รวมถึงค่าธรรมเนียม และข้อกําหนดในการสัมภาษณ์วีซ่า จะขึ้นอยู่กับชนิดของหนังสือเดินทาง และจุดประสงค์ในการเดินทางของท่าน โปรดดูตารางด้านล่างก่อนการสมัครวีซ่า'}}
{'subdataset': 'nus_sms', 'translation': {'en': 'Yup... Okay. Cya tmr... So long nvr write already... Dunno whether tmr can come up with 500 words', 'th': 'ใช่...ได้ แล้วเจอกันพรุ่งนี้... นานแล้วไม่เคยเขียน... ไม่รู้ว่าพรุ่งนี้จะทําได้ถึง500คําไหมเลย'}}
```

### Data Fields

- `subdataset`: subdataset from which the sentence pair comes from
- `translation`: 
  - `en`: English sentences (original source)
  - `th`: Thai sentences (originally target for translation)

### Data Splits

```
Split ratio (train, valid, test) : (0.8, 0.1, 0.1)
Number of paris (train, valid, test): 801,402 | 100,173 | 100,177

# Train
generated_reviews_yn: 218,637 ( 27.28% )
task_master_1: 185,671 ( 23.17% )
generated_reviews_translator: 105,561 ( 13.17% )
thai_websites: 93,518 ( 11.67% )
paracrawl: 46,802 (  5.84% )
nus_sms: 34,495 (  4.30% )
mozilla_common_voice: 2,451 (  4.05% )
wikipedia: 26,163 (  3.26% cd)
generated_reviews_crowd: 19,769 (  2.47% )
assorted_government: 19,712 (  2.46% )
aqdf: 10,466 (  1.31% )
msr_paraphrase: 8,157 (  1.02% ) 

# Valid
generated_reviews_yn: 30,786 ( 30.73% )
task_master_1: 18,531 ( 18.50% )
generated_reviews_translator: 13,884 ( 13.86% )
thai_websites: 13,381 ( 13.36% )
paracrawl: 6,618 (  6.61% )
nus_sms: 4,628 (  4.62% )
wikipedia: 3,796 (  3.79% )
assorted_government: 2,842 (  2.83% )
generated_reviews_crowd: 2,409 (  2.40% )
aqdf: 1,518 (  1.52% )
msr_paraphrase: 1,107 (  1.11% )
mozilla_common_voice: 673 (  0.67% )

# Test
generated_reviews_yn: 30,785 ( 30.73% )
task_master_1: 18,531 ( 18.50% )
generated_reviews_translator: 13,885 ( 13.86% )
thai_websites: 13,381 ( 13.36% )
paracrawl: 6,619 (  6.61% )
nus_sms: 4,627 (  4.62% )
wikipedia: 3,797 (  3.79% )
assorted_government: 2,844 (  2.83% )
generated_reviews_crowd: 2,409 (  2.40% )
aqdf: 1,519 (  1.52% )
msr_paraphrase: 1,107 (  1.11% )
mozilla_common_voice : 673 (  0.67% )
```

## Dataset Creation

### Curation Rationale

[AIResearch](https://airesearch.in.th/), funded by [VISTEC](https://www.vistec.ac.th/) and [depa](https://www.depa.or.th/th/home), curated this dataset as part of public NLP infrastructure. The center releases the dataset and baseline models under CC-BY-SA 4.0. 

### Source Data

#### Initial Data Collection and Normalization

The sentence pairs are curated from news, Wikipedia articles, SMS messages, task-based dialogs, webcrawled data and government documents. Sentence pairs are generated by:
- Professional translators
- Crowdsourced translators
- Google Translate API and human annotators (accepted or rejected)
- Sentence alignment with [multilingual universal sentence encoder](https://tfhub.dev/google/universal-sentence-encoder-multilingual/3); the author created [CRFCut](https://github.com/vistec-AI/crfcut) to segment Thai sentences to be abel to align with their English counterparts (sentence segmented by [NLTK](https://www.nltk.org/))

For detailed explanation of dataset curation, see https://arxiv.org/pdf/2007.03541.pdf

### Annotations

#### Sources and Annotation process

- generated_reviews_yn: generated by [CTRL](https://arxiv.org/abs/1909.05858), translated to Thai by Google Translate API and annotated as accepted or rejected by human annotators (we do not include rejected sentence pairs)
- task_master_1: [Taskmaster-1](https://research.google/tools/datasets/taskmaster-1/) translated by professional translators hired by [AIResearch](https://airesearch.in.th/)
- generated_reviews_translator: professional translators hired by [AIResearch](https://airesearch.in.th/)
- thai_websites: webcrawling from top 500 websites in Thailand; respective content creators; the authors only did sentence alignment
- paracrawl: replicating Paracrawl's methodology for webcrawling; respective content creators; the authors only did sentence alignment
- nus_sms: [The National University of Singapore SMS Corpus](https://scholarbank.nus.edu.sg/handle/10635/137343) translated by crowdsourced translators hired by [AIResearch](https://airesearch.in.th/)
- wikipedia: Thai Wikipedia; respective content creators; the authors only did sentence alignment
- assorted_government: Government document in PDFs from various government websites; respective content creators; the authors only did sentence alignment
- generated_reviews_crowd: generated by [CTRL](https://arxiv.org/abs/1909.05858), translated to Thai by crowdsourced translators hired by [AIResearch](https://airesearch.in.th/)
- aqdf: Bilingual news from [Asia Pacific Defense Forum](https://ipdefenseforum.com/); respective content creators; the authors only did sentence alignment
- msr_paraphrase: [Microsoft Research Paraphrase Corpus](https://www.microsoft.com/en-us/download/details.aspx?id=52398) translated to Thai by crowdsourced translators hired by [AIResearch](https://airesearch.in.th/)
- mozilla_common_voice: English version of [Mozilla Common Voice](https://commonvoice.mozilla.org/) translated to Thai by crowdsourced translators hired by [AIResearch](https://airesearch.in.th/)

### Personal and Sensitive Information

There are risks of personal information to be included in the webcrawled data namely `paracrawl` and `thai_websites`.

## Considerations for Using the Data

### Social Impact of Dataset

- The first and currently largest English-Thai machine translation dataset that is strictly cleaned and deduplicated, compare to other sources such as Paracrawl.

### Discussion of Biases

- Gender-based ending honorifics in Thai (ครับ/ค่ะ) might not be balanced due to more female translators than male for `task_master_1`

### Other Known Limitations

#### Segment Alignment between Languages With and Without Boundaries
Unlike English, there is no segment boundary marking in Thai. One segment in Thai may or may not cover all
the content of an English segment. Currently, we mitigate this problem by grouping Thai segments together before
computing the text similarity scores. We then choose the combination with the highest text similarity score. It can be
said that adequacy is the main issue in building this dataset.
Quality of Translation from Crawled Websites
Some websites use machine translation models such as Google Translate to localize their content. As a result, Thai
segments retrieved from web crawling might face issues of fluency since we do not use human annotators to perform
quality control.

#### Quality Control of Crowdsourced Translators
When we use a crowdsourcing platform to translate the content, we can not fully control the quality of the translation.
To combat this, we filter out low-quality segments by using a text similarity threshold, based on cosine similarity of
universal sentence encoder vectors. Moreover, some crowdsourced translators might copy and paste source segments to
a translation engine and take the results as answers to the platform. To further improve, we can apply techniques such
as described in [Zaidan, 2012] to control the quality and avoid fraud on the platform.

#### Domain Dependence of Machine Tranlsation Models
We test domain dependence of machine translation models by comparing models trained and tested on the same dataset,
using 80/10/10 train-validation-test split, and models trained on one dataset and tested on the other.

## Additional Information

### Dataset Curators

[AIResearch](https://airesearch.in.th/), funded by [VISTEC](https://www.vistec.ac.th/) and [depa](https://www.depa.or.th/th/home)

### Licensing Information

CC-BY-SA 4.0

### Citation Information

```
@article{lowphansirikul2020scb,
  title={scb-mt-en-th-2020: A Large English-Thai Parallel Corpus},
  author={Lowphansirikul, Lalita and Polpanumas, Charin and Rutherford, Attapol T and Nutanong, Sarana},
  journal={arXiv preprint arXiv:2007.03541},
  year={2020}
}
```
