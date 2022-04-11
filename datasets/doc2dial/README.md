---
annotations_creators:
- expert-generated
language_creators:
- found
languages:
- en
licenses:
- cc-by-3.0
multilinguality:
- monolingual
size_categories:
- 1K<n<10K
source_datasets:
- original
task_categories:
- question-answering
task_ids:
- closed-domain-qa
paperswithcode_id: doc2dial
pretty_name: doc2dial
---

# Dataset Card for doc2dial

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

- **Homepage:** https://doc2dial.github.io
- **Repository:** [Needs More Information]
- **Paper:** https://www.aclweb.org/anthology/2020.emnlp-main.652.pdf
- **Leaderboard:**
- **Point of Contact:**

### Dataset Summary

Doc2dial is dataset of goal-oriented dialogues that are grounded in the associated documents. It includes over 4500 annotated conversations with an average of 14 turns that are grounded in over 450 documents from four domains. Compared to the prior document-grounded dialogue datasets this dataset covers a variety of dialogue scenes in information-seeking conversations.

### Supported Tasks and Leaderboards

> Supported Task: [Shared Task](https://doc2dial.github.io/workshop2021/shared.html) hosted by DialDoc21 at ACL.

> Leaderboard: [LINK](https://eval.ai/web/challenges/challenge-page/793)

### Languages

English

## Dataset Structure

### Data Instances

Sample data instance for `dialogue_domain` :

```
{
    "dial_id": "9f44c1539efe6f7e79b02eb1b413aa43",
    "doc_id": "Top 5 DMV Mistakes and How to Avoid Them#3_0",
    "domain": "dmv",
    "turns": [
        {
            "da": "query_condition",
            "references": [
                {
                    "sp_id": "4",
                    "label": "precondition"
                }
            ],
            "role": "user",
            "turn_id": 1,
            "utterance": "Hello, I forgot o update my address, can you help me with that?"
        },
        {
            "da": "response_solution",
            "references": [
                {
                    "sp_id": "6",
                    "label": "solution"
                },
                {
                    "sp_id": "7",
                    "label": "solution"
                },
                {
                    "sp_id": "4",
                    "label": "references"
                }
            ],
            "role": "agent",
            "turn_id": 2,
            "utterance": "hi, you have to report any change of address to DMV within 10 days after moving. You should do this both for the address associated with your license and all the addresses associated with all your vehicles."
        },
        {
            "da": "query_solution",
            "references": [
                {
                    "sp_id": "56",
                    "label": "solution"
                },
                {
                    "sp_id": "48",
                    "label": "references"
                }
            ],
            "role": "user",
            "turn_id": 3,
            "utterance": "Can I do my DMV transactions online?"
        },
        {
            "da": "respond_solution",
            "references": [
                {
                    "sp_id": "56",
                    "label": "solution"
                },
                {
                    "sp_id": "48",
                    "label": "references"
                }
            ],
            "role": "agent",
            "turn_id": 4,
            "utterance": "Yes, you can sign up for MyDMV for all the online transactions needed."
        },
        {
            "da": "query_condition",
            "references": [
                {
                    "sp_id": "48",
                    "label": "precondition"
                }
            ],
            "role": "user",
            "turn_id": 5,
            "utterance": "Thanks, and in case I forget to bring all of the documentation needed to the DMV office, what can I do?"
        },
        {
            "da": "respond_solution",
            "references": [
                {
                    "sp_id": "49",
                    "label": "solution"
                },
                {
                    "sp_id": "50",
                    "label": "solution"
                },
                {
                    "sp_id": "52",
                    "label": "solution"
                },
                {
                    "sp_id": "48",
                    "label": "references"
                }
            ],
            "role": "agent",
            "turn_id": 6,
            "utterance": "This happens often with our customers so that's why our website and MyDMV are so useful for our customers. Just check if you can make your transaction online so you don't have to go to the DMV Office."
        },
        {
            "da": "query_solution",
            "references": [
                {
                    "sp_id": "6",
                    "label": "solution"
                },
                {
                    "sp_id": "7",
                    "label": "solution"
                },
                {
                    "sp_id": "4",
                    "label": "references"
                }
            ],
            "role": "user",
            "turn_id": 7,
            "utterance": "Ok, and can you tell me again where should I report my new address?"
        },
        {
            "da": "respond_solution",
            "references": [
                {
                    "sp_id": "6",
                    "label": "solution"
                },
                {
                    "sp_id": "7",
                    "label": "solution"
                },
                {
                    "sp_id": "4",
                    "label": "references"
                }
            ],
            "role": "agent",
            "turn_id": 8,
            "utterance": "Sure. Any change of address must be reported to the DMV, that's for the address associated with your license and any of your vehicles."
        },
        {
            "da": "query_condition",
            "references": [
                {
                    "sp_id": "40",
                    "label": "precondition"
                }
            ],
            "role": "user",
            "turn_id": 9,
            "utterance": "Can you tell me more about Traffic points and their cost?"
        },
        {
            "da": "respond_solution",
            "references": [
                {
                    "sp_id": "41",
                    "label": "solution"
                },
                {
                    "sp_id": "43",
                    "label": "solution"
                },
                {
                    "sp_id": "40",
                    "label": "references"
                }
            ],
            "role": "agent",
            "turn_id": 10,
            "utterance": "Traffic points is the system used by DMV to track dangerous drivers. The cost of the traffic points is independent of the DRA, so you get a separate charge based on the total points you accumulate."
        }
    ]
}
```



Sample data instance for `document_domain` :

```
{
    "doc_id": "Benefits Planner: Retirement | Online Calculator (WEP Version)#1_0",
    "domain": "ssa",
    "doc_html_raw": "<main class=\"content\" id=\"content\" role=\"main\">\n\n<section>\n\n<div>\n<h2>\nBenefits Planner: Retirement\n</h2>\n</div>\n</section>\n\n\n<section>\n\n<div>\n\n<div>\n\n\n</div>\n\n<article>\n<section>\n\n<h3>Online Calculator (WEP Version)</h3>\n<p>The calculator shown below allows you to estimate your Social Security benefit.\nHowever, for the most accurate estimates, <a>use the Detailed Calculator</a>.</p>\n<p>You need to enter all your past earnings\n, which are shown on your <a>online </a>.</p>\n\n<p>Please Note:</p>\n<ul class=\"browser-default\">\n<li>The Online Calculator is updated periodically<span>*</span> with new benefit increases and other benefit amounts. Therefore, it is likely that your benefit estimates in the future will differ from those calculated today.</li>\n<li>The Online Calculator works on PCs and Macs with Javascript enabled.</li>\n<li>Some browsers may not allow you to print the table below. </li>\n</ul>\n<p></p>\n\n<div>\nThe Online Calculator temporarily stores information on your local computer while your browser is open. To protect your personal information, you should close your browser after you have finished your estimate.\n</div>\n<p></p>\n\n<div>\n<p>Note: If your birthday is on January 1st, we figure your benefit as if your birthday was in the previous year.</p>\n<p>If you qualify for benefits as a Survivor, your <a>full retirement age for survivors benefits</a> may be different.</p></div>\n\n<div>\n</div></section></article></div></section></main>",
    "doc_html_ts": "<main><section><div><h2 sent_id=\"1\" text_id=\"1\">Benefits Planner: Retirement</h2></div></section><section><div><article><section><h3 sent_id=\"2\" text_id=\"2\">Online Calculator (WEP Version)</h3><div tag_id=\"1\"><u sent_id=\"3\" tag_id=\"1\"><u sent_id=\"3\" tag_id=\"1\" text_id=\"3\">The calculator shown below allows you to estimate your Social Security benefit .</u></u><u sent_id=\"4\" tag_id=\"1\"><u sent_id=\"4\" tag_id=\"1\" text_id=\"4\">However ,</u><u sent_id=\"4\" tag_id=\"1\" text_id=\"5\">for the most accurate estimates ,</u><u sent_id=\"4\" tag_id=\"1\" text_id=\"6\">use the Detailed Calculator .</u></u></div><div tag_id=\"2\"><u sent_id=\"5\" tag_id=\"2\"><u sent_id=\"5\" tag_id=\"2\" text_id=\"7\">You need to enter all your past earnings , which are shown on your online .</u></u></div><div tag_id=\"3\"><u sent_id=\"6\" tag_id=\"3\"><u sent_id=\"6\" tag_id=\"3\" text_id=\"8\">Please Note:</u></u></div><ul class=\"browser-default\" tag_id=\"3\"><li tag_id=\"3\"><div tag_id=\"3\"><u sent_id=\"9\" tag_id=\"3\"><u sent_id=\"9\" tag_id=\"3\" text_id=\"9\">The Online Calculator is updated periodically * with new benefit increases and other benefit amounts .</u></u><u sent_id=\"10\" tag_id=\"3\"><u sent_id=\"10\" tag_id=\"3\" text_id=\"10\">Therefore ,</u><u sent_id=\"10\" tag_id=\"3\" text_id=\"11\">it is likely that your benefit estimates in the future will differ from those calculated today .</u></u></div></li><li tag_id=\"3\"><u sent_id=\"11\" tag_id=\"3\"><u sent_id=\"11\" tag_id=\"3\" text_id=\"12\">The Online Calculator works on PCs and Macs with Javascript enabled .</u></u></li><li tag_id=\"3\"><u sent_id=\"12\" tag_id=\"3\"><u sent_id=\"12\" tag_id=\"3\" text_id=\"13\">Some browsers may not allow you to print the table below .</u></u></li></ul><div>The Online Calculator temporarily stores information on your local computer while your browser is open. To protect your personal information, you should close your browser after you have finished your estimate.</div><div><div tag_id=\"4\"><u sent_id=\"13\" tag_id=\"4\"><u sent_id=\"13\" tag_id=\"4\" text_id=\"14\">Note:</u></u><u sent_id=\"14\" tag_id=\"4\"><u sent_id=\"14\" tag_id=\"4\" text_id=\"15\">If your birthday is on January 1st ,</u><u sent_id=\"14\" tag_id=\"4\" text_id=\"16\">we figure your benefit as if your birthday was in the previous year .</u></u></div><div tag_id=\"5\"><u sent_id=\"15\" tag_id=\"5\"><u sent_id=\"15\" tag_id=\"5\" text_id=\"17\">If you qualify for benefits as a Survivor ,</u><u sent_id=\"15\" tag_id=\"5\" text_id=\"18\">your full retirement age for survivors benefits may be different .</u></u></div></div></section></article></div></section></main>",
    "doc_text": "\n\nBenefits Planner: Retirement \n\n\nOnline Calculator (WEP Version) \nThe calculator shown below allows you to estimate your Social Security benefit. However , for the most accurate estimates , use the Detailed Calculator. You need to enter all your past earnings, which are shown on your online. Please Note: The Online Calculator is updated periodically * with new benefit increases and other benefit amounts. Therefore , it is likely that your benefit estimates in the future will differ from those calculated today. The Online Calculator works on PCs and Macs with Javascript enabled. Some browsers may not allow you to print the table below. Note: If your birthday is on January 1st , we figure your benefit as if your birthday was in the previous year. If you qualify for benefits as a Survivor , your full retirement age for survivors benefits may be different. ",
    "title": "Benefits Planner: Retirement | Online Calculator (WEP Version)#1",
    "spans": [
        {
            "end_sec": 32,
            "end_sp": 32,
            "id_sec": "t_0",
            "id_sp": "1",
            "parent_titles": "[]",
            "start_sec": 0,
            "start_sp": 0,
            "tag": "h2",
            "text_sec": "\n\nBenefits Planner: Retirement \n",
            "text_sp": "\n\nBenefits Planner: Retirement \n",
            "title": "Benefits Planner: Retirement"
        },
        {
            "end_sec": 67,
            "end_sp": 67,
            "id_sec": "t_1",
            "id_sp": "2",
            "parent_titles": "[{'id_sp': '1', 'text': 'Benefits Planner: Retirement', 'level': 'h2'}]",
            "start_sec": 32,
            "start_sp": 32,
            "tag": "h3",
            "text_sec": "\n\nOnline Calculator (WEP Version) \n",
            "text_sp": "\n\nOnline Calculator (WEP Version) \n",
            "title": "Online Calculator (WEP Version)"
        },
        {
            "end_sec": 220,
            "end_sp": 147,
            "id_sec": "1",
            "id_sp": "3",
            "parent_titles": "[]",
            "start_sec": 67,
            "start_sp": 67,
            "tag": "u",
            "text_sec": "The calculator shown below allows you to estimate your Social Security benefit. However , for the most accurate estimates , use the Detailed Calculator. ",
            "text_sp": "The calculator shown below allows you to estimate your Social Security benefit. ",
            "title": "Online Calculator (WEP Version)"
        }
    ]
}
```

Sample data instance for `doc2dial_rc` :

```
{
    "id": "78f72b08b43791a4a70363fe62b8de08_1",
    "is_impossible": false,
    "question": "Hello, I want to know about the retirement plan.",
    "answers": {
        "answer_start": [
            0
        ],
        "text": [
            "\n\nBenefits Planner: Retirement \n\n\nOnline Calculator (WEP Version) \n"
        ]
    },
    "context": "\n\nBenefits Planner: Retirement \n\n\nOnline Calculator (WEP Version) \nThe calculator shown below allows you to estimate your Social Security benefit. However , for the most accurate estimates , use the Detailed Calculator. You need to enter all your past earnings, which are shown on your online. Please Note: The Online Calculator is updated periodically * with new benefit increases and other benefit amounts. Therefore , it is likely that your benefit estimates in the future will differ from those calculated today. The Online Calculator works on PCs and Macs with Javascript enabled. Some browsers may not allow you to print the table below. Note: If your birthday is on January 1st , we figure your benefit as if your birthday was in the previous year. If you qualify for benefits as a Survivor , your full retirement age for survivors benefits may be different. ",
    "title": "Benefits Planner: Retirement | Online Calculator (WEP Version)#1_0",
    "domain": "ssa"
}
```







### Data Fields

For `document_domain`,

- `doc_id`: the ID of a document;
- `title`: the title of the document;
- `domain`: the domain of the document;
- `doc_text`: the text content of the document (without HTML markups);
- `doc_html_ts`: the document content with HTML markups and the annotated spans that are indicated by `text_id` attribute, which corresponds to `id_sp`.
- `doc_html_raw`: the document content with HTML markups and without span annotations.
- `spans`: key-value pairs of all spans in the document, with `id_sp` as key. Each span includes the following,
  - `id_sp`: the id of a  span as noted by `text_id` in  `doc_html_ts`;
  - `start_sp`/  `end_sp`: the start/end position of the text span in `doc_text`;
  - `text_sp`: the text content of the span.
  - `id_sec`: the id of the (sub)section (e.g. `<p>`) or title (`<h2>`) that contains the span.
  - `start_sec` / `end_sec`: the start/end position of the (sub)section in `doc_text`.
  - `text_sec`: the text of the (sub)section.
  - `title`: the title of the (sub)section.
  - `parent_titles`: the parent titles of the `title`.



For `dialogue_domain`:

- `dial_id`: the ID of a dialogue;
- `doc_id`: the ID of the associated document;
- `domain`: domain of the document;
- `turns`: a list of dialogue turns. Each turn includes,
  - `turn_id`: the time order of the turn;
  - `role`: either "agent" or "user";
  - `da`: dialogue act;
  - `references`: the grounding span (`id_sp`) in the associated document. If a turn is an irrelevant turn, i.e., `da` ends with "ood", `reference` is empty.  **Note** that spans with labels "*precondition*"/"*solution*" are the actual grounding spans. Spans with label "*reference*" are the related titles or contextual reference,  which is used for the purpose of describing a dialogue scene better to crowd contributors.
  - `utterance`: the human-generated utterance based on the dialogue scene.



For `doc2dial_rc`, this conforms to [SQuAD](https://rajpurkar.github.io/SQuAD-explorer/) data format. For how to load Doc2Dial data for reading comprehension task, please refer [here](https://github.com/doc2dial/sharedtask-dialdoc2021).

- `id`: the ID of a QA instance;
- `question`: user query;
- `answers`: the answers that are grounded in the associated document;
  - `answer_start`: the start position of the grounding span in the associated document (`context`);
  - `text`: the text content of the grounding span;
- `title`: the title of the associated document;
- `domain`: the domain of the associated document;
- `context`: the text content of the associated document (without HTML markups).



### Data Splits

Training & dev split for dialogue domain
Training split only for document domain

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

Song Feng, Hui Wan, Chulaka Gunasekara, Siva Sankalp Patel,Sachindra Joshi. Luis A. Lastras

### Licensing Information

Creative Commons Attribution 3.0 Unported

### Citation Information

@inproceedings{feng-etal-2020-doc2dial,
    title = "doc2dial: A Goal-Oriented Document-Grounded Dialogue Dataset",
    author = "Feng, Song  and Wan, Hui  and Gunasekara, Chulaka  and Patel, Siva  and Joshi, Sachindra  and Lastras, Luis",
    booktitle = "Proceedings of the 2020 Conference on Empirical Methods in Natural Language Processing (EMNLP)",
    month = nov,
    year = "2020",
    publisher = "Association for Computational Linguistics",
    url = "https://www.aclweb.org/anthology/2020.emnlp-main.652",
}

### Contributions

Thanks to [@songfeng](https://github.com/songfeng), [@KMFODA](https://github.com/KMFODA) for adding this dataset.