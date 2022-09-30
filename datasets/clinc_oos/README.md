---
annotations_creators:
- expert-generated
language_creators:
- crowdsourced
language:
- en
license:
- cc-by-3.0
multilinguality:
- monolingual
size_categories:
- 10K<n<100K
source_datasets:
- original
task_categories:
- text-classification
task_ids:
- intent-classification
paperswithcode_id: clinc150
pretty_name: CLINC150
---

# Dataset Card for CLINC150

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

- **Homepage:** [Github](https://github.com/clinc/oos-eval/)
- **Repository:** [Github](https://github.com/clinc/oos-eval/)
- **Paper:** [Aclweb](https://www.aclweb.org/anthology/D19-1131)
- **Leaderboard:** [PapersWithCode](https://paperswithcode.com/sota/text-classification-on-clinc-oos)
- **Point of Contact:**

### Dataset Summary

Task-oriented dialog systems need to know when a query falls outside their range of supported intents, but current text classification corpora only define label sets that cover every example. We introduce a new dataset that includes queries that are out-of-scope (OOS), i.e., queries that do not fall into any of the system's supported intents. This poses a new challenge because models cannot assume that every query at inference time belongs to a system-supported intent class. Our dataset also covers 150 intent classes over 10 domains, capturing the breadth that a production task-oriented agent must handle. It offers a way of more rigorously and realistically benchmarking text classification in task-driven dialog systems.

### Supported Tasks and Leaderboards

- `intent-classification`: This dataset is for evaluating the performance of intent classification systems in the presence of "out-of-scope" queries, i.e., queries that do not fall into any of the system-supported intent classes. The dataset includes both in-scope and out-of-scope data. [here](https://paperswithcode.com/sota/text-classification-on-clinc-oos).

### Languages

English

## Dataset Structure

### Data Instances

A sample from the training set is provided below:
```
{
    'text' : 'can you walk me through setting up direct deposits to my bank of internet savings account',
    'label' : 108 
}
```

### Data Fields

- text : Textual data
- label : 150 intent classes over 10 domains, the dataset contains one label for 'out-of-scope' intent. 

The Label Id to Label Name map is mentioned in the table below:

| **Label Id** 	| **Label name** 	|
|---	|---	|
| 0 	| restaurant_reviews 	|
| 1 	| nutrition_info 	|
| 2 	| account_blocked 	|
| 3 	| oil_change_how 	|
| 4 	| time 	|
| 5 	| weather 	|
| 6 	| redeem_rewards 	|
| 7 	| interest_rate 	|
| 8 	| gas_type 	|
| 9 	| accept_reservations 	|
| 10 	| smart_home 	|
| 11 	| user_name 	|
| 12 	| report_lost_card 	|
| 13 	| repeat 	|
| 14 	| whisper_mode 	|
| 15 	| what_are_your_hobbies 	|
| 16 	| order 	|
| 17 	| jump_start 	|
| 18 	| schedule_meeting 	|
| 19 	| meeting_schedule 	|
| 20 	| freeze_account 	|
| 21 	| what_song 	|
| 22 	| meaning_of_life 	|
| 23 	| restaurant_reservation 	|
| 24 	| traffic 	|
| 25 	| make_call 	|
| 26 	| text 	|
| 27 	| bill_balance 	|
| 28 	| improve_credit_score 	|
| 29 	| change_language 	|
| 30 	| no 	|
| 31 	| measurement_conversion 	|
| 32 	| timer 	|
| 33 	| flip_coin 	|
| 34 	| do_you_have_pets 	|
| 35 	| balance 	|
| 36 	| tell_joke 	|
| 37 	| last_maintenance 	|
| 38 	| exchange_rate 	|
| 39 	| uber 	|
| 40 	| car_rental 	|
| 41 	| credit_limit 	|
| 42 	| oos 	|
| 43 	| shopping_list 	|
| 44 	| expiration_date 	|
| 45 	| routing 	|
| 46 	| meal_suggestion 	|
| 47 	| tire_change 	|
| 48 	| todo_list 	|
| 49 	| card_declined 	|
| 50 	| rewards_balance 	|
| 51 	| change_accent 	|
| 52 	| vaccines 	|
| 53 	| reminder_update 	|
| 54 	| food_last 	|
| 55 	| change_ai_name 	|
| 56 	| bill_due 	|
| 57 	| who_do_you_work_for 	|
| 58 	| share_location 	|
| 59 	| international_visa 	|
| 60 	| calendar 	|
| 61 	| translate 	|
| 62 	| carry_on 	|
| 63 	| book_flight 	|
| 64 	| insurance_change 	|
| 65 	| todo_list_update 	|
| 66 	| timezone 	|
| 67 	| cancel_reservation 	|
| 68 	| transactions 	|
| 69 	| credit_score 	|
| 70 	| report_fraud 	|
| 71 	| spending_history 	|
| 72 	| directions 	|
| 73 	| spelling 	|
| 74 	| insurance 	|
| 75 	| what_is_your_name 	|
| 76 	| reminder 	|
| 77 	| where_are_you_from 	|
| 78 	| distance 	|
| 79 	| payday 	|
| 80 	| flight_status 	|
| 81 	| find_phone 	|
| 82 	| greeting 	|
| 83 	| alarm 	|
| 84 	| order_status 	|
| 85 	| confirm_reservation 	|
| 86 	| cook_time 	|
| 87 	| damaged_card 	|
| 88 	| reset_settings 	|
| 89 	| pin_change 	|
| 90 	| replacement_card_duration 	|
| 91 	| new_card 	|
| 92 	| roll_dice 	|
| 93 	| income 	|
| 94 	| taxes 	|
| 95 	| date 	|
| 96 	| who_made_you 	|
| 97 	| pto_request 	|
| 98 	| tire_pressure 	|
| 99 	| how_old_are_you 	|
| 100 	| rollover_401k 	|
| 101 	| pto_request_status 	|
| 102 	| how_busy 	|
| 103 	| application_status 	|
| 104 	| recipe 	|
| 105 	| calendar_update 	|
| 106 	| play_music 	|
| 107 	| yes 	|
| 108 	| direct_deposit 	|
| 109 	| credit_limit_change 	|
| 110 	| gas 	|
| 111 	| pay_bill 	|
| 112 	| ingredients_list 	|
| 113 	| lost_luggage 	|
| 114 	| goodbye 	|
| 115 	| what_can_i_ask_you 	|
| 116 	| book_hotel 	|
| 117 	| are_you_a_bot 	|
| 118 	| next_song 	|
| 119 	| change_speed 	|
| 120 	| plug_type 	|
| 121 	| maybe 	|
| 122 	| w2 	|
| 123 	| oil_change_when 	|
| 124 	| thank_you 	|
| 125 	| shopping_list_update 	|
| 126 	| pto_balance 	|
| 127 	| order_checks 	|
| 128 	| travel_alert 	|
| 129 	| fun_fact 	|
| 130 	| sync_device 	|
| 131 	| schedule_maintenance 	|
| 132 	| apr 	|
| 133 	| transfer 	|
| 134 	| ingredient_substitution 	|
| 135 	| calories 	|
| 136 	| current_location 	|
| 137 	| international_fees 	|
| 138 	| calculator 	|
| 139 	| definition 	|
| 140 	| next_holiday 	|
| 141 	| update_playlist 	|
| 142 	| mpg 	|
| 143 	| min_payment 	|
| 144 	| change_user_name 	|
| 145 	| restaurant_suggestion 	|
| 146 	| travel_notification 	|
| 147 	| cancel 	|
| 148 	| pto_used 	|
| 149 	| travel_suggestion 	|
| 150 	| change_volume 	|

### Data Splits

The dataset comes in different subsets:

- `small` : Small, in which there are only 50 training queries per each in-scope intent
- `imbalanced` : Imbalanced, in which intents have either 25, 50, 75, or 100 training queries.
- `plus`: OOS+, in which there are 250 out-of-scope training examples, rather than 100.


|   name   |train|validation|test|
|----------|----:|---------:|---:|
|small|7600|     3100|  5500 |
|imbalanced|10625|     3100|   5500|
|plus|15250|     3100|   5500|



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

[More Information Needed]

### Citation Information
```
@inproceedings{larson-etal-2019-evaluation,
    title = "An Evaluation Dataset for Intent Classification and Out-of-Scope Prediction",
    author = "Larson, Stefan  and
      Mahendran, Anish  and
      Peper, Joseph J.  and
      Clarke, Christopher  and
      Lee, Andrew  and
      Hill, Parker  and
      Kummerfeld, Jonathan K.  and
      Leach, Kevin  and
      Laurenzano, Michael A.  and
      Tang, Lingjia  and
      Mars, Jason",
    booktitle = "Proceedings of the 2019 Conference on Empirical Methods in Natural Language Processing and the 9th International Joint Conference on Natural Language Processing (EMNLP-IJCNLP)",
    year = "2019",
    url = "https://www.aclweb.org/anthology/D19-1131"
}
```
### Contributions

Thanks to [@sumanthd17](https://github.com/sumanthd17) for adding this dataset.
