---
annotations_creators:
- crowdsourced
language_creators:
- crowdsourced
languages:
- en
licenses:
- mit
multilinguality:
- monolingual
pretty_name: Reddit TIFU
size_categories:
- 100K<n<1M
source_datasets:
- original
task_categories:
- summarization
task_ids:
- summarization-other-reddit-posts-summarization
paperswithcode_id: reddit-tifu
---

# Dataset Card for "reddit_tifu"

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

- **Homepage:** [https://github.com/ctr4si/MMN](https://github.com/ctr4si/MMN)
- **Repository:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Paper:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Point of Contact:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Size of downloaded dataset files:** 1279.08 MB
- **Size of the generated dataset:** 219.12 MB
- **Total amount of disk used:** 1498.20 MB

### Dataset Summary

Reddit dataset, where TIFU denotes the name of subbreddit /r/tifu.
As defined in the publication, style "short" uses title as summary and
"long" uses tldr as summary.

Features includes:
  - document: post text without tldr.
  - tldr: tldr line.
  - title: trimmed title without tldr.
  - ups: upvotes.
  - score: score.
  - num_comments: number of comments.
  - upvote_ratio: upvote ratio.

### Supported Tasks and Leaderboards

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Languages

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

## Dataset Structure

We show detailed information for up to 5 configurations of the dataset.

### Data Instances

#### long

- **Size of downloaded dataset files:** 639.54 MB
- **Size of the generated dataset:** 87.74 MB
- **Total amount of disk used:** 727.29 MB

An example of 'train' looks as follows.
```
{'ups': 115.0,
 'num_comments': 23.0,
 'upvote_ratio': 0.88,
 'score': 115.0,
 'documents': 'this actually happened a couple of years ago. i grew up in germany where i went to a german secondary school that went from 5th to 13th grade (we still had 13 grades then, they have since changed that). my school was named after anne frank and we had a club that i was very active in from 9th grade on, which was dedicated to teaching incoming 5th graders about anne franks life, discrimination, anti-semitism, hitler, the third reich and that whole spiel. basically a day where the students\' classes are cancelled and instead we give them an interactive history and social studies class with lots of activities and games. \n\nthis was my last year at school and i already had a lot of experience doing these project days with the kids. i was running the thing with a friend, so it was just the two of us and 30-something 5th graders. we start off with a brief introduction and brainstorming: what do they know about anne frank and the third reich? you\'d be surprised how much they know. anyway after the brainstorming we do a few activities, and then we take a short break. after the break we split the class into two groups to make it easier to handle. one group watches a short movie about anne frank while the other gets a tour through our poster presentation that our student group has been perfecting over the years. then the groups switch. \n\ni\'m in the classroom to show my group the movie and i take attendance to make sure no one decided to run away during break. i\'m going down the list when i come to the name sandra (name changed). a kid with a boyish haircut and a somewhat deeper voice, wearing clothes from the boy\'s section at a big clothing chain in germany, pipes up. \n\nnow keep in mind, these are all 11 year olds, they are all pre-pubescent, their bodies are not yet showing any sex specific features one would be able to see while they are fully clothed (e.g. boobs, beards,...). this being a 5th grade in the rather conservative (for german standards) bavaria, i was confused. i looked down at the list again making sure i had read the name right. look back up at the kid. \n\nme: "you\'re sandra?"\n\nkid: "yep."\n\nme: "oh, sorry. *thinking the kid must be from somewhere where sandra is both a girl\'s and boy\'s name* where are you from? i\'ve only ever heard that as a girl\'s name before."\n\nthe class starts laughing. sandra gets really quiet. "i am a girl..." she says. some of the other students start saying that their parents made the same mistake when they met sandra. i feel so sorry and stupid. i get the class to calm down and finish taking attendance. we watch the movie in silence. after the movie, when we walked down to where the poster presentation took place i apologised to sandra. i felt so incredibly terrible, i still do to this day. throughout the rest of the day i heard lots of whispers about sandra. i tried to stop them whenever they came up, but there was no stopping the 5th grade gossip i had set in motion.\n\nsandra, if you\'re out there, i am so incredibly sorry for humiliating you in front of your class. i hope you are happy and healthy and continue to live your life the way you like. don\'t let anyone tell you you have to dress or act a certain way just because of the body parts you were born with. i\'m sorry if i made you feel like you were wrong for dressing and acting differently. i\'m sorry i probably made that day hell for you. i\'m sorry for my ignorance.',
 'tldr': 'confuse a 5th grade girl for a boy in front of half of her class. kids are mean. sorry sandra.**',
 'title': 'gender-stereotyping'}
```

#### short

- **Size of downloaded dataset files:** 639.54 MB
- **Size of the generated dataset:** 131.37 MB
- **Total amount of disk used:** 770.92 MB

An example of 'train' looks as follows.
```
{'ups': 50.0,
 'num_comments': 13.0,
 'upvote_ratio': 0.77,
 'score': 50.0,
 'documents': "i was on skype on my tablet as i went to the toilet iming a friend. i don't multitask very well, so i forgot one of the most important things to do before pooping. i think the best part was when i realised and told my mate who just freaked out because i was talking to him on the john!",
 'tldr': '',
 'title': 'forgetting to pull my underwear down before i pooped.'}
```

### Data Fields

The data fields are the same among all splits.

#### long
- `ups`: a `float32` feature.
- `num_comments`: a `float32` feature.
- `upvote_ratio`: a `float32` feature.
- `score`: a `float32` feature.
- `documents`: a `string` feature.
- `tldr`: a `string` feature.
- `title`: a `string` feature.

#### short
- `ups`: a `float32` feature.
- `num_comments`: a `float32` feature.
- `upvote_ratio`: a `float32` feature.
- `score`: a `float32` feature.
- `documents`: a `string` feature.
- `tldr`: a `string` feature.
- `title`: a `string` feature.

### Data Splits

|name |train|
|-----|----:|
|long |42139|
|short|79740|

## Dataset Creation

### Curation Rationale

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Source Data

#### Initial Data Collection and Normalization

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

#### Who are the source language producers?

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Annotations

#### Annotation process

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

#### Who are the annotators?

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Personal and Sensitive Information

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

## Considerations for Using the Data

### Social Impact of Dataset

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Discussion of Biases

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Other Known Limitations

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

## Additional Information

### Dataset Curators

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Licensing Information

MIT License.

### Citation Information

```
@misc{kim2018abstractive,
    title={Abstractive Summarization of Reddit Posts with Multi-level Memory Networks},
    author={Byeongchang Kim and Hyunwoo Kim and Gunhee Kim},
    year={2018},
    eprint={1811.00783},
    archivePrefix={arXiv},
    primaryClass={cs.CL}
}
```

### Contributions

Thanks to [@patrickvonplaten](https://github.com/patrickvonplaten), [@thomwolf](https://github.com/thomwolf) for adding this dataset.
