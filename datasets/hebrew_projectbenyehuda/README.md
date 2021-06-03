---
annotations_creators:
- expert-generated
language_creators:
- found
languages:
- he
licenses:
- mit
multilinguality:
- monolingual
size_categories:
- 10K<n<100K
source_datasets:
- original
task_categories:
- sequence-modeling
task_ids:
- language-modeling
paperswithcode_id: null
---

# Dataset Card for Hebrew Projectbenyehuda

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

- **Homepage:** https://github.com/projectbenyehuda/public_domain_dump
- **Repository:** https://github.com/projectbenyehuda/public_domain_dump
- **Paper:** 
- **Leaderboard:**
- **Point of Contact:** 

### Dataset Summary

This repository contains a dump of thousands of public domain works in Hebrew, from Project Ben-Yehuda, in plaintext UTF-8 files, with and without diacritics (nikkud), and in HTML files. The pseudocatalogue.csv file is a list of titles, authors, genres, and file paths, to help you process the dump.

The Releases tab contains a downloadable ZIP archive of the full release. The git repo can be used to track individual file changes, or for incremenetal updates. In the ZIPs, each format (plaintext, plaintext stripped of diacritics, and HTML) has a ZIP file containing one directory per author, with all the author's works under that directory.

To request changes or improvements to this dump, file an issue against this repository.

All these works are in the public domain, so you are free to make any use of them, and do not need to ask for permission.

If you would like to give credit, please credit "Project Ben-Yehuda volunteers", and include a link to the site. We'd also love to hear about the uses you've made of this dump, as it encourages us to keep producing the dump. E-mail us with a brief description (and links, if/as appropriate) of your re-use, at editor@benyehuda.org.

There are 10078 files, 3181136 lines

Data Annotation: 

### Supported Tasks and Leaderboards

[More Information Needed]

### Languages

Hebrew

## Dataset Structure

Sample:
```
'authors' = {str} 'אחד העם'
'genre' = {str} 'מאמרים ומסות'
'id' = {int} 10
'original_language' = {str} ''
'source_edition' = {str} ''
'text' = {str} '\n\n\n\t\n\tחצי-נחמה\n\t\n\n\n\n1\n\nבין כל הצרות שנתחדשו עלינו בעת האחרונה תעשׂה ביחוד רושם מעציב בלב כל איש ישׂראל התחדשות ‘עלילת־הדם’. העלילה הנתעבה הזאת, בכל יָשנה, היתה ותהיה תמיד בעינינו כחדשה, ומימי הבינים ועד עתה תצטין בפעולתה החזקה על רוח עמנו, לא רק במקום המע
'title' = {str} 'חצי-נחמה'
'translators' = {str} ''
'url' = {str} 'https://raw.githubusercontent.com/projectbenyehuda/public_domain_dump/master/txt/p23/m10.txt'
```

### Data Instances

[More Information Needed]

### Data Fields

- `authors` 
- `genre` 
- `id`
- `original_language` 
- `source_edition` 
- `text` 
- `title`
- `translators` 
- `url` 

### Data Splits

|                          | train  | 
|--------------------------|--------|
| corpus                   | 10078  |


## Dataset Creation

### Curation Rationale

[More Information Needed]

### Source Data

#### Initial Data Collection and Normalization


#### Who are the source language producers?

[More Information Needed]

Researchers

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


MIT License



Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

### Citation Information

@article{,
  author = {},
  title = {Public domain texts from Project Ben-Yehuda},
  journal = {},
  url = {https://github.com/projectbenyehuda/public_domain_dump},
  year = {2020},
}
### Contributions

Thanks to [@imvladikon](https://github.com/imvladikon) for adding this dataset.