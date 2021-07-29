---
annotations_creators:
- crowdsourced
- other
language_creators:
- found
languages:
- en
- ja
licenses:
- cc-by-4.0
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

# Dataset Card for SNOW T15 and T23 (simplified Japanese corpus)

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

- **Homepage:** [SNOW T15](http://www.jnlp.org/SNOW/T15), [SNOW T23](http://www.jnlp.org/SNOW/T23)
- **Repository:** [N/A]
- **Paper:** ["Simplified Corpus with Core Vocabulary"](https://www.aclweb.org/anthology/L18-1185), ["やさしい⽇本語対訳コーパスの構築"](https://www.anlp.jp/proceedings/annual_meeting/2017/pdf_dir/B5-1.pdf), ["Crowdsourced Corpus of Sentence Simplification with Core Vocabulary"](https://www.aclweb.org/anthology/L18-1072)
- **Leaderboard:** [N/A]
- **Point of Contact:** Check the homepage.

### Dataset Summary

- **SNOW T15:**  
  The simplified corpus for the Japanese language. The corpus has 50,000 manually simplified and aligned sentences.  
  This corpus contains the original sentences, simplified sentences and English translation of the original sentences.  
  It can be used for automatic text simplification as well as translating simple Japanese into English and vice-versa.  
  The core vocabulary is restricted to 2,000 words where it is selected by accounting for several factors such as meaning preservation, variation, simplicity and the UniDic word segmentation criterion.  
  For details, refer to the explanation page of Japanese simplification (http://www.jnlp.org/research/Japanese_simplification).  
  The original texts are from "small_parallel_enja: 50k En/Ja Parallel Corpus for Testing SMT Methods", which is a bilingual corpus for machine translation.

- **SNOW T23:**  
  An expansion corpus of 35,000 sentences rewritten in easy Japanese (simple Japanese vocabulary) based on SNOW T15.  
  The original texts are from "Tanaka Corpus" (http://www.edrdg.org/wiki/index.php/Tanaka_Corpus).

### Supported Tasks and Leaderboards

It can be used for automatic text simplification in Japanese as well as translating simple Japanese into English and vice-versa.

### Languages

Japanese, simplified Japanese, and English.

## Dataset Structure

### Data Instances

SNOW T15 is xlsx file with ID, "#日本語(原文)" (Japanese (original)), "#やさしい日本語" (simplified Japanese), "#英語(原文)" (English (original)).  
SNOW T23 is xlsx file with ID, "#日本語(原文)" (Japanese (original)), "#やさしい日本語" (simplified Japanese), "#英語(原文)" (English (original)), and "#固有名詞" (proper noun).

### Data Fields

- `ID`: sentence ID.
- `original_ja`: original Japanese sentence.
- `simplified_ja`: simplified Japanese sentence.
- `original_en`: original English sentence.
- `proper_noun`: (included only in SNOW T23) Proper nowus that the workers has extracted as proper nouns. The authors instructed workers not to rewrite proper nouns, leaving the determination of proper nouns to the workers.

### Data Splits

The data is not split.

## Dataset Creation

### Curation Rationale

A dataset on the study of automatic conversion to simplified Japanese (Japanese simplification).

### Source Data

#### Initial Data Collection and Normalization

- **SNOW T15:**  
  The original texts are from "small_parallel_enja: 50k En/Ja Parallel Corpus for Testing SMT Methods", which is a bilingual corpus for machine translation.

- **SNOW T23:**  
  The original texts are from "Tanaka Corpus" (http://www.edrdg.org/wiki/index.php/Tanaka_Corpus).

#### Who are the source language producers?

[N/A]

### Annotations

#### Annotation process

- **SNOW T15:**  
  Five students in the laboratory rewrote the original Japanese sentences to simplified Japanese all by hand.  
  The core vocabulary is restricted to 2,000 words where it is selected by accounting for several factors such as meaning preservation, variation, simplicity and the UniDic word segmentation criterion.

- **SNOW T23:**  
  Seven people, gathered through crowdsourcing, rewrote all the sentences manually.  
  Each worker rewrote 5,000 sentences, of which 100 sentences were rewritten to be common among the workers.  
  The average length of the sentences was kept as close to the same as possible so that the amount of work was not varied among the workers.

#### Who are the annotators?

Five students for SNOW T15, seven crowd workers for SNOW T23.

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

The datasets are part of SNOW, Japanese language resources/tools created by Natural Language Processing Laboratory, Nagaoka University of Technology, Japan.

### Licensing Information

CC BY 4.0

### Citation Information

```
@inproceedings{maruyama-yamamoto-2018-simplified,
    title = "Simplified Corpus with Core Vocabulary",
    author = "Maruyama, Takumi  and
      Yamamoto, Kazuhide",
    booktitle = "Proceedings of the Eleventh International Conference on Language Resources and Evaluation ({LREC} 2018)",
    month = may,
    year = "2018",
    address = "Miyazaki, Japan",
    publisher = "European Language Resources Association (ELRA)",
    url = "https://www.aclweb.org/anthology/L18-1185",
}

@inproceedings{yamamoto-2017-simplified-japanese,
    title = "やさしい⽇本語対訳コーパスの構築",
    author = "⼭本 和英  and
      丸⼭ 拓海  and
      ⾓張 ⻯晴  and
      稲岡 夢⼈  and
      ⼩川 耀⼀朗  and
      勝⽥ 哲弘  and
      髙橋 寛治",
    booktitle = "言語処理学会第23回年次大会",
    month = 3月,
    year = "2017",
    address = "茨城, 日本",
    publisher = "言語処理学会",
    url = "https://www.anlp.jp/proceedings/annual_meeting/2017/pdf_dir/B5-1.pdf",
}

@inproceedings{katsuta-yamamoto-2018-crowdsourced,
    title = "Crowdsourced Corpus of Sentence Simplification with Core Vocabulary",
    author = "Katsuta, Akihiro  and
      Yamamoto, Kazuhide",
    booktitle = "Proceedings of the Eleventh International Conference on Language Resources and Evaluation ({LREC} 2018)",
    month = may,
    year = "2018",
    address = "Miyazaki, Japan",
    publisher = "European Language Resources Association (ELRA)",
    url = "https://www.aclweb.org/anthology/L18-1072",
}
```

### Contributions

Thanks to [@forest1988](https://github.com/forest1988), [@lhoestq](https://github.com/lhoestq) for adding this dataset.