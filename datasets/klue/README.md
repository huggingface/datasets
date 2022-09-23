---
pretty_name: KLUE
annotations_creators:
- expert-generated
language_creators:
- expert-generated
language:
- ko
license:
- cc-by-sa-4.0
multilinguality:
- monolingual
size_categories:
- 10K<n<100K
source_datasets:
- original
task_categories:
- fill-mask
- question-answering
- text-classification
- text-generation
- token-classification
task_ids:
- extractive-qa
- named-entity-recognition
- natural-language-inference
- other-dialogue-state-tracking
- parsing
- semantic-similarity-scoring
- text-scoring
- token-classification-other-relation-extraction
- topic-classification
paperswithcode_id: klue
configs:
- dp
- mrc
- ner
- nli
- re
- sts
- wos
- ynat
dataset_info:
- config_name: ynat
  features:
  - name: guid
    dtype: string
  - name: title
    dtype: string
  - name: label
    dtype:
      class_label:
        names:
          0: IT과학
          1: 경제
          2: 사회
          3: 생활문화
          4: 세계
          5: 스포츠
          6: 정치
  - name: url
    dtype: string
  - name: date
    dtype: string
  splits:
  - name: train
    num_bytes: 10109664
    num_examples: 45678
  - name: validation
    num_bytes: 2039197
    num_examples: 9107
  download_size: 4932555
  dataset_size: 12148861
- config_name: sts
  features:
  - name: guid
    dtype: string
  - name: source
    dtype: string
  - name: sentence1
    dtype: string
  - name: sentence2
    dtype: string
  - name: labels
    struct:
    - name: label
      dtype: float64
    - name: real-label
      dtype: float64
    - name: binary-label
      dtype:
        class_label:
          names:
            0: negative
            1: positive
  splits:
  - name: train
    num_bytes: 2832921
    num_examples: 11668
  - name: validation
    num_bytes: 122657
    num_examples: 519
  download_size: 1349875
  dataset_size: 2955578
- config_name: nli
  features:
  - name: guid
    dtype: string
  - name: source
    dtype: string
  - name: premise
    dtype: string
  - name: hypothesis
    dtype: string
  - name: label
    dtype:
      class_label:
        names:
          0: entailment
          1: neutral
          2: contradiction
  splits:
  - name: train
    num_bytes: 5719930
    num_examples: 24998
  - name: validation
    num_bytes: 673276
    num_examples: 3000
  download_size: 1257374
  dataset_size: 6393206
- config_name: ner
  features:
  - name: sentence
    dtype: string
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: B-DT
          1: I-DT
          2: B-LC
          3: I-LC
          4: B-OG
          5: I-OG
          6: B-PS
          7: I-PS
          8: B-QT
          9: I-QT
          10: B-TI
          11: I-TI
          12: O
  splits:
  - name: train
    num_bytes: 19891953
    num_examples: 21008
  - name: validation
    num_bytes: 4937579
    num_examples: 5000
  download_size: 4308644
  dataset_size: 24829532
- config_name: re
  features:
  - name: guid
    dtype: string
  - name: sentence
    dtype: string
  - name: subject_entity
    struct:
    - name: word
      dtype: string
    - name: start_idx
      dtype: int32
    - name: end_idx
      dtype: int32
    - name: type
      dtype: string
  - name: object_entity
    struct:
    - name: word
      dtype: string
    - name: start_idx
      dtype: int32
    - name: end_idx
      dtype: int32
    - name: type
      dtype: string
  - name: label
    dtype:
      class_label:
        names:
          0: no_relation
          1: org:dissolved
          2: org:founded
          3: org:place_of_headquarters
          4: org:alternate_names
          5: org:member_of
          6: org:members
          7: org:political/religious_affiliation
          8: org:product
          9: org:founded_by
          10: org:top_members/employees
          11: org:number_of_employees/members
          12: per:date_of_birth
          13: per:date_of_death
          14: per:place_of_birth
          15: per:place_of_death
          16: per:place_of_residence
          17: per:origin
          18: per:employee_of
          19: per:schools_attended
          20: per:alternate_names
          21: per:parents
          22: per:children
          23: per:siblings
          24: per:spouse
          25: per:other_family
          26: per:colleagues
          27: per:product
          28: per:religion
          29: per:title
  - name: source
    dtype: string
  splits:
  - name: train
    num_bytes: 11145538
    num_examples: 32470
  - name: validation
    num_bytes: 2559300
    num_examples: 7765
  download_size: 5669259
  dataset_size: 13704838
- config_name: dp
  features:
  - name: sentence
    dtype: string
  - name: index
    list: int32
  - name: word_form
    list: string
  - name: lemma
    list: string
  - name: pos
    list: string
  - name: head
    list: int32
  - name: deprel
    list: string
  splits:
  - name: train
    num_bytes: 7900009
    num_examples: 10000
  - name: validation
    num_bytes: 1557506
    num_examples: 2000
  download_size: 2033461
  dataset_size: 9457515
- config_name: mrc
  features:
  - name: title
    dtype: string
  - name: context
    dtype: string
  - name: news_category
    dtype: string
  - name: source
    dtype: string
  - name: guid
    dtype: string
  - name: is_impossible
    dtype: bool
  - name: question_type
    dtype: int32
  - name: question
    dtype: string
  - name: answers
    sequence:
    - name: answer_start
      dtype: int32
    - name: text
      dtype: string
  splits:
  - name: train
    num_bytes: 46505665
    num_examples: 17554
  - name: validation
    num_bytes: 15583053
    num_examples: 5841
  download_size: 19218422
  dataset_size: 62088718
- config_name: wos
  features:
  - name: guid
    dtype: string
  - name: domains
    list: string
  - name: dialogue
    list:
    - name: role
      dtype: string
    - name: text
      dtype: string
    - name: state
      list: string
  splits:
  - name: train
    num_bytes: 26677002
    num_examples: 8000
  - name: validation
    num_bytes: 3488943
    num_examples: 1000
  download_size: 4785657
  dataset_size: 30165945
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