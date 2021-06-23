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
- 100K<n<1M
source_datasets:
- extended|other-Switchboard-1 Telephone Speech Corpus, Release 2
task_categories:
- text-classification
task_ids:
- multi-label-classification
paperswithcode_id: null
---

# Dataset Card for swda

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

- **Homepage: [The Switchboard Dialog Act Corpus](http://compprag.christopherpotts.net/swda.html)**
- **Repository: [NathanDuran/Switchboard-Corpus](https://github.com/cgpotts/swda)**
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
| H-Seq2seq (Colombo et al., 2020) | 85.0 | [Guiding attention in Sequence-to-sequence models for Dialogue Act prediction](https://ojs.aaai.org/index.php/AAAI/article/view/6259/6115)
| SGNN (Ravi et al., 2018) | 83.1 | [Self-Governing Neural Networks for On-Device Short Text Classification](https://www.aclweb.org/anthology/D18-1105.pdf)
| CASA (Raheja et al., 2019) | 82.9 | [Dialogue Act Classification with Context-Aware Self-Attention](https://www.aclweb.org/anthology/N19-1373.pdf)
| DAH-CRF (Li et al., 2019) | 82.3 | [A Dual-Attention Hierarchical Recurrent Neural Network for Dialogue Act Classification](https://www.aclweb.org/anthology/K19-1036.pdf)
| ALDMN (Wan et al., 2018) | 81.5 | [Improved Dynamic Memory Network for Dialogue Act Classification with Adversarial Training](https://arxiv.org/pdf/1811.05021.pdf) 
| CRF-ASN (Chen et al., 2018) | 81.3 | [Dialogue Act Recognition via CRF-Attentive Structured Network](https://arxiv.org/abs/1711.05568)
| Pretrained H-Transformer (Chapuis et al., 2020) |  79.3 | [Hierarchical Pre-training for Sequence Labelling in Spoken Dialog] (https://www.aclweb.org/anthology/2020.findings-emnlp.239)
| Bi-LSTM-CRF (Kumar et al., 2017) | 79.2 | [Dialogue Act Sequence Labeling using Hierarchical encoder with CRF](https://arxiv.org/abs/1709.04250) | [Link](https://github.com/YanWenqiang/HBLSTM-CRF) |
| RNN with 3 utterances in context (Bothe et al., 2018) | 77.34 | [A Context-based Approach for Dialogue Act Recognition using Simple Recurrent Neural Networks](https://arxiv.org/abs/1805.06280) | |

### Languages

The language supported is English.

## Dataset Structure

Utterance are tagged with the [SWBD-DAMSL](https://web.stanford.edu/~jurafsky/ws97/manual.august1.html) DA.

### Data Instances


An example from the dataset is:

`{'act_tag': 115, 'caller': 'A', 'conversation_no': 4325, 'damsl_act_tag': 26, 'from_caller': 1632, 'from_caller_birth_year': 1962, 'from_caller_dialect_area': 'WESTERN', 'from_caller_education': 2, 'from_caller_sex': 'FEMALE', 'length': 5, 'pos': 'Okay/UH ./.', 'prompt': 'FIND OUT WHAT CRITERIA THE OTHER CALLER WOULD USE IN SELECTING CHILD CARE SERVICES FOR A PRESCHOOLER.  IS IT EASY OR DIFFICULT TO FIND SUCH CARE?', 'ptb_basename': '4/sw4325', 'ptb_treenumbers': '1', 'subutterance_index': 1, 'swda_filename': 'sw00utt/sw_0001_4325.utt', 'talk_day': '03/23/1992', 'text': 'Okay.  /', 'to_caller': 1519, 'to_caller_birth_year': 1971, 'to_caller_dialect_area': 'SOUTH MIDLAND', 'to_caller_education': 1, 'to_caller_sex': 'FEMALE', 'topic_description': 'CHILD CARE', 'transcript_index': 0, 'trees': '(INTJ (UH Okay) (. .) (-DFL- E_S))', 'utterance_index': 1}`

### Data Fields

* `swda_filename`:            (str) The filename: directory/basename.
* `ptb_basename`:             (str) The Treebank filename: add ".pos" for POS and ".mrg" for trees
* `conversation_no`:          (int) The conversation Id, to key into the metadata database.
* `transcript_index`:         (int) The line number of this item in the transcript (counting only utt lines).
* `act_tag`:                  (list of str) The Dialog Act Tags (separated by ||| in the file). Check Dialog act annotations for more details.
* `damsl_act_tag`:            (list of str) The Dialog Act Tags of the 217 variation tags.
* `caller`:                   (str) A, B, @A, @B, @@A, @@B
* `utterance_index`:          (int) The encoded index of the utterance (the number in A.49, B.27, etc.)
* `subutterance_index`:       (int) Utterances can be broken across line. This gives the internal position.
* `text`:                     (str) The text of the utterance
* `pos`:                      (str) The POS tagged version of the utterance, from PtbBasename+.pos
* `trees`:                    (str) The tree(s) containing this utterance (separated by ||| in the file). Use `[Tree.fromstring(t) for t in row_value.split("|||")]` to convert to (list of nltk.tree.Tree).
* `ptb_treenumbers`:          (list of int) The tree numbers in the PtbBasename+.mrg
* `talk_day`:                 (str) Date of talk.
* `length`:                   (int) Length of talk in seconds.
* `topic_description`:        (str) Short description of topic that's being discussed.
* `prompt`:                   (str) Long decription/query/instruction.
* `from_caller`:              (int) The numerical Id of the from (A) caller.
* `from_caller_sex`:          (str) MALE, FEMALE.
* `from_caller_education`:    (int) Called education level 0, 1, 2, 3, 9.
* `from_caller_birth_year`:   (int) Caller birth year YYYY.
* `from_caller_dialect_area`: (str) MIXED, NEW ENGLAND, NORTH MIDLAND, NORTHERN, NYC, SOUTH MIDLAND, SOUTHERN, UNK, WESTERN.
* `to_caller`:                (int) The numerical Id of the to (B) caller.
* `to_caller_sex`:            (str) MALE, FEMALE.
* `to_caller_education`:      (int) Called education level 0, 1, 2, 3, 9.
* `to_caller_birth_year`:     (int) Caller birth year YYYY.
* `to_caller_dialect_area`:   (str) MIXED, NEW ENGLAND, NORTH MIDLAND, NORTHERN, NYC, SOUTH MIDLAND, SOUTHERN, UNK, WESTERN.
    

### Dialog act annotations


|         | name                              | act_tag            | example                                              | train_count     | full_count     |
|-----    |-------------------------------    |----------------    |--------------------------------------------------    |-------------    |------------    |
| 1       | Statement-non-opinion             | sd                 | Me, I'm in the legal department.                     | 72824           | 75145          |
| 2       | Acknowledge (Backchannel)         | b                  | Uh-huh.                                              | 37096           | 38298          |
| 3       | Statement-opinion                 | sv                 | I think it's great                                   | 25197           | 26428          |
| 4       | Agree/Accept                      | aa                 | That's exactly it.                                   | 10820           | 11133          |
| 5       | Abandoned or Turn-Exit            | %                  | So, -                                                | 10569           | 15550          |
| 6       | Appreciation                      | ba                 | I can imagine.                                       | 4633            | 4765           |
| 7       | Yes-No-Question                   | qy                 | Do you have to have any special training?            | 4624            | 4727           |
| 8       | Non-verbal                        | x                  | [Laughter], [Throat_clearing]                        | 3548            | 3630           |
| 9       | Yes answers                       | ny                 | Yes.                                                 | 2934            | 3034           |
| 10      | Conventional-closing              | fc                 | Well, it's been nice talking to you.                 | 2486            | 2582           |
| 11      | Uninterpretable                   | %                  | But, uh, yeah                                        | 2158            | 15550          |
| 12      | Wh-Question                       | qw                 | Well, how old are you?                               | 1911            | 1979           |
| 13      | No answers                        | nn                 | No.                                                  | 1340            | 1377           |
| 14      | Response Acknowledgement          | bk                 | Oh, okay.                                            | 1277            | 1306           |
| 15      | Hedge                             | h                  | I don't know if I'm making any sense or not.         | 1182            | 1226           |
| 16      | Declarative Yes-No-Question       | qy^d               | So you can afford to get a house?                    | 1174            | 1219           |
| 17      | Other                             | fo_o_fw_by_bc      | Well give me a break, you know.                      | 1074            | 883            |
| 18      | Backchannel in question form      | bh                 | Is that right?                                       | 1019            | 1053           |
| 19      | Quotation                         | ^q                 | You can't be pregnant and have cats                  | 934             | 983            |
| 20      | Summarize/reformulate             | bf                 | Oh, you mean you switched schools for the kids.      | 919             | 952            |
| 21      | Affirmative non-yes answers       | na                 | It is.                                               | 836             | 847            |
| 22      | Action-directive                  | ad                 | Why don't you go first                               | 719             | 746            |
| 23      | Collaborative Completion          | ^2                 | Who aren't contributing.                             | 699             | 723            |
| 24      | Repeat-phrase                     | b^m                | Oh, fajitas                                          | 660             | 688            |
| 25      | Open-Question                     | qo                 | How about you?                                       | 632             | 656            |
| 26      | Rhetorical-Questions              | qh                 | Who would steal a newspaper?                         | 557             | 575            |
| 27      | Hold before answer/agreement      | ^h                 | I'm drawing a blank.                                 | 540             | 556            |
| 28      | Reject                            | ar                 | Well, no                                             | 338             | 346            |
| 29      | Negative non-no answers           | ng                 | Uh, not a whole lot.                                 | 292             | 302            |
| 30      | Signal-non-understanding          | br                 | Excuse me?                                           | 288             | 298            |
| 31      | Other answers                     | no                 | I don't know                                         | 279             | 286            |
| 32      | Conventional-opening              | fp                 | How are you?                                         | 220             | 225            |
| 33      | Or-Clause                         | qrr                | or is it more of a company?                          | 207             | 209            |
| 34      | Dispreferred answers              | arp_nd             | Well, not so much that.                              | 205             | 207            |
| 35      | 3rd-party-talk                    | t3                 | My goodness, Diane, get down from there.             | 115             | 117            |
| 36      | Offers, Options, Commits          | oo_co_cc           | I'll have to check that out                          | 109             | 110            |
| 37      | Self-talk                         | t1                 | What's the word I'm looking for                      | 102             | 103            |
| 38      | Downplayer                        | bd                 | That's all right.                                    | 100             | 103            |
| 39      | Maybe/Accept-part                 | aap_am             | Something like that                                  | 98              | 105            |
| 40      | Tag-Question                      | ^g                 | Right?                                               | 93              | 92             |
| 41      | Declarative Wh-Question           | qw^d               | You are what kind of buff?                           | 80              | 80             |
| 42      | Apology                           | fa                 | I'm sorry.                                           | 76              | 79             |
| 43      | Thanking                          | ft                 | Hey thanks a lot                                     | 67              | 78             |

### Data Splits

I used info from the [Probabilistic-RNN-DA-Classifier](https://github.com/NathanDuran/Probabilistic-RNN-DA-Classifier) repo:
The same training and test splits as used by [Stolcke et al. (2000)](https://web.stanford.edu/~jurafsky/ws97).
The development set is a subset of the training set to speed up development and testing used in the paper [Probabilistic Word Association for Dialogue Act Classification with Recurrent Neural Networks](https://www.researchgate.net/publication/326640934_Probabilistic_Word_Association_for_Dialogue_Act_Classification_with_Recurrent_Neural_Networks_19th_International_Conference_EANN_2018_Bristol_UK_September_3-5_2018_Proceedings).

|Dataset    |# Transcripts  |# Utterances   |
|-----------|:-------------:|:-------------:|
|Training   |1115           |192,768        |
|Validation |21             |3,196          |
|Test       |19             |4,088          |


## Dataset Creation

### Curation Rationale

[More Information Needed]

### Source Data

#### Initial Data Collection and Normalization

The SwDA is not inherently linked to the Penn Treebank 3 parses of Switchboard, and it is far from straightforward to align the two resources Calhoun et al. 2010, §2.4. In addition, the SwDA is not distributed with the Switchboard's tables of metadata about the conversations and their participants. 

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

### Contributions

Thanks to [@gmihaila](https://github.com/gmihaila) for adding this dataset.
