---
annotations_creators:
- found
language_creators:
- machine-generated
languages:
- en
licenses:
- unknown
multilinguality:
- monolingual
size_categories:
- 100K<n<1M
source_datasets:
- original
task_categories:
- other
task_ids:
- other-other-open-information-extraction
paperswithcode_id: tupleinf-open-ie-dataset
pretty_name: TupleInf Open IE
---

# Dataset Card for TupleInf Open IE

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

- **Homepage: [Tuple IE Homepage](https://allenai.org/data/tuple-ie)**
- **Repository:**
- **Paper: [Answering Complex Questions Using Open Information Extraction](https://www.semanticscholar.org/paper/Answering-Complex-Questions-Using-Open-Information-Khot-Sabharwal/0ff595f0645a3e25a2f37145768985b10ead0509)**
- **Leaderboard:**
- **Point of Contact:**

### Dataset Summary

The TupleInf Open IE dataset contains Open IE tuples extracted from 263K sentences that were used by the solver in “Answering Complex Questions Using Open Information Extraction” (referred as Tuple KB, T). These sentences were collected from a large Web corpus using training questions from 4th and 8th grade as queries. This dataset contains 156K sentences collected for 4th grade questions and 107K sentences for 8th grade questions. Each sentence is followed by the Open IE v4 tuples using their simple format.

### Supported Tasks and Leaderboards

[More Information Needed]

### Languages

The text in the dataset is in English, collected from a large Web corpus using training questions from 4th and 8th grade as queries.

## Dataset Structure

### Data Instances

This dataset contains setences with corresponding relation tuples extracted from each sentence. Each instance should contain a sentence and followed by the [Open IE v4](https://github.com/allenai/openie-standalone) tuples using their *simple format*.
An example of an instance:

```JSON
{
  "sentence": "0.04593 kg Used a triple beam balance to mass a golf ball.",
  "tuples": {
    "score": 0.8999999761581421,
    "tuple_text": "(0.04593 kg; Used; a triple beam balance; to mass a golf ball)",
    "context": "",
    "arg1": "0.04593 kg",
    "rel": "Used",
    "arg2s": ["a triple beam balance", "to mass a golf ball"],
  }
}
```

### Data Fields

- `sentence`: the input text/sentence.
- `tuples`: the extracted relation tuples from the sentence.
  - `score`: the confident score for each tuple.
  - `tuple_text`: the relationship representation text of the extraction, in the *simple format* of [Open IE v4](https://github.com/allenai/openie-standalone).
  - `context`: an optional representation of the context for this extraction. Defaults to `""` if there's no context.
  - `arg1`: the first argument in the relationship.
  - `rel`: the relation.
  - `arg2s`: a sequence of the 2nd arguments in the realtionship.

### Data Splits

|    name   | train|
|-----------|-----:|
|    all    |267719|
| 4th_grade |158910|
| 8th_grade |108809|

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

[More Information Needed]

### Citation Information

```bibtex
@article{Khot2017AnsweringCQ,
  title={Answering Complex Questions Using Open Information Extraction},
  author={Tushar Khot and A. Sabharwal and Peter Clark},
  journal={ArXiv},
  year={2017},
  volume={abs/1704.05572}
}
```

### Contributions

Thanks to [@mattbui](https://github.com/mattbui) for adding this dataset.
