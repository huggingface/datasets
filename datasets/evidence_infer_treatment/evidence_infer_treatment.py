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
"""Inferring Which Medical Treatments Work from Reports of Clinical Trials"""

from __future__ import absolute_import, division, print_function

import csv
import os

import datasets


_CITATION = """\
@inproceedings{lehman-etal-2019-inferring,
    title = "Inferring Which Medical Treatments Work from Reports of Clinical Trials",
    author = "Lehman, Eric  and
      DeYoung, Jay  and
      Barzilay, Regina  and
      Wallace, Byron C.",
    booktitle = "Proceedings of the 2019 Conference of the North {A}merican Chapter of the Association for Computational Linguistics: Human Language Technologies, Volume 1 (Long and Short Papers)",
    month = jun,
    year = "2019",
    address = "Minneapolis, Minnesota",
    publisher = "Association for Computational Linguistics",
    url = "https://www.aclweb.org/anthology/N19-1371",
    pages = "3705--3717",
}
"""

_DESCRIPTION = """\
Data and code from our "Inferring Which Medical Treatments Work from Reports of Clinical Trials", NAACL 2019. This work concerns inferring the results reported in clinical trials from text.

The dataset consists of biomedical articles describing randomized control trials (RCTs) that compare multiple treatments. Each of these articles will have multiple questions, or 'prompts' associated with them. These prompts will ask about the relationship between an intervention and comparator with respect to an outcome, as reported in the trial. For example, a prompt may ask about the reported effects of aspirin as compared to placebo on the duration of headaches. For the sake of this task, we assume that a particular article will report that the intervention of interest either significantly increased, significantly decreased or had significant effect on the outcome, relative to the comparator.

The dataset could be used for automatic data extraction of the results of a given RCT. This would enable readers to discover the effectiveness of different treatments without needing to read the paper.
"""


class EvidenceInferenceConfig(datasets.BuilderConfig):
    """ BuilderConfig for NewDataset"""

    def __init__(self, zip_file, **kwargs):
        """

        Args:
            zip_file: The location of zip file containing original data
            **kwargs: keyword arguments forwarded to super.
        """
        self.zip_file = zip_file
        super().__init__(**kwargs)


class EvidenceInferTreatment(datasets.GeneratorBasedBuilder):
    f"""{_DESCRIPTION}"""

    # This is an example of a dataset with multiple configurations.
    # If you don't want/need to define several sub-sets in your dataset,
    # just remove the BUILDER_CONFIG_CLASS and the BUILDER_CONFIGS attributes.
    BUILDER_CONFIG_CLASS = EvidenceInferenceConfig
    BUILDER_CONFIGS = [
        EvidenceInferenceConfig(
            name="2.0",
            description="EvidenceInference V2",
            version=datasets.Version("2.0.0"),
            zip_file="http://evidence-inference.ebm-nlp.com/v2.0.tar.gz",
        ),
        EvidenceInferenceConfig(
            name="1.1",
            description="EvidenceInference V1.1",
            version=datasets.Version("1.1.0"),
            zip_file="https://github.com/jayded/evidence-inference/archive/v1.1.zip",
        ),
    ]

    def _info(self):
        features = datasets.Features(
            {
                "Text": datasets.Value("string"),
                "PMCID": datasets.Value("int32"),
                "Prompts": datasets.Sequence(
                    datasets.Features(
                        {
                            "PromptID": datasets.Value("int32"),
                            "PMCID": datasets.Value("int32"),
                            "Outcome": datasets.Value("string"),
                            "Intervention": datasets.Value("string"),
                            "Comparator": datasets.Value("string"),
                            "Annotations": datasets.Sequence(
                                datasets.Features(
                                    {
                                        "UserID": datasets.Value("int32"),
                                        "PromptID": datasets.Value("int32"),
                                        "PMCID": datasets.Value("int32"),
                                        "Valid Label": datasets.Value("bool"),
                                        "Valid Reasoning": datasets.Value("bool"),
                                        "Label": datasets.Value("string"),
                                        "Annotations": datasets.Value("string"),
                                        "Label Code": datasets.Value("int32"),
                                        "In Abstract": datasets.Value("bool"),
                                        "Evidence Start": datasets.Value("int32"),
                                        "Evidence End": datasets.Value("int32"),
                                    }
                                )
                            ),
                        }
                    )
                ),
            }
        )

        return datasets.DatasetInfo(
            # This is the description that will appear on the datasets page.
            description=_DESCRIPTION,
            # datasets.features.FeatureConnectors
            features=features,
            # If there's a common (input, target) tuple from the features,
            # specify them here. They'll be used if as_supervised=True in
            # builder.as_dataset.
            supervised_keys=None,
            # Homepage of the dataset for documentation
            homepage="https://github.com/jayded/evidence-inference",
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        dl_dir = dl_manager.download_and_extract(self.config.zip_file)
        if self.config.name == "1.1":
            dl_dir = os.path.join(dl_dir, "evidence-inference-1.1", "annotations")

        SPLITS = {}
        for split in ["train", "test", "validation"]:
            filename = os.path.join(dl_dir, "splits", f"{split}_article_ids.txt")
            with open(filename, "r", encoding="utf-8") as f:
                for line in f:
                    id_ = int(line.strip())
                    SPLITS[id_] = split

        ALL_PROMPTS = {}
        prompts_filename = os.path.join(dl_dir, "prompts_merged.csv")
        with open(prompts_filename, "r", encoding="utf-8") as f:
            data = csv.DictReader(f)
            for item in data:
                prompt_id = int(item["PromptID"])
                ALL_PROMPTS[prompt_id] = {"Prompt": item, "Annotations": []}

        annotations_filename = os.path.join(dl_dir, "annotations_merged.csv")
        with open(annotations_filename, "r", encoding="utf-8") as f:
            data = csv.DictReader(f)
            for item in data:
                prompt_id = int(item["PromptID"])

                if "Annotations" not in ALL_PROMPTS[prompt_id]:
                    ALL_PROMPTS[prompt_id]["Annotations"] = []

                ALL_PROMPTS[prompt_id]["Annotations"].append(item)

        # Simplify everything
        directory = os.path.join(dl_dir, "txt_files")
        ALL_IDS = {"train": [], "test": [], "validation": []}
        for prompt_id, item in ALL_PROMPTS.items():
            pmcid = int(item["Prompt"]["PMCID"])
            if pmcid not in SPLITS:
                if os.path.isfile(os.path.join(directory, f"PMC{pmcid}.txt")):
                    split = "train"
                else:
                    continue
            else:
                split = SPLITS[pmcid]

            values = ALL_IDS[split]

            filtered = [v for v in values if v["PMCID"] == pmcid]
            if len(filtered) == 1:
                value = filtered[0]
            else:
                value = {"PMCID": pmcid, "Prompts": []}
                values.append(value)

            new_item = item["Prompt"]
            new_item["Annotations"] = item["Annotations"]
            value["Prompts"].append(new_item)

        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "directory": os.path.join(dl_dir, "txt_files"),
                    "items": ALL_IDS["train"],
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "directory": directory,
                    "items": ALL_IDS["test"],
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "directory": os.path.join(dl_dir, "txt_files"),
                    "items": ALL_IDS["validation"],
                },
            ),
        ]

    def _generate_examples(self, directory, items):
        """ Yields examples. """
        for id_, item in enumerate(items):
            pmcid = item["PMCID"]
            filename = os.path.join(directory, f"PMC{pmcid}.txt")
            with open(filename, "r", encoding="utf-8") as f:
                text = f.read()

            yield id_, {"Text": text, **item}
