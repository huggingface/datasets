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
"""Wiki Asp datasert for Multi-domain Aspect-based Summarization"""


import json
import os

import datasets


# Find for instance the citation on arxiv or on the dataset repo/website
_CITATION = """\
@article{hayashi20tacl,
  title   = {WikiAsp: A Dataset for Multi-domain Aspect-based Summarization},
  authors = {Hiroaki Hayashi and Prashant Budania and Peng Wang and Chris Ackerson and Raj Neervannan and Graham Neubig},
  journal = {Transactions of the Association for Computational Linguistics (TACL)},
  year    = {2020},
  url     = {https://arxiv.org/abs/2011.07832}
}
"""

_DESCRIPTION = """\
WikiAsp is a multi-domain, aspect-based summarization dataset in the encyclopedic
domain. In this task, models are asked to summarize cited reference documents of a
Wikipedia article into aspect-based summaries. Each of the 20 domains include 10
domain-specific pre-defined aspects.
"""

_HOMEPAGE = "https://github.com/neulab/wikiasp"

_LICENSE = "CC BY-SA 4.0"

# Download links
_URLs = {
    "album": "http://phontron.com/download/wikiasp/Album.tar.bz2",
    "animal": "http://phontron.com/download/wikiasp/Animal.tar.bz2",
    "artist": "http://phontron.com/download/wikiasp/Artist.tar.bz2",
    "building": "http://phontron.com/download/wikiasp/Building.tar.bz2",
    "company": "http://phontron.com/download/wikiasp/Company.tar.bz2",
    "educational_institution": "http://phontron.com/download/wikiasp/EducationalInstitution.tar.bz2",
    "event": "http://phontron.com/download/wikiasp/Event.tar.bz2",
    "film": "http://phontron.com/download/wikiasp/Film.tar.bz2",
    "group": "http://phontron.com/download/wikiasp/Group.tar.bz2",
    "historic_place": "http://phontron.com/download/wikiasp/HistoricPlace.tar.bz2",
    "infrastructure": "http://phontron.com/download/wikiasp/Infrastructure.tar.bz2",
    "mean_of_transportation": "http://phontron.com/download/wikiasp/MeanOfTransportation.tar.bz2",
    "office_holder": "http://phontron.com/download/wikiasp/OfficeHolder.tar.bz2",
    "plant": "http://phontron.com/download/wikiasp/Plant.tar.bz2",
    "single": "http://phontron.com/download/wikiasp/Single.tar.bz2",
    "soccer_player": "http://phontron.com/download/wikiasp/SoccerPlayer.tar.bz2",
    "software": "http://phontron.com/download/wikiasp/Software.tar.bz2",
    "television_show": "http://phontron.com/download/wikiasp/TelevisionShow.tar.bz2",
    "town": "http://phontron.com/download/wikiasp/Town.tar.bz2",
    "written_work": "http://phontron.com/download/wikiasp/WrittenWork.tar.bz2",
}


class WikiAsp(datasets.GeneratorBasedBuilder):
    """TODO: Short description of my dataset."""

    VERSION = datasets.Version("1.1.0")

    # This is an example of a dataset with multiple configurations.
    # If you don't want/need to define several sub-sets in your dataset,
    # just remove the BUILDER_CONFIG_CLASS and the BUILDER_CONFIGS attributes.

    # If you need to make complex sub-parts in the datasets with configurable options
    # You can create your own builder configuration class to store attribute, inheriting from datasets.BuilderConfig
    # BUILDER_CONFIG_CLASS = MyBuilderConfig

    # You will  be able to load one or the other configurations in the following list with
    # data = datasets.load_dataset('my_dataset', 'first_domain')
    # data = datasets.load_dataset('my_dataset', 'second_domain')
    BUILDER_CONFIGS = [
        datasets.BuilderConfig(
            name="album", version=VERSION, description="A subset of dataset from the musical album domain"
        ),
        datasets.BuilderConfig(
            name="animal", version=VERSION, description="A subset of dataset from the animal domain"
        ),
        datasets.BuilderConfig(
            name="artist", version=VERSION, description="A subset of dataset from the artist domain"
        ),
        datasets.BuilderConfig(
            name="building", version=VERSION, description="A subset of dataset from the buildings domain"
        ),
        datasets.BuilderConfig(
            name="company", version=VERSION, description="A subset of dataset from the company domain"
        ),
        datasets.BuilderConfig(
            name="educational_institution",
            version=VERSION,
            description="A subset of dataset from the educational institution domain",
        ),
        datasets.BuilderConfig(
            name="event", version=VERSION, description="A subset of dataset from the events domain"
        ),
        datasets.BuilderConfig(name="film", version=VERSION, description="A subset of dataset from the film domain"),
        datasets.BuilderConfig(name="group", version=VERSION, description="A subset of dataset from the group domain"),
        datasets.BuilderConfig(
            name="historic_place", version=VERSION, description="A subset of dataset from the historic places domain"
        ),
        datasets.BuilderConfig(
            name="infrastructure", version=VERSION, description="A subset of dataset from the infrastructure domain"
        ),
        datasets.BuilderConfig(
            name="mean_of_transportation",
            version=VERSION,
            description="A subset of dataset from the transportation mean domain",
        ),
        datasets.BuilderConfig(
            name="office_holder", version=VERSION, description="A subset of dataset from the office holder domain"
        ),
        datasets.BuilderConfig(name="plant", version=VERSION, description="A subset of dataset from the plant domain"),
        datasets.BuilderConfig(
            name="single", version=VERSION, description="A subset of dataset from the musical single domain"
        ),
        datasets.BuilderConfig(
            name="soccer_player", version=VERSION, description="A subset of dataset from the soccer player domain"
        ),
        datasets.BuilderConfig(
            name="software", version=VERSION, description="A subset of dataset from the software domain"
        ),
        datasets.BuilderConfig(
            name="television_show", version=VERSION, description="A subset of dataset from the television show domain"
        ),
        datasets.BuilderConfig(name="town", version=VERSION, description="A subset of dataset from the town domain"),
        datasets.BuilderConfig(
            name="written_work", version=VERSION, description="A subset of dataset from the written work domain"
        ),
    ]

    def _info(self):
        features = datasets.Features(
            {
                "exid": datasets.Value("string"),
                "inputs": datasets.Sequence(datasets.Value("string")),
                "targets": datasets.Sequence(datasets.Sequence(datasets.Value("string"))),
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
        my_urls = _URLs[self.config.name]
        data_dir = dl_manager.download_and_extract(my_urls)
        data_dir = os.path.join(data_dir, self.config.name.title().replace("_", ""))
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "filepath": os.path.join(data_dir, "train.jsonl"),
                    "split": "train",
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                gen_kwargs={"filepath": os.path.join(data_dir, "test.jsonl"), "split": "test"},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                gen_kwargs={
                    "filepath": os.path.join(data_dir, "valid.jsonl"),
                    "split": "dev",
                },
            ),
        ]

    def _generate_examples(self, filepath, split):
        """Yields examples."""
        with open(filepath, encoding="utf-8") as f:
            for id_, row in enumerate(f):
                data = json.loads(row)
                yield id_, {
                    "exid": data["exid"],
                    "inputs": data["inputs"],
                    "targets": data["targets"],
                }
