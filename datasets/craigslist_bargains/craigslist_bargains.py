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
"""TODO: Add a description here."""


import json

import datasets


_CITATION = """\
@misc{he2018decoupling,
    title={Decoupling Strategy and Generation in Negotiation Dialogues},
    author={He He and Derek Chen and Anusha Balakrishnan and Percy Liang},
    year={2018},
    eprint={1808.09637},
    archivePrefix={arXiv},
    primaryClass={cs.CL}
}
"""

_DESCRIPTION = """\
We study negotiation dialogues where two agents, a buyer and a seller,
negotiate over the price of an time for sale. We collected a dataset of more
than 6K negotiation dialogues over multiple categories of products scraped from Craigslist.
Our goal is to develop an agent that negotiates with humans through such conversations.
The challenge is to handle both the negotiation strategy and the rich language for bargaining.
"""

_HOMEPAGE = "https://stanfordnlp.github.io/cocoa/"

_LICENSE = ""

_URLs = {
    "train": "https://worksheets.codalab.org/rest/bundles/0xd34bbbc5fb3b4fccbd19e10756ca8dd7/contents/blob/parsed.json",
    "validation": "https://worksheets.codalab.org/rest/bundles/0x15c4160b43d44ee3a8386cca98da138c/contents/blob/parsed.json",
    "test": "https://worksheets.codalab.org/rest/bundles/0x54d325bbcfb2463583995725ed8ca42b/contents/blob/",
}


class CraigslistBargains(datasets.GeneratorBasedBuilder):
    """
    Dialogue for buyer and a seller negotiating
    the price of an item for sale on Craigslist.
    """

    VERSION = datasets.Version("1.1.0")

    def _info(self):
        features = datasets.Features(
            {
                "agent_info": datasets.features.Sequence(
                    {
                        "Bottomline": datasets.Value("string"),
                        "Role": datasets.Value("string"),
                        "Target": datasets.Value("float"),
                    }
                ),
                "agent_turn": datasets.features.Sequence(datasets.Value("int32")),
                "dialogue_acts": datasets.features.Sequence(
                    {"intent": datasets.Value("string"), "price": datasets.Value("float")}
                ),
                "utterance": datasets.features.Sequence(datasets.Value("string")),
                "items": datasets.features.Sequence(
                    {
                        "Category": datasets.Value("string"),
                        "Images": datasets.Value("string"),
                        "Price": datasets.Value("float"),
                        "Description": datasets.Value("string"),
                        "Title": datasets.Value("string"),
                    }
                ),
            }
        )

        return datasets.DatasetInfo(
            # This is the description that will appear on the datasets page.
            description=_DESCRIPTION,
            # This defines the different columns of the dataset and their types
            features=features,  # Here we define them above because they are different between the two configurations
            # If there's a common (input, target) tuple from the features,
            # specify them here. They'll be used if as_supervised=True in
            # builder.as_dataset.
            supervised_keys=None,
            # Homepage of the dataset for documentation
            homepage=_HOMEPAGE,
            # License for the dataset if available
            license=_LICENSE,
            # Citation for the dataset
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""

        my_urls = _URLs
        data_dir = dl_manager.download_and_extract(my_urls)

        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "filepath": data_dir["train"],
                    "split": "train",
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={"filepath": data_dir["test"], "split": "test"},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "filepath": data_dir["validation"],
                    "split": "validation",
                },
            ),
        ]

    def _generate_examples(self, filepath, split):
        """Yields examples."""

        # Set default values for items when the information is missing
        # `items` is the description of the item advertised on craigslist
        # to which the conversation is referring
        default_items = {"Category": "", "Images": "", "Price": -1.0, "Description": "", "Title": ""}

        # Set default values for the rules-based `metadata` generated by
        # the Stanford NLP Cocoa project for the Craigslist Bargains dataset
        # For more information on producing the `metadata` values for the train
        # and dev sets, see https://worksheets.codalab.org/bundles/0xd34bbbc5fb3b4fccbd19e10756ca8dd7
        default_metadata = {"price": -1.0, "intent": ""}

        with open(filepath, encoding="utf-8") as f:
            concat_sep = ","
            jsons = json.loads(f.read())
            for id_, j in enumerate(jsons):

                # Get scenario information.
                # This is nformation about position of each agent
                scenario = j.get("scenario")
                kbs = scenario["kbs"]
                agent_info = [kb["personal"] for kb in kbs]
                agent_info = [{k: str(v) for k, v in ai.items()} for ai in agent_info]

                # Get item information.
                # This is information about item listing for each agent
                items = [i["item"] for i in kbs]

                # Flatten `list` elements in items
                # (e.g. if there are multiple image names, descriptions...)
                # to align more easily with arrow schema
                for item in items:
                    for k in item:
                        if type(item[k]) == list:
                            item[k] = concat_sep.join(item[k])

                # Check for missing elements in `items`
                # and fill with default values
                for item in items:
                    for k in default_items:
                        if k not in item:
                            item[k] = default_items[k]
                        elif not item[k]:
                            item[k] = default_items[k]

                # Get interaction information.
                # This is information about messages exchanged
                # and rules-based dialogue acts assigned to each
                # dialogue segment
                events = j.get("events")
                agents = [e.get("agent") for e in events]
                agents = [a if type(a) == int else -1 for a in agents]
                data = [e.get("data") for e in events]
                utterances = [u if type(u) == str else "" for u in data]

                metadata = [e.get("metadata") for e in events]
                metadata = [m if m else default_metadata for m in metadata]

                # Check for missing keys in metadata, or missing
                # metadata altogether for test data split.
                # If anything missing, fill with defaults above.
                for m in metadata:
                    for k in default_metadata:
                        if k not in m:
                            m[k] = default_metadata[k]
                        elif not m[k]:
                            m[k] = default_metadata[k]

                yield id_, {
                    "agent_info": agent_info,
                    "agent_turn": agents,
                    "dialogue_acts": metadata,
                    "utterance": utterances,
                    "items": items,
                }
