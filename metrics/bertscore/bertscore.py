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
""" BERTScore metric. """

import bert_score

import datasets


_CITATION = """\
@inproceedings{bert-score,
  title={BERTScore: Evaluating Text Generation with BERT},
  author={Tianyi Zhang* and Varsha Kishore* and Felix Wu* and Kilian Q. Weinberger and Yoav Artzi},
  booktitle={International Conference on Learning Representations},
  year={2020},
  url={https://openreview.net/forum?id=SkeHuCVFDr}
}
"""

_DESCRIPTION = """\
BERTScore leverages the pre-trained contextual embeddings from BERT and matches words in candidate and reference
sentences by cosine similarity.
It has been shown to correlate with human judgment on sentence-level and system-level evaluation.
Moreover, BERTScore computes precision, recall, and F1 measure, which can be useful for evaluating different language
generation tasks.

See the `README.md` file at [https://github.com/Tiiiger/bert_score](https://github.com/Tiiiger/bert_score) for more
information.
"""

_KWARGS_DESCRIPTION = """
BERTScore Metrics with the hashcode from a source against one or more references.

Args:
    predictions (list of str): Prediction/candidate sentences.
    references (list of str or list of list of str): Reference sentences.
    lang (str): Language of the sentences; required (e.g. 'en').
    model_type (str): Bert specification, default using the suggested
        model for the target language; has to specify at least one of
        `model_type` or `lang`.
    num_layers (int): The layer of representation to use,
        default using the number of layers tuned on WMT16 correlation data.
    verbose (bool): Turn on intermediate status update.
    idf (bool or dict): Use idf weighting; can also be a precomputed idf_dict.
    device (str): On which the contextual embedding model will be allocated on.
        If this argument is None, the model lives on cuda:0 if cuda is available.
    nthreads (int): Number of threads.
    batch_size (int): Bert score processing batch size,
        at least one of `model_type` or `lang`. `lang` needs to be
        specified when `rescale_with_baseline` is True.
    rescale_with_baseline (bool): Rescale bertscore with pre-computed baseline.
    baseline_path (str): Customized baseline file.

Returns:
    precision: Precision.
    recall: Recall.
    f1: F1 score.
    hashcode: Hashcode of the library.

Examples:

    >>> predictions = ["hello there", "general kenobi"]
    >>> references = ["hello there", "general kenobi"]
    >>> bertscore = datasets.load_metric("bertscore")
    >>> results = bertscore.compute(predictions=predictions, references=references, lang="en")
    >>> print([round(v, 2) for v in results["f1"]])
    [1.0, 1.0]
"""


@datasets.utils.file_utils.add_start_docstrings(_DESCRIPTION, _KWARGS_DESCRIPTION)
class BERTScore(datasets.Metric):
    def _info(self):
        return datasets.MetricInfo(
            description=_DESCRIPTION,
            citation=_CITATION,
            homepage="https://github.com/Tiiiger/bert_score",
            inputs_description=_KWARGS_DESCRIPTION,
            features=datasets.Features(
                {
                    "predictions": datasets.Value("string", id="sequence"),
                    "references": datasets.Sequence(datasets.Value("string", id="sequence"), id="references"),
                }
            ),
            codebase_urls=["https://github.com/Tiiiger/bert_score"],
            reference_urls=[
                "https://github.com/Tiiiger/bert_score",
                "https://arxiv.org/abs/1904.09675",
            ],
        )

    def _compute(
        self,
        predictions,
        references,
        lang=None,
        model_type=None,
        num_layers=None,
        verbose=False,
        idf=False,
        device=None,
        batch_size=64,
        nthreads=4,
        all_layers=False,
        rescale_with_baseline=False,
        baseline_path=None,
    ):
        if model_type is None:
            assert lang is not None, "either lang or model_type should be specified"
            model_type = bert_score.utils.lang2model[lang.lower()]

        if num_layers is None:
            num_layers = bert_score.utils.model2layers[model_type]

        hashcode = bert_score.utils.get_hash(
            model=model_type,
            num_layers=num_layers,
            idf=idf,
            rescale_with_baseline=rescale_with_baseline,
            use_custom_baseline=baseline_path is not None,
        )

        if not hasattr(self, "cached_bertscorer") or self.cached_bertscorer.hash != hashcode:
            self.cached_bertscorer = bert_score.BERTScorer(
                model_type=model_type,
                num_layers=num_layers,
                batch_size=batch_size,
                nthreads=nthreads,
                all_layers=all_layers,
                idf=idf,
                device=device,
                lang=lang,
                rescale_with_baseline=rescale_with_baseline,
                baseline_path=baseline_path,
            )

        (P, R, F) = self.cached_bertscorer.score(
            cands=predictions,
            refs=references,
            verbose=verbose,
            batch_size=batch_size,
        )
        output_dict = {
            "precision": P.tolist(),
            "recall": R.tolist(),
            "f1": F.tolist(),
            "hashcode": hashcode,
        }
        return output_dict

    def add_batch(self, predictions=None, references=None, **kwargs):
        """Add a batch of predictions and references for the metric's stack."""
        # References can be strings or lists of strings
        # Let's change strings to lists of strings with one element
        if references is not None:
            references = [[ref] if isinstance(ref, str) else ref for ref in references]
        super().add_batch(predictions=predictions, references=references, **kwargs)

    def add(self, prediction=None, reference=None, **kwargs):
        """Add one prediction and reference for the metric's stack."""
        # References can be strings or lists of strings
        # Let's change strings to lists of strings with one element
        if isinstance(reference, str):
            reference = [reference]
        super().add(prediction=prediction, reference=reference, **kwargs)
