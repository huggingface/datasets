---
annotations_creators:
  aidayago2:
  - crowdsourced
  - found
  - machine-generated
  cweb:
  - crowdsourced
  - found
  - machine-generated
  eli5:
  - crowdsourced
  - found
  fever:
  - crowdsourced
  - found
  - machine-generated
  hotpotqa:
  - crowdsourced
  - found
  - machine-generated
  nq:
  - crowdsourced
  - found
  - machine-generated
  structured_zeroshot:
  - crowdsourced
  - found
  - machine-generated
  trex:
  - crowdsourced
  - found
  - machine-generated
  triviaqa_support_only:
  - crowdsourced
  - found
  - machine-generated
  wned:
  - crowdsourced
  - found
  - machine-generated
  wow:
  - crowdsourced
  - found
  - machine-generated
language_creators:
  aidayago2:
  - crowdsourced
  cweb:
  - crowdsourced
  eli5:
  - found
  fever:
  - crowdsourced
  hotpotqa:
  - crowdsourced
  - found
  nq:
  - found
  structured_zeroshot:
  - crowdsourced
  trex:
  - crowdsourced
  triviaqa_support_only:
  - found
  wned:
  - crowdsourced
  wow:
  - crowdsourced
languages:
- en
licenses:
- mit
multilinguality:
- monolingual
size_categories:
  aidayago2:
  - 10K<n<100K
  cweb:
  - 10K<n<100K
  eli5:
  - 100K<n<1M
  fever:
  - 100K<n<1M
  hotpotqa:
  - 100K<n<1M
  nq:
  - 10K<n<100K
  structured_zeroshot:
  - 100K<n<1M
  trex:
  - 1M<n<10M
  triviaqa_support_only:
  - 10K<n<100K
  wned:
  - 1K<n<10K
  wow:
  - 100K<n<1M
source_datasets:
  aidayago2:
  - extended|other-aidayago
  - original
  cweb:
  - extended|other-wned-cweb
  - original
  eli5:
  - extended|other-hotpotqa
  - original
  fever:
  - extended|other-fever
  - original
  hotpotqa:
  - extended|other-hotpotqa
  - original
  nq:
  - extended|natural_questions
  - original
  structured_zeroshot:
  - extended|other-zero-shot-re
  - original
  trex:
  - extended|other-trex
  - original
  triviaqa_support_only:
  - extended|other-triviaqa
  - original
  wned:
  - extended|other-wned-wiki
  - original
  wow:
  - extended|other-wizardsofwikipedia
  - original
task_categories:
  aidayago2:
  - text-retrieval
  cweb:
  - text-retrieval
  eli5:
  - question-answering
  - text-retrieval
  fever:
  - text-classification
  - text-retrieval
  hotpotqa:
  - question-answering
  - text-retrieval
  nq:
  - question-answering
  - text-retrieval
  structured_zeroshot:
  - sequence-modeling
  - text-retrieval
  trex:
  - sequence-modeling
  - text-retrieval
  triviaqa_support_only:
  - question-answering
  - text-retrieval
  wned:
  - text-retrieval
  wow:
  - sequence-modeling
  - text-retrieval
task_ids:
  aidayago2:
  - document-retrieval
  - entity-linking-retrieval
  cweb:
  - document-retrieval
  - entity-linking-retrieval
  eli5:
  - abstractive-qa
  - document-retrieval
  - open-domain-qa
  fever:
  - document-retrieval
  - fact-checking
  - fact-checking-retrieval
  hotpotqa:
  - document-retrieval
  - extractive-qa
  - open-domain-qa
  nq:
  - document-retrieval
  - extractive-qa
  - open-domain-qa
  structured_zeroshot:
  - document-retrieval
  - slot-filling
  trex:
  - document-retrieval
  - slot-filling
  triviaqa_support_only:
  - document-retrieval
  - extractive-qa
  - open-domain-qa
  wned:
  - document-retrieval
  - entity-linking-retrieval
  wow:
  - dialogue-modeling
  - document-retrieval
paperswithcode_id: kilt
pretty_name: KILT
---

# Dataset Card for KILT

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

- **Homepage:** https://ai.facebook.com/tools/kilt/
- **Repository:** https://github.com/facebookresearch/KILT
- **Paper:** https://arxiv.org/abs/2009.02252
- **Leaderboard:** https://eval.ai/web/challenges/challenge-page/689/leaderboard/
- **Point of Contact:** [Needs More Information]

### Dataset Summary

KILT has been built from 11 datasets representing 5 types of tasks:

- Fact-checking
- Entity linking
- Slot filling
- Open domain QA
- Dialog generation

All these datasets have been grounded in a single pre-processed Wikipedia dump, allowing for fairer and more consistent evaluation as well as enabling new task setups such as multitask and transfer learning with minimal effort. KILT also provides tools to analyze and understand the predictions made by models, as well as the evidence they provide for their predictions.

#### Loading the KILT knowledge source and task data

The original KILT [release](https://github.com/facebookresearch/KILT) only provides question IDs for the TriviaQA task. Using the full dataset requires mapping those back to the TriviaQA questions, which can be done as follows: 

```python
from datasets import load_dataset

# Get the pre-processed Wikipedia knowledge source for kild
kilt_wiki = load_dataset("kilt_wikipedia")

# Get the KILT task datasets
kilt_triviaqa = load_dataset("kilt_tasks", name="triviaqa_support_only")

# Most tasks in KILT already have all required data, but KILT-TriviaQA
# only provides the question IDs, not the questions themselves.
# Thankfully, we can get the original TriviaQA data with:
trivia_qa = load_dataset('trivia_qa', 'unfiltered.nocontext')

# The KILT IDs can then be mapped to the TriviaQA questions with:
triviaqa_map = {}

def add_missing_data(x, trivia_qa_subset, triviaqa_map):
    i = triviaqa_map[x['id']]
    x['input'] = trivia_qa_subset[i]['question']
    x['output']['original_answer'] = trivia_qa_subset[i]['answer']['value']
    return x
    
for k in ['train', 'validation', 'test']:
    triviaqa_map = dict([(q_id, i) for i, q_id in enumerate(trivia_qa[k]['question_id'])])
    kilt_triviaqa[k] = kilt_triviaqa[k].filter(lambda x: x['id'] in triviaqa_map)
    kilt_triviaqa[k] = kilt_triviaqa[k].map(add_missing_data, fn_kwargs=dict(trivia_qa_subset=trivia_qa[k], triviaqa_map=triviaqa_map))
```

### Supported Tasks and Leaderboards

The dataset supports a leaderboard that evaluates models against task-specific metrics such as F1 or EM, as well as their ability to retrieve supporting information from Wikipedia.

The current best performing models can be found [here](https://eval.ai/web/challenges/challenge-page/689/leaderboard/).

### Languages

All tasks are in English (`en`).

## Dataset Structure

### Data Instances

An example of open-domain QA from the Natural Questions `nq` configuration looks as follows:
```
{'id': '-5004457603684974952',
 'input': 'who is playing the halftime show at super bowl 2016',
 'meta': {'left_context': '',
  'mention': '',
  'obj_surface': [],
  'partial_evidence': [],
  'right_context': '',
  'sub_surface': [],
  'subj_aliases': [],
  'template_questions': []},
 'output': [{'answer': 'Coldplay',
   'meta': {'score': 0},
   'provenance': [{'bleu_score': 1.0,
     'end_character': 186,
     'end_paragraph_id': 1,
     'meta': {'annotation_id': '-1',
      'evidence_span': [],
      'fever_page_id': '',
      'fever_sentence_id': -1,
      'yes_no_answer': ''},
     'section': 'Section::::Abstract.',
     'start_character': 178,
     'start_paragraph_id': 1,
     'title': 'Super Bowl 50 halftime show',
     'wikipedia_id': '45267196'}]},
  {'answer': 'Beyoncé',
   'meta': {'score': 0},
   'provenance': [{'bleu_score': 1.0,
     'end_character': 224,
     'end_paragraph_id': 1,
     'meta': {'annotation_id': '-1',
      'evidence_span': [],
      'fever_page_id': '',
      'fever_sentence_id': -1,
      'yes_no_answer': ''},
     'section': 'Section::::Abstract.',
     'start_character': 217,
     'start_paragraph_id': 1,
     'title': 'Super Bowl 50 halftime show',
     'wikipedia_id': '45267196'}]},
  {'answer': 'Bruno Mars',
   'meta': {'score': 0},
   'provenance': [{'bleu_score': 1.0,
     'end_character': 239,
     'end_paragraph_id': 1,
     'meta': {'annotation_id': '-1',
      'evidence_span': [],
      'fever_page_id': '',
      'fever_sentence_id': -1,
      'yes_no_answer': ''},
     'section': 'Section::::Abstract.',
     'start_character': 229,
     'start_paragraph_id': 1,
     'title': 'Super Bowl 50 halftime show',
     'wikipedia_id': '45267196'}]},
  {'answer': 'Coldplay with special guest performers Beyoncé and Bruno Mars',
   'meta': {'score': 0},
   'provenance': []},
  {'answer': 'British rock group Coldplay with special guest performers Beyoncé and Bruno Mars',
   'meta': {'score': 0},
   'provenance': []},
  {'answer': '',
   'meta': {'score': 0},
   'provenance': [{'bleu_score': 0.9657992720603943,
     'end_character': 341,
     'end_paragraph_id': 1,
     'meta': {'annotation_id': '2430977867500315580',
      'evidence_span': [],
      'fever_page_id': '',
      'fever_sentence_id': -1,
      'yes_no_answer': 'NONE'},
     'section': 'Section::::Abstract.',
     'start_character': 0,
     'start_paragraph_id': 1,
     'title': 'Super Bowl 50 halftime show',
     'wikipedia_id': '45267196'}]},
  {'answer': '',
   'meta': {'score': 0},
   'provenance': [{'bleu_score': -1.0,
     'end_character': -1,
     'end_paragraph_id': 1,
     'meta': {'annotation_id': '-1',
      'evidence_span': ['It was headlined by the British rock group Coldplay with special guest performers Beyoncé and Bruno Mars',
       'It was headlined by the British rock group Coldplay with special guest performers Beyoncé and Bruno Mars, who previously had headlined the Super Bowl XLVII and Super Bowl XLVIII halftime shows, respectively.',
       "The Super Bowl 50 Halftime Show took place on February 7, 2016, at Levi's Stadium in Santa Clara, California as part of Super Bowl 50. It was headlined by the British rock group Coldplay with special guest performers Beyoncé and Bruno Mars",
       "The Super Bowl 50 Halftime Show took place on February 7, 2016, at Levi's Stadium in Santa Clara, California as part of Super Bowl 50. It was headlined by the British rock group Coldplay with special guest performers Beyoncé and Bruno Mars,"],
      'fever_page_id': '',
      'fever_sentence_id': -1,
      'yes_no_answer': ''},
     'section': 'Section::::Abstract.',
     'start_character': -1,
     'start_paragraph_id': 1,
     'title': 'Super Bowl 50 halftime show',
     'wikipedia_id': '45267196'}]}]}
```

### Data Fields

Examples from all configurations have the following features:

- `input`: a `string` feature representing the query.
- `output`: a `list` of features each containing information for an answer, made up of:
  - `answer`: a `string` feature representing a possible answer.
  - `provenance`: a `list` of features representing Wikipedia passages that support the `answer`, denoted by:
    - `title`: a `string` feature, the title of the Wikipedia article the passage was retrieved from.
    - `section`: a `string` feature, the title of the section in Wikipedia article.
    - `wikipedia_id`: a `string` feature, a unique identifier for the Wikipedia article.
    - `start_character`: a `int32` feature.
    - `start_paragraph_id`: a `int32` feature.
    - `end_character`: a `int32` feature.
    - `end_paragraph_id`: a `int32` feature.


### Data Splits

The configurations have the following splits:

|             | Train       | Validation  | Test        |
| ----------- | ----------- | ----------- | ----------- |
| triviaqa    | 61844         | 5359  | 6586  |
| fever       | 104966        | 10444         | 10100         |
| aidayago2   | 18395         | 4784  | 4463  |
| wned   | | 3396 | 3376 |
| cweb   | | 5599 | 5543 |
| trex   | 2284168       | 5000  | 5000  |
| structured_zeroshot    | 147909        | 3724  | 4966  |
| nq     | 87372         | 2837  | 1444  |
| hotpotqa       | 88869         | 5600  | 5569  |
| eli5   | 272634        | 1507  | 600   |
| wow    | 94577         | 3058  | 2944  |


## Dataset Creation

### Curation Rationale

[Needs More Information]

### Source Data

#### Initial Data Collection and Normalization

[Needs More Information]

#### Who are the source language producers?

[Needs More Information]

### Annotations

#### Annotation process

[Needs More Information]

#### Who are the annotators?

[Needs More Information]

### Personal and Sensitive Information

[Needs More Information]

## Considerations for Using the Data

### Social Impact of Dataset

[Needs More Information]

### Discussion of Biases

[Needs More Information]

### Other Known Limitations

[Needs More Information]

## Additional Information

### Dataset Curators

[Needs More Information]

### Licensing Information

[Needs More Information]

### Citation Information

Cite as:
```
@inproceedings{kilt_tasks,
  author    = {Fabio Petroni and
               Aleksandra Piktus and
               Angela Fan and
               Patrick S. H. Lewis and
               Majid Yazdani and
               Nicola De Cao and
               James Thorne and
               Yacine Jernite and
               Vladimir Karpukhin and
               Jean Maillard and
               Vassilis Plachouras and
               Tim Rockt{\"{a}}schel and
               Sebastian Riedel},
  editor    = {Kristina Toutanova and
               Anna Rumshisky and
               Luke Zettlemoyer and
               Dilek Hakkani{-}T{\"{u}}r and
               Iz Beltagy and
               Steven Bethard and
               Ryan Cotterell and
               Tanmoy Chakraborty and
               Yichao Zhou},
  title     = {{KILT:} a Benchmark for Knowledge Intensive Language Tasks},
  booktitle = {Proceedings of the 2021 Conference of the North American Chapter of
               the Association for Computational Linguistics: Human Language Technologies,
               {NAACL-HLT} 2021, Online, June 6-11, 2021},
  pages     = {2523--2544},
  publisher = {Association for Computational Linguistics},
  year      = {2021},
  url       = {https://www.aclweb.org/anthology/2021.naacl-main.200/}
}
```

### Contributions

Thanks to [@thomwolf](https://github.com/thomwolf), [@yjernite](https://github.com/yjernite) for adding this dataset.
