annotations_creators:
- expert-generated
- machine-generated
language_creators:
- machine-generated
languages:
- en
licenses:
- mit
multilinguality:
- monolingual
size_categories:
- n<1K
source_datasets:
- original
task_categories:
- other
- sequence-modeling
task_ids:
- other-other-token-classification-of-text-errors
- slot-filling

# Dataset Card for [Needs More Information]

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

- **Homepage:** https://github.com/2dot71mily/youtube_captions_corrections
- **Repository:** https://github.com/2dot71mily/youtube_captions_corrections
- **Paper:** [N/A]
- **Leaderboard:** [N/A]
- **Point of Contact:** Emily McMilin

### Dataset Summary

This dataset is built from pairs of YouTube captions where both an auto-generated and a manually-corrected caption are available for a single specified language. It currently only in English, but scripts at repo support other languages. It was created after viewing errors in auto-generated captions at a recent virtual conference, with the hope that there could be some way to help correct those errors.

The dataset in the repo records in a non-destructive manner all the differences between an auto-generated and a manually-corrected caption for thousands of videos. This dataset focuses on what initially seems at a useful subset of those differences: only simple (e.g. ignoring case/punctuation/stop words) two-way (e.g. ignoring single-sided insertions) single-token differences.

### Supported Tasks and Leaderboards

- `token-classification`: The `default_seq` is tokens from the auto-generated YouTube captions. If `is_single_simple_diff` is labeled `1` at a given index, then the associated token in same index in the `default_seq` was found to have a (simple) difference to the token in the manually-corrected YouTube caption. A model can be trained to learn such errors in the auto-generated captions.

- `slot-filling`: The `correction_seq` is sparsely populated with tokens from the manually-corrected YouTube captions in the locations where there was found to be a (simple) difference to the token in the auto-generated YouTube captions. These 'incorrect' tokens in the `default_seq` can be masked in the locations where `is_single_simple_diff` is labeled `1`, so that a model can be trained to hopefully find a better word to fill in, rather than the 'incorrect' one.

End to end, the models could maybe first identify and then replace (with suitable alternatives) errors in YouTube and other auto-generated captions that are lacking manual corrections

### Languages

English

## Dataset Structure

### Data Instances

If `is_single_simple_diff` is labeled `1` at a given index, then the associated token in same index in the `default_seq` was found to have a (simple) difference to the token in the manually-corrected YouTube caption. The `correction_seq` is sparsely populated with tokens from the manually-corrected YouTube captions at those locations.

{
    'video_titles': '_QUEXsHfsA0', 
    'default_seq': ['you', 'can', 'read', 'the', 'whole', 'damn', 'thing', 'at', 'the', 'moment', 'as', 'you', 'see', "it's", 'a', 'laughter', 'but', 'by', 'the', 'time', 'you', 'see', 'this', 'it', "won't", 'be', 'so', 'we', 'have', 'a'], 
    'correction_seq':  ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', 'draft,', '', '', '', '', '', '', '', '', '', '', '', '', '', ''], 
    'is_single_simple_diff': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
}

### Data Fields

- 'video_ids': Unique ID used by YouTube for each video. Can paste into `https://www.youtube.com/watch?v=<{video_ids}` to see video
- 'default_seq': Tokenized auto-generated YouTube captions for the video
- 'correction_seq':  Tokenized manually-corrected YouTube captions only at those locations, where there is a simple difference between the auto-generated and manually-corrected captions
- 'is_single_simple_diff': 1` at every token where there is a simple difference between the auto-generated and manually-corrected captions

### Data Splits

No data splits

## Dataset Creation

### Curation Rationale

It was created after viewing errors in auto-generated captions at a recent virtual conference, with the hope that there could be some way to help correct those errors.

### Source Data

#### Initial Data Collection and Normalization

All captions are requested via `googleapiclient` and `youtube_transcript_api` at the `channel_id` and language granularity, using scripts written at https://github.com/2dot71mily/youtube_captions_corrections.

The captions are tokenized on spaces and the manually-corrected sequence has here been reduced to only include simple differences between it and the auto-generated sequence. Where simple is defined as:
two-way (e.g. ignoring single-sided insertions) single-token differences that ignore any case/punctuation/stop words differences 

#### Who are the source language producers?

Auto-generated scripts are from YouTube and the manually-corrected scripts are from creators, and any support they may have (e.g. community or software support)

### Annotations

#### Annotation process

Scripts at repo, https://github.com/2dot71mily/youtube_captions_corrections take a diff of the two captions and use this to create annotations.

#### Who are the annotators?

YouTube creators, and any support they may have (e.g. community or software support)

### Personal and Sensitive Information

All content publicly available on YouTube

## Considerations for Using the Data

### Social Impact of Dataset

[Needs More Information]

### Discussion of Biases

[Needs More Information]

### Other Known Limitations

[Needs More Information]

## Additional Information

### Dataset Curators

Emily McMilin

### Licensing Information

MIT License

### Citation Information

https://github.com/2dot71mily/youtube_captions_corrections