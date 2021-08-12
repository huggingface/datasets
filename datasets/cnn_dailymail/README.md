---
annotations_creators:
- no-annotation
language_creators:
- found
languages:
- en
licenses:
- apache-2.0
multilinguality:
- monolingual
size_categories:
- 100K<n<1M
source_datasets:
- original
task_categories:
- conditional-text-generation
task_ids:
- summarization
paperswithcode_id: cnn-daily-mail-1
pretty_name: CNN / Daily Mail
---
# Dataset Card for CNN Dailymail Dataset

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

- **Homepage:**
- **Repository:** [CNN / DailyMail Dataset repository](https://github.com/abisee/cnn-dailymail)
- **Paper:** [Abstractive Text Summarization Using Sequence-to-Sequence RNNs and Beyond](https://papers.nips.cc/paper/5945-teaching-machines-to-read-and-comprehend.pdf), [Get To The Point: Summarization with Pointer-Generator Networks](https://www.aclweb.org/anthology/K16-1028.pdf)
- **Leaderboard:** [Papers with Code leaderboard for CNN / Dailymail Dataset](https://paperswithcode.com/sota/document-summarization-on-cnn-daily-mail)
- **Point of Contact:** [Abigail See](mailto:abisee@stanford.edu)

### Dataset Summary

The CNN / DailyMail Dataset is an English-language dataset containing just over 300k unique news articles as written by journalists at CNN and the Daily Mail. The current version supports both extractive and abstractive summarization, though the original version was created for machine reading and comprehension and abstractive question answering. 

### Supported Tasks and Leaderboards

- 'summarization': [Versions 2.0.0 and 3.0.0 of the CNN / DailyMail Dataset](https://www.aclweb.org/anthology/K16-1028.pdf) can be used to train a model for abstractive and extractive summarization ([Version 1.0.0](https://papers.nips.cc/paper/5945-teaching-machines-to-read-and-comprehend.pdf) was developed for machine reading and comprehension and abstractive question answering). The model performance is measured by how high the output summary's [ROUGE](https://huggingface.co/metrics/rouge) score for a given article is when compared to the highlight as written by the original article author. [Zhong et al (2020)](https://www.aclweb.org/anthology/2020.acl-main.552.pdf) report a ROUGE-1 score of 44.41 when testing a model trained for extractive summarization. See the [Papers With Code leaderboard](https://paperswithcode.com/sota/document-summarization-on-cnn-daily-mail) for more models. 

### Languages

The BCP-47 code for English as generally spoken in the United States is en-US and the BCP-47 code for English as generally spoken in the United Kingdom is en-GB. It is unknown if other varieties of English are represented in the data.

## Dataset Structure

### Data Instances

For each instance, there is a string for the article, a string for the highlights, and a string for the id. See the [CNN / Daily Mail dataset viewer](https://huggingface.co/datasets/viewer/?dataset=cnn_dailymail&config=3.0.0) to explore more examples.

```
{'id': '0054d6d30dbcad772e20b22771153a2a9cbeaf62',
 'article': '(CNN) -- An American woman died aboard a cruise ship that docked at Rio de Janeiro on Tuesday, the same ship on which 86 passengers previously fell ill, according to the state-run Brazilian news agency, Agencia Brasil. The American tourist died aboard the MS Veendam, owned by cruise operator Holland America. Federal Police told Agencia Brasil that forensic doctors were investigating her death. The ship's doctors told police that the woman was elderly and suffered from diabetes and hypertension, according the agency. The other passengers came down with diarrhea prior to her death during an earlier part of the trip, the ship's doctors said. The Veendam left New York 36 days ago for a South America tour.'
 'highlights': 'The elderly woman suffered from diabetes and hypertension, ship's doctors say .\nPreviously, 86 passengers had fallen ill on the ship, Agencia Brasil says .'}
```

The average token count for the articles and the highlights are provided below:

| Feature    | Mean Token Count |
| ---------- | ---------------- |
| Article    | 781              |
| Highlights | 56               |

### Data Fields

- `id`: a string containing the heximal formated SHA1 hash of the url where the story was retrieved from
- `article`: a string containing the body of the news article 
- `highlights`: a string containing the highlight of the article as written by the article author

### Data Splits

The CNN/DailyMail dataset has 3 splits: _train_, _validation_, and _test_. Below are the statistics for Version 3.0.0 of the dataset.

| Dataset Split | Number of Instances in Split                |
| ------------- | ------------------------------------------- |
| Train         | 287,113                                     |
| Validation    | 13,368                                      |
| Test          | 11,490                                      |

## Dataset Creation

### Curation Rationale

Version 1.0.0 aimed to support supervised neural methodologies for machine reading and question answering with a large amount of real natural language training data and released about 313k unique articles and nearly 1M Cloze style questions to go with the articles. Versions 2.0.0 and 3.0.0 changed the structure of the dataset to support summarization rather than question answering. Version 3.0.0 provided a non-anonymized version of the data, whereas both the previous versions were preprocessed to replace named entities with unique identifier labels. 

### Source Data

#### Initial Data Collection and Normalization

The data consists of news articles and highlight sentences. In the question answering setting of the data, the articles are used as the context and entities are hidden one at a time in the highlight sentences, producing Cloze style questions where the goal of the model is to correctly guess which entity in the context has been hidden in the highlight. In the summarization setting, the highlight sentences are concatenated to form a summary of the article. The CNN articles were written between April 2007 and April 2015. The Daily Mail articles were written between June 2010 and April 2015. 

The code for the original data collection is available at <https://github.com/deepmind/rc-data>. The articles were downloaded using archives of <www.cnn.com> and <www.dailymail.co.uk> on the Wayback Machine. Articles were not included in the Version 1.0.0 collection if they exceeded 2000 tokens. Due to accessibility issues with the Wayback Machine, Kyunghyun Cho has made the datasets available at <https://cs.nyu.edu/~kcho/DMQA/>. An updated version of the code that does not anonymize the data is available at <https://github.com/abisee/cnn-dailymail>. 

Hermann et al provided their own tokenization script. The script provided by See uses the PTBTokenizer. It also lowercases the text and adds periods to lines missing them.

#### Who are the source language producers?

The text was written by journalists at CNN and the Daily Mail. 

### Annotations

The dataset does not contain any additional annotations.

#### Annotation process

[N/A]

#### Who are the annotators?

[N/A]

### Personal and Sensitive Information

Version 3.0 is not anonymized, so individuals' names can be found in the dataset. Information about the original author is not included in the dataset.

## Considerations for Using the Data

### Social Impact of Dataset

The purpose of this dataset is to help develop models that can summarize long paragraphs of text in one or two sentences.

This task is useful for efficiently presenting information given a large quantity of text. It should be made clear that any summarizations produced by models trained on this dataset are reflective of the language used in the articles, but are in fact automatically generated.

### Discussion of Biases

[Bordia and Bowman (2019)](https://www.aclweb.org/anthology/N19-3002.pdf) explore measuring gender bias and debiasing techniques in the CNN / Dailymail dataset, the Penn Treebank, and WikiText-2. They find the CNN / Dailymail dataset to have a slightly lower gender bias based on their metric compared to the other datasets, but still show evidence of gender bias when looking at words such as 'fragile'.

Because the articles were written by and for people in the US and the UK, they will likely present specifically US and UK perspectives and feature events that are considered relevant to those populations during the time that the articles were published. 

### Other Known Limitations

News articles have been shown to conform to writing conventions in which important information is primarily presented in the first third of the article [(Kryściński et al, 2019)](https://www.aclweb.org/anthology/D19-1051.pdf). [Chen et al (2016)](https://www.aclweb.org/anthology/P16-1223.pdf) conducted a manual study of 100 random instances of the first version of the dataset and found 25% of the samples to be difficult even for humans to answer correctly due to ambiguity and coreference errors. 

It should also be noted that machine-generated summarizations, even when extractive, may differ in truth values when compared to the original articles. 

## Additional Information

### Dataset Curators

The data was originally collected by Karl Moritz Hermann, Tomáš Kočiský, Edward Grefenstette, Lasse Espeholt, Will Kay, Mustafa Suleyman, and Phil Blunsom of Google DeepMind. Tomáš Kočiský and Phil Blunsom are also affiliated with the University of Oxford. They released scripts to collect and process the data into the question answering format. 

Ramesh Nallapati, Bowen Zhou, Cicero dos Santos, and Bing Xiang of IMB Watson and Çağlar Gu̇lçehre of Université de Montréal modified Hermann et al's collection scripts to restore the data to a summary format. They also produced both anonymized and non-anonymized versions.

The code for the non-anonymized version is made publicly available by Abigail See of Stanford University, Peter J. Liu of Google Brain and Christopher D. Manning of Stanford University at <https://github.com/abisee/cnn-dailymail>. The work at Stanford University was supported by the DARPA DEFT ProgramAFRL contract no. FA8750-13-2-0040.

### Licensing Information

The CNN / Daily Mail dataset version 1.0.0 is released under the [Apache-2.0 License](http://www.apache.org/licenses/LICENSE-2.0). 

### Citation Information

```
@inproceedings{see-etal-2017-get,
    title = "Get To The Point: Summarization with Pointer-Generator Networks",
    author = "See, Abigail  and
      Liu, Peter J.  and
      Manning, Christopher D.",
    booktitle = "Proceedings of the 55th Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)",
    month = jul,
    year = "2017",
    address = "Vancouver, Canada",
    publisher = "Association for Computational Linguistics",
    url = "https://www.aclweb.org/anthology/P17-1099",
    doi = "10.18653/v1/P17-1099",
    pages = "1073--1083",
    abstract = "Neural sequence-to-sequence models have provided a viable new approach for abstractive text summarization (meaning they are not restricted to simply selecting and rearranging passages from the original text). However, these models have two shortcomings: they are liable to reproduce factual details inaccurately, and they tend to repeat themselves. In this work we propose a novel architecture that augments the standard sequence-to-sequence attentional model in two orthogonal ways. First, we use a hybrid pointer-generator network that can copy words from the source text via pointing, which aids accurate reproduction of information, while retaining the ability to produce novel words through the generator. Second, we use coverage to keep track of what has been summarized, which discourages repetition. We apply our model to the CNN / Daily Mail summarization task, outperforming the current abstractive state-of-the-art by at least 2 ROUGE points.",
}
```

```
@inproceedings{DBLP:conf/nips/HermannKGEKSB15,
  author={Karl Moritz Hermann and Tomás Kociský and Edward Grefenstette and Lasse Espeholt and Will Kay and Mustafa Suleyman and Phil Blunsom},
  title={Teaching Machines to Read and Comprehend},
  year={2015},
  cdate={1420070400000},
  pages={1693-1701},
  url={http://papers.nips.cc/paper/5945-teaching-machines-to-read-and-comprehend},
  booktitle={NIPS},
  crossref={conf/nips/2015}
}

```

### Contributions

Thanks to [@thomwolf](https://github.com/thomwolf), [@lewtun](https://github.com/lewtun), [@jplu](https://github.com/jplu), [@jbragg](https://github.com/jbragg), [@patrickvonplaten](https://github.com/patrickvonplaten) and [@mcmillanmajora](https://github.com/mcmillanmajora) for adding this dataset.

