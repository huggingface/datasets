---
annotations_creators:
- expert-generated
language_creators:
- found
languages:
- yue
licenses:
- cc-by-4.0
multilinguality:
- monolingual
size_categories:
- 10K<n<100K
source_datasets:
- original
task_categories:
- conditional-text-generation
- sequence-modeling
task_ids:
- dialogue-modeling
- machine-translation
paperswithcode_id: hong-kong-cantonese-corpus
---

# Dataset Card for The Hong Kong Cantonese Corpus (HKCanCor)

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

- **Homepage:** http://compling.hss.ntu.edu.sg/hkcancor/
- **Repository:** https://github.com/fcbond/hkcancor
- **Paper:** [Luke and Wang, 2015](https://github.com/fcbond/hkcancor/blob/master/data/LukeWong_Hong-Kong-Cantonese-Corpus.pdf)
- **Leaderboard:** N/A
- **Point of Contact:** Luke Kang Kwong

### Dataset Summary
The Hong Kong Cantonese Corpus (HKCanCor) comprise transcribed conversations recorded 
between March 1997 and August 1998. It contains recordings of spontaneous speech (51 texts)
and radio programmes (42 texts), which involve 2 to 4 speakers, with 1 text of monologue.

In total, the corpus contains around 230,000 Chinese words. The text is word-segmented (i.e., tokenization is at word-level, and each token can span multiple Chinese characters). Tokens are annotated with part-of-speech (POS) tags and romanised Cantonese pronunciation. 

* Romanisation
  * Follows conventions set by the Linguistic Society of Hong Kong (LSHK).
* POS
  * The tagset used by this corpus extends the one in the Peita-Fujitsu-Renmin Ribao (PRF) corpus (Duan et al., 2000). Extensions were made to further capture Cantonese-specific phenomena. 
  * To facilitate everyday usage and for better comparability across languages and/or corpora, this dataset also includes the tags mapped to the [Universal Dependencies 2.0](https://universaldependencies.org/u/pos/index.html) format. This mapping references the [PyCantonese](https://github.com/jacksonllee/pycantonese) library.


### Supported Tasks and Leaderboards
[More Information Needed]

### Languages
Yue Chinese / Cantonese (Hong Kong).

## Dataset Structure
This corpus has 10801 utterances and approximately 230000 Chinese words. 
There is no predefined split. 

### Data Instances
Each instance contains a conversation id, speaker id within that conversation,
turn number, part-of-speech tag for each Chinese word in the PRF format and UD2.0 format, 
and the utterance written in Chinese characters as well as its LSHK format romanisation.


For example: 
```python
{
    'conversation_id': 'TNR016-DR070398-HAI6V'
    'pos_tags_prf': ['v', 'w'], 
    'pos_tags_ud': ['VERB', 'PUNCT'],
    'speaker': 'B', 
    'transcriptions': ['hai6', 'VQ1'], 
    'turn_number': 112, 
    'tokens': ['係', '。']
}
 ```

### Data Fields
- conversation_id: unique dialogue-level id
- pos_tags_prf: POS tag using the PRF format at token-level
- pos_tag_ud: POS tag using the UD2.0 format at token-level
- speaker: unique speaker id within dialogue
- transcriptions: token-level romanisation in the LSHK format
- turn_number: turn number in dialogue
- tokens: Chinese word or punctuation at token-level

### Data Splits
There are no specified splits in this dataset.

## Dataset Creation

### Curation Rationale

[More Information Needed]

### Source Data

#### Initial Data Collection and Normalization

[More Information Needed]

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
This work is licensed under a [Creative Commons Attribution 4.0 International License](https://creativecommons.org/licenses/by/4.0/deed.ast).


### Citation Information
This corpus was developed by [Luke and Wong, 2015](http://compling.hss.ntu.edu.sg/hkcancor/data/LukeWong_Hong-Kong-Cantonese-Corpus.pdf).
```
@article{luke2015hong,
  author={Luke, Kang-Kwong and Wong, May LY},
  title={The Hong Kong Cantonese corpus: design and uses},
  journal={Journal of Chinese Linguistics},
  year={2015},
  pages={309-330},
  month={12}
}
```
The POS tagset to Universal Dependency tagset mapping is provided by Jackson Lee, as a part of the [PyCantonese](https://github.com/jacksonllee/pycantonese) library. 
```
@misc{lee2020,
  author = {Lee, Jackson},
  title = {PyCantonese: Cantonese Linguistics and NLP in Python},
  year = {2020},
  publisher = {GitHub},
  journal = {GitHub repository},
  howpublished = {\url{https://github.com/jacksonllee/pycantonese}},
  commit = {1d58f44e1cb097faa69de6b617e1d28903b84b98}
}
```
### Contributions

Thanks to [@j-chim](https://github.com/j-chim) for adding this dataset.