# hindi-discourse
A repository for the hindi discourse analysis dataset and its related experiments.

<br>
<p align="center">
  <img src="MIDAS-logo.jpg" alt="MIDAS lab at IIIT-Delhi"  width="60%"/>
  <br>
</p>
<br>

The Hindi Discourse Analysis dataset is a corpus for analyzing discourse modes present in its sentences. It contains sentences from stories written by 11 famous authors from the 20th Century. 4-5 stories by each author have been selected which were available in the public domain resulting in a collection of 53 stories. Most of these short stories were originally written in Hindi but some of them were written in other Indian languages and later translated to Hindi.

The corpus contains a total of 10472 sentences belonging to the following categories:
- Argumentative
- Descriptive
- Dialogic
- Informative
- Narrative

## Dataset Overview

The labeled data could be downloaded from [here](https://github.com/midas-research/hindi-discourse/blob/master/discourse_dataset.json).

The data is shared in a json format. Each entry is a sentence along with it's annotated majority label:

{'Story_no': 15, 'Sentence': ' गाँठ से साढ़े तीन रुपये लग गये, जो अब पेट में जाकर खनकते भी नहीं! जो तेरी करनी मालिक! ” “इसमें मालिक की क्या करनी है? ”', 'Discourse Mode': 'Dialogue'}


#### Distribution of sentences in different discourse modes

<br>
<p align="center">
  <img src="train-test-distribution.png" alt="MIDAS lab at IIIT-Delhi"  width="40%"/>
  <br>
</p>
<br>

#### Inter-annotator agreements each discourse mode and for the entire dataset as measured using Fleiss‘s Kappa

<br>
<p align="center">
  <img src="inter-annotator-score.png" alt="MIDAS lab at IIIT-Delhi"  width="40%"/>
  <br>
</p>
<br>

#### Sample sentences from Hindi Discourse Analysis Dataset for each discourse mode

<br>
<p align="center">
  <img src="discourse-examples.png" alt="MIDAS lab at IIIT-Delhi"  width="70%"/>
  <br>
</p>
<br>

#### Most common stop-words for each discourse mode

<br>
<p align="center">
  <img src="most-common-stopwords.png" alt="MIDAS lab at IIIT-Delhi"  width="40%"/>
  <br>
</p>
<br>

#### Part-of-speech analysis for each discourse mode

Each entry in the table is the average number of words tagged as the column label. ADJ: Adjective, ADP: Adposition, ADV: adverb, AUX: auxiliary, CCONJ: Coordinating Conjunction, DET: Determiner, INTJ: Interjection, NOUN: Noun, NUM: Numeral, PART: Particle, PRON: Pronoun, PROPN: Proper Noun, PUNCT: Punctuation, SCONJ: Subordinating Conjunction, SYM: Symbol, VERB: verb

<br>
<p align="center">
  <img src="pos-analysis.png" alt="MIDAS lab at IIIT-Delhi"  width="80%"/>
  <br>
</p>
<br>

## Terms of Use

1. This corpus can be used freely for research purposes.
2. The paper listed below provide details of the creation and use of the corpus. If you use the corpus, then please cite the     paper.
3. If interested in commercial use of the corpus, send email to midas@iiitd.ac.in.
4. If you use the corpus in a product or application, then please credit the authors and [Multimodal Digital Media Analysis Lab - Indraprastha Institute of Information Technology, New Delhi](http://midas.iiitd.edu.in) appropriately. Also, if you send us an email, we will be thrilled to know about how you have used the corpus.
5. Multimodal Digital Media Analysis Lab - Indraprastha Institute of Information Technology, New Delhi, India disclaims any responsibility for the use of the corpus and does not provide technical support. However, the contact listed above will be happy to respond to queries and clarifications.
6. Rather than redistributing the corpus, please direct interested parties to this [page](https://github.com/midas-research/hindi-discourse)

Please feel free to send us an email:
- with feedback regarding the corpus.
- with information on how you have used the corpus.
- if interested in a collaborative research project.

Copyright (C) 2019 Multimodal Digital Media Analysis Lab - Indraprastha Institute of Information Technology, New Delhi (MIDAS, IIIT-Delhi)

## References
Paper accepted at LREC 2020. Please check back soon.


```

```