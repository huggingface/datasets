---
annotations_creators:
- crowdsourced
language_creators:
- crowdsourced
languages:
- en
licenses:
- other-nlm-license
multilinguality:
- monolingual
size_categories:
- 10M<n<100M
source_datasets:
- original
task_categories:
- conditional-text-generation
- sequence-modeling
- text-classification
- text-scoring
task_ids:
- language-modeling
- other-structured-to-text
- text-scoring-other-citation-estimation
- topic-classification
paperswithcode_id: pubmed
pretty_name: PubMed
---

# Dataset Card for PubMed

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

- **Homepage:** : [https://www.nlm.nih.gov/databases/download/pubmed_medline.html]()
- **Documentation:** : [https://www.nlm.nih.gov/databases/download/pubmed_medline_documentation.html]()
- **Repository:**
- **Paper:**
- **Leaderboard:**
- **Point of Contact:**

### Dataset Summary

NLM produces a baseline set of MEDLINE/PubMed citation records in XML format for download on an annual basis. The annual baseline is released in December of each year. Each day, NLM produces update files that include new, revised and deleted citations. See our documentation page for more information.

### Supported Tasks and Leaderboards

[More Information Needed]

### Languages

- English

## Dataset Structure

Bear in mind the data comes from XML that have various tags that are hard to reflect
in a concise JSON format. Tags and list are kind of non "natural" to XML documents
leading this library to make some choices regarding data. "Journal" info was dropped
altogether as it would have led to many fields being empty all the time.

The hierarchy is also a bit unnatural but the choice was made to keep as close as
possible to the original data for future releases that may change schema from NLM's side.

Author has been kept and contains either "ForeName", "LastName", "Initials", or "CollectiveName".
(All the fields will be present all the time, but only some will be filled)

### Data Instances

```json
{
    "MedlineCitation": {
        "PMID": 0,
        "DateCompleted": {"Year": 0, "Month": 0, "Day": 0},
        "NumberOfReferences": 0,
        "DateRevised": {"Year": 0, "Month": 0, "Day": 0},
        "Article": {
            "Abstract": {"AbstractText": "Some abstract (can be missing)" },
            "ArticleTitle": "Article title",
            "AuthorList": {"Author": [
                {"FirstName": "John", "ForeName": "Doe", "Initials": "JD", "CollectiveName": ""}
                {"CollectiveName": "The Manhattan Project", "FirstName": "", "ForeName": "", "Initials": ""}
            ]},
            "Language": "en",
            "GrantList": {
                "Grant": [],
            },
            "PublicationTypeList": {"PublicationType": []},
        },
        "MedlineJournalInfo": {"Country": "France"},
        "ChemicalList": {"Chemical": [{
            "RegistryNumber": "XX",
            "NameOfSubstance": "Methanol"
        }]},
        "CitationSubset": "AIM",
        "MeshHeadingList": {
            "MeshHeading": [],
        },
    },
    "PubmedData": {
        "ArticleIdList": {"ArticleId": "10.1002/bjs.1800650203"},
        "PublicationStatus": "ppublish",
        "History": {"PubMedPubDate": [{"Year": 0, "Month": 0, "Day": 0}]},
        "ReferenceList": [{"Citation": "Somejournal", "CitationId": 01}],
    },
}
```

### Data Fields

Main Fields will probably interest people are:

- "MedlineCitation" > "Article" > "AuthorList" > "Author"
- "MedlineCitation" > "Article" > "Abstract" > "AbstractText"
- "MedlineCitation" > "Article" > "Article Title"
- "MedlineCitation" > "ChemicalList" > "Chemical"
- "MedlineCitation" > "NumberOfReferences"

### Data Splits

There are no splits in this dataset. It is given as is.

## Dataset Creation

### Curation Rationale

[More Information Needed]

### Source Data

#### Initial Data Collection and Normalization

[https://www.nlm.nih.gov/databases/download/pubmed_medline_faq.html]()

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

[https://www.nlm.nih.gov/databases/download/terms_and_conditions.html]()

### Citation Information

[Courtesy of the U.S. National Library of Medicine](https://www.nlm.nih.gov/databases/download/terms_and_conditions.html).

### Contributions

Thanks to [@Narsil](https://github.com/Narsil) for adding this dataset.