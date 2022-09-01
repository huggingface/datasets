---
annotations_creators:
- expert-generated
language_creators:
- expert-generated
language:
- en
license:
- cc-by-sa-4.0
multilinguality:
- monolingual
size_categories:
- 100K<n<1M
- 10K<n<100K
- 1K<n<10K
source_datasets:
- original
task_categories:
- text-generation
- fill-mask
- text-classification
task_ids:
- dialogue-modeling
- language-modeling
- masked-language-modeling
- sentiment-classification
- text-classification-other-dialogue-act-classification
- text-classification-other-emotion-classification
- text-scoring
paperswithcode_id: null
pretty_name: SILICONE Benchmark
configs:
- dyda_da
- dyda_e
- iemocap
- maptask
- meld_e
- meld_s
- mrda
- oasis
- sem
- swda
---

# Dataset Card for SILICONE Benchmark

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

- **Homepage:** [N/A]
- **Repository:** https://github.com/eusip/SILICONE-benchmark
- **Paper:** https://arxiv.org/abs/2009.11152
- **Leaderboard:** [N/A]
- **Point of Contact:** [Ebenge Usip](ebenge.usip@telecom-paris.fr)

### Dataset Summary

The Sequence labellIng evaLuatIon benChmark fOr spoken laNguagE (SILICONE) benchmark is a collection of resources for training, evaluating, and analyzing natural language understanding systems specifically designed for spoken language. All datasets are in the English language and covers a variety of domains including daily life, scripted scenarios, joint task completion, phone call conversations, and televsion dialogue. Some datasets additionally include emotion and/or sentimant labels.

### Supported Tasks and Leaderboards

[More Information Needed]

### Languages

English.

## Dataset Structure

### Data Instances

#### DailyDialog Act Corpus (Dialogue Act)
For the `dyda_da` configuration one example from the dataset is:
```
{
  'Utterance': "the taxi drivers are on strike again .",
  'Dialogue_Act': 2, # "inform"
  'Dialogue_ID': "2"
}
```

#### DailyDialog Act Corpus (Emotion)
For the `dyda_e` configuration one example from the dataset is:
```
{
  'Utterance': "'oh , breaktime flies .'",
  'Emotion': 5, # "sadness"
  'Dialogue_ID': "997"
}
```

#### Interactive Emotional Dyadic Motion Capture (IEMOCAP) database
For the `iemocap` configuration one example from the dataset is:
```
{
  'Dialogue_ID': "Ses04F_script03_2",
  'Utterance_ID': "Ses04F_script03_2_F025",
  'Utterance': "You're quite insufferable.  I expect it's because you're drunk.",
  'Emotion': 0, # "ang"
}
```

#### HCRC MapTask Corpus
For the `maptask` configuration one example from the dataset is:
```
{
  'Speaker': "f",
  'Utterance': "i think that would bring me over the crevasse",
  'Dialogue_Act': 4, # "explain"
}
```


#### Multimodal EmotionLines Dataset (Emotion)
For the `meld_e` configuration one example from the dataset is:
```
{
  'Utterance': "'Push 'em out , push 'em out , harder , harder .'",
  'Speaker': "Joey",
  'Emotion': 3, # "joy"
  'Dialogue_ID': "1",
  'Utterance_ID': "2"
}
```

#### Multimodal EmotionLines Dataset (Sentiment)
For the `meld_s` configuration one example from the dataset is:
```
{
  'Utterance': "'Okay , y'know what ? There is no more left , left !'",
  'Speaker': "Rachel",
  'Sentiment': 0, # "negative"
  'Dialogue_ID': "2",
  'Utterance_ID': "4"
}
```

#### ICSI MRDA Corpus
For the `mrda` configuration one example from the dataset is:
```
{
  'Utterance_ID': "Bed006-c2_0073656_0076706",
  'Dialogue_Act': 0, # "s"
  'Channel_ID': "Bed006-c2",
  'Speaker': "mn015",
  'Dialogue_ID': "Bed006",
  'Utterance': "keith is not technically one of us yet ."
}
```

#### BT OASIS Corpus
For the `oasis` configuration one example from the dataset is:
```
{
  'Speaker': "b",
  'Utterance': "when i rang up um when i rang to find out why she said oh well your card's been declined",
  'Dialogue_Act': 21, # "inform"
}
```

#### SEMAINE database
For the `sem` configuration one example from the dataset is:
```
{
  'Utterance': "can you think of somebody who is like that ?",
  'NbPairInSession': "11",
  'Dialogue_ID': "59",
  'SpeechTurn': "674",
  'Speaker': "Agent",
  'Sentiment': 1, # "Neutral"
}
```

#### Switchboard Dialog Act (SwDA) Corpus
For the `swda` configuration one example from the dataset is:
```
{
  'Utterance': "but i 'd probably say that 's roughly right .",
  'Dialogue_Act': 33, # "aap_am"
  'From_Caller': "1255",
  'To_Caller': "1087",
  'Topic': "CRIME",
  'Dialogue_ID': "818",
  'Conv_ID': "sw2836",
}
```

### Data Fields

For the `dyda_da` configuration, the different fields are:
- `Utterance`: Utterance as a string.
- `Dialogue_Act`: Dialog act label of the utterance. It can be one of "commissive" (0), "directive" (1), "inform" (2) or "question" (3).
- `Dialogue_ID`: identifier of the dialogue as a string.

For the `dyda_e` configuration, the different fields are:
- `Utterance`: Utterance as a string.
- `Dialogue_Act`: Dialog act label of the utterance. It can be one of "anger" (0), "disgust" (1), "fear" (2), "happiness" (3), "no emotion" (4), "sadness" (5) or "surprise" (6).
- `Dialogue_ID`: identifier of the dialogue as a string.

For the `iemocap` configuration, the different fields are:
- `Dialogue_ID`: identifier of the dialogue as a string.
- `Utterance_ID`: identifier of the utterance as a string.
- `Utterance`: Utterance as a string.
- `Emotion`: Emotion label of the utterance. It can be one of "Anger" (0), "Disgust" (1), "Excitement" (2), "Fear" (3), "Frustration" (4), "Happiness" (5), "Neutral" (6), "Other" (7), "Sadness" (8), "Surprise" (9) or "Unknown" (10).

For the `maptask` configuration, the different fields are:
- `Speaker`: identifier of the speaker as a string.
- `Utterance`: Utterance as a string.
- `Dialogue_Act`: Dialog act label of the utterance. It can be one of "acknowledge" (0), "align" (1), "check" (2), "clarify" (3), "explain" (4), "instruct" (5), "query_w" (6), "query_yn" (7), "ready" (8), "reply_n" (9), "reply_w" (10) or "reply_y" (11).

For the `meld_e` configuration, the different fields are:
- `Utterance`: Utterance as a string.
- `Speaker`: Speaker as a string.
- `Emotion`: Emotion label of the utterance. It can be one of "anger" (0), "disgust" (1), "fear" (2), "joy" (3), "neutral" (4), "sadness" (5) or "surprise" (6).
- `Dialogue_ID`: identifier of the dialogue as a string.
- `Utterance_ID`: identifier of the utterance as a string.

For the `meld_s` configuration, the different fields are:
- `Utterance`: Utterance as a string.
- `Speaker`: Speaker as a string.
- `Sentiment`: Sentiment label of the utterance. It can be one of "negative" (0), "neutral" (1) or "positive" (2).
- `Dialogue_ID`: identifier of the dialogue as a string.
- `Utterance_ID`: identifier of the utterance as a string.

For the `mrda` configuration, the different fields are:
- `Utterance_ID`: identifier of the utterance as a string.
- `Dialogue_Act`: Dialog act label of the utterance. It can be one of "s" (0) [Statement/Subjective Statement], "d" (1) [Declarative Question], "b" (2) [Backchannel], "f" (3) [Follow-me] or "q" (4) [Question].
- `Channel_ID`: identifier of the channel as a string.
- `Speaker`: identifier of the speaker as a string.
- `Dialogue_ID`: identifier of the channel as a string.
- `Utterance`: Utterance as a string.

For the `oasis` configuration, the different fields are:
- `Speaker`: identifier of the speaker as a string.
- `Utterance`: Utterance as a string.
- `Dialogue_Act`: Dialog act label of the utterance. It can be one of "accept" (0), "ackn" (1), "answ" (2), "answElab" (3), "appreciate" (4), "backch" (5), "bye" (6), "complete" (7), "confirm" (8), "correct" (9), "direct" (10), "directElab" (11), "echo" (12), "exclaim" (13), "expressOpinion"(14), "expressPossibility" (15), "expressRegret" (16), "expressWish" (17), "greet" (18), "hold" (19),
"identifySelf" (20), "inform" (21), "informCont" (22), "informDisc" (23), "informIntent" (24), "init" (25), "negate" (26), "offer" (27), "pardon" (28), "raiseIssue" (29), "refer" (30), "refuse" (31), "reqDirect" (32), "reqInfo" (33), "reqModal" (34), "selfTalk" (35), "suggest" (36), "thank" (37), "informIntent-hold" (38), "correctSelf" (39), "expressRegret-inform" (40) or "thank-identifySelf" (41).

For the `sem` configuration, the different fields are:
- `Utterance`: Utterance as a string.
- `NbPairInSession`: number of utterance pairs in a dialogue.
- `Dialogue_ID`: identifier of the dialogue as a string.
- `SpeechTurn`: SpeakerTurn as a string.
- `Speaker`: Speaker as a string.
- `Sentiment`: Sentiment label of the utterance. It can be "Negative", "Neutral" or "Positive".

For the `swda` configuration, the different fields are:
`Utterance`: Utterance as a string.
`Dialogue_Act`: Dialogue act label of the utterance. It can be "sd" (0) [Statement-non-opinion], "b" (1) [Acknowledge (Backchannel)], "sv" (2) [Statement-opinion], "%" (3) [Uninterpretable], "aa" (4) [Agree/Accept], "ba" (5) [Appreciation], "fc" (6) [Conventional-closing], "qw" (7) [Wh-Question], "nn" (8) [No Answers], "bk" (9) [Response Acknowledgement], "h" (10) [Hedge], "qy^d" (11) [Declarative Yes-No-Question], "bh" (12) [Backchannel in Question Form], "^q" (13) [Quotation], "bf" (14) [Summarize/Reformulate], 'fo_o_fw_"_by_bc' (15) [Other], 'fo_o_fw_by_bc_"' (16) [Other], "na" (17) [Affirmative Non-yes Answers], "ad" (18) [Action-directive], "^2" (19) [Collaborative Completion], "b^m" (20) [Repeat-phrase], "qo" (21) [Open-Question], "qh" (22) [Rhetorical-Question], "^h" (23) [Hold Before Answer/Agreement], "ar" (24) [Reject], "ng" (25) [Negative Non-no Answers], "br" (26) [Signal-non-understanding], "no" (27) [Other Answers], "fp" (28) [Conventional-opening], "qrr" (29) [Or-Clause], "arp_nd" (30) [Dispreferred Answers], "t3" (31) [3rd-party-talk], "oo_co_cc" (32) [Offers, Options Commits], "aap_am" (33) [Maybe/Accept-part], "t1" (34) [Downplayer], "bd" (35) [Self-talk], "^g" (36) [Tag-Question], "qw^d" (37) [Declarative Wh-Question], "fa" (38) [Apology], "ft" (39) [Thanking], "+" (40) [Unknown], "x" (41) [Unknown], "ny" (42) [Unknown], "sv_fx" (43) [Unknown], "qy_qr" (44) [Unknown] or "ba_fe" (45) [Unknown].
`From_Caller`: identifier of the from caller as a string.
`To_Caller`: identifier of the to caller as a string.
`Topic`: Topic as a string.
`Dialogue_ID`: identifier of the dialogue as a string.
`Conv_ID`: identifier of the conversation as a string.

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

### Contributions

Thanks to [@eusip](https://github.com/eusip) and [@lhoestq](https://github.com/lhoestq) for adding this dataset.