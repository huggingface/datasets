---
annotations_creators:
- no-annotation
language_creators:
- found
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
- sequence-modeling
task_ids:
- language-modeling
---

# Dataset Card for CC-News

## Table of Contents
- [Dataset Description](#dataset-description)
  - [Dataset Summary](#dataset-summary)
  - [Supported Tasks](#supported-tasks-and-leaderboards)
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

- **Homepage:** [CC-News homepage](https://commoncrawl.org/2016/10/news-dataset-available/)
- **Point of Contact:** [Vladimir Blagojevic](mailto:dovlex@gmail.com)

### Dataset Summary

CC-News dataset contains news articles from news sites all over the world. The data is available on AWS S3 in the Common Crawl bucket at /crawl-data/CC-NEWS/. 
This version of the dataset has been prepared using [news-please](https://github.com/fhamborg/news-please) - an integrated web crawler and information extractor for news.  
It contains 708241 English language news articles published between Jan 2017 and December 2019. 
It represents a small portion of the English language subset of the CC-News dataset.

### Supported Tasks and Leaderboards

[N/A]

### Languages

The text in the dataset is in the English language. 

## Dataset Structure

### Data Instances

Dataset instance contains an article itself and the relevant article fields.
An example from the Cc-New train set looks as follows:
```
{
  'date': '2017-08-14 00:00:00',
  'description': '"The spirit of Green Day has always been about rising above oppression."',
  'domain': '1041jackfm.cbslocal.com',
  'image_url': 'https://cbs1041jackfm.files.wordpress.com/2017/08/billie-joe-armstrong-theo-wargo-getty-images.jpg?w=946',
  'text': 'By Abby Hassler\nGreen Day’s Billie Joe Armstrong has always been outspoken about his political beliefs. Following 
  the tragedy in Charlottesville, Virgina, over the weekend, Armstrong felt the need to speak out against the white supremacists 
  who caused much of the violence.\nRelated: Billie Joe Armstrong Wins #TBT with Childhood Studio Photo\n“My heart feels heavy. 
  I feel like what happened in Charlottesville goes beyond the point of anger,” Armstrong wrote on Facebook. “It makes me sad 
  and desperate. shocked. I f—— hate racism more than anything.”\n“The spirit of Green Day has always been about rising above 
  oppression. and sticking up for what you believe in and singing it at the top of your lungs,” Armstrong continued. 
  “We grew up fearing nuclear holocaust because of the cold war. those days are feeling way too relevant these days. 
  these issues are our ugly past.. and now it’s coming to haunt us. always resist these doomsday politicians. and in the 
  words of our punk forefathers .. Nazi punks f— off.”',
  'title': 'Green Day’s Billie Joe Armstrong Rails Against White Nationalists',
  'url': 'http://1041jackfm.cbslocal.com/2017/08/14/billie-joe-armstrong-white-nationalists/'
}
```

### Data Fields

- `date`: date of publication
- `description`: description or a summary of the article
- `domain`: source domain of the article (i.e. www.nytimes.com)
- `image_url`: URL of the article's image
- `text`: the actual article text in raw form
- `title`: title of the article
- `url`: article URL, the original URL where it was scraped. 


### Data Splits

CC-News dataset has only the training set, i.e. it has to be loaded with `train` split specified:
`cc_news = load_dataset('cc_news', split="train")`

## Dataset Creation

CC-News has been mostly used for language model training.

### Source Data

#### Initial Data Collection and Normalization

CC-News dataset has been proposed, created, and maintained by Sebastian Nagel. 
The data is publicly available on AWS S3 Common Crawl bucket at /crawl-data/CC-NEWS/. 
This version of the dataset has been prepared using [news-please](https://github.com/fhamborg/news-please) - an 
integrated web crawler and information extractor for news.  
It contains 708241 English language news articles published between Jan 2017 and December 2019.
Although news-please tags each news article with an appropriate language tag, these tags are somewhat unreliable. 
To strictly isolate English language articles an additional check has been performed using 
[Spacy langdetect pipeline](https://spacy.io/universe/project/spacy-langdetect).   
We selected articles with text fields scores of 80% probability or more of being English.
There are no strict guarantees that each article has all the relevant fields. For example, 527595 
articles have a valid description field. All articles have what appears to be a valid image URL, 
but they have not been verified.

#### Who are the source language producers?

The news websites throughout the World.

### Annotations

#### Annotation process

[N/A]

#### Who are the annotators?

[N/A]

### Personal and Sensitive Information

As one can imagine, data contains contemporary public figures or individuals who appeared in the news.

## Considerations for Using the Data

### Social Impact of Dataset

The purpose of this dataset is to help language model researchers develop better language models. 

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

[More Information Needed]
