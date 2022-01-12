# coding=utf-8
# Copyright 2020 HuggingFace Datasets Authors.
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

import os

import datasets


_CITATION = """\
@inproceedings{eiselen2014developing,
  title={Developing Text Resources for Ten South African Languages.},
  author={Eiselen, Roald and Puttkammer, Martin J},
  booktitle={LREC},
  pages={3698--3703},
  year={2014}
}
"""

_DESCRIPTION = """\
The development of linguistic resources for use in natural language processingis of utmost importance for the continued growth of research anddevelopment in the field, especially for resource-scarce languages. In this paper we describe the process and challenges of simultaneouslydevelopingmultiple linguistic resources for ten of the official languages of South Africa. The project focussed on establishing a set of foundational resources that can foster further development of both resources and technologies for the NLP industry in South Africa. The development efforts during the project included creating monolingual unannotated corpora, of which a subset of the corpora for each language was annotated on token, orthographic, morphological and morphosyntactic layers. The annotated subsetsincludes both development and test setsand were used in the creation of five core-technologies, viz. atokeniser, sentenciser,lemmatiser, part of speech tagger and morphological decomposer for each language. We report on the quality of these tools for each language and provide some more context of the importance of the resources within the South African context.
"""


class NCHLTConfig(datasets.BuilderConfig):
    """BuilderConfig for NCHLT"""

    def __init__(self, zip_file, **kwargs):
        """BuilderConfig forNCHLT.

        Args:
          zip_file: The URL where to get the data.
          **kwargs: keyword arguments forwarded to super.
        """
        self.zip_file = zip_file
        super(NCHLTConfig, self).__init__(**kwargs)


class NCHLT(datasets.GeneratorBasedBuilder):
    """NCHLT dataset."""

    BUILDER_CONFIGS = [
        NCHLTConfig(
            name="af",
            version=datasets.Version("1.0.0"),
            description="NCHLT Afrikaans Named Entity Annotated Corpus",
            zip_file="https://repo.sadilar.org/bitstream/handle/20.500.12185/299/nchlt_afrikaans_named_entity_annotated_corpus.zip",
        ),
        NCHLTConfig(
            name="nr",
            version=datasets.Version("1.0.0"),
            description="NCHLT isiNdebele Named Entity Annotated Corpus",
            zip_file="https://repo.sadilar.org/bitstream/handle/20.500.12185/306/nchlt_isindebele_named_entity_annotated_corpus.zip",
        ),
        NCHLTConfig(
            name="xh",
            version=datasets.Version("1.0.0"),
            description="NCHLT isiXhosa Named Entity Annotated Corpus",
            zip_file="https://repo.sadilar.org/bitstream/handle/20.500.12185/312/nchlt_isixhosa_named_entity_annotated_corpus.zip",
        ),
        NCHLTConfig(
            name="zu",
            version=datasets.Version("1.0.0"),
            description="NCHLT isiZulu Named Entity Annotated Corpus",
            zip_file="https://repo.sadilar.org/bitstream/handle/20.500.12185/319/nchlt_isizulu_named_entity_annotated_corpus.zip",
        ),
        NCHLTConfig(
            name="nso-sepedi",
            version=datasets.Version("1.0.0"),
            description="NCHLT Sepedi Named Entity Annotated Corpus",
            zip_file="https://repo.sadilar.org/bitstream/handle/20.500.12185/328/nchlt_sepedi_named_entity_annotated_corpus.zip",
        ),
        NCHLTConfig(
            name="nso-sesotho",
            version=datasets.Version("1.0.0"),
            description="NCHLT Sesotho Named Entity Annotated Corpus",
            zip_file="https://repo.sadilar.org/bitstream/handle/20.500.12185/334/nchlt_sesotho_named_entity_annotated_corpus.zip",
        ),
        NCHLTConfig(
            name="tn",
            version=datasets.Version("1.0.0"),
            description="NCHLT Setswana Named Entity Annotated Corpus",
            zip_file="https://repo.sadilar.org/bitstream/handle/20.500.12185/341/nchlt_setswana_named_entity_annotated_corpus.zip",
        ),
        NCHLTConfig(
            name="ss",
            version=datasets.Version("1.0.0"),
            description="NCHLT Siswati Named Entity Annotated Corpus",
            zip_file="https://repo.sadilar.org/bitstream/handle/20.500.12185/346/nchlt_siswati_named_entity_annotated_corpus.zip",
        ),
        NCHLTConfig(
            name="ve",
            version=datasets.Version("1.0.0"),
            description="NCHLT Tshivenda Named Entity Annotated Corpus",
            zip_file="https://repo.sadilar.org/bitstream/handle/20.500.12185/355/nchlt_tshivenda_named_entity_annotated_corpus.zip",
        ),
        NCHLTConfig(
            name="ts",
            version=datasets.Version("1.0.0"),
            description="NCHLT Xitsonga Named Entity Annotated Corpus",
            zip_file="https://repo.sadilar.org/bitstream/handle/20.500.12185/355/nchlt_tshivenda_named_entity_annotated_corpus.zip",
        ),
    ]

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "tokens": datasets.Sequence(datasets.Value("string")),
                    "ner_tags": datasets.Sequence(
                        datasets.features.ClassLabel(
                            names=[
                                "OUT",
                                "B-PERS",
                                "I-PERS",
                                "B-ORG",
                                "I-ORG",
                                "B-LOC",
                                "I-LOC",
                                "B-MISC",
                                "I-MISC",
                            ]
                        )
                    ),
                }
            ),
            supervised_keys=None,
            homepage="https://www.aclweb.org/anthology/W02-2024/",
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        dl_dir = dl_manager.download_and_extract(self.config.zip_file)
        all_filenames = set()
        for root, dirs, files in os.walk(dl_dir):
            for filename in files:
                if filename.endswith(".txt") and "readme.txt" not in filename.lower():
                    all_filenames.add(os.path.join(dl_dir, root, filename))

        return [
            datasets.SplitGenerator(name=datasets.Split.TRAIN, gen_kwargs={"filenames": all_filenames}),
        ]

    def _generate_examples(self, filenames):
        for filename in sorted(filenames):
            id_ = 0
            tokens = []
            ner_tags = []
            with open(filename, "r", encoding="utf-8") as f:
                for line in f:
                    if not line.strip():
                        yield id_, {"tokens": tokens, "ner_tags": ner_tags}
                        id_ += 1
                        tokens = []
                        ner_tags = []
                    else:
                        token, ner = line.strip().split("\t")
                        tokens.append(token)
                        ner_tags.append(ner)
