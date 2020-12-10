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
"""Doc2dial: A Goal-Oriented Document-Grounded Dialogue Dataset v0.9"""

from __future__ import absolute_import, division, print_function

import json
import os
import logging

import datasets

_CITATION = """\
@inproceedings{feng-etal-2020-doc2dial,
    title = "doc2dial: A Goal-Oriented Document-Grounded Dialogue Dataset",
    author = "Feng, Song  and Wan, Hui  and Gunasekara, Chulaka  and Patel, Siva  and Joshi, Sachindra  and Lastras, Luis",
    booktitle = "Proceedings of the 2020 Conference on Empirical Methods in Natural Language Processing (EMNLP)",
    month = nov,
    year = "2020",
    publisher = "Association for Computational Linguistics",
    url = "https://www.aclweb.org/anthology/2020.emnlp-main.652",
}
"""

_DESCRIPTION = """\
Doc2dial is dataset of goal-oriented dialogues that are grounded in the associated documents. \
It includes over 4500 annotated conversations with an average of 14 turns that are grounded \
in over 450 documents from four domains. Compared to the prior document-grounded dialogue datasets \
this dataset covers a variety of dialogue scenes in information-seeking conversations.
"""

_HOMEPAGE = "https://doc2dial.github.io/file/doc2dial/"

# TODO: Add the licence for the dataset here if you can find it
_LICENSE = ""

_URLs = {
    'dialogue_domain': "https://doc2dial.github.io/file/doc2dial.zip",
    'document_domain': "https://doc2dial.github.io/file/doc2dial.zip",
}

# class Doc2dialConfig(datasets.BuilderConfig):
#     """BuilderConfig for Doc2dial."""

#     def __init__(self, **kwargs):
#         """BuilderConfig for Doc2dial.

#         Args:
#           **kwargs: keyword arguments forwarded to super.
#         """
#         super(Doc2dialConfig, self).__init__(**kwargs)

class Doc2dial(datasets.GeneratorBasedBuilder):
    "Doc2dial: A Goal-Oriented Document-Grounded Dialogue Dataset v0.9"

    VERSION = datasets.Version("1.1.0")

    # You will be able to load one or the other configurations in the following list with
    # data = datasets.load_dataset('my_dataset', 'first_domain')
    # data = datasets.load_dataset('my_dataset', 'second_domain')
    BUILDER_CONFIGS = [
        datasets.BuilderConfig(name="dialogue_domain", version=VERSION, description="This part of my dataset covers a first domain"),
        datasets.BuilderConfig(name="document_domain", version=VERSION, description="This part of my dataset covers a second domain"),
    ]

    DEFAULT_CONFIG_NAME = "dialogue_domain" 

    def _info(self):

        if self.config.name == "dialogue_domain":
            features=datasets.Features(
                {
                    "dial_id": datasets.Value("string"),
                    "doc_id": datasets.Value("string"),
                    "domain": datasets.Value("string"),
                    # "turns": [
                    #     {
                    #         "turn_id": datasets.Value("int32"),
                    #         "role": datasets.Value("string"),
                    #         "da": datasets.Value("string"),
                    #         "reference": [
                    #             {
                    #                 "keys" : datasets.Value("string"),
                    #                 "values": datasets.Value("string"),   
                    #             }

                    #         ],
                    #         "utterance": datasets.Value("string"),
                    #     }
                    # ],
                }
            ),
        elif self.config.name == "document_domain":
            features = datasets.Features(
                {
                    "domain": datasets.Value("string"),
                    "doc_id": datasets.Value("string"),
                    "title": datasets.Value("string"),
                    "doc_text": datasets.Value("string"),
                    "spans" : datasets.Sequence(
                        {
                            "id_sp": datasets.Value("string"),
                            "tag": datasets.Value("string"),
                            "start_sp": datasets.Value("string"),
                            "end_sp": datasets.Value("string"),
                            "text_sp": datasets.Value("string"),
                            "title": datasets.Value("string"),
                            "parent_titles": datasets.Value("string"),
                            "id_sec": datasets.Value("string"),
                            "start_sec": datasets.Value("string"),
                            "text_sec": datasets.Value("string"),
                            "end_sec": datasets.Value("string"), 
                        }
                    ),                            
                }
            )

        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=features,
            # # No default supervised_keys (as we have to pass both question
            # # and context as input).
            supervised_keys=None,
            homepage=_HOMEPAGE,
            # citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        
        my_urls = _URLs[self.config.name]
        print('my_url:',my_urls)
        data_dir = dl_manager.download_and_extract(my_urls)

        if self.config.name == "dialogue_domain":
            return [
                datasets.SplitGenerator(name=datasets.Split.TRAIN, gen_kwargs={"filepath": os.path.join(data_dir, "doc2dial/v0.9/data/woOOD/doc2dial_dial_train.json")}),
                datasets.SplitGenerator(name=datasets.Split.VALIDATION, gen_kwargs={"filepath": os.path.join(data_dir, "doc2dial/v0.9/data/woOOD/doc2dial_dial_dev.json")}),
            ]
        elif self.config.name == "document_domain":
            return [
                datasets.SplitGenerator(name=datasets.Split.TRAIN, gen_kwargs={"filepath": os.path.join(data_dir, "doc2dial/v0.9/data/doc2dial_doc.json")}),
            ]

    def _generate_examples(self, filepath):
        """This function returns the examples in the raw (text) form."""

        # filepath = "/Users/karimfoda/Downloads/doc2dial/v0.9/data/woOOD/doc2dial_dial_dev.json"
        
        if self.config.name == "dialogue_domain":
            logging.info("generating examples from = %s", filepath)
            with open(filepath, encoding="utf-8") as f:
                data = json.load(f)
                for domain in data["dial_data"]:
                    print(domain)
                    for doc_id in data["dial_data"][domain]:
                        print(doc_id)
                        for dialogue in data["dial_data"][domain][doc_id]:
                            print(dialogue["dial_id"])

                            # Features currently used are "context", "question", and "answers".
                            # Others are extracted here for the ease of future expansions.
                            # yield dialogue["dial_id"], {
                            #         "dial_id":dialogue["dial_id"],
                            #         "domain":domain,
                            #         "doc_id": doc_id,
                                    # "turns" : 
                                    # [{
                                    #     "turn_id" : i['turn_id'],
                                    #     "role" : i['role'],
                                    #     "da" : i['da'],
                                    #     "reference" : 
                                    #     [{ 
                                    #         "keys" : ref,
                                    #         "values" : i["reference"][ref],
                                    #         } for ref in i['reference']],
                                    #     "utterance" : i['utterance']
                                    # } for i in dialogue['turns']],
                                # }
        elif self.config.name == "document_domain":

            logging.info("generating examples from = %s", filepath)
            with open(filepath, encoding="utf-8") as f:
                data = json.load(f)
                for domain in data["doc_data"]:
                    for doc_id in data["dial_data"][domain]:
                            for dialogue in data["dial_data"][domain][doc_id]:
                                a = 1
                                # yield {
                                # "domain": domain,
                                # "doc_id": doc_id,
                                # "title": dialogue['title'],
                                # "doc_text": dialogue['doc_text'],
                                # "spans" : {
                                #     "id_sp": [i['id_sp'] for i in dialogue['spans']],
                                #     "tag": [i['tag'] for i in dialogue['spans']],
                                #     "start_sp": [i['start_sp'] for i in dialogue['spans']],
                                #     "end_sp": [i['end_sp'] for i in dialogue['spans']],
                                #     "text_sp": [i['text_sp'] for i in dialogue['spans']],
                                #     "title": [i['title'] for i in dialogue['spans']],
                                #     "parent_titles": [i['parent_titles'] for i in dialogue['spans']],
                                #     "id_sec": [i['id_sec'] for i in dialogue['spans']],
                                #     "start_sec": [i['start_sec'] for i in dialogue['spans']],
                                #     "text_sec": [i['text_sec'] for i in dialogue['spans']],
                                #     "end_sec": [i['end_sec'] for i in dialogue['spans']],                              
                                # }}