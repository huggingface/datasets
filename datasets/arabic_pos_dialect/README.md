---
annotations_creators:
- expert-generated
language_creators:
- found
languages:
- ar
licenses:
- apache-2.0
multilinguality:
- multilingual
size_categories:
- n<1K
source_datasets:
- extended
task_categories:
- structure-prediction
task_ids:
- part-of-speech-tagging
paperswithcode_id: null
---

# Dataset Card for Arabic POS Dialect

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

- **Homepage:** https://alt.qcri.org/resources/da_resources/
- **Repository:** https://github.com/qcri/dialectal_arabic_resources
- **Paper:** http://www.lrec-conf.org/proceedings/lrec2018/pdf/562.pdf
- **Contacts:**
- Ahmed Abdelali < aabdelali @ hbku dot edu dot qa >
- Kareem Darwish < kdarwish @ hbku dot edu dot qa >
- Hamdy Mubarak < hmubarak @ hbku dot edu dot qa >

### Dataset Summary

This dataset was created to support part of speech (POS) tagging in dialects of Arabic. It contains sets of 350 manually segmented and POS tagged tweets for each of four dialects: Egyptian, Levantine, Gulf, and Maghrebi.

### Supported Tasks and Leaderboards

The dataset can be used to train a model for Arabic token segmentation and part of speech tagging in Arabic dialects. Success on this task is typically measured by achieving a high accuracy over a held out dataset. Darwish et al. (2018) train a CRF model across all four dialects and achieve an average accuracy of 89.3%. 

### Languages

The BCP-47 code is ar-Arab. The dataset consists of four dialects of Arabic, Egyptian (EGY), Levantine (LEV), Gulf (GLF), and Maghrebi (MGR), written in Arabic script. 

## Dataset Structure

### Data Instances

Below is a partial example from the Egyptian set:
```
- `Fold`: 4
- `SubFold`: A
- `Word`: [ليه, لما, تحب, حد, من, قلبك, ...]
- `Segmentation`: [ليه, لما, تحب, حد, من, قلب+ك, ...]
- `POS`: [PART, PART, V, NOUN, PREP, NOUN+PRON, ...]
```

### Data Fields

The `fold` and the `subfold` fields refer to the crossfold validation splits used by Darwish et al., which can be generated using this [script](https://github.com/qcri/dialectal_arabic_resources/blob/master/generate_splits.sh). 

- `fold`: An int32 indicating which fold the instance was in for the crossfold validation
- `subfold`: A string, either 'A' or 'B', indicating which subfold the instance was in for the crossfold validation
- `words`: A sequence of strings of the unsegmented token
- `segments`: A sequence of strings consisting of the segments of the word separated by '+' if there is more than one segment
- `pos_tags`: A sequence of strings of the part of speech tags of the segments separated by '+' if there is more than one segment

The POS tags consist of a set developed by [Darwish et al. (2017)](https://www.aclweb.org/anthology/W17-1316.pdf) for Modern Standard Arabic (MSA) plus an additional 6 tags (2 dialect-specific tags and 4 tweet-specific tags). 

|   Tag      | Purpose | Description                          |
| -----      | ------  | -----                                |
| ADV        | MSA     | Adverb                               |
| ADJ        | MSA     | Adjective                            |
| CONJ       | MSA     | Conjunction                          |
| DET        | MSA     | Determiner                           |
| NOUN       | MSA     | Noun                                 |
| NSUFF      | MSA     | Noun suffix                          |
| NUM        | MSA     | Number                               |
| PART       | MSA     | Particle                             |
| PREP       | MSA     | Preposition                          |
| PRON       | MSA     | Pronoun                              |
| PUNC       | MSA     | Preposition                          |
| V          | MSA     | Verb                                 | 
| ABBREV     | MSA     | Abbreviation                         |
| CASE       | MSA     | Alef of tanween fatha                |
| JUS        | MSA     | Jussification attached to verbs      |
| VSUFF      | MSA     | Verb Suffix                          | 
| FOREIGN    | MSA     | Non-Arabic as well as non-MSA words  |
| FUR_PART   | MSA     | Future particle "s" prefix and "swf" |
| PROG_PART  | Dialect | Progressive particle                 |
| NEG_PART   | Dialect | Negation particle                    |
| HASH       | Tweet   | Hashtag                              |
| EMOT       | Tweet   | Emoticon/Emoji                       |
| MENTION    | Tweet   | Mention                              |
| URL        | Tweet   | URL                                  |

### Data Splits

The dataset is split by dialect. 

|   Dialect             | Tweets |  Words  |
| -----                 | ------ |  -----  |
| Egyptian (EGY)        |  350   |  7481   |
| Levantine (LEV)       |  350   |  7221   |
| Gulf (GLF)            |  350   |  6767   |
| Maghrebi (MGR)        |  350   |  6400   |

## Dataset Creation

### Curation Rationale

This dataset was created to address the lack of computational resources available for dialects of Arabic. These dialects are typically used in speech, while written forms of the language are typically in Modern Standard Arabic. Social media, however, has provided a venue for people to use dialects in written format. 

### Source Data

This dataset builds off of the work of [Eldesouki et al. (2017)](https://arxiv.org/pdf/1708.05891.pdf) and [Samih et al. (2017b)](https://www.aclweb.org/anthology/K17-1043.pdf) who originally collected the tweets.

#### Initial Data Collection and Normalization

They started with 175 million Arabic tweets returned by the Twitter API using the query "lang:ar" in March 2014. They then filtered this set using author-identified locations and tokens that are unique to each dialect. Finally, they had native speakers of each dialect select 350 tweets that were heavily accented. 

#### Who are the source language producers?

The source language producers are people who posted on Twitter in Arabic using dialectal words from countries where the dialects of interest were spoken, as identified in [Mubarak and Darwish (2014)](https://www.aclweb.org/anthology/W14-3601.pdf). 

### Annotations

#### Annotation process

The segmentation guidelines are available at https://alt.qcri.org/resources1/da_resources/seg-guidelines.pdf. The tagging guidelines are not provided, but Darwish at al. note that there were multiple rounds of quality control and revision.

#### Who are the annotators?

The POS tags were annotated by native speakers of each dialect. Further information is not known.

### Personal and Sensitive Information

[More Information Needed]

## Considerations for Using the Data

### Social Impact of Dataset

Darwish et al find that the accuracy on the Maghrebi dataset suffered the most when the training set was from another dialect, and conversely training on Maghrebi yielded the worst results for all the other dialects. They suggest that Egyptian, Levantine, and Gulf may be more similar to each other and Maghrebi the most dissimilar to all of them. They also find that training on Modern Standard Arabic (MSA) and testing on dialects yielded significantly lower results compared to training on dialects and testing on MSA. This suggests that dialectal variation should be a significant consideration for future work in Arabic NLP applications, particularly when working with social media text. 

### Discussion of Biases

[More Information Needed]

### Other Known Limitations

[More Information Needed]

## Additional Information

### Dataset Curators

This dataset was curated by Kareem Darwish, Hamdy Mubarak, Mohamed Eldesouki and Ahmed Abdelali with the Qatar Computing Research Institute (QCRI), Younes Samih and Laura Kallmeyer with the University of Dusseldorf, Randah Alharbi and Walid Magdy with the University of Edinburgh, and Mohammed Attia with Google. No funding information was included.  

### Licensing Information

This dataset is licensed under the [Apache License, Version 2.0](http://www.apache.org/licenses/LICENSE-2.0).

### Citation Information

Kareem Darwish, Hamdy Mubarak, Ahmed Abdelali, Mohamed Eldesouki, Younes Samih, Randah Alharbi, Mohammed Attia, Walid Magdy and Laura Kallmeyer (2018) Multi-Dialect Arabic POS Tagging: A CRF Approach. Proceedings of the Eleventh International Conference on Language Resources and Evaluation (LREC 2018), May 7-12, 2018. Miyazaki, Japan.

```
@InProceedings{DARWISH18.562,
  author = {Kareem Darwish ,Hamdy Mubarak ,Ahmed Abdelali ,Mohamed Eldesouki ,Younes Samih ,Randah Alharbi ,Mohammed Attia ,Walid Magdy and Laura Kallmeyer},
  title = {Multi-Dialect Arabic POS Tagging: A CRF Approach},
  booktitle = {Proceedings of the Eleventh International Conference on Language Resources and Evaluation (LREC 2018)},
  year = {2018},
  month = {may},
  date = {7-12},
  location = {Miyazaki, Japan},
  editor = {Nicoletta Calzolari (Conference chair) and Khalid Choukri and Christopher Cieri and Thierry Declerck and Sara Goggi and Koiti Hasida and Hitoshi Isahara and Bente Maegaard and Joseph Mariani and Hélène Mazo and Asuncion Moreno and Jan Odijk and Stelios Piperidis and Takenobu Tokunaga},
  publisher = {European Language Resources Association (ELRA)},
  address = {Paris, France},
  isbn = {979-10-95546-00-9},
  language = {english}
  }
```

### Contributions

Thanks to [@mcmillanmajora](https://github.com/mcmillanmajora) for adding this dataset.