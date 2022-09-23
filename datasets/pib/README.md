---
task_categories:
- translation
- text-generation
- fill-mask
task_ids:
- language-modeling
- masked-language-modeling
multilinguality:
- translation
language:
- bn
- en
- gu
- hi
- ml
- mr
- or
- pa
- ta
- te
- ur
language_creators:
- other
annotations_creators:
- no-annotation
source_datasets:
- original
size_categories:
- 100K<n<1M
- 10K<n<100K
license:
- cc-by-4.0
paperswithcode_id: null
pretty_name: CVIT PIB
configs:
- bn-en
- bn-gu
- bn-hi
- bn-ml
- bn-mr
- bn-or
- bn-pa
- bn-ta
- bn-te
- bn-ur
- en-gu
- en-hi
- en-ml
- en-mr
- en-or
- en-pa
- en-ta
- en-te
- en-ur
- gu-hi
- gu-ml
- gu-mr
- gu-or
- gu-pa
- gu-ta
- gu-te
- gu-ur
- hi-ml
- hi-mr
- hi-or
- hi-pa
- hi-ta
- hi-te
- hi-ur
- ml-mr
- ml-or
- ml-pa
- ml-ta
- ml-te
- ml-ur
- mr-or
- mr-pa
- mr-ta
- mr-te
- mr-ur
- or-pa
- or-ta
- or-te
- or-ur
- pa-ta
- pa-te
- pa-ur
- ta-te
- ta-ur
- te-ur
dataset_info:
- config_name: or-ur
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - or
        - ur
  splits:
  - name: train
    num_bytes: 27790211
    num_examples: 43766
  download_size: 393352875
  dataset_size: 27790211
- config_name: ml-or
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - ml
        - or
  splits:
  - name: train
    num_bytes: 16011549
    num_examples: 19413
  download_size: 393352875
  dataset_size: 16011549
- config_name: bn-ta
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - bn
        - ta
  splits:
  - name: train
    num_bytes: 28706668
    num_examples: 33005
  download_size: 393352875
  dataset_size: 28706668
- config_name: gu-mr
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - gu
        - mr
  splits:
  - name: train
    num_bytes: 24253770
    num_examples: 30766
  download_size: 393352875
  dataset_size: 24253770
- config_name: hi-or
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - hi
        - or
  splits:
  - name: train
    num_bytes: 45086618
    num_examples: 61070
  download_size: 393352875
  dataset_size: 45086618
- config_name: en-or
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - en
        - or
  splits:
  - name: train
    num_bytes: 51258494
    num_examples: 98230
  download_size: 393352875
  dataset_size: 51258494
- config_name: mr-ur
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - mr
        - ur
  splits:
  - name: train
    num_bytes: 34053295
    num_examples: 49691
  download_size: 393352875
  dataset_size: 34053295
- config_name: en-ta
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - en
        - ta
  splits:
  - name: train
    num_bytes: 74931542
    num_examples: 118759
  download_size: 393352875
  dataset_size: 74931542
- config_name: hi-ta
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - hi
        - ta
  splits:
  - name: train
    num_bytes: 57628429
    num_examples: 64945
  download_size: 393352875
  dataset_size: 57628429
- config_name: bn-en
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - bn
        - en
  splits:
  - name: train
    num_bytes: 53291968
    num_examples: 93560
  download_size: 393352875
  dataset_size: 53291968
- config_name: bn-or
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - bn
        - or
  splits:
  - name: train
    num_bytes: 19819136
    num_examples: 26456
  download_size: 393352875
  dataset_size: 19819136
- config_name: ml-ta
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - ml
        - ta
  splits:
  - name: train
    num_bytes: 21685938
    num_examples: 23609
  download_size: 393352875
  dataset_size: 21685938
- config_name: gu-ur
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - gu
        - ur
  splits:
  - name: train
    num_bytes: 20312414
    num_examples: 29938
  download_size: 393352875
  dataset_size: 20312414
- config_name: bn-ml
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - bn
        - ml
  splits:
  - name: train
    num_bytes: 15545271
    num_examples: 18149
  download_size: 393352875
  dataset_size: 15545271
- config_name: ml-pa
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - ml
        - pa
  splits:
  - name: train
    num_bytes: 18114904
    num_examples: 21978
  download_size: 393352875
  dataset_size: 18114904
- config_name: en-pa
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - en
        - pa
  splits:
  - name: train
    num_bytes: 56316514
    num_examples: 103296
  download_size: 393352875
  dataset_size: 56316514
- config_name: bn-hi
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - bn
        - hi
  splits:
  - name: train
    num_bytes: 40970170
    num_examples: 49598
  download_size: 393352875
  dataset_size: 40970170
- config_name: hi-pa
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - hi
        - pa
  splits:
  - name: train
    num_bytes: 59293062
    num_examples: 75200
  download_size: 393352875
  dataset_size: 59293062
- config_name: gu-te
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - gu
        - te
  splits:
  - name: train
    num_bytes: 14517828
    num_examples: 16335
  download_size: 393352875
  dataset_size: 14517828
- config_name: pa-ta
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - pa
        - ta
  splits:
  - name: train
    num_bytes: 39144065
    num_examples: 46349
  download_size: 393352875
  dataset_size: 39144065
- config_name: hi-ml
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - hi
        - ml
  splits:
  - name: train
    num_bytes: 24015298
    num_examples: 27167
  download_size: 393352875
  dataset_size: 24015298
- config_name: or-te
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - or
        - te
  splits:
  - name: train
    num_bytes: 9011734
    num_examples: 10475
  download_size: 393352875
  dataset_size: 9011734
- config_name: en-ml
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - en
        - ml
  splits:
  - name: train
    num_bytes: 27754969
    num_examples: 44986
  download_size: 393352875
  dataset_size: 27754969
- config_name: en-hi
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - en
        - hi
  splits:
  - name: train
    num_bytes: 160009440
    num_examples: 269594
  download_size: 393352875
  dataset_size: 160009440
- config_name: bn-pa
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - bn
        - pa
  splits:
  - name: train
    num_bytes: 27522373
    num_examples: 35109
  download_size: 393352875
  dataset_size: 27522373
- config_name: mr-te
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - mr
        - te
  splits:
  - name: train
    num_bytes: 16838115
    num_examples: 18179
  download_size: 393352875
  dataset_size: 16838115
- config_name: mr-pa
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - mr
        - pa
  splits:
  - name: train
    num_bytes: 38720410
    num_examples: 50418
  download_size: 393352875
  dataset_size: 38720410
- config_name: bn-te
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - bn
        - te
  splits:
  - name: train
    num_bytes: 15529843
    num_examples: 17605
  download_size: 393352875
  dataset_size: 15529843
- config_name: gu-hi
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - gu
        - hi
  splits:
  - name: train
    num_bytes: 33606230
    num_examples: 41587
  download_size: 393352875
  dataset_size: 33606230
- config_name: ta-ur
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - ta
        - ur
  splits:
  - name: train
    num_bytes: 37593813
    num_examples: 48892
  download_size: 393352875
  dataset_size: 37593813
- config_name: te-ur
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - te
        - ur
  splits:
  - name: train
    num_bytes: 16485209
    num_examples: 21148
  download_size: 393352875
  dataset_size: 16485209
- config_name: or-pa
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - or
        - pa
  splits:
  - name: train
    num_bytes: 30081903
    num_examples: 43159
  download_size: 393352875
  dataset_size: 30081903
- config_name: gu-ml
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - gu
        - ml
  splits:
  - name: train
    num_bytes: 15749821
    num_examples: 18252
  download_size: 393352875
  dataset_size: 15749821
- config_name: gu-pa
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - gu
        - pa
  splits:
  - name: train
    num_bytes: 27441041
    num_examples: 35566
  download_size: 393352875
  dataset_size: 27441041
- config_name: hi-te
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - hi
        - te
  splits:
  - name: train
    num_bytes: 26473814
    num_examples: 28569
  download_size: 393352875
  dataset_size: 26473814
- config_name: en-te
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - en
        - te
  splits:
  - name: train
    num_bytes: 28620219
    num_examples: 44888
  download_size: 393352875
  dataset_size: 28620219
- config_name: ml-te
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - ml
        - te
  splits:
  - name: train
    num_bytes: 9690153
    num_examples: 10480
  download_size: 393352875
  dataset_size: 9690153
- config_name: pa-ur
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - pa
        - ur
  splits:
  - name: train
    num_bytes: 34959176
    num_examples: 51831
  download_size: 393352875
  dataset_size: 34959176
- config_name: hi-ur
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - hi
        - ur
  splits:
  - name: train
    num_bytes: 81262590
    num_examples: 109951
  download_size: 393352875
  dataset_size: 81262590
- config_name: mr-or
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - mr
        - or
  splits:
  - name: train
    num_bytes: 33998805
    num_examples: 47001
  download_size: 393352875
  dataset_size: 33998805
- config_name: en-ur
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - en
        - ur
  splits:
  - name: train
    num_bytes: 100571795
    num_examples: 202578
  download_size: 393352875
  dataset_size: 100571795
- config_name: ml-ur
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - ml
        - ur
  splits:
  - name: train
    num_bytes: 15663718
    num_examples: 20913
  download_size: 393352875
  dataset_size: 15663718
- config_name: bn-mr
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - bn
        - mr
  splits:
  - name: train
    num_bytes: 27604502
    num_examples: 34043
  download_size: 393352875
  dataset_size: 27604502
- config_name: gu-ta
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - gu
        - ta
  splits:
  - name: train
    num_bytes: 25089131
    num_examples: 29187
  download_size: 393352875
  dataset_size: 25089131
- config_name: pa-te
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - pa
        - te
  splits:
  - name: train
    num_bytes: 23119690
    num_examples: 25684
  download_size: 393352875
  dataset_size: 23119690
- config_name: bn-gu
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - bn
        - gu
  splits:
  - name: train
    num_bytes: 19899277
    num_examples: 25166
  download_size: 393352875
  dataset_size: 19899277
- config_name: bn-ur
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - bn
        - ur
  splits:
  - name: train
    num_bytes: 27540215
    num_examples: 39290
  download_size: 393352875
  dataset_size: 27540215
- config_name: ml-mr
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - ml
        - mr
  splits:
  - name: train
    num_bytes: 19723458
    num_examples: 22796
  download_size: 393352875
  dataset_size: 19723458
- config_name: or-ta
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - or
        - ta
  splits:
  - name: train
    num_bytes: 35357904
    num_examples: 44035
  download_size: 393352875
  dataset_size: 35357904
- config_name: ta-te
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - ta
        - te
  splits:
  - name: train
    num_bytes: 17415768
    num_examples: 17359
  download_size: 393352875
  dataset_size: 17415768
- config_name: gu-or
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - gu
        - or
  splits:
  - name: train
    num_bytes: 20111876
    num_examples: 27162
  download_size: 393352875
  dataset_size: 20111876
- config_name: en-gu
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - en
        - gu
  splits:
  - name: train
    num_bytes: 33630906
    num_examples: 59739
  download_size: 393352875
  dataset_size: 33630906
- config_name: hi-mr
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - hi
        - mr
  splits:
  - name: train
    num_bytes: 55680473
    num_examples: 69186
  download_size: 393352875
  dataset_size: 55680473
- config_name: mr-ta
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - mr
        - ta
  splits:
  - name: train
    num_bytes: 41585343
    num_examples: 48535
  download_size: 393352875
  dataset_size: 41585343
- config_name: en-mr
  features:
  - name: translation
    dtype:
      translation:
        languages:
        - en
        - mr
  splits:
  - name: train
    num_bytes: 65042597
    num_examples: 117199
  download_size: 393352875
  dataset_size: 65042597
---

# Dataset Card for CVIT PIB

## Table of Contents
- [Table of Contents](#table-of-contents)
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

- **Homepage:** http://preon.iiit.ac.in/~jerin/bhasha/
- **Paper:** https://arxiv.org/abs/2008.04860
- **Point of Contact:** [Mailing List](cvit-bhasha@googlegroups.com)

### Dataset Summary

This dataset is the large scale sentence aligned corpus in 11 Indian languages, viz. CVIT-PIB corpus that is the largest multilingual corpus available for Indian languages.

### Supported Tasks and Leaderboards

- Machine Translation

### Languages

Parallel data for following languages [en, bn, gu, hi, ml, mr, pa, or, ta, te, ur] are covered.

## Dataset Structure

### Data Instances

An example for the "gu-pa" language pair:
```
{
  'translation': {
    'gu': 'એવો નિર્ણય લેવાયો હતો કે ખંતપૂર્વકની કામગીરી હાથ ધરવા, કાયદેસર અને ટેકનિકલ મૂલ્યાંકન કરવા, વેન્ચર કેપિટલ ઇન્વેસ્ટમેન્ટ સમિતિની બેઠક યોજવા વગેરે એઆઇએફને કરવામાં આવેલ પ્રતિબદ્ધતાના 0.50 ટકા સુધી અને બાકીની રકમ એફએફએસને પૂર્ણ કરવામાં આવશે.',
    'pa': 'ਇਹ ਵੀ ਫੈਸਲਾ ਕੀਤਾ ਗਿਆ ਕਿ ਐੱਫਆਈਆਈ ਅਤੇ ਬਕਾਏ ਲਈ ਕੀਤੀਆਂ ਗਈਆਂ ਵਚਨਬੱਧਤਾਵਾਂ ਦੇ 0.50 % ਦੀ ਸੀਮਾ ਤੱਕ ਐੱਫਈਐੱਸ ਨੂੰ ਮਿਲਿਆ ਜਾਏਗਾ, ਇਸ ਨਾਲ ਉੱਦਮ ਪੂੰਜੀ ਨਿਵੇਸ਼ ਕਮੇਟੀ ਦੀ ਬੈਠਕ ਦਾ ਆਯੋਜਨ ਉਚਿਤ ਸਾਵਧਾਨੀ, ਕਾਨੂੰਨੀ ਅਤੇ ਤਕਨੀਕੀ ਮੁੱਲਾਂਕਣ ਲਈ ਸੰਚਾਲਨ ਖਰਚ ਆਦਿ ਦੀ ਪੂਰਤੀ ਹੋਵੇਗੀ।'
  }
}
```

### Data Fields

- `translation`: Translation field containing the parallel text for the pair of languages.

### Data Splits

The dataset is in a single "train" split.

## Dataset Creation

### Curation Rationale

[More Information Needed]

### Source Data

#### Initial Data Collection and Normalization

[More Information Needed]

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

[More Information Needed]

### Licensing Information

[Creative Commons Attribution-ShareAlike 4.0 International](https://creativecommons.org/licenses/by-sa/4.0/) license.

### Citation Information

```
@inproceedings{siripragada-etal-2020-multilingual,
    title = "A Multilingual Parallel Corpora Collection Effort for {I}ndian Languages",
    author = "Siripragada, Shashank  and
      Philip, Jerin  and
      Namboodiri, Vinay P.  and
      Jawahar, C V",
    booktitle = "Proceedings of the 12th Language Resources and Evaluation Conference",
    month = may,
    year = "2020",
    address = "Marseille, France",
    publisher = "European Language Resources Association",
    url = "https://aclanthology.org/2020.lrec-1.462",
    pages = "3743--3751",
    language = "English",
    ISBN = "979-10-95546-34-4",
}
@article{2020,
   title={Revisiting Low Resource Status of Indian Languages in Machine Translation},
   url={http://dx.doi.org/10.1145/3430984.3431026},
   DOI={10.1145/3430984.3431026},
   journal={8th ACM IKDD CODS and 26th COMAD},
   publisher={ACM},
   author={Philip, Jerin and Siripragada, Shashank and Namboodiri, Vinay P. and Jawahar, C. V.},
   year={2020},
   month={Dec}
}
```

### Contributions

Thanks to [@vasudevgupta7](https://github.com/vasudevgupta7) for adding this dataset,
and [@albertvillanova](https://github.com/albertvillanova) for updating its version.