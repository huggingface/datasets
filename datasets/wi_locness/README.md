---
annotations_creators:
- expert-generated
language_creators:
- crowdsourced
languages:
- en
licenses:
  wi:
  - other-wi-license
  locness:
  - other-locness-license
multilinguality:
- monolingual
- other-language-learner
size_categories:
- 1K<n<10K
source_datasets:
- original
task_categories:
- conditional-text-generation
task_ids:
- conditional-text-generation-other-grammatical-error-correction
paperswithcode_id: locness-corpus
pretty_name:
  wi: Cambridge English Write & Improve
  locness: LOCNESS
---

# Dataset Card for Cambridge English Write & Improve + LOCNESS Dataset

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

- **Homepage:** https://www.cl.cam.ac.uk/research/nl/bea2019st/#data
- **Repository:**
- **Paper:** https://www.aclweb.org/anthology/W19-4406/
- **Leaderboard:** https://competitions.codalab.org/competitions/20228#results
- **Point of Contact:**

### Dataset Summary

Write & Improve (Yannakoudakis et al., 2018) is an online web platform that assists non-native English students with their writing. Specifically, students from around the world submit letters, stories, articles and essays in response to various prompts, and the W&I system provides instant feedback. Since W&I went live in 2014, W&I annotators have manually annotated some of these submissions and assigned them a CEFR level.

The LOCNESS corpus (Granger, 1998) consists of essays written by native English students. It was originally compiled by researchers at the Centre for English Corpus Linguistics at the University of Louvain. Since native English students also sometimes make mistakes, we asked the W&I annotators to annotate a subsection of LOCNESS so researchers can test the effectiveness of their systems on the full range of English levels and abilities.

### Supported Tasks and Leaderboards

Grammatical error correction (GEC) is the task of automatically correcting grammatical errors in text; e.g. [I follows his advices -> I followed his advice]. It can be used to not only help language learners improve their writing skills, but also alert native speakers to accidental mistakes or typos.

The aim of the task of this dataset is to correct all types of errors in written text. This includes grammatical, lexical and orthographical errors.

The following Codalab competition contains the latest leaderboard, along with information on how to submit to the withheld W&I+LOCNESS test set: https://competitions.codalab.org/competitions/20228

### Languages

The dataset is in English.

## Dataset Structure

### Data Instances

An example from the `wi` configuration:

```
{
  'id': '1-140178',
  'userid': '21251',
  'cefr': 'A2.i',
  'text': 'My town is a medium size city with eighty thousand inhabitants. It has a high density population because its small territory. Despite of it is an industrial city, there are many shops and department stores.  I recommend visiting the artificial lake in the certer of the city which is surrounded by a park. Pasteries are very common and most of them offer the special dessert from the city. There are a comercial zone along the widest street of the city where you can find all kind of establishments: banks, bars, chemists, cinemas, pet shops, restaurants, fast food restaurants, groceries, travel agencies, supermarkets and others. Most of the shops have sales and offers at least three months of the year: January, June and August. The quality of the products and services are quite good, because there are a huge competition, however I suggest you taking care about some fakes or cheats.',
  'edits': {
    'start': [13, 77, 104, 126, 134, 256, 306, 375, 396, 402, 476, 484, 579, 671, 774, 804, 808, 826, 838, 850, 857, 862, 868],
    'end': [24, 78, 104, 133, 136, 262, 315, 379, 399, 411, 480, 498, 588, 671, 777, 807, 810, 835, 845, 856, 861, 867, 873],
    'text': ['medium-sized', '-', ' of', 'Although', '', 'center', None, 'of', 'is', 'commercial', 'kinds', 'businesses', 'grocers', ' in', 'is', 'is', '', '. However,', 'recommend', 'be', 'careful', 'of', '']
  }
}
```

An example from the `locness` configuration:

```
{
  'id': '7-5819177',
  'cefr': 'N',
  'text': 'Boxing is a common, well known and well loved sport amongst most countries in the world however it is also punishing, dangerous and disliked to the extent that many people want it banned, possibly with good reason.\nBoxing is a dangerous sport, there are relatively common deaths, tragic injuries and even disease. All professional boxers are at risk from being killed in his next fight. If not killed then more likely paralysed. There have been a number of cases in the last ten years of the top few boxers having tragic losses throughout their ranks. This is just from the elite few, and theres more from those below them.\nMore deaths would occur through boxing if it were banned. The sport would go underground, there would be no safety measures like gloves, a doctor, paramedics or early stopping of the fight if someone looked unable to continue. With this going on the people taking part will be dangerous, and on the streets. Dangerous dogs who were trained to kill and maim in similar underound dog fights have already proved deadly to innocent people, the new boxers could be even more at risk.\nOnce boxing is banned and no-one grows up knowing it as acceptable there will be no interest in boxing and hopefully less all round interest in violence making towns and cities much safer places to live in, there will be less fighting outside pubs and clubs and less violent attacks with little or no reason.\nchange the rules of boxing slightly would much improve the safety risks of the sport and not detract form the entertainment. There are all sorts of proposals, lighter and more cushioning gloves could be worn, ban punches to the head, headguards worn or make fights shorter, as most of the serious injuries occur in the latter rounds, these would all show off the boxers skill and tallent and still be entertaining to watch.\nEven if a boxer is a success and manages not to be seriously hurt he still faces serious consequences in later life diseases that attack the brains have been known to set in as a direct result of boxing, even Muhamed Ali, who was infamous(?) both for his boxing and his quick-witted intelligence now has Alzheimer disease and can no longer do many everyday acts.\nMany other sports are more dangerous than boxing, motor sports and even mountaineering has risks that are real. Boxers chose to box, just as racing drivers drive.',
  'edits': {
    'start': [24, 39, 52, 87, 242, 371, 400, 528, 589, 713, 869, 992, 1058, 1169, 1209, 1219, 1255, 1308, 1386, 1412, 1513, 1569, 1661, 1731, 1744, 1781, 1792, 1901, 1951, 2038, 2131, 2149, 2247, 2286],
    'end': [25, 40, 59, 95, 249, 374, 400, 538, 595, 713, 869, 1001, 1063, 1169, 1209, 1219, 1255, 1315, 1390, 1418, 1517, 1570, 1661, 1737, 1751, 1781, 1799, 1901, 1960, 2044, 2131, 2149, 2248, 2289],
    'text': ['-', '-', 'in', '. However,', '. There', 'their', ',', 'among', "there's", ' and', ',', 'underground', '. The', ',', ',', ',', ',', '. There', 'for', 'Changing', 'from', ';', ',', 'later', '. These', "'", 'talent', ',', '. Diseases', '. Even', ',', "'s", ';', 'have']
  }
}
```

### Data Fields

The fields of the dataset are:
- `id`: the id of the text as a string
- `cefr`: the [CEFR level](https://www.cambridgeenglish.org/exams-and-tests/cefr/) of the text as a string
- `userid`: id of the user
- `text`: the text of the submission as a string
- `edits`: the edits from W&I:
  - `start`: start indexes of each edit as a list of integers
  - `end`: end indexes of each edit as a list of integers
  - `text`: the text content of each edit as a list of strings
  - `from`: the original text of each edit as a list of strings

### Data Splits

|   name   |train|validation|
|----------|----:|---------:|
| wi       | 3000|       300|
| locness  |  N/A|        50|

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

Write & Improve License:

```
Cambridge English Write & Improve (CEWI) Dataset Licence Agreement

1. By downloading this dataset and licence, this licence agreement is
   entered into, effective this date, between you, the Licensee, and the
   University of Cambridge, the Licensor.

2. Copyright of the entire licensed dataset is held by the Licensor.
   No ownership or interest in the dataset is transferred to the
   Licensee.

3. The Licensor hereby grants the Licensee a non-exclusive
   non-transferable right to use the licensed dataset for
   non-commercial research and educational purposes.

4. Non-commercial purposes exclude without limitation any use of the
   licensed dataset or information derived from the dataset for or as
   part of a product or service which is sold, offered for sale,
   licensed, leased or rented.

5. The Licensee shall acknowledge use of the licensed dataset in all
   publications of research based on it, in whole or in part, through
   citation of the following publication:

   Helen Yannakoudakis, Øistein E. Andersen, Ardeshir Geranpayeh, 
   Ted Briscoe and Diane Nicholls. 2018. Developing an automated writing 
   placement system for ESL learners. Applied Measurement in Education.
   
6. The Licensee may publish excerpts of less than 100 words from the
   licensed dataset pursuant to clause 3.

7. The Licensor grants the Licensee this right to use the licensed dataset
   "as is". Licensor does not make, and expressly disclaims, any express or
   implied warranties, representations or endorsements of any kind
   whatsoever.

8. This Agreement shall be governed by and construed in accordance with
   the laws of England and the English courts shall have exclusive
   jurisdiction.
```

LOCNESS License:

```
LOCNESS Dataset Licence Agreement

1. The corpus is to be used for non-commercial purposes only

2. All publications on research partly or wholly based on the corpus should give credit to the Centre for English Corpus Linguistics (CECL), Université catholique de Louvain, Belgium. A scanned copy or offprint of the publication should also be sent to <sylviane.granger@uclouvain.be>. 

3. No part of the corpus is to be distributed to a third party without specific authorization from CECL. The corpus can only be used by the person agreeing to the licence terms and researchers working in close collaboration with him/her or students under his/her supervision, attached to the same institution, within the framework of the research project.
```

### Citation Information

```
@inproceedings{bryant-etal-2019-bea,
    title = "The {BEA}-2019 Shared Task on Grammatical Error Correction",
    author = "Bryant, Christopher  and
      Felice, Mariano  and
      Andersen, {\O}istein E.  and
      Briscoe, Ted",
    booktitle = "Proceedings of the Fourteenth Workshop on Innovative Use of NLP for Building Educational Applications",
    month = aug,
    year = "2019",
    address = "Florence, Italy",
    publisher = "Association for Computational Linguistics",
    url = "https://www.aclweb.org/anthology/W19-4406",
    doi = "10.18653/v1/W19-4406",
    pages = "52--75",
    abstract = "This paper reports on the BEA-2019 Shared Task on Grammatical Error Correction (GEC). As with the CoNLL-2014 shared task, participants are required to correct all types of errors in test data. One of the main contributions of the BEA-2019 shared task is the introduction of a new dataset, the Write{\&}Improve+LOCNESS corpus, which represents a wider range of native and learner English levels and abilities. Another contribution is the introduction of tracks, which control the amount of annotated data available to participants. Systems are evaluated in terms of ERRANT F{\_}0.5, which allows us to report a much wider range of performance statistics. The competition was hosted on Codalab and remains open for further submissions on the blind test set.",
}
```

### Contributions

Thanks to [@aseifert](https://github.com/aseifert) for adding this dataset.
