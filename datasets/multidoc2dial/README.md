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
- open-domain-qa
paperswithcode_id: multidoc2dial
---

# Dataset Card for MultiDoc2Dial

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

- **Homepage:** https://doc2dial.github.io/multidoc2dial/
- **Repository:** https://github.com/IBM/multidoc2dial
- **Paper:** https://arxiv.org/pdf/2109.12595.pdf
- **Leaderboard:**
- **Point of Contact:** sngfng@gmail.com

### Dataset Summary

MultiDoc2Dial is a new task and dataset on modeling goal-oriented dialogues grounded in multiple documents. 
Most previous works treat document-grounded dialogue modeling as a machine reading comprehension task based on a
single given document or passage. We aim to address more realistic scenarios where a goal-oriented information-seeking
conversation involves multiple topics, and hence is grounded on different documents. 

[comment]: <> (### Supported Tasks and Leaderboards)

[comment]: <> (> Supported Task: [Shared Task]&#40;https://doc2dial.github.io/workshop2021/shared.html&#41; hosted by DialDoc21 at ACL.)

[comment]: <> (> Leaderboard: [LINK]&#40;https://eval.ai/web/challenges/challenge-page/793&#41;)

### Languages

English

## Dataset Structure

### Data Instances

Sample data instance for `dialogue_domain` :

```
{
    "dial_data": {
        "dmv": [
            {
                "dial_id": "1409501a35697e0ce68561e29577b90a",
                "turns": [
                    {
                        "da": "query_condition",
                        "references": [
                            {
                                "label": "precondition",
                                "sp_id": "23",
                                "doc_id": "Top 5 DMV Mistakes and How to Avoid Them#3_0"
                            }
                        ],
                        "role": "user",
                        "turn_id": 1,
                        "utterance": "My insurance ended so what should i do"
                    },
                    {
                        "da": "respond_solution",
                        "references": [
                            {
                                "label": "solution",
                                "sp_id": "24",
                                "doc_id": "Top 5 DMV Mistakes and How to Avoid Them#3_0"
                            },
                            {
                                "label": "solution",
                                "sp_id": "25",
                                "doc_id": "Top 5 DMV Mistakes and How to Avoid Them#3_0"
                            },
                            {
                                "label": "solution",
                                "sp_id": "26",
                                "doc_id": "Top 5 DMV Mistakes and How to Avoid Them#3_0"
                            }
                        ],
                        "role": "agent",
                        "turn_id": 2,
                        "utterance": "You will need to get insurance or we will suspend your registration and license"
                    },
                    {
                        "da": "query_condition",
                        "references": [
                            {
                                "label": "precondition",
                                "sp_id": "28",
                                "doc_id": "Top 5 DMV Mistakes and How to Avoid Them#3_0"
                            }
                        ],
                        "role": "user",
                        "turn_id": 3,
                        "utterance": "Don't do that I'll get insurance"
                    },
                    {
                        "da": "respond_solution",
                        "references": [
                            {
                                "label": "solution",
                                "sp_id": "29",
                                "doc_id": "Top 5 DMV Mistakes and How to Avoid Them#3_0"
                            }
                        ],
                        "role": "agent",
                        "turn_id": 4,
                        "utterance": "Okay, have you received a letter from the DMV letting you know how to clear things up?"
                    },
                    {
                        "da": "query_solution",
                        "references": [
                            {
                                "label": "solution",
                                "sp_id": "13",
                                "doc_id": "Top 5 DMV Mistakes and How to Avoid Them#3_0"
                            }
                        ],
                        "role": "user",
                        "turn_id": 5,
                        "utterance": "I have, that is why I am here to clear that up and change the address on my license and registration"
                    },
                    {
                        "da": "respond_solution",
                        "references": [
                            {
                                "label": "solution",
                                "sp_id": "13",
                                "doc_id": "Top 5 DMV Mistakes and How to Avoid Them#3_0"
                            }
                        ],
                        "role": "agent",
                        "turn_id": 6,
                        "utterance": "Okay, we can take care of that"
                    },
                    {
                        "da": "query_condition",
                        "references": [
                            {
                                "label": "precondition",
                                "sp_id": "24",
                                "doc_id": "Help finding enough proof of ID#3_0"
                            }
                        ],
                        "role": "user",
                        "turn_id": 7,
                        "utterance": "Thank you so much. After looking through these requirements that I need to bring to DMV, can you tell me whether a GED certificate will be a valid proof of identification?"
                    },
                    {
                        "da": "respond_solution",
                        "references": [
                            {
                                "label": "solution",
                                "sp_id": "25",
                                "doc_id": "Help finding enough proof of ID#3_0"
                            },
                            {
                                "label": "solution",
                                "sp_id": "26",
                                "doc_id": "Help finding enough proof of ID#3_0"
                            },
                            {
                                "label": "solution",
                                "sp_id": "27",
                                "doc_id": "Help finding enough proof of ID#3_0"
                            }
                        ],
                        "role": "agent",
                        "turn_id": 8,
                        "utterance": "Sure, it is. You can contact your college and get a certified copy."
                    },
                    {
                        "da": "query_solution",
                        "references": [
                            {
                                "label": "solution",
                                "sp_id": "14",
                                "doc_id": "Help finding enough proof of ID#3_0"
                            },
                            {
                                "label": "solution",
                                "sp_id": "15",
                                "doc_id": "Help finding enough proof of ID#3_0"
                            },
                            {
                                "label": "solution",
                                "sp_id": "16",
                                "doc_id": "Help finding enough proof of ID#3_0"
                            }
                        ],
                        "role": "user",
                        "turn_id": 9,
                        "utterance": "Great. I think that I can found some bills, of some services, would that help too?"
                    },
                    {
                        "da": "respond_solution",
                        "references": [
                            {
                                "label": "solution",
                                "sp_id": "14",
                                "doc_id": "Help finding enough proof of ID#3_0"
                            },
                            {
                                "label": "solution",
                                "sp_id": "15",
                                "doc_id": "Help finding enough proof of ID#3_0"
                            },
                            {
                                "label": "solution",
                                "sp_id": "16",
                                "doc_id": "Help finding enough proof of ID#3_0"
                            }
                        ],
                        "role": "agent",
                        "turn_id": 10,
                        "utterance": "Yes, as long as they be a phone, electricity, gas, water or cable bill."
                    },
                    {
                        "da": "query_condition",
                        "references": [
                            {
                                "label": "precondition",
                                "sp_id": "35",
                                "doc_id": "Help finding enough proof of ID#3_0"
                            }
                        ],
                        "role": "user",
                        "turn_id": 11,
                        "utterance": "Can I use my union card?"
                    },
                    {
                        "da": "respond_solution",
                        "references": [
                            {
                                "label": "solution",
                                "sp_id": "36",
                                "doc_id": "Help finding enough proof of ID#3_0"
                            },
                            {
                                "label": "solution",
                                "sp_id": "37",
                                "doc_id": "Help finding enough proof of ID#3_0"
                            },
                            {
                                "label": "solution",
                                "sp_id": "38",
                                "doc_id": "Help finding enough proof of ID#3_0"
                            }
                        ],
                        "role": "agent",
                        "turn_id": 12,
                        "utterance": "Yes, it's also a valid document, no matter if you have no longer that union job."
                    }
                ]
            }
        ]
    }
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







### Data Fields

- **multidoc2dial_doc.json** contains the documents that are indexed by key `domain` and `doc_id` . Each document instance includes the following,

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

- **multidoc2dial_dial_train.json** and **multidoc2dial_dial_validation.json**  contain the training and dev split of dialogue data that are indexed by key `domain` . Please note: **For test split, we only include a dummy file in this version.**

  Each dialogue instance includes the following,

  - `dial_id`: the ID of a dialogue;
  - `turns`: a list of dialogue turns. Each turn includes,
    - `turn_id`: the time order of the turn;
    - `role`: either "agent" or "user";READ
    - `da`: dialogue act;
    - `references`: a list of spans with `id_sp` ,  `label` and `doc_id`. `references` is empty if a turn is for indicating previous user query not answerable or irrelevant to the document. **Note** that labels "*precondition*"/"*solution*" are fuzzy annotations that indicate whether a span is for describing a conditional context or a solution.
    - `utterance`: the human-generated utterance based on the dialogue scene.

### Data Splits

- Training & dev split for dialogue domain
- Training split only for document domain

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

Song Feng, Siva Sankalp Patel, Hui Wan, Sachindra Joshi

### Licensing Information

Creative Commons Attribution 3.0 Unported

### Citation Information

@inproceedings{feng2021multidoc2dial,
    title={MultiDoc2Dial: Modeling Dialogues Grounded in Multiple Documents},
    author={Feng, Song and Patel, Siva Sankalp and Wan, Hui and Joshi, Sachindra},
    booktitle={EMNLP},
    year={2021}
}

### Contributions

[@songfeng](https://github.com/songfeng) and [@sivasankalpp](https://github.com/sivasankalpp) added this dataset.