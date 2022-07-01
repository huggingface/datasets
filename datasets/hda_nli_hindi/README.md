---
annotations_creators:
- machine-generated
language_creators:
- found
language:
- hi
license:
- mit
multilinguality:
- monolingual
size_categories:
- 10K<n<100K
source_datasets:
- extended|hindi_discourse
task_categories:
- text-classification
task_ids:
- natural-language-inference
paperswithcode_id: null
pretty_name: Hindi Discourse Analysis Dataset
---

# Dataset Card for Hindi Discourse Analysis Dataset

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

- **HomePage:** [GitHub](https://github.com/midas-research/hindi-nli-data)
- **Paper:** [Aclweb](https://www.aclweb.org/anthology/2020.aacl-main.71)
- **Point of Contact:** [GitHub](https://github.com/midas-research/hindi-nli-data)

### Dataset Summary

- Dataset for Natural Language Inference in Hindi Language. Hindi Discourse Analysis (HDA) Dataset consists of textual-entailment pairs.
- Each row of the Datasets if made up of 4 columns - Premise, Hypothesis, Label and Topic.
- Premise and Hypothesis is written in Hindi while Entailment_Label is in English.
- Entailment_label is of 2 types - entailed and not-entailed.
- Entailed means that hypotheis can be inferred from premise and not-entailed means vice versa
- Dataset can be used to train models for Natural Language Inference tasks in Hindi Language.

### Supported Tasks and Leaderboards

- Natural Language Inference for Hindi

### Languages

- Dataset is in Hindi

## Dataset Structure

- Data is structured in TSV format. 
- train, test and dev files are in seperate files


### Dataset Instances

An example of 'train' looks as follows.

```
{'hypothesis': 'यह एक वर्णनात्मक कथन है।', 'label': 1, 'premise': 'जैसे उस का सारा चेहरा अपना हो और आँखें किसी दूसरे की जो चेहरे पर पपोटों के पीछे महसूर कर दी गईं।', 'topic': 1}


```
### Data Fields

Each row contatins 4 columns:
- premise: string
- hypothesis: string
- label: class label with values that correspond to "not-entailment" (0) or "entailment" (1)
- topic: class label with values that correspond to "Argumentative" (0), "Descriptive" (1), "Dialogic" (2), "Informative" (3) or "Narrative" (4).

### Data Splits

- Train : 31892
- Valid : 9460
- Test : 9970

## Dataset Creation

- We employ a recasting technique from Poliak et al. (2018a,b) to convert publicly available Hindi Discourse Analysis classification datasets in Hindi and pose them as TE problems
- In this recasting process, we build template hypotheses for each class in the label taxonomy
- Then, we pair the original annotated sentence with each of the template hypotheses to create TE samples.
- For more information on the recasting process, refer to paper https://www.aclweb.org/anthology/2020.aacl-main.71

### Source Data

Source Dataset for the recasting process is the BBC Hindi Headlines Dataset(https://github.com/NirantK/hindi2vec/releases/tag/bbc-hindi-v0.1)

#### Initial Data Collection and Normalization

-  Initial Data was collected by members of MIDAS Lab from Hindi Websites. They crowd sourced the data annotation process and selected two random stories from our corpus and had the three annotators work on them independently and classify each sentence based on the discourse mode.
- Please refer to this paper for detailed information: https://www.aclweb.org/anthology/2020.lrec-1.149/
- The Discourse is further classified into "Argumentative" , "Descriptive" , "Dialogic" , "Informative"  and  "Narrative" - 5 Clases.

#### Who are the source language producers?

Please refer to this paper for detailed information: https://www.aclweb.org/anthology/2020.lrec-1.149/

### Annotations

#### Annotation process

Annotation process has been described in Dataset Creation Section.

#### Who are the annotators?

Annotation is done automatically by machine and corresponding recasting process.

### Personal and Sensitive Information

No Personal and Sensitive Information is mentioned in the Datasets.

## Considerations for Using the Data

Pls refer to this paper: https://www.aclweb.org/anthology/2020.aacl-main.71

### Discussion of Biases

No known bias exist in the dataset.
Pls refer to this paper: https://www.aclweb.org/anthology/2020.aacl-main.71

### Other Known Limitations

No other known limitations . Size of data may not be enough to train large models

## Additional Information

Pls refer to this link: https://github.com/midas-research/hindi-nli-data

### Dataset Curators

It is written in the repo : https://github.com/midas-research/hindi-nli-data that 
- This corpus can be used freely for research purposes.
- The paper listed below provide details of the creation and use of the corpus. If you use the corpus, then please cite the paper.
- If interested in commercial use of the corpus, send email to midas@iiitd.ac.in.
- If you use the corpus in a product or application, then please credit the authors and Multimodal Digital Media Analysis Lab - Indraprastha Institute of Information Technology, New Delhi appropriately. Also, if you send us an email, we will be thrilled to know about how you have used the corpus.
- Multimodal Digital Media Analysis Lab - Indraprastha Institute of Information Technology, New Delhi, India disclaims any responsibility for the use of the corpus and does not provide technical support. However, the contact listed above will be happy to respond to queries and clarifications.
- Rather than redistributing the corpus, please direct interested parties to this page
- Please feel free to send us an email:
  - with feedback regarding the corpus.
  - with information on how you have used the corpus.
  - if interested in having us analyze your data for natural language inference.
  - if interested in a collaborative research project.


### Licensing Information

Copyright (C) 2019 Multimodal Digital Media Analysis Lab - Indraprastha Institute of Information Technology, New Delhi (MIDAS, IIIT-Delhi).
Pls contact authors for any information on the dataset.

### Citation Information

```
    @inproceedings{uppal-etal-2020-two,
    title = "Two-Step Classification using Recasted Data for Low Resource Settings",
    author = "Uppal, Shagun  and
      Gupta, Vivek  and
      Swaminathan, Avinash  and
      Zhang, Haimin  and
      Mahata, Debanjan  and
      Gosangi, Rakesh  and
      Shah, Rajiv Ratn  and
      Stent, Amanda",
    booktitle = "Proceedings of the 1st Conference of the Asia-Pacific Chapter of the Association for Computational Linguistics and the 10th International Joint Conference on Natural Language Processing",
    month = dec,
    year = "2020",
    address = "Suzhou, China",
    publisher = "Association for Computational Linguistics",
    url = "https://www.aclweb.org/anthology/2020.aacl-main.71",
    pages = "706--719",
    abstract = "An NLP model{'}s ability to reason should be independent of language. Previous works utilize Natural Language Inference (NLI) to understand the reasoning ability of models, mostly focusing on high resource languages like English. To address scarcity of data in low-resource languages such as Hindi, we use data recasting to create NLI datasets for four existing text classification datasets. Through experiments, we show that our recasted dataset is devoid of statistical irregularities and spurious patterns. We further study the consistency in predictions of the textual entailment models and propose a consistency regulariser to remove pairwise-inconsistencies in predictions. We propose a novel two-step classification method which uses textual-entailment predictions for classification task. We further improve the performance by using a joint-objective for classification and textual entailment. We therefore highlight the benefits of data recasting and improvements on classification performance using our approach with supporting experimental results.",
}
```

### Contributions

Thanks to [@avinsit123](https://github.com/avinsit123) for adding this dataset.
