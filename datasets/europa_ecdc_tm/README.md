---
annotations_creators:
- expert-generated
language_creators:
- expert-generated
languages:
- bg
- cs
- da
- de
- el
- en
- es
- et
- fi
- fr
- ga
- hu
- is
- it
- lt
- lv
- mt
- nl
- 'no'
- pl
- pt
- ro
- sk
- sl
- sv
licenses:
- cc-by-sa-4.0
multilinguality:
- translation
size_categories:
- 1K<n<10K
source_datasets:
- original
task_categories:
- conditional-text-generation
task_ids:
- machine-translation
paperswithcode_id: null
---

# Dataset Card for [Dataset Name]

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

- **Homepage:** [https://ec.europa.eu/jrc/en/language-technologies/ecdc-translation-memory](https://ec.europa.eu/jrc/en/language-technologies/ecdc-translation-memory)
- **Paper:** [https://link.springer.com/article/10.1007/s10579-014-9277-0](https://link.springer.com/article/10.1007/s10579-014-9277-0)
- **Point of Contact:** [Ralf Steinberger](mailto:Ralf.Steinberger@jrc.ec.europa.eu)

### Dataset Summary

In October 2012, the European Union (EU) agency 'European Centre for Disease Prevention and Control' (ECDC) released a translation memory (TM), i.e. a collection of sentences and their professionally produced translations, in twenty-five languages.

ECDC-TM covers 25 languages: the 23 official languages of the EU plus Norwegian (Norsk) and Icelandic. ECDC-TM was created by translating from English into the following 24 languages: Bulgarian, Czech, Danish, Dutch, English, Estonian, Gaelige (Irish), German, Greek, Finnish, French, Hungarian, Icelandic, Italian, Latvian, Lithuanian, Maltese, Norwegian (NOrsk), Polish, Portuguese, Romanian, Slovak, Slovenian, Spanish and Swedish.

All documents and sentences were originally written in English. They were then translated into the other languages by professional translators from the Translation Centre CdT in Luxembourg.

To load a language pair that is not part of the config, just specify the language code as language pair. For example, if you want to translate Czech to Greek:

`dataset = load_dataset("europa_ecdc_tm", language_pair=("cs", "el"))`

### Supported Tasks and Leaderboards

- `conditional-text-generation`: the dataset can be used to train a model for `machine-translation`. Machine translation models are usually evaluated using metrics such as [BLEU](https://huggingface.co/metrics/bleu), [ROUGE](https://huggingface.co/metrics/rouge) or [SacreBLEU](https://huggingface.co/metrics/sacrebleu). You can use the [mBART](https://huggingface.co/facebook/mbart-large-cc25) model for this task. This task has active leaderboards which can be found at [https://paperswithcode.com/task/machine-translation](https://paperswithcode.com/task/machine-translation), which usually rank models based on [BLEU score](https://huggingface.co/metrics/bleu).

### Languages

All documents and sentences were originally written in English (`en`). They were then translated into the other languages by professional translators from the Translation Centre CdT in Luxembourg.

Translations are available in these languages: `en`, `bg`, `cs`, `da`, `de`, `el`, `en`, `es`, `et`, `fi`, `fr`, `ga`, `hu`, `is`, `it`, `lt`, `lv`, `mt`, `nl`, `no`, `pl`, `pt`, `ro`, `sk`, `sl`, `sv`.

## Dataset Structure

### Data Instances

```
{
  "translation": {
    "<source_language>":"Sentence to translate",
    "<target_language>": "Translated sentence",
  },
}
```

### Data Fields

- `translation`: a multilingual `string` variable, with possible languages including `en`, `bg`, `cs`, `da`, `de`, `el`, `en`, `es`, `et`, `fi`, `fr`, `ga`, `hu`, `is`, `it`, `lt`, `lv`, `mt`, `nl`, `no`, `pl`, `pt`, `ro`, `sk`, `sl`, `sv`.


### Data Splits

The data is not splitted (only the `train` split is available).

## Dataset Creation

### Curation Rationale

The ECDC-TM is relatively small compared to the JRC-Acquis and to DGT-TM, but it has the advantage that it focuses on a very different domain, namely that of public health. Also, it includes translation units for the languages Irish (Gaelige, GA), Norwegian (Norsk, NO) and Icelandic (IS).

### Source Data

#### Initial Data Collection and Normalization

ECDC-TM was built on the basis of the website of the European Centre for Disease Prevention and Control (ECDC). The major part of the documents talks about health-related topics (anthrax, botulism, cholera, dengue fever, hepatitis, etc.), but some of the web pages also describe the organisation ECDC (e.g. its organisation, job opportunities) and its activities (e.g. epidemic intelligence, surveillance).

#### Who are the source language producers?

All documents and sentences were originally written in English, by the ECDC website content producers.

### Annotations

#### Annotation process

[More Information Needed]

#### Who are the annotators?

All documents and sentences were thus originally written in English. They were then translated into the other languages by professional translators from the Translation Centre CdT in Luxembourg.

### Personal and Sensitive Information

[More Information Needed]

## Considerations for Using the Data

### Social Impact of Dataset

Contains translations of sentences in the public healthcare domain, including technical terms (disease and treatment names for example).

### Discussion of Biases

[More Information Needed]

### Other Known Limitations

[More Information Needed]

## Additional Information

### Dataset Curators

[More Information Needed]

### Licensing Information

Copyright © EU / ECDC, 2020

#### Copyright

The Work (as defined below) is provided under the terms of this Licence (or later versions of
this Licence published by the European Commission). The work is protected by copyright
and/or other applicable law. Any use of the work other than as authorised under this
Licence or copyright law is prohibited.  
The terms provided herein conform to the reuse policy established by the Commission's
Reuse Decision (2011/833/EU).
By exercising any rights to the work provided here, you accept and agree to be bound by the
terms of this Licence. The Owner (as defined below) grants You the rights conferred by this
Licence in consideration of your acceptance of such terms and conditions.

#### Definitions

The ‘Owner’ shall mean jointly the European Union represented by the European
Commission and the European Centre for Disease Prevention and Control, which are the
original licensors and/or control the copyright and any other intellectual and industrial
property rights related to the Work.
The ‘Work’ is the information and/or data offered to You under this Licence, according to
the ‘Copyright Notice’:
Copyright (c) EU/ECDC, <YEAR>
‘You’ means the natural or legal person, or body of persons corporate or incorporate,
acquiring rights under this Licence.
‘Use’ means any act which is restricted by copyright or database rights, whether in the
original medium or in any other medium, and includes, without limitation, distributing,
copying, adapting, or modifying as may be technically necessary to use the Work in a
different mode or format. It includes ‘re‐Use’, meaning the use, communication to the
public and/or distribution of the Works for purposes other than the initial purpose for which
the Work was produced.

#### Rights 

You are herewith granted a worldwide, royalty‐free, perpetual, non‐exclusive Licence to Use
and re‐Use the Works and any modifications thereof for any commercial and non‐
commercial purpose allowed by the law, provided that the following conditions are met:
a) Unmodified distributions must retain the above Copyright Notice;
b) Unmodified distributions must retain the following ‘No Warranty’ disclaimer;
c) You will not use the name of the Owner to endorse or promote products and
services derived from Use of the Work without specific prior written permission.

#### No warranty

Each Work is provided ‘as is’ without, to the full extent permitted by law, representations,
warranties, obligations and liabilities of any kind, either express or implied, including, but
not limited to, any implied warranty of merchantability, integration, satisfactory quality and
fitness for a particular purpose.
Except in the cases of wilful misconduct or damages directly caused to natural persons, the
Owner will not be liable for any incidental, consequential, direct or indirect damages,
including, but not limited to, the loss of data, lost profits or any other financial loss arising
from the use of, or inability to use, the Work even if the Owner has been notified of the
possibility of such loss, damages, claims or costs, or for any claim by any third party. The
Owner may be liable under national statutory product liability laws as far as such laws apply
to the Work.

### Citation Information

```
@Article{Steinberger2014,
        author={Steinberger, Ralf
                and Ebrahim, Mohamed
                and Poulis, Alexandros
                and Carrasco-Benitez, Manuel
                and Schl{\"u}ter, Patrick
                and Przybyszewski, Marek
                and Gilbro, Signe},
        title={An overview of the European Union's highly multilingual parallel corpora},
        journal={Language Resources and Evaluation},
        year={2014},
        month={Dec},
        day={01},
        volume={48},
        number={4},
        pages={679-707},
        issn={1574-0218},
        doi={10.1007/s10579-014-9277-0},
        url={https://doi.org/10.1007/s10579-014-9277-0}
}
```

### Contributions

Thanks to [@SBrandeis](https://github.com/SBrandeis) for adding this dataset.