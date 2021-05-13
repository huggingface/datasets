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
"""LeNER-Br dataset"""


import datasets


logger = datasets.logging.get_logger(__name__)


_CITATION = """
@inproceedings{luz_etal_propor2018,
    author = {Pedro H. {Luz de Araujo} and Te\'{o}filo E. {de Campos} and
    Renato R. R. {de Oliveira} and Matheus Stauffer and
    Samuel Couto and Paulo Bermejo},
    title = {{LeNER-Br}: a Dataset for Named Entity Recognition in {Brazilian} Legal Text},
    booktitle = {International Conference on the Computational Processing of Portuguese ({PROPOR})},
    publisher = {Springer},
    series = {Lecture Notes on Computer Science ({LNCS})},
    pages = {313--323},
    year = {2018},
    month = {September 24-26},
    address = {Canela, RS, Brazil},
    doi = {10.1007/978-3-319-99722-3_32},
    url = {https://cic.unb.br/~teodecampos/LeNER-Br/},
}
"""

_DESCRIPTION = """
LeNER-Br is a Portuguese language dataset for named entity recognition
applied to legal documents. LeNER-Br consists entirely of manually annotated
legislation and legal cases texts and contains tags for persons, locations,
time entities, organizations, legislation and legal cases.
To compose the dataset, 66 legal documents from several Brazilian Courts were
collected. Courts of superior and state levels were considered, such as Supremo
Tribunal Federal, Superior Tribunal de Justiça, Tribunal de Justiça de Minas
Gerais and Tribunal de Contas da União. In addition, four legislation documents
were collected, such as "Lei Maria da Penha", giving a total of 70 documents
"""

_HOMEPAGE = "https://cic.unb.br/~teodecampos/LeNER-Br/"

_URL = "https://github.com/peluz/lener-br/raw/master/leNER-Br/"
_TRAINING_FILE = "train/train.conll"
_DEV_FILE = "dev/dev.conll"
_TEST_FILE = "test/test.conll"


class LenerBr(datasets.GeneratorBasedBuilder):
    """LeNER-Br dataset"""

    VERSION = datasets.Version("1.0.0")

    BUILDER_CONFIGS = [
        datasets.BuilderConfig(name="lener_br", version=VERSION, description="LeNER-Br dataset"),
    ]

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "id": datasets.Value("string"),
                    "tokens": datasets.Sequence(datasets.Value("string")),
                    "ner_tags": datasets.Sequence(
                        datasets.features.ClassLabel(
                            names=[
                                "O",
                                "B-ORGANIZACAO",
                                "I-ORGANIZACAO",
                                "B-PESSOA",
                                "I-PESSOA",
                                "B-TEMPO",
                                "I-TEMPO",
                                "B-LOCAL",
                                "I-LOCAL",
                                "B-LEGISLACAO",
                                "I-LEGISLACAO",
                                "B-JURISPRUDENCIA",
                                "I-JURISPRUDENCIA",
                            ]
                        )
                    ),
                }
            ),
            supervised_keys=None,
            homepage="https://cic.unb.br/~teodecampos/LeNER-Br/",
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        urls_to_download = {
            "train": f"{_URL}{_TRAINING_FILE}",
            "dev": f"{_URL}{_DEV_FILE}",
            "test": f"{_URL}{_TEST_FILE}",
        }
        downloaded_files = dl_manager.download_and_extract(urls_to_download)

        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={"filepath": downloaded_files["train"], "split": "train"},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                gen_kwargs={"filepath": downloaded_files["dev"], "split": "validation"},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                gen_kwargs={"filepath": downloaded_files["test"], "split": "test"},
            ),
        ]

    def _generate_examples(self, filepath, split):
        """Yields examples."""

        logger.info("⏳ Generating examples from = %s", filepath)

        with open(filepath, encoding="utf-8") as f:

            guid = 0
            tokens = []
            ner_tags = []

            for line in f:
                if line == "" or line == "\n":
                    if tokens:
                        yield guid, {
                            "id": str(guid),
                            "tokens": tokens,
                            "ner_tags": ner_tags,
                        }
                        guid += 1
                        tokens = []
                        ner_tags = []
                else:
                    splits = line.split(" ")
                    tokens.append(splits[0])
                    ner_tags.append(splits[1].rstrip())

            # last example
            yield guid, {
                "id": str(guid),
                "tokens": tokens,
                "ner_tags": ner_tags,
            }
