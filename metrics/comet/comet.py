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
""" COMET metric.

Requirements:
pip install unbabel-comet

Usage:

```python
from datasets import load_metric
comet_metric = load_metric('metrics/comet/comet.py')
#comet_metric = load_metric('comet')
#comet_metric = load_metric('comet', 'wmt-large-hter-estimator')


source = ["Dem Feuer konnte Einhalt geboten werden", "Schulen und Kindergärten wurden eröffnet."]
hypothesis = ["The fire could be stopped", "Schools and kindergartens were open"]
reference = ["They were able to control the fire.", "Schools and kindergartens opened"]

predictions = comet_metric.compute(predictions=hypothesis, references=reference, sources=source)
predictions['scores']
```
"""

from comet.models import download_model  # From: unbabel-comet

import datasets


logger = datasets.logging.get_logger(__name__)

_CITATION = """\
@inproceedings{rei-EtAl:2020:WMT,
   author    = {Rei, Ricardo  and  Stewart, Craig  and  Farinha, Ana C  and  Lavie, Alon},
   title     = {Unbabel's Participation in the WMT20 Metrics Shared Task},
   booktitle      = {Proceedings of the Fifth Conference on Machine Translation},
   month          = {November},
   year           = {2020},
   address        = {Online},
   publisher      = {Association for Computational Linguistics},
   pages     = {909--918},
}
@inproceedings{rei-etal-2020-comet,
   title = "{COMET}: A Neural Framework for {MT} Evaluation",
   author = "Rei, Ricardo  and
      Stewart, Craig  and
      Farinha, Ana C  and
      Lavie, Alon",
   booktitle = "Proceedings of the 2020 Conference on Empirical Methods in Natural Language Processing (EMNLP)",
   month = nov,
   year = "2020",
   address = "Online",
   publisher = "Association for Computational Linguistics",
   url = "https://www.aclweb.org/anthology/2020.emnlp-main.213",
   pages = "2685--2702",
}
"""

_DESCRIPTION = """\
Crosslingual Optimized Metric for Evaluation of Translation (COMET) is an open-source framework used to train Machine Translation metrics that achieve high levels of correlation with different types of human judgments (HTER, DA's or MQM).
With the release of the framework the authors also released fully trained models that were used to compete in the WMT20 Metrics Shared Task achieving SOTA in that years competition.

See the [README.md] file at https://unbabel.github.io/COMET/html/models.html for more information.
"""

_KWARGS_DESCRIPTION = """
COMET score.

Args:

`sources` (list of str): Source sentences
`predictions` (list of str): candidate translations
`references` (list of str): reference translations
`cuda` (bool): If set to True, runs COMET using GPU
`show_progress` (bool): Shows progress
`model`: COMET model to be used. Will default to `wmt-large-da-estimator-1719` if None.

Returns:
    `samples`: List of dictionaries with `src`, `mt`, `ref` and `score`.
    `scores`: List of scores.

Examples:

    >>> comet_metric = datasets.load_metric('comet') # doctest:+ELLIPSIS
    [...]Download succeeded. Loading model[...]
    >>> # comet_metric = load_metric('comet', 'wmt-large-hter-estimator')  # you can also choose which model to use
    >>> source = ["Dem Feuer konnte Einhalt geboten werden", "Schulen und Kindergärten wurden eröffnet."]
    >>> hypothesis = ["The fire could be stopped", "Schools and kindergartens were open"]
    >>> reference = ["They were able to control the fire.", "Schools and kindergartens opened"]
    >>> results = comet_metric.compute(predictions=hypothesis, references=reference, sources=source)
    >>> print([round(v, 2) for v in results["scores"]])
    [0.19, 0.92]
"""


@datasets.utils.file_utils.add_start_docstrings(_DESCRIPTION, _KWARGS_DESCRIPTION)
class COMET(datasets.Metric):
    def _info(self):

        return datasets.MetricInfo(
            description=_DESCRIPTION,
            citation=_CITATION,
            homepage="https://unbabel.github.io/COMET/html/index.html",
            inputs_description=_KWARGS_DESCRIPTION,
            features=datasets.Features(
                {
                    "predictions": datasets.Value("string", id="sequence"),
                    "references": datasets.Value("string", id="sequence"),
                }
            ),
            codebase_urls=["hhttps://github.com/Unbabel/COMET"],
            reference_urls=[
                "https://github.com/Unbabel/COMET",
                "https://www.aclweb.org/anthology/2020.emnlp-main.213/",
                "http://www.statmt.org/wmt20/pdf/2020.wmt-1.101.pdf6",
            ],
        )

    def _download_and_prepare(self, dl_manager):
        if self.config_name == "default":
            self.scorer = download_model("wmt-large-da-estimator-1719")
        else:
            self.scorer = download_model(self.config_name)

    def _compute(self, sources, predictions, references, cuda=True, show_progress=False):
        data = {"src": sources, "mt": predictions, "ref": references}
        data = [dict(zip(data, t)) for t in zip(*data.values())]
        samples, scores = self.scorer.predict(data, cuda=cuda, show_progress=show_progress)
        return {"scores": scores, "samples": samples}
