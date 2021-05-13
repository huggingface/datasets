# coding=utf-8
# Copyright 2020 The HuggingFace Datasets Authors and the current dataset script contributor.
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
"""The mLAMA Dataset"""


import json
import os

import datasets


_CITATION = """
@article{kassner2021multilingual,
  author    = {Nora Kassner and
               Philipp Dufter and
               Hinrich Sch{\"{u}}tze},
  title     = {Multilingual {LAMA:} Investigating Knowledge in Multilingual Pretrained
               Language Models},
  journal   = {CoRR},
  volume    = {abs/2102.00894},
  year      = {2021},
  url       = {https://arxiv.org/abs/2102.00894},
  archivePrefix = {arXiv},
  eprint    = {2102.00894},
  timestamp = {Tue, 09 Feb 2021 13:35:56 +0100},
  biburl    = {https://dblp.org/rec/journals/corr/abs-2102-00894.bib},
  bibsource = {dblp computer science bibliography, https://dblp.org},
  note      = {to appear in EACL2021}
}
"""


_DESCRIPTION = """mLAMA: a multilingual version of the LAMA benchmark (T-REx and GoogleRE) covering 53 languages."""

_HOMEPAGE = "http://cistern.cis.lmu.de/mlama/"

_LICENSE = "The Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0). https://creativecommons.org/licenses/by-nc-sa/4.0/"

_URL = "http://cistern.cis.lmu.de/mlama/mlama1.1.zip"

_LANGUAGES = (
    "af",
    "ar",
    "az",
    "be",
    "bg",
    "bn",
    "ca",
    "ceb",
    "cs",
    "cy",
    "da",
    "de",
    "el",
    "en",
    "es",
    "et",
    "eu",
    "fa",
    "fi",
    "fr",
    "ga",
    "gl",
    "he",
    "hi",
    "hr",
    "hu",
    "hy",
    "id",
    "it",
    "ja",
    "ka",
    "ko",
    "la",
    "lt",
    "lv",
    "ms",
    "nl",
    "pl",
    "pt",
    "ro",
    "ru",
    "sk",
    "sl",
    "sq",
    "sr",
    "sv",
    "ta",
    "th",
    "tr",
    "uk",
    "ur",
    "vi",
    "zh",
)
_RELATIONS = (
    "place_of_birth",
    "place_of_death",
    "P1001",
    "P101",
    "P103",
    "P106",
    "P108",
    "P127",
    "P1303",
    "P131",
    "P136",
    "P1376",
    "P138",
    "P140",
    "P1412",
    "P159",
    "P17",
    "P176",
    "P178",
    "P19",
    "P190",
    "P20",
    "P264",
    "P27",
    "P276",
    "P279",
    "P30",
    "P31",
    "P36",
    "P361",
    "P364",
    "P37",
    "P39",
    "P407",
    "P413",
    "P449",
    "P463",
    "P47",
    "P495",
    "P527",
    "P530",
    "P740",
    "P937",
)


class MLamaConfig(datasets.BuilderConfig):
    """BuilderConfig for mLAMA."""

    def __init__(self, languages=None, relations=None, **kwargs):
        """BuilderConfig for mLAMA.
        Args:
        languages: A subset of af,ar,az,be,bg,bn,ca,ceb,cs,cy,da,de,el,en,es,et,eu,fa,fi,fr,ga,gl,he,hi,hr,hu,hy,id,it,ja,ka,ko,la,lt,lv,ms,nl,pl,pt,ro,ru,sk,sl,sq,sr,sv,ta,th,tr,uk,ur,vi,zh
        relations: A subset of place_of_birth,place_of_death,P1001,P101,P103,P106,P108,P127,P1303,P131,P136,P1376,P138,P140,P1412,P159,P17,P176,P178,P19,P190,P20,P264,P27,P276,P279,P30,P31,P36,P361,P364,P37,P39,P407,P413,P449,P463,P47,P495,P527,P530,P740,P937
          **kwargs: keyword arguments forwarded to super.
        """
        super(MLamaConfig, self).__init__(**kwargs)
        self.languages = languages if languages is not None else _LANGUAGES
        self.relations = relations if relations is not None else _RELATIONS


class MLama(datasets.GeneratorBasedBuilder):
    """multilingual LAMA Dataset (mLAMA)"""

    VERSION = datasets.Version("1.1.0")
    BUILDER_CONFIG_CLASS = MLamaConfig
    BUILDER_CONFIGS = [
        MLamaConfig(
            name="all",
            languages=None,
            relations=None,
            version=datasets.Version("1.1.0"),
            description="Import of mLAMA for all languages and all relations.",
        )
    ]

    def _info(self):
        features = datasets.Features(
            {
                "uuid": datasets.Value("string"),
                "lineid": datasets.Value("uint32"),
                "obj_uri": datasets.Value("string"),
                "obj_label": datasets.Value("string"),
                "sub_uri": datasets.Value("string"),
                "sub_label": datasets.Value("string"),
                "template": datasets.Value("string"),
                "language": datasets.Value("string"),
                "predicate_id": datasets.Value("string"),
            }
        )
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=features,
            supervised_keys=None,
            homepage=_HOMEPAGE,
            license=_LICENSE,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        data_dir = dl_manager.download_and_extract(_URL)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                gen_kwargs={
                    "filepath": os.path.join(data_dir, "mlama1.1"),
                    "split": "test",
                },
            ),
        ]

    def _generate_examples(self, filepath, split):
        """Yields examples from the mLAMA dataset."""
        id_ = -1
        for language in self.config.languages:
            # load templates
            templates = {}
            with open(os.path.join(filepath, language, "templates.jsonl"), encoding="utf-8") as fp:
                for line in fp:
                    line = json.loads(line)
                    templates[line["relation"]] = line["template"]
            for relation in self.config.relations:
                # load triples
                with open(os.path.join(filepath, language, f"{relation}.jsonl"), encoding="utf-8") as fp:
                    for line in fp:
                        triple = json.loads(line)
                        triple["language"] = language
                        triple["predicate_id"] = relation
                        triple["template"] = templates.get(relation, "")
                        id_ += 1
                        yield id_, triple
