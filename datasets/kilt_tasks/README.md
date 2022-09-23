---
annotations_creators:
- crowdsourced
- found
- machine-generated
language_creators:
- crowdsourced
- found
language:
- en
license:
- mit
multilinguality:
- monolingual
size_categories:
- 100K<n<1M
- 10K<n<100K
- 1K<n<10K
- 1M<n<10M
source_datasets:
- extended|natural_questions
- extended|other-aidayago
- extended|other-fever
- extended|other-hotpotqa
- extended|other-trex
- extended|other-triviaqa
- extended|other-wizardsofwikipedia
- extended|other-wned-cweb
- extended|other-wned-wiki
- extended|other-zero-shot-re
- original
task_categories:
- fill-mask
- question-answering
- text-classification
- text-generation
- text-retrieval
- text2text-generation
task_ids:
- abstractive-qa
- dialogue-modeling
- document-retrieval
- entity-linking-retrieval
- extractive-qa
- fact-checking
- fact-checking-retrieval
- open-domain-abstractive-qa
- open-domain-qa
- slot-filling
paperswithcode_id: kilt
pretty_name: KILT
configs:
- aidayago2
- cweb
- eli5
- fever
- hotpotqa
- nq
- structured_zeroshot
- trex
- triviaqa_support_only
- wned
- wow
dataset_info:
- config_name: triviaqa_support_only
  features:
  - name: id
    dtype: string
  - name: input
    dtype: string
  - name: meta
    struct:
    - name: left_context
      dtype: string
    - name: mention
      dtype: string
    - name: right_context
      dtype: string
    - name: partial_evidence
      list:
      - name: start_paragraph_id
        dtype: int32
      - name: end_paragraph_id
        dtype: int32
      - name: title
        dtype: string
      - name: section
        dtype: string
      - name: wikipedia_id
        dtype: string
      - name: meta
        struct:
        - name: evidence_span
          list: string
    - name: obj_surface
      list: string
    - name: sub_surface
      list: string
    - name: subj_aliases
      list: string
    - name: template_questions
      list: string
  - name: output
    list:
    - name: answer
      dtype: string
    - name: meta
      struct:
      - name: score
        dtype: int32
    - name: provenance
      list:
      - name: bleu_score
        dtype: float32
      - name: start_character
        dtype: int32
      - name: start_paragraph_id
        dtype: int32
      - name: end_character
        dtype: int32
      - name: end_paragraph_id
        dtype: int32
      - name: meta
        struct:
        - name: fever_page_id
          dtype: string
        - name: fever_sentence_id
          dtype: int32
        - name: annotation_id
          dtype: string
        - name: yes_no_answer
          dtype: string
        - name: evidence_span
          list: string
      - name: section
        dtype: string
      - name: title
        dtype: string
      - name: wikipedia_id
        dtype: string
  splits:
  - name: test
    num_bytes: 341964
    num_examples: 6586
  - name: train
    num_bytes: 72024147
    num_examples: 61844
  - name: validation
    num_bytes: 6824774
    num_examples: 5359
  download_size: 111546348
  dataset_size: 79190885
- config_name: fever
  features:
  - name: id
    dtype: string
  - name: input
    dtype: string
  - name: meta
    struct:
    - name: left_context
      dtype: string
    - name: mention
      dtype: string
    - name: right_context
      dtype: string
    - name: partial_evidence
      list:
      - name: start_paragraph_id
        dtype: int32
      - name: end_paragraph_id
        dtype: int32
      - name: title
        dtype: string
      - name: section
        dtype: string
      - name: wikipedia_id
        dtype: string
      - name: meta
        struct:
        - name: evidence_span
          list: string
    - name: obj_surface
      list: string
    - name: sub_surface
      list: string
    - name: subj_aliases
      list: string
    - name: template_questions
      list: string
  - name: output
    list:
    - name: answer
      dtype: string
    - name: meta
      struct:
      - name: score
        dtype: int32
    - name: provenance
      list:
      - name: bleu_score
        dtype: float32
      - name: start_character
        dtype: int32
      - name: start_paragraph_id
        dtype: int32
      - name: end_character
        dtype: int32
      - name: end_paragraph_id
        dtype: int32
      - name: meta
        struct:
        - name: fever_page_id
          dtype: string
        - name: fever_sentence_id
          dtype: int32
        - name: annotation_id
          dtype: string
        - name: yes_no_answer
          dtype: string
        - name: evidence_span
          list: string
      - name: section
        dtype: string
      - name: title
        dtype: string
      - name: wikipedia_id
        dtype: string
  splits:
  - name: test
    num_bytes: 1042660
    num_examples: 10100
  - name: train
    num_bytes: 23941622
    num_examples: 104966
  - name: validation
    num_bytes: 3168503
    num_examples: 10444
  download_size: 45954548
  dataset_size: 28152785
- config_name: aidayago2
  features:
  - name: id
    dtype: string
  - name: input
    dtype: string
  - name: meta
    struct:
    - name: left_context
      dtype: string
    - name: mention
      dtype: string
    - name: right_context
      dtype: string
    - name: partial_evidence
      list:
      - name: start_paragraph_id
        dtype: int32
      - name: end_paragraph_id
        dtype: int32
      - name: title
        dtype: string
      - name: section
        dtype: string
      - name: wikipedia_id
        dtype: string
      - name: meta
        struct:
        - name: evidence_span
          list: string
    - name: obj_surface
      list: string
    - name: sub_surface
      list: string
    - name: subj_aliases
      list: string
    - name: template_questions
      list: string
  - name: output
    list:
    - name: answer
      dtype: string
    - name: meta
      struct:
      - name: score
        dtype: int32
    - name: provenance
      list:
      - name: bleu_score
        dtype: float32
      - name: start_character
        dtype: int32
      - name: start_paragraph_id
        dtype: int32
      - name: end_character
        dtype: int32
      - name: end_paragraph_id
        dtype: int32
      - name: meta
        struct:
        - name: fever_page_id
          dtype: string
        - name: fever_sentence_id
          dtype: int32
        - name: annotation_id
          dtype: string
        - name: yes_no_answer
          dtype: string
        - name: evidence_span
          list: string
      - name: section
        dtype: string
      - name: title
        dtype: string
      - name: wikipedia_id
        dtype: string
  splits:
  - name: test
    num_bytes: 14211859
    num_examples: 4463
  - name: train
    num_bytes: 68944642
    num_examples: 18395
  - name: validation
    num_bytes: 20743548
    num_examples: 4784
  download_size: 105637528
  dataset_size: 103900049
- config_name: wned
  features:
  - name: id
    dtype: string
  - name: input
    dtype: string
  - name: meta
    struct:
    - name: left_context
      dtype: string
    - name: mention
      dtype: string
    - name: right_context
      dtype: string
    - name: partial_evidence
      list:
      - name: start_paragraph_id
        dtype: int32
      - name: end_paragraph_id
        dtype: int32
      - name: title
        dtype: string
      - name: section
        dtype: string
      - name: wikipedia_id
        dtype: string
      - name: meta
        struct:
        - name: evidence_span
          list: string
    - name: obj_surface
      list: string
    - name: sub_surface
      list: string
    - name: subj_aliases
      list: string
    - name: template_questions
      list: string
  - name: output
    list:
    - name: answer
      dtype: string
    - name: meta
      struct:
      - name: score
        dtype: int32
    - name: provenance
      list:
      - name: bleu_score
        dtype: float32
      - name: start_character
        dtype: int32
      - name: start_paragraph_id
        dtype: int32
      - name: end_character
        dtype: int32
      - name: end_paragraph_id
        dtype: int32
      - name: meta
        struct:
        - name: fever_page_id
          dtype: string
        - name: fever_sentence_id
          dtype: int32
        - name: annotation_id
          dtype: string
        - name: yes_no_answer
          dtype: string
        - name: evidence_span
          list: string
      - name: section
        dtype: string
      - name: title
        dtype: string
      - name: wikipedia_id
        dtype: string
  splits:
  - name: test
    num_bytes: 13082096
    num_examples: 3376
  - name: validation
    num_bytes: 12659894
    num_examples: 3396
  download_size: 26163472
  dataset_size: 25741990
- config_name: cweb
  features:
  - name: id
    dtype: string
  - name: input
    dtype: string
  - name: meta
    struct:
    - name: left_context
      dtype: string
    - name: mention
      dtype: string
    - name: right_context
      dtype: string
    - name: partial_evidence
      list:
      - name: start_paragraph_id
        dtype: int32
      - name: end_paragraph_id
        dtype: int32
      - name: title
        dtype: string
      - name: section
        dtype: string
      - name: wikipedia_id
        dtype: string
      - name: meta
        struct:
        - name: evidence_span
          list: string
    - name: obj_surface
      list: string
    - name: sub_surface
      list: string
    - name: subj_aliases
      list: string
    - name: template_questions
      list: string
  - name: output
    list:
    - name: answer
      dtype: string
    - name: meta
      struct:
      - name: score
        dtype: int32
    - name: provenance
      list:
      - name: bleu_score
        dtype: float32
      - name: start_character
        dtype: int32
      - name: start_paragraph_id
        dtype: int32
      - name: end_character
        dtype: int32
      - name: end_paragraph_id
        dtype: int32
      - name: meta
        struct:
        - name: fever_page_id
          dtype: string
        - name: fever_sentence_id
          dtype: int32
        - name: annotation_id
          dtype: string
        - name: yes_no_answer
          dtype: string
        - name: evidence_span
          list: string
      - name: section
        dtype: string
      - name: title
        dtype: string
      - name: wikipedia_id
        dtype: string
  splits:
  - name: test
    num_bytes: 99209665
    num_examples: 5543
  - name: validation
    num_bytes: 89819628
    num_examples: 5599
  download_size: 190444736
  dataset_size: 189029293
- config_name: trex
  features:
  - name: id
    dtype: string
  - name: input
    dtype: string
  - name: meta
    struct:
    - name: left_context
      dtype: string
    - name: mention
      dtype: string
    - name: right_context
      dtype: string
    - name: partial_evidence
      list:
      - name: start_paragraph_id
        dtype: int32
      - name: end_paragraph_id
        dtype: int32
      - name: title
        dtype: string
      - name: section
        dtype: string
      - name: wikipedia_id
        dtype: string
      - name: meta
        struct:
        - name: evidence_span
          list: string
    - name: obj_surface
      list: string
    - name: sub_surface
      list: string
    - name: subj_aliases
      list: string
    - name: template_questions
      list: string
  - name: output
    list:
    - name: answer
      dtype: string
    - name: meta
      struct:
      - name: score
        dtype: int32
    - name: provenance
      list:
      - name: bleu_score
        dtype: float32
      - name: start_character
        dtype: int32
      - name: start_paragraph_id
        dtype: int32
      - name: end_character
        dtype: int32
      - name: end_paragraph_id
        dtype: int32
      - name: meta
        struct:
        - name: fever_page_id
          dtype: string
        - name: fever_sentence_id
          dtype: int32
        - name: annotation_id
          dtype: string
        - name: yes_no_answer
          dtype: string
        - name: evidence_span
          list: string
      - name: section
        dtype: string
      - name: title
        dtype: string
      - name: wikipedia_id
        dtype: string
  splits:
  - name: test
    num_bytes: 758742
    num_examples: 5000
  - name: train
    num_bytes: 1190269126
    num_examples: 2284168
  - name: validation
    num_bytes: 2573820
    num_examples: 5000
  download_size: 1757029516
  dataset_size: 1193601688
- config_name: structured_zeroshot
  features:
  - name: id
    dtype: string
  - name: input
    dtype: string
  - name: meta
    struct:
    - name: left_context
      dtype: string
    - name: mention
      dtype: string
    - name: right_context
      dtype: string
    - name: partial_evidence
      list:
      - name: start_paragraph_id
        dtype: int32
      - name: end_paragraph_id
        dtype: int32
      - name: title
        dtype: string
      - name: section
        dtype: string
      - name: wikipedia_id
        dtype: string
      - name: meta
        struct:
        - name: evidence_span
          list: string
    - name: obj_surface
      list: string
    - name: sub_surface
      list: string
    - name: subj_aliases
      list: string
    - name: template_questions
      list: string
  - name: output
    list:
    - name: answer
      dtype: string
    - name: meta
      struct:
      - name: score
        dtype: int32
    - name: provenance
      list:
      - name: bleu_score
        dtype: float32
      - name: start_character
        dtype: int32
      - name: start_paragraph_id
        dtype: int32
      - name: end_character
        dtype: int32
      - name: end_paragraph_id
        dtype: int32
      - name: meta
        struct:
        - name: fever_page_id
          dtype: string
        - name: fever_sentence_id
          dtype: int32
        - name: annotation_id
          dtype: string
        - name: yes_no_answer
          dtype: string
        - name: evidence_span
          list: string
      - name: section
        dtype: string
      - name: title
        dtype: string
      - name: wikipedia_id
        dtype: string
  splits:
  - name: test
    num_bytes: 1141537
    num_examples: 4966
  - name: train
    num_bytes: 47171201
    num_examples: 147909
  - name: validation
    num_bytes: 1612499
    num_examples: 3724
  download_size: 74927220
  dataset_size: 49925237
- config_name: nq
  features:
  - name: id
    dtype: string
  - name: input
    dtype: string
  - name: meta
    struct:
    - name: left_context
      dtype: string
    - name: mention
      dtype: string
    - name: right_context
      dtype: string
    - name: partial_evidence
      list:
      - name: start_paragraph_id
        dtype: int32
      - name: end_paragraph_id
        dtype: int32
      - name: title
        dtype: string
      - name: section
        dtype: string
      - name: wikipedia_id
        dtype: string
      - name: meta
        struct:
        - name: evidence_span
          list: string
    - name: obj_surface
      list: string
    - name: sub_surface
      list: string
    - name: subj_aliases
      list: string
    - name: template_questions
      list: string
  - name: output
    list:
    - name: answer
      dtype: string
    - name: meta
      struct:
      - name: score
        dtype: int32
    - name: provenance
      list:
      - name: bleu_score
        dtype: float32
      - name: start_character
        dtype: int32
      - name: start_paragraph_id
        dtype: int32
      - name: end_character
        dtype: int32
      - name: end_paragraph_id
        dtype: int32
      - name: meta
        struct:
        - name: fever_page_id
          dtype: string
        - name: fever_sentence_id
          dtype: int32
        - name: annotation_id
          dtype: string
        - name: yes_no_answer
          dtype: string
        - name: evidence_span
          list: string
      - name: section
        dtype: string
      - name: title
        dtype: string
      - name: wikipedia_id
        dtype: string
  splits:
  - name: test
    num_bytes: 334178
    num_examples: 1444
  - name: train
    num_bytes: 30388752
    num_examples: 87372
  - name: validation
    num_bytes: 6190493
    num_examples: 2837
  download_size: 60166499
  dataset_size: 36913423
- config_name: hotpotqa
  features:
  - name: id
    dtype: string
  - name: input
    dtype: string
  - name: meta
    struct:
    - name: left_context
      dtype: string
    - name: mention
      dtype: string
    - name: right_context
      dtype: string
    - name: partial_evidence
      list:
      - name: start_paragraph_id
        dtype: int32
      - name: end_paragraph_id
        dtype: int32
      - name: title
        dtype: string
      - name: section
        dtype: string
      - name: wikipedia_id
        dtype: string
      - name: meta
        struct:
        - name: evidence_span
          list: string
    - name: obj_surface
      list: string
    - name: sub_surface
      list: string
    - name: subj_aliases
      list: string
    - name: template_questions
      list: string
  - name: output
    list:
    - name: answer
      dtype: string
    - name: meta
      struct:
      - name: score
        dtype: int32
    - name: provenance
      list:
      - name: bleu_score
        dtype: float32
      - name: start_character
        dtype: int32
      - name: start_paragraph_id
        dtype: int32
      - name: end_character
        dtype: int32
      - name: end_paragraph_id
        dtype: int32
      - name: meta
        struct:
        - name: fever_page_id
          dtype: string
        - name: fever_sentence_id
          dtype: int32
        - name: annotation_id
          dtype: string
        - name: yes_no_answer
          dtype: string
        - name: evidence_span
          list: string
      - name: section
        dtype: string
      - name: title
        dtype: string
      - name: wikipedia_id
        dtype: string
  splits:
  - name: test
    num_bytes: 888476
    num_examples: 5569
  - name: train
    num_bytes: 33598679
    num_examples: 88869
  - name: validation
    num_bytes: 2371638
    num_examples: 5600
  download_size: 57516638
  dataset_size: 36858793
- config_name: eli5
  features:
  - name: id
    dtype: string
  - name: input
    dtype: string
  - name: meta
    struct:
    - name: left_context
      dtype: string
    - name: mention
      dtype: string
    - name: right_context
      dtype: string
    - name: partial_evidence
      list:
      - name: start_paragraph_id
        dtype: int32
      - name: end_paragraph_id
        dtype: int32
      - name: title
        dtype: string
      - name: section
        dtype: string
      - name: wikipedia_id
        dtype: string
      - name: meta
        struct:
        - name: evidence_span
          list: string
    - name: obj_surface
      list: string
    - name: sub_surface
      list: string
    - name: subj_aliases
      list: string
    - name: template_questions
      list: string
  - name: output
    list:
    - name: answer
      dtype: string
    - name: meta
      struct:
      - name: score
        dtype: int32
    - name: provenance
      list:
      - name: bleu_score
        dtype: float32
      - name: start_character
        dtype: int32
      - name: start_paragraph_id
        dtype: int32
      - name: end_character
        dtype: int32
      - name: end_paragraph_id
        dtype: int32
      - name: meta
        struct:
        - name: fever_page_id
          dtype: string
        - name: fever_sentence_id
          dtype: int32
        - name: annotation_id
          dtype: string
        - name: yes_no_answer
          dtype: string
        - name: evidence_span
          list: string
      - name: section
        dtype: string
      - name: title
        dtype: string
      - name: wikipedia_id
        dtype: string
  splits:
  - name: test
    num_bytes: 108108
    num_examples: 600
  - name: train
    num_bytes: 525586490
    num_examples: 272634
  - name: validation
    num_bytes: 13860153
    num_examples: 1507
  download_size: 562498660
  dataset_size: 539554751
- config_name: wow
  features:
  - name: id
    dtype: string
  - name: input
    dtype: string
  - name: meta
    struct:
    - name: left_context
      dtype: string
    - name: mention
      dtype: string
    - name: right_context
      dtype: string
    - name: partial_evidence
      list:
      - name: start_paragraph_id
        dtype: int32
      - name: end_paragraph_id
        dtype: int32
      - name: title
        dtype: string
      - name: section
        dtype: string
      - name: wikipedia_id
        dtype: string
      - name: meta
        struct:
        - name: evidence_span
          list: string
    - name: obj_surface
      list: string
    - name: sub_surface
      list: string
    - name: subj_aliases
      list: string
    - name: template_questions
      list: string
  - name: output
    list:
    - name: answer
      dtype: string
    - name: meta
      struct:
      - name: score
        dtype: int32
    - name: provenance
      list:
      - name: bleu_score
        dtype: float32
      - name: start_character
        dtype: int32
      - name: start_paragraph_id
        dtype: int32
      - name: end_character
        dtype: int32
      - name: end_paragraph_id
        dtype: int32
      - name: meta
        struct:
        - name: fever_page_id
          dtype: string
        - name: fever_sentence_id
          dtype: int32
        - name: annotation_id
          dtype: string
        - name: yes_no_answer
          dtype: string
        - name: evidence_span
          list: string
      - name: section
        dtype: string
      - name: title
        dtype: string
      - name: wikipedia_id
        dtype: string
  splits:
  - name: test
    num_bytes: 1340818
    num_examples: 2944
  - name: train
    num_bytes: 41873570
    num_examples: 63734
  - name: validation
    num_bytes: 2022128
    num_examples: 3054
  download_size: 52647339
  dataset_size: 45236516
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