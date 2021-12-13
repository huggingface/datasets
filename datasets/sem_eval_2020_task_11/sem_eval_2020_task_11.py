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


import glob
import os
from collections import defaultdict

import datasets


_CITATION = """
@misc{martino2020semeval2020,
      title={SemEval-2020 Task 11: Detection of Propaganda Techniques in News Articles},
      author={G. Da San Martino and A. Barrón-Cedeño and H. Wachsmuth and R. Petrov and P. Nakov},
      year={2020},
      eprint={2009.02696},
      archivePrefix={arXiv},
      primaryClass={cs.CL}
}
"""

_DESCRIPTION = """\
Propagandistic news articles use specific techniques to convey their message,
such as whataboutism, red Herring, and name calling, among many others.
The Propaganda Techniques Corpus (PTC) allows to study automatic algorithms to
detect them. We provide a permanent leaderboard to allow researchers both to
advertise their progress and to be up-to-speed with the state of the art on the
tasks offered (see below for a definition).
"""

_HOMEPAGE = "https://propaganda.qcri.org/ptc/index.html"

_LICENSE = ""


class SemEval_2020Task_11(datasets.GeneratorBasedBuilder):
    """Semeval 2020 task 11 propaganda detection dataset"""

    VERSION = datasets.Version("1.1.0")

    @property
    def manual_download_instructions(self):
        return """\
        To access the data for this task, register for the task at:
        https://propaganda.qcri.org/ptc/registration.php

        Once registered, go to the main page (https://propaganda.qcri.org/ptc/index.html)
        and enter your passcode to access your team page.

        Alternately, your team page can be access directly with your passcode via the url:
        https://propaganda.qcri.org/ptc/teampage.php?passcode=<YOUR_PASSCODE_HERE>

        From your team page, click on the download link for "PTC Corpus - Version 2".

        Untar this file with `tar -xvf ptc-corpus.tgz`, which will produce a directory called
        `datasets` which contains the subdirectories for text and annotations.

        To load the dataset, pass in the full path to the `datasets` directory
        in your call to `datasets.load_dataset('sem_eval_2020_task_11', data_dir=<path_to_datasets_dir>/datasets)`
        """

    def _info(self):
        features = datasets.Features(
            {
                "article_id": datasets.Value("string"),
                "text": datasets.Value("string"),
                "span_identification": datasets.features.Sequence(
                    {"start_char_offset": datasets.Value("int64"), "end_char_offset": datasets.Value("int64")}
                ),
                "technique_classification": datasets.features.Sequence(
                    {
                        "start_char_offset": datasets.Value("int64"),
                        "end_char_offset": datasets.Value("int64"),
                        "technique": datasets.features.ClassLabel(
                            names=[
                                "Appeal_to_Authority",
                                "Appeal_to_fear-prejudice",
                                "Bandwagon,Reductio_ad_hitlerum",
                                "Black-and-White_Fallacy",
                                "Causal_Oversimplification",
                                "Doubt",
                                "Exaggeration,Minimisation",
                                "Flag-Waving",
                                "Loaded_Language",
                                "Name_Calling,Labeling",
                                "Repetition",
                                "Slogans",
                                "Thought-terminating_Cliches",
                                "Whataboutism,Straw_Men,Red_Herring",
                            ]
                        ),
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
        path_to_manual_file = os.path.abspath(os.path.expanduser(dl_manager.manual_dir))

        tc_labels_template = os.path.join(path_to_manual_file, "test-task-tc-template.out")
        tc_test_template = self._process_tc_labels_template(tc_labels_template)

        keys = {}
        for split in ["train", "dev", "test"]:
            articles_path = os.path.join(path_to_manual_file, f"{split}-articles")
            articles_files = glob.glob(os.path.join(articles_path, "*.txt"))
            keys[split] = [os.path.splitext(os.path.basename(af))[0] for af in articles_files]

        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={"data_dir": path_to_manual_file, "keys": keys["train"], "split": "train", "labels": True},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "data_dir": path_to_manual_file,
                    "keys": keys["test"],
                    "split": "test",
                    "labels": False,
                    "tc_test_template": tc_test_template,
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={"data_dir": path_to_manual_file, "keys": keys["dev"], "split": "dev", "labels": True},
            ),
        ]

    def _generate_examples(self, data_dir, keys, split, labels, tc_test_template=None):
        """Yields examples."""

        # Get the main path for the articles
        articles_path = os.path.join(data_dir, f"{split}-articles")

        # If the split has labels, get the main paths for labels
        if labels:
            si_labels_dir = os.path.join(data_dir, f"{split}-labels-task-si")
            tc_labels_dir = os.path.join(data_dir, f"{split}-labels-task-flc-tc")

        # Iterate through each article
        for id_, key in enumerate(sorted(keys)):
            text_path = os.path.join(articles_path, key + ".txt")

            # Read the text for the article
            with open(text_path, encoding="utf-8") as f:
                text = f.read()

            # If the split has labels, load and parse the labels data
            if labels:

                # Get the path for the span labels for the current article
                # and load/split (tab-delimited) label file
                si_labels_path = os.path.join(si_labels_dir, f"{key}.task-si.labels")
                with open(si_labels_path, encoding="utf-8") as f:
                    si_labels = f.readlines()
                si_labels = [label.rstrip("\n").split("\t") for label in si_labels]

                # Span identification task is binary span classification,
                # so there is no associated label for the span
                # (i.e. tagged spans here belong to the positive class)
                span_identification = [
                    {"start_char_offset": int(i[1]), "end_char_offset": int(i[2])} for i in si_labels
                ]

                # Get the path for the technique labels for the current article
                # and load/split (tab-delimited) label file
                tc_labels_path = os.path.join(tc_labels_dir, f"{key}.task-flc-tc.labels")
                with open(tc_labels_path, encoding="utf-8") as f:
                    tc_labels = f.readlines()
                tc_labels = [label.rstrip("\n").split("\t") for label in tc_labels]

                # Technique classification task is a multi-class span classification task
                # so we load the start/end char offsets _as well as_ the class label for the span
                technique_classification = [
                    {"start_char_offset": int(i[2]), "end_char_offset": int(i[3]), "technique": i[1]}
                    for i in tc_labels
                ]

            else:
                # If the split _doesn't_ have labels, return empty lists
                # for the span and technique classification labels
                span_identification = []
                technique_classification = []

                # Add span offsets for technique classification task if provided
                if tc_test_template is not None:
                    tc_labels = tc_test_template[key]
                    technique_classification = [
                        {"start_char_offset": int(i[2]), "end_char_offset": int(i[3]), "technique": -1}
                        for i in tc_labels
                    ]

            yield id_, {
                "article_id": key,
                "text": text,
                "span_identification": span_identification,
                "technique_classification": technique_classification,
            }

    def _process_tc_labels_template(self, tc_labels_template):
        with open(tc_labels_template, encoding="utf-8") as f:
            tc_labels_test = f.readlines()

        tc_labels_test = [line.rstrip("\n").split("\t") for line in tc_labels_test]

        tc_test_template = defaultdict(lambda: [])

        for tc_label in tc_labels_test:
            key = tc_label[0]
            tc_test_template[f"article{key}"].append(tc_label)

        return tc_test_template
