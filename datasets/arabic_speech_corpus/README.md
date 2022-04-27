---
pretty_name: Arabic Speech Corpus
annotations_creators:
- expert-generated
language_creators:
- crowdsourced
languages:
- ar
licenses:
- cc-by-4.0
multilinguality:
- monolingual
paperswithcode_id: arabic-speech-corpus
size_categories:
- 1K<n<10K
source_datasets:
- original
task_categories:
- automatic-speech-recognition
task_ids: []
---

# Dataset Card for Arabic Speech Corpus

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

- **Homepage:** [Arabic Speech Corpus](http://en.arabicspeechcorpus.com/)
- **Repository:** [Needs More Information]
- **Paper:** [Modern standard Arabic phonetics for speech synthesis](http://en.arabicspeechcorpus.com/Nawar%20Halabi%20PhD%20Thesis%20Revised.pdf)
- **Leaderboard:** [Paperswithcode Leaderboard][Needs More Information]
- **Point of Contact:** [Nawar Halabi](mailto:nawar.halabi@gmail.com)

### Dataset Summary

This Speech corpus has been developed as part of PhD work carried out by Nawar Halabi at the University of Southampton. The corpus was recorded in south Levantine Arabic (Damascian accent) using a professional studio. Synthesized speech as an output using this corpus has produced a high quality, natural voice.

### Supported Tasks and Leaderboards

[Needs More Information]

### Languages

The audio is in Arabic.

## Dataset Structure

### Data Instances

A typical data point comprises the path to the audio file, usually called `file` and its transcription, called `text`.
An example from the dataset is:
```
{
    'file': '/Users/username/.cache/huggingface/datasets/downloads/extracted/baebe85e2cb67579f6f88e7117a87888c1ace390f4f14cb6c3e585c517ad9db0/arabic-speech-corpus/wav/ARA NORM  0002.wav',
	'audio': {'path': '/Users/username/.cache/huggingface/datasets/downloads/extracted/baebe85e2cb67579f6f88e7117a87888c1ace390f4f14cb6c3e585c517ad9db0/arabic-speech-corpus/wav/ARA NORM  0002.wav',
			   'array': array([-0.00048828, -0.00018311, -0.00137329, ...,  0.00079346, 0.00091553,  0.00085449], dtype=float32),
			   'sampling_rate': 48000},
		'orthographic': 'waraj~aHa Alt~aqoriyru Al~a*iy >aEad~ahu maEohadu >aboHaA^i haDabapi Alt~ibiti fiy Alo>akaAdiymiy~api AlS~iyniy~api liloEuluwmi - >ano tasotamir~a darajaAtu AloHaraArapi wamusotawayaAtu Alr~uTuwbapi fiy Alo<irotifaAEi TawaAla ha*aA Aloqarono',
    'phonetic': "sil w a r a' jj A H a tt A q r ii0' r u0 ll a * i0 < a E a' dd a h u0 m a' E h a d u0 < a b H aa' ^ i0 h A D A' b a t i0 tt i1' b t i0 f i0 l < a k aa d ii0 m ii0' y a t i0 SS II0 n ii0' y a t i0 l u0 l E u0 l uu0' m i0 sil < a' n t a s t a m i0' rr a d a r a j aa' t u0 l H a r aa' r a t i0 w a m u0 s t a w a y aa' t u0 rr U0 T UU0' b a t i0 f i0 l Ah i0 r t i0 f aa' E i0 T A' w A l a h aa' * a l q A' r n sil",
    'text': '\ufeffwaraj~aHa Alt~aqoriyru Al~aTHiy >aEad~ahu maEohadu >aboHaA^i haDabapi Alt~ibiti fiy Alo>akaAdiymiy~api AlS~iyniy~api liloEuluwmi - >ano tasotamir~a darajaAtu AloHaraArapi wamusotawayaAtu Alr~uTuwbapi fiy Alo<irotifaAEi TawaAla haTHaA Aloqarono'
}
```

### Data Fields

- file: A path to the downloaded audio file in .wav format.

- audio: A dictionary containing the path to the downloaded audio file, the decoded audio array, and the sampling rate. Note that when accessing the audio column: `dataset[0]["audio"]` the audio file is automatically decoded and resampled to `dataset.features["audio"].sampling_rate`. Decoding and resampling of a large number of audio files might take a significant amount of time. Thus it is important to first query the sample index before the `"audio"` column, *i.e.* `dataset[0]["audio"]` should **always** be preferred over `dataset["audio"][0]`.

- text: the transcription of the audio file.

- phonetic: the transcription in phonentics format. 

- orthographic: the transcriptions written in orthographic format. 

### Data Splits

|       | Train | Test |
| ----- | ----- | ---- | 
| dataset | 1813 | 100 |  



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

The dataset consists of people who have donated their voice online. You agree to not attempt to determine the identity of speakers in this dataset.

## Considerations for Using the Data

### Social Impact of Dataset

[More Information Needed]

### Discussion of Biases

[More Information Needed]

### Other Known Limitations

[Needs More Information]

## Additional Information

### Dataset Curators

The corpus was recorded in south Levantine Arabic (Damascian accent) using a professional studio by Nawar Halabi.

### Licensing Information

[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)

### Citation Information

```
@phdthesis{halabi2016modern,
  title={Modern standard Arabic phonetics for speech synthesis},
  author={Halabi, Nawar},
  year={2016},
  school={University of Southampton}
}
```

### Contributions

Thanks to [@zaidalyafeai](https://github.com/zaidalyafeai) for adding this dataset.
