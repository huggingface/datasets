---
annotations_creators:
- expert-generated
language_creators:
- expert-generated
languages:
- en
licenses:
- cc-by-sa-4.0
multilinguality:
- monolingual
size_categories:
- 10K<n<100K
source_datasets:
- original
task_categories:
- sequence-modeling
- text-classification
- text-scoring
task_ids:
  dyda_da:
  - dialogue-modeling
  - language-modeling
  - text-classification-other-dialogue-act-classification
  dyda_e:
  - dialogue-modeling
  - language-modeling
  - text-classification-other-emotion-classification
  iemocap:
  - dialogue-modeling
  - language-modeling
  - text-classification-other-emotion-classification
  maptask:
  - dialogue-modeling
  - language-modeling
  - text-classification-other-dialogue-act-classification
  meld_e:
  - dialogue-modeling
  - language-modeling
  - text-classification-other-emotion-classification
  meld_s:
  - dialogue-modeling
  - language-modeling
  - sentiment-classification
  mrda:
  - dialogue-modeling
  - language-modeling
  - text-classification-other-dialogue-act-classification
  oasis:
  - dialogue-modeling
  - language-modeling
  - text-classification-other-dialogue-act-classification
  sem:
  - dialogue-modeling
  - language-modeling
  - sentiment-classification
  swda:
  - dialogue-modeling
  - language-modeling
  - text-classification-other-dialogue-act-classification
---

# Dataset Card for SILICONE Benchmark

## Table of Contents
- [Benchmark Description](#benchmark-description)
  - [Benchmark Summary](#benchmark-summary)
  - [Languages](#languages)
- [Benchmark Structure](#dataset-structure)
  - [Dataset Instances](#data-instances)
  - [Data Fields](#data-fields)
  - [Data Splits](#data-splits)
- [Additional Information](#additional-information)
  - [Dataset Curators](#dataset-curators)
  - [Licensing Information](#licensing-information)
  - [Citation Information](#citation-information)

## Benchmark Description

<!-- - **Homepage:** -->
- **Repository:** https://github.com/eusip/SILICONE-benchmark
- **Paper:** https://arxiv.org/abs/2009.11152
- **Point of Contact:** Ebenge Usip, ebenge.usip@telecom-paris.fr
<!-- - **Leaderboard:** -->

### Benchmark Summary

The Sequence labellIng evaLuatIon benChmark fOr spoken laNguagE (SILICONE) benchmark is a collection of resources for training, evaluating, and analyzing natural language understanding systems specifically designed for spoken language. All datasets are in the English language and covers a variety of domains including daily life, scripted scenarios, joint task completion, phone call conversations, and televsion dialogue. Some datasets additionally include emotion and/or sentimant labels.

<!--
-- ### Supported Tasks and Leaderboards

[More Information Needed]
-->

### Languages

English.

## Benchmark Structure

### Dataset Instances

#### DailyDialog Act Corpus (Dialogue Act)
For the `dyda_da` configuration one example from the dataset is:
```
{
  'Utterance': "the taxi drivers are on strike again .",
  'Dialogue_Act': 2, # inform
  'Dialogue_ID': 2
}
```

#### DailyDialog Act Corpus (Emotion)
For the `dyda_e` configuration one example from the dataset is:
```
{
  'Utterance': "'oh , breaktime flies .'",
  'Emotion': 5, # sadness
  'Dialogue_ID': 997
}
```

#### Interactive Emotional Dyadic Motion Capture (IEMOCAP) database
For the `iemocap` configuration one example from the dataset is:
```
{
  'Dialogue_ID': Ses04F_script03_2,
  'Utterance_ID': Ses04F_script03_2_F025,
  'Utterance': "You're quite insufferable.  I expect it's because you're drunk.",
  'Emotion': 0, # ang
}
```

#### HCRC MapTask Corpus
For the `maptask` configuration one example from the dataset is:
```
{
  'Speaker': f,
  'Utterance': "i think that would bring me over the crevasse",
  'Dialogue_Act': 4, # explain
}
```


#### Multimodal EmotionLines Dataset (Emotion)
For the `meld_e` configuration one example from the dataset is:
```
{
  'Utterance': "'Push 'em out , push 'em out , harder , harder .'",
  'Speaker': Joey,
  'Emotion': 3, # joy
  'Dialogue_ID': 1,
  'Utterance_ID': 2
}
```

#### Multimodal EmotionLines Dataset (Sentiment)
For the `meld_s` configuration one example from the dataset is:
```
{
  'Utterance': "'Okay , y'know what ? There is no more left , left !'",
  'Speaker': Rachel,
  'Sentiment': 0, # negative
  'Dialogue_ID': 2,
  'Utterance_ID': 4
}
```

#### ICSI MRDA Corpus
For the `mrda` configuration one example from the dataset is:
```
{
  'Utterance_ID': Bed006-c2_0073656_0076706,
  'Dialogue_Act': 0, # s
  'Channel_ID': Bed006-c2,
  'Speaker': mn015,
  'Dialogue_ID': Bed006,
  'Utterance': "keith is not technically one of us yet ."
}
```

#### BT OASIS Corpus
For the `oasis` configuration one example from the dataset is:
```
{
  'Speaker': b,
  'Utterance': "when i rang up um when i rang to find out why she said oh well your card's been declined",
  'Dialogue_Act': 21, # inform
}
```

#### SEMAINE database
For the `sem` configuration one example from the dataset is:
```
{
  'Utterance': "can you think of somebody who is like that ?",
  'NbPairInSession': 11,
  'Dialogue_ID': 59,
  'SpeechTurn': 674,
  'Speaker': Agent,
  'Sentiment': 1, # Neutral
}
```

#### Switchboard Dialog Act (SwDA) Corpus
For the `swda` configuration one example from the dataset is:
```
{
  'Utterance': "but i 'd probably say that 's roughly right .",
  'Dialogue_Act': 33, # aap_am
  'From_Caller': 1255,
  'To_Caller': 1087,
  'Topic': CRIME,
  'Dialogue_ID': 818,
  'Conv_ID': sw2836,
}
```

### Data Fields

All data fields are formatted as `string` features.

### Data Splits

| Dataset name | Train  | Valid | Test  |
| ------------ | -----  | ----- | ----  |
| dyda_da      | 87170  | 8069  | 7740  |
| dyda_e       | 87170  | 8069  | 7740  |
| iemocap      | 7213   | 805   | 2021  |
| maptask      | 20905  | 2963  | 2894  |
| meld_e       | 9989   | 1109  | 2610  |
| meld_s       | 9989   | 1109  | 2610  |
| mrda         | 83944  | 9815  | 15470 |
| oasis        | 12076  | 1513  | 1478  |
| sem          | 4264   | 485   | 878   |
| swda         | 190709 | 21203 | 2714  |

<!--
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
-->

## Additional Information

### Benchmark Curators

Emile Chapuis, Pierre Colombo, Ebenge Usip.

### Licensing Information

This work is licensed under a [Creative Commons Attribution-NonCommercial-ShareAlike 4.0 Unported License](https://creativecommons.org/licenses/by-sa/4.0/).

### Citation Information

```
@inproceedings{chapuis-etal-2020-hierarchical,
    title = "Hierarchical Pre-training for Sequence Labelling in Spoken Dialog",
    author = "Chapuis, Emile  and
      Colombo, Pierre  and
      Manica, Matteo  and
      Labeau, Matthieu  and
      Clavel, Chlo{\'e}",
    booktitle = "Findings of the Association for Computational Linguistics: EMNLP 2020",
    month = nov,
    year = "2020",
    address = "Online",
    publisher = "Association for Computational Linguistics",
    url = "https://www.aclweb.org/anthology/2020.findings-emnlp.239",
    doi = "10.18653/v1/2020.findings-emnlp.239",
    pages = "2636--2648",
    abstract = "Sequence labelling tasks like Dialog Act and Emotion/Sentiment identification are a key component of spoken dialog systems. In this work, we propose a new approach to learn generic representations adapted to spoken dialog, which we evaluate on a new benchmark we call Sequence labellIng evaLuatIon benChmark fOr spoken laNguagE benchmark (SILICONE). SILICONE is model-agnostic and contains 10 different datasets of various sizes. We obtain our representations with a hierarchical encoder based on transformer architectures, for which we extend two well-known pre-training objectives. Pre-training is performed on OpenSubtitles: a large corpus of spoken dialog containing over 2.3 billion of tokens. We demonstrate how hierarchical encoders achieve competitive results with consistently fewer parameters compared to state-of-the-art models and we show their importance for both pre-training and fine-tuning.",
}
```