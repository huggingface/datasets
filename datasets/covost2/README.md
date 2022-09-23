---
annotations_creators:
- expert-generated
language_creators:
- crowdsourced
- expert-generated
language:
- ar
- ca
- cy
- de
- es
- et
- fa
- fr
- id
- it
- ja
- lv
- mn
- nl
- pt
- ru
- sl
- sv
- ta
- tr
- zh
language_bcp47:
- sv-SE
- zh-CN
license:
- cc-by-nc-4.0
multilinguality:
- multilingual
size_categories:
- 100K<n<1M
source_datasets:
- extended|other-common-voice
task_categories:
- automatic-speech-recognition
task_ids: []
paperswithcode_id: null
pretty_name: CoVoST 2
dataset_info:
- config_name: en_de
  features:
  - name: client_id
    dtype: string
  - name: file
    dtype: string
  - name: sentence
    dtype: string
  - name: translation
    dtype: string
  - name: id
    dtype: string
  splits:
  - name: test
    num_bytes: 5689684
    num_examples: 15531
  - name: train
    num_bytes: 110716293
    num_examples: 289430
  - name: validation
    num_bytes: 5971731
    num_examples: 15531
  download_size: 25779505
  dataset_size: 122377708
- config_name: en_tr
  features:
  - name: client_id
    dtype: string
  - name: file
    dtype: string
  - name: sentence
    dtype: string
  - name: translation
    dtype: string
  - name: id
    dtype: string
  splits:
  - name: test
    num_bytes: 5619271
    num_examples: 15531
  - name: train
    num_bytes: 109474265
    num_examples: 289430
  - name: validation
    num_bytes: 5914622
    num_examples: 15531
  download_size: 23659131
  dataset_size: 121008158
- config_name: en_fa
  features:
  - name: client_id
    dtype: string
  - name: file
    dtype: string
  - name: sentence
    dtype: string
  - name: translation
    dtype: string
  - name: id
    dtype: string
  splits:
  - name: test
    num_bytes: 6103617
    num_examples: 15531
  - name: train
    num_bytes: 119490720
    num_examples: 289430
  - name: validation
    num_bytes: 6423535
    num_examples: 15531
  download_size: 26148420
  dataset_size: 132017872
- config_name: en_sv-SE
  features:
  - name: client_id
    dtype: string
  - name: file
    dtype: string
  - name: sentence
    dtype: string
  - name: translation
    dtype: string
  - name: id
    dtype: string
  splits:
  - name: test
    num_bytes: 5580039
    num_examples: 15531
  - name: train
    num_bytes: 108557530
    num_examples: 289430
  - name: validation
    num_bytes: 5845918
    num_examples: 15531
  download_size: 23671482
  dataset_size: 119983487
- config_name: en_mn
  features:
  - name: client_id
    dtype: string
  - name: file
    dtype: string
  - name: sentence
    dtype: string
  - name: translation
    dtype: string
  - name: id
    dtype: string
  splits:
  - name: test
    num_bytes: 6293633
    num_examples: 15531
  - name: train
    num_bytes: 123950136
    num_examples: 289430
  - name: validation
    num_bytes: 6693044
    num_examples: 15531
  download_size: 27527436
  dataset_size: 136936813
- config_name: en_zh-CN
  features:
  - name: client_id
    dtype: string
  - name: file
    dtype: string
  - name: sentence
    dtype: string
  - name: translation
    dtype: string
  - name: id
    dtype: string
  splits:
  - name: test
    num_bytes: 5487808
    num_examples: 15531
  - name: train
    num_bytes: 106490939
    num_examples: 289430
  - name: validation
    num_bytes: 5735331
    num_examples: 15531
  download_size: 24280932
  dataset_size: 117714078
- config_name: en_cy
  features:
  - name: client_id
    dtype: string
  - name: file
    dtype: string
  - name: sentence
    dtype: string
  - name: translation
    dtype: string
  - name: id
    dtype: string
  splits:
  - name: test
    num_bytes: 5626428
    num_examples: 15531
  - name: train
    num_bytes: 109317182
    num_examples: 289430
  - name: validation
    num_bytes: 5894579
    num_examples: 15531
  download_size: 24224499
  dataset_size: 120838189
- config_name: en_ca
  features:
  - name: client_id
    dtype: string
  - name: file
    dtype: string
  - name: sentence
    dtype: string
  - name: translation
    dtype: string
  - name: id
    dtype: string
  splits:
  - name: test
    num_bytes: 5623227
    num_examples: 15531
  - name: train
    num_bytes: 109922455
    num_examples: 289430
  - name: validation
    num_bytes: 5924345
    num_examples: 15531
  download_size: 24167201
  dataset_size: 121470027
- config_name: en_sl
  features:
  - name: client_id
    dtype: string
  - name: file
    dtype: string
  - name: sentence
    dtype: string
  - name: translation
    dtype: string
  - name: id
    dtype: string
  splits:
  - name: test
    num_bytes: 5537805
    num_examples: 15531
  - name: train
    num_bytes: 107987860
    num_examples: 289430
  - name: validation
    num_bytes: 5838299
    num_examples: 15531
  download_size: 23421999
  dataset_size: 119363964
- config_name: en_et
  features:
  - name: client_id
    dtype: string
  - name: file
    dtype: string
  - name: sentence
    dtype: string
  - name: translation
    dtype: string
  - name: id
    dtype: string
  splits:
  - name: test
    num_bytes: 5543309
    num_examples: 15531
  - name: train
    num_bytes: 107707024
    num_examples: 289430
  - name: validation
    num_bytes: 5810185
    num_examples: 15531
  download_size: 23223843
  dataset_size: 119060518
- config_name: en_id
  features:
  - name: client_id
    dtype: string
  - name: file
    dtype: string
  - name: sentence
    dtype: string
  - name: translation
    dtype: string
  - name: id
    dtype: string
  splits:
  - name: test
    num_bytes: 5634939
    num_examples: 15531
  - name: train
    num_bytes: 109456930
    num_examples: 289430
  - name: validation
    num_bytes: 5896953
    num_examples: 15531
  download_size: 22904065
  dataset_size: 120988822
- config_name: en_ar
  features:
  - name: client_id
    dtype: string
  - name: file
    dtype: string
  - name: sentence
    dtype: string
  - name: translation
    dtype: string
  - name: id
    dtype: string
  splits:
  - name: test
    num_bytes: 5947069
    num_examples: 15531
  - name: train
    num_bytes: 116732296
    num_examples: 289430
  - name: validation
    num_bytes: 6280190
    num_examples: 15531
  download_size: 25301304
  dataset_size: 128959555
- config_name: en_ta
  features:
  - name: client_id
    dtype: string
  - name: file
    dtype: string
  - name: sentence
    dtype: string
  - name: translation
    dtype: string
  - name: id
    dtype: string
  splits:
  - name: test
    num_bytes: 7411400
    num_examples: 15531
  - name: train
    num_bytes: 146318684
    num_examples: 289430
  - name: validation
    num_bytes: 7944020
    num_examples: 15531
  download_size: 30037790
  dataset_size: 161674104
- config_name: en_lv
  features:
  - name: client_id
    dtype: string
  - name: file
    dtype: string
  - name: sentence
    dtype: string
  - name: translation
    dtype: string
  - name: id
    dtype: string
  splits:
  - name: test
    num_bytes: 5625189
    num_examples: 15531
  - name: train
    num_bytes: 109532576
    num_examples: 289430
  - name: validation
    num_bytes: 5905197
    num_examples: 15531
  download_size: 24573927
  dataset_size: 121062962
- config_name: en_ja
  features:
  - name: client_id
    dtype: string
  - name: file
    dtype: string
  - name: sentence
    dtype: string
  - name: translation
    dtype: string
  - name: id
    dtype: string
  splits:
  - name: test
    num_bytes: 5883608
    num_examples: 15531
  - name: train
    num_bytes: 114741253
    num_examples: 289430
  - name: validation
    num_bytes: 6161930
    num_examples: 15531
  download_size: 26664247
  dataset_size: 126786791
- config_name: fr_en
  features:
  - name: client_id
    dtype: string
  - name: file
    dtype: string
  - name: sentence
    dtype: string
  - name: translation
    dtype: string
  - name: id
    dtype: string
  splits:
  - name: test
    num_bytes: 5525498
    num_examples: 14760
  - name: train
    num_bytes: 75792665
    num_examples: 207374
  - name: validation
    num_bytes: 5487082
    num_examples: 14760
  download_size: 7282129
  dataset_size: 86805245
- config_name: de_en
  features:
  - name: client_id
    dtype: string
  - name: file
    dtype: string
  - name: sentence
    dtype: string
  - name: translation
    dtype: string
  - name: id
    dtype: string
  splits:
  - name: test
    num_bytes: 5066500
    num_examples: 13511
  - name: train
    num_bytes: 47678171
    num_examples: 127834
  - name: validation
    num_bytes: 5106253
    num_examples: 13511
  download_size: 9926797
  dataset_size: 57850924
- config_name: es_en
  features:
  - name: client_id
    dtype: string
  - name: file
    dtype: string
  - name: sentence
    dtype: string
  - name: translation
    dtype: string
  - name: id
    dtype: string
  splits:
  - name: test
    num_bytes: 4983920
    num_examples: 13221
  - name: train
    num_bytes: 29152515
    num_examples: 79015
  - name: validation
    num_bytes: 4974593
    num_examples: 13221
  download_size: 3202080
  dataset_size: 39111028
- config_name: ca_en
  features:
  - name: client_id
    dtype: string
  - name: file
    dtype: string
  - name: sentence
    dtype: string
  - name: translation
    dtype: string
  - name: id
    dtype: string
  splits:
  - name: test
    num_bytes: 4804941
    num_examples: 12730
  - name: train
    num_bytes: 35902579
    num_examples: 95854
  - name: validation
    num_bytes: 4798435
    num_examples: 12730
  download_size: 5021926
  dataset_size: 45505955
- config_name: it_en
  features:
  - name: client_id
    dtype: string
  - name: file
    dtype: string
  - name: sentence
    dtype: string
  - name: translation
    dtype: string
  - name: id
    dtype: string
  splits:
  - name: test
    num_bytes: 3412207
    num_examples: 8951
  - name: train
    num_bytes: 11952709
    num_examples: 31698
  - name: validation
    num_bytes: 3393315
    num_examples: 8940
  download_size: 1691247
  dataset_size: 18758231
- config_name: ru_en
  features:
  - name: client_id
    dtype: string
  - name: file
    dtype: string
  - name: sentence
    dtype: string
  - name: translation
    dtype: string
  - name: id
    dtype: string
  splits:
  - name: test
    num_bytes: 2923961
    num_examples: 6300
  - name: train
    num_bytes: 5610194
    num_examples: 12112
  - name: validation
    num_bytes: 2819414
    num_examples: 6110
  download_size: 1443078
  dataset_size: 11353569
- config_name: zh-CN_en
  features:
  - name: client_id
    dtype: string
  - name: file
    dtype: string
  - name: sentence
    dtype: string
  - name: translation
    dtype: string
  - name: id
    dtype: string
  splits:
  - name: test
    num_bytes: 1908633
    num_examples: 4898
  - name: train
    num_bytes: 2791288
    num_examples: 7085
  - name: validation
    num_bytes: 1918796
    num_examples: 4843
  download_size: 587550
  dataset_size: 6618717
- config_name: pt_en
  features:
  - name: client_id
    dtype: string
  - name: file
    dtype: string
  - name: sentence
    dtype: string
  - name: translation
    dtype: string
  - name: id
    dtype: string
  splits:
  - name: test
    num_bytes: 1384251
    num_examples: 4023
  - name: train
    num_bytes: 3095722
    num_examples: 9158
  - name: validation
    num_bytes: 1133404
    num_examples: 3318
  download_size: 476419
  dataset_size: 5613377
- config_name: fa_en
  features:
  - name: client_id
    dtype: string
  - name: file
    dtype: string
  - name: sentence
    dtype: string
  - name: translation
    dtype: string
  - name: id
    dtype: string
  splits:
  - name: test
    num_bytes: 1263271
    num_examples: 3445
  - name: train
    num_bytes: 18015738
    num_examples: 53949
  - name: validation
    num_bytes: 1241531
    num_examples: 3445
  download_size: 3864623
  dataset_size: 20520540
- config_name: et_en
  features:
  - name: client_id
    dtype: string
  - name: file
    dtype: string
  - name: sentence
    dtype: string
  - name: translation
    dtype: string
  - name: id
    dtype: string
  splits:
  - name: test
    num_bytes: 685375
    num_examples: 1571
  - name: train
    num_bytes: 808508
    num_examples: 1782
  - name: validation
    num_bytes: 690694
    num_examples: 1576
  download_size: 246569
  dataset_size: 2184577
- config_name: mn_en
  features:
  - name: client_id
    dtype: string
  - name: file
    dtype: string
  - name: sentence
    dtype: string
  - name: translation
    dtype: string
  - name: id
    dtype: string
  splits:
  - name: test
    num_bytes: 762577
    num_examples: 1759
  - name: train
    num_bytes: 900588
    num_examples: 2067
  - name: validation
    num_bytes: 765543
    num_examples: 1761
  download_size: 189710
  dataset_size: 2428708
- config_name: nl_en
  features:
  - name: client_id
    dtype: string
  - name: file
    dtype: string
  - name: sentence
    dtype: string
  - name: translation
    dtype: string
  - name: id
    dtype: string
  splits:
  - name: test
    num_bytes: 594979
    num_examples: 1699
  - name: train
    num_bytes: 2468140
    num_examples: 7108
  - name: validation
    num_bytes: 594458
    num_examples: 1699
  download_size: 543795
  dataset_size: 3657577
- config_name: tr_en
  features:
  - name: client_id
    dtype: string
  - name: file
    dtype: string
  - name: sentence
    dtype: string
  - name: translation
    dtype: string
  - name: id
    dtype: string
  splits:
  - name: test
    num_bytes: 570760
    num_examples: 1629
  - name: train
    num_bytes: 1391148
    num_examples: 3966
  - name: validation
    num_bytes: 566458
    num_examples: 1624
  download_size: 280904
  dataset_size: 2528366
- config_name: ar_en
  features:
  - name: client_id
    dtype: string
  - name: file
    dtype: string
  - name: sentence
    dtype: string
  - name: translation
    dtype: string
  - name: id
    dtype: string
  splits:
  - name: test
    num_bytes: 552356
    num_examples: 1695
  - name: train
    num_bytes: 743065
    num_examples: 2283
  - name: validation
    num_bytes: 575077
    num_examples: 1758
  download_size: 109802
  dataset_size: 1870498
- config_name: sv-SE_en
  features:
  - name: client_id
    dtype: string
  - name: file
    dtype: string
  - name: sentence
    dtype: string
  - name: translation
    dtype: string
  - name: id
    dtype: string
  splits:
  - name: test
    num_bytes: 517738
    num_examples: 1595
  - name: train
    num_bytes: 698800
    num_examples: 2160
  - name: validation
    num_bytes: 438319
    num_examples: 1349
  download_size: 96161
  dataset_size: 1654857
- config_name: lv_en
  features:
  - name: client_id
    dtype: string
  - name: file
    dtype: string
  - name: sentence
    dtype: string
  - name: translation
    dtype: string
  - name: id
    dtype: string
  splits:
  - name: test
    num_bytes: 519183
    num_examples: 1629
  - name: train
    num_bytes: 747290
    num_examples: 2337
  - name: validation
    num_bytes: 360941
    num_examples: 1125
  download_size: 88836
  dataset_size: 1627414
- config_name: sl_en
  features:
  - name: client_id
    dtype: string
  - name: file
    dtype: string
  - name: sentence
    dtype: string
  - name: translation
    dtype: string
  - name: id
    dtype: string
  splits:
  - name: test
    num_bytes: 115414
    num_examples: 360
  - name: train
    num_bytes: 602420
    num_examples: 1843
  - name: validation
    num_bytes: 165977
    num_examples: 509
  download_size: 58445
  dataset_size: 883811
- config_name: ta_en
  features:
  - name: client_id
    dtype: string
  - name: file
    dtype: string
  - name: sentence
    dtype: string
  - name: translation
    dtype: string
  - name: id
    dtype: string
  splits:
  - name: test
    num_bytes: 303843
    num_examples: 786
  - name: train
    num_bytes: 534564
    num_examples: 1358
  - name: validation
    num_bytes: 150428
    num_examples: 384
  download_size: 55659
  dataset_size: 988835
- config_name: ja_en
  features:
  - name: client_id
    dtype: string
  - name: file
    dtype: string
  - name: sentence
    dtype: string
  - name: translation
    dtype: string
  - name: id
    dtype: string
  splits:
  - name: test
    num_bytes: 241310
    num_examples: 684
  - name: train
    num_bytes: 396334
    num_examples: 1119
  - name: validation
    num_bytes: 226054
    num_examples: 635
  download_size: 54666
  dataset_size: 863698
- config_name: id_en
  features:
  - name: client_id
    dtype: string
  - name: file
    dtype: string
  - name: sentence
    dtype: string
  - name: translation
    dtype: string
  - name: id
    dtype: string
  splits:
  - name: test
    num_bytes: 277053
    num_examples: 844
  - name: train
    num_bytes: 406989
    num_examples: 1243
  - name: validation
    num_bytes: 259134
    num_examples: 792
  download_size: 51755
  dataset_size: 943176
- config_name: cy_en
  features:
  - name: client_id
    dtype: string
  - name: file
    dtype: string
  - name: sentence
    dtype: string
  - name: translation
    dtype: string
  - name: id
    dtype: string
  splits:
  - name: test
    num_bytes: 236713
    num_examples: 690
  - name: train
    num_bytes: 432071
    num_examples: 1241
  - name: validation
    num_bytes: 236107
    num_examples: 690
  download_size: 875557
  dataset_size: 904891
---

# Dataset Card for covost2

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

- **Homepage:** https://github.com/facebookresearch/covost
- **Repository:** https://github.com/facebookresearch/covost
- **Paper:** https://arxiv.org/abs/2007.10310
- **Leaderboard:** [Needs More Information]
- **Point of Contact:** Changhan Wang (changhan@fb.com), Juan Miguel Pino (juancarabina@fb.com), Jiatao Gu (jgu@fb.com)

### Dataset Summary

CoVoST 2 is a large-scale multilingual speech translation corpus covering translations from 21 languages into English \
and from English into 15 languages. The dataset is created using Mozillas open-source Common Voice database of \
crowdsourced voice recordings. There are 2,900 hours of speech represented in the corpus.

### Supported Tasks and Leaderboards

`speech-translation`: The dataset can be used for Speech-to-text translation (ST). The model is presented with an audio file in one language and asked to transcribe the audio file to written text in another language. The most common evaluation metric is the BLEU score. Examples can be found at https://github.com/pytorch/fairseq/blob/master/examples/speech_to_text/docs/covost_example.md .

### Languages

The dataset contains the audio, transcriptions, and translations in the following languages, French, German, Dutch, Russian, Spanish, Italian, Turkish, Persian, Swedish, Mongolian, Chinese, Welsh, Catalan, Slovenian, Estonian, Indonesian, Arabic, Tamil, Portuguese, Latvian, and Japanese. 

## Dataset Structure

### Data Instances

A typical data point comprises the path to the audio file, usually called `file`, its transcription, called `sentence`, and the translation in target language called `translation`.

```
{'client_id': 'd277a1f3904ae00b09b73122b87674e7c2c78e08120721f37b5577013ead08d1ea0c053ca5b5c2fb948df2c81f27179aef2c741057a17249205d251a8fe0e658',
 'file': '/home/suraj/projects/fairseq_s2t/covst/dataset/en/clips/common_voice_en_18540003.mp3',
 'audio': {'path': '/home/suraj/projects/fairseq_s2t/covst/dataset/en/clips/common_voice_en_18540003.mp3',
		   'array': array([-0.00048828, -0.00018311, -0.00137329, ...,  0.00079346, 0.00091553,  0.00085449], dtype=float32),
		   'sampling_rate': 48000},
 'id': 'common_voice_en_18540003',
 'sentence': 'When water is scarce, avoid wasting it.',
 'translation': 'Wenn Wasser knapp ist, verschwenden Sie es nicht.'}
```

### Data Fields

- file: A path to the downloaded audio file in .mp3 format.

- audio: A dictionary containing the path to the downloaded audio file, the decoded audio array, and the sampling rate. Note that when accessing the audio column: `dataset[0]["audio"]` the audio file is automatically decoded and resampled to `dataset.features["audio"].sampling_rate`. Decoding and resampling of a large number of audio files might take a significant amount of time. Thus it is important to first query the sample index before the `"audio"` column, *i.e.* `dataset[0]["audio"]` should **always** be preferred over `dataset["audio"][0]`.

- sentence: The transcription of the audio file in source language.

- translation: The transcription of the audio file in the target language. 

- id: unique id of the data sample.

### Data Splits

| config   | train  | validation | test  |
|----------|--------|------------|-------|
| en_de    | 289430 | 15531      | 15531 |
| en_tr    | 289430 | 15531      | 15531 |
| en_fa    | 289430 | 15531      | 15531 |
| en_sv-SE | 289430 | 15531      | 15531 |
| en_mn    | 289430 | 15531      | 15531 |
| en_zh-CN | 289430 | 15531      | 15531 |
| en_cy    | 289430 | 15531      | 15531 |
| en_ca    | 289430 | 15531      | 15531 |
| en_sl    | 289430 | 15531      | 15531 |
| en_et    | 289430 | 15531      | 15531 |
| en_id    | 289430 | 15531      | 15531 |
| en_ar    | 289430 | 15531      | 15531 |
| en_ta    | 289430 | 15531      | 15531 |
| en_lv    | 289430 | 15531      | 15531 |
| en_ja    | 289430 | 15531      | 15531 |
| fr_en    | 207374 | 14760      | 14760 |
| de_en    | 127834 | 13511      | 13511 |
| es_en    | 79015  | 13221      | 13221 |
| ca_en    | 95854  | 12730      | 12730 |
| it_en    | 31698  | 8940       | 8951  |
| ru_en    | 12112  | 6110       | 6300  |
| zh-CN_en | 7085   | 4843       | 4898  |
| pt_en    | 9158   | 3318       | 4023  |
| fa_en    | 53949  | 3445       | 3445  |
| et_en    | 1782   | 1576       | 1571  |
| mn_en    | 2067   | 1761       | 1759  |
| nl_en    | 7108   | 1699       | 1699  |
| tr_en    | 3966   | 1624       | 1629  |
| ar_en    | 2283   | 1758       | 1695  |
| sv-SE_en | 2160   | 1349       | 1595  |
| lv_en    | 2337   | 1125       | 1629  |
| sl_en    | 1843   | 509        | 360   |
| ta_en    | 1358   | 384        | 786   |
| ja_en    | 1119   | 635        | 684   |
| id_en    | 1243   | 792        | 844   |
| cy_en    | 1241   | 690        | 690   |


## Dataset Creation

### Curation Rationale

[Needs More Information]

### Source Data

#### Initial Data Collection and Normalization

[Needs More Information]

#### Who are the source language producers?

[Needs More Information]

### Annotations

#### Annotation process

[Needs More Information]

#### Who are the annotators?

[Needs More Information]

### Personal and Sensitive Information

The dataset consists of people who have donated their voice online. You agree to not attempt to determine the identity of speakers in this dataset.

## Considerations for Using the Data

### Social Impact of Dataset

[Needs More Information]

### Discussion of Biases

[Needs More Information]

### Other Known Limitations

[Needs More Information]

## Additional Information

### Dataset Curators

[Needs More Information]

### Licensing Information

[CC BY-NC 4.0](https://github.com/facebookresearch/covost/blob/main/LICENSE)

### Citation Information

```
@misc{wang2020covost,
    title={CoVoST 2: A Massively Multilingual Speech-to-Text Translation Corpus},
    author={Changhan Wang and Anne Wu and Juan Pino},
    year={2020},
    eprint={2007.10310},
    archivePrefix={arXiv},
    primaryClass={cs.CL}
```

### Contributions

Thanks to [@patil-suraj](https://github.com/patil-suraj) for adding this dataset.