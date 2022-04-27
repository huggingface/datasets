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
  - 10K<n<100K
  bn-hi:
  - 10K<n<100K
  bn-ml:
  - 10K<n<100K
  bn-mr:
  - 10K<n<100K
  bn-or:
  - 10K<n<100K
  bn-pa:
  - 10K<n<100K
  bn-ta:
  - 10K<n<100K
  bn-te:
  - 10K<n<100K
  bn-ur:
  - 10K<n<100K
  en-gu:
  - 10K<n<100K
  en-hi:
  - 100K<n<1M
  en-ml:
  - 10K<n<100K
  en-mr:
  - 100K<n<1M
  en-or:
  - 10K<n<100K
  en-pa:
  - 100K<n<1M
  en-ta:
  - 100K<n<1M
  en-te:
  - 10K<n<100K
  en-ur:
  - 100K<n<1M
  gu-hi:
  - 10K<n<100K
  gu-ml:
  - 10K<n<100K
  gu-mr:
  - 10K<n<100K
  gu-or:
  - 10K<n<100K
  gu-pa:
  - 10K<n<100K
  gu-ta:
  - 10K<n<100K
  gu-te:
  - 10K<n<100K
  gu-ur:
  - 10K<n<100K
  hi-ml:
  - 10K<n<100K
  hi-mr:
  - 10K<n<100K
  hi-or:
  - 10K<n<100K
  hi-pa:
  - 10K<n<100K
  hi-ta:
  - 10K<n<100K
  hi-te:
  - 10K<n<100K
  hi-ur:
  - 100K<n<1M
  ml-mr:
  - 10K<n<100K
  ml-or:
  - 10K<n<100K
  ml-pa:
  - 10K<n<100K
  ml-ta:
  - 10K<n<100K
  ml-te:
  - 10K<n<100K
  ml-ur:
  - 10K<n<100K
  mr-or:
  - 10K<n<100K
  mr-pa:
  - 10K<n<100K
  mr-ta:
  - 10K<n<100K
  mr-te:
  - 10K<n<100K
  mr-ur:
  - 10K<n<100K
  or-pa:
  - 10K<n<100K
  or-ta:
  - 10K<n<100K
  or-te:
  - 10K<n<100K
  or-ur:
  - 10K<n<100K
  pa-ta:
  - 10K<n<100K
  pa-te:
  - 10K<n<100K
  pa-ur:
  - 10K<n<100K
  ta-te:
  - 10K<n<100K
  ta-ur:
  - 10K<n<100K
  te-ur:
  - 10K<n<100K
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
