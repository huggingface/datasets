# coding=utf-8
# Copyright 2020 The HuggingFace Datasets Authors.
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
""" BLEURT metric. """

import os

from bleurt import score  # From: git+https://github.com/google-research/bleurt.git

import datasets


logger = datasets.logging.get_logger(__name__)


_CITATION = """\
@inproceedings{bleurt,
  title={BLEURT: Learning Robust Metrics for Text Generation},
  author={Thibault Sellam and Dipanjan Das and Ankur P. Parikh},
  booktitle={ACL},
  year={2020},
  url={https://arxiv.org/abs/2004.04696}
}
"""

_DESCRIPTION = """\
BLEURT a learnt evaluation metric for Natural Language Generation. It is built using multiple phases of transfer learning starting from a pretrained BERT model (Devlin et al. 2018)
and then employing another pre-training phrase using synthetic data. Finally it is trained on WMT human annotations. You may run BLEURT out-of-the-box or fine-tune
it for your specific application (the latter is expected to perform better).

See the [README.md] file at https://github.com/google-research/bleurt for more information.
"""

_KWARGS_DESCRIPTION = """
BLEURT score.

Args:
    `predictions` (list of str): prediction/candidate sentences
    `references` (list of str): reference sentences
    `checkpoint` BLEURT checkpoint. Will default to BLEURT-tiny if None.

Returns:
    'scores': List of scores.
Examples:

    >>> predictions = ["hello there", "general kenobi"]
    >>> references = ["hello there", "general kenobi"]
    >>> bleurt = datasets.load_metric("bleurt")
    >>> results = bleurt.compute(predictions=predictions, references=references)
    >>> print([round(v, 2) for v in results["scores"]])
    [1.03, 1.04]
"""

CHECKPOINT_URLS = {
    "bleurt-tiny-128": "https://storage.googleapis.com/bleurt-oss/bleurt-tiny-128.zip",
    "bleurt-tiny-512": "https://storage.googleapis.com/bleurt-oss/bleurt-tiny-512.zip",
    "bleurt-base-128": "https://storage.googleapis.com/bleurt-oss/bleurt-base-128.zip",
    "bleurt-base-512": "https://storage.googleapis.com/bleurt-oss/bleurt-base-512.zip",
    "bleurt-large-128": "https://storage.googleapis.com/bleurt-oss/bleurt-large-128.zip",
    "bleurt-large-512": "https://storage.googleapis.com/bleurt-oss/bleurt-large-512.zip",
    "bleurt-20-d3": "https://storage.googleapis.com/bleurt-oss-21/BLEURT-20-D3.zip",
    "bleurt-20-d6": "https://storage.googleapis.com/bleurt-oss-21/BLEURT-20-D6.zip",
    "bleurt-20-d12": "https://storage.googleapis.com/bleurt-oss-21/BLEURT-20-D12.zip",
    "bleurt-20": "https://storage.googleapis.com/bleurt-oss-21/BLEURT-20.zip",
}


@datasets.utils.file_utils.add_start_docstrings(_DESCRIPTION, _KWARGS_DESCRIPTION)
class BLEURT(datasets.Metric):
    def _info(self):

        return datasets.MetricInfo(
            description=_DESCRIPTION,
            citation=_CITATION,
            homepage="https://github.com/google-research/bleurt",
            inputs_description=_KWARGS_DESCRIPTION,
            features=datasets.Features(
                {
                    "predictions": datasets.Value("string", id="sequence"),
                    "references": datasets.Value("string", id="sequence"),
                }
            ),
            codebase_urls=["https://github.com/google-research/bleurt"],
            reference_urls=["https://github.com/google-research/bleurt", "https://arxiv.org/abs/2004.04696"],
        )

    def _download_and_prepare(self, dl_manager):

        # check that config name specifies a valid BLEURT model
        if self.config_name == "default":
            logger.warning(
                "Using default BLEURT-Base checkpoint for sequence maximum length 128. "
                "You can use a bigger model for better results with e.g.: datasets.load_metric('bleurt', 'bleurt-large-512')."
            )
            self.config_name = "bleurt-base-128"
        if self.config_name not in CHECKPOINT_URLS.keys():
            raise KeyError(
                f"{self.config_name} model not found. You should supply the name of a model checkpoint for bleurt in {CHECKPOINT_URLS.keys()}"
            )

        # download the model checkpoint specified by self.config_name and set up the scorer
        model_path = dl_manager.download_and_extract(CHECKPOINT_URLS[self.config_name])
        self.scorer = score.BleurtScorer(os.path.join(model_path, self.config_name))

    def _compute(self, predictions, references):
        scores = self.scorer.score(references=references, candidates=predictions)
        return {"scores": scores}
