---
annotations_creators:
- expert-generated
language_creators:
- crowdsourced
languages:
- en
- ta
licenses:
- unknown
multilinguality:
- multilingual
size_categories:
- 10K<n<100K
source_datasets:
- original
task_categories:
- text-classification
task_ids:
- sentiment-classification
paperswithcode_id: null
---

# Dataset Card for Tamilmixsentiment

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

- **Homepage:** [Tamilmixsentiment Homepage](https://dravidian-codemix.github.io/2020/index.html)
- **Repository:** [Tamilmixsentiment repository](https://dravidian-codemix.github.io/2020/datasets.html)
- **Paper:** [Corpus Creation for Sentiment Analysis in Code-Mixed Tamil-English Text](https://www.aclweb.org/anthology/2020.sltu-1.28/)
- **Leaderboard:** [Rank list](https://drive.google.com/file/d/1Mf8-No-63koGRwdF13RrO01NAFBlNmI0/view?usp=sharing)
- **Point of Contact:** [Bharathi Raja Chakravarthi](mailto:bharathiraja.akr@gmail.com)

### Dataset Summary
The first gold standard Tamil-English code-switched, sentiment-annotated corpus containing 15,744 comment posts from YouTube.  This makes the largest general domain sentiment dataset for this relatively low-resource language with code-mixing phenomenon. The comment/post may contain more than one sentence but the average sentence length of the corpora is 1. Each comment/post is annotated with sentiment polarity at the comment/post level. This dataset also has class imbalance problems depicting real-world scenarios.

### Supported Tasks and Leaderboards
To identify sentiment polarity of the code-mixed dataset of comments/posts in Tamil-English collected from social media.

### Languages
Tamil-English code-switched.  The dataset contains all the three types of code-mixed sentences - Inter-Sentential switch, Intra-Sentential switch and Tag switching. Most comments were written in Roman script with either Tamil grammar with English lexicon or English grammar with Tamil lexicon. Some comments were written in Tamil script with English expressions in between. 


## Dataset Structure

### Data Instances

An example from the Tamilmixsentiment train set looks as follows:
```
text										label
Trailer late ah parthavanga like podunga	Positive 
```

### Data Fields

- `text`: Tamil-English code-mixed comment.
- `label`: list of the possible sentiments "Positive", "Negative", "Mixed_feelings", "unknown_state", "not-Tamil"

### Data Splits

The entire dataset of 15,744 sentences was randomly shuffled and split into three parts as follows:

|                             | Tain   | Valid | Test |
| -----                       | ------ | ----- | ---- |
| Tamilmixsentiment           |  11335 |  1260 | 3149 |


## Dataset Creation

### Curation Rationale

Sentiment analysis has become important in social media research (Yang and Eisenstein, 2017). Until recently these applications were created for high-resourced languages which analysed monolingual utterances. But social media in multilingual communities contains more code-mixed text.  Code-mixing is common among speakers in a bilingual speech community.  As English is seen as the language of prestige and education, the influence of lexicon, connectives and phrases from English language is common in spoken Tamil. Tamil has little annotated data for code-mixed scenarios. An annotated corpus developed for monolingual data cannot deal with code-mixed usage and therefore it fails to yield good results due to mixture of languages at different levels of linguistic analysis. Therefore this dataset of code-mixed Tamil-English sentiment annotated corpus is created.

### Source Data

#### Initial Data Collection and Normalization

The data was scraped from Youtube. In total 184,573 sentences for Tamil from YouTube comments from the trailers of a movies released in 2019. Many of the them contained sentences
that were either entirely written in English or code-mixed Tamil-English or fully written in Tamil. So we filtered out a non-code-mixed corpus based on language identification
at comment level using the langdetect library. The comment is written fully in Tamil or English, we discarded that comment since monolingual resources are available for these languages. We also identified if the sentences were written in other languages such as Hindi, Malayalam, Urdu, Telugu, and Kannada. We preprocessed the comments by removing the emoticons and applying a sentence
length filter. We want to create a code-mixed corpus of reasonable size with sentences that have fairly defined sentiments which will be useful for future research. Thus our filter removed sentences with less than five words and more than 15 words after cleaning the data. In the end we got 15,744 Tanglish sentences.

#### Who are the source language producers?

Youtube users

### Annotations

#### Annotation process

Three steps complete the annotation setup. First, each sentence was annotated by two people. In the second step, the data were collected if both of them agreed. In the case of conflict, a third person annotated the sentence. In the third step, if all the three of them did not agree, then two more annotators annotated the sentences.

#### Who are the annotators?

Eleven volunteers were involved in the process. All of them were native speakers of Tamil with diversity in gender, educational level and medium of instruction in their school education.

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

```
@inproceedings{chakravarthi-etal-2020-corpus,
    title = "Corpus Creation for Sentiment Analysis in Code-Mixed {T}amil-{E}nglish Text",
    author = "Chakravarthi, Bharathi Raja  and
      Muralidaran, Vigneshwaran  and
      Priyadharshini, Ruba  and
      McCrae, John Philip",
    booktitle = "Proceedings of the 1st Joint Workshop on Spoken Language Technologies for Under-resourced languages (SLTU) and Collaboration and Computing for Under-Resourced Languages (CCURL)",
    month = may,
    year = "2020",
    address = "Marseille, France",
    publisher = "European Language Resources association",
    url = "https://www.aclweb.org/anthology/2020.sltu-1.28",
    pages = "202--210",
    abstract = "Understanding the sentiment of a comment from a video or an image is an essential task in many applications. Sentiment analysis of a text can be useful for various decision-making processes. One such application is to analyse the popular sentiments of videos on social media based on viewer comments. However, comments from social media do not follow strict rules of grammar, and they contain mixing of more than one language, often written in non-native scripts. Non-availability of annotated code-mixed data for a low-resourced language like Tamil also adds difficulty to this problem. To overcome this, we created a gold standard Tamil-English code-switched, sentiment-annotated corpus containing 15,744 comment posts from YouTube. In this paper, we describe the process of creating the corpus and assigning polarities. We present inter-annotator agreement and show the results of sentiment analysis trained on this corpus as a benchmark.",
    language = "English",
    ISBN = "979-10-95546-35-1",
}
```
### Contributions

Thanks to [@jamespaultg](https://github.com/jamespaultg) for adding this dataset.