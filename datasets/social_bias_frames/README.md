---
pretty_name: Social Bias Frames
annotations_creators:
- crowdsourced
language_creators:
- found
language:
- en
license:
- cc-by-4.0
multilinguality:
- monolingual
size_categories:
- 100K<n<1M
source_datasets:
- original
task_categories:
- text2text-generation
- text-classification
task_ids:
- text2text-generation-other-explanation-generation
- hate-speech-detection
paperswithcode_id: null
---


# Dataset Card for "social_bias_frames"

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

- **Homepage:** [https://homes.cs.washington.edu/~msap/social-bias-frames/](https://homes.cs.washington.edu/~msap/social-bias-frames/)
- **Repository:** [https://homes.cs.washington.edu/~msap/social-bias-frames/](https://homes.cs.washington.edu/~msap/social-bias-frames/)
- **Paper:** [Social Bias Frames: Reasoning about Social and Power Implications of Language](https://www.aclweb.org/anthology/2020.acl-main.486.pdf)
- **Leaderboard:**
- **Point of Contact:** [Maartin Sap](mailto:msap@cs.washington.edu)
- **Size of downloaded dataset files:** 6.03 MB
- **Size of the generated dataset:** 42.41 MB
- **Total amount of disk used:** 48.45 MB

### Dataset Summary

Warning: this document and dataset contain content that may be offensive or upsetting.

Social Bias Frames is a new way of representing the biases and offensiveness that are implied in language. For example, these frames are meant to distill the implication that "women (candidates) are less qualified" behind the statement "we shouldn’t lower our standards to hire more women." The Social Bias Inference Corpus (SBIC) supports large-scale learning and evaluation of social implications with over 150k structured annotations of social media posts, spanning over 34k implications about a thousand demographic groups.

### Supported Tasks and Leaderboards

This dataset supports both classification and generation. Sap et al. developed several models using the SBIC. They report an F1 score of 78.8 in predicting whether the posts in the test set were offensive, an F1 score of 78.6 in predicting whether the posts were intending to be offensive, an F1 score of 80.7 in predicting whether the posts were lewd, and an F1 score of 69.9 in predicting whether the posts were targeting a specific group. 

Another of Sap et al.’s models performed better in the generation task. They report a BLUE score of 77.9, a Rouge-L score of 68.7, and a WMD score of 0.74 in generating a description of the targeted group given a post as well as a BLUE score of 52.6, a Rouge-L score of 44.9, and a WMD score of 2.79 in generating a description of the implied offensive statement given a post. See the paper for further details. 

### Languages

The language in SBIC is predominantly white-aligned English (78%, using a lexical dialect detector, [Blodgett et al., 2016](https://www.aclweb.org/anthology/D16-1120)). The curators find less than 10% of posts in SBIC are detected to have the AAE dialect category. The BCP-47 language tag is, presumably, en-US. 

## Dataset Structure

### Data Instances

Each instance contains a post that may contain an offensive statement and annotated information concerning the nature of the offensive implication as well as the demographics of the annotator and origin of the post. See the [Social Bias Frames dataset viewer](https://huggingface.co/datasets/viewer/?dataset=social_bias_frames) to explore more examples. 

#### default

- **Size of downloaded dataset files:** 6.03 MB
- **Size of the generated dataset:** 42.41 MB
- **Total amount of disk used:** 48.45 MB

An example of 'validation' looks as follows.
```
{
    "HITId": "3Z8UJEJOCZ74QHXOTFP0JOOGD7039J",
    "WorkerId": "7162172225567546910",
    "annotatorAge": "27.0",
    "annotatorGender": "woman",
    "annotatorMinority": "women",
    "annotatorPolitics": "liberal",
    "annotatorRace": "white",
    "dataSource": "t/davidson",
    "intentYN": "1.0",
    "offensiveYN": "1.0",
    "post": "Every half-breed cop in America is trying to rape white women.",
    "sexPhrase": "rape white women",
    "sexReason": "rape",
    "sexYN": "1.0",
    "speakerMinorityYN": "0.0",
    "targetCategory": "race",
    "targetMinority": "mixed folks",
    "targetStereotype": "mixed folks are rapists.",
    "whoTarget": "1.0"
}
```

### Data Fields

The data fields are the same among all splits.

#### default
- _whoTarget_: a string, ‘0.0’ if the target is a group, ‘1.0’ if the target is an individual, and blank if the post is not offensive
- _intentYN_: a string indicating if the intent behind the statement was to offend. This is a categorical variable with four possible answers, ‘1.0’ if yes, ‘0.66’ if probably, ‘0.33’ if probably not, and ‘0.0’ if no. 
- _sexYN_: a string indicating whether the post contains a sexual or lewd reference. This is a categorical variable with three possible answers, ‘1.0’ if yes, ‘0.5’ if maybe, ‘0.0’ if no. 
- _sexReason_: a string containing a free text explanation of what is sexual if indicated so, blank otherwise
- _offensiveYN_: a string indicating if the post could be offensive to anyone. This is a categorical variable with three possible answers, ‘1.0’ if yes, ‘0.5’ if maybe, ‘0.0’ if no.
- _annotatorGender_: a string indicating the gender of the MTurk worker
- _annotatorMinority_: a string indicating whether the MTurk worker identifies as a minority
- _sexPhrase_: a string indicating which part of the post references something sexual, blank otherwise
- _speakerMinorityYN_: a string indicating whether the speaker was part of the same minority group that's being targeted. This is a categorical variable with three possible answers, ‘1.0’ if yes, ‘0.5’ if maybe, ‘0.0’ if no. 
- _WorkerId_: a string hashed version of the MTurk workerId
- _HITId_: a string id that uniquely identifies each post
- _annotatorPolitics_: a string indicating the political leaning of the MTurk worker
- _annotatorRace_: a string indicating the race of the MTurk worker
- _annotatorAge_: a string indicating the age of the MTurk worker
- _post_: a string containing the text of the post that was annotated
- _targetMinority_: a string indicating the demographic group targeted
- _targetCategory_: a string indicating the high-level category of the demographic group(s) targeted
- _targetStereotype_: a string containing the implied statement
- _dataSource_: a string indicating the source of the post (`t/...`: means Twitter, `r/...`: means a subreddit)


### Data Splits

To ensure that no post appeared in multiple splits, the curators defined a training instance as the post and its three sets of annotations. They then split the dataset into train, validation, and test sets (75%/12.5%/12.5%).

| name  |train |validation|test |
|-------|-----:|---------:|----:|
|default|112900|     16738|17501|

## Dataset Creation

### Curation Rationale

The main aim for this dataset is to cover a wide variety of social biases that are implied in text, both subtle and overt, and make the biases representative of real world discrimination that people experience [RWJF 2017](https://web.archive.org/web/20200620105955/https://www.rwjf.org/en/library/research/2017/10/discrimination-in-america--experiences-and-views.html). The curators also included some innocuous statements, to balance out biases, offensive, or harmful content.

### Source Data

The curators included online posts from the following sources sometime between 2014-2019:
- r/darkJokes, r/meanJokes, r/offensiveJokes
- Reddit microaggressions ([Breitfeller et al., 2019](https://www.aclweb.org/anthology/D19-1176/))
- Toxic language detection Twitter corpora ([Waseem & Hovy, 2016](https://www.aclweb.org/anthology/N16-2013/); [Davidson et al., 2017](https://www.aaai.org/ocs/index.php/ICWSM/ICWSM17/paper/viewPaper/15665); [Founa et al., 2018](https://www.aaai.org/ocs/index.php/ICWSM/ICWSM18/paper/viewPaper/17909))
- Data scraped from hate sites (Gab, Stormfront, r/incels, r/mensrights)

#### Initial Data Collection and Normalization

The curators wanted posts to be as self-contained as possible, therefore, they applied some filtering to prevent posts from being highly context-dependent. For Twitter data, they filtered out @-replies, retweets, and links, and subsample posts such that there is a smaller correlation between AAE and offensiveness (to avoid racial bias; [Sap et al., 2019](https://www.aclweb.org/anthology/P19-1163/)). For Reddit, Gab, and Stormfront, they only selected posts that were one sentence long, don't contain links, and are between 10 and 80 words. Furthemore, for Reddit, they automatically removed posts that target automated moderation.

#### Who are the source language producers?

Due to the nature of this corpus, there is no way to know who the speakers are. But, the speakers of the Reddit, Gab, and Stormfront posts are likely white men (see [Gender by subreddit](http://bburky.com/subredditgenderratios/), [Gab users](https://en.wikipedia.org/wiki/Gab_(social_network)#cite_note-insidetheright-22), [Stormfront description](https://en.wikipedia.org/wiki/Stormfront_(website))).

### Annotations

#### Annotation process

For each post, Amazon Mechanical Turk workers indicate whether the post is offensive, whether the intent was to offend, and whether it contains lewd or sexual content.  Only if annotators  indicate potential offensiveness do they answer the group implication question. If the post targets or references a group or demographic, workers select or write which one(s); per selected group, they then write two to four stereotypes. Finally, workers are asked whether they think the speaker is part of one of the minority groups referenced by the post. The curators collected three annotations per post, and restricted the worker pool to the U.S. and Canada. The annotations in SBIC showed 82.4% pairwise agreement and Krippendorf’s α=0.45 on average.

Recent  work  has  highlighted  various  negative  side  effects  caused  by annotating potentially abusive or harmful content (e.g., acute stress; Roberts, 2016). The curators mitigated these by  limiting the number of posts that one worker could annotate in one day, paying workers above minimum wage ($7–12), and providing crisis management resources to the annotators.

#### Who are the annotators?

The annotators are Amazon Mechanical Turk workers aged 36±10 years old. The annotators consisted of 55% women, 42% men, and <1% non-binary and 82% identified as White, 4% Asian, 4% Hispanic, 4% Black. Information on their first language(s) and professional backgrounds was not collected. 

### Personal and Sensitive Information

Usernames are not included with the data, but the site where the post was collected is, so the user could potentially be recovered. 

## Considerations for Using the Data

### Social Impact of Dataset

The curators recognize that studying Social Bias Frames necessarily requires confronting online content that may be offensive or disturbing but argue that deliberate avoidance does not eliminate such problems. By assessing social media content through the lens of Social Bias Frames, automatic flagging or AI-augmented writing interfaces may be analyzed for potentially harmful online content with detailed explanations for users or moderators to consider and verify. In addition, the collective analysis over large corpora can also be insightful for educating people on reducing unconscious biases in their language by encouraging empathy towards a targeted group.

### Discussion of Biases

Because this is a corpus of social biases, a lot of posts contain implied or overt biases against the following groups (in decreasing order of prevalence):
- gender/sexuality
- race/ethnicity
- religion/culture
- social/political
- disability body/age
- victims

The curators warn that technology trained on this dataset could have side effects such as censorship and dialect-based racial bias. 

### Other Known Limitations

Because the curators found that the dataset is predominantly written in White-aligned English, they caution researchers to consider the potential for dialect or identity-based biases in labelling ([Davidson et al.,2019](https://www.aclweb.org/anthology/W19-3504.pdf); [Sap et al., 2019a](https://www.aclweb.org/anthology/P19-1163.pdf)) before deploying technology based on SBIC.

## Additional Information

### Dataset Curators

This dataset was developed by Maarten Sap of the Paul G. Allen School of Computer Science & Engineering at the University of Washington, Saadia Gabriel, Lianhui Qin, Noah A Smith, and Yejin Choi of the Paul G. Allen School of Computer Science & Engineering and the Allen Institute for Artificial Intelligence, and Dan Jurafsky of the Linguistics & Computer Science Departments of Stanford University.

### Licensing Information

The SBIC is licensed under the [Creative Commons 4.0 License](https://creativecommons.org/licenses/by/4.0/)

### Citation Information

```
@inproceedings{sap-etal-2020-social,
    title = "Social Bias Frames: Reasoning about Social and Power Implications of Language",
    author = "Sap, Maarten  and
      Gabriel, Saadia  and
      Qin, Lianhui  and
      Jurafsky, Dan  and
      Smith, Noah A.  and
      Choi, Yejin",
    booktitle = "Proceedings of the 58th Annual Meeting of the Association for Computational Linguistics",
    month = jul,
    year = "2020",
    address = "Online",
    publisher = "Association for Computational Linguistics",
    url = "https://www.aclweb.org/anthology/2020.acl-main.486",
    doi = "10.18653/v1/2020.acl-main.486",
    pages = "5477--5490",
    abstract = "Warning: this paper contains content that may be offensive or upsetting. Language has the power to reinforce stereotypes and project social biases onto others. At the core of the challenge is that it is rarely what is stated explicitly, but rather the implied meanings, that frame people{'}s judgments about others. For example, given a statement that {``}we shouldn{'}t lower our standards to hire more women,{''} most listeners will infer the implicature intended by the speaker - that {``}women (candidates) are less qualified.{''} Most semantic formalisms, to date, do not capture such pragmatic implications in which people express social biases and power differentials in language. We introduce Social Bias Frames, a new conceptual formalism that aims to model the pragmatic frames in which people project social biases and stereotypes onto others. In addition, we introduce the Social Bias Inference Corpus to support large-scale modelling and evaluation with 150k structured annotations of social media posts, covering over 34k implications about a thousand demographic groups. We then establish baseline approaches that learn to recover Social Bias Frames from unstructured text. We find that while state-of-the-art neural models are effective at high-level categorization of whether a given statement projects unwanted social bias (80{\%} F1), they are not effective at spelling out more detailed explanations in terms of Social Bias Frames. Our study motivates future work that combines structured pragmatic inference with commonsense reasoning on social implications.",
}

```

### Contributions

Thanks to [@thomwolf](https://github.com/thomwolf), [@lewtun](https://github.com/lewtun), [@otakumesi](https://github.com/otakumesi), [@mariamabarham](https://github.com/mariamabarham), [@lhoestq](https://github.com/lhoestq) for adding this dataset.