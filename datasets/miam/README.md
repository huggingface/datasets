---
annotations_creators:
- expert-generated
language_creators:
- expert-generated
language:
- de
- en
- es
- fr
- it
license:
- cc-by-sa-4.0
multilinguality:
- multilingual
size_categories:
- 10K<n<100K
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
- text-classification-other-dialogue-act-classification
paperswithcode_id: null
pretty_name: MIAM
configs:
- dihana
- ilisten
- loria
- maptask
- vm2
---

# Dataset Card for MIAM

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
- **Repository:** [N/A]
- **Paper:** [N/A]
- **Leaderboard:** [N/A]
- **Point of Contact:** [N/A]

### Dataset Summary

Multilingual dIalogAct benchMark is a collection of resources for training, evaluating, and
analyzing natural language understanding systems specifically designed for spoken language. Datasets
are in English, French, German, Italian and Spanish. They cover a variety of domains including
spontaneous speech, scripted scenarios, and joint task completion. All datasets contain dialogue act
labels.

### Supported Tasks and Leaderboards

[More Information Needed]

### Languages

English, French, German, Italian, Spanish.

## Dataset Structure

### Data Instances

#### Dihana Corpus
For the `dihana` configuration one example from the dataset is:
```
{
  'Speaker': 'U',
  'Utterance': 'Hola , quería obtener el horario para ir a Valencia',
  'Dialogue_Act': 9,  # 'Pregunta' ('Request')
  'Dialogue_ID': '0',
  'File_ID': 'B209_BA5c3',
}
```

#### iLISTEN Corpus
For the `ilisten` configuration one example from the dataset is:
```
{
  'Speaker': 'T_11_U11',
  'Utterance': 'ok, grazie per le informazioni',
  'Dialogue_Act': 6,  # 'KIND-ATTITUDE_SMALL-TALK'
  'Dialogue_ID': '0',
}
```

#### LORIA Corpus
For the `loria` configuration one example from the dataset is:
```
{
  'Speaker': 'Samir',
  'Utterance': 'Merci de votre visite, bonne chance, et à la prochaine !',
  'Dialogue_Act': 21,  # 'quit'
  'Dialogue_ID': '5',
  'File_ID': 'Dial_20111128_113927',
}
```

#### HCRC MapTask Corpus
For the `maptask` configuration one example from the dataset is:
```
{
  'Speaker': 'f',
  'Utterance': 'is it underneath the rope bridge or to the left',
  'Dialogue_Act': 6,  # 'query_w'
  'Dialogue_ID': '0',
  'File_ID': 'q4ec1',
}
```

#### VERBMOBIL
For the `vm2` configuration one example from the dataset is:
```
{
  'Utterance': 'ja was sind viereinhalb Stunden Bahngerüttel gegen siebzig Minuten Turbulenzen im Flugzeug',
  'Utterance': 'Utterance',
  'Dialogue_Act': 'Dialogue_Act',  # 'INFORM'
  'Speaker': 'A',
  'Dialogue_ID': '66',
}
```

### Data Fields

For the `dihana` configuration, the different fields are:
- `Speaker`: identifier of the speaker as a string.
- `Utterance`: Utterance as a string.
- `Dialogue_Act`: Dialog act label of the utterance. It can be one of 'Afirmacion' (0) [Feedback_positive], 'Apertura' (1) [Opening], 'Cierre' (2) [Closing], 'Confirmacion' (3) [Acknowledge], 'Espera' (4) [Hold], 'Indefinida' (5) [Undefined], 'Negacion' (6) [Feedback_negative], 'No_entendido' (7) [Request_clarify], 'Nueva_consulta' (8) [New_request], 'Pregunta' (9) [Request] or 'Respuesta' (10) [Reply].
- `Dialogue_ID`: identifier of the dialogue as a string.
- `File_ID`: identifier of the source file as a string.

For the `ilisten` configuration, the different fields are:
- `Speaker`: identifier of the speaker as a string.
- `Utterance`: Utterance as a string.
- `Dialogue_Act`: Dialog act label of the utterance. It can be one of 'AGREE' (0), 'ANSWER' (1), 'CLOSING' (2), 'ENCOURAGE-SORRY' (3), 'GENERIC-ANSWER' (4), 'INFO-REQUEST' (5), 'KIND-ATTITUDE_SMALL-TALK' (6), 'OFFER-GIVE-INFO' (7), 'OPENING' (8), 'PERSUASION-SUGGEST' (9), 'QUESTION' (10), 'REJECT' (11), 'SOLICITATION-REQ_CLARIFICATION' (12), 'STATEMENT' (13) or 'TALK-ABOUT-SELF' (14).
- `Dialogue_ID`: identifier of the dialogue as a string.

For the `loria` configuration, the different fields are:
- `Speaker`: identifier of the speaker as a string.
- `Utterance`: Utterance as a string.
- `Dialogue_Act`: Dialog act label of the utterance. It can be one of 'ack' (0), 'ask' (1), 'find_mold' (2), 'find_plans' (3), 'first_step' (4), 'greet' (5), 'help' (6), 'inform' (7), 'inform_engine' (8), 'inform_job' (9), 'inform_material_space' (10), 'informer_conditioner' (11), 'informer_decoration' (12), 'informer_elcomps' (13), 'informer_end_manufacturing' (14), 'kindAtt' (15), 'manufacturing_reqs' (16), 'next_step' (17), 'no' (18), 'other' (19), 'quality_control' (20), 'quit' (21), 'reqRep' (22), 'security_policies' (23), 'staff_enterprise' (24), 'staff_job' (25), 'studies_enterprise' (26), 'studies_job' (27), 'todo_failure' (28), 'todo_irreparable' (29), 'yes' (30)
- `Dialogue_ID`: identifier of the dialogue as a string.
- `File_ID`: identifier of the source file as a string.

For the `maptask` configuration, the different fields are:
- `Speaker`: identifier of the speaker as a string.
- `Utterance`: Utterance as a string.
- `Dialogue_Act`: Dialog act label of the utterance. It can be one of 'acknowledge' (0), 'align' (1), 'check' (2), 'clarify' (3), 'explain' (4), 'instruct' (5), 'query_w' (6), 'query_yn' (7), 'ready' (8), 'reply_n' (9), 'reply_w' (10) or 'reply_y' (11).
- `Dialogue_ID`: identifier of the dialogue as a string.
- `File_ID`: identifier of the source file as a string.

For the `vm2` configuration, the different fields are:
- `Utterance`: Utterance as a string.
- `Dialogue_Act`: Dialogue act label of the utterance. It can be one of 'ACCEPT' (0), 'BACKCHANNEL' (1), 'BYE' (2), 'CLARIFY' (3), 'CLOSE' (4), 'COMMIT' (5), 'CONFIRM' (6), 'DEFER' (7), 'DELIBERATE' (8), 'DEVIATE_SCENARIO' (9), 'EXCLUDE' (10), 'EXPLAINED_REJECT' (11), 'FEEDBACK' (12), 'FEEDBACK_NEGATIVE' (13), 'FEEDBACK_POSITIVE' (14), 'GIVE_REASON' (15), 'GREET' (16), 'INFORM' (17), 'INIT' (18), 'INTRODUCE' (19), 'NOT_CLASSIFIABLE' (20), 'OFFER' (21), 'POLITENESS_FORMULA' (22), 'REJECT' (23), 'REQUEST' (24), 'REQUEST_CLARIFY' (25), 'REQUEST_COMMENT' (26), 'REQUEST_COMMIT' (27), 'REQUEST_SUGGEST' (28), 'SUGGEST' (29), 'THANK' (30).
- `Speaker`: Speaker as a string.
- `Dialogue_ID`: identifier of the dialogue as a string.

### Data Splits

| Dataset name | Train | Valid | Test |
| ------------ | ----- | ----- | ---- |
| dihana       | 19063 | 2123  | 2361 |
| ilisten      | 1986  | 230   | 971  |
| loria        | 8465  | 942   | 1047 |
| maptask      | 25382 | 5221  | 5335 |
| vm2          | 25060 | 2860  | 2855 |

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

Anonymous.

### Licensing Information

This work is licensed under a [Creative Commons Attribution-NonCommercial-ShareAlike 4.0 Unported License](https://creativecommons.org/licenses/by-sa/4.0/).

### Citation Information

```
@inproceedings{colombo-etal-2021-code,
    title = "Code-switched inspired losses for spoken dialog representations",
    author = "Colombo, Pierre  and
      Chapuis, Emile  and
      Labeau, Matthieu  and
      Clavel, Chlo{\'e}",
    booktitle = "Proceedings of the 2021 Conference on Empirical Methods in Natural Language Processing",
    month = nov,
    year = "2021",
    address = "Online and Punta Cana, Dominican Republic",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/2021.emnlp-main.656",
    doi = "10.18653/v1/2021.emnlp-main.656",
    pages = "8320--8337",
    abstract = "Spoken dialogue systems need to be able to handle both multiple languages and multilinguality inside a conversation (\textit{e.g} in case of code-switching). In this work, we introduce new pretraining losses tailored to learn generic multilingual spoken dialogue representations. The goal of these losses is to expose the model to code-switched language. In order to scale up training, we automatically build a pretraining corpus composed of multilingual conversations in five different languages (French, Italian, English, German and Spanish) from OpenSubtitles, a huge multilingual corpus composed of 24.3G tokens. We test the generic representations on MIAM, a new benchmark composed of five dialogue act corpora on the same aforementioned languages as well as on two novel multilingual tasks (\textit{i.e} multilingual mask utterance retrieval and multilingual inconsistency identification). Our experiments show that our new losses achieve a better performance in both monolingual and multilingual settings.",
}
```

### Contributions

Thanks to [@eusip](https://github.com/eusip) and [@PierreColombo](https://github.com/PierreColombo) for adding this dataset.
