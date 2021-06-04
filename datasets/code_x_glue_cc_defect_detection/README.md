---
annotations_creators:
- found
language_creators:
- found
languages:
- code
licenses:
- other-C-UDA
multilinguality:
- other-programming-languages
size_categories:
- 10K<n<100K
source_datasets:
- original
task_categories:
- text-classification
task_ids:
- multi-class-classification
---
# Dataset Card for "code_x_glue_cc_defect_detection"

## Table of Contents
- [Dataset Description](#dataset-description)
  - [Dataset Summary](#dataset-summary)
  - [Supported Tasks](#supported-tasks)
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

## [Dataset Description](#dataset-description)

- **Homepage:** https://github.com/microsoft/CodeXGLUE/tree/main/Code-Code/Defect-detection

### [Dataset Summary](#dataset-summary)

CodeXGLUE Defect-detection dataset, available at https://github.com/microsoft/CodeXGLUE/tree/main/Code-Code/Defect-detection

Given a source code, the task is to identify whether it is an insecure code that may attack software systems, such as resource leaks, use-after-free vulnerabilities and DoS attack. We treat the task as binary classification (0/1), where 1 stands for insecure code and 0 for secure code.
The dataset we use comes from the paper Devign: Effective Vulnerability Identification by Learning Comprehensive Program Semantics via Graph Neural Networks. We combine all projects and split 80%/10%/10% for training/dev/test.

### [Supported Tasks](#supported-tasks)

[More Information Needed]

## [Dataset Structure](#dataset-structure)

### [Data Instances](#data-instances)

An example of 'test' looks as follows.
```
{
    "commit_id": "32bf6550cb9cc9f487a6722fe2bfc272a93c1065",
    "func": "int ff_get_wav_header(AVFormatContext *s, AVIOContext *pb,\n\n                      AVCodecContext *codec, int size, int big_endian)\n\n{\n\n    int id;\n\n    uint64_t bitrate;\n\n\n\n    if (size < 14) {\n\n        avpriv_request_sample(codec, \"wav header size < 14\");\n\n        return AVERROR_INVALIDDATA;\n\n    }\n\n\n\n    codec->codec_type  = AVMEDIA_TYPE_AUDIO;\n\n    if (!big_endian) {\n\n        id                 = avio_rl16(pb);\n\n        if (id != 0x0165) {\n\n            codec->channels    = avio_rl16(pb);\n\n            codec->sample_rate = avio_rl32(pb);\n\n            bitrate            = avio_rl32(pb) * 8LL;\n\n            codec->block_align = avio_rl16(pb);\n\n        }\n\n    } else {\n\n        id                 = avio_rb16(pb);\n\n        codec->channels    = avio_rb16(pb);\n\n        codec->sample_rate = avio_rb32(pb);\n\n        bitrate            = avio_rb32(pb) * 8LL;\n\n        codec->block_align = avio_rb16(pb);\n\n    }\n\n    if (size == 14) {  /* We're dealing with plain vanilla WAVEFORMAT */\n\n        codec->bits_per_coded_sample = 8;\n\n    } else {\n\n        if (!big_endian) {\n\n            codec->bits_per_coded_sample = avio_rl16(pb);\n\n        } else {\n\n            codec->bits_per_coded_sample = avio_rb16(pb);\n\n        }\n\n    }\n\n    if (id == 0xFFFE) {\n\n        codec->codec_tag = 0;\n\n    } else {\n\n        codec->codec_tag = id;\n\n        codec->codec_id  = ff_wav_codec_get_id(id,\n\n                                               codec->bits_per_coded_sample);\n\n    }\n\n    if (size >= 18 && id != 0x0165) {  /* We're obviously dealing with WAVEFORMATEX */\n\n        int cbSize = avio_rl16(pb); /* cbSize */\n\n        if (big_endian) {\n\n            avpriv_report_missing_feature(codec, \"WAVEFORMATEX support for RIFX files\\n\");\n\n            return AVERROR_PATCHWELCOME;\n\n        }\n\n        size  -= 18;\n\n        cbSize = FFMIN(size, cbSize);\n\n        if (cbSize >= 22 && id == 0xfffe) { /* WAVEFORMATEXTENSIBLE */\n\n            parse_waveformatex(pb, codec);\n\n            cbSize -= 22;\n\n            size   -= 22;\n\n        }\n\n        if (cbSize > 0) {\n\n            av_freep(&codec->extradata);\n\n            if (ff_get_extradata(codec, pb, cbSize) < 0)\n\n                return AVERROR(ENOMEM);\n\n            size -= cbSize;\n\n        }\n\n\n\n        /* It is possible for the chunk to contain garbage at the end */\n\n        if (size > 0)\n\n            avio_skip(pb, size);\n\n    } else if (id == 0x0165 && size >= 32) {\n\n        int nb_streams, i;\n\n\n\n        size -= 4;\n\n        av_freep(&codec->extradata);\n\n        if (ff_get_extradata(codec, pb, size) < 0)\n\n            return AVERROR(ENOMEM);\n\n        nb_streams         = AV_RL16(codec->extradata + 4);\n\n        codec->sample_rate = AV_RL32(codec->extradata + 12);\n\n        codec->channels    = 0;\n\n        bitrate            = 0;\n\n        if (size < 8 + nb_streams * 20)\n\n            return AVERROR_INVALIDDATA;\n\n        for (i = 0; i < nb_streams; i++)\n\n            codec->channels += codec->extradata[8 + i * 20 + 17];\n\n    }\n\n\n\n    if (bitrate > INT_MAX) {\n\n        if (s->error_recognition & AV_EF_EXPLODE) {\n\n            av_log(s, AV_LOG_ERROR,\n\n                   \"The bitrate %\"PRIu64\" is too large.\\n\",\n\n                    bitrate);\n\n            return AVERROR_INVALIDDATA;\n\n        } else {\n\n            av_log(s, AV_LOG_WARNING,\n\n                   \"The bitrate %\"PRIu64\" is too large, resetting to 0.\",\n\n                   bitrate);\n\n            codec->bit_rate = 0;\n\n        }\n\n    } else {\n\n        codec->bit_rate = bitrate;\n\n    }\n\n\n\n    if (codec->sample_rate <= 0) {\n\n        av_log(s, AV_LOG_ERROR,\n\n               \"Invalid sample rate: %d\\n\", codec->sample_rate);\n\n        return AVERROR_INVALIDDATA;\n\n    }\n\n    if (codec->codec_id == AV_CODEC_ID_AAC_LATM) {\n\n        /* Channels and sample_rate values are those prior to applying SBR\n\n         * and/or PS. */\n\n        codec->channels    = 0;\n\n        codec->sample_rate = 0;\n\n    }\n\n    /* override bits_per_coded_sample for G.726 */\n\n    if (codec->codec_id == AV_CODEC_ID_ADPCM_G726 && codec->sample_rate)\n\n        codec->bits_per_coded_sample = codec->bit_rate / codec->sample_rate;\n\n\n\n    return 0;\n\n}\n",
    "id": 3,
    "project": "FFmpeg",
    "target": false
}
```

### [Data Fields](#data-fields)

In the following each data field in go is explained for each config. The data fields are the same among all splits.

#### default

|field name| type |               description                |
|----------|------|------------------------------------------|
|id        |int32 | Index of the sample                      |
|func      |string| The source code                          |
|target    |bool  | 0 or 1 (vulnerability or not)            |
|project   |string| Original project that contains this code |
|commit_id |string| Commit identifier in the original project|

### [Data Splits](#data-splits)

| name  |train|validation|test|
|-------|----:|---------:|---:|
|default|21854|      2732|2732|

## [Dataset Creation](#dataset-creation)

### [Curation Rationale](#curation-rationale)

[More Information Needed]

### [Source Data](#source-data)

[More Information Needed]

### [Annotations](#annotations)

[More Information Needed]

### [Personal and Sensitive Information](#personal-and-sensitive-information)

[More Information Needed]

## [Considerations for Using the Data](#considerations-for-using-the-data)

### [Social Impact of Dataset](#social-impact-of-dataset)

[More Information Needed]

### [Discussion of Biases](#discussion-of-biases)

[More Information Needed]

### [Other Known Limitations](#other-known-limitations)

[More Information Needed]

## [Additional Information](#additional-information)

### [Dataset Curators](#dataset-curators)

https://github.com/microsoft, https://github.com/madlag

### [Licensing Information](#licensing-information)

Computational Use of Data Agreement (C-UDA) License.

### [Citation Information](#citation-information)

```
@inproceedings{zhou2019devign,
title={Devign: Effective vulnerability identification by learning comprehensive program semantics via graph neural networks},
author={Zhou, Yaqin and Liu, Shangqing and Siow, Jingkai and Du, Xiaoning and Liu, Yang},
booktitle={Advances in Neural Information Processing Systems},
pages={10197--10207}, year={2019}
```

