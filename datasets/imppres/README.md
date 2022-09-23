---
annotations_creators:
- machine-generated
language_creators:
- machine-generated
language:
- en
license:
- cc-by-nc-4.0
multilinguality:
- monolingual
size_categories:
- 1K<n<10K
source_datasets:
- original
task_categories:
- text-classification
task_ids:
- natural-language-inference
paperswithcode_id: imppres
pretty_name: IMPPRES
dataset_info:
- config_name: presupposition_all_n_presupposition
  features:
  - name: premise
    dtype: string
  - name: hypothesis
    dtype: string
  - name: trigger
    dtype: string
  - name: trigger1
    dtype: string
  - name: trigger2
    dtype: string
  - name: presupposition
    dtype: string
  - name: gold_label
    dtype:
      class_label:
        names:
          0: entailment
          1: neutral
          2: contradiction
  - name: UID
    dtype: string
  - name: pairID
    dtype: string
  - name: paradigmID
    dtype: int16
  splits:
  - name: all_n_presupposition
    num_bytes: 458492
    num_examples: 1900
  download_size: 335088
  dataset_size: 458492
- config_name: presupposition_both_presupposition
  features:
  - name: premise
    dtype: string
  - name: hypothesis
    dtype: string
  - name: trigger
    dtype: string
  - name: trigger1
    dtype: string
  - name: trigger2
    dtype: string
  - name: presupposition
    dtype: string
  - name: gold_label
    dtype:
      class_label:
        names:
          0: entailment
          1: neutral
          2: contradiction
  - name: UID
    dtype: string
  - name: pairID
    dtype: string
  - name: paradigmID
    dtype: int16
  splits:
  - name: both_presupposition
    num_bytes: 432792
    num_examples: 1900
  download_size: 335088
  dataset_size: 432792
- config_name: presupposition_change_of_state
  features:
  - name: premise
    dtype: string
  - name: hypothesis
    dtype: string
  - name: trigger
    dtype: string
  - name: trigger1
    dtype: string
  - name: trigger2
    dtype: string
  - name: presupposition
    dtype: string
  - name: gold_label
    dtype:
      class_label:
        names:
          0: entailment
          1: neutral
          2: contradiction
  - name: UID
    dtype: string
  - name: pairID
    dtype: string
  - name: paradigmID
    dtype: int16
  splits:
  - name: change_of_state
    num_bytes: 308627
    num_examples: 1900
  download_size: 335088
  dataset_size: 308627
- config_name: presupposition_cleft_existence
  features:
  - name: premise
    dtype: string
  - name: hypothesis
    dtype: string
  - name: trigger
    dtype: string
  - name: trigger1
    dtype: string
  - name: trigger2
    dtype: string
  - name: presupposition
    dtype: string
  - name: gold_label
    dtype:
      class_label:
        names:
          0: entailment
          1: neutral
          2: contradiction
  - name: UID
    dtype: string
  - name: pairID
    dtype: string
  - name: paradigmID
    dtype: int16
  splits:
  - name: cleft_existence
    num_bytes: 363238
    num_examples: 1900
  download_size: 335088
  dataset_size: 363238
- config_name: presupposition_cleft_uniqueness
  features:
  - name: premise
    dtype: string
  - name: hypothesis
    dtype: string
  - name: trigger
    dtype: string
  - name: trigger1
    dtype: string
  - name: trigger2
    dtype: string
  - name: presupposition
    dtype: string
  - name: gold_label
    dtype:
      class_label:
        names:
          0: entailment
          1: neutral
          2: contradiction
  - name: UID
    dtype: string
  - name: pairID
    dtype: string
  - name: paradigmID
    dtype: int16
  splits:
  - name: cleft_uniqueness
    num_bytes: 388779
    num_examples: 1900
  download_size: 335088
  dataset_size: 388779
- config_name: presupposition_only_presupposition
  features:
  - name: premise
    dtype: string
  - name: hypothesis
    dtype: string
  - name: trigger
    dtype: string
  - name: trigger1
    dtype: string
  - name: trigger2
    dtype: string
  - name: presupposition
    dtype: string
  - name: gold_label
    dtype:
      class_label:
        names:
          0: entailment
          1: neutral
          2: contradiction
  - name: UID
    dtype: string
  - name: pairID
    dtype: string
  - name: paradigmID
    dtype: int16
  splits:
  - name: only_presupposition
    num_bytes: 349018
    num_examples: 1900
  download_size: 335088
  dataset_size: 349018
- config_name: presupposition_possessed_definites_existence
  features:
  - name: premise
    dtype: string
  - name: hypothesis
    dtype: string
  - name: trigger
    dtype: string
  - name: trigger1
    dtype: string
  - name: trigger2
    dtype: string
  - name: presupposition
    dtype: string
  - name: gold_label
    dtype:
      class_label:
        names:
          0: entailment
          1: neutral
          2: contradiction
  - name: UID
    dtype: string
  - name: pairID
    dtype: string
  - name: paradigmID
    dtype: int16
  splits:
  - name: possessed_definites_existence
    num_bytes: 362334
    num_examples: 1900
  download_size: 335088
  dataset_size: 362334
- config_name: presupposition_possessed_definites_uniqueness
  features:
  - name: premise
    dtype: string
  - name: hypothesis
    dtype: string
  - name: trigger
    dtype: string
  - name: trigger1
    dtype: string
  - name: trigger2
    dtype: string
  - name: presupposition
    dtype: string
  - name: gold_label
    dtype:
      class_label:
        names:
          0: entailment
          1: neutral
          2: contradiction
  - name: UID
    dtype: string
  - name: pairID
    dtype: string
  - name: paradigmID
    dtype: int16
  splits:
  - name: possessed_definites_uniqueness
    num_bytes: 459403
    num_examples: 1900
  download_size: 335088
  dataset_size: 459403
- config_name: presupposition_question_presupposition
  features:
  - name: premise
    dtype: string
  - name: hypothesis
    dtype: string
  - name: trigger
    dtype: string
  - name: trigger1
    dtype: string
  - name: trigger2
    dtype: string
  - name: presupposition
    dtype: string
  - name: gold_label
    dtype:
      class_label:
        names:
          0: entailment
          1: neutral
          2: contradiction
  - name: UID
    dtype: string
  - name: pairID
    dtype: string
  - name: paradigmID
    dtype: int16
  splits:
  - name: question_presupposition
    num_bytes: 397227
    num_examples: 1900
  download_size: 335088
  dataset_size: 397227
- config_name: implicature_connectives
  features:
  - name: premise
    dtype: string
  - name: hypothesis
    dtype: string
  - name: gold_label_log
    dtype:
      class_label:
        names:
          0: entailment
          1: neutral
          2: contradiction
  - name: gold_label_prag
    dtype:
      class_label:
        names:
          0: entailment
          1: neutral
          2: contradiction
  - name: spec_relation
    dtype: string
  - name: item_type
    dtype: string
  - name: trigger
    dtype: string
  - name: lexemes
    dtype: string
  splits:
  - name: connectives
    num_bytes: 221868
    num_examples: 1200
  download_size: 335088
  dataset_size: 221868
- config_name: implicature_gradable_adjective
  features:
  - name: premise
    dtype: string
  - name: hypothesis
    dtype: string
  - name: gold_label_log
    dtype:
      class_label:
        names:
          0: entailment
          1: neutral
          2: contradiction
  - name: gold_label_prag
    dtype:
      class_label:
        names:
          0: entailment
          1: neutral
          2: contradiction
  - name: spec_relation
    dtype: string
  - name: item_type
    dtype: string
  - name: trigger
    dtype: string
  - name: lexemes
    dtype: string
  splits:
  - name: gradable_adjective
    num_bytes: 153672
    num_examples: 1200
  download_size: 335088
  dataset_size: 153672
- config_name: implicature_gradable_verb
  features:
  - name: premise
    dtype: string
  - name: hypothesis
    dtype: string
  - name: gold_label_log
    dtype:
      class_label:
        names:
          0: entailment
          1: neutral
          2: contradiction
  - name: gold_label_prag
    dtype:
      class_label:
        names:
          0: entailment
          1: neutral
          2: contradiction
  - name: spec_relation
    dtype: string
  - name: item_type
    dtype: string
  - name: trigger
    dtype: string
  - name: lexemes
    dtype: string
  splits:
  - name: gradable_verb
    num_bytes: 180702
    num_examples: 1200
  download_size: 335088
  dataset_size: 180702
- config_name: implicature_modals
  features:
  - name: premise
    dtype: string
  - name: hypothesis
    dtype: string
  - name: gold_label_log
    dtype:
      class_label:
        names:
          0: entailment
          1: neutral
          2: contradiction
  - name: gold_label_prag
    dtype:
      class_label:
        names:
          0: entailment
          1: neutral
          2: contradiction
  - name: spec_relation
    dtype: string
  - name: item_type
    dtype: string
  - name: trigger
    dtype: string
  - name: lexemes
    dtype: string
  splits:
  - name: modals
    num_bytes: 178560
    num_examples: 1200
  download_size: 335088
  dataset_size: 178560
- config_name: implicature_numerals_10_100
  features:
  - name: premise
    dtype: string
  - name: hypothesis
    dtype: string
  - name: gold_label_log
    dtype:
      class_label:
        names:
          0: entailment
          1: neutral
          2: contradiction
  - name: gold_label_prag
    dtype:
      class_label:
        names:
          0: entailment
          1: neutral
          2: contradiction
  - name: spec_relation
    dtype: string
  - name: item_type
    dtype: string
  - name: trigger
    dtype: string
  - name: lexemes
    dtype: string
  splits:
  - name: numerals_10_100
    num_bytes: 208620
    num_examples: 1200
  download_size: 335088
  dataset_size: 208620
- config_name: implicature_numerals_2_3
  features:
  - name: premise
    dtype: string
  - name: hypothesis
    dtype: string
  - name: gold_label_log
    dtype:
      class_label:
        names:
          0: entailment
          1: neutral
          2: contradiction
  - name: gold_label_prag
    dtype:
      class_label:
        names:
          0: entailment
          1: neutral
          2: contradiction
  - name: spec_relation
    dtype: string
  - name: item_type
    dtype: string
  - name: trigger
    dtype: string
  - name: lexemes
    dtype: string
  splits:
  - name: numerals_2_3
    num_bytes: 188784
    num_examples: 1200
  download_size: 335088
  dataset_size: 188784
- config_name: implicature_quantifiers
  features:
  - name: premise
    dtype: string
  - name: hypothesis
    dtype: string
  - name: gold_label_log
    dtype:
      class_label:
        names:
          0: entailment
          1: neutral
          2: contradiction
  - name: gold_label_prag
    dtype:
      class_label:
        names:
          0: entailment
          1: neutral
          2: contradiction
  - name: spec_relation
    dtype: string
  - name: item_type
    dtype: string
  - name: trigger
    dtype: string
  - name: lexemes
    dtype: string
  splits:
  - name: quantifiers
    num_bytes: 176814
    num_examples: 1200
  download_size: 335088
  dataset_size: 176814
---

# Dataset Card for IMPPRES

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

- **Homepage:** [Github](https://github.com/facebookresearch/Imppres)
- **Repository:** [Github](https://github.com/facebookresearch/Imppres)
- **Paper:** [Aclweb](https://www.aclweb.org/anthology/2020.acl-main.768)
- **Leaderboard:**
- **Point of Contact:**

### Dataset Summary
Over >25k semiautomatically generated sentence pairs illustrating well-studied pragmatic inference types. IMPPRES is an NLI dataset following the format of SNLI (Bowman et al., 2015), MultiNLI (Williams et al., 2018) and XNLI (Conneau et al., 2018), which was created to evaluate how well trained NLI models recognize several classes of presuppositions and scalar implicatures.

### Supported Tasks and Leaderboards

Natural Language Inference.

### Languages

English.

## Dataset Structure

### Data Instances

The data consists of 2 configurations: implicature and presupposition.
Each configuration consists of several different sub-datasets:

**Pressupposition**
- all_n_presupposition  
- change_of_state  
- cleft_uniqueness
- possessed_definites_existence   
- question_presupposition
- both_presupposition   
- cleft_existence  
- only_presupposition
- possessed_definites_uniqueness

**Implicature**
- connectives 
- gradable_adjective  
- gradable_verb  
- modals
- numerals_10_100  
- numerals_2_3  
- quantifiers

Each sentence type in IMPPRES is generated according to a template that specifies the linear order of the constituents in the sentence. The constituents are sampled from a vocabulary of over 3000 lexical items annotated with grammatical features needed to ensure wellformedness. We semiautomatically generate IMPPRES using a codebase developed by Warstadt et al. (2019a) and significantly expanded for the BLiMP dataset (Warstadt et al., 2019b).

Here is an instance of the raw presupposition data from any sub-dataset:
```buildoutcfg
{
"sentence1": "All ten guys that proved to boast might have been divorcing.", 
"sentence2": "There are exactly ten guys that proved to boast.", 
"trigger": "modal", 
"presupposition": "positive", 
"gold_label": "entailment", 
"UID": "all_n_presupposition", 
"pairID": "9e", 
"paradigmID": 0
}
```
and the raw implicature data from any sub-dataset:
```buildoutcfg
{
"sentence1": "That teenager couldn't yell.", 
"sentence2": "That teenager could yell.", 
"gold_label_log": "contradiction", 
"gold_label_prag": "contradiction", 
"spec_relation": "negation", 
"item_type": "control", 
"trigger": "modal", 
"lexemes": "can - have to"
}
```
### Data Fields
**Presupposition**

There is a slight mapping from the raw data fields in the presupposition sub-datasets and the fields appearing in the HuggingFace Datasets. 
When dealing with the HF Dataset, the following mapping of fields happens:
```buildoutcfg
"premise" -> "sentence1"
"hypothesis"-> "sentence2"
"trigger" -> "trigger" or "Not_In_Example"
"trigger1" -> "trigger1" or "Not_In_Example"
"trigger2" -> "trigger2" or "Not_In_Example"
"presupposition" -> "presupposition" or "Not_In_Example"
"gold_label" -> "gold_label"
"UID" -> "UID"
"pairID" -> "pairID"
"paradigmID" -> "paradigmID"
```
For the most part, the majority of the raw fields remain unchanged. However, when it comes to the various `trigger` fields, a new mapping was introduced. 
There are some examples in the dataset that only have the `trigger` field while other examples have the `trigger1` and `trigger2` field without the `trigger` or `presupposition` field. 
Nominally, most examples look like the example in the Data Instances section above. Occassionally, however, some examples will look like:
```buildoutcfg
{
'sentence1': 'Did that committee know when Lissa walked through the cafe?', 
'sentence2': 'That committee knew when Lissa walked through the cafe.', 
'trigger1': 'interrogative', 
'trigger2': 'unembedded', 
'gold_label': 'neutral', 
'control_item': True, 
'UID': 'question_presupposition', 
'pairID': '1821n', 
'paradigmID': 95
}
```
In this example, `trigger1` and `trigger2` appear and `presupposition` and `trigger` are removed. This maintains the length of the dictionary.
To account for these examples, we have thus introduced the mapping above such that all examples accessed through the HF Datasets interface will have the same size as well as the same fields.
In the event that an example does not have a value for one of the fields, the field is maintained in the dictionary but given a value of `Not_In_Example`. 

To illustrate this point, the example given in the Data Instances section above would look like the following in the HF Datasets:
```buildoutcfg
{
"premise": "All ten guys that proved to boast might have been divorcing.", 
"hypothesis": "There are exactly ten guys that proved to boast.", 
"trigger": "modal",
"trigger1":  "Not_In_Example",
"trigger2": "Not_In_Example"
"presupposition": "positive", 
"gold_label": "entailment", 
"UID": "all_n_presupposition", 
"pairID": "9e", 
"paradigmID": 0
}
```

Below is description of the fields:
```buildoutcfg
"premise": The premise. 
"hypothesis": The hypothesis. 
"trigger": A detailed discussion of trigger types appears in the paper.
"trigger1":  A detailed discussion of trigger types appears in the paper.
"trigger2": A detailed discussion of trigger types appears in the paper.
"presupposition": positive or negative. 
"gold_label": Corresponds to entailment, contradiction, or neutral. 
"UID": Unique id. 
"pairID": Sentence pair ID.
"paradigmID": ?
```
It is not immediately clear what the difference is between `trigger`, `trigger1`, and `trigger2` is or what the `paradigmID` refers to.

**Implicature**

The `implicature` fields only have the mapping below:
```buildoutcfg
"premise" -> "sentence1"
"hypothesis"-> "sentence2"
```
Here is a description of the fields:
```buildoutcfg
"premise": The premise. 
"hypothesis": The hypothesis. 
"gold_label_log": Gold label for a logical reading of the sentence pair.
"gold_label_prag": Gold label for a pragmatic reading of the sentence pair.
"spec_relation": ?
"item_type": ?
"trigger": A detailed discussion of trigger types appears in the paper.
"lexemes": ? 
```

### Data Splits

As the dataset was created to test already trained models, the only split that exists is for testing.


## Dataset Creation

### Curation Rationale

IMPPRES was created to evaluate how well trained NLI models recognize several classes of presuppositions and scalar implicatures.

### Source Data

#### Initial Data Collection and Normalization

[More Information Needed]

#### Who are the source language producers?

[More Information Needed]

### Annotations

#### Annotation process

[More Information Needed]

#### Who are the annotators?

The annotations were generated semi-automatically.

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

IMPPRES is available under a Creative Commons Attribution-NonCommercial 4.0 International Public License ("The License"). You may not use these files except in compliance with the License. Please see the LICENSE file for more information before you use the dataset.

### Citation Information

```buildoutcfg
@inproceedings{jeretic-etal-2020-natural,
    title = "Are Natural Language Inference Models {IMPPRESsive}? {L}earning {IMPlicature} and {PRESupposition}",
    author = "Jereti\v{c}, Paloma  and
      Warstadt, Alex  and
      Bhooshan, Suvrat  and
      Williams, Adina",
    booktitle = "Proceedings of the 58th Annual Meeting of the Association for Computational Linguistics",
    month = jul,
    year = "2020",
    address = "Online",
    publisher = "Association for Computational Linguistics",
    url = "https://www.aclweb.org/anthology/2020.acl-main.768",
    doi = "10.18653/v1/2020.acl-main.768",
    pages = "8690--8705",
    abstract = "Natural language inference (NLI) is an increasingly important task for natural language understanding, which requires one to infer whether a sentence entails another. However, the ability of NLI models to make pragmatic inferences remains understudied. We create an IMPlicature and PRESupposition diagnostic dataset (IMPPRES), consisting of 32K semi-automatically generated sentence pairs illustrating well-studied pragmatic inference types. We use IMPPRES to evaluate whether BERT, InferSent, and BOW NLI models trained on MultiNLI (Williams et al., 2018) learn to make pragmatic inferences. Although MultiNLI appears to contain very few pairs illustrating these inference types, we find that BERT learns to draw pragmatic inferences. It reliably treats scalar implicatures triggered by {``}some{''} as entailments. For some presupposition triggers like {``}only{''}, BERT reliably recognizes the presupposition as an entailment, even when the trigger is embedded under an entailment canceling operator like negation. BOW and InferSent show weaker evidence of pragmatic reasoning. We conclude that NLI training encourages models to learn some, but not all, pragmatic inferences.",
}
```

### Contributions

Thanks to [@aclifton314](https://github.com/aclifton314) for adding this dataset.