---
annotations_creators:
- no-annotation
language_creators:
- expert-generated
languages:
- en
licenses:
[
  "cc-by-nc-sa-2.0",
  "cc-by-nc-2.0",
  "cc-by-nd-2.0",
  "cc-by-sa-2.0",
  "cc-by-nc-nd-2.0",
  "cc-by-nc-1.0",
  "other-cc0",
  "other-hybrid-oa",
  "other-els-covid",
  "other-no-cc",
  "other-gold-oa",
  "other-green-oa",
  "other-bronze-oa",
  "other-biorxiv",
  "other-arxiv",
  "other-medrxiv",
  "other-unk"
]
multilinguality:
- monolingual
size_categories:
- 100K<n<1M
source_datasets:
- original
task_categories:
- other
task_ids:
- other-other-knowledge-extraction
---

# Dataset Card Creation Guide

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

- **Homepage:** [https://www.semanticscholar.org/cord19](https://www.semanticscholar.org/cord19)
- **Repository:** [https://github.com/allenai/cord19](https://github.com/allenai/cord19)
- **Paper:** [CORD-19: The COVID-19 Open Research Dataset](https://www.aclweb.org/anthology/2020.nlpcovid19-acl.1/)
- **Leaderboard:** [Kaggle challenge](https://www.kaggle.com/allen-institute-for-ai/CORD-19-research-challenge)


### Dataset Summary

CORD-19 is a corpus of academic papers about COVID-19 and related coronavirus research.  It's curated and maintained by the Semantic Scholar team at the Allen Institute for AI to support text mining and NLP research.

### Supported Tasks and Leaderboards

See tasks defined in the related [Kaggle challenge](https://www.kaggle.com/allen-institute-for-ai/CORD-19-research-challenge/tasks)

### Languages

The dataset is in english (en).

## Dataset Structure

### Data Instances

TODO

### Data Fields

Currently only the following fields are integrated: `cord_uid`, `sha`,`source_x`, `title`, `doi`, `abstract`, `publish_time`, `authors`, `journal`
- `cord_uid`:  A `str`-valued field that assigns a unique identifier to each CORD-19 paper.  This is not necessariy unique per row, which is explained in the FAQs.
- `sha`:  A `List[str]`-valued field that is the SHA1 of all PDFs associated with the CORD-19 paper.  Most papers will have either zero or one value here (since we either have a PDF or we don't), but some papers will have multiple.  For example, the main paper might have supplemental information saved in a separate PDF.  Or we might have two separate PDF copies of the same paper.  If multiple PDFs exist, their SHA1 will be semicolon-separated (e.g. `'4eb6e165ee705e2ae2a24ed2d4e67da42831ff4a; d4f0247db5e916c20eae3f6d772e8572eb828236'`)
- `source_x`:  A `List[str]`-valued field that is the names of sources from which we received this paper.  Also semicolon-separated.  For example, `'ArXiv; Elsevier; PMC; WHO'`.  There should always be at least one source listed.
- `title`:  A `str`-valued field for the paper title
- `doi`: A `str`-valued field for the paper DOI
- `pmcid`: A `str`-valued field for the paper's ID on PubMed Central.  Should begin with `PMC` followed by an integer.
- `pubmed_id`: An `int`-valued field for the paper's ID on PubMed.  
- `license`: A `str`-valued field with the most permissive license we've found associated with this paper.  Possible values include:  `'cc0', 'hybrid-oa', 'els-covid', 'no-cc', 'cc-by-nc-sa', 'cc-by', 'gold-oa', 'biorxiv', 'green-oa', 'bronze-oa', 'cc-by-nc', 'medrxiv', 'cc-by-nd', 'arxiv', 'unk', 'cc-by-sa', 'cc-by-nc-nd'`
- `abstract`: A `str`-valued field for the paper's abstract
- `publish_time`:  A `str`-valued field for the published date of the paper.  This is in `yyyy-mm-dd` format.  Not always accurate as some publishers will denote unknown dates with future dates like `yyyy-12-31`
- `authors`:  A `List[str]`-valued field for the authors of the paper.  Each author name is in `Last, First Middle` format and semicolon-separated.
- `journal`:  A `str`-valued field for the paper journal.  Strings are not normalized (e.g. `BMJ` and `British Medical Journal` can both exist). Empty string if unknown.
- `mag_id`:  Deprecated, but originally an `int`-valued field for the paper as represented in the Microsoft Academic Graph.
- `who_covidence_id`:  A `str`-valued field for the ID assigned by the WHO for this paper.  Format looks like `#72306`. 
- `arxiv_id`:  A `str`-valued field for the arXiv ID of this paper.
- `pdf_json_files`:  A `List[str]`-valued field containing paths from the root of the current data dump version to the parses of the paper PDFs into JSON format.  Multiple paths are semicolon-separated.  Example: `document_parses/pdf_json/4eb6e165ee705e2ae2a24ed2d4e67da42831ff4a.json; document_parses/pdf_json/d4f0247db5e916c20eae3f6d772e8572eb828236.json`
- `pmc_json_files`:  A `List[str]`-valued field.  Same as above, but corresponding to the full text XML files downloaded from PMC, parsed into the same JSON format as above.
- `url`: A `List[str]`-valued field containing all URLs associated with this paper.  Semicolon-separated.
- `s2_id`:  A `str`-valued field containing the Semantic Scholar ID for this paper.  Can be used with the Semantic Scholar API (e.g. `s2_id=9445722` corresponds to `http://api.semanticscholar.org/corpusid:9445722`)

### Data Splits

No annotation provided in this dataset so all instances are provided in training split.

## Dataset Creation

### Curation Rationale

See [official readme](https://github.com/allenai/cord19/blob/master/README.md)

### Source Data

See [official readme](https://github.com/allenai/cord19/blob/master/README.md)

#### Initial Data Collection and Normalization

See [official readme](https://github.com/allenai/cord19/blob/master/README.md)

#### Who are the source language producers?

See [official readme](https://github.com/allenai/cord19/blob/master/README.md)

### Annotations

No annotations

#### Annotation process

N/A

#### Who are the annotators?

N/A

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

[More Information Needed]

### Citation Information

```
@article{Wang2020CORD19TC,
  title={CORD-19: The Covid-19 Open Research Dataset},
  author={Lucy Lu Wang and Kyle Lo and Yoganand Chandrasekhar and Russell Reas and Jiangjiang Yang and Darrin Eide and
  K. Funk and Rodney Michael Kinney and Ziyang Liu and W. Merrill and P. Mooney and D. Murdick and Devvret Rishi and
  Jerry Sheehan and Zhihong Shen and B. Stilson and A. Wade and K. Wang and Christopher Wilhelm and Boya Xie and
  D. Raymond and Daniel S. Weld and Oren Etzioni and Sebastian Kohlmeier},
  journal={ArXiv},
  year={2020}
}
```