---
annotations_creators:
- expert-generated
language_creators:
- crowdsourced
- machine-generated
languages:
- en
- hi
licenses:
- cc-by-nc-sa-3.0
multilinguality:
- translation
size_categories:
- 100K<n<1M
source_datasets:
- original
task_categories:
- conditional-text-generation
task_ids:
- machine-translation
paperswithcode_id: hindencorp
---

# Dataset Card for HindEnCorp

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

- **Homepage:https://lindat.mff.cuni.cz/repository/xmlui/handle/11858/00-097C-0000-0023-625F-0**
- **Repository:https://lindat.mff.cuni.cz/repository/xmlui/**
- **Paper:http://www.lrec-conf.org/proceedings/lrec2014/pdf/835_Paper.pdf**
- **Leaderboard:**
- **Point of Contact:**

### Dataset Summary

HindEnCorp parallel texts (sentence-aligned) come from the following sources:
Tides, which contains 50K sentence pairs taken mainly from news articles. This dataset was originally col- lected for the DARPA-TIDES surprise-language con- test in 2002, later refined at IIIT Hyderabad and provided for the NLP Tools Contest at ICON 2008 (Venkatapathy, 2008).

Commentaries by Daniel Pipes contain 322 articles in English written by a journalist Daniel Pipes and translated into Hindi.

EMILLE. This corpus (Baker et al., 2002) consists of three components: monolingual, parallel and annotated corpora. There are fourteen monolingual sub- corpora, including both written and (for some lan- guages) spoken data for fourteen South Asian lan- guages. The EMILLE monolingual corpora contain in total 92,799,000 words (including 2,627,000 words of transcribed spoken data for Bengali, Gujarati, Hindi, Punjabi and Urdu). The parallel corpus consists of 200,000 words of text in English and its accompanying translations into Hindi and other languages.

Smaller datasets as collected by Bojar et al. (2010) include the corpus used at ACL 2005 (a subcorpus of EMILLE), a corpus of named entities from Wikipedia (crawled in 2009), and Agriculture domain parallel corpus.
￼
For the current release, we are extending the parallel corpus using these sources:
Intercorp (Čermák and Rosen,2012) is a large multilingual parallel corpus of 32 languages including Hindi. The central language used for alignment is Czech. Intercorp’s core texts amount to 202 million words. These core texts are most suitable for us because their sentence alignment is manually checked and therefore very reliable. They cover predominately short sto- ries and novels. There are seven Hindi texts in Inter- corp. Unfortunately, only for three of them the English translation is available; the other four are aligned only with Czech texts. The Hindi subcorpus of Intercorp contains 118,000 words in Hindi.

TED talks 3 held in various languages, primarily English, are equipped with transcripts and these are translated into 102 languages. There are 179 talks for which Hindi translation is available.

The Indic multi-parallel corpus (Birch et al., 2011; Post et al., 2012) is a corpus of texts from Wikipedia translated from the respective Indian language into English by non-expert translators hired over Mechanical Turk. The quality is thus somewhat mixed in many respects starting from typesetting and punctuation over capi- talization, spelling, word choice to sentence structure. A little bit of control could be in principle obtained from the fact that every input sentence was translated 4 times. We used the 2012 release of the corpus.

Launchpad.net is a software collaboration platform that hosts many open-source projects and facilitates also collaborative localization of the tools. We downloaded all revisions of all the hosted projects and extracted the localization (.po) files.

Other smaller datasets. This time, we added Wikipedia entities as crawled in 2013 (including any morphological variants of the named entitity that appears on the Hindi variant of the Wikipedia page) and words, word examples and quotes from the Shabdkosh online dictionary.

### Supported Tasks and Leaderboards

[More Information Needed]

### Languages

Hindi, English

## Dataset Structure

### Data Instances

[More Information Needed]

### Data Fields

HindEncorp Columns:

- source identifier (where do the segments come from)
- alignment type (number of English segments - number of Hindi segments)
- alignment quality, which is one of the following:
    "manual"  ... for sources that were sentence-aligned manually
    "implied" ... for sources where one side was constructed by translating
                  segment by segment
    float     ... a value somehow reflecting the goodness of the automatic
                  alignment; not really reliable
- English segment or segments
- Hindi segment or segments

Each of the segments field is in the plaintext or export format as described
above.

If there are more than one segments on a line (e.g. for lines with alignment
type 2-1 where there are two English segments), then the segments are delimited
with `<s>` in the text field.

### Data Splits

[More Information Needed]

## Dataset Creation

### Source Data

[More Information Needed]

#### Initial Data Collection and Normalization

[More Information Needed]

#### Who are the source language producers?

Daniel Pipes,Baker,Bojar,"Čermák and Rosen,2012","Birch et al., 2011; Post et al., 2012"

### Annotations

#### Annotation process

the 1st part of data TIDES was originally col- lected for the DARPA-TIDES surprise-language con- test in 2002, later refined at IIIT Hyderabad and provided for the NLP Tools Contest at ICON 2008 (Venkatapathy, 2008).
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

Bojar, Ondřej ; Diatka, Vojtěch ; Straňák, Pavel ; Tamchyna, Aleš ; Zeman, Daniel 

### Licensing Information

CC BY-NC-SA 3.0

### Citation Information

@InProceedings{hindencorp05:lrec:2014,
  author = {Ond{\v{r}}ej Bojar and Vojt{\v{e}}ch Diatka
            and Pavel Rychl{\'{y}} and Pavel Stra{\v{n}}{\'{a}}k
            and V{\'{\i}}t Suchomel and Ale{\v{s}} Tamchyna and Daniel Zeman},
  title = "{HindEnCorp - Hindi-English and Hindi-only Corpus for Machine
            Translation}",
  booktitle = {Proceedings of the Ninth International Conference on Language
               Resources and Evaluation (LREC'14)},
  year = {2014},
  month = {may},
  date = {26-31},
  address = {Reykjavik, Iceland},
  editor = {Nicoletta Calzolari (Conference Chair) and Khalid Choukri and
     Thierry Declerck and Hrafn Loftsson and Bente Maegaard and Joseph Mariani
     and Asuncion Moreno and Jan Odijk and Stelios Piperidis},
  publisher = {European Language Resources Association (ELRA)},
  isbn = {978-2-9517408-8-4},
  language = {english}
}


### Contributions

Thanks to [@rahul-art](https://github.com/rahul-art) for adding this dataset.