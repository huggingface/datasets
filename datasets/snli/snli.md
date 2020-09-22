# Dataset Card for SNLI
## Purpose
> What was the original purpose of the dataset / what was the driving need?

The [SNLI corpus (version 1.0)](https://nlp.stanford.edu/projects/snli/) was developed as a benchmark for natural langauge inference (NLI), also known as recognizing textual entailment (RTE), with the goal of producing a dataset large enough to train models using neural methodologies. It contains 570k English sentence pairs, which include a premise, a hypothesis, and a label indicating whether the hypothesis entails the premise, contradicts it, or neither. 

## Languages 
### Per language:
> * BCP-47 code(s)
> * Dialects (e.g. AAVE)

The BCP-47 code for English is en. Dialect information is unknown (see Speaker and Annotator sections for further details).

### Multilingual datasets:
> * info for each represented language, as well as size
> * How was the multi-linguality obtained (parallel text mining? translating from source language?)

The SNLI corpus is not a multilingual dataset.

## Who is/was involved in the dataset use and creation?
### Who are the dataset curators?
> * Paper authors
> * Lab/company short description
> * Funding information (e.g. supporting grants)

The SNLI corpus was developed by Samuel R. Bowman, Gabor Angeli, Christopher Potts, and Christopher D. Manning as part of the [Stanford NLP group](https://nlp.stanford.edu/).

It was supported by a Google Faculty Research Award, a gift from Bloomberg L.P., the Defense Advanced Research Projects Agency (DARPA) Deep Exploration and Filtering of Text (DEFT) Program under Air Force Research Laboratory (AFRL) contract no. FA8750-13-2-0040, the National Science Foundation under grant no. IIS 1159679, and the Department of the Navy, Office of Naval Research, under grant no. N00014-10-1-0109.

### Who are the language producers (who wrote the text / created the base content)?
> * Creator demographics (Wikipedia: Who writes Wikipedia? CNN/DM: US+UK journalists)
> * Creator compensation
> * Who else is represented in the data (e.g. mentioned in the text)

A large portion of the premises (160k) were produced in the [Flickr 30k corpus](http://shannon.cs.illinois.edu/DenotationGraph/) by an unknown number of crowdworkers. About 2,500 crowdworkers from Amazon Mechanical Turk produced the associated hypotheses. The premises from the Flickr 30k project describe people and animals whose photos were collected and presented to the Flickr 30k crowdworkers, but the SNLI corpus did not present the photos to the hypotheses creators. Neither report crowdworker or photo subject demographic information or crowdworker compensation.

An additional 4,000 premises come from the pilot study of the [VisualGenome corpus](https://visualgenome.org/static/paper/Visual_Genome.pdf). Though the pilot study itself is not described, the location information of the 33,000 AMT crowdworkers that participated over the course of the 6 months of data collection are aggregated. Most of the workers were located in the United States (93%), with others from the Philippines, Kenya, India, Russia, and Canada. Workers were paid $6-$8 per hour.

### Who are the annotators?
> * Annotator selection criteria
> * Annotator demographics
> * Annotator compensation

The annotators of the validation task were a closed set of about 30 trusted crowdworkers on Amazon Mechanical Turk. It is unknown if any demographic information was collected or how they were compensated.

## Data characteristics
* domains (e.g. medical)
* produced by humans, automatically generated, generated and human edited, etc.?
* effects of task construction on language use (e.g. “translationese”)
* when was the data produced?

The hypotheses were elicited by presenting crowdworkers with captions from preexisting datasets without the associated photos, but the vocabulary of the hypotheses still reflects the content of the photos as well as the caption style of writing (e.g. mostly present tense). The dataset developers report 37,026 distinct words in the corpus, ignoring case. They allowed bare NPs as well as full sentences. Using the Stanford PCFG Parser 3.5.2 (Klein and Manning, 2003) trained on the standard training set as well as on the Brown Corpus (Francis and Kucera 1979), the authors report that 74% of the premises and 88.9% of the hypotheses result in a parse rooted with an 'S'. The corpus was developed between 2014 and 2015. 

### How was the data collected?
* For web crawlers: time run and domain names
* Criteria for data selection / filtering (include keywords)
* Tools used
* If built on existing datasets, include links to original

Crowdworkers were presented with a caption without the associated photo and asked to produce three alternate captions, one that is definitely true, one that might be true, and one that is definitely false. See Section 2.1 and Figure 1 for details (Bowman et al., 2015).

The corpus includes content from the [Flickr 30k corpus](http://shannon.cs.illinois.edu/DenotationGraph/) and the [VisualGenome corpus](https://visualgenome.org/). The photo captions used to prompt the data creation were collected on Flickr by [Young et al. (2014)](https://www.aclweb.org/anthology/Q14-1006.pdf), who extended the Flickr 8K dataset developed by [Hodosh et al. (2013)](https://www.jair.org/index.php/jair/article/view/10833). Hodosh et al. collected photos from the following Flickr groups: strangers!, Wild-Child (Kids in Action), Dogs in Action (Read the Rules), Outdoor Activities, Action Photography, Flickr-Social (two or more people in the photo). Young et al. do not list the specific groups they collected photos from. The VisualGenome corpus also contains images from Flickr, originally collected in [MS-COCO](https://cocodataset.org/#home) and [YFCC100M](http://projects.dfki.uni-kl.de/yfcc100m/).

### Normalization information
* Pre- and/or post-processing
* Tools used

The premises from the Flickr 30k corpus corrected for spelling using the Linux spell checker and ungrammatical sentences were removed. Bowman et al. do not report any normalization, though they note that punctuation and capitalization are often omitted. 

### Annotation process
* link to guidelines if available, else, description, interannotator agreement and tools used

56,941 of the total sentence pairs were further annotated in a validation task. Four annotators each labeled a premise-hypothesis pair for entailment, contradiction, or neither, resulting in 5 total judgements including the original hypothesis author judgement. See Section 2.2 for more details (Bowman et al., 2015). 

The authors report 3/5 annotator agreement on 98% of the validation set and unanimous annotator agreement on 58.3% of the validation set. If a label was chosen by three annotators, that label was made the gold label. Following from this, 2% of the data did not have a consensus label and was labeled '-' by the authors. 

Label | Fleiss κ
------|---------
_contradiction_ | 0.77
_entailment_ | 0.72
_neutral_ | 0.60
overall | 0.70

## Dataset Structure
> See the [HF documentation](https://huggingface.co/docs/datasets/exploring.html#features-and-columns) for information on features and labels

### Splits, features, and labels
> * provide length statistics per feature
> * for labels, give possible values and describe label type (e.g. sentiment, topic) as well as the proportions of each value. If the value is an integer corresponding to a label category, describe the categories. If scores, say how they are computed / where they come from

The SNLI dataset has 3 splits: _train_, _validation_, and _test_. 
Dataset Split | Number of Instances in Split
--------------|--------------------------------------------
Train | 550,152
Validation | 10,000
Test | 10,000

Each data instance contains the following features: _premise_, _hypothesis_, _label_.

Feature | Mean Token Count
--------|-----------------
Premise | 14.1
Hypothesis | 8.3

The _label_ has 4 possible values, _0_, _1_, _2_, _-_.  which correspond to _entailment_, _neutral_, _contradiction_, and _no label_ respectively. The dataset was developed so that the first three values would be evenly distributed across the splits. See the Annotation Process section for details on _no label_.

### Span indices
> character/word level? Contiguous or not?

No span indices are included in this dataset.

### Example ID
> Does it map to other ID (e.g. across datasets) / have an inherent meaning

The ID is an integer starting from 0. It has no inherent meaning. 

### Free text description for context (e.g. describe difference between title / selftext / body in Reddit data) and example

For each ID, there is a string for the premise, a string for the hypothesis, and an integer for the label. Note that each premise appears three times with a different hypothesis and label. See the [SNLI corpus viewer](https://huggingface.co/nlp/viewer/?dataset=snli) to explore more examples.

ID | Premise | Hypothesis | Label
---|---------|------------|-------
0	| Two women are embracing while holding to go packages.	| The sisters are hugging goodbye while holding to go packages after just eating lunch.	| 1
1	| Two women are embracing while holding to go packages.	| Two woman are holding packages.	| 0
2	| Two women are embracing while holding to go packages.	| The men are fighting outside a deli. | 2

## Tasks supported:
### Task categorization / tags
> * Text to text: Machine translation, Summarization, Abstractive QA, Dialogue / multi-turn text
> * Language modeling
> * Text to structured: Text classification, NER, Extractive QA, Parsing (semantic, syntactic, text-to-SQL)
> * Structured to text: Table-to-text

Text to structured, three-way text classification

### Suggested metrics / models:
> * Per task per predicted feature
> * Give soa / good performing model results (with date)
> * Link to model card?

[SemBERT](https://arxiv.org/pdf/1909.02209.pdf) (Zhousheng Zhang et al, 2019b) is currently listed as SOTA, achieving 91.9% accuracy on the test set. See the [corpus webpage](https://nlp.stanford.edu/projects/snli/) for a list of published results.

## Known Limitations
### Known social biases
> Biases in the community, e.g. [Reddit] (https://yjernite.github.io/lfqa.html#reddit_biases), Wikipedia (see [Table 1](https://arxiv.org/abs/2005.00614))
> Biases in topics covered (e.g. Reddit ELI5/AskHistorians historical figures are mostly US/Western)

The language reflects the content of the photos collected from Flickr, as described in the Data Collection section.

### Other known limitations
> Original NLI: annotation artifacts, predictable from hypothesis only

[Gururangan et al (2018)](https://www.aclweb.org/anthology/N18-2017.pdf) showed that the SNLI corpus had a number of annotation artifacts. Using a simple classifer, they correctly predicted the label of the hypothesis 67% of the time without using the premise.

## Licensing information
The Stanford Natural Language Inference Corpus is licensed under a [Creative Commons Attribution-ShareAlike 4.0 International License](http://creativecommons.org/licenses/by-sa/4.0/).
