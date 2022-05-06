---
pretty_name: KLUE
annotations_creators:
- expert-generated
language_creators:
- expert-generated
languages:
- ko
licenses:
- cc-by-sa-4.0
multilinguality:
- monolingual
size_categories:
- 10K<n<100K
source_datasets:
- original
task_categories:
  ynat:
  - text-classification
  sts:
  - text-classification
  nli:
  - text-classification
  ner:
  - token-classification
  re:
  - token-classification
  dp:
  - token-classification
  mrc:
  - question-answering
  wos:
  - text-generation
  - fill-mask
task_ids:
  ynat:
  - topic-classification
  sts:
  - text-scoring
  - semantic-similarity-scoring
  nli:
  - natural-language-inference
  ner:
  - named-entity-recognition
  re:
  - token-classification-other-relation-extraction
  dp:
  - parsing
  mrc:
  - extractive-qa
  wos:
  - other-dialogue-state-tracking
paperswithcode_id: klue
---

# Dataset Card for KLUE

## Table of Contents
- [Dataset Description](#dataset-description)
  - [Dataset Summary](#dataset-summary)
  - [Supported Tasks](#supported-tasks-and-leaderboards)
  - [Languages](#languages)
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

- **Homepage:** https://klue-benchmark.com/
- **Repository:** https://github.com/KLUE-benchmark/KLUE
- **Paper:** [KLUE: Korean Language Understanding Evaluation](https://arxiv.org/abs/2105.09680)
- **Leaderboard:** [Leaderboard](https://klue-benchmark.com/leaderboard)
- **Point of Contact:** https://github.com/KLUE-benchmark/KLUE/issues

### Dataset Summary

KLUE is a collection of 8 tasks to evaluate natural language understanding capability of Korean language models. We delibrately select the 8 tasks, which are Topic Classification, Semantic Textual Similarity, Natural Language Inference, Named Entity Recognition, Relation Extraction, Dependency Parsing, Machine Reading Comprehension, and Dialogue State Tracking.

### Supported Tasks and Leaderboards

Topic Classification, Semantic Textual Similarity, Natural Language Inference, Named Entity Recognition, Relation Extraction, Dependency Parsing, Machine Reading Comprehension, and Dialogue State Tracking

### Languages

`ko-KR`

## Dataset Structure

### Data Instances

#### ynat
An example of 'train' looks as follows.

```
{'date': '2016.06.30. 오전 10:36',
 'guid': 'ynat-v1_train_00000',
 'label': 3,
 'title': '유튜브 내달 2일까지 크리에이터 지원 공간 운영',
 'url': 'https://news.naver.com/main/read.nhn?mode=LS2D&mid=shm&sid1=105&sid2=227&oid=001&aid=0008508947'}
```

#### sts
An example of 'train' looks as follows.

```
{'guid': 'klue-sts-v1_train_00000',
 'labels': {'label': 3.7, 'real-label': 3.714285714285714, 'binary-label': 1},
 'sentence1': '숙소 위치는 찾기 쉽고 일반적인 한국의 반지하 숙소입니다.',
 'sentence2': '숙박시설의 위치는 쉽게 찾을 수 있고 한국의 대표적인 반지하 숙박시설입니다.',
 'source': 'airbnb-rtt'}
```

#### nli
An example of 'train' looks as follows.

```
{'guid': 'klue-nli-v1_train_00000',
 'hypothesis': '힛걸 진심 최고로 멋지다.',
 'label': 0,
 'premise': '힛걸 진심 최고다 그 어떤 히어로보다 멋지다',
 'source': 'NSMC'}
```

#### ner
An example of 'train' looks as follows.

```
{'tokens': ['특', '히', ' ', '영', '동', '고', '속', '도', '로', ' ', '강', '릉', ' ', '방', '향', ' ', '문', '막', '휴', '게', '소', '에', '서', ' ', '만', '종', '분', '기', '점', '까', '지', ' ', '5', '㎞', ' ', '구', '간', '에', '는', ' ', '승', '용', '차', ' ', '전', '용', ' ', '임', '시', ' ', '갓', '길', '차', '로', '제', '를', ' ', '운', '영', '하', '기', '로', ' ', '했', '다', '.'],
 'ner_tags': [12, 12, 12, 2, 3, 3, 3, 3, 3, 12, 2, 3, 12, 12, 12, 12, 2, 3, 3, 3, 3, 12, 12, 12, 2, 3, 3, 3, 3, 12, 12, 12, 8, 9, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12],
 'sentence': '특히 <영동고속도로:LC> <강릉:LC> 방향 <문막휴게소:LC>에서 <만종분기점:LC>까지 <5㎞:QT> 구간에는 승용차 전용 임시 갓길차로제를 운영하기로 했다.'}
```

#### re
An example of 'train' looks as follows.

```
{'guid': 'klue-re-v1_train_00000',
 'label': 0,
 'object_entity': {'word': '조지 해리슨',
  'start_idx': 13,
  'end_idx': 18,
  'type': 'PER'},
 'sentence': '〈Something〉는 조지 해리슨이 쓰고 비틀즈가 1969년 앨범 《Abbey Road》에 담은 노래다.',
 'source': 'wikipedia',
 'subject_entity': {'word': '비틀즈',
  'start_idx': 24,
  'end_idx': 26,
  'type': 'ORG'}}
```

#### dp
An example of 'train' looks as follows.

```
{'deprel': ['NP', 'NP_OBJ', 'VP', 'NP', 'NP_SBJ', 'NP', 'NP_MOD', 'NP_CNJ', 'NP_CNJ', 'NP', 'NP', 'NP_OBJ', 'AP', 'VP'],
 'head': [2, 3, 14, 5, 14, 7, 10, 10, 10, 11, 12, 14, 14, 0],
 'index': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14],
 'lemma': ['해당', '그림 을', '보 면', '디즈니', '공주 들 이', '브리트니', '스피어스 의', '앨범 이나', '뮤직 비디오 ,', '화보', '속', '모습 을', '똑같이', '재연 하 였 다 .'],
 'pos': ['NNG', 'NNG+JKO', 'VV+EC', 'NNP', 'NNG+XSN+JKS', 'NNP', 'NNP+JKG', 'NNG+JC', 'NNG+NNG+SP', 'NNG', 'NNG', 'NNG+JKO', 'MAG', 'NNG+XSA+EP+EF+SF'],
 'sentence': '해당 그림을 보면 디즈니 공주들이 브리트니 스피어스의 앨범이나 뮤직비디오, 화보 속 모습을 똑같이 재연했다.',
 'word_form': ['해당', '그림을', '보면', '디즈니', '공주들이', '브리트니', '스피어스의', '앨범이나', '뮤직비디오,', '화보', '속', '모습을', '똑같이', '재연했다.']}
```

#### mrc
An example of 'train' looks as follows.

```
{'answers': {'answer_start': [478, 478], 'text': ['한 달가량', '한 달']},
 'context': '올여름 장마가 17일 제주도에서 시작됐다. 서울 등 중부지방은 예년보다 사나흘 정도 늦은 이달 말께 장마가 시작될 전망이다.17일 기상청에 따르면 제주도 남쪽 먼바다에 있는 장마전선의 영향으로 이날 제주도 산간 및 내륙지역에 호우주의보가 내려지면서 곳곳에 100㎜에 육박하는 많은 비가 내렸다. 제주의 장마는 평년보다 2~3일, 지난해보다는 하루 일찍 시작됐다. 장마는 고온다습한 북태평양 기단과 한랭 습윤한 오호츠크해 기단이 만나 형성되는 장마전선에서 내리는 비를 뜻한다.장마전선은 18일 제주도 먼 남쪽 해상으로 내려갔다가 20일께 다시 북상해 전남 남해안까지 영향을 줄 것으로 보인다. 이에 따라 20~21일 남부지방에도 예년보다 사흘 정도 장마가 일찍 찾아올 전망이다. 그러나 장마전선을 밀어올리는 북태평양 고기압 세력이 약해 서울 등 중부지방은 평년보다 사나흘가량 늦은 이달 말부터 장마가 시작될 것이라는 게 기상청의 설명이다. 장마전선은 이후 한 달가량 한반도 중남부를 오르내리며 곳곳에 비를 뿌릴 전망이다. 최근 30년간 평균치에 따르면 중부지방의 장마 시작일은 6월24~25일이었으며 장마기간은 32일, 강수일수는 17.2일이었다.기상청은 올해 장마기간의 평균 강수량이 350~400㎜로 평년과 비슷하거나 적을 것으로 내다봤다. 브라질 월드컵 한국과 러시아의 경기가 열리는 18일 오전 서울은 대체로 구름이 많이 끼지만 비는 오지 않을 것으로 예상돼 거리 응원에는 지장이 없을 전망이다.',
 'guid': 'klue-mrc-v1_train_12759',
 'is_impossible': False,
 'news_category': '종합',
 'question': '북태평양 기단과 오호츠크해 기단이 만나 국내에 머무르는 기간은?',
 'question_type': 1,
 'source': 'hankyung',
 'title': '제주도 장마 시작 … 중부는 이달 말부터'}
```

#### wos
An example of 'train' looks as follows.

```
{'dialogue': [{'role': 'user',
   'text': '쇼핑을 하려는데 서울 서쪽에 있을까요?',
   'state': ['관광-종류-쇼핑', '관광-지역-서울 서쪽']},
  {'role': 'sys',
   'text': '서울 서쪽에 쇼핑이 가능한 곳이라면 노량진 수산물 도매시장이 있습니다.',
   'state': []},
  {'role': 'user',
   'text': '오 네 거기 주소 좀 알려주세요.',
   'state': ['관광-종류-쇼핑', '관광-지역-서울 서쪽', '관광-이름-노량진 수산물 도매시장']},
  {'role': 'sys', 'text': '노량진 수산물 도매시장의 주소는 서울 동작구 93806입니다.', 'state': []},
  {'role': 'user',
   'text': '알려주시는김에 연락처랑 평점도 좀 알려주세요.',
   'state': ['관광-종류-쇼핑', '관광-지역-서울 서쪽', '관광-이름-노량진 수산물 도매시장']},
  {'role': 'sys', 'text': '그럼. 연락처는 6182006591이고 평점은 4점입니다.', 'state': []},
  {'role': 'user',
   'text': '와 감사합니다.',
   'state': ['관광-종류-쇼핑', '관광-지역-서울 서쪽', '관광-이름-노량진 수산물 도매시장']},
  {'role': 'sys', 'text': '감사합니다.', 'state': []}],
 'domains': ['관광'],
 'guid': 'wos-v1_train_00001'}
```

### Data Fields

#### ynat

+ `guid`: a `string` feature
+ `title`: a `string` feature
+ `label`: a classification label, with possible values `IT과학`(0), `경제`(1), `사회`(2), `생활문화`(3), `세계`(4), `스포츠`(5), `정치`(6)
+ `url`: a `string` feature
+ `date`: a `string` feature

#### sts

+ `guid`: a `string` feature
+ `source`: a `string` feature
+ `sentence1`: a `string` feature
+ `sentence2`: a `string` feature
+ `labels`: a dictionary feature containing
    + `label`: a `float64` feature
    + `real-label`: a `float64` feature
    + `binary-label`: a classification label, with possible values `negative`(0), `positive`(1)
  
#### nli

+ `guid`: a `string` feature
+ `source`: a `string` feature
+ `premise`: a `string` feature
+ `hypothesis`: a `string` feature
+ `label`: a classification label, with possible values `entailment`(0), `neutral`(1), `contradiction`(2)

#### ner

+ `sentence`: a `string` feature
+ `tokens`: a list of a `string` feature (tokenization is at character level)
+ `ner_tags`: a list of classification labels, with possible values including `B-DT`(0), `I-DT`(1), 
  `B-LC`(2), `I-LC`(3), `B-OG`(4), `I-OG`(5), `B-PS`(6), `I-PS`(7), `B-QT`(8), `I-QT`(9), `B-TI`(10), 
  `I-TI`(11), `O`(12)
  
#### re

+ `guid`: a `string` feature
+ `sentence`: a `string` feature
+ `subject_entity`: a dictionary feature containing
    + `word`: a `string` feature
    + `start_idx`: a `int32` feature 
    + `end_idx`: a `int32` feature
    + `type`: a `string` feature
+ `object_entity`: a dictionary feature containing
    + `word`: a `string` feature
    + `start_idx`: a `int32` feature 
    + `end_idx`: a `int32` feature
    + `type`: a `string` feature
+ `label`: a list of labels, with possible values including `no_relation`(0), `org:dissolved`(1), 
  `org:founded`(2), `org:place_of_headquarters`(3), `org:alternate_names`(4), `org:member_of`(5), 
  `org:members`(6), `org:political/religious_affiliation`(7), `org:product`(8), `org:founded_by`(9),`org:top_members/employees`(10), 
  `org:number_of_employees/members`(11), `per:date_of_birth`(12), `per:date_of_death`(13), `per:place_of_birth`(14), 
  `per:place_of_death`(15), `per:place_of_residence`(16), `per:origin`(17), `per:employee_of`(18), 
  `per:schools_attended`(19), `per:alternate_names`(20), `per:parents`(21), `per:children`(22), 
  `per:siblings`(23), `per:spouse`(24), `per:other_family`(25), `per:colleagues`(26), `per:product`(27), 
  `per:religion`(28), `per:title`(29),
+ `source`: a `string` feature

#### dp

+ `sentence`: a `string` feature
+ `index`: a list of `int32` feature 
+ `word_form`: a list of `string` feature
+ `lemma`: a list of `string` feature
+ `pos`: a list of `string` feature
+ `head`: a list of `int32` feature
+ `deprel`: a list of `string` feature


#### mrc

+ `title`: a `string` feature
+ `context`: a `string` feature
+ `news_category`: a `string` feature
+ `source`: a `string` feature
+ `guid`: a `string` feature
+ `is_impossible`: a `bool` feature
+ `question_type`: a `int32` feature
+ `question`: a `string` feature
+ `answers`: a dictionary feature containing
   + `answer_start`: a `int32` feature
   + `text`: a `string` feature
  

#### wos

+ `guid`: a `string` feature
+ `domains`: a `string` feature
+ `dialogue`: a list of dictionary feature containing
  + `role`: a `string` feature
  + `text`: a `string` feature
  + `state`: a `string` feature


### Data Splits

#### ynat

You can see more details in [here](https://klue-benchmark.com/tasks/66/data/description).

+ train: 45,678
+ validation: 9,107


#### sts

You can see more details in [here](https://klue-benchmark.com/tasks/67/data/description).

+ train: 11,668
+ validation: 519

#### nli

You can see more details in [here](https://klue-benchmark.com/tasks/68/data/description).

+ train: 24,998
+ validation: 3,000

#### ner

You can see more details in [here](https://klue-benchmark.com/tasks/69/overview/description).

+ train: 21,008
+ validation: 5,000

#### re

You can see more details in [here](https://klue-benchmark.com/tasks/70/overview/description).

+ train: 32,470
+ validation: 7,765

#### dp

You can see more details in [here](https://klue-benchmark.com/tasks/71/data/description).

+ train: 10,000
+ validation: 2,000

#### mrc

You can see more details in [here](https://klue-benchmark.com/tasks/72/overview/description).

+ train: 17,554
+ validation: 5,841

#### wos

You can see more details in [here](https://klue-benchmark.com/tasks/73/overview/description).

+ train: 8,000
+ validation: 1,000


## Dataset Creation

### Curation Rationale

[Needs More Information]

### Source Data

#### Initial Data Collection and Normalization

[Needs More Information]

#### Who are the source language producers?

[Needs More Information]

### Annotations

#### Annotation process

[Needs More Information]

#### Who are the annotators?

[Needs More Information]

### Personal and Sensitive Information

[Needs More Information]

## Considerations for Using the Data

### Social Impact of Dataset

[Needs More Information]

### Discussion of Biases

[Needs More Information]

### Other Known Limitations

[Needs More Information]

## Additional Information

### Dataset Curators

[Needs More Information]

### Licensing Information

[Needs More Information]

### Citation Information

```
@misc{park2021klue,
      title={KLUE: Korean Language Understanding Evaluation}, 
      author={Sungjoon Park and Jihyung Moon and Sungdong Kim and Won Ik Cho and Jiyoon Han and Jangwon Park and Chisung Song and Junseong Kim and Yongsook Song and Taehwan Oh and Joohong Lee and Juhyun Oh and Sungwon Lyu and Younghoon Jeong and Inkwon Lee and Sangwoo Seo and Dongjun Lee and Hyunwoo Kim and Myeonghwa Lee and Seongbo Jang and Seungwon Do and Sunkyoung Kim and Kyungtae Lim and Jongwon Lee and Kyumin Park and Jamin Shin and Seonghyun Kim and Lucy Park and Alice Oh and Jungwoo Ha and Kyunghyun Cho},
      year={2021},
      eprint={2105.09680},
      archivePrefix={arXiv},
      primaryClass={cs.CL}
}
```
### Contributions

Thanks to [@jungwhank](https://github.com/jungwhank), [@bzantium](https://github.com/bzantium) for adding this dataset.