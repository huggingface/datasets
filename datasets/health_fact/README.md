---
annotations_creators:
- expert-generated
language_creators:
- found
languages:
- en
licenses:
- mit
multilinguality:
- monolingual
size_categories:
- 10K<n<100K
source_datasets:
- original
task_categories:
- text-classification
task_ids:
- fact-checking
- multi-class-classification
---

# Dataset Card for PUBHEALTH

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

- **Homepage:** [PUBHEALTH homepage](https://github.com/neemakot/Health-Fact-Checking)
- **Repository:** [PUBHEALTH repository](https://github.com/neemakot/Health-Fact-Checking/blob/master/data/DATASHEET.md)
- **Paper:** [Explainable Automated Fact-Checking for Public Health Claims"](https://arxiv.org/abs/2010.09926)
- **Point of Contact:**[Neema Kotonya](mailto:nk2418@ic.ac.uk)

### Dataset Summary

PUBHEALTH is a comprehensive dataset for explainable automated fact-checking of public health claims. Each instance in the PUBHEALTH dataset has an associated veracity label (true, false, unproven, mixture). Furthermore each instance in the dataset has an explanation text field. The explanation is a justification for which the claim has been assigned a particular veracity label.

### Supported Tasks and Leaderboards

[More Information Needed]

### Languages

The text in the dataset is in English.

## Dataset Structure

### Data Instances

The following is an example instance of the PUBHEALTH dataset:
|  Field              |  Example                                                     |
| -----------------   | -------------------------------------------------------------|
| __claim__  	      | Expired boxes of cake and pancake mix are dangerously toxic. |
| __explanation__     | What's True:  Pancake and cake mixes that contain mold can cause life-threatening allergic reactions. What's False: Pancake and cake mixes that have passed their expiration dates are not inherently dangerous to ordinarily healthy people, and the yeast in packaged baking products does not "over time develops spores." |
| __label__           |  mixture                                                     |
| __author(s)__       | David Mikkelson                                              |
| __date published__  | April 19, 2006                                               |
| __tags__            | food, allergies, baking, cake                                |
| __main_text__        |   In April 2006, the experience of a 14-year-old who had eaten pancakes made from a mix that had gone moldy was described in the popular newspaper column Dear Abby. The account has since been circulated widely on the Internet as scores of concerned homemakers ponder the safety of the pancake and other baking mixes lurking in their larders [...]       |
| __evidence sources__    | [1] Bennett, Allan and Kim Collins.  “An Unusual Case of Anaphylaxis: Mold in Pancake Mix.” American Journal of Forensic Medicine & Pathology.   September 2001   (pp. 292-295). [2] Phillips, Jeanne. “Dear Abby.” 14 April 2006   [syndicated column]. |

### Data Fields

Mentioned above in data instances.

### Data Splits

|           | # Instances |
|-----------|-------------|
| train.tsv | 9832        |
| dev.tsv   | 1221        |
| test.tsv  | 1235        |
| total     | 12288       |


## Dataset Creation

### Curation Rationale

The dataset was created to explore fact-checking of difficult to verify claims i.e., those which require expertise from outside of the journalistics domain, in this case biomedical and public health expertise.

It was also created in response to the lack of fact-checking datasets which provide gold standard natural language explanations for verdicts/labels.

### Source Data

#### Initial Data Collection and Normalization

The dataset was retrieved from the following fact-checking, news reviews and news websites:

| URL                               | Type               |
|-----------------------------------|--------------------|
| http://snopes.com/                | fact-checking      |
| http://politifact.com/            | fact-checking      |
| http://truthorfiction.com/        | fact-checking      |
| https://www.factcheck.org/        | fact-checking      |
| https://fullfact.org/             | fact-checking      |
| https://apnews.com/               | news               |
| https://uk.reuters.com/           | news               |
| https://www.healthnewsreview.org/ | health news review |

#### Who are the source language producers?

[More Information Needed]

### Annotations

#### Annotation process

[More Information Needed]

#### Who are the annotators?

[More Information Needed]

### Personal and Sensitive Information

Not to our knowledge, but if it is brought to our attention that we are mistaken we will make the appropriate corrections to the dataset.

## Considerations for Using the Data

### Social Impact of Dataset

[More Information Needed]

### Discussion of Biases

[More Information Needed]

### Other Known Limitations

[More Information Needed]

## Additional Information

### Dataset Curators

The dataset was created by Neema Kotonya, and Francesca Toni, for their research paper "Explainable Automated Fact-Checking for Public Health Claims" presented at EMNLP 2020.

### Licensing Information

MIT License

### Citation Information
```
@inproceedings{kotonya-toni-2020-explainable,
    title = "Explainable Automated Fact-Checking for Public Health Claims",
    author = "Kotonya, Neema  and
      Toni, Francesca",
    booktitle = "Proceedings of the 2020 Conference on Empirical Methods in Natural Language Processing (EMNLP)",
    month = nov,
    year = "2020",
    address = "Online",
    publisher = "Association for Computational Linguistics",
    url = "https://www.aclweb.org/anthology/2020.emnlp-main.623",
    pages = "7740--7754",
}
```