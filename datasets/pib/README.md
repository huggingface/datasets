---
task_categories:
- sequence-modeling
task_ids:
- language-modeling
multilinguality:
- translation
languages:
- en
- hi
- ta
- te
- ml
- ur
- bn
- mr
- gu
- or
- pa
language_creators:
- other
annotations_creators:
- no-annotation
source_datasets:
- original
size_categories:
  bn-en:
  - 10K<n<100K
  bn-gu:
  - 1K<n<10K
  bn-hi:
  - 10K<n<100K
  bn-ml:
  - 1K<n<10K
  bn-mr:
  - 1K<n<10K
  bn-or:
  - n<1K
  bn-pa:
  - 1K<n<10K
  bn-ta:
  - 1K<n<10K
  bn-te:
  - n<1K
  bn-ur:
  - 1K<n<10K
  en-gu:
  - 10K<n<100K
  en-hi:
  - 100K<n<1M
  en-ml:
  - 10K<n<100K
  en-mr:
  - 10K<n<100K
  en-or:
  - 1K<n<10K
  en-pa:
  - 10K<n<100K
  en-ta:
  - 10K<n<100K
  en-te:
  - 1K<n<10K
  en-ur:
  - 10K<n<100K
  gu-hi:
  - 10K<n<100K
  gu-ml:
  - 1K<n<10K
  gu-mr:
  - 1K<n<10K
  gu-or:
  - n<1K
  gu-pa:
  - 1K<n<10K
  gu-ta:
  - 1K<n<10K
  gu-te:
  - 1K<n<10K
  gu-ur:
  - 1K<n<10K
  hi-ml:
  - 1K<n<10K
  hi-mr:
  - 10K<n<100K
  hi-or:
  - 1K<n<10K
  hi-pa:
  - 1K<n<10K
  hi-ta:
  - 10K<n<100K
  hi-te:
  - 1K<n<10K
  hi-ur:
  - 1K<n<10K
  ml-mr:
  - 1K<n<10K
  ml-or:
  - n<1K
  ml-pa:
  - 1K<n<10K
  ml-ta:
  - 1K<n<10K
  ml-te:
  - 1K<n<10K
  ml-ur:
  - 1K<n<10K
  mr-or:
  - n<1K
  mr-pa:
  - 1K<n<10K
  mr-ta:
  - 10K<n<100K
  mr-te:
  - n<1K
  mr-ur:
  - 1K<n<10K
  or-pa:
  - n<1K
  or-ta:
  - n<1K
  or-te:
  - n<1K
  or-ur:
  - n<1K
  pa-ta:
  - 1K<n<10K
  pa-te:
  - 1K<n<10K
  pa-ur:
  - 1K<n<10K
  ta-te:
  - 1K<n<10K
  ta-ur:
  - 1K<n<10K
  te-ur:
  - n<1K
licenses:
- cc-by-4.0
paperswithcode_id: null
pretty_name: CVIT PIB
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

[More Information Needed]

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
