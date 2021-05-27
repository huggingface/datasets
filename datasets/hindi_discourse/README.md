---
annotations_creators:
- other
language_creators:
- found
languages:
- hi
licenses:
- other-MIDAS-LAB-IIITD-Delhi
multilinguality:
- monolingual
size_categories:
- 1K<n<10K
source_datasets:
- original
task_categories:
- sequence-modeling
task_ids:
- sequence-modeling-other-discourse-analysis
paperswithcode_id: null
---

# Dataset Card for Discourse Analysis dataset

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

- **Homepage:** https://github.com/midas-research/hindi-discourse
- **Paper:** https://www.aclweb.org/anthology/2020.lrec-1.149/
- **Point of Contact:** https://github.com/midas-research/MeTooMA


### Dataset Summary

- The Hindi Discourse Analysis dataset is a corpus for analyzing discourse modes present in its sentences.
- It contains sentences from stories written by 11 famous authors from the 20th Century.
- 4-5 stories by each author have been selected which were available in the public domain resulting in a collection of 53 stories.
- Most of these short stories were originally written in Hindi but some of them were written in other Indian languages and later translated to Hindi.
The corpus contains a total of 10472 sentences belonging to the following categories:
- Argumentative
- Descriptive
- Dialogic
- Informative
- Narrative

### Supported Tasks and Leaderboards

- Discourse Analysis of Hindi.

### Languages

Hindi

## Dataset Structure
- The dataset is structured into JSON format.

### Data Instances
{'Story_no': 15, 'Sentence': ' गाँठ से साढ़े तीन रुपये लग गये, जो अब पेट में जाकर खनकते भी नहीं! जो तेरी करनी मालिक! ” “इसमें मालिक की क्या करनी है? ”', 'Discourse Mode': 'Dialogue'}

### Data Fields

Sentence number, story number, sentence and discourse mode

### Data Splits

- Train: 9983

## Dataset Creation

### Curation Rationale
- Present a new publicly available corpus
consisting of sentences from short stories written in a
low-resource language of Hindi having high quality annotation for five different discourse modes -
argumentative, narrative, descriptive, dialogic and informative.

- Perform a detailed analysis of the proposed annotated corpus and characterize the performance of
different classification algorithms.

### Source Data
- Source of all the data points in this dataset is Hindi stories written by famous authors of Hindi literature.

#### Initial Data Collection and Normalization

- All the data was collected from various Hindi websites.
- We chose against crowd-sourcing the annotation pro- cess because we wanted to directly work with the an- notators for qualitative feedback and to also ensure high quality annotations. 
- We employed three native Hindi speakers with college level education for the an- notation task. 
- We first selected two random stories from our corpus and had the three annotators work on them independently and classify each sentence based on the discourse mode.
- Please refer to this paper for detailed information: https://www.aclweb.org/anthology/2020.lrec-1.149/

#### Who are the source language producers?

Please refer to this paper for detailed information: https://www.aclweb.org/anthology/2020.lrec-1.149/

### Annotations

#### Annotation process

- The authors chose against crowd sourcing for labeling this dataset due to its highly sensitive nature.
- The annotators are domain experts having degress in advanced clinical psychology and gender studies.
- They were provided a guidelines document with instructions about each task and its definitions, labels and examples.
- They studied the document, worked a few examples to get used to this annotation task.
- They also provided feedback for improving the class definitions.
- The annotation process is not mutually exclusive, implying that presence of one label does not mean the
absence of the other one.

#### Who are the annotators?

- The annotators were three native Hindi speakers with college level education.
- Please refer to the accompnaying paper for a detailed annotation process.

### Personal and Sensitive Information
[More Information Needed]

## Considerations for Using the Data

### Social Impact of Dataset
- As a future work we would also like to use the presented corpus to see how it could be further used
in certain downstream tasks such as emotion analysis, machine translation,
textual entailment, and speech sythesis for improving storytelling experience in Hindi language.

### Discussion of Biases
[More Information Needed]

### Other Known Limitations

- We could not get the best performance using the deep learning model trained on the data, due to
  insufficient data for DL models.

## Additional Information

Please refer to this link: https://github.com/midas-research/hindi-discourse

### Dataset Curators

- If you use the corpus in a product or application, then please credit the authors
and [Multimodal Digital Media Analysis Lab - Indraprastha Institute of Information Technology, New Delhi]
(http://midas.iiitd.edu.in) appropriately.
Also, if you send us an email, we will be thrilled to know about how you have used the corpus.
- If interested in commercial use of the corpus, send email to midas@iiitd.ac.in.
- Multimodal Digital Media Analysis Lab - Indraprastha Institute of Information Technology, New Delhi, India
disclaims any responsibility for the use of the corpus and does not provide technical support.
However, the contact listed above will be happy to respond to queries and clarifications
- Please feel free to send us an email:
  - with feedback regarding the corpus.
  - with information on how you have used the corpus.
  - if interested in having us analyze your social media data.
  - if interested in a collaborative research project.

### Licensing Information

- If you use the corpus in a product or application, then please credit the authors
and [Multimodal Digital Media Analysis Lab - Indraprastha Institute of Information Technology, New Delhi]
(http://midas.iiitd.edu.in) appropriately.

### Citation Information

Please cite the following publication if you make use of the dataset: https://www.aclweb.org/anthology/2020.lrec-1.149/

```
@inproceedings{dhanwal-etal-2020-annotated,
    title = "An Annotated Dataset of Discourse Modes in {H}indi Stories",
    author = "Dhanwal, Swapnil  and
      Dutta, Hritwik  and
      Nankani, Hitesh  and
      Shrivastava, Nilay  and
      Kumar, Yaman  and
      Li, Junyi Jessy  and
      Mahata, Debanjan  and
      Gosangi, Rakesh  and
      Zhang, Haimin  and
      Shah, Rajiv Ratn  and
      Stent, Amanda",
    booktitle = "Proceedings of the 12th Language Resources and Evaluation Conference",
    month = may,
    year = "2020",
    address = "Marseille, France",
    publisher = "European Language Resources Association",
    url = "https://www.aclweb.org/anthology/2020.lrec-1.149",
    pages = "1191--1196",
    abstract = "In this paper, we present a new corpus consisting of sentences from Hindi short stories annotated for five different discourse modes argumentative, narrative, descriptive, dialogic and informative. We present a detailed account of the entire data collection and annotation processes. The annotations have a very high inter-annotator agreement (0.87 k-alpha). We analyze the data in terms of label distributions, part of speech tags, and sentence lengths. We characterize the performance of various classification algorithms on this dataset and perform ablation studies to understand the nature of the linguistic models suitable for capturing the nuances of the embedded discourse structures in the presented corpus.",
    language = "English",
    ISBN = "979-10-95546-34-4",
}
```

### Contributions

Thanks to [@duttahritwik](https://github.com/duttahritwik) for adding this dataset.