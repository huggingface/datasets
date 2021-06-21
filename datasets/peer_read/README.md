---
annotations_creators:
- expert-generated
language_creators:
- found
languages:
- en
licenses:
- unknown
multilinguality:
- monolingual
size_categories:
- 10K<n<100K
source_datasets:
- original
task_categories:
- text-classification
task_ids:
- text-classification-other-acceptability-classification
paperswithcode_id: peerread
---

# Dataset Card for peer_read

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

- **Homepage:** https://arxiv.org/abs/1804.09635
- **Repository:** https://github.com/allenai/PeerRead
- **Paper:** https://arxiv.org/pdf/1804.09635.pdf
- **Leaderboard:** [Needs More Information]
- **Point of Contact:** [Needs More Information]

### Dataset Summary

PearRead is a dataset of scientific peer reviews available to help researchers study this important artifact. The dataset consists of over 14K paper drafts and the corresponding accept/reject decisions in top-tier venues including ACL, NIPS and ICLR, as well as over 10K textual peer reviews written by experts for a subset of the papers.

### Supported Tasks and Leaderboards

[More Information Needed]

### Languages

en-English

## Dataset Structure

### Data Instances

[More Information Needed]

### Data Fields

#### parsed_pdfs
- `name`: `string` Filename in the dataset
- `metadata`: `dict` Paper metadata
    - `source`: `string` Paper source
    - `authors`: `list<string>` List of paper authors
    - `title`: `string` Paper title
    - `sections`: `list<dict>` List of section heading and corresponding description
        - `heading`: `string` Section heading
        - `text`: `string` Section description
    - `references`: `string` List of references
        - `title`: `string` Title of reference paper
        - `author`: `list<string>` List of reference paper authors
        - `venue`: `string` Reference venue
        - `citeRegEx`: `string` Reference citeRegEx
        - `shortCiteRegEx`: `string` Reference shortCiteRegEx
        - `year`: `int` Reference publish year
    - `referenceMentions`: `list<string>` List of reference mentions
        - `referenceID`: `int` Reference mention ID
        - `context`: `string` Reference mention context
        - `startOffset`: `int` Reference startOffset
        - `endOffset`: `int` Reference endOffset
    - `year`: `int` Paper publish year
    - `abstractText`: `string` Paper abstract
    - `creator`: `string` Paper creator

#### reviews
- `id`: `int` Review ID
- `conference`: `string` Conference name
- `comments`: `string` Review comments
- `subjects`: `string` Review subjects
- `version`: `string` Review version
- `date_of_submission`: `string`  Submission date
- `title`: `string` Paper title
- `authors`: `list<string>` List of paper authors
- `accepted`: `bool` Paper accepted flag
- `abstract`: `string` Paper abstract
- `histories`: `list<string>` Paper details with link
- `reviews`: `dict` Paper reviews
    - `date`: `string` Date of review
    - `title`: `string` Paper title
    - `other_keys`: `string` Reviewer other details
    - `originality`: `string` Originality score
    - `comments`: `string` Reviewer comments
    - `is_meta_review`: `bool` Review type flag
    - `recommendation`: `string` Reviewer recommendation
    - `replicability`: `string` Replicability score
    - `presentation_format`: `string` Presentation type
    - `clarity`: `string` Clarity score
    - `meaningful_comparison`: `string` Meaningful comparison score
    - `substance`: `string` Substance score
    - `reviewer_confidence`: `string` Reviewer confidence score
    - `soundness_correctness`: `string` Soundness correctness score
    - `appropriateness`: `string` Appropriateness score
    - `impact`: `string` Impact score
    
### Data Splits

[More Information Needed]

## Dataset Creation

### Curation Rationale

[More Information Needed]

### Source Data

#### Initial Data Collection and Normalization

[More Information Needed]

#### Who are the source language producers?

[More Information Needed]

### Annotations

#### Annotation process

[More Information Needed]

#### Who are the annotators?

[More Information Needed]

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

Dongyeop Kang, Waleed Ammar, Bhavana Dalvi Mishra, Madeleine van Zuylen, Sebastian Kohlmeier, Eduard Hovy, Roy Schwartz

### Licensing Information

[More Information Needed]

### Citation Information

@inproceedings{kang18naacl,
  title = {A Dataset of Peer Reviews (PeerRead): Collection, Insights and NLP Applications},
  author = {Dongyeop Kang and Waleed Ammar and Bhavana Dalvi and Madeleine van Zuylen and Sebastian Kohlmeier and Eduard Hovy and Roy Schwartz},
  booktitle = {Meeting of the North American Chapter of the Association for Computational Linguistics (NAACL)},
  address = {New Orleans, USA},
  month = {June},
  url = {https://arxiv.org/abs/1804.09635},
  year = {2018}
}

### Contributions

Thanks to [@vinaykudari](https://github.com/vinaykudari) for adding this dataset.