---
YAML tags:
{
  "task_categories": [
    "other"
  ],
  "task_ids": [],
  "multilinguality": [
    "monolingual"
  ],
  "languages": [
    "de"
  ],
  "language_creators": [
    "machine-generated"
  ],
  "annotations_creators": [
    "no-annotation"
  ],
  "source_datasets": [],
  "size_categories": [
    "100K<n<1M"
  ],
  "licenses": []
}

---

# Dataset Card for GermanCommonCrawl

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

- **Homepage:**
- **Repository:** https://github.com/German-NLP-Group/german-transformer-training
- **Paper:** 
- **Leaderboard:**
- **Point of Contact:** philipp.reissel@rwth-aachen.de

### Dataset Summary

German Only Extract from Common Crawl 

Stats: 

Total Size after Deduplication: 142 Mio Pages / 194 GB (Gzipped)
Total Size before Deduplcation: 263 Mio Pages / 392 GB (Gzipped)


### Supported Tasks and Leaderboards

This Dataset is for pretraining a German Language Model (Unsupervised).  

### Languages

German only (Sometimes websites are partially in another Language). One can filter these out through the `language_score` attribute. 

## Dataset Structure

### Data Instances

```
{'url': 'http://my-shop.ru/shop/books/545473.html', 
'date_download': '2016-10-20T19:38:58Z',
 'digest': 'sha1:F62EMGYLZDIKF4UL5JZYU47KWGGUBT7T', 
 'length': 1155, 
 'nlines': 4, 
 'source_domain': 'my-shop.ru', 
 'title': 'Grammatikalische Liebeslieder. Methodische Vorschläge', 
 'raw_content': 'Grammatikalische Liebeslieder. [....]', 
 'cc_segment': 'crawl-data/CC-MAIN-2016-44/segments/1476988717783.68/wet/CC-MAIN-20161020183837-00354-ip-10-171-6-4.ec2.internal.warc.wet.gz', 
 'original_nlines': 99, 
 'original_length': 2672, 
 'language': 'de', 
 'language_score': 1.0, 
 'perplexity': 283.0, 
 'bucket': 'head'}"
```

### Data Fields

- `url`: Original URL 
- `date_download`: Date when downloaded by Common Crawl
- `digest`: Hash 
- `length`: Number of Characters
- `nlines`: Number of lines 
- `source_domain`: Main Domain 
- `title`: Website Title
- `raw_content`: Website Text
- `cc_segment`: Common Crawl Segment = s3 path
- `original_nlines`: Number of lines before boilerplate removal
- `original_length`: Number of characters before boilerplate removal
- `language`: 'de'
- `language_score`: Probability of german only text
- `perplexity`: Quality of the text in comparison to wikipedia
- `bucket`: 'head'

### Data Splits

Train only

## Dataset Creation

### Curation Rationale

Handling and Filtering of Common Crawl Data requires large scale Server Ressources at a location in the US (for downloading speed). The total computing time needed to create this dataset is above 100k CPU hours. To give others the opportunity to train models with this dataset easily we make it publicly available. 

In most use cases you see an improved Model Performance when extending the pre-training Data so one can achieve highest accuracies as this is probably the largest available dataset. 


### Source Data

It was filtered from the Common Crawl Snapshots of the following months: 

1. 2015-48
2. 2016-18 
3. 2016-44
4. 2017-33
5. 2017-30
6. 2017-30
7. 2017-39 
8. 2017-51
9. 2018-09
10. 2018-17
11. 2018-30
12. 2018-39
13. 2018-51
14. 2019-09
15. 2019-18
16. 2019-30
17. 2019-47
18. 2020-10 

#### Initial Data Collection and Normalization

Filtering and deduplication of each month seperalety was performed with [CC_Net](https://github.com/facebookresearch/cc_net). The current datasets only contains the best part (head part) with the highest text quality (see CC_Net Paper for more details). Middle and tail part may be uploaded soon as well, or are available on request. 

Afterwards this Dataset was deduplicated again to filter out Websites which occur in multiple monthly snapshots. This deduplication removes all Websites which have either the same url or the same hash (this is to filter out websites which are accessible under multiple domains)

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


## Additional Information

### Dataset Curators

[More Information Needed]

### Licensing Information

[More Information Needed]

### Citation Information
```
@inproceedings{wenzek2020ccnet,
  title={CCNet: Extracting High Quality Monolingual Datasets from Web Crawl Data},
  author={Wenzek, Guillaume and Lachaux, Marie-Anne and Conneau, Alexis and Chaudhary, Vishrav and Guzm{\'a}n, Francisco and Joulin, Armand and Grave, {\'E}douard},
  booktitle={Proceedings of The 12th Language Resources and Evaluation Conference},
  pages={4003--4012},
  year={2020}
```
