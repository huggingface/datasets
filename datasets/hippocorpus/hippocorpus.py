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


import csv
import os

import datasets


# Find for instance the citation on arxiv or on the dataset repo/website
_CITATION = """\
@inproceedings{sap-etal-2020-recollection,
    title = "Recollection versus Imagination: Exploring Human Memory and Cognition via Neural Language Models",
    author = "Sap, Maarten  and
      Horvitz, Eric  and
      Choi, Yejin  and
      Smith, Noah A.  and
      Pennebaker, James",
    booktitle = "Proceedings of the 58th Annual Meeting of the Association for Computational Linguistics",
    month = jul,
    year = "2020",
    address = "Online",
    publisher = "Association for Computational Linguistics",
    url = "https://www.aclweb.org/anthology/2020.acl-main.178",
    doi = "10.18653/v1/2020.acl-main.178",
    pages = "1970--1978",
    abstract = "We investigate the use of NLP as a measure of the cognitive processes involved in storytelling, contrasting imagination and recollection of events. To facilitate this, we collect and release Hippocorpus, a dataset of 7,000 stories about imagined and recalled events. We introduce a measure of narrative flow and use this to examine the narratives for imagined and recalled events. Additionally, we measure the differential recruitment of knowledge attributed to semantic memory versus episodic memory (Tulving, 1972) for imagined and recalled storytelling by comparing the frequency of descriptions of general commonsense events with more specific realis events. Our analyses show that imagined stories have a substantially more linear narrative flow, compared to recalled stories in which adjacent sentences are more disconnected. In addition, while recalled stories rely more on autobiographical events based on episodic memory, imagined stories express more commonsense knowledge based on semantic memory. Finally, our measures reveal the effect of narrativization of memories in stories (e.g., stories about frequently recalled memories flow more linearly; Bartlett, 1932). Our findings highlight the potential of using NLP tools to study the traces of human cognition in language.",
}
"""

_DESCRIPTION = """\
To examine the cognitive processes of remembering and imagining and their traces in language, we introduce Hippocorpus, a dataset of 6,854 English diary-like short stories about recalled and imagined events. Using a crowdsourcing framework, we first collect recalled stories and summaries from workers, then provide these summaries to other workers who write imagined stories. Finally, months later, we collect a retold version of the recalled stories from a subset of recalled authors. Our dataset comes paired with author demographics (age, gender, race), their openness to experience, as well as some variables regarding the author's relationship to the event (e.g., how personal the event is, how often they tell its story, etc.).
"""

_HOMEPAGE = "https://msropendata.com/datasets/0a83fb6f-a759-4a17-aaa2-fbac84577318"


class Hippocorpus(datasets.GeneratorBasedBuilder):

    VERSION = datasets.Version("1.1.0")

    @property
    def manual_download_instructions(self):
        return """\
  To use hippocorpus you need to download it manually. Please go to its homepage (https://msropendata.com/datasets/0a83fb6f-a759-4a17-aaa2-fbac84577318)and login. Extract all files in one folder and use the path folder in datasets.load_dataset('hippocorpus', data_dir='path/to/folder/folder_name')
  """

    def _info(self):
        return datasets.DatasetInfo(
            # This is the description that will appear on the datasets page.
            description=_DESCRIPTION,
            # datasets.features.FeatureConnectors
            features=datasets.Features(
                {
                    # These are the features of your dataset like images, labels ...
                    "AssignmentId": datasets.Value("string"),
                    "WorkTimeInSeconds": datasets.Value("string"),
                    "WorkerId": datasets.Value("string"),
                    "annotatorAge": datasets.Value("float32"),
                    "annotatorGender": datasets.Value("string"),
                    "annotatorRace": datasets.Value("string"),
                    "distracted": datasets.Value("float32"),
                    "draining": datasets.Value("float32"),
                    "frequency": datasets.Value("float32"),
                    "importance": datasets.Value("float32"),
                    "logTimeSinceEvent": datasets.Value("string"),
                    "mainEvent": datasets.Value("string"),
                    "memType": datasets.Value("string"),
                    "mostSurprising": datasets.Value("string"),
                    "openness": datasets.Value("string"),
                    "recAgnPairId": datasets.Value("string"),
                    "recImgPairId": datasets.Value("string"),
                    "similarity": datasets.Value("string"),
                    "similarityReason": datasets.Value("string"),
                    "story": datasets.Value("string"),
                    "stressful": datasets.Value("string"),
                    "summary": datasets.Value("string"),
                    "timeSinceEvent": datasets.Value("string"),
                }
            ),
            # If there's a common (input, target) tuple from the features,
            # specify them here. They'll be used if as_supervised=True in
            # builder.as_dataset.
            supervised_keys=None,
            # Homepage of the dataset for documentation
            homepage=_HOMEPAGE,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        # dl_manager is a datasets.download.DownloadManager that can be used to
        # download and extract URLs
        data_dir = os.path.abspath(os.path.expanduser(dl_manager.manual_dir))

        if not os.path.exists(data_dir):
            raise FileNotFoundError(
                "{data_dir} does not exist. Make sure you insert a manual dir via `datasets.load_dataset('hippocorpus', data_dir=...)` that includes files unzipped from the hippocorpus zip. Manual download instructions: {self.manual_download_instructions}"
            )
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={"filepath": os.path.join(data_dir, "hippoCorpusV2.csv")},
            ),
        ]

    def _generate_examples(self, filepath):
        """Yields examples."""
        with open(filepath, encoding="utf-8") as f:
            data = csv.DictReader(f, delimiter=",", quoting=csv.QUOTE_NONE)
            for id_, row in enumerate(data):
                yield id_, {
                    "AssignmentId": row["AssignmentId"],
                    "WorkTimeInSeconds": row["WorkTimeInSeconds"],
                    "WorkerId": row["WorkerId"],
                    "annotatorAge": row["annotatorAge"],
                    "annotatorGender": row["annotatorGender"],
                    "annotatorRace": row["annotatorRace"],
                    "distracted": row["distracted"],
                    "draining": row["draining"],
                    "frequency": row["frequency"],
                    "importance": row["importance"],
                    "logTimeSinceEvent": row["logTimeSinceEvent"],
                    "mainEvent": row["mainEvent"],
                    "memType": row["memType"],
                    "mostSurprising": row["mostSurprising"],
                    "openness": row["openness"],
                    "recAgnPairId": row["recAgnPairId"],
                    "recImgPairId": row["recImgPairId"],
                    "similarity": row["similarity"],
                    "similarityReason": row["similarityReason"],
                    "story": row["story"],
                    "stressful": row["stressful"],
                    "summary": row["summary"],
                    "timeSinceEvent": row["timeSinceEvent"],
                }
