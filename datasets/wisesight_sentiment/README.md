---
annotations_creators:
- expert-generated
language_creators:
- found
languages:
- th
licenses:
- cc0-1.0
multilinguality:
- monolingual
size_categories:
- 10K<n<100K
source_datasets:
- original
task_categories:
- text-classification
task_ids:
- sentiment-classification
---

# Dataset Card for wisesight_sentiment

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

- **Homepage:** https://github.com/PyThaiNLP/wisesight-sentiment
- **Repository:** https://github.com/PyThaiNLP/wisesight-sentiment
- **Paper:**
- **Leaderboard:** https://www.kaggle.com/c/wisesight-sentiment/
- **Point of Contact:** https://github.com/PyThaiNLP/

### Dataset Summary

Wisesight Sentiment Corpus: Social media messages in Thai language with sentiment label (positive, neutral, negative, question)
- Released to public domain under Creative Commons Zero v1.0 Universal license.
- Labels: {"pos": 0, "neu": 1, "neg": 2, "q": 3}
- Size: 26,737 messages
- Language: Central Thai
- Style: Informal and conversational. With some news headlines and advertisement.
- Time period: Around 2016 to early 2019. With small amount from other period.
- Domains: Mixed. Majority are consumer products and services (restaurants, cosmetics, drinks, car, hotels), with some current affairs.
- Privacy:
    - Only messages that made available to the public on the internet (websites, blogs, social network sites).
    - For Facebook, this means the public comments (everyone can see) that made on a public page.
    - Private/protected messages and messages in groups, chat, and inbox are not included.
- Alternations and modifications:
    - Keep in mind that this corpus does not statistically represent anything in the language register.
    - Large amount of messages are not in their original form. Personal data are removed or masked.
    - Duplicated, leading, and trailing whitespaces are removed. Other punctuations, symbols, and emojis are kept intact.
    (Mis)spellings are kept intact.
    - Messages longer than 2,000 characters are removed.
    - Long non-Thai messages are removed. Duplicated message (exact match) are removed.
- More characteristics of the data can be explore [this notebook](https://github.com/PyThaiNLP/wisesight-sentiment/blob/master/exploration.ipynb)

### Supported Tasks and Leaderboards

Sentiment analysis / [Kaggle Leaderboard](https://www.kaggle.com/c/wisesight-sentiment/)

### Languages

Thai

## Dataset Structure

### Data Instances

```
{'category': 'pos', 'texts': 'น่าสนนน'}
{'category': 'neu', 'texts': 'ครับ #phithanbkk'}
{'category': 'neg', 'texts': 'ซื้อแต่ผ้าอนามัยแบบเย็นมาค่ะ แบบว่าอีห่ากูนอนไม่ได้'}
{'category': 'q', 'texts': 'มีแอลกอฮอลมั้ยคะ'}
```

### Data Fields

- `texts`: texts 
- `category`: sentiment of texts ranging from `pos` (positive; 0), `neu` (neutral; 1), `neg` (negative; 2) and `q` (question; 3)

### Data Splits

|           | train | valid | test  |
|-----------|-------|-------|-------|
| # samples | 21628 | 2404  | 2671  |
| # neu     | 11795 | 1291  | 1453  |
| # neg     | 5491  | 637   | 683   |
| # pos     | 3866  | 434   | 478   |
| # q       | 476   | 42    | 57    |
| avg words | 27.21 | 27.18 | 27.12 |
| avg chars | 89.82 | 89.50 | 90.36 |

## Dataset Creation

### Curation Rationale

Originally, the dataset was conceived for the [In-class Kaggle Competition](https://www.kaggle.com/c/wisesight-sentiment/) at Chulalongkorn university by [Ekapol Chuangsuwanich](https://www.cp.eng.chula.ac.th/en/about/faculty/ekapolc/) (Faculty of Engineering, Chulalongkorn University). It has since become one of the  benchmarks for sentiment analysis in Thai.

### Source Data

#### Initial Data Collection and Normalization

- Style: Informal and conversational. With some news headlines and advertisement.
- Time period: Around 2016 to early 2019. With small amount from other period.
- Domains: Mixed. Majority are consumer products and services (restaurants, cosmetics, drinks, car, hotels), with some current affairs.
- Privacy:
  - Only messages that made available to the public on the internet (websites, blogs, social network sites).
  - For Facebook, this means the public comments (everyone can see) that made on a public page.
  - Private/protected messages and messages in groups, chat, and inbox are not included.
  - Usernames and non-public figure names are removed
  - Phone numbers are masked (e.g. 088-888-8888, 09-9999-9999, 0-2222-2222)
  - If you see any personal data still remain in the set, please tell us - so we can remove them.
- Alternations and modifications:
  - Keep in mind that this corpus does not statistically represent anything in the language register.
  - Large amount of messages are not in their original form. Personal data are removed or masked.
  - Duplicated, leading, and trailing whitespaces are removed. Other punctuations, symbols, and emojis are kept intact.
  - (Mis)spellings are kept intact.
  - Messages longer than 2,000 characters are removed.
  - Long non-Thai messages are removed. Duplicated message (exact match) are removed.


#### Who are the source language producers?

Social media users in Thailand

### Annotations

#### Annotation process

- Sentiment values are assigned by human annotators.
- A human annotator put his/her best effort to assign just one label, out of four, to a message.
- Agreement, enjoyment, and satisfaction are positive. Disagreement, sadness, and disappointment are negative.
- Showing interest in a topic or in a product is counted as positive. In this sense, a question about a particular product could has a positive sentiment value, if it shows the interest in the product.
- Saying that other product or service is better is counted as negative.
- General information or news title tend to be counted as neutral.

#### Who are the annotators?

Outsourced annotators hired by [Wisesight (Thailand) Co., Ltd.](https://github.com/wisesight/)

### Personal and Sensitive Information

-  The authors tried to exclude any known personally identifiable information from this data set.
- Usernames and non-public figure names are removed
- Phone numbers are masked (e.g. 088-888-8888, 09-9999-9999, 0-2222-2222)
- If you see any personal data still remain in the set, please tell us - so we can remove them.

## Considerations for Using the Data

### Social Impact of Dataset

- `wisesight_sentiment` is the first and one of the few open datasets for sentiment analysis of social media data in Thai
- There are risks of personal information that escape the anonymization process

### Discussion of Biases

- A message can be ambiguous. When possible, the judgement will be based solely on the text itself.
  - In some situation, like when the context is missing, the annotator may have to rely on his/her own world knowledge and just guess.
  - In some cases, the human annotator may have an access to the message's context, like an image. These additional information are not included as part of this corpus.

### Other Known Limitations

- The labels are imbalanced; over half of the texts are `neu` (neutral) whereas there are very few `q` (question).
- Misspellings in social media texts make word tokenization process for Thai difficult, thus impacting the model performance

## Additional Information

### Dataset Curators

Thanks [PyThaiNLP](https://github.com/PyThaiNLP/pythainlp) community, [Kitsuchart Pasupa](http://www.it.kmitl.ac.th/~kitsuchart/) (Faculty of Information Technology, King Mongkut's Institute of Technology Ladkrabang), and [Ekapol Chuangsuwanich](https://www.cp.eng.chula.ac.th/en/about/faculty/ekapolc/) (Faculty of Engineering, Chulalongkorn University) for advice. The original Kaggle competition, using the first version of this corpus, can be found at https://www.kaggle.com/c/wisesight-sentiment/ 

### Licensing Information

- If applicable, copyright of each message content belongs to the original poster.
- **Annotation data (labels) are released to public domain.**
- [Wisesight (Thailand) Co., Ltd.](https://github.com/wisesight/) helps facilitate the annotation, but does not necessarily agree upon the labels made by the human annotators. This annotation is for research purpose and does not reflect the professional work that Wisesight has been done for its customers.
- The human annotator does not necessarily agree or disagree with the message. Likewise, the label he/she made to the message does not necessarily reflect his/her personal view towards the message.

### Citation Information

Please cite the following if you make use of the dataset:

Arthit Suriyawongkul, Ekapol Chuangsuwanich, Pattarawat Chormai, and Charin Polpanumas. 2019. **PyThaiNLP/wisesight-sentiment: First release.** September.

BibTeX:
```
@software{bact_2019_3457447,
  author       = {Suriyawongkul, Arthit and
                  Chuangsuwanich, Ekapol and
                  Chormai, Pattarawat and
                  Polpanumas, Charin},
  title        = {PyThaiNLP/wisesight-sentiment: First release},
  month        = sep,
  year         = 2019,
  publisher    = {Zenodo},
  version      = {v1.0},
  doi          = {10.5281/zenodo.3457447},
  url          = {https://doi.org/10.5281/zenodo.3457447}
}
```
