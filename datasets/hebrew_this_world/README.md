---
annotations_creators:
- expert-generated
language_creators:
- found
languages:
- he
licenses:
- gpl
multilinguality:
- monolingual
size_categories:
- 1K<n<10K
source_datasets:
- original
task_categories:
- sequence-modeling
task_ids:
- language-modeling
paperswithcode_id: null
---

# Dataset Card for HebrewSentiment

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

- **Homepage:** https://thisworld.online/
- **Repository:** https://github.com/thisworld1/thisworld.online
- **Paper:** 
- **Leaderboard:**
- **Point of Contact:** 

### Dataset Summary

HebrewThisWorld is a data set consists of 2028 issues of the newspaper 'This World' edited by Uri Avnery and were published between 1950 and 1989. Released under the AGPLv3 license.

Data Annotation: 

### Supported Tasks and Leaderboards

Language modeling

### Languages

Hebrew

## Dataset Structure

csv file with "," delimeter

### Data Instances

Sample:

```json
{
  "issue_num": 637,
  "page_count": 16,
  "date": "1950-01-01",
  "date_he": "1 בינואר 1950",
  "year": "1950",
  "href": "https://thisworld.online/1950/637",
  "pdf": "https://olam.eu-central-1.linodeobjects.com/pdfs/B-I0637-D010150.pdf",
  "coverpage": "https://olam.eu-central-1.linodeobjects.com/pages/637/t-1.png",
  "backpage": "https://olam.eu-central-1.linodeobjects.com/pages/637/t-16.png",
  "content": "\nלפיד\nהנוער ־ בירושלים צילומים :\n\nב. רותנברג\n\nוזהו הלפיד\n...",
  "url": "https://thisworld.online/api/1950/637"
}
```

### Data Fields

- `issue_num`: ID/Number of the issue 
- `page_count`: Page count of the current issue
- `date`: Published date
- `date_he`: Published date in Hebrew
- `year`: Year of the issue
- `href`: URL to the issue to scan/print etc.
- `pdf`:  URL to the issue to scan in pdf
- `coverpage`:  URL to coverpage
- `backpage`: URL to backpage
- `content`: text content of the issue
- `url`: URL 


### Data Splits

|                          | train  | 
|--------------------------|--------|
| corpus                   | 2028  |



## Dataset Creation


### Curation Rationale

[More Information Needed]

### Source Data

[thisworld.online](https://thisworld.online/)

#### Initial Data Collection and Normalization

[More Information Needed]

#### Who are the source language producers?

[More Information Needed]

### Annotations


#### Annotation process

[More Information Needed]

#### Who are the annotators?

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

GNU AGPLv3+

This is free software, and you are welcome to redistribute it under certain conditions.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

### Citation Information

[More Information Needed]

### Contributions

Thanks to [@lhoestq](https://github.com/lhoestq), [@imvladikon](https://github.com/imvladikon) for adding this dataset.