---
pretty_name: Multi-Dimensional Gender Bias Classification
annotations_creators:
- crowdsourced
- found
- machine-generated
language_creators:
- crowdsourced
- found
language:
- en
license:
- mit
multilinguality:
- monolingual
size_categories:
- 100K<n<1M
- 10K<n<100K
- 1K<n<10K
- 1M<n<10M
- n<1K
source_datasets:
- extended|other-convai2
- extended|other-light
- extended|other-opensubtitles
- extended|other-yelp
- original
task_categories:
- text-classification
task_ids:
- text-classification-other-gender-bias
paperswithcode_id: md-gender
configs:
- convai2_inferred
- funpedia
- gendered_words
- image_chat
- light_inferred
- name_genders
- new_data
- opensubtitles_inferred
- wizard
- yelp_inferred
dataset_info:
- config_name: gendered_words
  features:
  - name: word_masculine
    dtype: string
  - name: word_feminine
    dtype: string
  splits:
  - name: train
    num_bytes: 4988
    num_examples: 222
  download_size: 232629010
  dataset_size: 4988
- config_name: name_genders
  features:
  - name: name
    dtype: string
  - name: assigned_gender
    dtype:
      class_label:
        names:
          0: M
          1: F
  - name: count
    dtype: int32
  splits:
  - name: yob1880
    num_bytes: 43404
    num_examples: 2000
  - name: yob1881
    num_bytes: 41944
    num_examples: 1935
  - name: yob1882
    num_bytes: 46211
    num_examples: 2127
  - name: yob1883
    num_bytes: 45221
    num_examples: 2084
  - name: yob1884
    num_bytes: 49886
    num_examples: 2297
  - name: yob1885
    num_bytes: 49810
    num_examples: 2294
  - name: yob1886
    num_bytes: 51935
    num_examples: 2392
  - name: yob1887
    num_bytes: 51458
    num_examples: 2373
  - name: yob1888
    num_bytes: 57531
    num_examples: 2651
  - name: yob1889
    num_bytes: 56177
    num_examples: 2590
  - name: yob1890
    num_bytes: 58509
    num_examples: 2695
  - name: yob1891
    num_bytes: 57767
    num_examples: 2660
  - name: yob1892
    num_bytes: 63493
    num_examples: 2921
  - name: yob1893
    num_bytes: 61525
    num_examples: 2831
  - name: yob1894
    num_bytes: 63927
    num_examples: 2941
  - name: yob1895
    num_bytes: 66346
    num_examples: 3049
  - name: yob1896
    num_bytes: 67224
    num_examples: 3091
  - name: yob1897
    num_bytes: 65886
    num_examples: 3028
  - name: yob1898
    num_bytes: 71088
    num_examples: 3264
  - name: yob1899
    num_bytes: 66225
    num_examples: 3042
  - name: yob1900
    num_bytes: 81305
    num_examples: 3730
  - name: yob1901
    num_bytes: 68723
    num_examples: 3153
  - name: yob1902
    num_bytes: 73321
    num_examples: 3362
  - name: yob1903
    num_bytes: 74019
    num_examples: 3389
  - name: yob1904
    num_bytes: 77751
    num_examples: 3560
  - name: yob1905
    num_bytes: 79802
    num_examples: 3655
  - name: yob1906
    num_bytes: 79392
    num_examples: 3633
  - name: yob1907
    num_bytes: 86342
    num_examples: 3948
  - name: yob1908
    num_bytes: 87965
    num_examples: 4018
  - name: yob1909
    num_bytes: 92591
    num_examples: 4227
  - name: yob1910
    num_bytes: 101491
    num_examples: 4629
  - name: yob1911
    num_bytes: 106787
    num_examples: 4867
  - name: yob1912
    num_bytes: 139448
    num_examples: 6351
  - name: yob1913
    num_bytes: 153110
    num_examples: 6968
  - name: yob1914
    num_bytes: 175167
    num_examples: 7965
  - name: yob1915
    num_bytes: 205921
    num_examples: 9357
  - name: yob1916
    num_bytes: 213468
    num_examples: 9696
  - name: yob1917
    num_bytes: 218446
    num_examples: 9913
  - name: yob1918
    num_bytes: 229209
    num_examples: 10398
  - name: yob1919
    num_bytes: 228656
    num_examples: 10369
  - name: yob1920
    num_bytes: 237286
    num_examples: 10756
  - name: yob1921
    num_bytes: 239616
    num_examples: 10857
  - name: yob1922
    num_bytes: 237569
    num_examples: 10756
  - name: yob1923
    num_bytes: 235046
    num_examples: 10643
  - name: yob1924
    num_bytes: 240113
    num_examples: 10869
  - name: yob1925
    num_bytes: 235098
    num_examples: 10638
  - name: yob1926
    num_bytes: 230970
    num_examples: 10458
  - name: yob1927
    num_bytes: 230004
    num_examples: 10406
  - name: yob1928
    num_bytes: 224583
    num_examples: 10159
  - name: yob1929
    num_bytes: 217057
    num_examples: 9820
  - name: yob1930
    num_bytes: 216352
    num_examples: 9791
  - name: yob1931
    num_bytes: 205361
    num_examples: 9298
  - name: yob1932
    num_bytes: 207268
    num_examples: 9381
  - name: yob1933
    num_bytes: 199031
    num_examples: 9013
  - name: yob1934
    num_bytes: 202758
    num_examples: 9180
  - name: yob1935
    num_bytes: 199614
    num_examples: 9037
  - name: yob1936
    num_bytes: 196379
    num_examples: 8894
  - name: yob1937
    num_bytes: 197757
    num_examples: 8946
  - name: yob1938
    num_bytes: 199603
    num_examples: 9032
  - name: yob1939
    num_bytes: 196979
    num_examples: 8918
  - name: yob1940
    num_bytes: 198141
    num_examples: 8961
  - name: yob1941
    num_bytes: 200858
    num_examples: 9085
  - name: yob1942
    num_bytes: 208363
    num_examples: 9425
  - name: yob1943
    num_bytes: 207940
    num_examples: 9408
  - name: yob1944
    num_bytes: 202227
    num_examples: 9152
  - name: yob1945
    num_bytes: 199478
    num_examples: 9025
  - name: yob1946
    num_bytes: 214614
    num_examples: 9705
  - name: yob1947
    num_bytes: 229327
    num_examples: 10371
  - name: yob1948
    num_bytes: 226615
    num_examples: 10241
  - name: yob1949
    num_bytes: 227278
    num_examples: 10269
  - name: yob1950
    num_bytes: 227946
    num_examples: 10303
  - name: yob1951
    num_bytes: 231613
    num_examples: 10462
  - name: yob1952
    num_bytes: 235483
    num_examples: 10646
  - name: yob1953
    num_bytes: 239654
    num_examples: 10837
  - name: yob1954
    num_bytes: 242389
    num_examples: 10968
  - name: yob1955
    num_bytes: 245652
    num_examples: 11115
  - name: yob1956
    num_bytes: 250674
    num_examples: 11340
  - name: yob1957
    num_bytes: 255370
    num_examples: 11564
  - name: yob1958
    num_bytes: 254520
    num_examples: 11522
  - name: yob1959
    num_bytes: 260051
    num_examples: 11767
  - name: yob1960
    num_bytes: 263474
    num_examples: 11921
  - name: yob1961
    num_bytes: 269493
    num_examples: 12182
  - name: yob1962
    num_bytes: 270244
    num_examples: 12209
  - name: yob1963
    num_bytes: 271872
    num_examples: 12282
  - name: yob1964
    num_bytes: 274590
    num_examples: 12397
  - name: yob1965
    num_bytes: 264889
    num_examples: 11952
  - name: yob1966
    num_bytes: 269321
    num_examples: 12151
  - name: yob1967
    num_bytes: 274867
    num_examples: 12397
  - name: yob1968
    num_bytes: 286774
    num_examples: 12936
  - name: yob1969
    num_bytes: 304909
    num_examples: 13749
  - name: yob1970
    num_bytes: 328047
    num_examples: 14779
  - name: yob1971
    num_bytes: 339657
    num_examples: 15295
  - name: yob1972
    num_bytes: 342321
    num_examples: 15412
  - name: yob1973
    num_bytes: 348414
    num_examples: 15682
  - name: yob1974
    num_bytes: 361188
    num_examples: 16249
  - name: yob1975
    num_bytes: 376491
    num_examples: 16944
  - name: yob1976
    num_bytes: 386565
    num_examples: 17391
  - name: yob1977
    num_bytes: 403994
    num_examples: 18175
  - name: yob1978
    num_bytes: 405430
    num_examples: 18231
  - name: yob1979
    num_bytes: 423423
    num_examples: 19039
  - name: yob1980
    num_bytes: 432317
    num_examples: 19452
  - name: yob1981
    num_bytes: 432980
    num_examples: 19475
  - name: yob1982
    num_bytes: 437986
    num_examples: 19694
  - name: yob1983
    num_bytes: 431531
    num_examples: 19407
  - name: yob1984
    num_bytes: 434085
    num_examples: 19506
  - name: yob1985
    num_bytes: 447113
    num_examples: 20085
  - name: yob1986
    num_bytes: 460315
    num_examples: 20657
  - name: yob1987
    num_bytes: 477677
    num_examples: 21406
  - name: yob1988
    num_bytes: 499347
    num_examples: 22367
  - name: yob1989
    num_bytes: 531020
    num_examples: 23775
  - name: yob1990
    num_bytes: 552114
    num_examples: 24716
  - name: yob1991
    num_bytes: 560932
    num_examples: 25109
  - name: yob1992
    num_bytes: 568151
    num_examples: 25427
  - name: yob1993
    num_bytes: 579778
    num_examples: 25966
  - name: yob1994
    num_bytes: 580223
    num_examples: 25997
  - name: yob1995
    num_bytes: 581949
    num_examples: 26080
  - name: yob1996
    num_bytes: 589131
    num_examples: 26423
  - name: yob1997
    num_bytes: 601284
    num_examples: 26970
  - name: yob1998
    num_bytes: 621587
    num_examples: 27902
  - name: yob1999
    num_bytes: 635355
    num_examples: 28552
  - name: yob2000
    num_bytes: 662398
    num_examples: 29772
  - name: yob2001
    num_bytes: 673111
    num_examples: 30274
  - name: yob2002
    num_bytes: 679392
    num_examples: 30564
  - name: yob2003
    num_bytes: 692931
    num_examples: 31185
  - name: yob2004
    num_bytes: 711776
    num_examples: 32048
  - name: yob2005
    num_bytes: 723065
    num_examples: 32549
  - name: yob2006
    num_bytes: 757620
    num_examples: 34088
  - name: yob2007
    num_bytes: 776893
    num_examples: 34961
  - name: yob2008
    num_bytes: 779403
    num_examples: 35079
  - name: yob2009
    num_bytes: 771032
    num_examples: 34709
  - name: yob2010
    num_bytes: 756717
    num_examples: 34073
  - name: yob2011
    num_bytes: 752804
    num_examples: 33908
  - name: yob2012
    num_bytes: 748915
    num_examples: 33747
  - name: yob2013
    num_bytes: 738288
    num_examples: 33282
  - name: yob2014
    num_bytes: 737219
    num_examples: 33243
  - name: yob2015
    num_bytes: 734183
    num_examples: 33121
  - name: yob2016
    num_bytes: 731291
    num_examples: 33010
  - name: yob2017
    num_bytes: 721444
    num_examples: 32590
  - name: yob2018
    num_bytes: 708657
    num_examples: 32033
  download_size: 232629010
  dataset_size: 43393095
- config_name: new_data
  features:
  - name: text
    dtype: string
  - name: original
    dtype: string
  - name: labels
    list:
      class_label:
        names:
          0: ABOUT:female
          1: ABOUT:male
          2: PARTNER:female
          3: PARTNER:male
          4: SELF:female
          5: SELF:male
  - name: class_type
    dtype:
      class_label:
        names:
          0: about
          1: partner
          2: self
  - name: turker_gender
    dtype:
      class_label:
        names:
          0: man
          1: woman
          2: nonbinary
          3: prefer not to say
          4: no answer
  - name: episode_done
    dtype: bool_
  - name: confidence
    dtype: string
  splits:
  - name: train
    num_bytes: 369753
    num_examples: 2345
  download_size: 232629010
  dataset_size: 369753
- config_name: funpedia
  features:
  - name: text
    dtype: string
  - name: title
    dtype: string
  - name: persona
    dtype: string
  - name: gender
    dtype:
      class_label:
        names:
          0: gender-neutral
          1: female
          2: male
  splits:
  - name: test
    num_bytes: 396417
    num_examples: 2938
  - name: train
    num_bytes: 3225542
    num_examples: 23897
  - name: validation
    num_bytes: 402205
    num_examples: 2984
  download_size: 232629010
  dataset_size: 4024164
- config_name: image_chat
  features:
  - name: caption
    dtype: string
  - name: id
    dtype: string
  - name: male
    dtype: bool_
  - name: female
    dtype: bool_
  splits:
  - name: test
    num_bytes: 530126
    num_examples: 5000
  - name: train
    num_bytes: 1061285
    num_examples: 9997
  - name: validation
    num_bytes: 35868670
    num_examples: 338180
  download_size: 232629010
  dataset_size: 37460081
- config_name: wizard
  features:
  - name: text
    dtype: string
  - name: chosen_topic
    dtype: string
  - name: gender
    dtype:
      class_label:
        names:
          0: gender-neutral
          1: female
          2: male
  splits:
  - name: test
    num_bytes: 53126
    num_examples: 470
  - name: train
    num_bytes: 1158785
    num_examples: 10449
  - name: validation
    num_bytes: 57824
    num_examples: 537
  download_size: 232629010
  dataset_size: 1269735
- config_name: convai2_inferred
  features:
  - name: text
    dtype: string
  - name: binary_label
    dtype:
      class_label:
        names:
          0: ABOUT:female
          1: ABOUT:male
  - name: binary_score
    dtype: float32
  - name: ternary_label
    dtype:
      class_label:
        names:
          0: ABOUT:female
          1: ABOUT:male
          2: ABOUT:gender-neutral
  - name: ternary_score
    dtype: float32
  splits:
  - name: test
    num_bytes: 608046
    num_examples: 7801
  - name: train
    num_bytes: 9853669
    num_examples: 131438
  - name: validation
    num_bytes: 608046
    num_examples: 7801
  download_size: 232629010
  dataset_size: 11069761
- config_name: light_inferred
  features:
  - name: text
    dtype: string
  - name: binary_label
    dtype:
      class_label:
        names:
          0: ABOUT:female
          1: ABOUT:male
  - name: binary_score
    dtype: float32
  - name: ternary_label
    dtype:
      class_label:
        names:
          0: ABOUT:female
          1: ABOUT:male
          2: ABOUT:gender-neutral
  - name: ternary_score
    dtype: float32
  splits:
  - name: test
    num_bytes: 1375745
    num_examples: 12765
  - name: train
    num_bytes: 10931355
    num_examples: 106122
  - name: validation
    num_bytes: 679692
    num_examples: 6362
  download_size: 232629010
  dataset_size: 12986792
- config_name: opensubtitles_inferred
  features:
  - name: text
    dtype: string
  - name: binary_label
    dtype:
      class_label:
        names:
          0: ABOUT:female
          1: ABOUT:male
  - name: binary_score
    dtype: float32
  - name: ternary_label
    dtype:
      class_label:
        names:
          0: ABOUT:female
          1: ABOUT:male
          2: ABOUT:gender-neutral
  - name: ternary_score
    dtype: float32
  splits:
  - name: test
    num_bytes: 3830528
    num_examples: 49108
  - name: train
    num_bytes: 27966476
    num_examples: 351036
  - name: validation
    num_bytes: 3363802
    num_examples: 41957
  download_size: 232629010
  dataset_size: 35160806
- config_name: yelp_inferred
  features:
  - name: text
    dtype: string
  - name: binary_label
    dtype:
      class_label:
        names:
          0: ABOUT:female
          1: ABOUT:male
  - name: binary_score
    dtype: float32
  splits:
  - name: test
    num_bytes: 53887700
    num_examples: 534460
  - name: train
    num_bytes: 260582945
    num_examples: 2577862
  - name: validation
    num_bytes: 324349
    num_examples: 4492
  download_size: 232629010
  dataset_size: 314794994
---

# Dataset Card for Multi-Dimensional Gender Bias Classification

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

- **Homepage:** [ParlAI MD Gender Project Page](https://parl.ai/projects/md_gender/)
- **Repository:** [ParlAI Github MD Gender Repository](https://github.com/facebookresearch/ParlAI/tree/master/projects/md_gender)
- **Paper:** [Multi-Dimensional Gender Bias Classification](https://www.aclweb.org/anthology/2020.emnlp-main.23.pdf)
- **Leaderboard:** [Needs More Information]
- **Point of Contact:** edinan@fb.com

### Dataset Summary

The Multi-Dimensional Gender Bias Classification dataset is based on a general framework that decomposes gender bias in text along several pragmatic and semantic dimensions: bias from the gender of the person being spoken about, bias from the gender of the person being spoken to, and bias from the gender of the speaker. It contains seven large scale datasets automatically annotated for gender information (there are eight in the original project but the Wikipedia set is not included in the HuggingFace distribution), one crowdsourced evaluation benchmark of utterance-level gender rewrites, a list of gendered names, and a list of gendered words in English. 

### Supported Tasks and Leaderboards

- `text-classification-other-gender-bias`: The dataset can be used to train a model for classification of various kinds of gender bias. The model performance is evaluated based on the accuracy of the predicted labels as compared to the given labels in the dataset. Dinan et al's (2020) Transformer model achieved an average of 67.13% accuracy in binary gender prediction across the ABOUT, TO, and AS tasks. See the paper for more results.

### Languages

The data is in English as spoken on the various sites where the data was collected. The associated BCP-47 code `en`.

## Dataset Structure

### Data Instances

The following are examples of data instances from the various configs in the dataset. See the [MD Gender Bias dataset viewer](https://huggingface.co/datasets/viewer/?dataset=md_gender_bias) to explore more examples.

An example from the `new_data` config:
```
{'class_type': 0, 
 'confidence': 'certain', 
 'episode_done': True, 
 'labels': [1], 
 'original': 'She designed monumental Loviisa war cemetery in 1920', 
 'text': 'He designed monumental Lovissa War Cemetery in 1920.', 
 'turker_gender': 4}
```

An example from the `funpedia` config:
```
{'gender': 2, 
 'persona': 'Humorous', 
 'text': 'Max Landis is a comic book writer who wrote Chronicle, American Ultra, and Victor Frankestein.', 
 'title': 'Max Landis'}
```

An example from the `image_chat` config:
```
{'caption': '<start> a young girl is holding a pink umbrella in her hand <eos>', 
 'female': True, 
 'id': '2923e28b6f588aff2d469ab2cccfac57', 
 'male': False}
```

An example from the `wizard` config:
```
{'chosen_topic': 'Krav Maga', 
 'gender': 2, 
 'text': 'Hello. I hope you might enjoy or know something about Krav Maga?'}
```

An example from the `convai2_inferred` config (the other `_inferred` configs have the same fields, with the exception of `yelp_inferred`, which does not have the `ternary_label` or `ternary_score` fields):
```
{'binary_label': 1, 
'binary_score': 0.6521999835968018, 
'ternary_label': 2, 
'ternary_score': 0.4496000111103058, 
'text': "hi , how are you doing ? i'm getting ready to do some cheetah chasing to stay in shape ."}
```

An example from the `gendered_words` config:
```
{'word_feminine': 'countrywoman',
 'word_masculine': 'countryman'}
```

An example from the `name_genders` config:
```
{'assigned_gender': 1,
 'count': 7065,
 'name': 'Mary'}
```

### Data Fields

The following are the features for each of the configs.

For the `new_data` config:
- `text`: the text to be classified
- `original`: the text before reformulation
- `labels`: a `list` of classification labels, with possible values including `ABOUT:female`, `ABOUT:male`, `PARTNER:female`, `PARTNER:male`, `SELF:female`.
- `class_type`: a classification label, with possible values including `about` (0), `partner` (1), `self` (2).
- `turker_gender`: a classification label, with possible values including `man` (0), `woman` (1), `nonbinary` (2), `prefer not to say` (3), `no answer` (4).
- `episode_done`: a boolean indicating whether the conversation was completed.
- `confidence`: a string indicating the confidence of the annotator in response to the instance label being ABOUT/TO/AS a man or woman. Possible values are `certain`, `pretty sure`, and `unsure`.  

For the `funpedia` config:
- `text`: the text to be classified.
- `gender`: a classification label, with possible values including `gender-neutral` (0), `female` (1), `male` (2), indicating the gender of the person being talked about.
- `persona`: a string describing the persona assigned to the user when talking about the entity.
- `title`: a string naming the entity the text is about.

For the `image_chat` config:
- `caption`: a string description of the contents of the original image.
- `female`: a boolean indicating whether the gender of the person being talked about is female, if the image contains a person. 
- `id`: a string indicating the id of the image.
- `male`: a boolean indicating whether the gender of the person being talked about is male, if the image contains a person. 

For the `wizard` config:
- `text`: the text to be classified.
- `chosen_topic`: a string indicating the topic of the text.
- `gender`: a classification label, with possible values including `gender-neutral` (0), `female` (1), `male` (2), indicating the gender of the person being talked about.

For the `_inferred` configurations (again, except the `yelp_inferred` split, which does not have the `ternary_label` or `ternary_score` fields):
- `text`: the text to be classified.
- `binary_label`: a classification label, with possible values including `ABOUT:female`, `ABOUT:male`.
- `binary_score`: a float indicating a score between 0 and 1.
- `ternary_label`: a classification label, with possible values including `ABOUT:female`, `ABOUT:male`, `ABOUT:gender-neutral`.
- `ternary_score`: a float indicating a score between 0 and 1.

For the word list:
- `word_masculine`: a string indicating the masculine version of the word.
- `word_feminine`: a string indicating the feminine version of the word.

For the gendered name list:
- `assigned_gender`: an integer, 1 for female, 0 for male.
- `count`: an integer.
- `name`: a string of the name.

### Data Splits

The different parts of the data can be accessed through the different configurations:
- `gendered_words`: A list of common nouns with a masculine and feminine variant.
- `new_data`: Sentences reformulated and annotated along all three axes.
- `funpedia`, `wizard`: Sentences from Funpedia and Wizards of Wikipedia annotated with ABOUT gender with entity gender information.
- `image_chat`: sentences about images annotated  with ABOUT gender based on gender information from the entities in the image
- `convai2_inferred`, `light_inferred`, `opensubtitles_inferred`, `yelp_inferred`:  Data from several source datasets with ABOUT annotations inferred by a trined classifier.

| Split      | M    | F   | N    | U    | Dimension |
| ---------- | ---- | --- | ---- | ---- | --------- |
| Image Chat | 39K  | 15K | 154K | -    | ABOUT     | 
| Funpedia   | 19K  | 3K  | 1K   | -    | ABOUT     |
| Wizard     | 6K   | 1K  | 1K   | -    | ABOUT     |
| Yelp       | 1M   | 1M  | -    | -    | AS        |
| ConvAI2    | 22K  | 22K | -    | 86K  | AS        |
| ConvAI2    | 22K  | 22K | -    | 86K  | TO        |
| OpenSub    | 149K | 69K | -    | 131K | AS        |
| OpenSub    | 95K  | 45K | -    | 209K | TO        |
| LIGHT      | 13K  | 8K  | -    | 83K  | AS        |
| LIGHT      | 13K  | 8K  | -    | 83K  | TO        |
| ---------- | ---- | --- | ---- | ---- | --------- |
| MDGender   | 384  | 401 | -    | -    | ABOUT     |
| MDGender   | 396  | 371 | -    | -    | AS        |
| MDGender   | 411  | 382 | -    | -    | TO        |

## Dataset Creation

### Curation Rationale

The curators chose to annotate the existing corpora to make their classifiers reliable on all dimensions (ABOUT/TO/AS) and across multiple domains. However, none of the existing datasets cover all three dimensions at the same time, and many of the gender labels are noisy. To enable reliable evaluation, the curators collected a specialized corpus, found in the `new_data` config, which acts as a gold-labeled dataset for the masculine and feminine classes.

### Source Data

#### Initial Data Collection and Normalization

For the `new_data` config, the curators collected conversations between two speakers. Each speaker was provided with a persona description containing gender information, then tasked with adopting that persona and having a conversation. They were also provided with small sections of a biography from Wikipedia as the conversation topic in order to encourage crowdworkers to discuss ABOUT/TO/AS gender information. To ensure there is ABOUT/TO/AS gender information contained in each utterance, the curators asked a second set of annotators to rewrite each utterance to make it very clear that they are speaking ABOUT a man or a woman, speaking AS a man or a woman, and speaking TO a man or a woman. 

#### Who are the source language producers?

This dataset was collected from crowdworkers from Amazon’s Mechanical Turk. All workers are English-speaking and located in the United States.

| Reported Gender   | Percent of Total |
| ----------------- | ---------------- |
| Man               | 67.38            |
| Woman             | 18.34            |
| Non-binary        | 0.21             |
| Prefer not to say | 14.07            |

### Annotations

#### Annotation process

For the `new_data` config, annotators were asked to label how confident they are that someone else could predict the given gender label, allowing for flexibility between explicit genderedness (like the use of "he" or "she") and statistical genderedness.

Many of the annotated datasets contain cases where the ABOUT, AS, TO labels are not provided (i.e. unknown). In such instances, the curators apply one of two strategies. They apply the imputation strategy for data for which the ABOUT label is unknown using a classifier trained only on other Wikipedia data for which this label is provided. Data without a TO or AS label was assigned one at random, choosing between masculine and feminine with equal probability. Details of how each of the eight training datasets was annotated are as follows:

1. Wikipedia- to annotate ABOUT, the curators used a Wikipedia dump and extract biography pages using named entity recognition. They labeled pages with a gender based on the number of gendered pronouns (he vs. she vs. they) and labeled each paragraph in the page with this label for the ABOUT dimension. 

2. Funpedia- Funpedia ([Miller et al., 2017](https://www.aclweb.org/anthology/D17-2014/)) contains rephrased Wikipedia sentences in a more conversational way. The curators retained only biography related sentences and annotate similar to Wikipedia, to give ABOUT labels.

3. Wizard of Wikipedia- [Wizard of Wikipedia](https://parl.ai/projects/wizard_of_wikipedia/) contains two people discussing a topic in Wikipedia. The curators retain only the conversations on Wikipedia biographies and annotate to create ABOUT labels.

4. ImageChat- [ImageChat](https://klshuster.github.io/image_chat/) contains conversations discussing the contents of an image. The curators used the [Xu et al. image captioning system](https://github.com/AaronCCWong/Show-Attend-and-Tell) to identify the contents of an image and select gendered examples.

5. Yelp- The curators used the Yelp reviewer gender predictor developed by ([Subramanian et al., 2018](https://arxiv.org/pdf/1811.00552.pdf)) and retain reviews for which the classifier is very confident – this creates labels for the content creator of the review (AS). They impute ABOUT labels on this dataset using a classifier trained on the datasets 1-4.

6. ConvAI2- [ConvAI2](https://parl.ai/projects/convai2/) contains persona-based conversations. Many personas contain sentences such as 'I am a old woman' or 'My name is Bob' which allows annotators to annotate the gender of the speaker (AS) and addressee (TO) with some confidence. Many of the personas have unknown gender. The curators impute ABOUT labels on this dataset using a classifier trained on the datasets 1-4.

7. OpenSubtitles- [OpenSubtitles](http://www.opensubtitles.org/) contains subtitles for movies in different languages. The curators retained English subtitles that contain a character name or identity. They annotated the character’s gender using gender kinship terms such as daughter and gender probability distribution calculated by counting the masculine and feminine names of baby names in the United States. Using the character’s gender, they produced labels for the AS dimension. They produced labels for the TO dimension by taking the gender of the next character to speak if there is another utterance in the conversation; otherwise, they take the gender of the last character to speak. They impute ABOUT labels on this dataset using a classifier trained on the datasets 1-4.

8. LIGHT- [LIGHT](https://parl.ai/projects/light/) contains persona-based conversation. Similarly to ConvAI2, annotators labeled the gender of each persona, giving labels for the speaker (AS) and speaking partner (TO). The curators impute ABOUT labels on this dataset using a classifier trained on the datasets 1-4.

#### Who are the annotators?

This dataset was annotated by crowdworkers from Amazon’s Mechanical Turk. All workers are English-speaking and located in the United States.

### Personal and Sensitive Information

For privacy reasons the curators did not associate the self-reported gender of the annotator with the labeled examples in the dataset and only report these statistics in aggregate. 

## Considerations for Using the Data

### Social Impact of Dataset

This dataset is intended for applications such as controlling for gender bias in generative models, detecting gender bias in arbitrary text, and classifying text as offensive based on its genderedness. 

### Discussion of Biases

Over two thirds of annotators identified as men, which may introduce biases into the dataset.

Wikipedia is also well known to have gender bias in equity of biographical coverage and lexical bias in noun references to women (see the paper's appendix for citations).

### Other Known Limitations

The limitations of the Multi-Dimensional Gender Bias Classification dataset have not yet been investigated, but the curators acknowledge that more work is required to address the intersectionality of gender identities, i.e., when gender non-additively interacts with other identity characteristics. The curators point out that negative gender stereotyping is known to be alternatively weakened or reinforced by the presence of social attributes like dialect, class and race and that these differences have been found to affect gender classification in images and sentences encoders. See the paper for references.

## Additional Information

### Dataset Curators

Emily Dinan, Angela Fan, Ledell Wu, Jason Weston, Douwe Kiela, and Adina Williams at Facebook AI Research. Angela Fan is also affiliated with Laboratoire Lorrain d’Informatique et Applications (LORIA).

### Licensing Information

The Multi-Dimensional Gender Bias Classification dataset is licensed under the [MIT License](https://opensource.org/licenses/MIT).

### Citation Information

```
@inproceedings{dinan-etal-2020-multi,
    title = "Multi-Dimensional Gender Bias Classification",
    author = "Dinan, Emily  and
      Fan, Angela  and
      Wu, Ledell  and
      Weston, Jason  and
      Kiela, Douwe  and
      Williams, Adina",
    booktitle = "Proceedings of the 2020 Conference on Empirical Methods in Natural Language Processing (EMNLP)",
    month = nov,
    year = "2020",
    address = "Online",
    publisher = "Association for Computational Linguistics",
    url = "https://www.aclweb.org/anthology/2020.emnlp-main.23",
    doi = "10.18653/v1/2020.emnlp-main.23",
    pages = "314--331",
    abstract = "Machine learning models are trained to find patterns in data. NLP models can inadvertently learn socially undesirable patterns when training on gender biased text. In this work, we propose a novel, general framework that decomposes gender bias in text along several pragmatic and semantic dimensions: bias from the gender of the person being spoken about, bias from the gender of the person being spoken to, and bias from the gender of the speaker. Using this fine-grained framework, we automatically annotate eight large scale datasets with gender information. In addition, we collect a new, crowdsourced evaluation benchmark. Distinguishing between gender bias along multiple dimensions enables us to train better and more fine-grained gender bias classifiers. We show our classifiers are valuable for a variety of applications, like controlling for gender bias in generative models, detecting gender bias in arbitrary text, and classifying text as offensive based on its genderedness.",
}
```

### Contributions

Thanks to [@yjernite](https://github.com/yjernite) and [@mcmillanmajora](https://github.com/mcmillanmajora)for adding this dataset.