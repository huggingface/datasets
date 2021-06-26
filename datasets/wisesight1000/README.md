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
- n<1K
source_datasets:
- extended|wisesight_sentiment
task_categories:
- structure-prediction
task_ids:
- structure-prediction-other-word-tokenization
paperswithcode_id: null
---

# Dataset Card for `wisesight1000`

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

- **Homepage:** https://github.com/PyThaiNLP/wisesight-sentiment
- **Repository:** https://github.com/PyThaiNLP/wisesight-sentiment/blob/master/word-tokenization/
- **Paper:**
- **Leaderboard:**
- **Point of Contact:** https://github.com/PyThaiNLP/

### Dataset Summary

`wisesight1000` contains Thai social media texts randomly drawn from the full `wisesight-sentiment`, tokenized by human annotators.
Out of the labels `neg` (negative), `neu` (neutral), `pos` (positive), `q` (question), 250 samples each. Some texts are removed because they look like spam. Because these samples are representative of real world content, we believe having these annotaed samples will allow the community to robustly evaluate tokenization algorithms.

### Supported Tasks and Leaderboards

word tokenization

### Languages

Thai

## Dataset Structure

### Data Instances

```
{'char': ['E', 'u', 'c', 'e', 'r', 'i', 'n', ' ', 'p', 'r', 'o', ' ', 'a', 'c', 'n', 'e', ' ', 'ค', '่', 'ะ', ' ', 'ใ', 'ช', '้', 'แ', 'ล', '้', 'ว', 'ส', 'ิ', 'ว', 'ข', 'ึ', '้', 'น', 'เ', 'พ', 'ิ', '่', 'ม', 'ท', 'ุ', 'ก', 'ว', 'ั', 'น', ' ', 'ม', 'า', 'ด', 'ู', 'ก', 'ั', 'น', 'น', 'ะ', 'ค', 'ะ', ' ', 'ว', '่', 'า', 'จ', 'ั', 'ด', 'ก', 'า', 'ร', 'ป', 'ั', 'ญ', 'ห', 'า', 'ส', 'ิ', 'ว', 'ใ', 'น', '7', 'ว', 'ั', 'น', 'ไ', 'ด', '้', 'ร', 'ึ', 'ม', 'ั', '่', 'ย', 'ย', 'ย', 'ย', 'ย', 'ย', 'ย', 'ย', ' ', 'ล', '่', 'า', 'ส', 'ุ', 'ด', 'ไ', 'ป', 'ล', '้', 'า', 'ง', 'ห', 'น', '้', '…', '\n'], 'char_type': [0, 8, 8, 8, 8, 8, 8, 5, 8, 8, 8, 5, 8, 8, 8, 8, 5, 1, 9, 10, 5, 11, 1, 9, 11, 1, 9, 1, 1, 10, 1, 1, 10, 9, 1, 11, 1, 10, 9, 1, 1, 10, 1, 1, 4, 1, 5, 1, 10, 1, 10, 1, 4, 1, 1, 10, 1, 10, 5, 1, 9, 10, 1, 4, 1, 1, 10, 1, 1, 4, 1, 3, 10, 1, 10, 1, 11, 1, 2, 1, 4, 1, 11, 1, 9, 1, 10, 1, 4, 9, 1, 1, 1, 1, 1, 1, 1, 1, 5, 1, 9, 10, 1, 10, 1, 11, 1, 1, 9, 10, 1, 3, 1, 9, 4, 4], 'is_beginning': [1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 1, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0]}
{'char': ['แ', 'พ', 'ง', 'เ', 'ว', '่', 'อ', 'ร', '์', ' ', 'เ', 'บ', 'ี', 'ย', 'ร', '์', 'ช', '้', 'า', 'ง', 'ต', '้', 'น', 'ท', 'ุ', 'น', 'ข', 'ว', 'ด', 'ล', 'ะ', 'ไ', 'ม', '่', 'ถ', 'ึ', 'ง', ' ', '5', '0', ' ', 'ข', 'า', 'ย', ' ', '1', '2', '0', ' ', '😰', '😰', '😰', '์', '\n'], 'char_type': [11, 1, 1, 11, 1, 9, 1, 1, 7, 5, 11, 1, 10, 1, 1, 7, 1, 9, 10, 1, 1, 9, 1, 1, 10, 1, 1, 1, 1, 1, 10, 11, 1, 9, 1, 10, 1, 5, 2, 2, 5, 1, 10, 1, 5, 2, 2, 2, 5, 4, 4, 4, 7, 4], 'is_beginning': [1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 1, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0]}
```

### Data Fields

- `char`: characters
- `char_type`: character types as adopted from []() by [deepcut](https://github.com/rkcosmos/deepcut)
- `is_beginning`: 1 if beginning of word else 0

### Data Splits

No explicit split is given.

## Dataset Creation

### Curation Rationale

The dataset was created from `wisesight-sentiment` to be a word tokenization benchmark that is closer to texts in the wild, since other Thai word tokenization datasets such as [BEST](https://aiforthai.in.th/corpus.php) are mostly texts from news articles, which do not have some real-world features like misspellings.

### Source Data

#### Initial Data Collection and Normalization

The data are sampled from `wisesight-sentiment` which has the following data collection and normalization:
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
[More Information Needed]

#### Who are the annotators?

The annotation was done by several people, including Nitchakarn Chantarapratin, [Pattarawat Chormai](https://github.com/heytitle), [Ponrawee Prasertsom](https://github.com/ponrawee), [Jitkapat Sawatphol](https://github.com/jitkapat), [Nozomi Yamada](https://github.com/nozomiyamada), and [Attapol Rutherford](https://attapol.github.io/).

### Personal and Sensitive Information

-  The authors tried to exclude any known personally identifiable information from this data set.
- Usernames and non-public figure names are removed
- Phone numbers are masked (e.g. 088-888-8888, 09-9999-9999, 0-2222-2222)
- If you see any personal data still remain in the set, please tell us - so we can remove them.

## Considerations for Using the Data

### Social Impact of Dataset

- word tokenization dataset from texts in the wild

### Discussion of Biases

- no guideline is given by the authors on word tokenization 

### Other Known Limitations

[More Information Needed]

## Additional Information

### Dataset Curators

Thanks [PyThaiNLP](https://github.com/PyThaiNLP/pythainlp) community, [Kitsuchart Pasupa](http://www.it.kmitl.ac.th/~kitsuchart/) (Faculty of Information Technology, King Mongkut's Institute of Technology Ladkrabang), and [Ekapol Chuangsuwanich](https://www.cp.eng.chula.ac.th/en/about/faculty/ekapolc/) (Faculty of Engineering, Chulalongkorn University) for advice. The original Kaggle competition, using the first version of this corpus, can be found at https://www.kaggle.com/c/wisesight-sentiment/ 

### Licensing Information

CC0

### Citation Information

Dataset:
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

Character type features:
```
@inproceedings{haruechaiyasak2009tlex,
  title={TLex: Thai lexeme analyser based on the conditional random fields},
  author={Haruechaiyasak, Choochart and Kongyoung, Sarawoot},
  booktitle={Proceedings of 8th International Symposium on Natural Language Processing},
  year={2009}
}
```

### Contributions

Thanks to [@cstorm125](https://github.com/cstorm125) for adding this dataset.