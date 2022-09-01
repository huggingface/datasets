---
annotations_creators:
- no-annotation
language_creators:
- expert-generated
language:
- en
license:
- apache-2.0
multilinguality:
- monolingual
size_categories:
- 100K<n<1M
source_datasets:
- original
task_categories:
- question-answering
- multiple-choice
task_ids:
- multiple-choice-qa
- open-domain-qa
paperswithcode_id: medmcqa
pretty_name: MedMCQA
---

# Dataset Card for MedMCQA

## Table of Contents
- [Dataset Description](#dataset-description)
  - [Dataset Summary](#dataset-summary)
  - [Supported Tasks](#supported-tasks-and-leaderboards)
  - [Languages](#languages)
- [Dataset Structure](#dataset-structure)
  - [Data Instances](#data-instances)
  - [Data Fields](#data-instances)
  - [Data Splits](#data-instances)
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

## Dataset Description

- **Homepage:** https://medmcqa.github.io
- **Repository:** https://github.com/medmcqa/medmcqa
- **Paper:** https://arxiv.org/abs/2203.14371
- **Leaderboard:** https://paperswithcode.com/dataset/medmcqa
- **Point of Contact:** [Aaditya Ura](mailto:aadityaura@gmail.com)

### Dataset Summary

MedMCQA is a large-scale, Multiple-Choice Question Answering (MCQA) dataset designed to address real-world medical entrance exam questions.

MedMCQA has more than 194k high-quality AIIMS & NEET PG entrance exam MCQs covering 2.4k healthcare topics and 21 medical subjects are collected with an average token length of 12.77 and high topical diversity.

Each sample contains a question, correct answer(s), and other options which require a deeper language understanding as it tests the 10+ reasoning abilities of a model across a wide range of medical subjects & topics. A detailed explanation of the solution, along with the above information, is provided in this study.

MedMCQA provides an open-source dataset for the Natural Language Processing community.
It is expected that this dataset would facilitate future research toward achieving better QA systems.
The dataset contains questions about the following topics:

- Anesthesia
- Anatomy
- Biochemistry
- Dental
- ENT
- Forensic Medicine (FM)
- Obstetrics and Gynecology (O&G)
- Medicine
- Microbiology
- Ophthalmology
- Orthopedics
- Pathology
- Pediatrics
- Pharmacology
- Physiology
- Psychiatry
- Radiology
- Skin
- Preventive & Social Medicine (PSM)
- Surgery

### Supported Tasks and Leaderboards

multiple-choice-QA, open-domain-QA: The dataset can be used to train a model for multi-choice questions answering, open domain questions answering. Questions in these exams are challenging and generally require deeper domain and language understanding as it tests the 10+ reasoning abilities across a wide range of medical subjects & topics.

### Languages

The questions and answers are available in English.

## Dataset Structure

### Data Instances

```
{
    "question":"A 40-year-old man presents with 5 days of productive cough and fever. Pseudomonas aeruginosa is isolated from a pulmonary abscess. CBC shows an acute effect characterized by marked leukocytosis (50,000 mL) and the differential count reveals a shift to left in granulocytes. Which of the following terms best describes these hematologic findings?",
    "exp": "Circulating levels of leukocytes and their precursors may occasionally reach very high levels (>50,000 WBC mL). These extreme elevations are sometimes called leukemoid reactions because they are similar to the white cell counts observed in leukemia, from which they must be distinguished. The leukocytosis occurs initially because of the accelerated release of granulocytes from the bone marrow (caused by cytokines, including TNF and IL-1) There is a rise in the number of both mature and immature neutrophils in the blood, referred to as a shift to the left. In contrast to bacterial infections, viral infections (including infectious mononucleosis) are characterized by lymphocytosis Parasitic infestations and certain allergic reactions cause eosinophilia, an increase in the number of circulating eosinophils. Leukopenia is defined as an absolute decrease in the circulating WBC count.",
    "cop":1,
    "opa":"Leukemoid reaction",
    "opb":"Leukopenia",
    "opc":"Myeloid metaplasia",
    "opd":"Neutrophilia",
    "subject_name":"Pathology",
    "topic_name":"Basic Concepts and Vascular changes of Acute Inflammation",
    "id":"4e1715fe-0bc3-494e-b6eb-2d4617245aef",
    "choice_type":"single"
}
```
### Data Fields

- `id` : a string question identifier for each example
- `question` : question text (a string)
- `opa` : Option A
- `opb` : Option B
- `opc` : Option C
- `opd` : Option D
- `cop` : Correct option, i.e., 1,2,3,4
- `choice_type` ({"single", "multi"}): Question choice type.
  - "single": Single-choice question, where each choice contains a single option.
  - "multi": Multi-choice question, where each choice contains a combination of multiple suboptions.
- `exp` : Expert's explanation of the answer
- `subject_name` : Medical Subject name of the particular question
- `topic_name` : Medical topic name from the particular subject

### Data Splits

The goal of MedMCQA is to emulate the rigor of real word medical exams. To enable that, a predefined split of the dataset is provided. The split is by exams instead of the given questions. This also ensures the reusability and generalization ability of the models. 

The training set of MedMCQA consists of all the collected mock & online test series, whereas the test set consists of all AIIMS PG exam MCQs (years 1991-present). The development set consists of NEET PG exam MCQs (years 2001-present) to approximate real exam evaluation.

Similar questions from train , test and dev set were removed based on similarity. The final split sizes are as follow:

|                             | Train   | Test | Valid |
| -----                       | ------ | ----- | ---- |
| Question #| 182,822 |  6,150 | 4,183|
| Vocab       | 94,231 |  11,218 | 10,800 |
| Max Ques tokens    | 220  |  135| 88 |
| Max Ans tokens | 38 | 21 | 25 |

## Dataset Creation

### Curation Rationale

Before this attempt, very few works have been done to construct biomedical MCQA datasets (Vilares and Gomez-Rodr, 2019), and they are (1) mostly small, containing up to few thousand questions, and (2) cover a limited number of Medical topics and Subjects. This paper addresses the aforementioned limitations by introducing MedMCQA, a new large-scale, Multiple-Choice Question Answering
(MCQA) dataset designed to address real-world medical entrance exam questions.

### Source Data

#### Initial Data Collection and Normalization

Historical Exam questions from official websites - AIIMS & NEET PG (1991- present)
The raw data is collected from open websites and books


#### Who are the source language producers?

The dataset was created by Ankit Pal, Logesh Kumar Umapathi and Malaikannan Sankarasubbu

### Annotations

#### Annotation process

The dataset does not contain any additional annotations.



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

If you find this useful in your research, please consider citing the dataset paper 

```
@InProceedings{pmlr-v174-pal22a,
  title = 	 {MedMCQA: A Large-scale Multi-Subject Multi-Choice Dataset for Medical domain Question Answering},
  author =       {Pal, Ankit and Umapathi, Logesh Kumar and Sankarasubbu, Malaikannan},
  booktitle = 	 {Proceedings of the Conference on Health, Inference, and Learning},
  pages = 	 {248--260},
  year = 	 {2022},
  editor = 	 {Flores, Gerardo and Chen, George H and Pollard, Tom and Ho, Joyce C and Naumann, Tristan},
  volume = 	 {174},
  series = 	 {Proceedings of Machine Learning Research},
  month = 	 {07--08 Apr},
  publisher =    {PMLR},
  pdf = 	 {https://proceedings.mlr.press/v174/pal22a/pal22a.pdf},
  url = 	 {https://proceedings.mlr.press/v174/pal22a.html},
  abstract = 	 {This paper introduces MedMCQA, a new large-scale, Multiple-Choice Question Answering (MCQA) dataset designed to address real-world medical entrance exam questions. More than 194k high-quality AIIMS &amp; NEET PG entrance exam MCQs covering 2.4k healthcare topics and 21 medical subjects are collected with an average token length of 12.77 and high topical diversity. Each sample contains a question, correct answer(s), and other options which requires a deeper language understanding as it tests the 10+ reasoning abilities of a model across a wide range of medical subjects &amp; topics. A detailed explanation of the solution, along with the above information, is provided in this study.}
}
```

### Contributions

Thanks to [@monk1337](https://github.com/monk1337) for adding this dataset.
