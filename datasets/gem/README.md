---
annotations_creators:
  common_gen:
  - crowdsourced
  - found
  cs_restaurants:
  - crowdsourced
  - found
  dart:
  - crowdsourced
  - found
  e2e_nlg:
  - crowdsourced
  - found
  mlsum_de:
  - found
  mlsum_es:
  - found
  schema_guided_dialog:
  - crowdsourced
  totto:
  - crowdsourced
  - found
  web_nlg_en:
  - crowdsourced
  - found
  web_nlg_ru:
  - crowdsourced
  - found
  wiki_auto_asset_turk:
  - crowdsourced
  - found
  wiki_lingua_es_en:
  - found
  wiki_lingua_ru_en:
  - found
  wiki_lingua_tr_en:
  - found
  wiki_lingua_vi_en:
  - found
  xsum:
  - found
language_creators:
  common_gen:
  - found
  cs_restaurants:
  - found
  dart:
  - found
  e2e_nlg:
  - found
  mlsum_de:
  - found
  mlsum_es:
  - found
  schema_guided_dialog:
  - crowdsourced
  - machine-generated
  totto:
  - found
  web_nlg_en:
  - found
  web_nlg_ru:
  - found
  wiki_auto_asset_turk:
  - found
  wiki_lingua_es_en:
  - found
  wiki_lingua_ru_en:
  - found
  wiki_lingua_tr_en:
  - found
  wiki_lingua_vi_en:
  - found
  xsum:
  - found
languages:
  common_gen:
  - en
  cs_restaurants:
  - cs
  dart:
  - en
  e2e_nlg:
  - en
  mlsum_de:
  - de
  mlsum_es:
  - es
  schema_guided_dialog:
  - en
  totto:
  - en
  web_nlg_en:
  - en
  web_nlg_ru:
  - ru
  wiki_auto_asset_turk:
  - en
  wiki_lingua_es_en:
  - en
  - es
  wiki_lingua_ru_en:
  - en
  - ru
  wiki_lingua_tr_en:
  - en
  - tr
  wiki_lingua_vi_en:
  - en
  - vi
  xsum:
  - en
licenses:
- other-research-only
multilinguality:
  common_gen:
  - monolingual
  cs_restaurants:
  - monolingual
  dart:
  - monolingual
  e2e_nlg:
  - monolingual
  mlsum_de:
  - monolingual
  mlsum_es:
  - monolingual
  schema_guided_dialog:
  - monolingual
  totto:
  - monolingual
  web_nlg_en:
  - monolingual
  web_nlg_ru:
  - monolingual
  wiki_auto_asset_turk:
  - monolingual
  wiki_lingua_es_en:
  - multilingual
  wiki_lingua_ru_en:
  - multilingual
  wiki_lingua_tr_en:
  - multilingual
  wiki_lingua_vi_en:
  - multilingual
  xsum:
  - monolingual
size_categories:
  common_gen:
  - 10K<n<100K
  cs_restaurants:
  - 1K<n<10K
  dart:
  - 10K<n<100K
  e2e_nlg:
  - 10K<n<100K
  mlsum_de:
  - 100K<n<1M
  mlsum_es:
  - 100K<n<1M
  schema_guided_dialog:
  - 100K<n<1M
  totto:
  - 100K<n<1M
  web_nlg_en:
  - 10K<n<100K
  web_nlg_ru:
  - 10K<n<100K
  wiki_auto_asset_turk:
  - 100K<n<1M
  wiki_lingua_es_en:
  - 100K<n<1M
  wiki_lingua_ru_en:
  - 10K<n<100K
  wiki_lingua_tr_en:
  - 1K<n<10K
  wiki_lingua_vi_en:
  - 10K<n<100K
  xsum:
  - 10K<n<100K
source_datasets:
  common_gen:
  - extended|other-vision-datasets
  - original
  cs_restaurants:
  - original
  dart:
  - original
  e2e_nlg:
  - original
  mlsum_de:
  - original
  mlsum_es:
  - original
  schema_guided_dialog:
  - original
  totto:
  - original
  web_nlg_en:
  - original
  web_nlg_ru:
  - original
  wiki_auto_asset_turk:
  - original
  wiki_lingua_es_en:
  - original
  wiki_lingua_ru_en:
  - original
  wiki_lingua_tr_en:
  - original
  wiki_lingua_vi_en:
  - original
  xsum:
  - original
task_categories:
  common_gen:
  - conditional-text-generation
  cs_restaurants:
  - conditional-text-generation
  dart:
  - conditional-text-generation
  e2e_nlg:
  - conditional-text-generation
  mlsum_de:
  - conditional-text-generation
  mlsum_es:
  - conditional-text-generation
  schema_guided_dialog:
  - sequence-modeling
  totto:
  - conditional-text-generation
  web_nlg_en:
  - conditional-text-generation
  web_nlg_ru:
  - conditional-text-generation
  wiki_auto_asset_turk:
  - conditional-text-generation
  wiki_lingua_es_en:
  - conditional-text-generation
  wiki_lingua_ru_en:
  - conditional-text-generation
  wiki_lingua_tr_en:
  - conditional-text-generation
  wiki_lingua_vi_en:
  - conditional-text-generation
  xsum:
  - conditional-text-generation
task_ids:
  common_gen:
  - other-stuctured-to-text
  cs_restaurants:
  - other-stuctured-to-text
  dart:
  - other-stuctured-to-text
  e2e_nlg:
  - other-stuctured-to-text
  mlsum_de:
  - summarization
  mlsum_es:
  - summarization
  schema_guided_dialog:
  - dialogue-modeling
  totto:
  - table-to-text
  web_nlg_en:
  - other-stuctured-to-text
  web_nlg_ru:
  - other-stuctured-to-text
  wiki_auto_asset_turk:
  - text-simplification
  wiki_lingua_es_en:
  - summarization
  wiki_lingua_ru_en:
  - summarization
  wiki_lingua_tr_en:
  - summarization
  wiki_lingua_vi_en:
  - summarization
  xsum:
  - summarization
---

# Dataset Card for "gem"

## Table of Contents
- [Dataset Description](#dataset-description)
  - [Dataset Summary](#dataset-summary)
  - [Supported Tasks](#supported-tasks)
  - [Languages](#languages)
- [Dataset Structure](#dataset-structure)
  - [Data Instances](#data-instances)
  - [Data Fields](#data-fields)
  - [Data Splits Sample Size](#data-splits-sample-size)
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

## [Dataset Description](#dataset-description)

- **Homepage:** [https://gem-benchmark.github.io/](https://gem-benchmark.github.io/)
- **Repository:**
- **Paper:**
- **Point of Contact:** [Sebastian Gehrman](gehrmann@google.com)
- **Size of downloaded dataset files:** 2084.23 MB
- **Size of the generated dataset:** 3734.73 MB
- **Total amount of disk used:** 5818.96 MB

### [Dataset Summary](#dataset-summary)

GEM is a benchmark environment for Natural Language Generation with a focus on its Evaluation,
both through human annotations and automated Metrics.

GEM aims to:
- measure NLG progress across 13 datasets spanning many NLG tasks and languages.
- provide an in-depth analysis of data and models presented via data statements and challenge sets.
- develop standards for evaluation of generated text using both automated and human metrics.

It is our goal to regularly update GEM and to encourage toward more inclusive practices in dataset development
by extending existing data or developing datasets for additional languages.

You can find more complete information in the dataset cards for each of the subsets:
- [CommonGen](https://gem-benchmark.github.io/data_cards/CommonGen)
- [Czech Restaurant](https://gem-benchmark.github.io/data_cards/Czech%20Restaurant)
- [DART](https://gem-benchmark.github.io/data_cards/DART)
- [E2E](https://gem-benchmark.github.io/data_cards/E2E)
- [MLSum](https://gem-benchmark.github.io/data_cards/MLSum)
- [Schema-Guided Dialog](https://gem-benchmark.github.io/data_cards/Schema-Guided%20DIalog)
- [WebNLG](https://gem-benchmark.github.io/data_cards/WebNLG)
- [Wiki-Auto](https://gem-benchmark.github.io/data_cards/Wiki-Auto)/[ASSET](https://gem-benchmark.github.io/data_cards/ASSET)/[TURK](https://gem-benchmark.github.io/data_cards/TURK)
- [WikiLingua](https://gem-benchmark.github.io/data_cards/WikiLingua)
- [XSum](https://gem-benchmark.github.io/data_cards/XSum)

The subsets are organized by task:
```
{
    "summarization": {
        "mlsum": ["mlsum_de", "mlsum_es"],
        "wiki_lingua": ["wiki_lingua_es_en", "wiki_lingua_ru_en", "wiki_lingua_tr_en", "wiki_lingua_vi_en"],
        "xsum": ["xsum"],
    },
    "struct2text": {
        "common_gen": ["common_gen"],
        "cs_restaurants": ["cs_restaurants"],
        "dart": ["dart"],
        "e2e": ["e2e_nlg"],
        "totto": ["totto"],
        "web_nlg": ["web_nlg_en", "web_nlg_ru"],
    },
    "simplification": {
        "wiki_auto_asset_turk": ["wiki_auto_asset_turk"],
    },
    "dialog": {
        "schema_guided_dialog": ["schema_guided_dialog"],
    },
}
```

Each example has one `target` per example in its training set, and a set of `references` (with one or more items) in its validation and test set.

### [Supported Tasks](#supported-tasks)

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### [Languages](#languages)

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

## [Dataset Structure](#dataset-structure)

We show detailed information for up to 5 configurations of the dataset.

### [Data Instances](#data-instances)

#### common_gen

- **Size of downloaded dataset files:** 1.76 MB
- **Size of the generated dataset:** 8.80 MB
- **Total amount of disk used:** 10.56 MB

An example of `validation` looks as follows.
```
{'concept_set_id': 0,
 'concepts': ['field', 'look', 'stand'],
 'gem_id': 'common_gen-validation-0',
 'references': ['The player stood in the field looking at the batter.',
                'The coach stands along the field, looking at the goalkeeper.',
                'I stood and looked across the field, peacefully.',
                'Someone stands, looking around the empty field.'],
 'target': 'The player stood in the field looking at the batter.'}
```

#### cs_restaurants

- **Size of downloaded dataset files:** 1.40 MB
- **Size of the generated dataset:** 1.25 MB
- **Total amount of disk used:** 2.64 MB

An example of `validation` looks as follows.
```
{'dialog_act': '?request(area)',
 'dialog_act_delexicalized': '?request(area)',
 'gem_id': 'cs_restaurants-validation-0',
 'references': ['Jakou lokalitu hledáte ?'],
 'target': 'Jakou lokalitu hledáte ?',
 'target_delexicalized': 'Jakou lokalitu hledáte ?'}
```

#### dart

- **Size of downloaded dataset files:** 28.01 MB
- **Size of the generated dataset:** 26.17 MB
- **Total amount of disk used:** 54.18 MB

An example of `validation` looks as follows.
```
{'dart_id': 0,
 'gem_id': 'dart-validation-0',
 'references': ['A school from Mars Hill, North Carolina, joined in 1973.'],
 'subtree_was_extended': True,
 'target': 'A school from Mars Hill, North Carolina, joined in 1973.',
 'target_sources': ['WikiSQL_decl_sents'],
 'tripleset': [['Mars Hill College', 'JOINED', '1973'], ['Mars Hill College', 'LOCATION', 'Mars Hill, North Carolina']]}
```

#### e2e_nlg

- **Size of downloaded dataset files:** 13.92 MB
- **Size of the generated dataset:** 11.58 MB
- **Total amount of disk used:** 25.50 MB

An example of `validation` looks as follows.
```
{'gem_id': 'e2e_nlg-validation-0',
 'meaning_representation': 'name[Alimentum], area[city centre], familyFriendly[no]',
 'references': ['There is a place in the city centre, Alimentum, that is not family-friendly.'],
 'target': 'There is a place in the city centre, Alimentum, that is not family-friendly.'}
```

#### mlsum_de

- **Size of downloaded dataset files:** 331.27 MB
- **Size of the generated dataset:** 907.00 MB
- **Total amount of disk used:** 1238.27 MB

An example of `validation` looks as follows.
```
{'date': '00/04/2019',
 'gem_id': 'mlsum_de-validation-0',
 'references': ['In einer Kleinstadt auf der Insel Usedom war eine junge Frau tot in ihrer Wohnung gefunden worden. Nun stehen zwei Bekannte unter Verdacht.'],
 'target': 'In einer Kleinstadt auf der Insel Usedom war eine junge Frau tot in ihrer Wohnung gefunden worden. Nun stehen zwei Bekannte unter Verdacht.',
 'text': 'Kerzen und Blumen stehen vor dem Eingang eines Hauses, in dem eine 18-jährige Frau tot aufgefunden wurde. In einer Kleinstadt auf der Insel Usedom war eine junge Frau tot in ...',
 'title': 'Tod von 18-Jähriger auf Usedom: Zwei Festnahmen',
 'topic': 'panorama',
 'url': 'https://www.sueddeutsche.de/panorama/usedom-frau-tot-festnahme-verdaechtige-1.4412256'}
```

#### mlsum_es

- **Size of downloaded dataset files:** 490.29 MB
- **Size of the generated dataset:** 1253.63 MB
- **Total amount of disk used:** 1743.92 MB

An example of `validation` looks as follows.
```
{'date': '05/01/2019',
 'gem_id': 'mlsum_es-validation-0',
 'references': ['El diseñador que dio carta de naturaleza al estilo genuinamente americano celebra el medio siglo de su marca entre grandes fastos y problemas financieros. Conectar con las nuevas generaciones es el regalo que precisa más que nunca'],
 'target': 'El diseñador que dio carta de naturaleza al estilo genuinamente americano celebra el medio siglo de su marca entre grandes fastos y problemas financieros. Conectar con las nuevas generaciones es el regalo que precisa más que nunca',
 'text': 'Un oso de peluche marcándose un heelflip de monopatín es todo lo que Ralph Lauren necesitaba esta Navidad. Estampado en un jersey de lana azul marino, supone la guinda que corona ...',
 'title': 'Ralph Lauren busca el secreto de la eterna juventud',
 'topic': 'elpais estilo',
 'url': 'http://elpais.com/elpais/2019/01/04/estilo/1546617396_933318.html'}
```

#### schema_guided_dialog

- **Size of downloaded dataset files:** 8.24 MB
- **Size of the generated dataset:** 43.66 MB
- **Total amount of disk used:** 51.91 MB

An example of `validation` looks as follows.
```
{'dialog_acts': [{'act': 2, 'slot': 'song_name', 'values': ['Carnivore']}, {'act': 2, 'slot': 'playback_device', 'values': ['TV']}],
 'dialog_id': '10_00054',
 'gem_id': 'schema_guided_dialog-validation-0',
 'prompt': 'Yes, I would.',
 'references': ['Please confirm the song Carnivore on tv.'],
 'target': 'Please confirm the song Carnivore on tv.',
 'turn_id': 15}
```

#### totto

- **Size of downloaded dataset files:** 179.03 MB
- **Size of the generated dataset:** 722.88 MB
- **Total amount of disk used:** 901.91 MB

An example of `validation` looks as follows.
```
{'example_id': '7391450717765563190',
 'gem_id': 'totto-validation-0',
 'highlighted_cells': [[3, 0], [3, 2], [3, 3]],
 'overlap_subset': 'True',
 'references': ['Daniel Henry Chamberlain was the 76th Governor of South Carolina from 1874.',
                'Daniel Henry Chamberlain was the 76th Governor of South Carolina, beginning in 1874.',
                'Daniel Henry Chamberlain was the 76th Governor of South Carolina who took office in 1874.'],
 'sentence_annotations': [{'final_sentence': 'Daniel Henry Chamberlain was the 76th Governor of South Carolina from 1874.',
                           'original_sentence': 'Daniel Henry Chamberlain (June 23, 1835 – April 13, 1907) was an American planter, lawyer, author and the 76th Governor of South Carolina '
                                                'from 1874 until 1877.',
                           'sentence_after_ambiguity': 'Daniel Henry Chamberlain was the 76th Governor of South Carolina from 1874.',
                           'sentence_after_deletion': 'Daniel Henry Chamberlain was the 76th Governor of South Carolina from 1874.'},
                          ...
                          ],
 'table': [[{'column_span': 1, 'is_header': True, 'row_span': 1, 'value': '#'},
            {'column_span': 2, 'is_header': True, 'row_span': 1, 'value': 'Governor'},
            {'column_span': 1, 'is_header': True, 'row_span': 1, 'value': 'Took Office'},
            {'column_span': 1, 'is_header': True, 'row_span': 1, 'value': 'Left Office'}],
           [{'column_span': 1, 'is_header': True, 'row_span': 1, 'value': '74'},
            {'column_span': 1, 'is_header': False, 'row_span': 1, 'value': '-'},
            {'column_span': 1, 'is_header': False, 'row_span': 1, 'value': 'Robert Kingston Scott'},
            {'column_span': 1, 'is_header': False, 'row_span': 1, 'value': 'July 6, 1868'}],
           ...
          ],
 'table_page_title': 'List of Governors of South Carolina',
 'table_section_text': 'Parties Democratic Republican',
 'table_section_title': 'Governors under the Constitution of 1868',
 'table_webpage_url': 'http://en.wikipedia.org/wiki/List_of_Governors_of_South_Carolina',
 'target': 'Daniel Henry Chamberlain was the 76th Governor of South Carolina from 1874.',
 'totto_id': 0}
```

#### web_nlg_en

- **Size of downloaded dataset files:** 12.35 MB
- **Size of the generated dataset:** 13.95 MB
- **Total amount of disk used:** 26.29 MB

An example of `validation` looks as follows.
```
{'category': 'Airport',
 'gem_id': 'web_nlg_en-validation-0',
 'input': ['Aarhus | leader | Jacob_Bundsgaard'],
 'references': ['The leader of Aarhus is Jacob Bundsgaard.'],
 'target': 'The leader of Aarhus is Jacob Bundsgaard.',
 'webnlg_id': 'dev/Airport/1/Id1'}
```

#### web_nlg_ru

- **Size of downloaded dataset files:** 7.28 MB
- **Size of the generated dataset:** 8.02 MB
- **Total amount of disk used:** 15.30 MB

An example of `validation` looks as follows.
```
{'category': 'Airport',
 'gem_id': 'web_nlg_ru-validation-0',
 'input': ['Punjab,_Pakistan | leaderTitle | Provincial_Assembly_of_the_Punjab'],
 'references': ['Пенджаб, Пакистан, возглавляется Провинциальной ассамблеей Пенджаба.', 'Пенджаб, Пакистан возглавляется Провинциальной ассамблеей Пенджаба.'],
 'target': 'Пенджаб, Пакистан, возглавляется Провинциальной ассамблеей Пенджаба.',
 'webnlg_id': 'dev/Airport/1/Id1'}
```

#### wiki_auto_asset_turk

- **Size of downloaded dataset files:** 121.37 MB
- **Size of the generated dataset:** 145.69 MB
- **Total amount of disk used:** 267.07 MB

An example of `validation` looks as follows.
```
{'gem_id': 'wiki_auto_asset_turk-validation-0',
 'references': ['The Gandalf Awards honor excellent writing in in fantasy literature.'],
 'source': 'The Gandalf Awards, honoring achievement in fantasy literature, were conferred by the World Science Fiction Society annually from 1974 to 1981.',
 'source_id': '350_691837-1-0-0',
 'target': 'The Gandalf Awards honor excellent writing in in fantasy literature.',
 'target_id': '350_691837-0-0-0'}
```

#### wiki_lingua_es_en

- **Size of downloaded dataset files:** 161.56 MB
- **Size of the generated dataset:** 274.28 MB
- **Total amount of disk used:** 435.84 MB

An example of `validation` looks as follows.
```
'references': ["Practice matted hair prevention from early in your cat's life. Make sure that your cat is grooming itself effectively. Keep a close eye on cats with long hair."],
'source': 'Muchas personas presentan problemas porque no cepillaron el pelaje de sus gatos en una etapa temprana de su vida, ya que no lo consideraban necesario. Sin embargo, a medida que...',
'target': "Practice matted hair prevention from early in your cat's life. Make sure that your cat is grooming itself effectively. Keep a close eye on cats with long hair."}
```

#### wiki_lingua_ru_en

- **Size of downloaded dataset files:** 161.56 MB
- **Size of the generated dataset:** 201.43 MB
- **Total amount of disk used:** 362.99 MB

An example of `validation` looks as follows.
```
{'gem_id': 'wiki_lingua_ru_en-val-0',
 'references': ['Get immediate medical care if you notice signs of a complication. Undergo diagnostic tests to check for gallstones and complications. Ask your doctor about your treatment '
                'options.'],
 'source': 'И хотя, скорее всего, вам не о чем волноваться, следует незамедлительно обратиться к врачу, если вы подозреваете, что у вас возникло осложнение желчекаменной болезни. Это ...',
 'target': 'Get immediate medical care if you notice signs of a complication. Undergo diagnostic tests to check for gallstones and complications. Ask your doctor about your treatment '
           'options.'}
```

#### wiki_lingua_tr_en

- **Size of downloaded dataset files:** 161.56 MB
- **Size of the generated dataset:** 9.87 MB
- **Total amount of disk used:** 171.42 MB

An example of `validation` looks as follows.
```
{'gem_id': 'wiki_lingua_tr_en-val-0',
 'references': ['Open Instagram. Go to the video you want to download. Tap ⋮. Tap Copy Link. Open  Google Chrome. Tap the address bar. Go to the SaveFromWeb site. Tap the "Paste Instagram Video" text box. Tap and hold the text box. Tap PASTE. Tap Download. Download the video. Find the video on your Android.'],
 'source': 'Instagram uygulamasının çok renkli kamera şeklindeki simgesine dokun. Daha önce giriş yaptıysan Instagram haber kaynağı açılır. Giriş yapmadıysan istendiğinde e-posta adresini ...',
 'target': 'Open Instagram. Go to the video you want to download. Tap ⋮. Tap Copy Link. Open  Google Chrome. Tap the address bar. Go to the SaveFromWeb site. Tap the "Paste Instagram Video" text box. Tap and hold the text box. Tap PASTE. Tap Download. Download the video. Find the video on your Android.'}
```

#### wiki_lingua_vi_en

- **Size of downloaded dataset files:** 161.56 MB
- **Size of the generated dataset:** 39.12 MB
- **Total amount of disk used:** 200.68 MB

An example of `validation` looks as follows.
```
{'gem_id': 'wiki_lingua_vi_en-val-0',
 'references': ['Select the right time of year for planting the tree. You will usually want to plant your tree when it is dormant, or not flowering, during cooler or colder times of year.'],
 'source': 'Bạn muốn cung cấp cho cây cơ hội tốt nhất để phát triển và sinh tồn. Trồng cây đúng thời điểm trong năm chính là yếu tố then chốt. Thời điểm sẽ thay đổi phụ thuộc vào loài cây ...',
 'target': 'Select the right time of year for planting the tree. You will usually want to plant your tree when it is dormant, or not flowering, during cooler or colder times of year.'}
```

#### xsum

- **Size of downloaded dataset files:** 243.08 MB
- **Size of the generated dataset:** 67.40 MB
- **Total amount of disk used:** 310.48 MB

An example of `validation` looks as follows.
```
{'document': 'Burberry reported pre-tax profits of £166m for the year to March. A year ago it made a loss of £16.1m, hit by charges at its Spanish operations.\n'
             'In the past year it has opened 21 new stores and closed nine. It plans to open 20-30 stores this year worldwide.\n'
             'The group has also focused on promoting the Burberry brand online...',
 'gem_id': 'xsum-validation-0',
 'references': ['Luxury fashion designer Burberry has returned to profit after opening new stores and spending more on online marketing'],
 'target': 'Luxury fashion designer Burberry has returned to profit after opening new stores and spending more on online marketing',
 'xsum_id': '10162122'}
```

### [Data Fields](#data-fields)

The data fields are the same among all splits.

#### common_gen
- `gem_id`: a `string` feature.
- `concept_set_id`: a `int32` feature.
- `concepts`: a `list` of `string` features.
- `target`: a `string` feature.
- `references`: a `list` of `string` features.

#### cs_restaurants
- `gem_id`: a `string` feature.
- `dialog_act`: a `string` feature.
- `dialog_act_delexicalized`: a `string` feature.
- `target_delexicalized`: a `string` feature.
- `target`: a `string` feature.
- `references`: a `list` of `string` features.

#### dart
- `gem_id`: a `string` feature.
- `dart_id`: a `int32` feature.
- `tripleset`: a `list` of `string` features.
- `subtree_was_extended`: a `bool` feature.
- `target_sources`: a `list` of `string` features.
- `target`: a `string` feature.
- `references`: a `list` of `string` features.

#### e2e_nlg
- `gem_id`: a `string` feature.
- `meaning_representation`: a `string` feature.
- `target`: a `string` feature.
- `references`: a `list` of `string` features.

#### mlsum_de
- `gem_id`: a `string` feature.
- `text`: a `string` feature.
- `topic`: a `string` feature.
- `url`: a `string` feature.
- `title`: a `string` feature.
- `date`: a `string` feature.
- `target`: a `string` feature.
- `references`: a `list` of `string` features.

#### mlsum_es
- `gem_id`: a `string` feature.
- `text`: a `string` feature.
- `topic`: a `string` feature.
- `url`: a `string` feature.
- `title`: a `string` feature.
- `date`: a `string` feature.
- `target`: a `string` feature.
- `references`: a `list` of `string` features.

#### schema_guided_dialog
- `gem_id`: a `string` feature.
- `act`: a classification label, with possible values including `AFFIRM` (0), `AFFIRM_INTENT` (1), `CONFIRM` (2), `GOODBYE` (3), `INFORM` (4).
- `slot`: a `string` feature.
- `values`: a `list` of `string` features.
- `dialog_id`: a `string` feature.
- `turn_id`: a `int32` feature.
- `prompt`: a `string` feature.
- `target`: a `string` feature.
- `references`: a `list` of `string` features.

#### totto
- `gem_id`: a `string` feature.
- `totto_id`: a `int32` feature.
- `table_page_title`: a `string` feature.
- `table_webpage_url`: a `string` feature.
- `table_section_title`: a `string` feature.
- `table_section_text`: a `string` feature.
- `column_span`: a `int32` feature.
- `is_header`: a `bool` feature.
- `row_span`: a `int32` feature.
- `value`: a `string` feature.
- `highlighted_cells`: a `list` of `int32` features.
- `example_id`: a `string` feature.
- `original_sentence`: a `string` feature.
- `sentence_after_deletion`: a `string` feature.
- `sentence_after_ambiguity`: a `string` feature.
- `final_sentence`: a `string` feature.
- `overlap_subset`: a `string` feature.
- `target`: a `string` feature.
- `references`: a `list` of `string` features.

#### web_nlg_en
- `gem_id`: a `string` feature.
- `input`: a `list` of `string` features.
- `target`: a `string` feature.
- `references`: a `list` of `string` features.
- `category`: a `string` feature.
- `webnlg_id`: a `string` feature.

#### web_nlg_ru
- `gem_id`: a `string` feature.
- `input`: a `list` of `string` features.
- `target`: a `string` feature.
- `references`: a `list` of `string` features.
- `category`: a `string` feature.
- `webnlg_id`: a `string` feature.

#### wiki_auto_asset_turk
- `gem_id`: a `string` feature.
- `source_id`: a `string` feature.
- `target_id`: a `string` feature.
- `source`: a `string` feature.
- `target`: a `string` feature.
- `references`: a `list` of `string` features.

#### wiki_lingua_es_en
- `gem_id`: a `string` feature.
- `source`: a `string` feature.
- `target`: a `string` feature.
- `references`: a `list` of `string` features.

#### wiki_lingua_ru_en
- `gem_id`: a `string` feature.
- `source`: a `string` feature.
- `target`: a `string` feature.
- `references`: a `list` of `string` features.

#### wiki_lingua_tr_en
- `gem_id`: a `string` feature.
- `source`: a `string` feature.
- `target`: a `string` feature.
- `references`: a `list` of `string` features.

#### wiki_lingua_vi_en
- `gem_id`: a `string` feature.
- `source`: a `string` feature.
- `target`: a `string` feature.
- `references`: a `list` of `string` features.

#### xsum
- `gem_id`: a `string` feature.
- `xsum_id`: a `string` feature.
- `document`: a `string` feature.
- `target`: a `string` feature.
- `references`: a `list` of `string` features.

### [Data Splits Sample Size](#data-splits-sample-size)

#### common_gen

|          |train|validation|test|
|----------|----:|---------:|---:|
|common_gen|67389|       993|1497|

#### cs_restaurants

|              |train|validation|test|
|--------------|----:|---------:|---:|
|cs_restaurants| 3569|       781| 842|

#### dart

|    |train|validation|test|
|----|----:|---------:|---:|
|dart|62659|      2768|6959|

#### e2e_nlg

|       |train|validation|test|
|-------|----:|---------:|---:|
|e2e_nlg|33525|      4299|4693|

#### mlsum_de

|        |train |validation|test |
|--------|-----:|---------:|----:|
|mlsum_de|220748|     11392|10695|

#### mlsum_es

|        |train |validation|test |
|--------|-----:|---------:|----:|
|mlsum_es|259886|      9977|13365|

#### schema_guided_dialog

|                    |train |validation|test |
|--------------------|-----:|---------:|----:|
|schema_guided_dialog|164982|     10000|10000|

#### totto

|     |train |validation|test|
|-----|-----:|---------:|---:|
|totto|121153|      7700|7700|

#### web_nlg_en

|          |train|validation|test|
|----------|----:|---------:|---:|
|web_nlg_en|35426|      1667|1779|

#### web_nlg_ru

|          |train|validation|test|
|----------|----:|---------:|---:|
|web_nlg_ru|14630|       790|1102|

#### wiki_auto_asset_turk

|                    |train |validation|test_asset|test_turk|
|--------------------|-----:|---------:|---------:|--------:|
|wiki_auto_asset_turk|373801|     73249|       359|      359|

#### wiki_lingua_es_en

|                 |train|validation|test |
|-----------------|----:|---------:|----:|
|wiki_lingua_es_en|79515|      8835|19797|

#### wiki_lingua_ru_en

|                 |train|validation|test|
|-----------------|----:|---------:|---:|
|wiki_lingua_ru_en|36898|      4100|9094|

#### wiki_lingua_tr_en

|                 |train|validation|test|
|-----------------|----:|---------:|---:|
|wiki_lingua_tr_en| 3193|       355| 808|

#### wiki_lingua_vi_en

|                 |train|validation|test|
|-----------------|----:|---------:|---:|
|wiki_lingua_vi_en| 9206|      1023|2167|

#### xsum

|    |train|validation|test|
|----|----:|---------:|---:|
|xsum|23206|      1117|1166|

## [Dataset Creation](#dataset-creation)

### [Curation Rationale](#curation-rationale)

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### [Source Data](#source-data)

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### [Annotations](#annotations)

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### [Personal and Sensitive Information](#personal-and-sensitive-information)

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

## [Considerations for Using the Data](#considerations-for-using-the-data)

### [Social Impact of Dataset](#social-impact-of-dataset)

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### [Discussion of Biases](#discussion-of-biases)

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### [Other Known Limitations](#other-known-limitations)

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

## [Additional Information](#additional-information)

### [Dataset Curators](#dataset-curators)

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### [Licensing Information](#licensing-information)

CC-BY-SA-4.0

### [Citation Information](#citation-information)

```
@InProceedings{acl:gem,
title = {The GEM Benchmark:Natural Language Generation, its Evaluation and Metrics},
authors={Sebastian Gehrmann et al.},
year={2021}
}

```

### Contributions

Thanks to [@yjernite](https://github.com/yjernite) for adding this dataset.