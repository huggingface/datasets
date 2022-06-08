---
annotations_creators:
- no-annotation
language_creators:
- found
languages:
- en
licenses:
- other-
multilinguality:
- monolingual
pretty_name: The Pile
size_categories:
- unknown
source_datasets:
- original
task_categories:
- text-generation
- fill-mask
task_ids:
- language-modeling
- masked-language-modeling
---

# Dataset Card for The Pile

## Table of Contents
- [Table of Contents](#table-of-contents)
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

- **Homepage:** https://pile.eleuther.ai/
- **Repository:** https://github.com/EleutherAI/the-pile
- **Paper:** [The Pile: An 800GB Dataset of Diverse Text for Language Modeling](https://arxiv.org/abs/2101.00027)
- **Leaderboard:**
- **Point of Contact:** [EleutherAI](mailto:contact@eleuther.ai)

### Dataset Summary

The Pile is a 825 GiB diverse, open source language modelling data set that consists of 22 smaller, high-quality
datasets combined together.


### Supported Tasks and Leaderboards

[More Information Needed]

### Languages

This dataset is in English (`EN`).

## Dataset Structure

### Data Instances

#### all
```
{
  'meta': {'pile_set_name': 'Pile-CC'},
  'text': 'It is done, and submitted. You can play “Survival of the Tastiest” on Android, and on the web. Playing on...'
}
```

#### enron_emails
```
{
  'text': 'Name\t\t\tNew Title\t\t\t\tEffective Date\t\t\tMid Year promotion Yes/No\n\nFloyd, Jodie\t\tSr Cust Svc Rep (no change)\t\t7/16/01\t\t\t\tNo\n\nBuehler, Craig\t\tSr Mkt/Sup Analyst (no change)\t\t7/16/01\t\t\t\tNo\n\nWagoner, Mike\t\tTeam Advisor - Gas Control\t\t7/1/01\t\t\t\tNo\n\nClapper, Karen\t\tSr Cust Svc Rep\t\t\t8/1/01\t\t\t\tYes\n\nGreaney, Chris\t\tSr Cust Svc Rep\t\t\t8/1/01\t\t\t\tYes\n\nWilkens, Jerry\t\tSr Cust Svc Rep\t\t\t8/1/01\t\t\t\tYes\n\nMinton, Kevin\t\tPipeline Controller\t\t\t8/1/01\t\t\t\tYes\n\nCox, Don\t\tPipeline Controller\t\t\t8/1/01\t\t\t\tYes\n\nHanagriff, Richard\tSr Accounting Control Spec\t\t8/1/01\t\t\t\tYes\n\n\nThanks,\nMS'
  'meta': "{}",

}
```

#### europarl
```
{
  'text': 'Uvádění biocidních přípravků na trh - Nový návrh revize týkající se biocidních přípravků (rozprava) \nPředsedající\nDalším bodem je společná rozprava o následujících tématech:\nzpráva paní Sârbuové za Výbor pro životní prostředí, veřejné zdraví a bezpečnost potravin o návrhu...'
  'meta': "{'language': 'cs'}",

}
```

#### free_law
```
{
  'meta':  "{'case_jurisdiction': 'scotus.tar.gz', 'case_ID': '110921.json','date_created': '2010-04-28T17:12:49Z'}",
  'text': '\n461 U.S. 238 (1983)\nOLIM ET AL.\nv.\nWAKINEKONA\nNo. 81-1581.\nSupreme Court of United States.\nArgued...'
}
```

#### hacker_news
```
{
  'text': "\nChina Deserves Donald Trump - rm2889\nhttps://www.nytimes.com/2019/05/21/opinion/china-trump-trade.html\n======\nNotPaidToPost\n> so he’d be wise to curb his nationalistic “no-one-tells-China-what-to-do”\n> bluster\n\nThis comment highlights both ignorance of Chinese history and continuing\nAmerican arrogance.\n\nChina has been painfully dictated what to do during the last 200 years. This\nhas had a profound effect on the country and has led to the collapse of\nimperial rule and the drive to 'rejuvenate'...",
  'meta':  "{'id': '19979654'}",
}
```

#### nih_exporter
```
{
  'text': "The National Domestic Violence Hotline (NDVH) and the National Dating Abuse Helpline (NDAH), which are supported by the Division of Family Violence Prevention and Services within the Family and Youth Services Bureau, serve as critical partners in the intervention, prevention, and resource assistance efforts of the network of family violence, domestic violence, and dating violence service providers. They provide crisis intervention and support services; information about resources on domestic...",
  'meta':  " {'APPLICATION_ID': 100065}",
}
```

#### pubmed
```
{
  'meta': {'pmid': 11409574, 'language': 'eng'},
  'text': 'Epidemiology of hypoxaemia in children with acute lower respiratory infection.\nTo determine the prevalence of hypoxaemia in children aged under 5 years suffering acute lower respiratory infections (ALRI), the risk factors for hypoxaemia in children under 5 years of age with ALRI, and the association of hypoxaemia with an increased risk of dying in children of the same age. Systematic review of the published literature. Out-patient clinics, emergency departments and hospitalisation wards in 23 health centres from 10 countries. Cohort studies reporting the frequency of hypoxaemia in children under 5 years of age with ALRI, and the association between hypoxaemia and the risk of dying. Prevalence of hypoxaemia measured in children with ARI and relative risks for the association between the severity of illness and the frequency of hypoxaemia, and between hypoxaemia and the risk of dying. Seventeen published studies were found that included 4,021 children under 5 with acute respiratory infections (ARI) and reported the prevalence of hypoxaemia. Out-patient children and those with a clinical diagnosis of upper ARI had a low risk of hypoxaemia (pooled estimate of 6% to 9%). The prevalence increased to 31% and to 43% in patients in emergency departments and in cases with clinical pneumonia, respectively, and it was even higher among hospitalised children (47%) and in those with radiographically confirmed pneumonia (72%). The cumulated data also suggest that hypoxaemia is more frequent in children living at high altitude. Three papers reported an association between hypoxaemia and death, with relative risks varying between 1.4 and 4.6. Papers describing predictors of hypoxaemia have focused on clinical signs for detecting hypoxaemia rather than on identifying risk factors for developing this complication. Hypoxaemia is a common and potentially lethal complication of ALRI in children under 5, particularly among those with severe disease and those living at high altitude. Given the observed high prevalence of hypoxaemia and its likely association with increased mortality, efforts should be made to improve the detection of hypoxaemia and to provide oxygen earlier to more children with severe ALRI.'
}
```

#### pubmed_central
```
{
  'meta': "{id': 'PMC5595690'}",
  'text': 'Introduction {#acel12642-sec-0001}\n============\n\nAlzheimer\\\'s disease (AD), the most common cause of...'
}
```

#### ubuntu_irc
```
{
  'text': "#ubuntu 2004-07-05\n* Window 3\n* \tServer: [0]  <None>\n* \tScreen: 0x817e90c\n* \tGeometry Info: [0 11 0 11 11 11] \n* \tCO, LI are [94 49] \n* \tCurrent channel: #ubuntu\n* \tQuery User: <None> \n*\tPrompt: <None>\n* \tSecond status line is OFF\n* \tSplit line is ON triple is OFF\n* \tLogging is ON\n* \tLogfile is irclogs/ubuntu.log\n* \tNotification is OFF\n* \tHold mode is OFF\n* \tWindow level is NONE\n* \tLastlog level is ALL\n* \tNotify level is ALL\n<mdz> lifeless: using tla effectively for all packages in Warty requ...",
  'meta': "{'channel': 'ubuntu', 'month': 7}"
}
```

#### uspto
```
{
  'text': "1. Field of the Invention\nIn an extensive plant breeding program, Grant Merrill, originator and now deceased, originated a large number of new and distinct varieties of fruit trees, and which included the herein-claimed variety of peach tree. Such plant breeding program was undertaken in originator's experimental orchard located near Exeter, Tulare County, Calif.\n2. Prior Varieties\nAmong the existent varieties of peach trees which were known to originator, particular reference is made to Gemfree (U.S. Plant Pat. No. 1,409) and June Lady (U.S. Plant Pat. No. 3,022) hereinafter mentioned for the purpose of comparison.",
  'meta': "{'bibliographic_information': {'Patent Number': 'PP0049700', 'Series Code': '6', 'Application Number': '2845415', 'Application Type': '6', 'Art unit': '337', 'Application Filing Date': '19810720', 'Title of Invention': 'Peach tree (A3-10)', 'Issue Date': '19830104', 'Number of Claims': '1', 'Exemplary Claim Number(s)': '1', 'Primary Examiner': 'Bagwill; Robert E.', 'Number of Drawing Sheets': '1', 'Number of figures': '1'}, 'source_file': 'https://bulkdata.uspto.gov/data/patent/grant/redbook/fulltext/1983/pftaps19830104_wk01.zip', 'abstract': 'A peach tree which is large, vigorous, and spreading; foliated with large, lanceolate leaves having a finely serrate margin, a petiole of medium length and thickness, and medium size, reniform glands; blooms from medium size, conic, plump, pubescent buds; the flowers, medium in blooming period compared with other varieties, being of medium size, and pink; and is a regular and very productive bearer of medium but variable size, round truncate, clingstone fruit having yellow skin substantially overspread with red, yellow flesh mottled with red adjacent the skin, and an amber stone.', 'classifications': [{'OCL': ['Plt', '43'], 'EDF': ['3'], 'ICL': ['A01H', '503'], 'FSC': ['Plt'], 'FSS': ['43']}], 'inventors': [{'inventor name': 'Merrill, deceased; Grant', 'Street': '325 Breese Ave.', 'City': 'late of Red Bluff', 'State': 'CA'}, {'inventor name': 'Merrill, executrix; by Lucile B.', 'Street': '325 Breese Ave.', 'City': 'Red Bluff', 'State': 'CA', 'Zip code': '96080'}]}"
}
```

### Data Fields

#### all

- `text` (str): Text.
- `meta` (dict): Metadata of the data instance with keys:
  - pile_set_name: Name of the subset.

#### enron_emails

- `text` (str): Text.
- `meta` (str): Metadata of the data instance.

#### europarl

- `text` (str): Text.
- `meta` (str): Metadata of the data instance with: language.

#### free_law

- `text` (str): Text.
- `meta` (str): Metadata of the data instance with: case_ID, case_jurisdiction, date_created.

#### hacker_news

- `text` (str): Text.
- `meta` (str): Metadata of the data instance with: id.

#### nih_exporter

- `text` (str): Text.
- `meta` (str): Metadata of the data instance with: APPLICATION_ID.

#### pubmed

- `text` (str): Text.
- `meta` (str): Metadata of the data instance with: pmid, language.

#### pubmed_central

- `text` (str): Text.
- `meta` (str): Metadata of the data instance with: ID of the data instance.

#### ubuntu_irc

- `text` (str): Text.
- `meta` (str): Metadata of the data instance with: channel, month.

#### uspto

- `text` (str): Text.
- `meta` (str): Metadata of the data instance with: bibliographic_information, source_file, abstract, classifications, 
  inventors.

### Data Splits

The "all" configuration is composed of 3 splits: train, validation and test.

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

Please refer to the specific license depending on the subset you use:
- PubMed Central: [MIT License](https://github.com/EleutherAI/pile-pubmedcentral/blob/master/LICENSE)

### Citation Information

```
@misc{gao2020pile,
      title={The Pile: An 800GB Dataset of Diverse Text for Language Modeling},
      author={Leo Gao and Stella Biderman and Sid Black and Laurence Golding and Travis Hoppe and Charles Foster and Jason Phang and Horace He and Anish Thite and Noa Nabeshima and Shawn Presser and Connor Leahy},
      year={2020},
      eprint={2101.00027},
      archivePrefix={arXiv},
      primaryClass={cs.CL}
}
```

### Contributions

Thanks to [@github-username](https://github.com/<github-username>) for adding this dataset.
