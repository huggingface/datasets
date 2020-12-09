---
annotations_creators:
- found
language_creators:
- found
languages:
- C
licenses:
- other-C-UDA
multilinguality:
- other-programming-languages
size_categories:
- 10K<n<100K
source_datasets: []
task_categories:
- text-classification
task_ids:
- multi-class-classification
---
# Dataset Card for "code_x_glue_cc_defect_detection"

## Table of Contents
- [Dataset Description](#dataset-description)
  - [Dataset Summary](#dataset-summary)
- [Dataset Structure](#dataset-structure)
  - [Data Instances](#data-instances)
  - [Data Fields](#data-fields)
  - [Data Splits](#data-splits)
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


## [Dataset Structure](#dataset-structure)
 

### [Data Instances](#data-instances)

 

 

An example of 'train' looks as follows.
```
{
    "commit_id": "973b1a6b9070e2bf17d17568cbaf4043ce931f51", 
    "func": "static av_cold int vdadec_init(AVCodecContext *avctx)\n\n{\n\n    VDADecoderContext *ctx = avctx->priv_data;\n\n    struct vda_context *vda_ctx = &ctx->vda_ctx;\n\n    OSStatus status;\n\n    int ret;\n\n\n\n    ctx->h264_initialized = 0;\n\n\n\n    /* init pix_fmts of codec */\n\n    if (!ff_h264_vda_decoder.pix_fmts) {\n\n        if (kCFCoreFoundationVersionNumber < kCFCoreFoundationVersionNumber10_7)\n\n            ff_h264_vda_decoder.pix_fmts = vda_pixfmts_prior_10_7;\n\n        else\n\n            ff_h264_vda_decoder.pix_fmts = vda_pixfmts;\n\n    }\n\n\n\n    /* init vda */\n\n    memset(vda_ctx, 0, sizeof(struct vda_context));\n\n    vda_ctx->width = avctx->width;\n\n    vda_ctx->height = avctx->height;\n\n    vda_ctx->format = 'avc1';\n\n    vda_ctx->use_sync_decoding = 1;\n\n    vda_ctx->use_ref_buffer = 1;\n\n    ctx->pix_fmt = avctx->get_format(avctx, avctx->codec->pix_fmts);\n\n    switch (ctx->pix_fmt) {\n\n    case AV_PIX_FMT_UYVY422:\n\n        vda_ctx->cv_pix_fmt_type = '2vuy';\n\n        break;\n\n    case AV_PIX_FMT_YUYV422:\n\n        vda_ctx->cv_pix_fmt_type = 'yuvs';\n\n        break;\n\n    case AV_PIX_FMT_NV12:\n\n        vda_ctx->cv_pix_fmt_type = '420v';\n\n        break;\n\n    case AV_PIX_FMT_YUV420P:\n\n        vda_ctx->cv_pix_fmt_type = 'y420';\n\n        break;\n\n    default:\n\n        av_log(avctx, AV_LOG_ERROR, \"Unsupported pixel format: %d\\n\", avctx->pix_fmt);\n\n        goto failed;\n\n    }\n\n    status = ff_vda_create_decoder(vda_ctx,\n\n                                   avctx->extradata, avctx->extradata_size);\n\n    if (status != kVDADecoderNoErr) {\n\n        av_log(avctx, AV_LOG_ERROR,\n\n                \"Failed to init VDA decoder: %d.\\n\", status);\n\n        goto failed;\n\n    }\n\n    avctx->hwaccel_context = vda_ctx;\n\n\n\n    /* changes callback functions */\n\n    avctx->get_format = get_format;\n\n    avctx->get_buffer2 = get_buffer2;\n\n#if FF_API_GET_BUFFER\n\n    // force the old get_buffer to be empty\n\n    avctx->get_buffer = NULL;\n\n#endif\n\n\n\n    /* init H.264 decoder */\n\n    ret = ff_h264_decoder.init(avctx);\n\n    if (ret < 0) {\n\n        av_log(avctx, AV_LOG_ERROR, \"Failed to open H.264 decoder.\\n\");\n\n        goto failed;\n\n    }\n\n    ctx->h264_initialized = 1;\n\n\n\n    return 0;\n\n\n\nfailed:\n\n    vdadec_close(avctx);\n\n    return -1;\n\n}\n", 
    "id": 0, 
    "project": "FFmpeg", 
    "target": false
}
```
 



### [Data Fields](#data-fields)

 
In the following each data field in go is explained for each config. The data fields are the same among all splits.

#### default

|field name|         type         |               description                |
|----------|----------------------|------------------------------------------|
|id        |int32                 | Index of the sample                      |
|func      |string                | The source code                          |
|target    |datasets.Value("bool"]| 0 or 1 (vulnerability or not)            |
|project   |string                | Original project that contains this code |
|commit_id |string                | Commit identifier in the original project|






### [Data Splits](#data-splits)

 


| name  |train|validation|test|
|-------|----:|---------:|---:|
|default|21854|      2732|2732|







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




