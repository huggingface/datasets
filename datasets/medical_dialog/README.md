---
annotations_creators:
- found
language_creators:
- expert-generated
- found
languages:
- en
- zh
licenses:
- unknown
multilinguality:
- monolingual
size_categories:
- 1M<n<10M
source_datasets:
- original
task_categories:
- question-answering
task_ids:
- closed-domain-qa
paperswithcode_id: null
pretty_name: MedDialog
configs:
- en
- zh
---

# Dataset Card for MedDialog

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

[//]: # (- **Homepage:** )
- **Repository:** https://github.com/UCSD-AI4H/Medical-Dialogue-System
- **Paper:** [MedDialog: Two Large-scale Medical Dialogue Datasets](https://arxiv.org/abs/2004.03329)
[//]: # (- **Leaderboard:** )
[//]: # (- **Point of Contact:** )

### Dataset Summary

The MedDialog dataset (Chinese) contains conversations (in Chinese) between doctors and patients. It has 1.1 million dialogues and 4 million utterances. The data is continuously growing and more dialogues will be added. The raw dialogues are from haodf.com. All copyrights of the data belong to haodf.com.

The MedDialog dataset (English) contains conversations (in English) between doctors and patients. It has 0.26 million dialogues. The data is continuously growing and more dialogues will be added. The raw dialogues are from healthcaremagic.com and icliniq.com. All copyrights of the data belong to healthcaremagic.com and icliniq.com.

Directions for using the pre-trained model using BERT using PyTorch is available in the Homepage.


### Supported Tasks and Leaderboards

Closed domain qa

### Languages

Monolingual. The datasets are in English (EN) and Chinese (ZH)

## Dataset Structure

### Data Instances

There are 4 configurations:
- Raw data:
  - en
  - zh
- Processed data:
  - processed.en
  - processed.zh

#### en

Each consultation consists of the below:
- ID
- URL
- Description of patient’s medical condition
- Dialogue

The dataset is built from [icliniq.com](https://www.icliniq.com/), [healthcaremagic.com](https://www.healthcaremagic.com/), [healthtap.com](https://www.healthtap.com/) and all copyrights of the data belong to these websites.

#### zh

Each consultation consists of the below:
- ID
- URL
- Description of patient’s medical condition
- Dialogue
- (Optional) Diagnosis and suggestions.

The dataset is built from [Haodf.com](https://www.haodf.com/) and all copyrights of the data belong to [Haodf.com](https://www.haodf.com/).

One example for chinese is

```
{
{'dialogue_id': 2,
  'dialogue_turns': [{'speaker': '病人',
    'utterance': '孩子哭闹时，鸡鸡旁边会肿起，情绪平静时肿块会消失，去一个私人诊所看过，说是疝气.如果确定是疝气，是不是一定要手术治疗？我孩子只有1岁10月，自愈的可能性大吗？如果一定要手术，这么小的孩子风险大吗？术后的恢复困难吗？谢谢.'},
   {'speaker': '医生', 'utterance': '南方医的B超说得不清楚，可能是鞘膜积液，可到我医院复查一个B超。'}],
  'dialogue_url': 'https://www.haodf.com/doctorteam/flow_team_6477251152.htm',
  'file_name': '2020.txt'},
}
```

#### processed.en
```
{
  'description': 'throat a bit sore and want to get a good imune booster, especially in light of the virus. please advise. have not been in contact with nyone with the virus.',
  'utterances': [
    'patient: throat a bit sore and want to get a good imune booster, especially in light of the virus. please advise. have not been in contact with nyone with the virus.',
    "doctor: during this pandemic. throat pain can be from a strep throat infection (antibiotics needed), a cold or influenza or other virus, or from some other cause such as allergies or irritants. usually, a person sees the doctor (call first) if the sore throat is bothersome, recurrent, or doesn't go away quickly. covid-19 infections tend to have cough, whereas strep throat usually lacks cough but has more throat pain. (3/21/20)"
  ]
}
```

#### processed.zh
```
{
  'utterances': [
    '病人：强制性脊柱炎，晚上睡觉翻身时腰骶骨区域疼痛，其他身体任何部位均不疼痛。', 
    '医生：应该没有问题，但最好把图像上传看看。'
  ]
}
```

### Data Fields

For generating the QA only the below fields have been considered:
- ID : Consultatation Identifier (restarts for each file)
- URL: The url link of the extracted conversation
- Dialogue : The conversation between the doctor and the patient.

These are arranged as below in the prepared dataset. Each item will be represented with these parameters.

- "file_name": string - signifies the file from which the conversation was extracted
- "dialogue_id": int32 - the dialogue id
- "dialogue_url": string - url of the conversation
- "dialogue_turns": datasets.Sequence - sequence of dialogues between patient and the doctor.Consists ClassLabel(names=["病人", "医生"]), and "utterance"(string) for each turn. (ClassLable(names=["Patient", "Doctor"]) for english)

#### processed.en
- `description` (str): Description of the dialog.
- `utterances` (list of str): Dialog utterances between patient and doctor.

#### processed.zh
- `utterances` (list of str): Dialog utterances between patient and doctor.

### Data Splits

There are no data splits on the original raw data. The "train" split for each language contains:
- en: 229674 examples
- zh: 1921127 examples

For processed configurations, data is split into train, validation and test, with the following number of examples:

|              |   train | validation |   test |
|--------------|--------:|-----------:|-------:|
| processed.en |     482 |         60 |     61 |
| processed.zh | 2725989 |     340748 | 340754 |

## Dataset Creation

### Curation Rationale

Medical dialogue systems are promising in assisting in telemedicine to increase access to healthcare services, improve the quality of patient care, and reduce medical costs. 

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

Unknow.

### Citation Information
```
@article{chen2020meddiag,
  title={MedDialog: a large-scale medical dialogue dataset},
  author={Chen, Shu and Ju, Zeqian and Dong, Xiangyu and Fang, Hongchao and Wang, Sicheng and Yang, Yue and Zeng, Jiaqi and Zhang, Ruisi and Zhang, Ruoyu and Zhou, Meng and Zhu, Penghui and Xie, Pengtao},
  journal={arXiv preprint arXiv:2004.03329}, 
  year={2020}
}
```

### Contributions

Thanks to [@vrindaprabhu](https://github.com/vrindaprabhu) for adding this dataset.