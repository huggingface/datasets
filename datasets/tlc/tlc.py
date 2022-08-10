#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Thai Literature Corpora (TLC): Corpora of machine-ingestible Thai classical literature texts."""


import json

import datasets


_CITATION = """\
@misc{
  author={Sawatphol, Jitkapat},
  title={Thai Literature Corpora},
  year={2019},
  howpublished={\\url{https://attapol.github.io/tlc.html}}
}
"""

_HOMEPAGE = "https://attapol.github.io/tlc.html"

_DESCRIPTION = """\
Thai Literature Corpora (TLC): Corpora of machine-ingestible Thai classical literature texts.

Release: 6/25/19

It consists of two datasets:

## TLC set
It is texts from [Vajirayana Digital Library](https://vajirayana.org/), stored by chapters and stanzas (non-tokenized).

tlc v.2.0 (6/17/19 : a total of 34 documents, 292,270 lines, 31,790,734 characters)
tlc v.1.0 (6/11/19 : a total of 25 documents, 113,981 lines, 28,775,761 characters)

## TNHC set
It is texts from Thai National Historical Corpus, stored by lines (manually tokenized).

tnhc v.1.0 (6/25/19 : a total of 47 documents, 756,478 lines, 13,361,142 characters)
"""

_URLs = {
    "tlcv1.0": "https://github.com/jitkapat/thailitcorpus/releases/download/v.1.0/tlc_v.1.0.tar.gz",
    "tlcv2.0": "https://github.com/jitkapat/thailitcorpus/releases/download/v.2.0/tlc_v.2.0.tar.gz",
    "tnhcv1.0": "https://github.com/jitkapat/thailitcorpus/releases/download/v.1.0/tnhc_v.1.0.tar.gz",
}
_FILENAMES = {
    "tlcv1.0": "นิราศอิเหนา.json",
    "tlcv2.0": "นิราศอิเหนา.json",
    "tnhcv1.0": "กาพย์เห่เรือ.json",
}


class TlcConfig(datasets.BuilderConfig):
    """BuilderConfig for Tlc."""

    def __init__(self, **kwargs):
        """BuilderConfig for Tlc.

        Args:
          **kwargs: keyword arguments forwarded to super.
        """
        super(TlcConfig, self).__init__(**kwargs)


class Tlc(datasets.GeneratorBasedBuilder):
    """Thai Literature Corpora (TLC): Corpora of machine-ingestible Thai classical literature texts."""

    BUILDER_CONFIGS = [
        datasets.BuilderConfig(
            name="tlcv1.0", version=datasets.Version("1.0.0"), description="Thai Literature Corpora"
        ),
        datasets.BuilderConfig(
            name="tlcv2.0", version=datasets.Version("2.0.0"), description="Thai Literature Corpora"
        ),
        datasets.BuilderConfig(
            name="tnhcv1.0",
            version=datasets.Version("1.0.0"),
            description="Thai Literature Corpora: Thai National Historical Corpus",
        ),
    ]

    DEFAULT_CONFIG_NAME = "tlcv2.0"

    def _info(self):
        if self.config.name.startswith("tlc"):
            features = datasets.Features(
                {
                    "ch_num": datasets.Value("string"),
                    "title": datasets.Value("string"),
                    "text": datasets.Sequence(datasets.Sequence(datasets.Value("string"))),
                }
            )
        else:
            features = datasets.Features(
                {
                    "text": datasets.Sequence((datasets.Value("string"))),
                }
            )

        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=features,
            supervised_keys=None,
            homepage=_HOMEPAGE,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        archive = dl_manager.download(_URLs[self.config.name])

        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={"files": dl_manager.iter_archive(archive), "filepath": _FILENAMES[self.config.name]},
            )
        ]

    def _generate_examples(self, files, filepath):
        _id = 0
        for path, f in files:
            if path == filepath:
                data = json.loads(f.read().decode("utf-8"))
                for d in data:
                    if self.config.name.startswith("tlc"):
                        yield _id, d
                    else:
                        yield _id, {"text": d}
                    _id += 1
                break
