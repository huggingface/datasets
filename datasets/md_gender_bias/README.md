---
annotations_creators:
  convai2_inferred:
  - machine-generated
  funpedia:
  - found
  gendered_words:
  - found
  image_chat:
  - found
  light_inferred:
  - machine-generated
  name_genders:
  - found
  new_data:
  - crowdsourced
  - found
  opensubtitles_inferred:
  - machine-generated
  wizard:
  - found
  yelp_inferred:
  - machine-generated
language_creators:
  convai2_inferred:
  - found
  funpedia:
  - found
  gendered_words:
  - found
  image_chat:
  - found
  light_inferred:
  - found
  name_genders:
  - found
  new_data:
  - crowdsourced
  - found
  opensubtitles_inferred:
  - found
  wizard:
  - found
  yelp_inferred:
  - found
languages:
- en
licenses:
- mit
multilinguality:
- monolingual
size_categories:
  convai2_inferred:
  - 100K<n<1M
  funpedia:
  - 10K<n<100K
  gendered_words:
  - n<1K
  image_chat:
  - 100K<n<1M
  light_inferred:
  - 100K<n<1M
  name_genders:
  - n>1M
  new_data:
  - 1K<n<10K
  opensubtitles_inferred:
  - 100K<n<1M
  wizard:
  - 10K<n<100K
  yelp_inferred:
  - n>1M
source_datasets:
  convai2_inferred:
  - extended|other-convai2
  - original
  funpedia:
  - original
  gendered_words:
  - original
  image_chat:
  - original
  light_inferred:
  - extended|other-light
  - original
  name_genders:
  - original
  new_data:
  - original
  opensubtitles_inferred:
  - extended|other-opensubtitles
  - original
  wizard:
  - original
  yelp_inferred:
  - extended|other-yelp
  - original
task_categories:
- text-classification
task_ids:
- text-classification-other-gender-bias
---

# Dataset Card for Multi-Dimensional Gender Bias Classification

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
  - [Contributions](#contributions)

## Dataset Description

- **Homepage:** https://parl.ai/projects/md_gender/
- **Repository:** [Needs More Information]
- **Paper:** https://arxiv.org/abs/2005.00614
- **Leaderboard:** [Needs More Information]
- **Point of Contact:** edinan@fb.com

### Dataset Summary

The Multi-Dimensional Gender Bias Classification dataset is based on a general framework that decomposes gender bias in text along several pragmatic and semantic dimensions: bias from the gender of the person being spoken about, bias from the gender of the person being spoken to, and bias from the gender of the speaker. It contains seven large scale datasets automatically annotated for gender information (there are eight in the original project but the Wikipedia set is not included here), one novel, crowdsourced evaluation benchmark of utterance-level gender rewrites, and a list of gendered words in English. 

### Supported Tasks and Leaderboards

- `text-classification-other-gender-bias`: 

### Languages

The data is in English as spoken on the various sites where the data was collected. The associated BCP-47 code `en`.

## Dataset Structure

### Data Instances

```
{'class_type': 0, 
 'confidence': 'certain', 
 'episode_done': True, 
 'labels': [1], 
 'original': ' She designed monumental Loviisa war cemetery in 1920', 
 'text': 'He designed monumental Lovissa War Cemetery in 1920.', 
 'turker_gender': 4}
```

### Data Fields

The data has the following features.

For the `new_data` config:
- `text`: the text to be classified
- `original`: the text before reformulation
- `labels`: a `list` of classification labels, with possible values including `ABOUT:female`, `ABOUT:male`, `PARTNER:female`, `PARTNER:male`, `SELF:female`.
- `class_type`: a classification label, with possible values including `about`, `partner`, `self`.
- `turker_gender`: a classification label, with possible values including `man`, `woman`, `nonbinary`, `prefer not to say`, `no answer`.

For the other annotated datasets:
- `text`: the text to be classified.
- `gender`: a classification label, with possible values including `gender-neutral`, `female`, `male`.

For the `_inferred` configurations:
- `text`: the text to be classified.
- `binary_label`: a classification label, with possible values including `ABOUT:female`, `ABOUT:male`.
- `binary_score`: a score between 0 and 1.
- `ternary_label`: a classification label, with possible values including `ABOUT:female`, `ABOUT:male`, `ABOUT:gender-neutral`.
- `ternary_score`: a score between 0 and 1.

### Data Splits

The different parts of the data can be accessed through the different configurations:
- `gendered_words`: A list of common nouns with a masculine and feminine variant.
- `new_data`: Sentences reformulated and annotated along all three axes.
- `funpedia`, `wizard`: Sentences from Funpedia and Wizards of Wikipedia annotated with ABOUT gender with entity gender information.
- `image_chat`: sentences about images annotated  with ABOUT gender based on gender information from the entities in the image
- `convai2_inferred`, `light_inferred`, `opensubtitles_inferred`, `yelp_inferred`:  Data from several source datasets with ABOUT annotations inferred by a trined classifier.

| Split      | M    | F   | N    | U    | Dimension |
| ---------- | ---- | --- | ---- | ---- | --------- |
| Image Chat | 39K  | 15K | 154K | -    | ABOUT     | 
| Funpedia   | 19K  | 3K  | 1K   | -    | ABOUT     |
| Wizard     | 6K   | 1K  | 1K   | -    | ABOUT     |
| Yelp       | 1M   | 1M  | -    | -    | AS        |
| ConvAI2    | 22K  | 22K | -    | 86K  | AS        |
| ConvAI2    | 22K  | 22K | -    | 86K  | TO        |
| OpenSub    | 149K | 69K | -    | 131K | AS        |
| OpenSub    | 95K  | 45K | -    | 209K | TO        |
| LIGHT      | 13K  | 8K  | -    | 83K  | AS        |
| LIGHT      | 13K  | 8K  | -    | 83K  | TO        |
| ---------- | ---- | --- | ---- | ---- | --------- |
| MDGender   | 384  | 401 | -    | -    | ABOUT     |
| MDGender   | 396  | 371 | -    | -    | AS        |
| MDGender   | 411  | 382 | -    | -    | TO        |

## Dataset Creation

### Curation Rationale

To make our classifiers reliable on all dimensions across multiple domains, we train on a variety of datasets. However, none of the existing data covers all three dimensions at the same time, and furthermore, many of the gender labels are noisy. To enable reliable evaluation, we collect a specialized corpus, MDGENDER, which acts as a gold-labeled dataset for the masculine and feminine classes.

### Source Data

#### Initial Data Collection and Normalization

[Needs More Information]

#### Who are the source language producers?

This dataset was collected using crowdworkers from Amazon’s Mechanical Turk. All workers are English-speaking and located in the United States.

| Reported Gender   | Percent of Total |
| ----------------- | ---------------- |
| Man               | 67.38            |
| Woman             | 18.34            |
| Non-binary        | 0.21             |
| Prefer not to say | 14.07            |

### Annotations

#### Annotation process

Many of our annotated datasets contain cases where the ABOUT, AS, TO labels are not provided (i.e. unknown). For example, often we do not know the gender of the content creator for Wikipedia (i.e., the AS dimension is unknown). To retain such examples for training, we either impute the gender label or provide a label at random. We apply the imputation strategy for data for which the ABOUT label is unknown using a classifier trained only onother Wikipedia data for which this label is provided. Data without a TO or AS label was assigned one at random, choosing between masculine and feminine with equal probability. From epoch to epoch, we switch these arbitrarily assigned labels so that the model learns to label unknown examples as masculine or feminine with roughly equal probability. This label flipping allows us to retain greater quantities of data by preserving unknown samples. During training, we balance the data across the masculine, feminine, and neutral classes by up-sampling classes with fewer examples. We describe in more detail how each of the eight training datasets is annotated:

1. Wikipedia- to annotate ABOUT, we use a Wikipedia dump and extract biography pages. We identify biographies using named entity recognition applied to the title of the page (Honnibal and Montani, 2017). We label pages with a gender based on the number of gendered pronouns (he vs. she vs. they) and label each paragraph in the page with this label for the ABOUT dimension. Wikipedia is well known to have gender bias in equity of biographical coverage and lexical bias in noun references to women (see the paper for references), making it an interesting test bed for our investigation.

2. Funpedia- Funpedia (Miller et al., 2017) contains rephrased Wikipedia sentences in a more conversational way. We retain only biography related sentences and annotate similar to Wikipedia, to give ABOUT labels.

3. Wizard of Wikipedia- Wizard of Wikipedia (Dinan et al., 2019c) contains two people discussing a topic in Wikipedia. We retain only the conversations on Wikipedia biographies and annotate to create ABOUT labels.

4. ImageChat- ImageChat (Shuster et al., 2018) contains conversations discussing the contents of an image. We use the [Xu et al. image captioning system](https://github.com/AaronCCWong/Show-Attend-and-Tell) to identify the contents of an image and select gendered examples.

5. Yelp- we use the Yelp reviewer gender predictor developed by (Subramanian et al., 2018) and retain reviews for which the classifier is very confident – this creates labels for the content creator of the review (AS). We impute ABOUT labels on this dataset using a classifier trained on the datasets 1-4.

6. ConvAI2- ConvAI2 (Dinan  et  al.,  2019b) contains persona-based conversations. Many personas contain sentences such as 'I am a old woman' or 'My name is Bob' which allows annotators to annotate the gender of the speaker (AS) and addressee (TO) with some confidence. Many of the personas have unknown gender. We impute ABOUT labels on this dataset using a classifier trained on the datasets 1-4.

7. OpenSubtitiles- OpenSubtitles (Lison andTiedemann, 2016) contains subtitles for movies in different languages. We retain English subtitles that contain a character name or identity. We annotate the character’s gender using gender kinship terms such as daughter and gender probability distribution calculated by counting the masculine and feminine names of baby names in the United States. Using the character’s gender, we get labels for the AS dimension. We get labels for the TO dimension by taking the gender of the next character to speak if there is another utterance in the conversation; otherwise, we take the gender of the last character to speak. We impute ABOUT labels on this dataset using a classifier trained on the datasets 1-4.

8. LIGHT- LIGHT contains persona-based conversation. Similarly to ConvAI2, annotators labeled the gender of each persona (Dinanet al., 2020), giving us labels for the speaker (AS) and speaking partner (TO). We impute ABOUT labels on this dataset using a classifier trained on the datasets 1-4.

#### Who are the annotators?

[Needs More Information]

### Personal and Sensitive Information

or privacy reasons we do not associate the self-reported gender of the annotator with the labeled examples in the dataset and only report these statistics in aggregate

## Considerations for Using the Data

### Social Impact of Dataset

[Needs More Information]

### Discussion of Biases

Over two thirds of annotators identified as men, which may introduce its own biases into the dataset.

### Other Known Limitations

[Needs More Information]

## Additional Information

### Dataset Curators

Emily Dinan, Angela Fan, Ledell Wu, Jason Weston, Douwe Kiela, and Adina Williams at Facebook AI Research. Angela Fan is also affiliated with Laboratoire Lorrain d’Informatique et Applications (LORIA).

### Licensing Information

MIT License

### Citation Information

```
@inproceedings{dinan-etal-2020-multi,
    title = "Multi-Dimensional Gender Bias Classification",
    author = "Dinan, Emily  and
      Fan, Angela  and
      Wu, Ledell  and
      Weston, Jason  and
      Kiela, Douwe  and
      Williams, Adina",
    booktitle = "Proceedings of the 2020 Conference on Empirical Methods in Natural Language Processing (EMNLP)",
    month = nov,
    year = "2020",
    address = "Online",
    publisher = "Association for Computational Linguistics",
    url = "https://www.aclweb.org/anthology/2020.emnlp-main.23",
    doi = "10.18653/v1/2020.emnlp-main.23",
    pages = "314--331",
    abstract = "Machine learning models are trained to find patterns in data. NLP models can inadvertently learn socially undesirable patterns when training on gender biased text. In this work, we propose a novel, general framework that decomposes gender bias in text along several pragmatic and semantic dimensions: bias from the gender of the person being spoken about, bias from the gender of the person being spoken to, and bias from the gender of the speaker. Using this fine-grained framework, we automatically annotate eight large scale datasets with gender information. In addition, we collect a new, crowdsourced evaluation benchmark. Distinguishing between gender bias along multiple dimensions enables us to train better and more fine-grained gender bias classifiers. We show our classifiers are valuable for a variety of applications, like controlling for gender bias in generative models, detecting gender bias in arbitrary text, and classifying text as offensive based on its genderedness.",
}
```

### Contributions

Thanks to [@yjernite](https://github.com/yjernite) for adding this dataset.
