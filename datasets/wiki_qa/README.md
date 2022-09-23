---
annotations_creators:
- crowdsourced
language:
- en
language_creators:
- found
license:
- other
multilinguality:
- monolingual
pretty_name: WikiQA
size_categories:
- 10K<n<100K
source_datasets:
- original
task_categories:
- question-answering
task_ids:
- open-domain-qa
paperswithcode_id: wikiqa
dataset_info:
  features:
  - name: question_id
    dtype: string
  - name: question
    dtype: string
  - name: document_title
    dtype: string
  - name: answer
    dtype: string
  - name: label
    dtype:
      class_label:
        names:
          0: '0'
          1: '1'
  splits:
  - name: test
    num_bytes: 1337903
    num_examples: 6165
  - name: train
    num_bytes: 4469148
    num_examples: 20360
  - name: validation
    num_bytes: 591833
    num_examples: 2733
  download_size: 7094233
  dataset_size: 6398884
---

# Dataset Card for "wiki_qa"

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

- **Homepage:** [https://www.microsoft.com/en-us/download/details.aspx?id=52419](https://www.microsoft.com/en-us/download/details.aspx?id=52419)
- **Repository:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Paper:** [WikiQA: A Challenge Dataset for Open-Domain Question Answering](https://aclanthology.org/D15-1237/)
- **Point of Contact:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Size of downloaded dataset files:** 6.77 MB
- **Size of the generated dataset:** 6.10 MB
- **Total amount of disk used:** 12.87 MB

### Dataset Summary

Wiki Question Answering corpus from Microsoft.

The WikiQA corpus is a publicly available set of question and sentence pairs, collected and annotated for research on open-domain question answering.

### Supported Tasks and Leaderboards

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Languages

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

## Dataset Structure

### Data Instances

#### default

- **Size of downloaded dataset files:** 6.77 MB
- **Size of the generated dataset:** 6.10 MB
- **Total amount of disk used:** 12.87 MB

An example of 'train' looks as follows.
```
{
    "answer": "Glacier caves are often called ice caves , but this term is properly used to describe bedrock caves that contain year-round ice.",
    "document_title": "Glacier cave",
    "label": 0,
    "question": "how are glacier caves formed?",
    "question_id": "Q1"
}
```

### Data Fields

The data fields are the same among all splits.

#### default
- `question_id`: a `string` feature.
- `question`: a `string` feature.
- `document_title`: a `string` feature.
- `answer`: a `string` feature.
- `label`: a classification label, with possible values including `0` (0), `1` (1).

### Data Splits

| name  |train|validation|test|
|-------|----:|---------:|---:|
|default|20360|      2733|6165|

## Dataset Creation

### Curation Rationale

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Source Data

#### Initial Data Collection and Normalization

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

#### Who are the source language producers?

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Annotations

#### Annotation process

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

#### Who are the annotators?

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Personal and Sensitive Information

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

## Considerations for Using the Data

### Social Impact of Dataset

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Discussion of Biases

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Other Known Limitations

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

## Additional Information

### Dataset Curators

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Licensing Information

MICROSOFT RESEARCH DATA LICENSE AGREEMENT
FOR
MICROSOFT RESEARCH WIKIQA CORPUS

These license terms are an agreement between Microsoft Corporation (or based on where you live, one of its
affiliates) and you. Please read them. They apply to the data associated with this license above, which includes
the media on which you received it, if any. The terms also apply to any Microsoft:
- updates,
- supplements,
- Internet-based services, and
- support services
for this data, unless other terms accompany those items. If so, those terms apply.
BY USING THE DATA, YOU ACCEPT THESE TERMS. IF YOU DO NOT ACCEPT THEM, DO NOT USE THE DATA.
If you comply with these license terms, you have the rights below.

1. SCOPE OF LICENSE.
a. You may use, copy, modify, create derivative works, and distribute the Dataset:
i. for research and technology development purposes only. Examples of research and technology
development uses are teaching, academic research, public demonstrations and experimentation ;
and
ii. to publish (or present papers or articles) on your results from using such Dataset.
b. The data is licensed, not sold. This agreement only gives you some rights to use the data. Microsoft reserves
all other rights. Unless applicable law gives you more rights despite this limitation, you may use the data only
as expressly permitted in this agreement. In doing so, you must comply with any technical limitations in the
data that only allow you to use it in certain ways.
You may not
- work around any technical limitations in the data;
- reverse engineer, decompile or disassemble the data, except and only to the extent that applicable law
expressly permits, despite this limitation;
- rent, lease or lend the data;
- transfer the data or this agreement to any third party; or
- use the data directly in a commercial product without Microsoft’s permission.

2. DISTRIBUTION REQUIREMENTS:
a. If you distribute the Dataset or any derivative works of the Dataset, you will distribute them under the
same terms and conditions as in this Agreement, and you will not grant other rights to the Dataset or
derivative works that are different from those provided by this Agreement.
b. If you have created derivative works of the Dataset, and distribute such derivative works, you will
cause the modified files to carry prominent notices so that recipients know that they are not receiving
Page 1 of 3the original Dataset. Such notices must state: (i) that you have changed the Dataset; and (ii) the date
of any changes.

3. DISTRIBUTION RESTRICTIONS. You may not: (a) alter any copyright, trademark or patent notice in the
Dataset; (b) use Microsoft’s trademarks in a way that suggests your derivative works or modifications come from
or are endorsed by Microsoft; (c) include the Dataset in malicious, deceptive or unlawful programs.

4. OWNERSHIP. Microsoft retains all right, title, and interest in and to any Dataset provided to you under this
Agreement. You acquire no interest in the Dataset you may receive under the terms of this Agreement.

5. LICENSE TO MICROSOFT. Microsoft is granted back, without any restrictions or limitations, a non-exclusive,
perpetual, irrevocable, royalty-free, assignable and sub-licensable license, to reproduce, publicly perform or
display, use, modify, post, distribute, make and have made, sell and transfer your modifications to and/or
derivative works of the Dataset, for any purpose.

6. FEEDBACK. If you give feedback about the Dataset to Microsoft, you give to Microsoft, without charge, the right
to use, share and commercialize your feedback in any way and for any purpose. You also give to third parties,
without charge, any patent rights needed for their products, technologies and services to use or interface with
any specific parts of a Microsoft dataset or service that includes the feedback. You will not give feedback that is
subject to a license that requires Microsoft to license its Dataset or documentation to third parties because we
include your feedback in them. These rights survive this Agreement.

7. EXPORT RESTRICTIONS. The Dataset is subject to United States export laws and regulations. You must
comply with all domestic and international export laws and regulations that apply to the Dataset. These laws
include restrictions on destinations, end users and end use. For additional information, see
www.microsoft.com/exporting.

8. ENTIRE AGREEMENT. This Agreement, and the terms for supplements, updates, Internet-based services and
support services that you use, are the entire agreement for the Dataset.

9. SUPPORT SERVICES. Because this data is “as is,” we may not provide support services for it.

10. APPLICABLE LAW.
a. United States. If you acquired the software in the United States, Washington state law governs the
interpretation of this agreement and applies to claims for breach of it, regardless of conflict of laws principles.
The laws of the state where you live govern all other claims, including claims under state consumer protection
laws, unfair competition laws, and in tort.
b. Outside the United States. If you acquired the software in any other country, the laws of that country
apply.

11. LEGAL EFFECT. This Agreement describes certain legal rights. You may have other rights under the laws of your
country. You may also have rights with respect to the party from whom you acquired the Dataset. This
Agreement does not change your rights under the laws of your country if the laws of your country do not permit
it to do so.

12. DISCLAIMER OF WARRANTY. The Dataset is licensed “as-is.” You bear the risk of using it. Microsoft gives no
express warranties, guarantees or conditions. You may have additional consumer rights or statutory guarantees
under your local laws which this agreement cannot change. To the extent permitted under your local laws,
Microsoft excludes the implied warranties of merchantability, fitness for a particular purpose and non-
infringement.

13. LIMITATION ON AND EXCLUSION OF REMEDIES AND DAMAGES. YOU CAN RECOVER FROM
MICROSOFT AND ITS SUPPLIERS ONLY DIRECT DAMAGES UP TO U.S. $5.00. YOU CANNOT RECOVER ANY
OTHER DAMAGES, INCLUDING CONSEQUENTIAL, LOST PROFITS, SPECIAL, INDIRECT OR INCIDENTAL
DAMAGES.

This limitation applies to
- anything related to the software, services, content (including code) on third party Internet sites, or third party
programs; and Page 2 of 3
- claims for breach of contract, breach of warranty, guarantee or condition, strict liability, negligence, or other
 tort to the extent permitted by applicable law.

It also applies even if Microsoft knew or should have known about the possibility of the damages. The above
limitation or exclusion may not apply to you because your country may not allow the exclusion or limitation of
incidental, consequential or other damages.

### Citation Information

```
@inproceedings{yang-etal-2015-wikiqa,
    title = "{W}iki{QA}: A Challenge Dataset for Open-Domain Question Answering",
    author = "Yang, Yi  and
      Yih, Wen-tau  and
      Meek, Christopher",
    booktitle = "Proceedings of the 2015 Conference on Empirical Methods in Natural Language Processing",
    month = sep,
    year = "2015",
    address = "Lisbon, Portugal",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/D15-1237",
    doi = "10.18653/v1/D15-1237",
    pages = "2013--2018",
}
```

### Contributions

Thanks to [@patrickvonplaten](https://github.com/patrickvonplaten), [@mariamabarham](https://github.com/mariamabarham), [@lewtun](https://github.com/lewtun), [@thomwolf](https://github.com/thomwolf) for adding this dataset.