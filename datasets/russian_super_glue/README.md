---
pretty_name: Russian SuperGLUE
annotations_creators:
- crowdsourced
- expert-generated
language_creators:
- crowdsourced
- expert-generated
language:
- ru-RU
license:
- mit
multilinguality:
- monolingual
size_categories:
- 100K<n<1M
- 1M<n<10M
- 10M<n<100M
- 100M<n<1B
source_datasets:
- original
task_categories:
- text-classification
task_ids:
- natural-language-inference
- multi-class-classification
---

# Dataset Card for [Russian SuperGLUE]

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

- **Homepage:** https://russiansuperglue.com/
- **Repository:** https://github.com/RussianNLP/RussianSuperGLUE
- **Paper:** https://russiansuperglue.com/download/main_article
- **Leaderboard:** https://russiansuperglue.com/leaderboard/2
- **Point of Contact:** [More Information Needed]

### Dataset Summary

Modern universal language models and transformers such as BERT, ELMo, XLNet, RoBERTa and others need to be properly
compared and evaluated. In the last year, new models and methods for pretraining and transfer learning have driven 
striking performance improvements across a range of language understanding tasks.


We offer testing methodology based on tasks, typically proposed for “strong AI” — logic, commonsense, reasoning.
Adhering to the GLUE and SuperGLUE methodology, we present a set of test tasks for general language understanding
and leaderboard models.


For the first time a complete test for Russian language was developed, which is similar to its English analog.
Many datasets were composed for the first time, and a leaderboard of models for the Russian language with comparable
results is also presented.

### Supported Tasks and Leaderboards

Supported tasks, barring a few additions, are equivalent to the original SuperGLUE tasks.

|Task Name|Equiv. to|
|----|---:|
|Linguistic Diagnostic for Russian|Broadcoverage Diagnostics (AX-b)|
|Russian Commitment Bank (RCB)|CommitmentBank (CB)|
|Choice of Plausible Alternatives for Russian language (PARus)|Choice of Plausible Alternatives (COPA)|
|Russian Multi-Sentence Reading Comprehension (MuSeRC)|Multi-Sentence Reading Comprehension (MultiRC)|
|Textual Entailment Recognition for Russian (TERRa)|Recognizing Textual Entailment (RTE)|
|Russian Words in Context (based on RUSSE)|Words in Context (WiC)|
|The Winograd Schema Challenge (Russian)|The Winograd Schema Challenge (WSC)|
|Yes/no Question Answering Dataset for the Russian (DaNetQA)|BoolQ|
|Russian Reading Comprehension with Commonsense Reasoning (RuCoS)|Reading Comprehension with Commonsense Reasoning (ReCoRD)|

### Languages

All tasks are in Russian.

## Dataset Structure

### Data Instances

Note that there are no labels in the `test` splits. This is signified by the `-1` value.

#### LiDiRus

- **Size of downloaded dataset files:** 0.047 MB
- **Size of the generated dataset:** 0.47 MB
- **Total amount of disk used:** 0.517 MB

An example of 'test' looks as follows
```
{
    "sentence1": "Новая игровая консоль доступна по цене.",
    "sentence2": "Новая игровая консоль недоступна по цене.",
    "knowledge": "",
    "lexical-semantics": "Morphological negation",
    "logic": "Negation",
    "predicate-argument-structure": "",
    "idx": 10,
    "label": 1
}
```

#### RCB

- **Size of downloaded dataset files:** 0.134 MB
- **Size of the generated dataset:** 0.504 MB
- **Total amount of disk used:** 0.641 MB

An example of 'train'/'dev' looks as follows
```
{
    "premise": "— Пойдём пообедаем. Я с утра ничего не ел. Отель, как видишь, весьма посредственный, но мне сказали,
     что в здешнем ресторане отлично готовят.",
    "hypothesis": "В здешнем ресторане отлично готовят.",
    "verb": "сказать",
    "negation": "no_negation",
    "idx": 10,
    "label": 2
}
```

An example of 'test' looks as follows
```
{
    "premise": "Я уверен, что вместе мы победим. Да, парламентское большинство думает иначе.",
    "hypothesis": "Вместе мы проиграем.",
    "verb": "думать",
    "negation": "no_negation",
    "idx": 10,
    "label": -1
}
```

#### PARus

- **Size of downloaded dataset files:** 0.057 MB
- **Size of the generated dataset:** 0.187 MB
- **Total amount of disk used:**  0.245 MB

An example of 'train'/'dev' looks as follows
```
{
    "premise": "Женщина чинила кран.",
    "choice1": "Кран подтекал.",
    "choice2": "Кран был выключен.",
    "question": "cause",
    "idx": 10,
    "label": 0
}
```

An example of 'test' looks as follows
```
{
    "premise": "Ребятам было страшно.",
    "choice1": "Их вожатый рассказал им историю про призрака.",
    "choice2": "Они жарили маршмеллоу на костре.",
    "question": "cause",
    "idx": 10,
    "label": -1
}
```
#### MuSeRC

- **Size of downloaded dataset files:** 1.2 MB
- **Size of the generated dataset:** 57 MB
- **Total amount of disk used:** 59 MB

An example of 'train'/'dev' looks as follows
```
{
    "paragraph": "(1) Но люди не могут существовать без природы, поэтому в парке стояли железобетонные скамейки —
     деревянные моментально ломали. (2) В парке бегали ребятишки, водилась шпана, которая развлекалась игрой в карты,
     пьянкой, драками, «иногда насмерть». (3) «Имали они тут и девок...» (4) Верховодил шпаной Артемка-мыло, с
     вспененной белой головой. (5) Людочка сколько ни пыталась усмирить лохмотья на буйной голове Артемки, ничего у
     неё не получалось. (6) Его «кудри, издали напоминавшие мыльную пену, изблизя оказались что липкие рожки из
     вокзальной столовой — сварили их, бросили комком в пустую тарелку, так они, слипшиеся, неподъёмно и лежали.
     (7) Да и не ради причёски приходил парень к Людочке. (8) Как только её руки становились занятыми ножницами
     и расчёской, Артемка начинал хватать её за разные места. (9) Людочка сначала увёртывалась от хватких рук Артемки,
     а когда не помогло, стукнула его машинкой по голове и пробила до крови, пришлось лить йод на голову «ухажористого
     человека». (10) Артемка заулюлюкал и со свистом стал ловить воздух. (11) С тех пор «домогания свои хулиганские
     прекратил», более того, шпане повелел Людочку не трогать.",
    "question": "Как развлекались в парке ребята?",
    "answer": "Развлекались игрой в карты, пьянкой, драками, снимали они тут и девок.",
    "idx":
    {
        "paragraph": 0,
        "question": 2,
        "answer": 10
    },
    "label": 1
}
```

An example of 'test' looks as follows
```

{
    "paragraph": "\"(1) Издательство Viking Press совместно с компанией TradeMobile выпустят мобильное приложение,
     посвященное Анне Франк, передает The Daily Telegraph. (2) Программа будет включать в себя фрагменты из дневника
     Анны, озвученные британской актрисой Хеленой Бонэм Картер. (3) Помимо этого, в приложение войдут фотографии
     и видеозаписи, документы из архива Фонда Анны Франк, план здания в Амстердаме, где Анна с семьей скрывались от
     нацистов, и факсимильные копии страниц дневника. (4) Приложение, которое получит название Anne Frank App, выйдет
     18 октября. (5) Интерфейс программы будет англоязычным. (6) На каких платформах будет доступно Anne Frank App,
     не уточняется. Анна Франк родилась в Германии в 1929 году. (7) Когда в стране начались гонения на евреев, Анна с
     семьей перебрались в Нидерланды. (8) С 1942 года члены семьи Франк и еще несколько человек скрывались от нацистов
     в потайных комнатах дома в Амстердаме, который занимала компания отца Анны. (9) В 1944 году группу по доносу
     обнаружили гестаповцы. (10) Обитатели \"Убежища\" (так Анна называла дом в дневнике) были отправлены в концлагеря;
     выжить удалось только отцу девочки Отто Франку. (11) Находясь в \"Убежище\", Анна вела дневник, в котором описывала
     свою жизнь и жизнь своих близких. (12) После ареста книгу с записями сохранила подруга семьи Франк и впоследствии
     передала ее отцу Анны. (13) Дневник был впервые опубликован в 1947 году. (14) Сейчас он переведен более
     чем на 60 языков.\"",
    "question": "Какая информация войдет в новой мобильное приложение?",
    "answer": "Видеозаписи Анны Франк.",
    "idx":
    {
        "paragraph": 0,
        "question": 2,
        "answer": 10
    },
    "label": -1
}
```
#### TERRa

- **Size of downloaded dataset files:** 0.887 MB
- **Size of the generated dataset:** 3.28 MB
- **Total amount of disk used:** 4.19 MB

An example of 'train'/'dev' looks as follows
```
{
    "premise": "Музей, расположенный в Королевских воротах, меняет экспозицию. На смену выставке, рассказывающей об
     истории ворот и их реставрации, придет «Аптека трех королей». Как рассказали в музее, посетители попадут в 
     традиционный интерьер аптеки.",
    "hypothesis": "Музей закроется навсегда.",
    "idx": 10,
    "label": 1
}
```

An example of 'test' looks as follows
```
{
    "premise": "Маршрутка полыхала несколько минут. Свидетели утверждают, что приезду пожарных салон «Газели» выгорел полностью. К счастью, пассажиров внутри не было, а водитель успел выскочить из кабины.",
    "hypothesis": "Маршрутка выгорела.",
    "idx": 10,
    "label": -1
}
```

#### RUSSE

- **Size of downloaded dataset files:** 3.7 MB
- **Size of the generated dataset:** 20 MB
- **Total amount of disk used:** 24 MB

An example of 'train'/'dev' looks as follows
```
{
    "word": "дух",
    "sentence1": "Завертелась в доме веселая коловерть: праздничный стол, праздничный дух, шумные разговоры",
    "sentence2": "Вижу: духи собралися / Средь белеющих равнин. // Бесконечны, безобразны, / В мутной месяца игре / Закружились бесы разны, / Будто листья в ноябре",
    "start1": 68,
    "start2": 6,
    "end1": 72,
    "end2": 11,
    "gold_sense1": 3,
    "gold_sense2": 4,
    "idx": 10,
    "label": 0
}
```

An example of 'test' looks as follows
```
{
    "word": "доска",
    "sentence1": "На 40-й день после трагедии в переходе была установлена мемориальная доска, надпись на которой гласит: «В память о погибших и пострадавших от террористического акта 8 августа 2000 года».",
    "sentence2": "Фото с 36-летним миллиардером привлекло сеть его необычной фигурой при стойке на доске и кремом на лице.",
    "start1": 69,
    "start2": 81,
    "end1": 73,
    "end2": 85,
    "gold_sense1": -1,
    "gold_sense2": -1,
    "idx": 10,
    "label": -1
}
```

#### RWSD

- **Size of downloaded dataset files:** 0.04 MB
- **Size of the generated dataset:** 0.279 MB
- **Total amount of disk used:**  0.320 MB

An example of 'train'/'dev' looks as follows
```
{
    "text": "Женя поблагодарила Сашу за помощь, которую она оказала.",
    "span1_index": 0,
    "span2_index": 6,
    "span1_text": "Женя",
    "span2_text": "она оказала",
    "idx": 10,
    "label": 0
}
```

An example of 'test' looks as follows
```
{
    "text": "Мод и Дора видели, как через прерию несутся поезда, из двигателей тянулись клубы черного дыма. Ревущие 
    звуки их моторов и дикие, яростные свистки можно было услышать издалека. Лошади убежали, когда они увидели 
    приближающийся поезд.",
    "span1_index": 22,
    "span2_index": 30,
    "span1_text": "свистки",
    "span2_text": "они увидели",
    "idx": 10,
    "label": -1
}
```

#### DaNetQA

- **Size of downloaded dataset files:** 1.3 MB
- **Size of the generated dataset:** 4.6 MB
- **Total amount of disk used:**  5.9 MB

An example of 'train'/'dev' looks as follows
```
{
    "question": "Вреден ли алкоголь на первых неделях беременности?",
    "passage": "А Бакингем-Хоуз и её коллеги суммировали последствия, найденные в обзорных статьях ранее. Частые случаи
     задержки роста плода, результатом чего является укороченный средний срок беременности и сниженный вес при рождении.
     По сравнению с нормальными детьми, дети 3-4-недельного возраста демонстрируют «менее оптимальную»  двигательную 
     активность, рефлексы, и ориентацию в пространстве, а дети 4-6 лет показывают низкий уровень работы 
     нейроповеденческих функций, внимания, эмоциональной экспрессии, и развития речи и языка. Величина этих влияний 
     часто небольшая, частично в связи с независимыми переменными: включая употребление во время беременности 
     алкоголя/табака, а также факторы среды . У детей школьного возраста проблемы с устойчивым вниманием и контролем 
     своего поведения, а также незначительные с ростом, познавательными и языковыми способностями.",
    "idx": 10,
    "label": 1
}
```

An example of 'test' looks as follows
```
{
    "question": "Вредна ли жесткая вода?",
    "passage": "Различают временную  жёсткость, обусловленную гидрокарбонатами кальция и магния Са2; Mg2, и постоянную
     жёсткость, вызванную присутствием других солей, не выделяющихся при кипячении воды: в основном, сульфатов и 
     хлоридов Са и Mg. Жёсткая вода при умывании сушит кожу, в ней плохо образуется пена при использовании мыла.
     Использование жёсткой воды вызывает появление осадка  на стенках котлов, в трубах и т. п. В то же время, 
     использование слишком мягкой воды может приводить к коррозии труб, так как, в этом случае отсутствует 
     кислотно-щелочная буферность, которую обеспечивает гидрокарбонатная  жёсткость. Потребление жёсткой или мягкой 
     воды обычно не является опасным для здоровья, однако есть данные о том, что высокая жёсткость способствует 
     образованию мочевых камней, а низкая — незначительно увеличивает риск сердечно-сосудистых заболеваний. Вкус 
     природной питьевой воды, например, воды родников, обусловлен именно присутствием солей жёсткости.",
    "idx": 100,
    "label": -1
}
```

#### RuCoS

- **Size of downloaded dataset files:** 54 MB
- **Size of the generated dataset:** 193 MB
- **Total amount of disk used:** 249 MB

An example of 'train'/'dev' looks as follows
```
{
    "passage": "В Абхазии 24 августа на досрочных выборах выбирают нового президента. Кто бы ни стал победителем,
     возможности его будут ограничены, говорят эксперты, опрошенные DW. В Абхазии 24 августа проходят досрочные выборы
     президента не признанной международным сообществом республики. Толчком к их проведению стали массовые протесты в 
     конце мая 2014 года, в результате которых со своего поста был вынужден уйти действующий президент Абхазии Александр
     Анкваб. Эксперты называют среди наиболее перспективных кандидатов находящегося в оппозиции политика Рауля Хаджимбу,
     экс-главу службы безопасности Аслана Бжанию и генерала Мираба Кишмарию, исполняющего обязанности министра обороны.
     У кого больше шансов\n\"Ставки делаются на победу Хаджимбы.\n@highlight\nВ Швеции задержаны двое граждан РФ в связи
     с нападением на чеченского блогера\n@highlight\nТуризм в эпоху коронавируса: куда поехать? И ехать ли 
     вообще?\n@highlight\nКомментарий: Россия накануне эпидемии - виноватые назначены заранее",
    "query": "Несмотря на то, что Кремль вложил много денег как в @placeholder, так и в Южную Осетию, об экономическом
     восстановлении данных регионов говорить не приходится, считает Хальбах: \"Многие по-прежнему живут в 
     полуразрушенных домах и временных жилищах\".",
    "entities":
    [
        "DW.",
        "Абхазии ",
        "Александр Анкваб.",
        "Аслана Бжанию ",
        "Мираба Кишмарию,",
        "РФ ",
        "Рауля Хаджимбу,",
        "Россия ",
        "Хаджимбы.",
        "Швеции "
    ],
    "answers":
    [
        "Абхазии"
    ],
    "idx":
    {
        "passage": 500,
        "query": 500
    }
}
```

An example of 'test' looks as follows
```
{
    "passage": "Почему и как изменится курс белорусского рубля? Какие инструменты следует предпочесть населению, чтобы 
    сохранить сбережения, DW рассказали финансовые аналитики Беларуси. На последних валютных торгах БВФБ 2015 года в 
    среду, 30 декабря, курс белорусского рубля к доллару - 18569, к евро - 20300, к российскому рублю - 255. В 2016 
    году белорусскому рублю пророчат падение как минимум на 12 процентов к корзине валют, к которой привязан его курс. 
    А чтобы избежать потерь, белорусам советуют диверсифицировать инвестиционные портфели. Чем обусловлены прогнозные 
    изменения котировок белорусского рубля, и какие финансовые инструменты стоит предпочесть, чтобы минимизировать риск
    потерь?\n@highlight\nВ Германии за сутки выявлено более 100 новых заражений коронавирусом\n@highlight\nРыночные цены
    на нефть рухнули из-за провала переговоров ОПЕК+\n@highlight\nВ Италии за сутки произошел резкий скачок смертей от
    COVID-19",
    "query": "Последнее, убежден аналитик, инструмент для узкого круга профессиональных инвесторов, культуры следить за
     финансовым состоянием предприятий - такой, чтобы играть на рынке корпоративных облигаций, - в @placeholder пока нет.",
    "entities":
    [
        "DW ",
        "Беларуси.",
        "Германии ",
        "Италии ",
        "ОПЕК+"
    ],
    "answers": [],
    "idx":
    {
        "passage": 500,
        "query": 500
    }
}
```

### Data Fields

#### LiDiRus

- `idx`: an `int32` feature
- `label`: a classification label, with possible values `entailment` (0), `not_entailment` (1)
- `sentence1`: a `string` feature
- `sentence2`: a `string` feature
- `knowledge`: a `string` feature with possible values `''`, `'World knowledge'`, `'Common sense'`
- `lexical-semantics`: a `string` feature
- `logic`: a `string` feature
- `predicate-argument-structure`: a `string` feature


#### RCB

- `idx`: an `int32` feature
- `label`: a classification label, with possible values `entailment` (0), `contradiction` (1), `neutral` (2)
- `premise`: a `string` feature
- `hypothesis`: a `string` feature
- `verb`: a `string` feature
- `negation`: a `string` feature with possible values `'no_negation'`, `'negation'`, `''`, `'double_negation'`

#### PARus

- `idx`: an `int32` feature
- `label`: a classification label, with possible values `choice1` (0), `choice2` (1)
- `premise`: a `string` feature
- `choice1`: a `string` feature
- `choice2`: a `string` feature
- `question`: a `string` feature with possible values `'cause'`, `'effect'`

#### MuSeRC
- `idx`: an `int32` feature
- `label` : a classification label, with possible values `false` (0) , `true` (1) (does the provided `answer` contain 
  a factual response to the `question`)
- `paragraph`: a `string` feature
- `question`: a `string` feature
- `answer`: a `string` feature


#### TERRa
- `idx`: an `int32` feature
- `label`: a classification label, with possible values `entailment` (0), `not_entailment` (1)
- `premise`: a `string` feature
- `hypothesis`: a `string` feature

#### RUSSE
- `idx`: an `int32` feature
- `label` : a classification label, with possible values `false` (0), `true` (1) (whether the given `word` used in the
  same sense in both sentences)
- `word`: a `string` feature
- `sentence1`: a `string` feature
- `sentence2`: a `string` feature
- `gold_sense1`: an `int32` feature
- `gold_sense2`: an `int32` feature
- `start1`: an `int32` feature
- `start2`: an `int32` feature
- `end1`: an `int32` feature
- `end2`: an `int32` feature

#### RWSD

- `idx`: an `int32` feature
- `label` : a classification label, with possible values `false` (0), `true` (1) (whether the given spans are
  coreferential)
- `text`: a `string` feature
- `span1_index`: an `int32` feature
- `span2_index`: an `int32` feature
- `span1_text`: a `string` feature
- `span2_text`: a `string` feature


#### DaNetQA
- `idx`: an `int32` feature
- `label` : a classification label, with possible values `false` (0), `true` (1) (yes/no answer to the `question` found
  in the `passage`)
- `question`: a `string` feature
- `passage`: a `string` feature

#### RuCoS

- `idx`: an `int32` feature
- `passage`: a `string` feature
- `query`: a `string` feature
- `entities`: a `list of strings` feature
- `answers`: a `list of strings` feature


[More Information Needed]

### Data Splits

#### 	LiDiRus
|   |test|
|---|---:|
|LiDiRus|1104|

#### RCB

| |train|validation|test|
|----|---:|----:|---:|
|RCB|438|220|438|

#### PARus

| |train|validation|test|
|----|---:|----:|---:|
|PARus|400|100|500|

#### MuSeRC

| |train|validation|test|
|----|---:|----:|---:|
|MuSeRC|500|100|322|


#### TERRa

| |train|validation|test|
|----|---:|----:|---:|
|TERRa|2616|307|3198|


#### RUSSE

| |train|validation|test|
|----|---:|----:|---:|
|RUSSE|19845|8508|18892|


#### RWSD

| |train|validation|test|
|----|---:|----:|---:|
|RWSD|606|204|154|


#### DaNetQA

| |train|validation|test|
|----|---:|----:|---:|
|DaNetQA|1749|821|805|


#### RuCoS

| |train|validation|test|
|----|---:|----:|---:|
|RuCoS|72193|7577|7257|

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

All our datasets are published by MIT License.

### Citation Information
```
@article{shavrina2020russiansuperglue,
                  title={RussianSuperGLUE: A Russian Language Understanding Evaluation Benchmark},
                  author={Shavrina, Tatiana and Fenogenova, Alena and Emelyanov, Anton and Shevelev, Denis and Artemova, Ekaterina and Malykh, Valentin and Mikhailov, Vladislav and Tikhonova, Maria and Chertok, Andrey and Evlampiev, Andrey},
                  journal={arXiv preprint arXiv:2010.15925},
                  year={2020}
                  }
```
### Contributions

Thanks to [@slowwavesleep](https://github.com/slowwavesleep) for adding this dataset.
