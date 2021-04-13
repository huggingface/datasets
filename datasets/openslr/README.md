---
annotations_creators:
- found
language_creators:
- found
languages:
  SLR41:
  - jv
  SLR42:
  - km
  SLR43:
  - ne
  SLR44:
  - su
  SLR63:
  - ml
  SLR64:
  - mr
  SLR65:
  - ta
  SLR66:
  - te
  SLR69:
  - ca
licenses:
- cc-by-sa-4.0
multilinguality:
- multilingual
size_categories:
- 1K<n<10K
source_datasets:
- original
task_categories:
- other
task_ids:
- other-other-automatic-speech-recognition
---

# Dataset Card for openslr

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
  - [Contributions](#contributions)

## Dataset Description

- **Homepage:** https://www.openslr.org/
- **Repository:** [Needs More Information]
- **Paper:** [Needs More Information]
- **Leaderboard:** [Needs More Information]
- **Point of Contact:** [Needs More Information]

### Dataset Summary

OpenSLR is a site devoted to hosting speech and language resources, such as training corpora for speech recognition, 
and software related to speech recognition. Currently, following resources are available: 

#### SLR41: High quality TTS data for Javanese.
This data set contains high-quality transcribed audio data for Javanese. The data set consists of wave files, 
and a TSV file. The file line_index.tsv contains a filename and the transcription of audio in the file. Each 
filename is prepended with a speaker identification number.

The data set has been manually quality checked, but there might still be errors.

This dataset was collected by Google in collaboration with Gadjah Mada University in Indonesia.

The dataset is distributed under Creative Commons Attribution-ShareAlike 4.0 International Public License.
See [LICENSE](https://www.openslr.org/resources/41/LICENSE) file and 
https://github.com/google/language-resources#license for license information.

Copyright 2016, 2017, 2018 Google LLC

#### SLR42: High quality TTS data for Khmer.
This data set contains high-quality transcribed audio data for Khmer. The data set consists of wave files, 
and a TSV file. The file line_index.tsv contains a filename and the transcription of audio in the file. 
Each filename is prepended with a speaker identification number.

The data set has been manually quality checked, but there might still be errors.

This dataset was collected by Google.

The dataset is distributed under Creative Commons Attribution-ShareAlike 4.0 International Public License.
See [LICENSE](https://www.openslr.org/resources/42/LICENSE) file and 
https://github.com/google/language-resources#license for license information.

Copyright 2016, 2017, 2018 Google LLC

#### SLR43: High quality TTS data for Nepali.
This data set contains high-quality transcribed audio data for Nepali. The data set consists of wave files, 
and a TSV file. The file line_index.tsv contains a filename and the transcription of audio in the file. 
Each filename is prepended with a speaker identification number.

The data set has been manually quality checked, but there might still be errors.

This dataset was collected by Google in Nepal.

The dataset is distributed under Creative Commons Attribution-ShareAlike 4.0 International Public License.
See [LICENSE](https://www.openslr.org/resources/43/LICENSE) file and 
https://github.com/google/language-resources#license for license information.

Copyright 2016, 2017, 2018 Google LLC

#### SLR44: High quality TTS data for Sundanese.
This data set contains high-quality transcribed audio data for Sundanese. The data set consists of wave files, 
and a TSV file. The file line_index.tsv contains a filename and the transcription of audio in the file. 
Each filename is prepended with a speaker identification number.

The data set has been manually quality checked, but there might still be errors.

This dataset was collected by Google in collaboration with Universitas Pendidikan Indonesia.

The dataset is distributed under Creative Commons Attribution-ShareAlike 4.0 International Public License.
See [LICENSE](https://www.openslr.org/resources/44/LICENSE) file and 
https://github.com/google/language-resources#license for license information.

Copyright 2016, 2017, 2018 Google LLC

#### SLR63: Crowdsourced high-quality Malayalam multi-speaker speech data set
This data set contains transcribed high-quality audio of Malayalam sentences recorded by volunteers. The data set 
consists of wave files, and a TSV file (line_index.tsv). The file line_index.tsv contains a anonymized FileID and 
the transcription of audio in the file.

The data set has been manually quality checked, but there might still be errors.

Please report any issues in the following issue tracker on GitHub. https://github.com/googlei18n/language-resources/issues

The dataset is distributed under Creative Commons Attribution-ShareAlike 4.0 International Public License.
See [LICENSE](https://www.openslr.org/resources/63/LICENSE) file and 
https://github.com/google/language-resources#license for license information.

Copyright 2018, 2019 Google, Inc.

#### SLR64: Crowdsourced high-quality Marathi multi-speaker speech data set
This data set contains transcribed high-quality audio of Marathi sentences recorded by volunteers. The data set 
consists of wave files, and a TSV file (line_index.tsv). The file line_index.tsv contains a anonymized FileID and 
the transcription of audio in the file.

The data set has been manually quality checked, but there might still be errors.

Please report any issues in the following issue tracker on GitHub. https://github.com/googlei18n/language-resources/issues

The dataset is distributed under Creative Commons Attribution-ShareAlike 4.0 International Public License.
See [LICENSE](https://www.openslr.org/resources/64/LICENSE) file and 
https://github.com/google/language-resources#license for license information.

Copyright 2018, 2019 Google, Inc.
#### SLR65: Crowdsourced high-quality Tamil multi-speaker speech data set
This data set contains transcribed high-quality audio of Tamil sentences recorded by volunteers. The data set 
consists of wave files, and a TSV file (line_index.tsv). The file line_index.tsv contains a anonymized FileID and 
the transcription of audio in the file.

The data set has been manually quality checked, but there might still be errors.

Please report any issues in the following issue tracker on GitHub. https://github.com/googlei18n/language-resources/issues

The dataset is distributed under Creative Commons Attribution-ShareAlike 4.0 International Public License.
See [LICENSE](https://www.openslr.org/resources/65/LICENSE) file and 
https://github.com/google/language-resources#license for license information.

Copyright 2018, 2019 Google, Inc.

#### SLR66: Crowdsourced high-quality Telugu multi-speaker speech data set
This data set contains transcribed high-quality audio of Telugu sentences recorded by volunteers. The data set 
consists of wave files, and a TSV file (line_index.tsv). The file line_index.tsv contains a anonymized FileID and 
the transcription of audio in the file.

The data set has been manually quality checked, but there might still be errors.

Please report any issues in the following issue tracker on GitHub. https://github.com/googlei18n/language-resources/issues

The dataset is distributed under Creative Commons Attribution-ShareAlike 4.0 International Public License.
See [LICENSE](https://www.openslr.org/resources/66/LICENSE) file and 
https://github.com/google/language-resources#license for license information.

Copyright 2018, 2019 Google, Inc.

#### SLR69: Crowdsourced high-quality Catalan multi-speaker speech data set
This data set contains transcribed high-quality audio of Catalan sentences recorded by volunteers. The data set 
consists of wave files, and a TSV file (line_index.tsv). The file line_index.tsv contains a anonymized FileID and 
the transcription of audio in the file.

The data set has been manually quality checked, but there might still be errors.

Please report any issues in the following issue tracker on GitHub. https://github.com/googlei18n/language-resources/issues

The dataset is distributed under Creative Commons Attribution-ShareAlike 4.0 International Public License.
See [LICENSE](https://www.openslr.org/resources/69/LICENSE) file and 
https://github.com/google/language-resources#license for license information.

Copyright 2018, 2019 Google, Inc.

### Supported Tasks and Leaderboards

[Needs More Information]

### Languages

Javanese, Khmer, Nepali, Sundanese, Malayalam, Marathi, Tamil, Telugu, Catalan

## Dataset Structure

### Data Instances

A typical data point comprises the path to the audio file, called path and its sentence. 

#### SLR41, SLR42, SLR43, SLR44, SLR63, SLR64, SLR65, SLR66, SLR69  
```
{
  'path': '/home/cahya/.cache/huggingface/datasets/downloads/extracted/4d9cf915efc21110199074da4d492566dee6097068b07a680f670fcec9176e62/su_id_female/wavs/suf_00297_00037352660.wav'
  'sentence': 'Panonton ting haruleng ningali Kelly Clarkson keur nyanyi di tipi',
}
```

### Data Fields

path: The path to the audio file

sentence: The sentence the user was prompted to speak

### Data Splits

The speech material has only train dataset.

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

[More Information Needed] 

### Other Known Limitations

[More Information Needed] 

## Additional Information

### Dataset Curators

[More Information Needed] 

### Licensing Information

[More Information Needed] 

### Citation Information

#### SLR41, SLR42, SLR43, SLR44 
```
@inproceedings{kjartansson-etal-tts-sltu2018,
    title = {{A Step-by-Step Process for Building TTS Voices Using Open Source Data and Framework for Bangla, Javanese, Khmer, Nepali, Sinhala, and Sundanese}},
    author = {Keshan Sodimana and Knot Pipatsrisawat and Linne Ha and Martin Jansche and Oddur Kjartansson and Pasindu De Silva and Supheakmungkol Sarin},
    booktitle = {Proc. The 6th Intl. Workshop on Spoken Language Technologies for Under-Resourced Languages (SLTU)},
    year  = {2018},
    address = {Gurugram, India},
    month = aug,
    pages = {66--70},
    URL   = {http://dx.doi.org/10.21437/SLTU.2018-14}
}
```

#### SLR63, SLR64, SLR65, SLR66
```
@inproceedings{he-etal-2020-open,
  title = {{Open-source Multi-speaker Speech Corpora for Building Gujarati, Kannada, Malayalam, Marathi, Tamil and Telugu Speech Synthesis Systems}},
  author = {He, Fei and Chu, Shan-Hui Cathy and Kjartansson, Oddur and Rivera, Clara and Katanova, Anna and Gutkin, Alexander and Demirsahin, Isin and Johny, Cibu and Jansche, Martin and Sarin, Supheakmungkol and Pipatsrisawat, Knot},
  booktitle = {Proceedings of The 12th Language Resources and Evaluation Conference (LREC)},
  month = may,
  year = {2020},
  address = {Marseille, France},
  publisher = {European Language Resources Association (ELRA)},
  pages = {6494--6503},
  url = {https://www.aclweb.org/anthology/2020.lrec-1.800},
  ISBN = "{979-10-95546-34-4},
}
```

#### SLR69
```
@inproceedings{kjartansson-etal-2020-open,
    title = {{Open-Source High Quality Speech Datasets for Basque, Catalan and Galician}},
    author = {Kjartansson, Oddur and Gutkin, Alexander and Butryna, Alena and Demirsahin, Isin and Rivera, Clara},
    booktitle = {Proceedings of the 1st Joint Workshop on Spoken Language Technologies for Under-resourced languages (SLTU) and Collaboration and Computing for Under-Resourced Languages (CCURL)},
    year = {2020},
    pages = {21--27},
    month = may,
    address = {Marseille, France},
    publisher = {European Language Resources association (ELRA)},
    url = {https://www.aclweb.org/anthology/2020.sltu-1.3},
    ISBN = {979-10-95546-35-1},
}
```

### Contributions

Thanks to [@cahya-wirawan](https://github.com/cahya-wirawan) for adding this dataset.
