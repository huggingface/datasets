---
annotations_creators:
- no-annotation
language_creators:
- crowdsourced
languages:
- en
licenses:
- cc-by-sa-3.0
multilinguality:
- monolingual
size_categories:
- 1M<n<10M
source_datasets:
- original
task_categories:
- question-answering
task_ids:
- abstractive-qa
- open-domain-qa
paperswithcode_id: null
pretty_name: SO StackSample
---

# Dataset Card for SO StackSample

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

- **Homepage:** https://www.kaggle.com/stackoverflow/stacksample

### Dataset Summary

Dataset with the text of 10% of questions and answers from the Stack Overflow programming Q&A website.

This is organized as three tables:

Questions table contains the title, body, creation date, closed date (if applicable), score, and owner ID for all non-deleted Stack Overflow questions whose Id is a multiple of 10.
Answers table contains the body, creation date, score, and owner ID for each of the answers to these questions. The ParentId column links back to the Questions table.
Tags table contains the tags on each of these questions.

### Supported Tasks and Leaderboards

Example projects include:

- Identifying tags from question text
- Predicting whether questions will be upvoted, downvoted, or closed based on their text
- Predicting how long questions will take to answer
- Open Domain Q/A

### Languages

English (en) and Programming Languages.

## Dataset Structure

### Data Instances

For Answers:
```
{
  "Id": { # Unique ID given to the Answer post
    "feature_type": "Value",
    "dtype": "int32"
  },
  "OwnerUserId": { # The UserID of the person who generated the Answer on StackOverflow. -1 means NA
    "feature_type": "Value",
    "dtype": "int32"
  },
  "CreationDate": { # The date the Answer was generated. Follows standard datetime format.
    "feature_type": "Value",
    "dtype": "string"
  },
  "ParentId": { # Refers to the `Id` of the Question the Answer belong to.
    "feature_type": "Value",
    "dtype": "int32"
  },
  "Score": { # The sum of up and down votes given to the Answer. Can be negative.
    "feature_type": "Value",
    "dtype": "int32"
  },
  "Body": { # The body content of the Answer.
    "feature_type": "Value",
    "dtype": "string"
  }
}
```

For Questions:
```
{
  "Id": { # Unique ID given to the Question post
    "feature_type": "Value",
    "dtype": "int32"
  },
  "OwnerUserId": { # The UserID of the person who generated the Question on StackOverflow. -1 means NA.
    "feature_type": "Value",
    "dtype": "int32"
  },
  "CreationDate": { # The date the Question was generated. Follows standard datetime format.
    "feature_type": "Value",
    "dtype": "string"
  },
  "ClosedDate": { # The date the Question was generated. Follows standard datetime format. Can be NA.
    "feature_type": "Value",
    "dtype": "string"
  },
  "Score": { # The sum of up and down votes given to the Question. Can be negative.
    "feature_type": "Value",
    "dtype": "int32"
  },
  "Title": { # The title of the Question.
    "feature_type": "Value",
    "dtype": "string"
  },
  "Body": { # The body content of the Question.
    "feature_type": "Value",
    "dtype": "string"
  }
}
```

For Tags:
```
{
  "Id": { # ID of the Question the tag belongs to
    "feature_type": "Value",
    "dtype": "int32"
  },
  "Tag": { # The tag name
    "feature_type": "Value",
    "dtype": "string"
  }
}
```

`

### Data Fields

For Answers:
-`Id`: Unique ID given to the Answer post
`OwnerUserId`: The UserID of the person who generated the Answer on StackOverflow. -1 means NA
"`CreationDate`": The date the Answer was generated. Follows standard datetime format.
"`ParentId`": Refers to the `Id` of the Question the Answer belong to.
"`Score`": The sum of up and down votes given to the Answer. Can be negative.
"`Body`": The body content of the Answer.

For Questions:
- `Id`: Unique ID given to the Question post.
- `OwnerUserId`: The UserID of the person who generated the Question on StackOverflow. -1 means NA.
- `CreationDate`: The date the Question was generated. Follows standard datetime format.
- `ClosedDate`: The date the Question was generated. Follows standard datetime format. Can be NA.
- `Score`: The sum of up and down votes given to the Question. Can be negative.
- `Title`: {The title of the Question.
- `Body`: The body content of the Question.

For Tags:
- `Id`: ID of the Question the tag belongs to.
- `Tag`: The tag name.

### Data Splits

The dataset has 3 splits:
- `Answers`
- `Questions`
- `Tags`

## Dataset Creation

### Curation Rationale

Datasets of all R questions and all Python questions are also available on Kaggle, but this dataset is especially useful for analyses that span many languages.

### Source Data

#### Initial Data Collection and Normalization

[More Information Needed]

#### Who are the source language producers?

StackOverflow Users.

### Annotations

#### Annotation process

[More Information Needed]

#### Who are the annotators?

[More Information Needed]

### Personal and Sensitive Information

This data contains information that can identify individual users of StackOverflow. The information is self-reported.

[Needs More Information]

## Considerations for Using the Data

### Social Impact of Dataset

StackOverflow answers are not guaranteed to be safe, secure, or correct. Some answers may purposefully be insecure as is done in this https://stackoverflow.com/a/35571883/5768407 answer from user [`zys`](https://stackoverflow.com/users/5259310/zys), where they show a solution to purposefully bypass Google Play store security checks. Such answers can lead to biased models that use this data and can further propogate unsafe and insecure programming practices.

[Needs More Information]

### Discussion of Biases

[Needs More Information]

### Other Known Limitations

[Needs More Information]

## Additional Information

### Dataset Curators

[Needs More Information]

### Licensing Information

All Stack Overflow user contributions are licensed under CC-BY-SA 3.0 with attribution required.

### Citation Information

The content is from Stack Overflow.

### Contributions

Thanks to [@ncoop57](https://github.com/ncoop57) for adding this dataset.