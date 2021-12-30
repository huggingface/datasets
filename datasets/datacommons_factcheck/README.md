---
annotations_creators:
- expert-generated
language_creators:
- found
languages:
- en
licenses:
- cc-by-nc-4.0
multilinguality:
- monolingual
size_categories:
  fctchk_politifact_wapo:
  - 1K<n<10K
  weekly_standard:
  - n<1K
source_datasets:
- original
task_categories:
- text-classification
task_ids:
- fact-checking
paperswithcode_id: null
---

# Dataset Card for DataCommons Fact Checked claims

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

- **Homepage:** [Data Commons fact checking FAQ](https://datacommons.org/factcheck/faq)

### Dataset Summary

A dataset of fact checked claims by news media maintained by [datacommons.org](https://datacommons.org/) containing the claim, author, and judgments, as well as the URL of the full explanation by the original fact-checker.

The fact checking is done by [FactCheck.org](https://www.factcheck.org/), [PolitiFact](https://www.politifact.com/), and [The Washington Post](https://www.washingtonpost.com/).

### Supported Tasks and Leaderboards

[More Information Needed]

### Languages

The data is in English (`en`).

## Dataset Structure

### Data Instances

An example of fact checking instance looks as follows:
```
{'claim_author_name': 'Facebook posts',
 'claim_date': '2019-01-01',
 'claim_text': 'Quotes Michelle Obama as saying, "White folks are what’s wrong with America."',
 'review_date': '2019-01-03',
 'review_rating': 'Pants on Fire',
 'review_url': 'https://www.politifact.com/facebook-fact-checks/statements/2019/jan/03/facebook-posts/did-michelle-obama-once-say-white-folks-are-whats-/',
 'reviewer_name': 'PolitiFact'}
```

### Data Fields

A data instance has the following fields:
- `review_date`: the day the fact checking report was posted. Missing values are replaced with empty strings
- `review_url`: URL for the full fact checking report
- `reviewer_name`: the name of the fact checking service.
- `claim_text`: the full text of the claim being reviewed.
- `claim_author_name`: the author of the claim being reviewed. Missing values are replaced with empty strings
- `claim_date` the date of the claim. Missing values are replaced with empty strings
- `review_rating`: the judgments of the fact checker (under `alternateName`, names vary by fact checker)

### Data Splits

No splits are provided. There are a total of 5632 claims fact-checked.

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

The fact checking is done by [FactCheck.org](https://www.factcheck.org/), [PolitiFact](https://www.politifact.com/), [The Washington Post](https://www.washingtonpost.com/), and [The Weekly Standard](https://www.weeklystandard.com/).

- [FactCheck.org](https://www.factcheck.org/) self describes as "a nonpartisan, nonprofit 'consumer advocate' for voters that aims to reduce the level of deception and confusion in U.S. politics." It was founded by journalists Kathleen Hall Jamieson and Brooks Jackson and is currently directed by Eugene Kiely.
- [PolitiFact](https://www.politifact.com/) describe their ethics as "seeking to present the true facts, unaffected by agenda or biases, [with] journalists setting their own opinions aside." It was started in August 2007 by Times Washington Bureau Chief Bill Adair. The organization was acquired in February 2018 by the Poynter Institute, a non-profit journalism education and news media research center that also owns the Tampa Bay Times.
- [The Washington Post](https://www.washingtonpost.com/) is a newspaper considered to be near the center of the American political spectrum. In 2013 Amazon.com founder Jeff Bezos bought the newspaper and affiliated publications.

The original data source also contains 132 items reviewed by [The Weekly Standard](https://www.weeklystandard.com/), which was a neo-conservative American newspaper. IT is the most politically loaded source of the group, which was originally a vocal creitic of the activity of fact-checking, and has historically taken stances [close to the American right](https://en.wikipedia.org/wiki/The_Weekly_Standard#Support_of_the_invasion_of_Iraq). It also had to admit responsibility for baseless accusations against a well known author in a public [libel case](https://en.wikipedia.org/wiki/The_Weekly_Standard#Libel_case). The fact checked items from this source can be found in the `weekly_standard` configuration but should be used only with full understanding of this context.

### Personal and Sensitive Information

[More Information Needed]

## Considerations for Using the Data

### Social Impact of Dataset

[More Information Needed]

### Discussion of Biases

See section above describing the [fact checking organizations](#who-are-the-annotators?).

[More Information Needed]

### Other Known Limitations

[More Information Needed]

## Additional Information

### Dataset Curators

This fact checking dataset is maintained by [datacommons.org](https://datacommons.org/), a Google initiative.

### Licensing Information

All fact checked items are released under a `CC-BY-NC-4.0` License.

### Citation Information

[More Information Needed]

### Contributions

Thanks to [@yjernite](https://github.com/yjernite) for adding this dataset.