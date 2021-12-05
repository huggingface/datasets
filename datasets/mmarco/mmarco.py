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
"""mMARCO dataset."""


import json
import datasets


_CITATION = """
@misc{bonifacio2021mmarco,
      title={mMARCO: A Multilingual Version of the MS MARCO Passage Ranking Dataset}, 
      author={Luiz Henrique Bonifacio and Israel Campiotti and Vitor Jeronymo and Roberto Lotufo and Rodrigo Nogueira},
      year={2021},
      eprint={2108.13897},
      archivePrefix={arXiv},
      primaryClass={cs.CL}
}
"""

_DESCRIPTION = """
mMARCO translated datasets
"""

_V1_BASE_URLS = {
    "collections": "https://huggingface.co/datasets/unicamp-dl/mmarco/resolve/main/data/v1.1/collections/",
    "train":       "https://huggingface.co/datasets/unicamp-dl/mmarco/resolve/main/data/v1.1/queries/train/",
    "dev":         "https://huggingface.co/datasets/unicamp-dl/mmarco/resolve/main/data/v1.1/queries/dev/",
}


class MsMarcoConfig(datasets.BuilderConfig):
    """BuilderConfig for MS MARCO."""
    language: str = "english"

    def __init__(self, **kwargs):
        """BuilderConfig for MS MARCO

        Args:
          **kwargs: keyword arguments forwarded to super.
        """
        super(MsMarcoConfig, self).__init__(**kwargs)


class MsMarco(datasets.GeneratorBasedBuilder):

    BUILDER_CONFIGS = [
        MsMarcoConfig(
            name="v1.1",
            description="""version v1.1""",
            version=datasets.Version("1.1.0", ""),
        ),
        MsMarcoConfig(
            name="v2.1",
            description="""version v2.1""",
            version=datasets.Version("2.1.0", ""),
        ),
    ]

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION + "\n" + self.config.description,
            features=datasets.Features(
                {
                    "doc_id": datasets.Value("int32"),
                    "document": datasets.Value("string")
                }
            ),
            homepage="https://github.com/unicamp-dl/mMARCO",
            citation=_CITATION
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        
        if self.config.name == "v2.1":
            dl_path = dl_manager.download_and_extract(_V2_URLS)
        else:
            _V1_URLS = {
                "collections": _V1_BASE_URLS["collections"] + self.config.language + '_collection.tsv',
                "train": _V1_BASE_URLS["train"] + self.config.language + '_queries.train.tsv',
                "dev": _V1_BASE_URLS["dev"] + self.config.language + '_queries.dev.tsv'
            }
            dl_path = dl_manager.download_and_extract(_V1_URLS)
        
        return [
            datasets.SplitGenerator(
                name="collection",
                gen_kwargs={"filepath": dl_path["collections"]}
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={"filepath": dl_path["train"]}
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                gen_kwargs={"filepath": dl_path["dev"]}
            ),
        ]

    def _generate_examples(self, filepath):
        """Yields examples."""
        with open(filepath, encoding="utf-8") as f:
            if self.config.name == "v1.1":
                for line in f:
                    doc_id, doc = line.rstrip().split('\t')
                    features = {
                        "doc_id": doc_id,
                        "document": doc
                    }
                    yield doc_id, features