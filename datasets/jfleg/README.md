---
annotations_creators:
- expert-generated
language_creators:
- found
languages:
- en
licenses:
- cc-by-nc-sa-4.0
multilinguality:
- monolingual
- other-language-learner
size_categories:
- 1K<n<10K
source_datasets:
- extended|other-GUG-grammaticality-judgements
task_categories:
- conditional-text-generation
task_ids:
- conditional-text-generation-other-grammatical-error-correction
paperswithcode_id: jfleg
---

# Dataset Card for JFLEG

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

- **Homepage:** [Github](https://github.com/keisks/jfleg)
- **Repository:** [Github](https://github.com/keisks/jfleg)
- **Paper:** [Napoles et al., 2020](https://www.aclweb.org/anthology/E17-2037/)
- **Leaderboard:** [Leaderboard](https://github.com/keisks/jfleg#leader-board-published-results)
- **Point of Contact:** Courtney Napoles, Keisuke Sakaguchi

### Dataset Summary
JFLEG (JHU FLuency-Extended GUG) is an English grammatical error correction (GEC) corpus. It is a gold standard benchmark for developing and evaluating GEC systems with respect to fluency (extent to which a text is native-sounding) as well as grammaticality. For each source document, there are four human-written corrections.

### Supported Tasks and Leaderboards
Grammatical error correction.

### Languages
English (native as well as L2 writers)

## Dataset Structure

### Data Instances
Each instance contains a source sentence and four corrections. For example:
```python
{
  'sentence': "They are moved by solar energy ."
  'corrections': [
    "They are moving by solar energy .",
    "They are moved by solar energy .",
    "They are moved by solar energy .",
    "They are propelled by solar energy ." 
  ]
}
 ```

### Data Fields
- sentence: original sentence written by an English learner
- corrections: corrected versions by human annotators. The order of the annotations are consistent (eg first sentence will always be written by annotator "ref0").

### Data Splits
- This dataset contains 1511 examples in total and comprise a dev and test split. 
- There are 754 and 747 source sentences for dev and test, respectively. 
- Each sentence has 4 corresponding corrected versions. 

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

[More Information Needed]

### Licensing Information
This work is licensed under a [Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License](https://creativecommons.org/licenses/by-nc-sa/4.0/).

### Citation Information
This benchmark was proposed by [Napoles et al., 2020](https://www.aclweb.org/anthology/E17-2037/).

```
@InProceedings{napoles-sakaguchi-tetreault:2017:EACLshort,
  author    = {Napoles, Courtney  and  Sakaguchi, Keisuke  and  Tetreault, Joel},
  title     = {JFLEG: A Fluency Corpus and Benchmark for Grammatical Error Correction},
  booktitle = {Proceedings of the 15th Conference of the European Chapter of the Association for Computational Linguistics: Volume 2, Short Papers},
  month     = {April},
  year      = {2017},
  address   = {Valencia, Spain},
  publisher = {Association for Computational Linguistics},
  pages     = {229--234},
  url       = {http://www.aclweb.org/anthology/E17-2037}
}

@InProceedings{heilman-EtAl:2014:P14-2,
  author    = {Heilman, Michael  and  Cahill, Aoife  and  Madnani, Nitin  and  Lopez, Melissa  and  Mulholland, Matthew  and  Tetreault, Joel},
  title     = {Predicting Grammaticality on an Ordinal Scale},
  booktitle = {Proceedings of the 52nd Annual Meeting of the Association for Computational Linguistics (Volume 2: Short Papers)},
  month     = {June},
  year      = {2014},
  address   = {Baltimore, Maryland},
  publisher = {Association for Computational Linguistics},
  pages     = {174--180},
  url       = {http://www.aclweb.org/anthology/P14-2029}
}
```

### Contributions

Thanks to [@j-chim](https://github.com/j-chim) for adding this dataset.