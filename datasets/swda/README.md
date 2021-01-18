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


An example from the dataset is:

`{'act_tag': 125, 'caller': 'A', 'conversation_no': 3774, 'damsl_act_tag': 4, 'pos': "So/UH I/PRP 've/VBP been/VBN concerned/JJ about/IN crime/NN lately/RB ./.", 'ptb_basename': '3/sw3774', 'ptb_treenumbers': '', 'swda_filename': 'sw10utt/sw_1029_3774.utt', 'text': "{C So } I've been concerned about crime lately. /", 'transcript_index': 0, 'trees': '', 'utterance_index': 1}`


### Data Fields

'swda_filename':       (str) The filename: directory/basename

'ptb_basename':        (str) The Treebank filename: add ".pos" for POS and ".mrg" for trees

'conversation_no':     (int) The conversation Id, to key into the metadata database.

'transcript_index':    (int) The line number of this item in the transcript (counting only utt lines).

'act_tag':             (list of str) The Dialog Act Tags (separated by ||| in the file).

'caller':              (str) A, B, @A, @B, @@A, @@B

'utterance_index':     (int) The encoded index of the utterance (the number in A.49, B.27, etc.)

'subutterance_index':  (int) Utterances can be broken across line. This gives the internal position.

'text':                (str) The text of the utterance

'pos':                 (str) The POS tagged version of the utterance, from PtbBasename+.pos

'trees':               (list of nltk.tree.Tree) The tree(s) containing this utterance (separated by ||| in the file).

'ptb_treenumbers':     (list of int) The tree numbers in the PtbBasename+.mrg
    




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
