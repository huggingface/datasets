---
annotations_creators:
- expert-generated
language_creators:
- found
language:
- en
license:
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
pretty_name: PeerRead
dataset_info:
- config_name: parsed_pdfs
  features:
  - name: name
    dtype: string
  - name: metadata
    struct:
    - name: source
      dtype: string
    - name: title
      dtype: string
    - name: authors
      sequence: string
    - name: emails
      sequence: string
    - name: sections
      sequence:
      - name: heading
        dtype: string
      - name: text
        dtype: string
    - name: references
      sequence:
      - name: title
        dtype: string
      - name: author
        sequence: string
      - name: venue
        dtype: string
      - name: citeRegEx
        dtype: string
      - name: shortCiteRegEx
        dtype: string
      - name: year
        dtype: int32
    - name: referenceMentions
      sequence:
      - name: referenceID
        dtype: int32
      - name: context
        dtype: string
      - name: startOffset
        dtype: int32
      - name: endOffset
        dtype: int32
    - name: year
      dtype: int32
    - name: abstractText
      dtype: string
    - name: creator
      dtype: string
  splits:
  - name: test
    num_bytes: 34284777
    num_examples: 637
  - name: train
    num_bytes: 571263679
    num_examples: 11090
  - name: validation
    num_bytes: 32488519
    num_examples: 637
  download_size: 1246688292
  dataset_size: 638036975
- config_name: reviews
  features:
  - name: id
    dtype: string
  - name: conference
    dtype: string
  - name: comments
    dtype: string
  - name: subjects
    dtype: string
  - name: version
    dtype: string
  - name: date_of_submission
    dtype: string
  - name: title
    dtype: string
  - name: authors
    sequence: string
  - name: accepted
    dtype: bool
  - name: abstract
    dtype: string
  - name: histories
    sequence:
      sequence: string
  - name: reviews
    sequence:
    - name: date
      dtype: string
    - name: title
      dtype: string
    - name: other_keys
      dtype: string
    - name: originality
      dtype: string
    - name: comments
      dtype: string
    - name: is_meta_review
      dtype: bool
    - name: is_annotated
      dtype: bool
    - name: recommendation
      dtype: string
    - name: replicability
      dtype: string
    - name: presentation_format
      dtype: string
    - name: clarity
      dtype: string
    - name: meaningful_comparison
      dtype: string
    - name: substance
      dtype: string
    - name: reviewer_confidence
      dtype: string
    - name: soundness_correctness
      dtype: string
    - name: appropriateness
      dtype: string
    - name: impact
      dtype: string
  splits:
  - name: test
    num_bytes: 878906
    num_examples: 637
  - name: train
    num_bytes: 15234922
    num_examples: 11090
  - name: validation
    num_bytes: 864799
    num_examples: 637
  download_size: 1246688292
  dataset_size: 16978627
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