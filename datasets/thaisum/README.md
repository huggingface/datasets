---
annotations_creators:
- no-annotation
language_creators:
- found
languages:
- th
licenses:
- mit
multilinguality:
- monolingual
size_categories:
- 100K<n<1M
source_datasets:
- original
task_categories:
- conditional-text-generation
- sequence-modeling
task_ids:
- language-modeling
- summarization
---

# Dataset Card for `thaisum`

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

- **Homepage:** https://github.com/nakhunchumpolsathien/ThaiSum
- **Repository:** https://github.com/nakhunchumpolsathien/ThaiSum
- **Paper:**
- **Leaderboard:**
- **Point of Contact:** https://github.com/nakhunchumpolsathien

### Dataset Summary

ThaiSum is a large-scale corpus for Thai text summarization obtained from several online news websites namely Thairath, ThaiPBS, Prachathai, and The Standard. This dataset consists of over 350,000 article and summary pairs written by journalists.

### Supported Tasks and Leaderboards

summarization, language modeling

### Languages

Thai

## Dataset Structure

### Data Instances

```
{'body': 'กีเก ซานเชซ ฟลอเรส\xa0 กุนซือเลือดกระทิงของทีมวัตฟอร์ด\xa0 เมินประเด็นจุดโทษปัญหาในเกมพรีเมียร์ลีก อังกฤษ นัดที่แตนอาละวาดเปิดบ้านพ่าย คริสตัล พาเลซ 0-1ชี้ทีมของเขาเล่นไม่ดีพอเอง,สำนักข่าวต่างประเทศรายงานวันที่ 27 ก.ย. ว่า กีเก ซานเชซ ฟลอเรส\xa0 ผู้จัดการทีมชาวสเปน ของ แตนอาละวาด วัตฟอร์ด\xa0 ยอมรับทีมของเขาเล่นได้ไม่ดีพอเอง ในเกมพรีเมียร์ลีก อังกฤษ นัดเปิดบ้านพ่าย อินทรีผงาด คริสตัล พาเลซ 0-1 เมื่อคืนวันอาทิตย์ที่ผ่านมา,เกมนี้จุดเปลี่ยนมาอยู่ที่การได้จุดโทษในช่วงครึ่งหลังของ คริสตัล พาเลซ ซึ่งไม่ค่อยชัดเจนเท่าไหร่ว่า อัลลัน นียอม นั้นไปทำฟาล์วใส่ วิลฟรีด ซาฮา ในเขตโทษหรือไม่ แต่ผู้ตัดสินก็ชี้เป็นจุดโทษ ซึ่ง โยอัน กาบาย สังหารไม่พลาด และเป็นประตูชัยช่วยให้ คริสตัล พาเลซ เอาชนะ วัตฟอร์ด ไป 1-0 และเป็นการพ่ายแพ้ในบ้านนัดแรกของวัตฟอร์ดในฤดูกาลนี้อีกด้วย,ฟลอเรส กล่าวว่า มันเป็นเรื่องยากในการหยุดเกมรุกของคริสตัล พาเลซ ซึ่งมันอึดอัดจริงๆสำหรับเรา เราเล่นกันได้ไม่ดีนักในตอนที่ได้ครองบอล เราต้องเล่นทางริมเส้นให้มากกว่านี้ เราไม่สามารถหยุดเกมสวนกลับของพวกเขาได้ และแนวรับของเราก็ยืนไม่เป็นระเบียบสักเท่าไหร่ในช่วงครึ่งแรก ส่วนเรื่องจุดโทษการตัดสินใจขั้นสุดท้ายมันอยู่ที่ผู้ตัดสิน ซึ่งมันเป็นการตัดสินใจที่สำคัญ ผมเองก็ไม่รู้ว่าเขาตัดสินถูกหรือเปล่า บางทีมันอาจเป็นจุดที่ตัดสินเกมนี้เลย แต่เราไม่ได้แพ้เกมนี้เพราะจุดโทษ เราแพ้ในวันนี้เพราะเราเล่นไม่ดีและคริสตัล พาเลซ เล่นดีกว่าเรา เราไม่ได้มีฟอร์มการเล่นที่ดีในเกมนี้เลย', 'summary': 'กีเก ซานเชซ ฟลอเรส  กุนซือเลือดกระทิงของทีมวัตฟอร์ด  เมินประเด็นจุดโทษปัญหาในเกมพรีเมียร์ลีก อังกฤษ นัดที่แตนอาละวาดเปิดบ้านพ่าย คริสตัล พาเลซ 0-1ชี้ทีมของเขาเล่นไม่ดีพอเอง', 'tags': 'พรีเมียร์ลีก,วัตฟอร์ด,คริสตัล พาเลซ,กีเก ซานเชซ ฟลอเรส,ข่าวกีฬา,ข่าว,ไทยรัฐออนไลน์', 'title': 'ฟลอเรส รับ วัตฟอร์ดห่วยเองเกมพ่ายพาเลซคาบ้าน', 'type': '', 'url': 'https://www.thairath.co.th/content/528322'}
```

### Data Fields

- `title`: title of article
- `body`: body of article
- `summary`: summary of article
- `type`: type of article, if any
- `tags`: tags of article, separated by `,`
- `url`: URL of article

### Data Splits

train/valid/test: 358868 / 11000 / 11000

## Dataset Creation

### Curation Rationale

Sequence-to-sequence (Seq2Seq) models have shown great achievement in text summarization. However, Seq2Seq model often requires large-scale training data to achieve effective results. Although many impressive advancements in text summarization field have been made, most of summarization studies focus on resource-rich languages. The progress of Thai text summarization is still far behind. The dearth of large-scale dataset keeps Thai text summarization in its infancy. As far as our knowledge goes, there is not a large-scale dataset for Thai text summarization available anywhere. Thus, we present ThaiSum, a large-scale corpus for Thai text summarization obtained from several online news websites namely Thairath, ThaiPBS, Prachathai, and The Standard. 

### Source Data

#### Initial Data Collection and Normalization

We used a python library named Scrapy to crawl articles from several news websites namely Thairath, Prachatai, ThaiPBS and, The Standard. We first collected news URLs provided in their sitemaps. During web-crawling, we used HTML markup and metadata available in HTML pages to identify article text, summary, headline, tags and label. Collected articles were published online from 2014 to August 2020.  <br> <br>
We further performed data cleansing process to minimize noisy data. We filtered out articles that their article text or summary is missing. Articles that contains article text with less than 150 words or summary with less than 15 words were removed. We also discarded articles that contain at least one of these following tags: ‘ดวง’ (horoscope), ‘นิยาย’ (novel), ‘อินสตราแกรมดารา’ (celebrity Instagram), ‘คลิปสุดฮา’(funny video) and ‘สรุปข่าว’ (highlight news). Some summaries were completely irrelevant to their original article texts. To eliminate those irrelevant summaries, we calculated abstractedness score between summary and its article text. Abstractedness score is written formally as: <br>
<center><a href="https://www.codecogs.com/eqnedit.php?latex=\begin{equation}&space;\frac{|S-A|}{r}&space;\times&space;100&space;\end{equation}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?\begin{equation}&space;\frac{|S-A|}{r}&space;\times&space;100&space;\end{equation}" title="\begin{equation} \frac{|S-A|}{r} \times 100 \end{equation}" /></a></center><br>
<br>Where 𝑆 denotes set of article tokens. 𝐴 denotes set of summary tokens. 𝑟 denotes a total number of summary tokens. We omitted articles that have abstractedness score at 1-grams higher than 60%. 
<br><br>

It is important to point out that we used [PyThaiNLP](https://github.com/PyThaiNLP/pythainlp), version 2.2.4, tokenizing engine = newmm, to process Thai texts in this study. It is challenging to tokenize running Thai text into words or sentences because there are not clear word/sentence delimiters in Thai language. Therefore, using different tokenization engines may result in different segment of words/sentences. 

After data-cleansing process, ThaiSum dataset contains over 358,000 articles. The size of this dataset is comparable to a well-known English document summarization dataset, CNN/Dily mail dataset. Moreover, we analyse the characteristics of this dataset by measuring the abstractedness level, compassion rate, and content diversity.  For more details, see [thaisum_exploration.ipynb](https://github.com/nakhunchumpolsathien/ThaiSum/blob/master/thaisum_exploration.ipynb).

#### Dataset Statistics

ThaiSum dataset consists of 358,868 articles. Average lengths of article texts and summaries are approximately 530 and 37 words respectively. As mentioned earlier, we also collected headlines, tags and labels provided in each article. Tags are similar to keywords of the article. An article normally contains several tags but a few labels. Tags can be name of places or persons that article is about while labels indicate news category (politic, entertainment, etc.). Ultimatly, ThaiSum contains 538,059 unique tags and 59 unique labels. Note that not every article contains tags or labels. 

|Dataset Size| 358,868 |  articles |
|:---|---:|---:|
|Avg. Article Length|   529.5 | words| 
|Avg. Summary Length  | 37.3  | words| 
|Avg. Headline Length |   12.6  | words| 
|Unique Vocabulary Size | 407,355 | words| 
|Occurring > 10 times | 81,761  | words| 
|Unique News Tag Size |   538,059 | tags| 
|Unique News Label Size | 59  | labels| 

#### Who are the source language producers?

Journalists of respective articles

### Annotations

#### Annotation process

`summary`, `type` and `tags` are created by journalists who wrote the articles and/or their publishers. 

#### Who are the annotators?

`summary`, `type` and `tags` are created by journalists who wrote the articles and/or their publishers.

### Personal and Sensitive Information

All data are public news articles. No personal and sensitive information is expected to be included.

## Considerations for Using the Data

### Social Impact of Dataset

- News summarization in Thai
- Language modeling for Thai news

### Discussion of Biases


- [ThaiPBS](https://www.thaipbs.or.th/home) [receives funding from Thai government](https://www.bangkokbiznews.com/blog/detail/648740).
- [Thairath](https://www.thairath.co.th/) is known as [the most popular newspaper in Thailand](https://mgronline.com/onlinesection/detail/9620000058532); no clear political leaning.
- [The Standard](https://thestandard.co/) is a left-leaning online magazine.
- [Prachathai](https://prachatai.com/)  is a left-leaning, human-right-focused news site.

### Other Known Limitations

[More Information Needed]

## Additional Information

### Dataset Curators

[@nakhunchumpolsathien](https://github.com/nakhunchumpolsathien/)
[@caramelWaffle](https://github.com/caramelWaffle)

### Licensing Information

MIT License

### Citation Information

```
@mastersthesis{chumpolsathien_2020, 
    title={Using Knowledge Distillation from Keyword Extraction to Improve the Informativeness of Neural Cross-lingual Summarization},
    author={Chumpolsathien, Nakhun}, 
    year={2020}, 
    school={Beijing Institute of Technology}
```
