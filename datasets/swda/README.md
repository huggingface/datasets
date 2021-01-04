---
annotations_creators:
- found
language_creators:
- found
languages:
- en
licenses:
- cc-by-nc-sa-3.0
multilinguality:
- monolingual
size_categories:
- n<1K
source_datasets:
- extended|other-Switchboard-1 Telephone Speech Corpus, Release 2
task_categories:
- text-classification
task_ids:
- multi-label-classification
---

# Dataset Card for swda

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

## Dataset Description

- **Homepage: [The Switchboard Dialog Act Corpus](http://compprag.christopherpotts.net/swda.html)**
- **Repository: [NathanDuran/Switchboard-Corpus](https://github.com/NathanDuran/Switchboard-Corpus)**
- **Paper:[The Switchboard Dialog Act Corpus](http://compprag.christopherpotts.net/swda.html)**
= **Leaderboard: [Dialogue act classification](https://github.com/sebastianruder/NLP-progress/blob/master/english/dialogue.md#dialogue-act-classification)**
- **Point of Contact: [Christopher Potts](https://web.stanford.edu/~cgpotts/)**

### Dataset Summary

The Switchboard Dialog Act Corpus (SwDA) extends the Switchboard-1 Telephone Speech Corpus, Release 2 with 
turn/utterance-level dialog-act tags. The tags summarize syntactic, semantic, and pragmatic information about the 
associated turn. The SwDA project was undertaken at UC Boulder in the late 1990s.
The SwDA is not inherently linked to the Penn Treebank 3 parses of Switchboard, and it is far from straightforward to 
align the two resources. In addition, the SwDA is not distributed with the Switchboard's tables of metadata about the 
conversations and their participants.


### Supported Tasks and Leaderboards

| Model           | Accuracy  |  Paper / Source | Code |
| ------------- | :-----:| --- | --- |
| SGNN (Ravi et al., 2018) | 83.1 | [Self-Governing Neural Networks for On-Device Short Text Classification](https://www.aclweb.org/anthology/D18-1105.pdf)
| CASA (Raheja et al., 2019) | 82.9 | [Dialogue Act Classification with Context-Aware Self-Attention](https://www.aclweb.org/anthology/N19-1373.pdf)
| DAH-CRF (Li et al., 2019) | 82.3 | [A Dual-Attention Hierarchical Recurrent Neural Network for Dialogue Act Classification](https://www.aclweb.org/anthology/K19-1036.pdf)
| ALDMN (Wan et al., 2018) | 81.5 | [Improved Dynamic Memory Network for Dialogue Act Classification with Adversarial Training](https://arxiv.org/pdf/1811.05021.pdf)
| CRF-ASN (Chen et al., 2018) | 81.3 | [Dialogue Act Recognition via CRF-Attentive Structured Network](https://arxiv.org/abs/1711.05568) | |
| Bi-LSTM-CRF (Kumar et al., 2017) | 79.2 | [Dialogue Act Sequence Labeling using Hierarchical encoder with CRF](https://arxiv.org/abs/1709.04250) | [Link](https://github.com/YanWenqiang/HBLSTM-CRF) |
| RNN with 3 utterances in context (Bothe et al., 2018) | 77.34 | [A Context-based Approach for Dialogue Act Recognition using Simple Recurrent Neural Networks](https://arxiv.org/abs/1805.06280) | |

### Languages

The language supported is English.

## Dataset Structure

Utterance are tagged with the [SWBD-DAMSL](https://web.stanford.edu/~jurafsky/ws97/manual.august1.html) DA.

### Data Instances

A|What is the nature of your company's business?|qw

B|Well, it's actually, uh,|^h

B|we do oil well services.|sd

### Data Fields

Utterances are written one per line in the format Speaker | Utterance Text | Dialogue Act Tag.
Setting the utterance_only_flag == True, will change the default output to only one utterance per line i.e. no speaker or DA tags.
Utterances marked as Non-verbal ('x' tags) are removed i.e. 'Laughter' or 'Throat_clearing'.
Utterances marked as Interrupted ('+' tags) and continued later are concatenated to make un-interrupted sentences.
All disfluency annotations are removed i.e. '#', '<', '>', etc.

## Dialogue Acts
Dialogue Act                   |        Labels        |  Count   |    %     |   Train Count   | Train %  |   Test Count    |  Test %  |    Val Count    |  Val %  
--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---:
Statement-non-opinion          |          sd          |  75136   |  37.62   |      72549      |  37.71   |      1317       |  32.30   |      1270       |  38.81  
Acknowledge (Backchannel)      |          b           |  38281   |  19.17   |      36950      |  19.21   |       764       |  18.73   |       567       |  17.33  
Statement-opinion              |          sv          |  26421   |  13.23   |      25087      |  13.04   |       718       |  17.61   |       616       |  18.83  
Uninterpretable                |          %           |  15195   |   7.61   |      14597      |   7.59   |       349       |   8.56   |       249       |   7.61  
Agree/Accept                   |          aa          |  11123   |   5.57   |      10770      |   5.60   |       207       |   5.08   |       146       |   4.46  
Appreciation                   |          ba          |   4757   |   2.38   |      4619       |   2.40   |       76        |   1.86   |       62        |   1.89  
Yes-No-Question                |          qy          |   4725   |   2.37   |      4594       |   2.39   |       84        |   2.06   |       47        |   1.44  
Yes Answers                    |          ny          |   3030   |   1.52   |      2918       |   1.52   |       73        |   1.79   |       39        |   1.19  
Conventional-closing           |          fc          |   2581   |   1.29   |      2480       |   1.29   |       81        |   1.99   |       20        |   0.61  
Wh-Question                    |          qw          |   1976   |   0.99   |      1896       |   0.99   |       55        |   1.35   |       25        |   0.76  
No Answers                     |          nn          |   1374   |   0.69   |      1334       |   0.69   |       26        |   0.64   |       14        |   0.43  
Response Acknowledgement       |          bk          |   1306   |   0.65   |      1271       |   0.66   |       28        |   0.69   |        7        |   0.21  
Hedge                          |          h           |   1226   |   0.61   |      1181       |   0.61   |       23        |   0.56   |       22        |   0.67  
Declarative Yes-No-Question    |         qy^d         |   1218   |   0.61   |      1167       |   0.61   |       36        |   0.88   |       15        |   0.46  
Backchannel in Question Form   |          bh          |   1053   |   0.53   |      1015       |   0.53   |       21        |   0.51   |       17        |   0.52  
Quotation                      |          ^q          |   983    |   0.49   |       931       |   0.48   |       17        |   0.42   |       35        |   1.07  
Summarize/Reformulate          |          bf          |   952    |   0.48   |       905       |   0.47   |       23        |   0.56   |       24        |   0.73  
Other                          |   fo_o_fw_"_by_bc    |   879    |   0.44   |       857       |   0.45   |       15        |   0.37   |        7        |   0.21  
Affirmative Non-yes Answers    |          na          |   847    |   0.42   |       831       |   0.43   |       10        |   0.25   |        6        |   0.18  
Action-directive               |          ad          |   745    |   0.37   |       712       |   0.37   |       27        |   0.66   |        6        |   0.18  
Collaborative Completion       |          ^2          |   723    |   0.36   |       690       |   0.36   |       19        |   0.47   |       14        |   0.43  
Repeat-phrase                  |         b^m          |   687    |   0.34   |       655       |   0.34   |       21        |   0.51   |       11        |   0.34  
Open-Question                  |          qo          |   656    |   0.33   |       631       |   0.33   |       16        |   0.39   |        9        |   0.28  
Rhetorical-Question            |          qh          |   575    |   0.29   |       554       |   0.29   |       12        |   0.29   |        9        |   0.28  
Hold Before Answer/Agreement   |          ^h          |   556    |   0.28   |       539       |   0.28   |        7        |   0.17   |       10        |   0.31  
Reject                         |          ar          |   344    |   0.17   |       337       |   0.18   |        3        |   0.07   |        4        |   0.12  
Negative Non-no Answers        |          ng          |   302    |   0.15   |       290       |   0.15   |        6        |   0.15   |        6        |   0.18  
Signal-non-understanding       |          br          |   298    |   0.15   |       286       |   0.15   |        9        |   0.22   |        3        |   0.09  
Other Answers                  |          no          |   284    |   0.14   |       277       |   0.14   |        6        |   0.15   |        1        |   0.03  
Conventional-opening           |          fp          |   225    |   0.11   |       220       |   0.11   |        5        |   0.12   |        0        |   0.00  
Or-Clause                      |         qrr          |   209    |   0.10   |       206       |   0.11   |        2        |   0.05   |        1        |   0.03  
Dispreferred Answers           |        arp_nd        |   207    |   0.10   |       204       |   0.11   |        3        |   0.07   |        0        |   0.00  
3rd-party-talk                 |          t3          |   117    |   0.06   |       115       |   0.06   |        0        |   0.00   |        2        |   0.06  
Offers, Options Commits        |       oo_co_cc       |   110    |   0.06   |       109       |   0.06   |        0        |   0.00   |        1        |   0.03  
Maybe/Accept-part              |        aap_am        |   104    |   0.05   |       97        |   0.05   |        7        |   0.17   |        0        |   0.00  
Downplayer                     |          t1          |   103    |   0.05   |       102       |   0.05   |        1        |   0.02   |        0        |   0.00  
Self-talk                      |          bd          |   103    |   0.05   |       100       |   0.05   |        1        |   0.02   |        2        |   0.06  
Tag-Question                   |          ^g          |    92    |   0.05   |       92        |   0.05   |        0        |   0.00   |        0        |   0.00  
Declarative Wh-Question        |         qw^d         |    80    |   0.04   |       79        |   0.04   |        1        |   0.02   |        0        |   0.00  
Apology                        |          fa          |    79    |   0.04   |       76        |   0.04   |        2        |   0.05   |        1        |   0.03  
Thanking                       |          ft          |    78    |   0.04   |       67        |   0.03   |        7        |   0.17   |        4        |   0.12  

![Label Frequencies](swda_data/metadata/Swda%20Label%20Frequency%20Distributions.png)

### Data Splits

he data is split into the original training and test sets suggested by the authors (1115 training and 19 test). The remaining 21 dialogues have been used as a validation set.

## Dataset Creation

### Curation Rationale

[More Information Needed]

### Source Data

#### Initial Data Collection and Normalization

- Total number of utterances: 199740
- Maximum utterance length: 133
- Mean utterance length: 9.6
- Total number of dialogues: 1155
- Maximum dialogue length: 457
- Mean dialogue length: 172.9
- Vocabulary size: 22301
- Number of labels: 41
- Number of dialogue in train set: 1115
- Maximum length of dialogue in train set: 457
- Number of dialogue in test set: 19
- Maximum length of dialogue in test set: 330
- Number of dialogue in val set: 21
- Maximum length of dialogue in val set: 299

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

[Christopher Potts](https://web.stanford.edu/~cgpotts/), Stanford Linguistics.

### Licensing Information

This work is licensed under a [Creative Commons Attribution-NonCommercial-ShareAlike 3.0 Unported License.](http://creativecommons.org/licenses/by-nc-sa/3.0/)

### Citation Information

```
@techreport{Jurafsky-etal:1997,
	Address = {Boulder, CO},
	Author = {Jurafsky, Daniel and Shriberg, Elizabeth and Biasca, Debra},
	Institution = {University of Colorado, Boulder Institute of Cognitive Science},
	Number = {97-02},
	Title = {Switchboard {SWBD}-{DAMSL} Shallow-Discourse-Function Annotation Coders Manual, Draft 13},
	Year = {1997}}

@article{Shriberg-etal:1998,
	Author = {Shriberg, Elizabeth and Bates, Rebecca and Taylor, Paul and Stolcke, Andreas and Jurafsky, Daniel and Ries, Klaus and Coccaro, Noah and Martin, Rachel and Meteer, Marie and Van Ess-Dykema, Carol},
	Journal = {Language and Speech},
	Number = {3--4},
	Pages = {439--487},
	Title = {Can Prosody Aid the Automatic Classification of Dialog Acts in Conversational Speech?},
	Volume = {41},
	Year = {1998}}

@article{Stolcke-etal:2000,
	Author = {Stolcke, Andreas and Ries, Klaus and Coccaro, Noah and Shriberg, Elizabeth and Bates, Rebecca and Jurafsky, Daniel and Taylor, Paul and Martin, Rachel and Meteer, Marie and Van Ess-Dykema, Carol},
	Journal = {Computational Linguistics},
	Number = {3},
	Pages = {339--371},
	Title = {Dialogue Act Modeling for Automatic Tagging and Recognition of Conversational Speech},
	Volume = {26},
	Year = {2000}}
```
