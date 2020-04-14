# Release notes

## Nightly

### Features

*   Add `in_memory` option to cache small dataset in RAM.
*   Better sharding, shuffling and sub-split
*   It is now possible to add arbitrary metadata to `tfds.core.DatasetInfo`
    which will be stored/restored with the dataset. See `tfds.core.Metadata`.
*   Better proxy support, possibility to add certificate
*   Add `decoders` kwargs to override the default feature decoding
    ([guide](https://github.com/tensorflow/datasets/tree/master/docs/decode.md)).
*   Add `duke_ultrasound` dataset of ultrasound phantoms and invivo liver images
    from the [MimickNet paper](https://arxiv.org/abs/1908.05782)
*   Add Dmlab dataset from the
    [VTAB benchmark](https://arxiv.org/abs/1910.04867).
*   Add e-SNLI dataset from the paper
    [e-SNLI](http://papers.nips.cc/paper/8163-e-snli-natural-language-inference-with-natural-language-explanations.pdf).
*   Add [Opinosis dataset](https://www.aclweb.org/anthology/C10-1039.pdf).
*   Add SCAN dataset introduced [here](https://arxiv.org/pdf/1711.00350.pdf).
*   Add [Imagewang](https://github.com/fastai/imagenette) dataset.
*   Add DIV2K dataset from the paper
    [DIV2K](http://www.vision.ee.ethz.ch/~timofter/publications/Agustsson-CVPRW-2017.pdf)
*   Add CFQ (Compositional Freebase Questions) dataset from
    [this paper](https://openreview.net/pdf?id=SygcCnNKwr).
