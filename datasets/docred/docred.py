"""DocRED: A Large-Scale Document-Level Relation Extraction Dataset"""

from __future__ import absolute_import, division, print_function

import json
import os

import datasets


_CITATION = """\
@inproceedings{yao2019DocRED,
  title={{DocRED}: A Large-Scale Document-Level Relation Extraction Dataset},
  author={Yao, Yuan and Ye, Deming and Li, Peng and Han, Xu and Lin, Yankai and Liu, Zhenghao and Liu, \
  Zhiyuan and Huang, Lixin and Zhou, Jie and Sun, Maosong},
  booktitle={Proceedings of ACL 2019},
  year={2019}
}
"""

_DESCRIPTION = """\
Multiple entities in a document generally exhibit complex inter-sentence relations, and cannot be well handled by \
existing relation extraction (RE) methods that typically focus on extracting intra-sentence relations for single \
entity pairs. In order to accelerate the research on document-level RE, we introduce DocRED, a new dataset constructed \
from Wikipedia and Wikidata with three features:
    - DocRED annotates both named entities and relations, and is the largest human-annotated dataset for document-level RE from plain text.
    - DocRED requires reading multiple sentences in a document to extract entities and infer their relations by synthesizing all information of the document.
    - Along with the human-annotated data, we also offer large-scale distantly supervised data, which enables DocRED to be adopted for both supervised and weakly supervised scenarios.
"""

_URLS = {
    "dev": "https://drive.google.com/uc?export=download&id=1fDmfUUo5G7gfaoqWWvK81u08m71TK2g7",
    "train_distant": "https://drive.google.com/uc?export=download&id=1fDmfUUo5G7gfaoqWWvK81u08m71TK2g7",
    "train_annotated": "https://drive.google.com/uc?export=download&id=1NN33RzyETbanw4Dg2sRrhckhWpzuBQS9",
    "test": "https://drive.google.com/uc?export=download&id=1lAVDcD94Sigx7gR3jTfStI66o86cflum",
    "rel_info": "https://drive.google.com/uc?id=1y9A0zKrvETc1ddUFuFhBg3Xfr7FEL4dW&export=download",
}


class DocRed(datasets.GeneratorBasedBuilder):
    """DocRED: A Large-Scale Document-Level Relation Extraction Dataset"""

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "title": datasets.Value("string"),
                    "sents": datasets.features.Sequence(datasets.features.Sequence(datasets.Value("string"))),
                    "vertexSet": [
                        [
                            {
                                "name": datasets.Value("string"),
                                "sent_id": datasets.Value("int32"),
                                "pos": datasets.features.Sequence(datasets.Value("int32")),
                                "type": datasets.Value("string"),
                            }
                        ]
                    ],
                    "labels": datasets.features.Sequence(
                        {
                            "head": datasets.Value("int32"),
                            "tail": datasets.Value("int32"),
                            "relation_id": datasets.Value("string"),
                            "relation_text": datasets.Value("string"),
                            "evidence": datasets.features.Sequence(datasets.Value("int32")),
                        }
                    ),
                }
            ),
            supervised_keys=None,
            homepage="https://github.com/thunlp/DocRED",
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        downloads = {}
        for key in _URLS.keys():
            downloads[key] = dl_manager.download_and_extract(_URLS[key])
            #  Fix for dummy data
            if os.path.isdir(downloads[key]):
                downloads[key] = os.path.join(downloads[key], key + ".json")

        return [
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                gen_kwargs={"filepath": downloads["dev"], "rel_info": downloads["rel_info"]},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST, gen_kwargs={"filepath": downloads["test"], "rel_info": downloads["rel_info"]}
            ),
            datasets.SplitGenerator(
                name="train_annotated",
                gen_kwargs={"filepath": downloads["train_annotated"], "rel_info": downloads["rel_info"]},
            ),
            datasets.SplitGenerator(
                name="train_distant",
                gen_kwargs={"filepath": downloads["train_distant"], "rel_info": downloads["rel_info"]},
            ),
        ]

    def _generate_examples(self, filepath, rel_info):
        """Generate DocRED examples."""
        relation_name_map = json.load(open(rel_info))
        data = json.load(open(filepath))

        for idx, example in enumerate(data):

            # Test set has no labels - Results need to be uploaded to Codalab
            if "labels" not in example.keys():
                example["labels"] = []

            for label in example["labels"]:
                # Rename and include full relation names
                label["relation_text"] = relation_name_map[label["r"]]
                label["relation_id"] = label["r"]
                label["head"] = label["h"]
                label["tail"] = label["t"]
                del label["r"]
                del label["h"]
                del label["t"]

            yield idx, example
