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
pretty_name: Eraser MultiRC (Multi-Sentence Reading Comprehension)
size_categories:
- 10K<n<100K
source_datasets:
- original
task_categories:
- multiple-choice
task_ids:
- multiple-choice-qa
- multiple-choice-other-inference
paperswithcode_id: null
dataset_info:
  features:
  - name: passage
    dtype: string
  - name: query_and_answer
    dtype: string
  - name: label
    dtype:
      class_label:
        names:
          0: 'False'
          1: 'True'
  - name: evidences
    sequence: string
  splits:
  - name: test
    num_bytes: 9194475
    num_examples: 4848
  - name: train
    num_bytes: 47922877
    num_examples: 24029
  - name: validation
    num_bytes: 6529020
    num_examples: 3214
  download_size: 1667550
  dataset_size: 63646372
---

# Dataset Card for "eraser_multi_rc"

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

- **Homepage:** http://cogcomp.org/multirc/
- **Repository:** https://github.com/CogComp/multirc
- **Paper:** [Looking Beyond the Surface: A Challenge Set for Reading Comprehension over Multiple Sentences](https://cogcomp.seas.upenn.edu/page/publication_view/833)
- **Point of Contact:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Size of downloaded dataset files:** 1.59 MB
- **Size of the generated dataset:** 60.70 MB
- **Total amount of disk used:** 62.29 MB

### Dataset Summary

MultiRC (Multi-Sentence Reading Comprehension) is a dataset of short paragraphs and multi-sentence questions that can be answered from the content of the paragraph.

We have designed the dataset with three key challenges in mind:
- The number of correct answer-options for each question is not pre-specified. This removes the over-reliance of current approaches on answer-options and forces them to decide on the correctness of each candidate answer independently of others. In other words, unlike previous work, the task here is not to simply identify the best answer-option, but to evaluate the correctness of each answer-option individually.
- The correct answer(s) is not required to be a span in the text.
- The paragraphs in our dataset have diverse provenance by being extracted from 7 different domains such as news, fiction, historical text etc., and hence are expected to be more diverse in their contents as compared to single-domain datasets.

The goal of this dataset is to encourage the research community to explore approaches that can do more than sophisticated lexical-level matching. 

### Supported Tasks and Leaderboards

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Languages

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

## Dataset Structure

### Data Instances

#### default

- **Size of downloaded dataset files:** 1.59 MB
- **Size of the generated dataset:** 60.70 MB
- **Total amount of disk used:** 62.29 MB

An example of 'validation' looks as follows.
```
This example was too long and was cropped:

{
    "evidences": "[\"Allan sat down at his desk and pulled the chair in close .\", \"Opening a side drawer , he took out a piece of paper and his ink...",
    "label": 0,
    "passage": "\"Allan sat down at his desk and pulled the chair in close .\\nOpening a side drawer , he took out a piece of paper and his inkpot...",
    "query_and_answer": "Name few objects said to be in or on Allan 's desk || Eraser"
}
```

### Data Fields

The data fields are the same among all splits.

#### default
- `passage`: a `string` feature.
- `query_and_answer`: a `string` feature.
- `label`: a classification label, with possible values including `False` (0), `True` (1).
- `evidences`: a `list` of `string` features.

### Data Splits

| name  |train|validation|test|
|-------|----:|---------:|---:|
|default|24029|      3214|4848|

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

https://github.com/CogComp/multirc/blob/master/LICENSE

Research and Academic Use License
Cognitive Computation Group
University of Illinois at Urbana-Champaign

Downloading software implies that you accept the following license terms:

Under this Agreement, The Board of Trustees of the University of Illinois ("University"), a body corporate and politic of the State of Illinois with its principal offices at 506 South Wright Street, Urbana, Illinois 61801, U.S.A., on behalf of its Department of Computer Science on the Urbana-Champaign Campus, provides the software ("Software") described in Appendix A, attached hereto and incorporated herein, to the Licensee identified below ("Licensee") subject to the following conditions:

	1. Upon execution of this Agreement by Licensee below, the University grants, and Licensee accepts, a roylaty-free, non-exclusive license:
		A. To use unlimited copies of the Software for its own academic and research purposes.
		B. To make derivative works. However, if Licensee distributes any derivative work based on or derived from the Software (with such distribution limited to binary form only), then Licensee will (1) notify the University (c/o Professor Dan Roth, e-mail: danr@cs.uiuc.edu) regarding its distribution of the derivative work and provide a copy if requested, and (2) clearly notify users that such derivative work is a modified version and not the original Software distributed by the University.
		C. To redistribute (sublicense) derivative works based on the Software in binary form only to third parties provided that (1) the copyright notice and any accompanying legends or proprietary notices are reproduced on all copies, (2) no royalty is charged for such copies, and (3) third parties are restricted to using the derivative work for academic and research purposes only, without further sublicensing rights.
	No license is granted herein that would permit Licensee to incorporate the Software into a commercial product, or to otherwise commercially exploit the Software. Should Licensee wish to make commercial use of the Software, Licensee should contact the University, c/o the Office of Technology Management ("OTM") to negotiate an appropriate license for such commercial use. To contact the OTM: otmmailaccount@ad.uiuc.edu; telephone: (217)333-3781;  fax: (217) 265-5530.
	2. THE UNIVERSITY GIVES NO WARRANTIES, EITHER EXPRESSED OR IMPLIED, FOR THE SOFTWARE AND/OR ASSOCIATED MATERIALS PROVIDED UNDER THIS AGREEMENT, INCLUDING, WITHOUT LIMITATION, WARRANTY OF MERCHANTABILITY AND WARRANTY OF FITNESS FOR A PARTICULAR PURPOSE, AND ANY WARRANTY AGAINST INFRINGEMENT OF ANY INTELLECTUAL PROPERTY RIGHTS.
	3. Licensee understands the Software is a research tool for which no warranties as to capabilities or accuracy are made, and Licensee accepts the Software on an "as is, with all defects" basis, without maintenance, debugging , support or improvement. Licensee assumes the entire risk as to the results and performance of the Software and/or associated materials. Licensee agrees that University shall not be held liable for any direct, indirect, consequential, or incidental damages with respect to any claim by Licensee or any third party on account of or arising from this Agreement or use of the Software and/or associated materials.
	4. Licensee understands the Software is proprietary to the University. Licensee will take all reasonable steps to insure that the source code is protected and secured from unauthorized disclosure, use, or release and will treat it with at least the same level of care as Licensee would use to protect and secure its own proprietary computer programs and/or information, but using no less than reasonable care.
	5. In the event that Licensee shall be in default in the performance of any material obligations under this Agreement, and if the default has not been remedied within sixty (60) days after the date of notice in writing of such default, University may terminate this Agreement by written notice. In the event of termination, Licensee shall promptly return to University the original and any copies of licensed Software in Licensee's possession. In the event of any termination of this Agreement, any and all sublicenses granted by Licensee to third parties pursuant to this Agreement (as permitted by this Agreement) prior to the date of such termination shall nevertheless remain in full force and effect.
	6. The Software was developed, in part, with support from the National Science Foundation, and the Federal Government has certain license rights in the Software.
	7. This Agreement shall be construed and interpreted in accordance with the laws of the State of Illinois, U.S.A..
	8. This Agreement shall be subject to all United States Government laws and regulations now and hereafter applicable to the subject matter of this Agreement, including specifically the Export Law provisions of the Departments of Commerce and State. Licensee will not export or re-export the Software without the appropriate United States or foreign government license.

By its registration below, Licensee confirms that it understands the terms and conditions of this Agreement, and agrees to be bound by them. This Agreement shall become effective as of the date of execution by Licensee.

### Citation Information

```
@unpublished{eraser2019,
    title = {ERASER: A Benchmark to Evaluate Rationalized NLP Models},
    author = {Jay DeYoung and Sarthak Jain and Nazneen Fatema Rajani and Eric Lehman and Caiming Xiong and Richard Socher and Byron C. Wallace}
}
@inproceedings{MultiRC2018,
    author = {Daniel Khashabi and Snigdha Chaturvedi and Michael Roth and Shyam Upadhyay and Dan Roth},
    title = {Looking Beyond the Surface:A Challenge Set for Reading Comprehension over Multiple Sentences},
    booktitle = {Proceedings of North American Chapter of the Association for Computational Linguistics (NAACL)},
    year = {2018}
}
```

### Contributions

Thanks to [@lewtun](https://github.com/lewtun), [@patrickvonplaten](https://github.com/patrickvonplaten), [@thomwolf](https://github.com/thomwolf) for adding this dataset.