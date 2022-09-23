---
annotations_creators:
- found
language_creators:
- found
language:
- en
license:
- unknown
multilinguality:
- monolingual
size_categories:
- 10K<n<100K
- 1K<n<10K
- n<1K
source_datasets:
- original
task_categories:
- text-classification
task_ids:
- multi-class-classification
paperswithcode_id: null
pretty_name: pragmeval
configs:
- emergent
- emobank-arousal
- emobank-dominance
- emobank-valence
- gum
- mrda
- pdtb
- persuasiveness-claimtype
- persuasiveness-eloquence
- persuasiveness-premisetype
- persuasiveness-relevance
- persuasiveness-specificity
- persuasiveness-strength
- sarcasm
- squinky-formality
- squinky-implicature
- squinky-informativeness
- stac
- switchboard
- verifiability
dataset_info:
- config_name: verifiability
  features:
  - name: sentence
    dtype: string
  - name: label
    dtype:
      class_label:
        names:
          0: experiential
          1: unverifiable
          2: non-experiential
  - name: idx
    dtype: int32
  splits:
  - name: test
    num_bytes: 251799
    num_examples: 2424
  - name: train
    num_bytes: 592520
    num_examples: 5712
  - name: validation
    num_bytes: 65215
    num_examples: 634
  download_size: 5330724
  dataset_size: 909534
- config_name: emobank-arousal
  features:
  - name: sentence
    dtype: string
  - name: label
    dtype:
      class_label:
        names:
          0: low
          1: high
  - name: idx
    dtype: int32
  splits:
  - name: test
    num_bytes: 69276
    num_examples: 683
  - name: train
    num_bytes: 567660
    num_examples: 5470
  - name: validation
    num_bytes: 71221
    num_examples: 684
  download_size: 5330724
  dataset_size: 708157
- config_name: switchboard
  features:
  - name: sentence
    dtype: string
  - name: label
    dtype:
      class_label:
        names:
          0: Response Acknowledgement
          1: Uninterpretable
          2: Or-Clause
          3: Reject
          4: Statement-non-opinion
          5: 3rd-party-talk
          6: Repeat-phrase
          7: Hold Before Answer/Agreement
          8: Signal-non-understanding
          9: Offers, Options Commits
          10: Agree/Accept
          11: Dispreferred Answers
          12: Hedge
          13: Action-directive
          14: Tag-Question
          15: Self-talk
          16: Yes-No-Question
          17: Rhetorical-Question
          18: No Answers
          19: Open-Question
          20: Conventional-closing
          21: Other Answers
          22: Acknowledge (Backchannel)
          23: Wh-Question
          24: Declarative Wh-Question
          25: Thanking
          26: Yes Answers
          27: Affirmative Non-yes Answers
          28: Declarative Yes-No-Question
          29: Backchannel in Question Form
          30: Apology
          31: Downplayer
          32: Conventional-opening
          33: Collaborative Completion
          34: Summarize/Reformulate
          35: Negative Non-no Answers
          36: Statement-opinion
          37: Appreciation
          38: Other
          39: Quotation
          40: Maybe/Accept-part
  - name: idx
    dtype: int32
  splits:
  - name: test
    num_bytes: 34013
    num_examples: 649
  - name: train
    num_bytes: 1021220
    num_examples: 18930
  - name: validation
    num_bytes: 116058
    num_examples: 2113
  download_size: 5330724
  dataset_size: 1171291
- config_name: persuasiveness-eloquence
  features:
  - name: sentence1
    dtype: string
  - name: sentence2
    dtype: string
  - name: label
    dtype:
      class_label:
        names:
          0: low
          1: high
  - name: idx
    dtype: int32
  splits:
  - name: test
    num_bytes: 18379
    num_examples: 90
  - name: train
    num_bytes: 153946
    num_examples: 725
  - name: validation
    num_bytes: 19376
    num_examples: 91
  download_size: 5330724
  dataset_size: 191701
- config_name: mrda
  features:
  - name: sentence
    dtype: string
  - name: label
    dtype:
      class_label:
        names:
          0: Declarative-Question
          1: Statement
          2: Reject
          3: Or-Clause
          4: 3rd-party-talk
          5: Continuer
          6: Hold Before Answer/Agreement
          7: Assessment/Appreciation
          8: Signal-non-understanding
          9: Floor Holder
          10: Sympathy
          11: Dispreferred Answers
          12: Reformulate/Summarize
          13: Exclamation
          14: Interrupted/Abandoned/Uninterpretable
          15: Expansions of y/n Answers
          16: Action-directive
          17: Tag-Question
          18: Accept
          19: Rhetorical-question Continue
          20: Self-talk
          21: Rhetorical-Question
          22: Yes-No-question
          23: Open-Question
          24: Rising Tone
          25: Other Answers
          26: Commit
          27: Wh-Question
          28: Repeat
          29: Follow Me
          30: Thanking
          31: Offer
          32: About-task
          33: Reject-part
          34: Affirmative Non-yes Answers
          35: Apology
          36: Downplayer
          37: Humorous Material
          38: Accept-part
          39: Collaborative Completion
          40: Mimic Other
          41: Understanding Check
          42: Misspeak Self-Correction
          43: Or-Question
          44: Topic Change
          45: Negative Non-no Answers
          46: Floor Grabber
          47: Correct-misspeaking
          48: Maybe
          49: Acknowledge-answer
          50: Defending/Explanation
  - name: idx
    dtype: int32
  splits:
  - name: test
    num_bytes: 419797
    num_examples: 6459
  - name: train
    num_bytes: 963913
    num_examples: 14484
  - name: validation
    num_bytes: 111813
    num_examples: 1630
  download_size: 5330724
  dataset_size: 1495523
- config_name: gum
  features:
  - name: sentence1
    dtype: string
  - name: sentence2
    dtype: string
  - name: label
    dtype:
      class_label:
        names:
          0: preparation
          1: evaluation
          2: circumstance
          3: solutionhood
          4: justify
          5: result
          6: evidence
          7: purpose
          8: concession
          9: elaboration
          10: background
          11: condition
          12: cause
          13: restatement
          14: motivation
          15: antithesis
          16: no_relation
  - name: idx
    dtype: int32
  splits:
  - name: test
    num_bytes: 40334
    num_examples: 248
  - name: train
    num_bytes: 270401
    num_examples: 1700
  - name: validation
    num_bytes: 35405
    num_examples: 259
  download_size: 5330724
  dataset_size: 346140
- config_name: emergent
  features:
  - name: sentence1
    dtype: string
  - name: sentence2
    dtype: string
  - name: label
    dtype:
      class_label:
        names:
          0: observing
          1: for
          2: against
  - name: idx
    dtype: int32
  splits:
  - name: test
    num_bytes: 38842
    num_examples: 259
  - name: train
    num_bytes: 313257
    num_examples: 2076
  - name: validation
    num_bytes: 38948
    num_examples: 259
  download_size: 5330724
  dataset_size: 391047
- config_name: persuasiveness-relevance
  features:
  - name: sentence1
    dtype: string
  - name: sentence2
    dtype: string
  - name: label
    dtype:
      class_label:
        names:
          0: low
          1: high
  - name: idx
    dtype: int32
  splits:
  - name: test
    num_bytes: 18880
    num_examples: 90
  - name: train
    num_bytes: 153158
    num_examples: 725
  - name: validation
    num_bytes: 19663
    num_examples: 91
  download_size: 5330724
  dataset_size: 191701
- config_name: persuasiveness-specificity
  features:
  - name: sentence1
    dtype: string
  - name: sentence2
    dtype: string
  - name: label
    dtype:
      class_label:
        names:
          0: low
          1: high
  - name: idx
    dtype: int32
  splits:
  - name: test
    num_bytes: 12712
    num_examples: 62
  - name: train
    num_bytes: 106594
    num_examples: 504
  - name: validation
    num_bytes: 13766
    num_examples: 62
  download_size: 5330724
  dataset_size: 133072
- config_name: persuasiveness-strength
  features:
  - name: sentence1
    dtype: string
  - name: sentence2
    dtype: string
  - name: label
    dtype:
      class_label:
        names:
          0: low
          1: high
  - name: idx
    dtype: int32
  splits:
  - name: test
    num_bytes: 10225
    num_examples: 46
  - name: train
    num_bytes: 79679
    num_examples: 371
  - name: validation
    num_bytes: 10052
    num_examples: 46
  download_size: 5330724
  dataset_size: 99956
- config_name: emobank-dominance
  features:
  - name: sentence
    dtype: string
  - name: label
    dtype:
      class_label:
        names:
          0: low
          1: high
  - name: idx
    dtype: int32
  splits:
  - name: test
    num_bytes: 83319
    num_examples: 798
  - name: train
    num_bytes: 660303
    num_examples: 6392
  - name: validation
    num_bytes: 86802
    num_examples: 798
  download_size: 5330724
  dataset_size: 830424
- config_name: squinky-implicature
  features:
  - name: sentence
    dtype: string
  - name: label
    dtype:
      class_label:
        names:
          0: low
          1: high
  - name: idx
    dtype: int32
  splits:
  - name: test
    num_bytes: 56549
    num_examples: 465
  - name: train
    num_bytes: 471552
    num_examples: 3724
  - name: validation
    num_bytes: 58087
    num_examples: 465
  download_size: 5330724
  dataset_size: 586188
- config_name: sarcasm
  features:
  - name: sentence1
    dtype: string
  - name: sentence2
    dtype: string
  - name: label
    dtype:
      class_label:
        names:
          0: notsarc
          1: sarc
  - name: idx
    dtype: int32
  splits:
  - name: test
    num_bytes: 269724
    num_examples: 469
  - name: train
    num_bytes: 2177332
    num_examples: 3754
  - name: validation
    num_bytes: 257834
    num_examples: 469
  download_size: 5330724
  dataset_size: 2704890
- config_name: squinky-formality
  features:
  - name: sentence
    dtype: string
  - name: label
    dtype:
      class_label:
        names:
          0: low
          1: high
  - name: idx
    dtype: int32
  splits:
  - name: test
    num_bytes: 58242
    num_examples: 452
  - name: train
    num_bytes: 459721
    num_examples: 3622
  - name: validation
    num_bytes: 59921
    num_examples: 453
  download_size: 5330724
  dataset_size: 577884
- config_name: stac
  features:
  - name: sentence1
    dtype: string
  - name: sentence2
    dtype: string
  - name: label
    dtype:
      class_label:
        names:
          0: Comment
          1: Contrast
          2: Q_Elab
          3: Parallel
          4: Explanation
          5: Narration
          6: Continuation
          7: Result
          8: Acknowledgement
          9: Alternation
          10: Question_answer_pair
          11: Correction
          12: Clarification_question
          13: Conditional
          14: Sequence
          15: Elaboration
          16: Background
          17: no_relation
  - name: idx
    dtype: int32
  splits:
  - name: test
    num_bytes: 70451
    num_examples: 1304
  - name: train
    num_bytes: 645969
    num_examples: 11230
  - name: validation
    num_bytes: 71400
    num_examples: 1247
  download_size: 5330724
  dataset_size: 787820
- config_name: pdtb
  features:
  - name: sentence1
    dtype: string
  - name: sentence2
    dtype: string
  - name: label
    dtype:
      class_label:
        names:
          0: Synchrony
          1: Contrast
          2: Asynchronous
          3: Conjunction
          4: List
          5: Condition
          6: Pragmatic concession
          7: Restatement
          8: Pragmatic cause
          9: Alternative
          10: Pragmatic condition
          11: Pragmatic contrast
          12: Instantiation
          13: Exception
          14: Cause
          15: Concession
  - name: idx
    dtype: int32
  splits:
  - name: test
    num_bytes: 235851
    num_examples: 1085
  - name: train
    num_bytes: 2968638
    num_examples: 12907
  - name: validation
    num_bytes: 276997
    num_examples: 1204
  download_size: 5330724
  dataset_size: 3481486
- config_name: persuasiveness-premisetype
  features:
  - name: sentence1
    dtype: string
  - name: sentence2
    dtype: string
  - name: label
    dtype:
      class_label:
        names:
          0: testimony
          1: warrant
          2: invented_instance
          3: common_knowledge
          4: statistics
          5: analogy
          6: definition
          7: real_example
  - name: idx
    dtype: int32
  splits:
  - name: test
    num_bytes: 14395
    num_examples: 70
  - name: train
    num_bytes: 122631
    num_examples: 566
  - name: validation
    num_bytes: 15920
    num_examples: 71
  download_size: 5330724
  dataset_size: 152946
- config_name: squinky-informativeness
  features:
  - name: sentence
    dtype: string
  - name: label
    dtype:
      class_label:
        names:
          0: low
          1: high
  - name: idx
    dtype: int32
  splits:
  - name: test
    num_bytes: 56872
    num_examples: 464
  - name: train
    num_bytes: 464855
    num_examples: 3719
  - name: validation
    num_bytes: 60447
    num_examples: 465
  download_size: 5330724
  dataset_size: 582174
- config_name: persuasiveness-claimtype
  features:
  - name: sentence1
    dtype: string
  - name: sentence2
    dtype: string
  - name: label
    dtype:
      class_label:
        names:
          0: Value
          1: Fact
          2: Policy
  - name: idx
    dtype: int32
  splits:
  - name: test
    num_bytes: 3717
    num_examples: 19
  - name: train
    num_bytes: 31259
    num_examples: 160
  - name: validation
    num_bytes: 3803
    num_examples: 20
  download_size: 5330724
  dataset_size: 38779
- config_name: emobank-valence
  features:
  - name: sentence
    dtype: string
  - name: label
    dtype:
      class_label:
        names:
          0: low
          1: high
  - name: idx
    dtype: int32
  splits:
  - name: test
    num_bytes: 66178
    num_examples: 643
  - name: train
    num_bytes: 539652
    num_examples: 5150
  - name: validation
    num_bytes: 62809
    num_examples: 644
  download_size: 5330724
  dataset_size: 668639
---

# Dataset Card for pragmeval

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

- **Homepage:**
- **Repository:**
- **Paper:**
- **Leaderboard:**
- **Point of Contact:**

### Dataset Summary

[More Information Needed]

### Supported Tasks and Leaderboards

[More Information Needed]

### Languages

[More Information Needed]

## Dataset Structure

### Data Instances

[More Information Needed]

### Data Fields

[More Information Needed]

### Data Splits

[More Information Needed]

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

[More Information Needed]

### Contributions

Thanks to [@sileod](https://github.com/sileod) for adding this dataset.