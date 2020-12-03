---
annotations_creators:
  mlqa:
  - crowdsourced
  nc:
  - machine-generated
  ner:
  - expert-generated
  - found
  ntg:
  - machine-generated
  paws-x:
  - expert-generated
  pos:
  - expert-generated
  - found
  qadsm:
  - machine-generated
  qam:
  - machine-generated
  qg:
  - machine-generated
  wpr:
  - machine-generated
  xnli:
  - machine-generated
language_creators:
  mlqa:
  - found
  nc:
  - found
  ner:
  - crowdsourced
  - expert-generated
  ntg:
  - machine-generated
  paws-x:
  - expert-generated
  pos:
  - crowdsourced
  - expert-generated
  qadsm:
  - found
  qam:
  - found
  qg:
  - machine-generated
  wpr:
  - found
  xnli:
  - crowdsourced
  - expert-generated
languages:
  mlqa:
  - ar
  - de
  - en
  - es
  - hi
  - vi
  - zh
  nc:
  - en
  - de
  - es
  - fr
  - ru
  ner:
  - de
  - en
  - es
  - nl
  ntg:
  - en
  - de
  - es
  - fr
  - ru
  paws-x:
  - en
  - de
  - es
  - fr
  pos:
  - ar
  - bg
  - de
  - el
  - en
  - es
  - fr
  - hi
  - it
  - nl
  - pl
  - ru
  - th
  - tr
  - ur
  - vi
  - zh
  qadsm:
  - en
  - de
  - fr
  qam:
  - en
  - de
  - fr
  qg:
  - en
  - de
  - fr
  - pt
  - it
  - zh
  wpr:
  - en
  - de
  - fr
  - es
  - it
  - pt
  - zh
  xnli:
  - ar
  - bg
  - de
  - el
  - en
  - es
  - fr
  - hi
  - ru
  - sw
  - th
  - tr
  - ur
  - vi
  - zh
licenses:
  mlqa:
  - cc-by-sa-4.0
  nc:
  - unknown
  ner:
  - unknown
  ntg:
  - unknown
  paws-x:
  - unknown
  pos:
  - other-Licence Universal Dependencies v2.5
  qadsm:
  - unknown
  qam:
  - unknown
  qg:
  - unknown
  wpr:
  - unknown
  xnli:
  - cc-by-nc-4.0
multilinguality:
  mlqa:
  - multilingual
  nc:
  - multilingual
  ner:
  - multilingual
  ntg:
  - multilingual
  paws-x:
  - multilingual
  pos:
  - multilingual
  qadsm:
  - multilingual
  qam:
  - multilingual
  qg:
  - multilingual
  wpr:
  - multilingual
  xnli:
  - multilingual
  - translation
size_categories:
  mlqa:
  - 100K<n<1M
  nc:
  - 100K<n<1M
  ner:
  - 10K<n<100K
  ntg:
  - 100K<n<1M
  paws-x:
  - 10K<n<100K
  pos:
  - 10K<n<100K
  qadsm:
  - 100K<n<1M
  qam:
  - 100K<n<1M
  qg:
  - 100K<n<1M
  wpr:
  - 100K<n<1M
  xnli:
  - 100K<n<1M
source_datasets:
  mlqa:
  - extended|squad
  nc:
  - original
  ner:
  - extended|conll2003
  ntg:
  - original
  paws-x:
  - original
  pos: 
  - original
  qadsm:
  - original
  qam:
  - original
  qg:
  - original
  wpr:
  - original
  xnli:
  - extended|xnli
task_categories:
  mlqa:
  - question-answering
  nc:
  - text-classification
  ner:
  - structure-prediction
  ntg:
  - conditional-text-generation
  paws-x:
  - text-classification
  pos:
  - structure-prediction
  qadsm:
  - text-classification
  qam:
  - text-classification
  qg:
  - conditional-text-generation
  wpr:
  - text-classification
  xnli:
  - text-classification
task_ids:
  mlqa:
  - extractive-qa
  - open-domain-qa
  nc:
  - topic-classification
  ner:
  - named-entity-recognition
  ntg:
  - summarization
  paws-x:
  - text-classification-other-paraphrase identification
  pos:
  - parsing
  qadsm:
  - acceptability-classification
  qam:
  - acceptability-classification
  qg:
  - conditional-text-generation-other-question-answering
  wpr:
  - acceptability-classification
  xnli:
  - natural-language-inference
---

# Dataset Card for XGLUE

## Table of Contents
- [Dataset Description](#dataset-description)
  - [Dataset Summary](#dataset-summary)
  - [Leaderboards](#leaderboards)
- [Dataset Structure](#dataset-structure)
  - [Data Instances](#data-instances)
  - [Data Fields](#data-instances)
  - [Data Splits](#data-instances)
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

## Dataset Description

- **Homepage:** [XGLUE homepage](https://microsoft.github.io/XGLUE/)
- **Paper:** [XGLUE: A New Benchmark Dataset for Cross-lingual Pre-training, Understanding and Generation](https://arxiv.org/abs/1907.09190)

### Dataset Summary

XGLUE is a new benchmark dataset to evaluate the performance of cross-lingual pre-trained models with respect to cross-lingual natural language understanding and generation. 

The training data of each task is in English while the validation and test data is present in multiple different languages.
The following table shows which languages are present as validation and test data for each config.

![Available Languages for Test and Validation Data](https://raw.githubusercontent.com/patrickvonplaten/scientific_images/master/xglue_langs.png)

Therefore, for each config, a cross-lingual pre-trained model should be fine-tuned on the English training data, and evaluated on for all languages.

### Leaderboards

The XGLUE leaderboard can be found on the [homepage](https://microsoft.github.io/XGLUE/) and 
consits of a XGLUE-Understanding Score (the average of the tasks `ner`, `pos`, `mlqa`, `nc`, `xnli`, `paws-x`, `qadsm`, `wpr`, `qam`) and a XGLUE-Generation Score (the average of the tasks `qg`, `ntg`).

## Dataset Structure

### Data Instances

#### ner

An example of 'test.nl' looks as follows.

```
{
  "ner": [
    "O",
    "O",
    "O",
    "B-LOC",
    "O",
    "B-LOC",
    "O",
    "B-LOC",
    "O",
    "O",
    "O",
    "O",
    "O",
    "O",
    "O",
    "B-PER",
    "I-PER",
    "O",
    "O",
    "B-LOC",
    "O",
    "O"
  ],
  "words": [
    "Dat",
    "is",
    "in",
    "Itali\u00eb",
    ",",
    "Spanje",
    "of",
    "Engeland",
    "misschien",
    "geen",
    "probleem",
    ",",
    "maar",
    "volgens",
    "'",
    "Der",
    "Kaiser",
    "'",
    "in",
    "Duitsland",
    "wel",
    "."
  ]
}
```

#### pos

An example of 'test.fr' looks as follows.

```
{
  "pos": [
    "PRON",
    "VERB",
    "SCONJ",
    "ADP",
    "PRON",
    "CCONJ",
    "DET",
    "NOUN",
    "ADP",
    "NOUN",
    "CCONJ",
    "NOUN",
    "ADJ",
    "PRON",
    "PRON",
    "AUX",
    "ADV",
    "VERB",
    "PUNCT",
    "PRON",
    "VERB",
    "VERB",
    "DET",
    "ADJ",
    "NOUN",
    "ADP",
    "DET",
    "NOUN",
    "PUNCT"
  ],
  "words": [
    "Je",
    "sens",
    "qu'",
    "entre",
    "\u00e7a",
    "et",
    "les",
    "films",
    "de",
    "m\u00e9decins",
    "et",
    "scientifiques",
    "fous",
    "que",
    "nous",
    "avons",
    "d\u00e9j\u00e0",
    "vus",
    ",",
    "nous",
    "pourrions",
    "emprunter",
    "un",
    "autre",
    "chemin",
    "pour",
    "l'",
    "origine",
    "."
  ]
}
```

#### mlqa

An example of 'test.hi' looks as follows.

```
{
  "answers": {
    "answer_start": [
      378
    ],
    "text": [
      "\u0909\u0924\u094d\u0924\u0930 \u092a\u0942\u0930\u094d\u0935"
    ]
  },
  "context": "\u0909\u0938\u0940 \"\u090f\u0930\u093f\u092f\u093e XX \" \u0928\u093e\u092e\u0915\u0930\u0923 \u092a\u094d\u0930\u0923\u093e\u0932\u0940 \u0915\u093e \u092a\u094d\u0930\u092f\u094b\u0917 \u0928\u0947\u0935\u093e\u0926\u093e \u092a\u0930\u0940\u0915\u094d\u0937\u0923 \u0938\u094d\u0925\u0932 \u0915\u0947 \u0905\u0928\u094d\u092f \u092d\u093e\u0917\u094b\u0902 \u0915\u0947 \u0932\u093f\u090f \u0915\u093f\u092f\u093e \u0917\u092f\u093e \u0939\u0948\u0964\u092e\u0942\u0932 \u0930\u0942\u092a \u092e\u0947\u0902 6 \u092c\u091f\u0947 10 \u092e\u0940\u0932 \u0915\u093e \u092f\u0939 \u0906\u092f\u0924\u093e\u0915\u093e\u0930 \u0905\u0921\u094d\u0921\u093e \u0905\u092c \u0924\u0925\u093e\u0915\u0925\u093f\u0924 '\u0917\u094d\u0930\u0942\u092e \u092c\u0949\u0915\u094d\u0938 \" \u0915\u093e \u090f\u0915 \u092d\u093e\u0917 \u0939\u0948, \u091c\u094b \u0915\u093f 23 \u092c\u091f\u0947 25.3 \u092e\u0940\u0932 \u0915\u093e \u090f\u0915 \u092a\u094d\u0930\u0924\u093f\u092c\u0902\u0927\u093f\u0924 \u0939\u0935\u093e\u0908 \u0915\u094d\u0937\u0947\u0924\u094d\u0930 \u0939\u0948\u0964 \u092f\u0939 \u0915\u094d\u0937\u0947\u0924\u094d\u0930 NTS \u0915\u0947 \u0906\u0902\u0924\u0930\u093f\u0915 \u0938\u0921\u093c\u0915 \u092a\u094d\u0930\u092c\u0902\u0927\u0928 \u0938\u0947 \u091c\u0941\u0921\u093c\u093e \u0939\u0948, \u091c\u093f\u0938\u0915\u0940 \u092a\u0915\u094d\u0915\u0940 \u0938\u0921\u093c\u0915\u0947\u0902 \u0926\u0915\u094d\u0937\u093f\u0923 \u092e\u0947\u0902 \u092e\u0930\u0915\u0930\u0940 \u0915\u0940 \u0913\u0930 \u0914\u0930 \u092a\u0936\u094d\u091a\u093f\u092e \u092e\u0947\u0902 \u092f\u0941\u0915\u094d\u0915\u093e \u092b\u094d\u0932\u0948\u091f \u0915\u0940 \u0913\u0930 \u091c\u093e\u0924\u0940 \u0939\u0948\u0902\u0964 \u091d\u0940\u0932 \u0938\u0947 \u0909\u0924\u094d\u0924\u0930 \u092a\u0942\u0930\u094d\u0935 \u0915\u0940 \u0913\u0930 \u092c\u0922\u093c\u0924\u0947 \u0939\u0941\u090f \u0935\u094d\u092f\u093e\u092a\u0915 \u0914\u0930 \u0914\u0930 \u0938\u0941\u0935\u094d\u092f\u0935\u0938\u094d\u0925\u093f\u0924 \u0917\u094d\u0930\u0942\u092e \u091d\u0940\u0932 \u0915\u0940 \u0938\u0921\u093c\u0915\u0947\u0902 \u090f\u0915 \u0926\u0930\u094d\u0930\u0947 \u0915\u0947 \u091c\u0930\u093f\u092f\u0947 \u092a\u0947\u091a\u0940\u0926\u093e \u092a\u0939\u093e\u0921\u093c\u093f\u092f\u094b\u0902 \u0938\u0947 \u0939\u094b\u0915\u0930 \u0917\u0941\u091c\u0930\u0924\u0940 \u0939\u0948\u0902\u0964 \u092a\u0939\u0932\u0947 \u0938\u0921\u093c\u0915\u0947\u0902 \u0917\u094d\u0930\u0942\u092e \u0918\u093e\u091f\u0940",
  "question": "\u091d\u0940\u0932 \u0915\u0947 \u0938\u093e\u092a\u0947\u0915\u094d\u0937 \u0917\u094d\u0930\u0942\u092e \u0932\u0947\u0915 \u0930\u094b\u0921 \u0915\u0939\u093e\u0901 \u091c\u093e\u0924\u0940 \u0925\u0940?"
}
```

#### nc

An example of 'test.es' looks as follows.

```
{
  "news_body": "El bizcocho es seguramente el producto m\u00e1s b\u00e1sico y sencillo de toda la reposter\u00eda : consiste en poco m\u00e1s que mezclar unos cuantos ingredientes, meterlos al horno y esperar a que se hagan. Por obra y gracia del impulsor qu\u00edmico, tambi\u00e9n conocido como \"levadura de tipo Royal\", despu\u00e9s de un rato de calorcito esta combinaci\u00f3n de harina, az\u00facar, huevo, grasa -aceite o mantequilla- y l\u00e1cteo se transforma en uno de los productos m\u00e1s deliciosos que existen para desayunar o merendar . Por muy manazas que seas, es m\u00e1s que probable que tu bizcocho casero supere en calidad a cualquier infamia industrial envasada. Para lograr un bizcocho digno de admiraci\u00f3n s\u00f3lo tienes que respetar unas pocas normas que afectan a los ingredientes, proporciones, mezclado, horneado y desmoldado. Todas las tienes resumidas en unos dos minutos el v\u00eddeo de arriba, en el que adem \u00e1s aprender\u00e1s alg\u00fan truquillo para que tu bizcochaco quede m\u00e1s fino, jugoso, esponjoso y amoroso. M\u00e1s en MSN:",
  "news_category": "foodanddrink",
  "news_title": "Cocina para lerdos: las leyes del bizcocho"
}
```

#### xnli

An example of 'validation.th' looks as follows.

```
{
  "hypothesis": "\u0e40\u0e02\u0e32\u0e42\u0e17\u0e23\u0e2b\u0e32\u0e40\u0e40\u0e21\u0e48\u0e02\u0e2d\u0e07\u0e40\u0e02\u0e32\u0e2d\u0e22\u0e48\u0e32\u0e07\u0e23\u0e27\u0e14\u0e40\u0e23\u0e47\u0e27\u0e2b\u0e25\u0e31\u0e07\u0e08\u0e32\u0e01\u0e17\u0e35\u0e48\u0e23\u0e16\u0e42\u0e23\u0e07\u0e40\u0e23\u0e35\u0e22\u0e19\u0e2a\u0e48\u0e07\u0e40\u0e02\u0e32\u0e40\u0e40\u0e25\u0e49\u0e27",
  "label": 1,
  "premise": "\u0e41\u0e25\u0e30\u0e40\u0e02\u0e32\u0e1e\u0e39\u0e14\u0e27\u0e48\u0e32, \u0e21\u0e48\u0e32\u0e21\u0e4a\u0e32 \u0e1c\u0e21\u0e2d\u0e22\u0e39\u0e48\u0e1a\u0e49\u0e32\u0e19"
}
```

#### paws-x

An example of 'test.es' looks as follows.

```
{
  "label": 1,
  "sentence1": "La excepci\u00f3n fue entre fines de 2005 y 2009 cuando jug\u00f3 en Suecia con Carlstad United BK, Serbia con FK Borac \u010ca\u010dak y el FC Terek Grozny de Rusia.",
  "sentence2": "La excepci\u00f3n se dio entre fines del 2005 y 2009, cuando jug\u00f3 con Suecia en el Carlstad United BK, Serbia con el FK Borac \u010ca\u010dak y el FC Terek Grozny de Rusia."
}
```

#### qadsm

An example of 'train' looks as follows.

```
{
  "ad_description": "Your New England Cruise Awaits! Holland America Line Official Site.",
  "ad_title": "New England Cruises",
  "query": "cruise portland maine",
  "relevance_label": 1
}
```

#### wpr

An example of 'test.zh' looks as follows.

```
{
  "query": "maxpro\u5b98\u7f51",
  "relavance_label": 0,
  "web_page_snippet": "\u5728\u7ebf\u8d2d\u4e70\uff0c\u552e\u540e\u670d\u52a1\u3002vivo\u667a\u80fd\u624b\u673a\u5f53\u5b63\u660e\u661f\u673a\u578b\u6709NEX\uff0cvivo X21\uff0cvivo X20\uff0c\uff0cvivo X23\u7b49\uff0c\u5728vivo\u5b98\u7f51\u8d2d\u4e70\u624b\u673a\u53ef\u4ee5\u4eab\u53d712 \u671f\u514d\u606f\u4ed8\u6b3e\u3002 \u54c1\u724c Funtouch OS \u4f53\u9a8c\u5e97 | ...",
  "wed_page_title": "vivo\u667a\u80fd\u624b\u673a\u5b98\u65b9\u7f51\u7ad9-AI\u975e\u51e1\u6444\u5f71X23"
}
```

#### qam

An example of 'validation.en' looks as follows.

```
{
  "annswer": "Erikson has stated that after the last novel of the Malazan Book of the Fallen was finished, he and Esslemont would write a comprehensive guide tentatively named The Encyclopaedia Malazica.",
  "label": 0,
  "question": "main character of malazan book of the fallen"
}
```

#### qg

An example of 'test.de' looks as follows.

```
{
  "answer_passage": "Medien bei WhatsApp automatisch speichern. Tippen Sie oben rechts unter WhatsApp auf die drei Punkte oder auf die Men\u00fc-Taste Ihres Smartphones. Dort wechseln Sie in die \"Einstellungen\" und von hier aus weiter zu den \"Chat-Einstellungen\". Unter dem Punkt \"Medien Auto-Download\" k\u00f6nnen Sie festlegen, wann die WhatsApp-Bilder heruntergeladen werden sollen.",
  "question": "speichenn von whats app bilder unterbinden"
}
```

#### ntg

An example of 'test.en' looks as follows.

```
{
  "news_body": "Check out this vintage Willys Pickup! As they say, the devil is in the details, and it's not every day you see such attention paid to every last area of a restoration like with this 1961 Willys Pickup . Already the Pickup has a unique look that shares some styling with the Jeep, plus some original touches you don't get anywhere else. It's a classy way to show up to any event, all thanks to Hollywood Motors . A burgundy paint job contrasts with white lower panels and the roof. Plenty of tasteful chrome details grace the exterior, including the bumpers, headlight bezels, crossmembers on the grille, hood latches, taillight bezels, exhaust finisher, tailgate hinges, etc. Steel wheels painted white and chrome hubs are a tasteful addition. Beautiful oak side steps and bed strips add a touch of craftsmanship to this ride. This truck is of real showroom quality, thanks to the astoundingly detailed restoration work performed on it, making this Willys Pickup a fierce contender for best of show. Under that beautiful hood is a 225 Buick V6 engine mated to a three-speed manual transmission, so you enjoy an ideal level of control. Four wheel drive is functional, making it that much more utilitarian and downright cool. The tires are new, so you can enjoy a lot of life out of them, while the wheels and hubs are in great condition. Just in case, a fifth wheel with a tire and a side mount are included. Just as important, this Pickup runs smoothly, so you can go cruising or even hit the open road if you're interested in participating in some classic rallies. You might associate Willys with the famous Jeep CJ, but the automaker did produce a fair amount of trucks. The Pickup is quite the unique example, thanks to distinct styling that really turns heads, making it a favorite at quite a few shows. Source: Hollywood Motors Check These Rides Out Too: Fear No Trails With These Off-Roaders 1965 Pontiac GTO: American Icon For Sale In Canada Low-Mileage 1955 Chevy 3100 Represents Turn In Pickup Market",
  "news_title": "This 1961 Willys Pickup Will Let You Cruise In Style"
}
```

### Data Fields

#### ner

In the following each data field in ner is explained. The data fields are the same among all splits.

- `words`: a list of words composing the sentence.
- `ner`: a list of entitity classes corresponding to each word respectively.


#### pos

In the following each data field in pos is explained. The data fields are the same among all splits.

- `words`: a list of words composing the sentence.
- `pos`: a list of "part-of-speech" classes corresponding to each word respectively.


#### mlqa

In the following each data field in mlqa is explained. The data fields are the same among all splits.

- `context`: a string, the context containing the answer.
- `question`: a string, the question to be answered.
- `answers`: a string, the answer to `question`.


#### nc

In the following each data field in nc is explained. The data fields are the same among all splits.

- `news_title`: a string, to the title of the news report.
- `news_body`: a string, to the actual news report.
- `news_category`: a string, the category of the news report, *e.g.* `foodanddrink`


#### xnli

In the following each data field in xnli is explained. The data fields are the same among all splits.

- `premise`: a string, the context/premise, *i.e.* the first sentence for natural language inference.
- `hypothesis`: a string, a sentence whereas its relation to `premise` is to be classified, *i.e.* the second sentence for natural language inference.
- `label`: a class catory (int), natural language inference relation class between `hypothesis` and `premise`. One of 0: entailment, 1: contradiction, 2: neutral.


#### paws-x

In the following each data field in paws-x is explained. The data fields are the same among all splits.

- `sentence1`: a string, a sentence.
- `sentence2`: a string, a sentence whereas the sentence is either a paraphrase of `sentence1` or not.
- `label`: a class label (int), whether `sentence2` is a paraphrase of `sentence1` One of 0: different, 1: same.


#### qadsm

In the following each data field in qadsm is explained. The data fields are the same among all splits.

- `query`: a string, the search query one would insert into a search engine.
- `ad_title`: a string, the title of the advertisement.
- `ad_description`: a string, the content of the advertisement, *i.e.* the main body.
- `relevance_label`: a class label (int), how relevant the advertisement `ad_title` + `ad_description` is to the search query `query`. One of 0: Bad, 1: Good.


#### wpr

In the following each data field in wpr is explained. The data fields are the same among all splits.

- `query`: a string, the search query one would insert into a search engine.
- `web_page_title`: a string, the title of a web page.
- `web_page_snippet`: a string, the content of a web page, *i.e.* the main body.
- `relavance_label`: a class label (int), how relevant the web page `web_page_snippet` + `web_page_snippet` is to the search query `query`. One of 0: Bad, 1: Fair, 2: Good, 3: Excellent, 4: Perfect.


#### qam

In the following each data field in qam is explained. The data fields are the same among all splits.

- `question`: a string, a question.
- `answer`: a string, a possible answer to `question`.
- `label`: a class label (int), whether the `answer` is relevant to the `question`. One of 0: False, 1: True.


#### qg

In the following each data field in qg is explained. The data fields are the same among all splits.

- `answer_passage`: a string, a detailed answer to the `question`.
- `question`: a string, a question.


#### ntg

In the following each data field in ntg is explained. The data fields are the same among all splits.

- `news_body`: a string, the content of a news article.
- `news_title`: a string, the title corresponding to the news article `news_body`.


### Data Splits

#### ner

The following table shows the number of data samples/number of rows for each split in ner.

|   |train|validation.en|validation.de|validation.es|validation.nl|test.en|test.de|test.es|test.nl|
|---|----:|------------:|------------:|------------:|------------:|------:|------:|------:|------:|
|ner|14042|         3252|         2874|         1923|         2895|   3454|   3007|   1523|   5202|


#### pos

The following table shows the number of data samples/number of rows for each split in pos.

|   |train|validation.en|validation.de|validation.es|validation.nl|validation.bg|validation.el|validation.fr|validation.pl|validation.tr|validation.vi|validation.zh|validation.ur|validation.hi|validation.it|validation.ar|validation.ru|validation.th|test.en|test.de|test.es|test.nl|test.bg|test.el|test.fr|test.pl|test.tr|test.vi|test.zh|test.ur|test.hi|test.it|test.ar|test.ru|test.th|
|---|----:|------------:|------------:|------------:|------------:|------------:|------------:|------------:|------------:|------------:|------------:|------------:|------------:|------------:|------------:|------------:|------------:|------------:|------:|------:|------:|------:|------:|------:|------:|------:|------:|------:|------:|------:|------:|------:|------:|------:|------:|
|pos|25376|         2001|          798|         1399|          717|         1114|          402|         1475|         2214|          987|          799|          499|          551|         1658|          563|          908|          578|          497|   2076|    976|    425|    595|   1115|    455|    415|   2214|    982|    799|    499|    534|   1683|    481|    679|    600|    497|


#### mlqa

The following table shows the number of data samples/number of rows for each split in mlqa.

|    |train|validation.en|validation.de|validation.ar|validation.es|validation.hi|validation.vi|validation.zh|test.en|test.de|test.ar|test.es|test.hi|test.vi|test.zh|
|----|----:|------------:|------------:|------------:|------------:|------------:|------------:|------------:|------:|------:|------:|------:|------:|------:|------:|
|mlqa|87599|         1148|          512|          517|          500|          507|          511|          504|  11590|   4517|   5335|   5253|   4918|   5495|   5137|


#### nc

The following table shows the number of data samples/number of rows for each split in nc.

|   |train |validation.en|validation.de|validation.es|validation.fr|validation.ru|test.en|test.de|test.es|test.fr|test.ru|
|---|-----:|------------:|------------:|------------:|------------:|------------:|------:|------:|------:|------:|------:|
|nc |100000|        10000|        10000|        10000|        10000|        10000|  10000|  10000|  10000|  10000|  10000|


#### xnli

The following table shows the number of data samples/number of rows for each split in xnli.

|    |train |validation.en|validation.ar|validation.bg|validation.de|validation.el|validation.es|validation.fr|validation.hi|validation.ru|validation.sw|validation.th|validation.tr|validation.ur|validation.vi|validation.zh|test.en|test.ar|test.bg|test.de|test.el|test.es|test.fr|test.hi|test.ru|test.sw|test.th|test.tr|test.ur|test.vi|test.zh|
|----|-----:|------------:|------------:|------------:|------------:|------------:|------------:|------------:|------------:|------------:|------------:|------------:|------------:|------------:|------------:|------------:|------:|------:|------:|------:|------:|------:|------:|------:|------:|------:|------:|------:|------:|------:|------:|
|xnli|392702|         2490|         2490|         2490|         2490|         2490|         2490|         2490|         2490|         2490|         2490|         2490|         2490|         2490|         2490|         2490|   5010|   5010|   5010|   5010|   5010|   5010|   5010|   5010|   5010|   5010|   5010|   5010|   5010|   5010|   5010|

The following table shows the number of data samples/number of rows for each split in mlqa.

|    |train|validation.en|validation.de|validation.ar|validation.es|validation.hi|validation.vi|validation.zh|test.en|test.de|test.ar|test.es|test.hi|test.vi|test.zh|                                                                                                                                                      
|----|----:|------------:|------------:|------------:|------------:|------------:|------------:|------------:|------:|------:|------:|------:|------:|------:|------:|                                                                                                                                                      
|mlqa|87599|         1148|          512|          517|          500|          507|          511|          504|  11590|   4517|   5335|   5253|   4918|   5495|   5137|                                                                                                                                                      


#### nc

The following table shows the number of data samples/number of rows for each split in nc.

|   |train |validation.en|validation.de|validation.es|validation.fr|validation.ru|test.en|test.de|test.es|test.fr|test.ru|
|---|-----:|------------:|------------:|------------:|------------:|------------:|------:|------:|------:|------:|------:|
|nc |100000|        10000|        10000|        10000|        10000|        10000|  10000|  10000|  10000|  10000|  10000|


#### xnli

The following table shows the number of data samples/number of rows for each split in xnli.

|    |train |validation.en|validation.ar|validation.bg|validation.de|validation.el|validation.es|validation.fr|validation.hi|validation.ru|validation.sw|validation.th|validation.tr|validation.ur|validation.vi|validation.zh|test.en|test.ar|test.bg|test.de|test.el|test.es|test.fr|test.hi|test.ru|test.sw|test.th|test.tr|test.ur|test.vi|test.zh|
|----|-----:|------------:|------------:|------------:|------------:|------------:|------------:|------------:|------------:|------------:|------------:|------------:|------------:|------------:|------------:|------------:|------:|------:|------:|------:|------:|------:|------:|------:|------:|------:|------:|------:|------:|------:|------:|
|xnli|392702|         2490|         2490|         2490|         2490|         2490|         2490|         2490|         2490|         2490|         2490|         2490|         2490|         2490|         2490|         2490|   5010|   5010|   5010|   5010|   5010|   5010|   5010|   5010|   5010|   5010|   5010|   5010|   5010|   5010|   5010|


#### paws-x

The following table shows the number of data samples/number of rows for each split in paws-x.

|      |train|validation.en|validation.de|validation.es|validation.fr|test.en|test.de|test.es|test.fr|
|------|----:|------------:|------------:|------------:|------------:|------:|------:|------:|------:|
|paws-x|49401|         2000|         2000|         2000|         2000|   2000|   2000|   2000|   2000|


#### qadsm

The following table shows the number of data samples/number of rows for each split in qadsm.

|     |train |validation.en|validation.de|validation.fr|test.en|test.de|test.fr|
|-----|-----:|------------:|------------:|------------:|------:|------:|------:|
|qadsm|100000|        10000|        10000|        10000|  10000|  10000|  10000|


#### wpr

The following table shows the number of data samples/number of rows for each split in wpr.

|   |train|validation.en|validation.de|validation.es|validation.fr|validation.it|validation.pt|validation.zh|test.en|test.de|test.es|test.fr|test.it|test.pt|test.zh|
|---|----:|------------:|------------:|------------:|------------:|------------:|------------:|------------:|------:|------:|------:|------:|------:|------:|------:|
|wpr|99997|        10008|        10004|        10004|        10005|        10003|        10001|        10002|  10004|   9997|  10006|  10020|  10001|  10015|   9999|


#### qam

The following table shows the number of data samples/number of rows for each split in qam.

|   |train |validation.en|validation.de|validation.fr|test.en|test.de|test.fr|
|---|-----:|------------:|------------:|------------:|------:|------:|------:|
|qam|100000|        10000|        10000|        10000|  10000|  10000|  10000|


#### qg

The following table shows the number of data samples/number of rows for each split in qg.

|   |train |validation.en|validation.de|validation.es|validation.fr|validation.it|validation.pt|test.en|test.de|test.es|test.fr|test.it|test.pt|
|---|-----:|------------:|------------:|------------:|------------:|------------:|------------:|------:|------:|------:|------:|------:|------:|
|qg |100000|        10000|        10000|        10000|        10000|        10000|        10000|  10000|  10000|  10000|  10000|  10000|  10000|


#### ntg

The following table shows the number of data samples/number of rows for each split in ntg.

|   |train |validation.en|validation.de|validation.es|validation.fr|validation.ru|test.en|test.de|test.es|test.fr|test.ru|
|---|-----:|------------:|------------:|------------:|------------:|------------:|------:|------:|------:|------:|------:|
|ntg|300000|        10000|        10000|        10000|        10000|        10000|  10000|  10000|  10000|  10000|  10000|

## Dataset Creation

### Curation Rationale

[More Information Needed]

### Source Data

#### Initial Data Collection and Normalization

[More Information Needed]

#### Who are the source language producers?

[More Information Needed]

### Annotations

[More Information Needed]

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

The dataset is maintained mainly by Yaobo Liang, Yeyun Gong, Nan Duan, Ming Gong, Linjun Shou, and Daniel Campos from Microsoft Research.

### Licensing Information

The licensing status of the dataset hinges on the legal status of [XGLUE](https://microsoft.github.io/XGLUE/) hich is unclear.

### Citation Information

```
@article{Liang2020XGLUEAN,
  title={XGLUE: A New Benchmark Dataset for Cross-lingual Pre-training, Understanding and Generation},
  author={Yaobo Liang and Nan Duan and Yeyun Gong and Ning Wu and Fenfei Guo and Weizhen Qi and Ming Gong and Linjun Shou and Daxin Jiang and Guihong Cao and Xiaodong Fan and Ruofei Zhang and Rahul Agrawal and Edward Cui and Sining Wei and Taroon Bharti and Ying Qiao and Jiun-Hung Chen and Winnie Wu and Shuguang Liu and Fan Yang and Daniel Campos and Rangan Majumder and Ming Zhou},
  journal={arXiv},
  year={2020},
  volume={abs/2004.01401}
}
```
