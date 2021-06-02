---
annotations_creators:
- crowdsourced
language_creators:
- found
languages:
- en
licenses:
- cc-by-sa-3.0
multilinguality:
- monolingual
size_categories:
- 10K<n<100K
source_datasets:
- extended|natural_questions
- original
task_categories:
- question-answering
task_ids:
- open-domain-qa
paperswithcode_id: ambigqa
---

# Dataset Card for AmbigQA: Answering Ambiguous Open-domain Questions

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

- [**Homepage:**](https://nlp.cs.washington.edu/ambigqa/)
- [**Repository:**](https://github.com/shmsw25/AmbigQA)
- [**Paper:**](https://arxiv.org/pdf/2004.10645.pdf)

### Dataset Summary

AmbigNQ, a dataset covering 14,042 questions from NQ-open, an existing open-domain QA benchmark. We find that over half of the questions in NQ-open are ambiguous. The types of ambiguity are diverse and sometimes subtle, many of which are only apparent after examining evidence provided by a very large text corpus.  AMBIGNQ, a dataset with
14,042 annotations on NQ-OPEN questions containing diverse types of ambiguity.
We provide two distributions of our new dataset AmbigNQ: a `full` version with all annotation metadata and a `light` version with only inputs and outputs.

### Supported Tasks and Leaderboards

`question-answering`

### Languages

English

## Dataset Structure
### Data Instances

An example from the data set looks as follows:
```
{'annotations': {'answer': [[]],
  'qaPairs': [{'answer': [['April 19, 1987'], ['December 17, 1989']],
    'question': ['When did the Simpsons first air on television as an animated short on the Tracey Ullman Show?',
     'When did the Simpsons first air as a half-hour prime time show?']}],
  'type': ['multipleQAs']},
 'id': '-4469503464110108318',
 'nq_answer': ['December 17 , 1989'],
 'nq_doc_title': 'The Simpsons',
 'question': 'When did the simpsons first air on television?',
 'used_queries': {'query': ['When did the simpsons first air on television?'],
  'results': [{'snippet': ['The <b>Simpsons</b> is an American animated <b>television</b> sitcom starring the animated \nSimpson family, ... Since its <b>debut</b> on December 17, 1989, the show <b>has</b> \nbroadcast 673 episodes and its 30th season started ... The <b>Simpsons first</b> season \n<b>was</b> the Fox network&#39;s <b>first TV</b> series to rank among a season&#39;s top 30 highest-\nrated shows.',
     'The <b>Simpsons</b> is an American animated sitcom created by Matt Groening for the \nFox ... Since its <b>debut</b> on December 17, 1989, 674 episodes of The <b>Simpsons</b> \nhave been broadcast. ... When producer James L. Brooks <b>was</b> working on the \n<b>television</b> variety show The Tracey Ullman Show, he decided to include small \nanimated&nbsp;...',
     '... in shorts from The Tracey Ullman Show as their <b>television debut</b> in 1987. The \n<b>Simpsons</b> shorts are a series of animated shorts that <b>aired</b> as a recurring \nsegment on Fox variety <b>television</b> series The Tracey ... The final short to <b>air was</b> &quot;\n<b>TV Simpsons</b>&quot;, originally airing on May 14, 1989. The <b>Simpsons</b> later debuted on\n&nbsp;...',
     'The <b>first</b> season of the American animated <b>television</b> series The <b>Simpsons</b> \noriginally <b>aired</b> on the Fox network between December 17, 1989, and May 13, \n1990, beginning with the Christmas special &quot;<b>Simpsons</b> Roasting on an Open Fire\n&quot;. The executive producers for the <b>first</b> production season <b>were</b> Matt Groening,&nbsp;...',
     'The <b>Simpsons</b> is an American animated <b>television</b> sitcom created by Matt \nGroening for the Fox ... Since its <b>debut</b> on December 17, 1989, The <b>Simpsons</b> \n<b>has</b> broadcast 674 episodes. The show holds several American <b>television</b> \nlongevity&nbsp;...',
     'The opening sequence of the American animated <b>television</b> series The <b>Simpsons</b> \nis among the most popular opening sequences in <b>television</b> and is accompanied \nby one of <b>television&#39;s</b> most recognizable theme songs. The <b>first</b> episode to use \nthis intro <b>was</b> the series&#39; second episode &quot;Bart the ... <b>was</b> the <b>first</b> episode of The \n<b>Simpsons</b> to <b>air</b> in 720p high-definition <b>television</b>,&nbsp;...',
     '&quot;<b>Simpsons</b> Roasting on an Open Fire&quot;, titled onscreen as &quot;The <b>Simpsons</b> \nChristmas Special&quot;, is the premiere episode of the American animated <b>TV</b> series \nThe <b>Simpsons</b>, ... The show <b>was</b> originally intended to <b>debut</b> earlier in 1989 with &quot;\nSome Enchanted Evening&quot;, but due to animation problems with that episode, the \nshow&nbsp;...',
     '&quot;Stark Raving Dad&quot; is the <b>first</b> episode of the third season of the American \nanimated <b>television</b> series The <b>Simpsons</b>. It <b>first aired</b> on the Fox network in the \nUnited States on September 19, 1991. ... The <b>Simpsons was</b> the second highest \nrated show on Fox the week it <b>aired</b>, behind Married... with Children. &quot;Stark \nRaving Dad,&quot;&nbsp;...',
     'The <b>Simpsons</b>&#39; twentieth season <b>aired</b> on Fox from September 28, 2008 to May \n17, 2009. With this season, the show tied Gunsmoke as the longest-running \nAmerican primetime <b>television</b> series in terms of total number ... It <b>was</b> the <b>first</b>-\never episode of the show to <b>air</b> in Europe before being seen in the United States.',
     'The animated <b>TV</b> show The <b>Simpsons</b> is an American English language \nanimated sitcom which ... The <b>Simpsons was</b> dubbed for the <b>first</b> time in Punjabi \nand <b>aired</b> on Geo <b>TV</b> in Pakistan. The name of the localised Punjabi version is \nTedi Sim&nbsp;...'],
    'title': ['History of The Simpsons',
     'The Simpsons',
     'The Simpsons shorts',
     'The Simpsons (season 1)',
     'List of The Simpsons episodes',
     'The Simpsons opening sequence',
     'Simpsons Roasting on an Open Fire',
     'Stark Raving Dad',
     'The Simpsons (season 20)',
     'Non-English versions of The Simpsons']}]},
 'viewed_doc_titles': ['The Simpsons']}
```

### Data Fields

Full
```
{'id': Value(dtype='string', id=None),
 'question': Value(dtype='string', id=None),
 'annotations': Sequence(feature={'type': Value(dtype='string', id=None), 'answer': Sequence(feature=Value(dtype='string', id=None), length=-1, id=None), 'qaPairs': Sequence(feature={'question': Value(dtype='string', id=None), 'answer': Sequence(feature=Value(dtype='string', id=None), length=-1, id=None)}, length=-1, id=None)}, length=-1, id=None),
 'viewed_doc_titles': Sequence(feature=Value(dtype='string', id=None), length=-1, id=None),
 'used_queries': Sequence(feature={'query': Value(dtype='string', id=None), 'results': Sequence(feature={'title': Value(dtype='string', id=None), 'snippet': Value(dtype='string', id=None)}, length=-1, id=None)}, length=-1, id=None),
 'nq_answer': Sequence(feature=Value(dtype='string', id=None), length=-1, id=None),
 'nq_doc_title': Value(dtype='string', id=None)}
```
In the original data format `annotations` have different keys depending on the `type` field = `singleAnswer` or `multipleQAs`. But this implementation uses an empty list `[]` for the unavailable keys 

please refer to Dataset Contents(https://github.com/shmsw25/AmbigQA#dataset-contents) for more details.

```
for example in train_light_dataset:
    for i,t in enumerate(example['annotations']['type']):
        if t =='singleAnswer':
            # use the example['annotations']['answer'][i]
            # example['annotations']['qaPairs'][i] - > is []
            print(example['annotations']['answer'][i])
        else:
            # use the example['annotations']['qaPairs'][i]
            # example['annotations']['answer'][i] - > is []
            print(example['annotations']['qaPairs'][i])
```

please refer to Dataset Contents(https://github.com/shmsw25/AmbigQA#dataset-contents) for more details.

Light version only has `id`, `question`, `annotations` fields

### Data Splits

- train: 10036
- validation: 2002


## Dataset Creation

### Curation Rationale

[More Information Needed]

### Source Data

- Wikipedia
- NQ-open:
```
@article{ kwiatkowski2019natural,
  title={ Natural questions: a benchmark for question answering research},
  author={ Kwiatkowski, Tom and Palomaki, Jennimaria and Redfield, Olivia and Collins, Michael and Parikh, Ankur and Alberti, Chris and Epstein, Danielle and Polosukhin, Illia and Devlin, Jacob and Lee, Kenton and others },
  journal={ Transactions of the Association for Computational Linguistics },
  year={ 2019 }
}
```

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

[CC BY-SA 3.0](http://creativecommons.org/licenses/by-sa/3.0/)

### Citation Information
```
@inproceedings{ min2020ambigqa,
    title={ {A}mbig{QA}: Answering Ambiguous Open-domain Questions },
    author={ Min, Sewon and Michael, Julian and Hajishirzi, Hannaneh and Zettlemoyer, Luke },
    booktitle={ EMNLP },
    year={2020}
}
```
### Contributions

Thanks to [@cceyda](https://github.com/cceyda) for adding this dataset.