# Swedish NER Corpus

## Table of Contents
- [Dataset Description](#dataset-description)
  - [Dataset Summary](#dataset-summary)
  - [Languages](#languages)
- [Dataset Structure](#dataset-structure)
  - [Data Fields](#data-instances)

## Dataset Description

- **Homepage:** [https://github.com/klintan/swedish-ner-corpus](https://github.com/klintan/swedish-ner-corpus)
- **Repository:** [https://github.com/klintan/swedish-ner-corpus](https://github.com/klintan/swedish-ner-corpus)

### Dataset Summary

Webbnyheter 2012 from Spraakbanken, semi-manually annotated and adapted for CoreNLP Swedish NER. Semi-manually defined in this case as: Bootstrapped from Swedish Gazetters then manually correcte/reviewed by two independent native speaking swedish annotators. No annotator agreement calculated.


### Languages

Swedish

## Dataset Structure

### Data Fields

- `id`: id of the sentence
- `token`: current token
- `ner_tag`: ner tag of the token
