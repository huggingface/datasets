---
annotations_creators:
- other
language_creators:
- other
language:
- en
license:
- unknown
multilinguality:
- monolingual
size_categories:
- 10K<n<100K
- 1M<n<10M
source_datasets:
- original
task_categories:
- text-classification
task_ids:
- text-classification-other-discourse-marker-prediction
paperswithcode_id: discovery
pretty_name: Discovery
configs:
- discovery
- discoverysmall
dataset_info:
- config_name: discovery
  features:
  - name: sentence1
    dtype: string
  - name: sentence2
    dtype: string
  - name: label
    dtype:
      class_label:
        names:
          0: '[no-conn]'
          1: absolutely,
          2: accordingly
          3: actually,
          4: additionally
          5: admittedly,
          6: afterward
          7: again,
          8: already,
          9: also,
          10: alternately,
          11: alternatively
          12: although,
          13: altogether,
          14: amazingly,
          15: and
          16: anyway,
          17: apparently,
          18: arguably,
          19: as_a_result,
          20: basically,
          21: because_of_that
          22: because_of_this
          23: besides,
          24: but
          25: by_comparison,
          26: by_contrast,
          27: by_doing_this,
          28: by_then
          29: certainly,
          30: clearly,
          31: coincidentally,
          32: collectively,
          33: consequently
          34: conversely
          35: curiously,
          36: currently,
          37: elsewhere,
          38: especially,
          39: essentially,
          40: eventually,
          41: evidently,
          42: finally,
          43: first,
          44: firstly,
          45: for_example
          46: for_instance
          47: fortunately,
          48: frankly,
          49: frequently,
          50: further,
          51: furthermore
          52: generally,
          53: gradually,
          54: happily,
          55: hence,
          56: here,
          57: historically,
          58: honestly,
          59: hopefully,
          60: however
          61: ideally,
          62: immediately,
          63: importantly,
          64: in_contrast,
          65: in_fact,
          66: in_other_words
          67: in_particular,
          68: in_short,
          69: in_sum,
          70: in_the_end,
          71: in_the_meantime,
          72: in_turn,
          73: incidentally,
          74: increasingly,
          75: indeed,
          76: inevitably,
          77: initially,
          78: instead,
          79: interestingly,
          80: ironically,
          81: lastly,
          82: lately,
          83: later,
          84: likewise,
          85: locally,
          86: luckily,
          87: maybe,
          88: meaning,
          89: meantime,
          90: meanwhile,
          91: moreover
          92: mostly,
          93: namely,
          94: nationally,
          95: naturally,
          96: nevertheless
          97: next,
          98: nonetheless
          99: normally,
          100: notably,
          101: now,
          102: obviously,
          103: occasionally,
          104: oddly,
          105: often,
          106: on_the_contrary,
          107: on_the_other_hand
          108: once,
          109: only,
          110: optionally,
          111: or,
          112: originally,
          113: otherwise,
          114: overall,
          115: particularly,
          116: perhaps,
          117: personally,
          118: plus,
          119: preferably,
          120: presently,
          121: presumably,
          122: previously,
          123: probably,
          124: rather,
          125: realistically,
          126: really,
          127: recently,
          128: regardless,
          129: remarkably,
          130: sadly,
          131: second,
          132: secondly,
          133: separately,
          134: seriously,
          135: significantly,
          136: similarly,
          137: simultaneously
          138: slowly,
          139: so,
          140: sometimes,
          141: soon,
          142: specifically,
          143: still,
          144: strangely,
          145: subsequently,
          146: suddenly,
          147: supposedly,
          148: surely,
          149: surprisingly,
          150: technically,
          151: thankfully,
          152: then,
          153: theoretically,
          154: thereafter,
          155: thereby,
          156: therefore
          157: third,
          158: thirdly,
          159: this,
          160: though,
          161: thus,
          162: together,
          163: traditionally,
          164: truly,
          165: truthfully,
          166: typically,
          167: ultimately,
          168: undoubtedly,
          169: unfortunately,
          170: unsurprisingly,
          171: usually,
          172: well,
          173: yet,
  - name: idx
    dtype: int32
  splits:
  - name: test
    num_bytes: 18615474
    num_examples: 87000
  - name: train
    num_bytes: 334809726
    num_examples: 1566000
  - name: validation
    num_bytes: 18607661
    num_examples: 87000
  download_size: 146233621
  dataset_size: 372032861
- config_name: discoverysmall
  features:
  - name: sentence1
    dtype: string
  - name: sentence2
    dtype: string
  - name: label
    dtype:
      class_label:
        names:
          0: '[no-conn]'
          1: absolutely,
          2: accordingly
          3: actually,
          4: additionally
          5: admittedly,
          6: afterward
          7: again,
          8: already,
          9: also,
          10: alternately,
          11: alternatively
          12: although,
          13: altogether,
          14: amazingly,
          15: and
          16: anyway,
          17: apparently,
          18: arguably,
          19: as_a_result,
          20: basically,
          21: because_of_that
          22: because_of_this
          23: besides,
          24: but
          25: by_comparison,
          26: by_contrast,
          27: by_doing_this,
          28: by_then
          29: certainly,
          30: clearly,
          31: coincidentally,
          32: collectively,
          33: consequently
          34: conversely
          35: curiously,
          36: currently,
          37: elsewhere,
          38: especially,
          39: essentially,
          40: eventually,
          41: evidently,
          42: finally,
          43: first,
          44: firstly,
          45: for_example
          46: for_instance
          47: fortunately,
          48: frankly,
          49: frequently,
          50: further,
          51: furthermore
          52: generally,
          53: gradually,
          54: happily,
          55: hence,
          56: here,
          57: historically,
          58: honestly,
          59: hopefully,
          60: however
          61: ideally,
          62: immediately,
          63: importantly,
          64: in_contrast,
          65: in_fact,
          66: in_other_words
          67: in_particular,
          68: in_short,
          69: in_sum,
          70: in_the_end,
          71: in_the_meantime,
          72: in_turn,
          73: incidentally,
          74: increasingly,
          75: indeed,
          76: inevitably,
          77: initially,
          78: instead,
          79: interestingly,
          80: ironically,
          81: lastly,
          82: lately,
          83: later,
          84: likewise,
          85: locally,
          86: luckily,
          87: maybe,
          88: meaning,
          89: meantime,
          90: meanwhile,
          91: moreover
          92: mostly,
          93: namely,
          94: nationally,
          95: naturally,
          96: nevertheless
          97: next,
          98: nonetheless
          99: normally,
          100: notably,
          101: now,
          102: obviously,
          103: occasionally,
          104: oddly,
          105: often,
          106: on_the_contrary,
          107: on_the_other_hand
          108: once,
          109: only,
          110: optionally,
          111: or,
          112: originally,
          113: otherwise,
          114: overall,
          115: particularly,
          116: perhaps,
          117: personally,
          118: plus,
          119: preferably,
          120: presently,
          121: presumably,
          122: previously,
          123: probably,
          124: rather,
          125: realistically,
          126: really,
          127: recently,
          128: regardless,
          129: remarkably,
          130: sadly,
          131: second,
          132: secondly,
          133: separately,
          134: seriously,
          135: significantly,
          136: similarly,
          137: simultaneously
          138: slowly,
          139: so,
          140: sometimes,
          141: soon,
          142: specifically,
          143: still,
          144: strangely,
          145: subsequently,
          146: suddenly,
          147: supposedly,
          148: surely,
          149: surprisingly,
          150: technically,
          151: thankfully,
          152: then,
          153: theoretically,
          154: thereafter,
          155: thereby,
          156: therefore
          157: third,
          158: thirdly,
          159: this,
          160: though,
          161: thus,
          162: together,
          163: traditionally,
          164: truly,
          165: truthfully,
          166: typically,
          167: ultimately,
          168: undoubtedly,
          169: unfortunately,
          170: unsurprisingly,
          171: usually,
          172: well,
          173: yet,
  - name: idx
    dtype: int32
  splits:
  - name: test
    num_bytes: 187471
    num_examples: 869
  - name: train
    num_bytes: 3355192
    num_examples: 15662
  - name: validation
    num_bytes: 185296
    num_examples: 871
  download_size: 146233621
  dataset_size: 3727959
---


# Dataset Card for Discovery

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

- **Homepage:** https://github.com/synapse-developpement/Discovery
- **Repository:** https://github.com/synapse-developpement/Discovery
- **Paper:** https://www.aclweb.org/anthology/N19-1351/
- **Leaderboard:**
- **Point of Contact:** damien.sileo at kuleuven.be

### Dataset Summary

Discourse marker prediction with 174 markers

### Supported Tasks and Leaderboards

[More Information Needed]

### Languages

English

## Dataset Structure

input : sentence1, sentence2, 
label: marker originally between sentence1 and sentence2

### Data Instances

[More Information Needed]

### Data Fields

[More Information Needed]

### Data Splits

Train/Val/Test

## Dataset Creation

### Curation Rationale

[More Information Needed]

### Source Data

Aranea english web corpus

#### Initial Data Collection and Normalization

[More Information Needed]

#### Who are the source language producers?

[More Information Needed]

### Annotations

Self supervised (see paper)

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

[More Information Needed]

### Citation Information

```
@inproceedings{sileo-etal-2019-mining,
    title = "Mining Discourse Markers for Unsupervised Sentence Representation Learning",
    author = "Sileo, Damien  and
      Van De Cruys, Tim  and
      Pradel, Camille  and
      Muller, Philippe",
    booktitle = "Proceedings of the 2019 Conference of the North {A}merican Chapter of the Association for Computational Linguistics: Human Language Technologies, Volume 1 (Long and Short Papers)",
    month = jun,
    year = "2019",
    address = "Minneapolis, Minnesota",
    publisher = "Association for Computational Linguistics",
    url = "https://www.aclweb.org/anthology/N19-1351",
    pages = "3477--3486",
    abstract = "Current state of the art systems in NLP heavily rely on manually annotated datasets, which are expensive to construct. Very little work adequately exploits unannotated data {--} such as discourse markers between sentences {--} mainly because of data sparseness and ineffective extraction methods. In the present work, we propose a method to automatically discover sentence pairs with relevant discourse markers, and apply it to massive amounts of data. Our resulting dataset contains 174 discourse markers with at least 10k examples each, even for rare markers such as {``}coincidentally{''} or {``}amazingly{''}. We use the resulting data as supervision for learning transferable sentence embeddings. In addition, we show that even though sentence representation learning through prediction of discourse marker yields state of the art results across different transfer tasks, it{'}s not clear that our models made use of the semantic relation between sentences, thus leaving room for further improvements.",
}
```

### Contributions

Thanks to [@sileod](https://github.com/sileod) for adding this dataset.