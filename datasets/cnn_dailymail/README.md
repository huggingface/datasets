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
---
# Dataset Card for CNN Dailymail Dataset

## Table of Contents
- [Tasks Supported](#tasks-supported)
- [Purpose](#purpose)
- [Languages](#languages)
- [People Involved](#who-iswas-involved-in-the-dataset-use-and-creation)
- [Data Characteristics](#data-characteristics)
- [Dataset Structure](#dataset-structure)
- [Known Limitations](#known-limitations)
- [Licensing information](#licensing-information)

## Tasks supported:
### Task categorization / tags

[Versions 2.0.0 and 3.0.0 of the CCN / DailyMail Dataset](https://www.aclweb.org/anthology/K16-1028.pdf) were developed for abstractive and extractive summarization. [Version 1.0.0](https://papers.nips.cc/paper/5945-teaching-machines-to-read-and-comprehend.pdf) was developed for machine reading and comprehension and abstractive question answering. 

## Purpose

Version 1.0.0 aimed to support supervised neural methodologies for machine reading and question answering with a large amount of real natural language training data and released about 313k unique articles and nearly 1M Cloze style questions to go with the articles. Versions 2.0.0 and 3.0.0 changed the structure of the dataset to support summarization rather than question answering. Version 3.0.0 provided a non-anonymized version of the data, whereas both the previous versions were preprocessed to replace named entities with unique identifier labels. 

## Languages 
### Per language:

The BCP-47 code for English as generally spoken in the United States is en-US and the BCP-47 code for English as generally spoken in the United Kingdom is en-GB. It is unknown if other varieties of English are represented in the data.

## Who is/was involved in the dataset use and creation? 
### Who are the dataset curators? 

The data was originally collected by Karl Moritz Hermann, Tomáš Kočiský, Edward Grefenstette, Lasse Espeholt, Will Kay, Mustafa Suleyman, and Phil Blunsom of Google DeepMind. Tomáš Kočiský and Phil Blunsom are also affiliated with the University of Oxford. They released scripts to collect and process the data into the question answering format. 

Ramesh Nallapati, Bowen Zhou, Cicero dos Santos, and Bing Xiang of IMB Watson and Çağlar Gu̇lçehre of Université de Montréal modified Hermann et al's collection scripts to restore the data to a summary format. They also produced both anonymized and non-anonymized versions.

The code for the non-anonymized version is made publicly available by Abigail See of Stanford University, Peter J. Liu of Google Brain and Christopher D. Manning of Stanford University at <https://github.com/abisee/cnn-dailymail>. The work at Stanford University was supported by the DARPA DEFT ProgramAFRL contract no. FA8750-13-2-0040.


### Who are the language producers (who wrote the text / created the base content)?

The text was written by journalists at CNN and the Daily Mail. 

### Who are the annotators?

No annotation was provided with the dataset.

## Data characteristics

The data consists of news articles and highlight sentences. In the question answering setting of the data, the articles are used as the context and entities are hidden one at a time in the highlight sentences, producing Cloze style questions where the goal of the model is to correctly guess which entity in the context has been hidden in the highlight. In the summarization setting, the highlight sentences are concatenated to form a summary of the article. The CNN articles were written between April 2007 and April 2015. The Daily Mail articles were written between June 2010 and April 2015. 

### How was the data collected?

The code for the original data collection is available at <https://github.com/deepmind/rc-data>. The articles were downloaded using archives of <www.cnn.com> and <www.dailymail.co.uk> on the Wayback Machine. Articles were not included in the Version 1.0.0 collection if they exceeded 2000 tokens. Due to accessibility issues with the Wayback Machine, Kyunghyun Cho has made the datasets available at <https://cs.nyu.edu/~kcho/DMQA/>. An updated version of the code that does not anonymize the data is available at <https://github.com/abisee/cnn-dailymail>. 


### Normalization information

Hermann et al provided their own tokenization script. The script provided by See uses the PTBTokenizer. It also lowercases the text and adds periods to lines missing them.

### Annotation process

No annotation was provided with the dataset.

## Dataset Structure
### Splits, features, and labels

The CNN/DailyMail dataset has 3 splits: _train_, _validation_, and _test_. Below are the statistics for Version 3.0.0 of the dataset.

Dataset Split | Number of Instances in Split
--------------|--------------------------------------------
Train | 287,113
Validation | 13,368
Test | 11,490

Each data instance contains the following features: _article_, _highlights_, _id_.

Feature | Mean Token Count
--------|-----------------
Article | 781 
Highlights | 56

### Span indices

No span indices are included in this dataset.

### Example ID

An example ID is '0001d1afc246a7964130f43ae940af6bc6c57f01'. These are heximal formated SHA1 hashes of the urls where the stories were retrieved from.

### Free text description for context (e.g. describe difference between title / selftext / body in Reddit data) and example

For each ID, there is a string for the article, a string for the highlights, and a string for the id. See the [CNN / Daily Mail dataset viewer](https://huggingface.co/nlp/viewer/?dataset=cnn_dailymail&config=3.0.0) to explore more examples.

ID | Article | Hightlights 
---|---------|------------
0054d6d30dbcad772e20b22771153a2a9cbeaf62 | (CNN) -- An American woman died aboard a cruise ship that docked at Rio de Janeiro on Tuesday, the same ship on which 86 passengers previously fell ill, according to the state-run Brazilian news agency, Agencia Brasil. The American tourist died aboard the MS Veendam, owned by cruise operator Holland America. Federal Police told Agencia Brasil that forensic doctors were investigating her death. The ship's doctors told police that the woman was elderly and suffered from diabetes and hypertension, according the agency. The other passengers came down with diarrhea prior to her death during an earlier part of the trip, the ship's doctors said. The Veendam left New York 36 days ago for a South America tour.	| The elderly woman suffered from diabetes and hypertension, ship's doctors say .\nPreviously, 86 passengers had fallen ill on the ship, Agencia Brasil says .

### Suggested metrics / models:

[Zhong et al (2020)](https://www.aclweb.org/anthology/2020.acl-main.552.pdf) report a ROUGE-1 score of 44.41. See the [Papers With Code leaderboard](https://paperswithcode.com/sota/document-summarization-on-cnn-daily-mail) for more models. 

## Known Limitations
### Known social biases

[Bordia and Bowman (2019)](https://www.aclweb.org/anthology/N19-3002.pdf) explore measuring gender bias and debiasing techniques in the CNN / Dailymail dataset, the Penn Treebank, and WikiText-2. They find the CNN / Dailymail dataset to have a slightly lower gender bias based on their metric compared to the other datasets, but still show evidence of gender bias when looking at words such as 'fragile'.

### Other known limitations

News articles have been shown to conform to writing conventions in which important information is primarily presented in the first third of the article [(Kryściński et al, 2019)](https://www.aclweb.org/anthology/D19-1051.pdf). [Chen et al (2016)](https://www.aclweb.org/anthology/P16-1223.pdf) conducted a manual study of 100 random instances of the first version of the dataset and found 25% of the samples to be difficult even for humans to answer correctly due to ambiguity and coreference errors. 

## Licensing information

The CNN / Daily Mail dataset version 1.0.0 is released under the [Apache-2.0 License](http://www.apache.org/licenses/LICENSE-2.0). 
