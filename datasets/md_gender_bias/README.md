---
pretty_name: Multi-Dimensional Gender Bias Classification
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
  - 1M<n<10M
  new_data:
  - 1K<n<10K
  opensubtitles_inferred:
  - 100K<n<1M
  wizard:
  - 10K<n<100K
  yelp_inferred:
  - 1M<n<10M
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
paperswithcode_id: md-gender
---

# Dataset Card for Multi-Dimensional Gender Bias Classification

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

- **Homepage:** [ParlAI MD Gender Project Page](https://parl.ai/projects/md_gender/)
- **Repository:** [ParlAI Github MD Gender Repository](https://github.com/facebookresearch/ParlAI/tree/master/projects/md_gender)
- **Paper:** [Multi-Dimensional Gender Bias Classification](https://www.aclweb.org/anthology/2020.emnlp-main.23.pdf)
- **Leaderboard:** [Needs More Information]
- **Point of Contact:** edinan@fb.com

### Dataset Summary

The Multi-Dimensional Gender Bias Classification dataset is based on a general framework that decomposes gender bias in text along several pragmatic and semantic dimensions: bias from the gender of the person being spoken about, bias from the gender of the person being spoken to, and bias from the gender of the speaker. It contains seven large scale datasets automatically annotated for gender information (there are eight in the original project but the Wikipedia set is not included in the HuggingFace distribution), one crowdsourced evaluation benchmark of utterance-level gender rewrites, a list of gendered names, and a list of gendered words in English. 

### Supported Tasks and Leaderboards

- `text-classification-other-gender-bias`: The dataset can be used to train a model for classification of various kinds of gender bias. The model performance is evaluated based on the accuracy of the predicted labels as compared to the given labels in the dataset. Dinan et al's (2020) Transformer model achieved an average of 67.13% accuracy in binary gender prediction across the ABOUT, TO, and AS tasks. See the paper for more results.

### Languages

The data is in English as spoken on the various sites where the data was collected. The associated BCP-47 code `en`.

## Dataset Structure

### Data Instances

The following are examples of data instances from the various configs in the dataset. See the [MD Gender Bias dataset viewer](https://huggingface.co/datasets/viewer/?dataset=md_gender_bias) to explore more examples.

An example from the `new_data` config:
```
{'class_type': 0, 
 'confidence': 'certain', 
 'episode_done': True, 
 'labels': [1], 
 'original': 'She designed monumental Loviisa war cemetery in 1920', 
 'text': 'He designed monumental Lovissa War Cemetery in 1920.', 
 'turker_gender': 4}
```

An example from the `funpedia` config:
```
{'gender': 2, 
 'persona': 'Humorous', 
 'text': 'Max Landis is a comic book writer who wrote Chronicle, American Ultra, and Victor Frankestein.', 
 'title': 'Max Landis'}
```

An example from the `image_chat` config:
```
{'caption': '<start> a young girl is holding a pink umbrella in her hand <eos>', 
 'female': True, 
 'id': '2923e28b6f588aff2d469ab2cccfac57', 
 'male': False}
```

An example from the `wizard` config:
```
{'chosen_topic': 'Krav Maga', 
 'gender': 2, 
 'text': 'Hello. I hope you might enjoy or know something about Krav Maga?'}
```

An example from the `convai2_inferred` config (the other `_inferred` configs have the same fields, with the exception of `yelp_inferred`, which does not have the `ternary_label` or `ternary_score` fields):
```
{'binary_label': 1, 
'binary_score': 0.6521999835968018, 
'ternary_label': 2, 
'ternary_score': 0.4496000111103058, 
'text': "hi , how are you doing ? i'm getting ready to do some cheetah chasing to stay in shape ."}
```

An example from the `gendered_words` config:
```
{'word_feminine': 'countrywoman',
 'word_masculine': 'countryman'}
```

An example from the `name_genders` config:
```
{'assigned_gender': 1,
 'count': 7065,
 'name': 'Mary'}
```

### Data Fields

The following are the features for each of the configs.

For the `new_data` config:
- `text`: the text to be classified
- `original`: the text before reformulation
- `labels`: a `list` of classification labels, with possible values including `ABOUT:female`, `ABOUT:male`, `PARTNER:female`, `PARTNER:male`, `SELF:female`.
- `class_type`: a classification label, with possible values including `about` (0), `partner` (1), `self` (2).
- `turker_gender`: a classification label, with possible values including `man` (0), `woman` (1), `nonbinary` (2), `prefer not to say` (3), `no answer` (4).
- `episode_done`: a boolean indicating whether the conversation was completed.
- `confidence`: a string indicating the confidence of the annotator in response to the instance label being ABOUT/TO/AS a man or woman. Possible values are `certain`, `pretty sure`, and `unsure`.  

For the `funpedia` config:
- `text`: the text to be classified.
- `gender`: a classification label, with possible values including `gender-neutral` (0), `female` (1), `male` (2), indicating the gender of the person being talked about.
- `persona`: a string describing the persona assigned to the user when talking about the entity.
- `title`: a string naming the entity the text is about.

For the `image_chat` config:
- `caption`: a string description of the contents of the original image.
- `female`: a boolean indicating whether the gender of the person being talked about is female, if the image contains a person. 
- `id`: a string indicating the id of the image.
- `male`: a boolean indicating whether the gender of the person being talked about is male, if the image contains a person. 

For the `wizard` config:
- `text`: the text to be classified.
- `chosen_topic`: a string indicating the topic of the text.
- `gender`: a classification label, with possible values including `gender-neutral` (0), `female` (1), `male` (2), indicating the gender of the person being talked about.

For the `_inferred` configurations (again, except the `yelp_inferred` split, which does not have the `ternary_label` or `ternary_score` fields):
- `text`: the text to be classified.
- `binary_label`: a classification label, with possible values including `ABOUT:female`, `ABOUT:male`.
- `binary_score`: a float indicating a score between 0 and 1.
- `ternary_label`: a classification label, with possible values including `ABOUT:female`, `ABOUT:male`, `ABOUT:gender-neutral`.
- `ternary_score`: a float indicating a score between 0 and 1.

For the word list:
- `word_masculine`: a string indicating the masculine version of the word.
- `word_feminine`: a string indicating the feminine version of the word.

For the gendered name list:
- `assigned_gender`: an integer, 1 for female, 0 for male.
- `count`: an integer.
- `name`: a string of the name.

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

The curators chose to annotate the existing corpora to make their classifiers reliable on all dimensions (ABOUT/TO/AS) and across multiple domains. However, none of the existing datasets cover all three dimensions at the same time, and many of the gender labels are noisy. To enable reliable evaluation, the curators collected a specialized corpus, found in the `new_data` config, which acts as a gold-labeled dataset for the masculine and feminine classes.

### Source Data

#### Initial Data Collection and Normalization

For the `new_data` config, the curators collected conversations between two speakers. Each speaker was provided with a persona description containing gender information, then tasked with adopting that persona and having a conversation. They were also provided with small sections of a biography from Wikipedia as the conversation topic in order to encourage crowdworkers to discuss ABOUT/TO/AS gender information. To ensure there is ABOUT/TO/AS gender information contained in each utterance, the curators asked a second set of annotators to rewrite each utterance to make it very clear that they are speaking ABOUT a man or a woman, speaking AS a man or a woman, and speaking TO a man or a woman. 

#### Who are the source language producers?

This dataset was collected from crowdworkers from Amazon’s Mechanical Turk. All workers are English-speaking and located in the United States.

| Reported Gender   | Percent of Total |
| ----------------- | ---------------- |
| Man               | 67.38            |
| Woman             | 18.34            |
| Non-binary        | 0.21             |
| Prefer not to say | 14.07            |

### Annotations

#### Annotation process

For the `new_data` config, annotators were asked to label how confident they are that someone else could predict the given gender label, allowing for flexibility between explicit genderedness (like the use of "he" or "she") and statistical genderedness.

Many of the annotated datasets contain cases where the ABOUT, AS, TO labels are not provided (i.e. unknown). In such instances, the curators apply one of two strategies. They apply the imputation strategy for data for which the ABOUT label is unknown using a classifier trained only on other Wikipedia data for which this label is provided. Data without a TO or AS label was assigned one at random, choosing between masculine and feminine with equal probability. Details of how each of the eight training datasets was annotated are as follows:

1. Wikipedia- to annotate ABOUT, the curators used a Wikipedia dump and extract biography pages using named entity recognition. They labeled pages with a gender based on the number of gendered pronouns (he vs. she vs. they) and labeled each paragraph in the page with this label for the ABOUT dimension. 

2. Funpedia- Funpedia ([Miller et al., 2017](https://www.aclweb.org/anthology/D17-2014/)) contains rephrased Wikipedia sentences in a more conversational way. The curators retained only biography related sentences and annotate similar to Wikipedia, to give ABOUT labels.

3. Wizard of Wikipedia- [Wizard of Wikipedia](https://parl.ai/projects/wizard_of_wikipedia/) contains two people discussing a topic in Wikipedia. The curators retain only the conversations on Wikipedia biographies and annotate to create ABOUT labels.

4. ImageChat- [ImageChat](https://klshuster.github.io/image_chat/) contains conversations discussing the contents of an image. The curators used the [Xu et al. image captioning system](https://github.com/AaronCCWong/Show-Attend-and-Tell) to identify the contents of an image and select gendered examples.

5. Yelp- The curators used the Yelp reviewer gender predictor developed by ([Subramanian et al., 2018](https://arxiv.org/pdf/1811.00552.pdf)) and retain reviews for which the classifier is very confident – this creates labels for the content creator of the review (AS). They impute ABOUT labels on this dataset using a classifier trained on the datasets 1-4.

6. ConvAI2- [ConvAI2](https://parl.ai/projects/convai2/) contains persona-based conversations. Many personas contain sentences such as 'I am a old woman' or 'My name is Bob' which allows annotators to annotate the gender of the speaker (AS) and addressee (TO) with some confidence. Many of the personas have unknown gender. The curators impute ABOUT labels on this dataset using a classifier trained on the datasets 1-4.

7. OpenSubtitles- [OpenSubtitles](http://www.opensubtitles.org/) contains subtitles for movies in different languages. The curators retained English subtitles that contain a character name or identity. They annotated the character’s gender using gender kinship terms such as daughter and gender probability distribution calculated by counting the masculine and feminine names of baby names in the United States. Using the character’s gender, they produced labels for the AS dimension. They produced labels for the TO dimension by taking the gender of the next character to speak if there is another utterance in the conversation; otherwise, they take the gender of the last character to speak. They impute ABOUT labels on this dataset using a classifier trained on the datasets 1-4.

8. LIGHT- [LIGHT](https://parl.ai/projects/light/) contains persona-based conversation. Similarly to ConvAI2, annotators labeled the gender of each persona, giving labels for the speaker (AS) and speaking partner (TO). The curators impute ABOUT labels on this dataset using a classifier trained on the datasets 1-4.

#### Who are the annotators?

This dataset was annotated by crowdworkers from Amazon’s Mechanical Turk. All workers are English-speaking and located in the United States.

### Personal and Sensitive Information

For privacy reasons the curators did not associate the self-reported gender of the annotator with the labeled examples in the dataset and only report these statistics in aggregate. 

## Considerations for Using the Data

### Social Impact of Dataset

This dataset is intended for applications such as controlling for gender bias in generative models, detecting gender bias in arbitrary text, and classifying text as offensive based on its genderedness. 

### Discussion of Biases

Over two thirds of annotators identified as men, which may introduce biases into the dataset.

Wikipedia is also well known to have gender bias in equity of biographical coverage and lexical bias in noun references to women (see the paper's appendix for citations).

### Other Known Limitations

The limitations of the Multi-Dimensional Gender Bias Classification dataset have not yet been investigated, but the curators acknowledge that more work is required to address the intersectionality of gender identities, i.e., when gender non-additively interacts with other identity characteristics. The curators point out that negative gender stereotyping is known to be alternatively weakened or reinforced by the presence of social attributes like dialect, class and race and that these differences have been found to affect gender classification in images and sentences encoders. See the paper for references.

## Additional Information

### Dataset Curators

Emily Dinan, Angela Fan, Ledell Wu, Jason Weston, Douwe Kiela, and Adina Williams at Facebook AI Research. Angela Fan is also affiliated with Laboratoire Lorrain d’Informatique et Applications (LORIA).

### Licensing Information

The Multi-Dimensional Gender Bias Classification dataset is licensed under the [MIT License](https://opensource.org/licenses/MIT).

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

Thanks to [@yjernite](https://github.com/yjernite) and [@mcmillanmajora](https://github.com/mcmillanmajora)for adding this dataset.
