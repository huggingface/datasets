---
annotations_creators:
- machine-generated
language_creators:
- crowdsourced
languages:
- en
licenses:
- cc-by-2.0
multilinguality:
- monolingual
size_categories:
- 100M<n<1B
source_datasets:
- original
task_categories:
- other
- text-generation
- fill-mask
- text-classification
task_ids:
- language-modeling
- masked-language-modeling
- multi-class-classification
- multi-label-classification
- other-other-citation-recommendation
paperswithcode_id: s2orc
pretty_name: S2ORC
---

# Dataset Card for S2ORC: The Semantic Scholar Open Research Corpus

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

- **Homepage:** [S2ORC: The Semantic Scholar Open Research Corpus](https://allenai.org/data/s2orc)
- **Repository:** [S2ORC: The Semantic Scholar Open Research Corpus](https://github.com/allenai/s2orc)
- **Paper:** [S2ORC: The Semantic Scholar Open Research Corpus](https://www.aclweb.org/anthology/2020.acl-main.447/)
- **Point of Contact:** [Kyle Lo](kylel@allenai.org)

### Dataset Summary

A large corpus of 81.1M English-language academic papers spanning many academic disciplines. Rich metadata, paper abstracts, resolved bibliographic references, as well as structured full text for 8.1M open access papers. Full text annotated with automatically-detected inline mentions of citations, figures, and tables, each linked to their corresponding paper objects. Aggregated papers from hundreds of academic publishers and digital archives into a unified source, and create the largest publicly-available collection of machine-readable academic text to date.

### Supported Tasks and Leaderboards

[More Information Needed]

### Languages

The text in the dataset is in English.

## Dataset Structure

### Data Instances

Example Paper Record:

```
{
   "id":"4cd223df721b722b1c40689caa52932a41fcc223",
   "title":"Knowledge-rich, computer-assisted composition of Chinese couplets",
   "paperAbstract":"Recent research effort in poem composition has focused on the use of automatic language generation...",
   "entities":[

   ],
   "fieldsOfStudy":[
      "Computer Science"
   ],
   "s2Url":"https://semanticscholar.org/paper/4cd223df721b722b1c40689caa52932a41fcc223",
   "pdfUrls":[
      "https://doi.org/10.1093/llc/fqu052"
   ],
   "s2PdfUrl":"",
   "authors":[
      {
         "name":"John Lee",
         "ids":[
            "3362353"
         ]
      },
      "..."
   ],
   "inCitations":[
      "c789e333fdbb963883a0b5c96c648bf36b8cd242"
   ],
   "outCitations":[
      "abe213ed63c426a089bdf4329597137751dbb3a0",
      "..."
   ],
   "year":2016,
   "venue":"DSH",
   "journalName":"DSH",
   "journalVolume":"31",
   "journalPages":"152-163",
   "sources":[
      "DBLP"
   ],
   "doi":"10.1093/llc/fqu052",
   "doiUrl":"https://doi.org/10.1093/llc/fqu052",
   "pmid":"",
   "magId":"2050850752"
}
```

### Data Fields

#### Identifier fields

* `paper_id`: a `str`-valued field that is a unique identifier for each S2ORC paper.

* `arxiv_id`: a `str`-valued field for papers on [arXiv.org](https://arxiv.org).

* `acl_id`: a `str`-valued field for papers on [the ACL Anthology](https://www.aclweb.org/anthology/).

* `pmc_id`: a `str`-valued field for papers on [PubMed Central](https://www.ncbi.nlm.nih.gov/pmc/articles).

* `pubmed_id`: a `str`-valued field for papers on [PubMed](https://pubmed.ncbi.nlm.nih.gov/), which includes MEDLINE.  Also known as `pmid` on PubMed.

* `mag_id`: a `str`-valued field for papers on [Microsoft Academic](https://academic.microsoft.com).

* `doi`: a `str`-valued field for the [DOI](http://doi.org/).

Notably:

* Resolved citation links are represented by the cited paper's `paper_id`.
* The `paper_id` resolves to a Semantic Scholar paper page, which can be verified using the `s2_url` field.
* We don't always have a value for every identifier field.  When missing, they take `null` value.

#### Metadata fields

* `title`: a `str`-valued field for the paper title.  Every S2ORC paper *must* have one, though the source can be from publishers or parsed from PDFs.  We prioritize publisher-provided values over parsed values.

* `authors`: a `List[Dict]`-valued field for the paper authors.  Authors are listed in order.  Each dictionary has the keys `first`, `middle`, `last`, and `suffix` for the author name, which are all `str`-valued with exception of `middle`, which is a `List[str]`-valued field.  Every S2ORC paper *must* have at least one author.

* `venue` and `journal`: `str`-valued fields for the published venue/journal.  *Please note that there is not often agreement as to what constitutes a "venue" versus a "journal". Consolidating these fields is being considered for future releases.*

* `year`: an `int`-valued field for the published year.  If a paper is preprinted in 2019 but published in 2020, we try to ensure the `venue/journal` and `year` fields agree & prefer non-preprint published info. Missing years are replaced by -1. *We know this decision prohibits certain types of analysis like comparing preprint & published versions of a paper.  We're looking into it for future releases.*

* `abstract`: a `str`-valued field for the abstract.  These are provided directly from gold sources (not parsed from PDFs).  We preserve newline breaks in structured abstracts, which are common in medical papers, by denoting breaks with `':::'`.

* `inbound_citations`: a `List[str]`-valued field containing `paper_id` of other S2ORC papers that cite the current paper.  *Currently derived from PDF-parsed bibliographies, but may have gold sources in the future.*

* `outbound_citations`: a `List[str]`-valued field containing `paper_id` of other S2ORC papers that the current paper cites.  Same note as above.

* `has_inbound_citations`: a `bool`-valued field that is `true` if `inbound_citations` has at least one entry, and `false` otherwise.

* `has_outbound_citations` a `bool`-valued field that is `true` if `outbound_citations` has at least one entry, and `false` otherwise.

We don't always have a value for every metadata field.  When missing, `str` fields take `null` value, while `List` fields are empty lists.

### Data Splits

There is no train/dev/test split given in the dataset

## Dataset Creation

### Curation Rationale

Academic papers are an increasingly important textual domain for natural language processing (NLP) research. Aside from capturing valuable knowledge from humankind’s collective research efforts, academic papers exhibit many interesting characteristics – thousands of words organized into sections, objects such as tables, figures and equations, frequent inline references to these objects, footnotes, other papers, and more

### Source Data

#### Initial Data Collection and Normalization

To construct S2ORC, we must overcome challenges in (i) paper metadata aggregation, (ii) identifying open access publications, and (iii) clustering papers, in addition to identifying, extracting, and cleaning the full text and bibliometric annotations associated with each paper. The pipeline for creating S2ORC is:

1) Process PDFs and LATEX sources to derive metadata, clean full text, inline citations and references, and bibliography entries,
2) Select the best metadata and full text parses for each paper cluster,
3) Filter paper clusters with insufficient metadata or content, and
4) Resolve bibliography links between paper clusters in the corpus.

#### Who are the source language producers?

S2ORC is constructed using data from the Semantic Scholar literature corpus (Ammar et al., 2018). Papers in Semantic Scholar are derived from numerous sources: obtained directly from publishers, from resources such as MAG, from various archives such as arXiv or PubMed, or crawled from the open Internet. Semantic Scholar clusters these papers based on title similarity and DOI overlap, resulting in an initial set of approximately 200M paper clusters.

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

Semantic Scholar Open Research Corpus is licensed under ODC-BY.

### Citation Information

```
@misc{lo2020s2orc,
      title={S2ORC: The Semantic Scholar Open Research Corpus},
      author={Kyle Lo and Lucy Lu Wang and Mark Neumann and Rodney Kinney and Dan S. Weld},
      year={2020},
      eprint={1911.02782},
      archivePrefix={arXiv},
      primaryClass={cs.CL}
}
```
### Contributions

Thanks to [@bhavitvyamalik](https://github.com/bhavitvyamalik) for adding this dataset.
