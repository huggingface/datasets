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
"""ASSIN dataset."""


import xml.etree.ElementTree as ET

import datasets


_CITATION = """
@inproceedings{fonseca2016assin,
  title={ASSIN: Avaliacao de similaridade semantica e inferencia textual},
  author={Fonseca, E and Santos, L and Criscuolo, Marcelo and Aluisio, S},
  booktitle={Computational Processing of the Portuguese Language-12th International Conference, Tomar, Portugal},
  pages={13--15},
  year={2016}
}
"""

_DESCRIPTION = """
The ASSIN (Avaliação de Similaridade Semântica e INferência textual) corpus is a corpus annotated with pairs of sentences written in
Portuguese that is suitable for the  exploration of textual entailment and paraphrasing classifiers. The corpus contains pairs of sentences
extracted from news articles written in European Portuguese (EP) and Brazilian Portuguese (BP), obtained from Google News Portugal
and Brazil, respectively. To create the corpus, the authors started by collecting a set of news articles describing the
same event (one news article from Google News Portugal and another from Google News Brazil) from Google News.
Then, they employed Latent Dirichlet Allocation (LDA) models to retrieve pairs of similar sentences between sets of news
articles that were grouped together around the same topic. For that, two LDA models were trained (for EP and for BP)
on external and large-scale collections of unannotated news articles from Portuguese and Brazilian news providers, respectively.
Then, the authors defined a lower and upper threshold for the sentence similarity score of the retrieved pairs of sentences,
taking into account that high similarity scores correspond to sentences that contain almost the same content (paraphrase candidates),
and low similarity scores correspond to sentences that are very different in content from each other (no-relation candidates).
From the collection of pairs of sentences obtained at this stage, the authors performed some manual grammatical corrections
and discarded some of the pairs wrongly retrieved. Furthermore, from a preliminary analysis made to the retrieved sentence pairs
the authors noticed that the number of contradictions retrieved during the previous stage was very low. Additionally, they also
noticed that event though paraphrases are not very frequent, they occur with some frequency in news articles. Consequently,
in contrast with the majority of the currently available corpora for other languages, which consider as labels “neutral”, “entailment”
and “contradiction” for the task of RTE, the authors of the ASSIN corpus decided to use as labels “none”, “entailment” and “paraphrase”.
Finally, the manual annotation of pairs of sentences was performed by human annotators. At least four annotators were randomly
selected to annotate each pair of sentences, which is done in two steps: (i) assigning a semantic similarity label (a score between 1 and 5,
from unrelated to very similar); and (ii) providing an entailment label (one sentence entails the other, sentences are paraphrases,
or no relation). Sentence pairs where at least three annotators do not agree on the entailment label were considered controversial
and thus discarded from the gold standard annotations. The full dataset has 10,000 sentence pairs, half of which in Brazilian Portuguese
and half in European Portuguese. Either language variant has 2,500 pairs for training, 500 for validation and 2,000 for testing.
"""

_HOMEPAGE = "http://nilc.icmc.usp.br/assin/"

_LICENSE = ""

_URL = "http://nilc.icmc.usp.br/assin/assin.tar.gz"


class Assin(datasets.GeneratorBasedBuilder):
    """ASSIN dataset."""

    VERSION = datasets.Version("1.0.0")

    BUILDER_CONFIGS = [
        datasets.BuilderConfig(
            name="full",
            version=VERSION,
            description="If you want to use all the ASSIN data (Brazilian Portuguese and European Portuguese)",
        ),
        datasets.BuilderConfig(
            name="ptpt",
            version=VERSION,
            description="If you want to use only the ASSIN European Portuguese subset",
        ),
        datasets.BuilderConfig(
            name="ptbr",
            version=VERSION,
            description="If you want to use only the ASSIN Brazilian Portuguese subset",
        ),
    ]

    DEFAULT_CONFIG_NAME = "full"

    def _info(self):
        features = datasets.Features(
            {
                "sentence_pair_id": datasets.Value("int64"),
                "premise": datasets.Value("string"),
                "hypothesis": datasets.Value("string"),
                "relatedness_score": datasets.Value("float32"),
                "entailment_judgment": datasets.features.ClassLabel(names=["NONE", "ENTAILMENT", "PARAPHRASE"]),
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
        archive = dl_manager.download(_URL)

        train_paths = []
        dev_paths = []
        test_paths = []

        if self.config.name == "full" or self.config.name == "ptpt":
            train_paths.append("assin-ptpt-train.xml")
            dev_paths.append("assin-ptpt-dev.xml")
            test_paths.append("assin-ptpt-test.xml")

        if self.config.name == "full" or self.config.name == "ptbr":
            train_paths.append("assin-ptbr-train.xml")
            dev_paths.append("assin-ptbr-dev.xml")
            test_paths.append("assin-ptbr-test.xml")

        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={
                    "filepaths": train_paths,
                    "files": dl_manager.iter_archive(archive),
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                gen_kwargs={
                    "filepaths": test_paths,
                    "files": dl_manager.iter_archive(archive),
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                gen_kwargs={
                    "filepaths": dev_paths,
                    "files": dl_manager.iter_archive(archive),
                },
            ),
        ]

    def _generate_examples(self, filepaths, files):
        """Yields examples."""

        id_ = 0

        for path, f in files:
            if path in filepaths:

                tree = ET.parse(f)
                root = tree.getroot()

                for pair in root:

                    yield id_, {
                        "sentence_pair_id": int(pair.attrib.get("id")),
                        "premise": pair.find(".//t").text,
                        "hypothesis": pair.find(".//h").text,
                        "relatedness_score": float(pair.attrib.get("similarity")),
                        "entailment_judgment": pair.attrib.get("entailment").upper(),
                    }

                    id_ += 1
