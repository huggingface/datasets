---
annotations_creators:
- expert-generated
language_creators:
- expert-generated
languages:
  am:
  - am
  ha:
  - ha
  ig:
  - ig
  rw:
  - rw
  lg:
  - lg
  luo:
  - luo
  pcm:
  - pcm
  sw:
  - sw
  wo:
  - wo
  yo:
  - yo

licenses:
- unknown
multilinguality:
- multilingual
size_categories:
- 10K<n<100K
source_datasets:
- original
task_categories:
- token-classification
task_ids:
- named-entity-recognition
paperswithcode_id: null
pretty_name: MasakhaNER
---

# Dataset Card for MasakhaNER

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

- **Homepage:** [homepage](https://github.com/masakhane-io/masakhane-ner)
- **Repository:** [github](https://github.com/masakhane-io/masakhane-ner)
- **Paper:** [paper](https://arxiv.org/abs/2103.11811)
- **Point of Contact:** [Masakhane](https://www.masakhane.io/) or didelani@lsv.uni-saarland.de

### Dataset Summary

MasakhaNER is the first large publicly available high-quality dataset for named entity recognition (NER) in ten African languages.

Named entities are phrases that contain the names of persons, organizations, locations, times and quantities. Example:

[PER Wolff] , currently a journalist in [LOC Argentina] , played with [PER Del Bosque] in the final years of the seventies in [ORG Real Madrid] .

MasakhaNER is a named entity dataset consisting of PER, ORG, LOC, and DATE entities annotated by Masakhane for ten African languages:
- Amharic
- Hausa
- Igbo
- Kinyarwanda
- Luganda
- Luo
- Nigerian-Pidgin
- Swahili
- Wolof
- Yoruba

The train/validation/test sets are available for all the ten languages.

For more details see https://arxiv.org/abs/2103.11811


### Supported Tasks and Leaderboards

[More Information Needed]

- `named-entity-recognition`: The performance in this task is measured with [F1](https://huggingface.co/metrics/f1) (higher is better). A named entity is correct only if it is an exact match of the corresponding entity in the data.

### Languages

There are ten languages available :
- Amharic (amh)
- Hausa (hau)
- Igbo (ibo)
- Kinyarwanda (kin)
- Luganda (kin)
- Luo (luo)
- Nigerian-Pidgin (pcm)
- Swahili (swa)
- Wolof (wol)
- Yoruba (yor)

## Dataset Structure

### Data Instances

The examples look like this for Yorùbá:

```
from datasets import load_dataset
data = load_dataset('masakhaner', 'yor') 

# Please, specify the language code

# A data point consists of sentences seperated by empty line and tab-seperated tokens and tags. 
{'id': '0',
 'ner_tags': [B-DATE, I-DATE, 0, 0, 0, 0, 0, B-PER, I-PER, I-PER, O, O, O, O],
 'tokens': ['Wákàtí', 'méje', 'ti', 'ré', 'kọjá', 'lọ', 'tí', 'Luis', 'Carlos', 'Díaz', 'ti', 'di', 'awati', '.']
}
```

### Data Fields

- `id`: id of the sample
- `tokens`: the tokens of the example text
- `ner_tags`: the NER tags of each token

The NER tags correspond to this list:
```
"O", "B-PER", "I-PER", "B-ORG", "I-ORG", "B-LOC", "I-LOC", "B-DATE", "I-DATE",
```

In the NER tags, a B denotes the first item of a phrase and an I any non-initial word. There are four types of phrases: person names (PER), organizations (ORG), locations (LOC) and dates & time (DATE).

It is assumed that named entities are non-recursive and non-overlapping. In case a named entity is embedded in another named entity usually, only the top level entity is marked.

### Data Splits

For all languages, there are three splits.

The original splits were named `train`, `dev` and `test` and they correspond to the `train`, `validation` and `test` splits.

The splits have the following sizes :

| Language        | train | validation | test |
|-----------------|------:|-----------:|-----:|
| Amharic         |  1750 |        250 |  500 |
| Hausa           |  1903 |        272 |  545 |
| Igbo            |  2233 |        319 |  638 |
| Kinyarwanda     |  2110 |        301 |  604 |
| Luganda         |  2003 |        200 |  401 |
| Luo             |   644 |         92 |  185 |
| Nigerian-Pidgin |  2100 |        300 |  600 |
| Swahili         |  2104 |        300 |  602 |
| Wolof           |  1871 |        267 |  536 |
| Yoruba          |  2124 |        303 |  608 |

## Dataset Creation

### Curation Rationale

The dataset was introduced to introduce new resources to ten languages that were under-served for natural language processing.

[More Information Needed]

### Source Data

The source of the data is from the news domain, details can be found here https://arxiv.org/abs/2103.11811

#### Initial Data Collection and Normalization

The articles were word-tokenized, information on the exact pre-processing pipeline is unavailable.

#### Who are the source language producers?

The source language was produced by journalists and writers employed by the news agency and newspaper mentioned above.

### Annotations

#### Annotation process

Details can be found here https://arxiv.org/abs/2103.11811

#### Who are the annotators?

Annotators were recruited from [Masakhane](https://www.masakhane.io/)

### Personal and Sensitive Information

The data is sourced from newspaper source and only contains mentions of public figures or individuals

## Considerations for Using the Data

### Social Impact of Dataset
[More Information Needed]


### Discussion of Biases
[More Information Needed]


### Other Known Limitations

Users should keep in mind that the dataset only contains news text, which might limit the applicability of the developed systems to other domains.

## Additional Information

### Dataset Curators


### Licensing Information

The licensing status of the data is CC 4.0 Non-Commercial

### Citation Information

Provide the [BibTex](http://www.bibtex.org/)-formatted reference for the dataset. For example:
```
@article{Adelani2021MasakhaNERNE,
  title={MasakhaNER: Named Entity Recognition for African Languages},
  author={D. Adelani and Jade Abbott and Graham Neubig and Daniel D'Souza and Julia Kreutzer and Constantine Lignos 
  and Chester Palen-Michel and Happy Buzaaba and Shruti Rijhwani and Sebastian Ruder and Stephen Mayhew and 
  Israel Abebe Azime and S. Muhammad and Chris C. Emezue and Joyce Nakatumba-Nabende and Perez Ogayo and 
  Anuoluwapo Aremu and Catherine Gitau and Derguene Mbaye and J. Alabi and Seid Muhie Yimam and Tajuddeen R. Gwadabe and
  Ignatius Ezeani and Rubungo Andre Niyongabo and Jonathan Mukiibi and V. Otiende and Iroro Orife and Davis David and 
  Samba Ngom and Tosin P. Adewumi and Paul Rayson and Mofetoluwa Adeyemi and Gerald Muriuki and Emmanuel Anebi and 
  C. Chukwuneke and N. Odu and Eric Peter Wairagala and S. Oyerinde and Clemencia Siro and Tobius Saul Bateesa and 
  Temilola Oloyede and Yvonne Wambui and Victor Akinode and Deborah Nabagereka and Maurice Katusiime and 
  Ayodele Awokoya and Mouhamadane Mboup and D. Gebreyohannes and Henok Tilaye and Kelechi Nwaike and Degaga Wolde and
   Abdoulaye Faye and Blessing Sibanda and Orevaoghene Ahia and Bonaventure F. P. Dossou and Kelechi Ogueji and 
   Thierno Ibrahima Diop and A. Diallo and Adewale Akinfaderin and T. Marengereke and Salomey Osei},
  journal={ArXiv},
  year={2021},
  volume={abs/2103.11811}
}
```

### Contributions

Thanks to [@dadelani](https://github.com/dadelani) for adding this dataset.
