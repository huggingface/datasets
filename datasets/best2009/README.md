---
annotations_creators:
- expert-generated
language_creators:
- found
languages:
- th
licenses:
- cc-by-nc-sa-3.0
multilinguality:
- monolingual
size_categories:
- 100K<n<1M
source_datasets:
- original
task_categories:
- structure-prediction
task_ids:
- structure-prediction-other-word-tokenization
paperswithcode_id: null
---

# Dataset Card for `best2009`

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

- **Homepage:** https://aiforthai.in.th/
- **Repository:** https://aiforthai.in.th/corpus.php
- **Paper:**
- **Leaderboard:**
- **Point of Contact:** https://aiforthai.in.th/

### Dataset Summary

`best2009` is a Thai word-tokenization dataset from encyclopedia, novels, news and articles by [NECTEC](https://www.nectec.or.th/) (148,995/2,252 lines of train/test). It was created for [BEST 2010: Word Tokenization Competition](https://thailang.nectec.or.th/archive/indexa290.html?q=node/10). The test set answers are not provided publicly.

### Supported Tasks and Leaderboards

word tokenization

### Languages

Thai

## Dataset Structure

### Data Instances

```
{'char': ['?', 'ภ', 'ู', 'ม', 'ิ', 'ป', 'ั', 'ญ', 'ญ', 'า', 'ช', 'า', 'ว', 'บ', '้', 'า', 'น', '\n'], 'char_type': [4, 1, 10, 1, 10, 1, 4, 1, 1, 10, 1, 10, 1, 1, 9, 10, 1, 4], 'fname': 'encyclopedia_00031.txt', 'is_beginning': [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1]}
{'char': ['ภ', 'ู', 'ม', 'ิ', 'ป', 'ั', 'ญ', 'ญ', 'า', 'ช', 'า', 'ว', 'บ', '้', 'า', 'น', ' ', 'ห', 'ม', 'า', 'ย', 'ถ', 'ึ', 'ง', ' ', 'ค', 'ว', 'า', 'ม', 'ร', 'ู', '้', 'ข', 'อ', 'ง', 'ช', 'า', 'ว', 'บ', '้', 'า', 'น', ' ', 'ซ', 'ึ', '่', 'ง', 'เ', 'ร', 'ี', 'ย', 'น', 'ร', 'ู', '้', 'ม', 'า', 'จ', 'า', 'ก', 'พ', '่', 'อ', 'แ', 'ม', '่', ' ', 'ป', 'ู', '่', 'ย', '่', 'า', 'ต', 'า', 'ย', 'า', 'ย', ' ', 'ญ', 'า', 'ต', 'ิ', 'พ', 'ี', '่', 'น', '้', 'อ', 'ง', ' ', 'ห', 'ร', 'ื', 'อ', 'ผ', 'ู', '้', 'ม', 'ี', 'ค', 'ว', 'า', 'ม', 'ร', 'ู', '้', 'ใ', 'น', 'ห', 'ม', 'ู', '่', 'บ', '้', 'า', 'น', 'ใ', 'น', 'ท', '้', 'อ', 'ง', 'ถ', 'ิ', '่', 'น', 'ต', '่', 'า', 'ง', 'ๆ', '\n'], 'char_type': [1, 10, 1, 10, 1, 4, 1, 1, 10, 1, 10, 1, 1, 9, 10, 1, 5, 3, 1, 10, 1, 1, 10, 1, 5, 1, 1, 10, 1, 1, 10, 9, 1, 1, 1, 1, 10, 1, 1, 9, 10, 1, 5, 1, 10, 9, 1, 11, 1, 10, 1, 1, 1, 10, 9, 1, 10, 1, 10, 1, 1, 9, 1, 11, 1, 9, 5, 1, 10, 9, 1, 9, 10, 1, 10, 1, 10, 1, 5, 1, 10, 1, 10, 1, 10, 9, 1, 9, 1, 1, 5, 3, 1, 10, 1, 3, 10, 9, 1, 10, 1, 1, 10, 1, 1, 10, 9, 11, 1, 3, 1, 10, 9, 1, 9, 10, 1, 11, 1, 1, 9, 1, 1, 1, 10, 9, 1, 1, 9, 10, 1, 7, 4], 'fname': 'encyclopedia_00031.txt', 'is_beginning': [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1]}
```

### Data Fields

- `fname`: file name; also marks if article is articles, news, encyclopedia or novels
- `char`: characters
- `char_type`: character types as adopted from []() by [deepcut](https://github.com/rkcosmos/deepcut)
- `is_beginning`: is beginning of word

### Data Splits

|                         | train      | test    |
|-------------------------|------------|---------|
| # lines                 | 148,995    | 2,252   |
| avg words per line      | 39.05      | NA      |
| total words             | 5,818,521  | NA      |
| avg characters per line | 140.39     | 202.79  |
| total characters        | 20,918,132 | 456,684 |
| # lines articles        | 16,990     | NA      |
| # lines encyclopedia    | 50,631     | NA      |
| # lines novels          | 50,140     | NA      |
| # lines news            | 31,234     | NA      |

## Dataset Creation

### Curation Rationale

The dataset was created for [BEST 2010: Word Tokenization Competition](https://thailang.nectec.or.th/archive/indexa290.html?q=node/10) by [NECTEC](https://www.nectec.or.th/).

### Source Data

#### Initial Data Collection and Normalization

[More Information Needed]

#### Who are the source language producers?

Respective authors of the articles, news, encyclopedia and novels

### Annotations

#### Annotation process

Detailed annotation guidelines can be found in `BEST_Guideline_Release1.pdf` as part of the uncompressed files. Word tokenization standard used was [InterBEST2009](http://hltshare.fbk.eu/IWSLT2015/InterBEST2009Guidelines-2.pdf)

#### Who are the annotators?

[More Information Needed]

### Personal and Sensitive Information

All data are curated from public sources. No personal and sensitive information is expected to be included.

## Considerations for Using the Data

### Social Impact of Dataset

- word tokenization dataset from articles, news, encyclopedia and novels

### Discussion of Biases

- texts are relatively formal ones from articles, news, encyclopedia and novels.
- word tokenization standard used was [InterBEST2009](http://hltshare.fbk.eu/IWSLT2015/InterBEST2009Guidelines-2.pdf).

### Other Known Limitations

- some tags unrelated to word tokenization (`<NE>` and `<AB>`) are cleaned out.
- no word boundary provdied for the test set

## Additional Information

### Dataset Curators

[NECTEC](https://www.nectec.or.th/)

### Licensing Information

CC-BY-NC-SA 3.0

### Citation Information

Dataset:
```
@inproceedings{kosawat2009best,
  title={BEST 2009: Thai word segmentation software contest},
  author={Kosawat, Krit and Boriboon, Monthika and Chootrakool, Patcharika and Chotimongkol, Ananlada and Klaithin, Supon and Kongyoung, Sarawoot and Kriengket, Kanyanut and Phaholphinyo, Sitthaa and Purodakananda, Sumonmas and Thanakulwarapas, Tipraporn and others},
  booktitle={2009 Eighth International Symposium on Natural Language Processing},
  pages={83--88},
  year={2009},
  organization={IEEE}
}
@inproceedings{boriboon2009best,
  title={Best corpus development and analysis},
  author={Boriboon, Monthika and Kriengket, Kanyanut and Chootrakool, Patcharika and Phaholphinyo, Sitthaa and Purodakananda, Sumonmas and Thanakulwarapas, Tipraporn and Kosawat, Krit},
  booktitle={2009 International Conference on Asian Language Processing},
  pages={322--327},
  year={2009},
  organization={IEEE}
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