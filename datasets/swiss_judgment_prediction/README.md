---
pretty_name: Swiss-Judgment-Prediction
annotations_creators:
- found
language_creators:
- found
language:
- de 
- fr
- it
license:
- cc-by-sa-4.0
multilinguality:
- multilingual
size_categories:
- 10K<n<100K
source_datasets:
- original
task_categories:
- text-classification
task_ids:
- text-classification-other-judgement-prediction
---

# Dataset Card for "SwissJudgmentPrediction"

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

- **Homepage:** https://github.com/JoelNiklaus/SwissCourtRulingCorpus
- **Repository:** https://github.com/JoelNiklaus/SwissCourtRulingCorpus
- **Paper:** https://arxiv.org/abs/2110.00806
- **Leaderboard:** N/A
- **Point of Contact:** [Joel Niklaus](mailto:joel.niklaus@inf.unibe.ch)

### Dataset Summary

**Documents**

Swiss-Judgment-Prediction is a multilingual, diachronic dataset of 85K Swiss Federal Supreme Court (FSCS) cases annotated with the respective binarized judgment outcome (approval/dismissal), posing a challenging text classification task. We also provide additional metadata, i.e., the publication year, the legal area and the canton of origin per case, to promote robustness and fairness studies on the critical area of legal NLP.

### Supported Tasks and Leaderboards

SwissJudgmentPrediction can be used for the legal judgment prediction task.

The dataset is not yet part of an established benchmark.

### Languages

Switzerland has four official languages with 3 languages (German, French and Italian) being represented in more than 1000 Swiss Federal Supreme court decisions. The decisions are written by the judges and clerks in the language of the proceedings.

## Dataset Structure

### Data Instances

**Multilingual use of the dataset**

When the dataset is used in a multilingual setting selecting the the 'all_languages' flag:

```python
from datasets import load_dataset
dataset = load_dataset('swiss_judgment_prediction', 'all_languages')
```

```
{
  "id": 48757,
  "year": 2015,
  "facts": "Sachverhalt: A. X._ war bei der Krankenversicherung C._ taggeldversichert. Infolge einer Arbeitsunf\u00e4higkeit leistete ihm die C._ vom 30. Juni 2011 bis am 28. Juni 2013 Krankentaggelder, wobei die Leistungen bis am 30. September 2012 auf Grundlage einer Arbeitsunf\u00e4higkeit von 100% und danach basierend auf einer Arbeitsunf\u00e4higkeit von 55% erbracht wurden. Die Neueinsch\u00e4tzung der Arbeitsf\u00e4higkeit erfolgte anhand eines Gutachtens der D._ AG vom 27. August 2012, welches im Auftrag der C._ erstellt wurde. X._ machte daraufhin gegen\u00fcber der C._ geltend, er sei entgegen dem Gutachten auch nach dem 30. September 2012 zu 100% arbeitsunf\u00e4hig gewesen. Ferner verlangte er von der D._ AG zwecks externer \u00dcberpr\u00fcfung des Gutachtens die Herausgabe s\u00e4mtlicher diesbez\u00fcglicher Notizen, Auswertungen und Unterlagen. A._ (als Gesch\u00e4ftsf\u00fchrer der D._ AG) und B._ (als f\u00fcr das Gutachten medizinisch Verantwortliche) antworteten ihm, dass sie alle Unterlagen der C._ zugestellt h\u00e4tten und dass allf\u00e4llige Fragen zum Gutachten direkt der C._ zu stellen seien. X._ reichte am 2. Januar 2014 eine Strafanzeige gegen A._ und B._ ein. Er wirft diesen vor, ihn durch die Nichtherausgabe der Dokumente und durch Behinderung des IV-Verfahrens gen\u00f6tigt, Daten besch\u00e4digt bzw. vernichtet und ein falsches \u00e4rztliches Zeugnis ausgestellt zu haben. Zudem h\u00e4tten sie durch die Verz\u00f6gerung des IV-Verfahrens und insbesondere durch das falsche \u00e4rztliche Zeugnis sein Verm\u00f6gen arglistig gesch\u00e4digt. B. Die Staatsanwaltschaft des Kantons Bern, Region Oberland, nahm das Verfahren wegen N\u00f6tigung, Datenbesch\u00e4digung, falschem \u00e4rztlichem Zeugnis und arglistiger Verm\u00f6genssch\u00e4digung mit Verf\u00fcgung vom 10. November 2014 nicht an die Hand. Das Obergericht des Kantons Bern wies die von X._ dagegen erhobene Beschwerde am 27. April 2015 ab, soweit darauf einzutreten war. C. X._ beantragt mit Beschwerde in Strafsachen, der Beschluss vom 27. April 2015 sei aufzuheben und die Angelegenheit zur korrekten Ermittlung des Sachverhalts an die Staatsanwaltschaft zur\u00fcckzuweisen. Er stellt zudem den sinngem\u00e4ssen Antrag, das bundesgerichtliche Verfahren sei w\u00e4hrend der Dauer des konnexen Strafverfahrens gegen eine Teilgutachterin und des ebenfalls konnexen Zivil- oder Strafverfahrens gegen die C._ wegen Einsichtsverweigerung in das mutmasslich gef\u00e4lschte Originalgutachten zu sistieren. X._ ersucht um unentgeltliche Rechtspflege. ",
  "labels": 0,  # dismissal
  "language": "de",
  "region": "Espace Mittelland",
  "canton": "be",
  "legal area": "penal law"
}
```

**Monolingual use of the dataset**

When the dataset is used in a monolingual setting selecting the ISO language code for one of the 3 supported languages. For example:

```python
from datasets import load_dataset
dataset = load_dataset('swiss_judgment_prediction', 'de')
```

```
{
  "id": 48757,
  "year": 2015,
  "facts": "Sachverhalt: A. X._ war bei der Krankenversicherung C._ taggeldversichert. Infolge einer Arbeitsunf\u00e4higkeit leistete ihm die C._ vom 30. Juni 2011 bis am 28. Juni 2013 Krankentaggelder, wobei die Leistungen bis am 30. September 2012 auf Grundlage einer Arbeitsunf\u00e4higkeit von 100% und danach basierend auf einer Arbeitsunf\u00e4higkeit von 55% erbracht wurden. Die Neueinsch\u00e4tzung der Arbeitsf\u00e4higkeit erfolgte anhand eines Gutachtens der D._ AG vom 27. August 2012, welches im Auftrag der C._ erstellt wurde. X._ machte daraufhin gegen\u00fcber der C._ geltend, er sei entgegen dem Gutachten auch nach dem 30. September 2012 zu 100% arbeitsunf\u00e4hig gewesen. Ferner verlangte er von der D._ AG zwecks externer \u00dcberpr\u00fcfung des Gutachtens die Herausgabe s\u00e4mtlicher diesbez\u00fcglicher Notizen, Auswertungen und Unterlagen. A._ (als Gesch\u00e4ftsf\u00fchrer der D._ AG) und B._ (als f\u00fcr das Gutachten medizinisch Verantwortliche) antworteten ihm, dass sie alle Unterlagen der C._ zugestellt h\u00e4tten und dass allf\u00e4llige Fragen zum Gutachten direkt der C._ zu stellen seien. X._ reichte am 2. Januar 2014 eine Strafanzeige gegen A._ und B._ ein. Er wirft diesen vor, ihn durch die Nichtherausgabe der Dokumente und durch Behinderung des IV-Verfahrens gen\u00f6tigt, Daten besch\u00e4digt bzw. vernichtet und ein falsches \u00e4rztliches Zeugnis ausgestellt zu haben. Zudem h\u00e4tten sie durch die Verz\u00f6gerung des IV-Verfahrens und insbesondere durch das falsche \u00e4rztliche Zeugnis sein Verm\u00f6gen arglistig gesch\u00e4digt. B. Die Staatsanwaltschaft des Kantons Bern, Region Oberland, nahm das Verfahren wegen N\u00f6tigung, Datenbesch\u00e4digung, falschem \u00e4rztlichem Zeugnis und arglistiger Verm\u00f6genssch\u00e4digung mit Verf\u00fcgung vom 10. November 2014 nicht an die Hand. Das Obergericht des Kantons Bern wies die von X._ dagegen erhobene Beschwerde am 27. April 2015 ab, soweit darauf einzutreten war. C. X._ beantragt mit Beschwerde in Strafsachen, der Beschluss vom 27. April 2015 sei aufzuheben und die Angelegenheit zur korrekten Ermittlung des Sachverhalts an die Staatsanwaltschaft zur\u00fcckzuweisen. Er stellt zudem den sinngem\u00e4ssen Antrag, das bundesgerichtliche Verfahren sei w\u00e4hrend der Dauer des konnexen Strafverfahrens gegen eine Teilgutachterin und des ebenfalls konnexen Zivil- oder Strafverfahrens gegen die C._ wegen Einsichtsverweigerung in das mutmasslich gef\u00e4lschte Originalgutachten zu sistieren. X._ ersucht um unentgeltliche Rechtspflege. ",
  "labels": 0,  # dismissal
  "language": "de",
  "region": "Espace Mittelland",
  "canton": "be",
  "legal area": "penal law"
}
```

### Data Fields

**Multilingual use of the dataset**

The following data fields are provided for documents (`train`, `dev`, `test`):

`id`: (**int**) a unique identifier of the for the document \
`year`: (**int**) the publication year \
`text`: (**str**) the facts of the case \
`label`: (**class label**) the judgment outcome: 0 (dismissal) or 1 (approval) \
`language`: (**str**) one of (de, fr, it) \
`region`: (**str**) the region of the lower court \
`canton`: (**str**) the canton of the lower court \
`legal area`: (**str**) the legal area of the case 



**Monolingual use of the dataset**

The following data fields are provided for documents (`train`, `dev`, `test`):

`id`: (**int**) a unique identifier of the for the document \
`year`: (**int**) the publication year \
`text`: (**str**) the facts of the case \
`label`: (**class label**) the judgment outcome: 0 (dismissal) or 1 (approval) \
`language`: (**str**) one of (de, fr, it) \
`region`: (**str**) the region of the lower court \
`canton`: (**str**) the canton of the lower court \
`legal area`: (**str**) the legal area of the case 


### Data Splits

| Language |  ISO code | Number of Documents (Training/Dev/Test) | 
| ---- | ---- |  ---- |  
| German    | **de**   | 35'452 / 4'705 / 9'725
| French    | **fr**   | 21'179 / 3'095 / 6'820
Italian     | **it**   | 3'072 / 408 / 812

## Dataset Creation

### Curation Rationale

The dataset was curated by Niklaus et al. (2021).

### Source Data

#### Initial Data Collection and Normalization

The original data are available at the Swiss Federal Supreme Court (https://www.bger.ch) in unprocessed formats (HTML). The documents were downloaded from the Entscheidsuche portal (https://entscheidsuche.ch) in HTML. 

#### Who are the source language producers?

Switzerland has four official languages with 3 languages (German, French and Italian) being represented in more than 1000 Swiss Federal Supreme court decisions. The decisions are written by the judges and clerks in the language of the proceedings.

### Annotations

#### Annotation process

The decisions have been annotated with the binarized judgment outcome using parsers and regular expressions.

#### Who are the annotators?

Joel Niklaus and Adrian Jörg annotated the binarized judgment outcomes.
Metadata is published by the Swiss Federal Supreme Court (https://www.bger.ch).

### Personal and Sensitive Information

The dataset contains publicly available court decisions from the Swiss Federal Supreme Court. Personal or sensitive information has been anonymized by the court before publication according to the following guidelines: https://www.bger.ch/home/juridiction/anonymisierungsregeln.html.

## Considerations for Using the Data

### Social Impact of Dataset

[More Information Needed]

### Discussion of Biases

[More Information Needed]

### Other Known Limitations

[More Information Needed]

## Additional Information

### Dataset Curators

Niklaus et al. (2021)

### Licensing Information

We release the data under CC-BY-4.0 which complies with the court licensing (https://www.bger.ch/files/live/sites/bger/files/pdf/de/urteilsveroeffentlichung_d.pdf)

© Swiss Federal Supreme Court, 2000-2020

The copyright for the editorial content of this website and the consolidated texts, which is owned by the Swiss Federal Supreme Court, is licensed under the Creative Commons Attribution 4.0 International licence. This means that you can re-use the content provided you acknowledge the source and indicate any changes you have made.

Source: https://www.bger.ch/files/live/sites/bger/files/pdf/de/urteilsveroeffentlichung_d.pdf

### Citation Information

*Joel Niklaus, Ilias Chalkidis, and Matthias Stürmer.*
*Swiss-Judgment-Prediction: A Multilingual Legal Judgment Prediction Benchmark*
*Proceedings of the 2021 Natural Legal Language Processing Workshop. Punta Cana, Dominican Republic. 2021*
```
@InProceedings{niklaus-etal-2021-swiss,
  author = {Niklaus, Joel
                and Chalkidis, Ilias
                and Stürmer, Matthias},
  title = {Swiss-Judgment-Prediction: A Multilingual Legal Judgment Prediction Benchmark},
  booktitle = {Proceedings of the 2021 Natural Legal Language Processing Workshop},
  year = {2021},
  location = {Punta Cana, Dominican Republic},
}
```

### Contributions

Thanks to [@joelniklaus](https://github.com/joelniklaus) for adding this dataset.
