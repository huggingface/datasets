---
pretty_name: Arabic Speech Corpus
annotations_creators:
- expert-generated
language_creators:
- crowdsourced
language:
- ar
license:
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
train-eval-index:
- config: clean
  task: automatic-speech-recognition
  task_id: speech_recognition
  splits:
    train_split: train
    eval_split: test
  col_mapping:
    file: path
    text: text
  metrics:
  - type: wer
    name: WER
  - type: cer
    name: CER
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

The corpus was created with Speech Synthesis as the main application in mind. Although it has been used as part of a larger corpus for speech recognition and speech denoising. Here are some explanations why the corpus was built the way it is:

* Corpus size: Budget limitations and the research goal resulted in the decision not to gather more data. The goal was to show that high quality speech synthesis is possible with smaller corpora.
* Phonetic diversity: Just like with many corpora, the phonetic diversity was acheived using greedy methods. Start with a core set of utterances and add more utterances which contribute to adding more phonetic diversity the most iterativly. The measure of diversity is based on the diphone frequency.
* Content: News, sports, economics, fully diacritised content from the internet was gathered. The choice of utterances was random to avoid copyright issues. Because of corpus size, acheiving diversity of content type was difficult and was not the goal.
* Non-sense utterances: The corpus contains a large set of utterances that are generated computationally to compensate for the diphones missing in the main part of the corpus. The usefullness of non-sense utterances was not proven in the PhD thesis.
* The talent: The voice talent had a Syrian dialect from Damascus and spoke in formal Arabic.

Please refer to [PhD thesis](#Citation-Information) for more detailed information.

### Source Data

#### Initial Data Collection and Normalization

News, sports, economics, fully diacritised content from the internet was gathered. The choice of utterances was random to avoid copyright issues. Because of corpus size, acheiving diversity of content type was difficult and was not the goal. We were restricted to content which was fully diacritised to make the annotation process easier.

Just like with many corpora, the phonetic diversity was acheived using greedy methods. Start with a core set of utterances and add more utterances which contribute to adding more phonetic diversity the most iterativly. The measure of diversity is based on the diphone frequency.

Please refer to [PhD thesis](#Citation-Information).

#### Who are the source language producers?

Please refer to [PhD thesis](#Citation-Information).

### Annotations

#### Annotation process

Three annotators aligned audio with phonemes with the help of HTK forced alignment. They worked on overlapping parts as well to assess annotator agreement and the quality of the annotations. The entire corpus was checked by human annotators.

Please refer to [PhD thesis](#Citation-Information).

#### Who are the annotators?

Nawar Halabi and two anonymous Arabic language teachers.

### Personal and Sensitive Information

The dataset consists of people who have donated their voice online. You agree to not attempt to determine the identity of speakers in this dataset. The voice talent agreed in writing for their voice to be used in speech technologies as long as they stay anonymous.

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

This dataset was created by:
* Nawar Halabi [@nawarhalabi](https://github.com/nawarhalabi) main creator and annotator.
* Two anonymous Arabic langauge teachers as annotators.
* One anonymous voice talent.
* Thanks to [@zaidalyafeai](https://github.com/zaidalyafeai) for adding this dataset.
