# coding=utf-8
# Copyright 2020 The TensorFlow Datasets Authors and the HuggingFace Datasets Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Lint as: python3
"""Wikipedia knowledge source for KILT"""

from __future__ import absolute_import, division, print_function

import json
import logging

import datasets


_CITATION = """\
@inproceedings{fb_kilt,
    author    = {Fabio Petroni and
                 Aleksandra Piktus and
                 Angela Fan and
                 Patrick Lewis and
                 Majid Yazdani and
                 Nicola De Cao and
                 James Thorne and
                 Yacine Jernite and
                 Vassilis Plachouras and
                 Tim Rockt\"aschel and
                 Sebastian Riedel},
    title     = {{KILT:} a {B}enchmark for {K}nowledge {I}ntensive {L}anguage {T}asks},
    journal   = {CoRR},
    archivePrefix = {arXiv},
    year      = {2020},
"""

_DESCRIPTION = """\
KILT-Wikipedia: Wikipedia pre-processed for KILT.
"""


class KILTWikipediaConfig(datasets.BuilderConfig):
    """BuilderConfig for KILTWikipedia."""

    def __init__(self, **kwargs):
        """BuilderConfig for KILTWikipedia.

            Args:
        .
              **kwargs: keyword arguments forwarded to super.
        """
        super(KILTWikipediaConfig, self).__init__(
            version=datasets.Version("1.0.0", "Wikipedia pre-processed for KILT"), **kwargs
        )


class KILTWikipedia(datasets.GeneratorBasedBuilder):
    """KILTWikipedia: Wikipedia pre-processed for KILT. Version 1.0."""

    BUILDER_CONFIGS = [
        KILTWikipediaConfig(
            name="2019-08-01",
            description="Wikipedia pre-processed for KILT from 2019/08/01 dump",
        ),
    ]

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "kilt_id": datasets.Value("string"),
                    "wikipedia_id": datasets.Value("string"),
                    "wikipedia_title": datasets.Value("string"),
                    "text": datasets.features.Sequence({"paragraph": datasets.Value("string")}),
                    "anchors": datasets.features.Sequence(
                        {
                            "paragraph_id": datasets.Value("int32"),
                            "start": datasets.Value("int32"),
                            "end": datasets.Value("int32"),
                            "text": datasets.Value("string"),
                            "href": datasets.Value("string"),
                            "wikipedia_title": datasets.Value("string"),
                            "wikipedia_id": datasets.Value("string"),
                        }
                    ),
                    "categories": datasets.Value("string"),
                    "wikidata_info": datasets.Features(
                        {
                            "description": datasets.Value("string"),
                            "enwikiquote_title": datasets.Value("string"),
                            "wikidata_id": datasets.Value("string"),
                            "wikidata_label": datasets.Value("string"),
                            "wikipedia_title": datasets.Value("string"),
                            "aliases": datasets.features.Sequence({"alias": datasets.Value("string")}),
                        }
                    ),
                    "history": datasets.Features(
                        {
                            "pageid": datasets.Value("int32"),
                            "parentid": datasets.Value("int32"),
                            "revid": datasets.Value("int32"),
                            "pre_dump": datasets.Value("bool"),
                            "timestamp": datasets.Value("string"),
                            "url": datasets.Value("string"),
                        }
                    ),
                }
            ),
            # No default supervised_keys (as we have to pass both premise
            # and hypothesis as input).
            supervised_keys=None,
            homepage="https://github.com/facebookresearch/KILT",
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):

        downloaded_path = dl_manager.download_and_extract(
            "http://dl.fbaipublicfiles.com/KILT/kilt_knowledgesource.json"
        )

        return [
            datasets.SplitGenerator(name="full", gen_kwargs={"filepath": downloaded_path}),
        ]

    def _generate_examples(self, filepath):
        """Generate Wikipedia articles for KILT.

        Args:
          filepath: a string

        Yields:
          dictionaries representing article data and metadata
        """
        logging.info("generating examples from = %s", filepath)
        with open(filepath, encoding="utf-8") as f:
            for idx, line in enumerate(f):
                pre_article = json.loads(line.strip())
                article = dict([(k, pre_article[k]) for k in ["wikipedia_id", "wikipedia_title", "categories"]])
                # wikidata
                article["wikidata_info"] = {}
                pre_article["wikidata_info"] = pre_article.get("wikidata_info", {})
                if pre_article["wikidata_info"].get("aliases", None) is None:
                    pre_article["wikidata_info"]["aliases"] = []
                for k in ["description", "enwikiquote_title", "wikidata_id", "wikidata_label", "wikipedia_title"]:
                    val = pre_article["wikidata_info"].get(k, None)
                    article["wikidata_info"][k] = "" if val is None else val
                article["wikidata_info"]["aliases"] = {"alias": pre_article["wikidata_info"]["aliases"]}
                # history
                article["history"] = {}
                pre_article["history"] = pre_article.get("history", {})
                pre_dump = pre_article["history"].get("pre_dump", None)
                article["history"]["pre_dump"] = False if pre_dump is None else pre_dump
                for k in ["pageid", "parentid", "revid"]:
                    val = pre_article["history"].get(k, None)
                    article["history"][k] = -1 if val is None else val
                for k in ["timestamp", "url"]:
                    val = pre_article["history"].get(k, None)
                    article["history"][k] = "" if val is None else val
                # everything else
                article["kilt_id"] = pre_article["_id"]
                article["text"] = {"paragraph": pre_article["text"]}
                article["anchors"] = {}
                for k in ["paragraph_id", "start", "end", "text", "href", "wikipedia_title", "wikipedia_id"]:
                    article["anchors"][k] = [anchor.get(k, "") for anchor in pre_article["anchors"]]
                yield idx, article
