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
---

# Dataset Card for HebrewSentiment

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

| issue\_num | page\_count | date       | date\_he        | year | href                               | pdf                                               | coverpage                                         | backpage                                          | content                                               | url                                    | 
| ---------- | ----------- | ---------- | --------------- | ---- | ---------------------------------- | ------------------------------------------------- | ------------------------------------------------- | ------------------------------------------------- | ----------------------------------------------------- | -------------------------------------- | 
| 2403       | 72          | 1983-09-20 | 20 בספטמבר 1983 | 1983 | https://thisworld.online/1983/2403 | https://olam.eu-central-1.linodeobjects.com/pd... | https://olam.eu-central-1.linodeobjects.com/pa... | https://olam.eu-central-1.linodeobjects.com/pa... | ,י״ג תשרי תשמ״ד20.9.83 ,\\n\\nמיסטר 2403\\n\\nכתבת... | https://thisworld.online/api/1983/2403 |



### Data Fields

- `issue_num`: The modern hebrew inpput text.
- `page_count`: The sentiment label. 0=positive , 1=negative, 2=off-topic.
- `date`: The sentiment label. 0=positive , 1=negative, 2=off-topic.
- `date_he`: The sentiment label. 0=positive , 1=negative, 2=off-topic.
- `year`: The sentiment label. 0=positive , 1=negative, 2=off-topic.
- `href`: The sentiment label. 0=positive , 1=negative, 2=off-topic.
- `pdf`: The sentiment label. 0=positive , 1=negative, 2=off-topic.
- `coverpage`: The sentiment label. 0=positive , 1=negative, 2=off-topic.
- `backpage`: The sentiment label. 0=positive , 1=negative, 2=off-topic.
- `content`: The sentiment label. 0=positive , 1=negative, 2=off-topic.
- `url`: The sentiment label. 0=positive , 1=negative, 2=off-topic.


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