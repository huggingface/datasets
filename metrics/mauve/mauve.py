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
""" MAUVE metric from https://github.com/krishnap25/mauve. """

import faiss  # Here to have a nice missing dependency error message early on
import numpy  # Here to have a nice missing dependency error message early on
import requests  # Here to have a nice missing dependency error message early on
import sklearn  # Here to have a nice missing dependency error message early on
import tqdm  # Here to have a nice missing dependency error message early on
from mauve import compute_mauve  # From: mauve-text

import datasets


_CITATION = """\
@inproceedings{pillutla-etal:mauve:neurips2021,
  title={MAUVE: Measuring the Gap Between Neural Text and Human Text using Divergence Frontiers},
  author={Pillutla, Krishna and Swayamdipta, Swabha and Zellers, Rowan and Thickstun, John and Welleck, Sean and Choi, Yejin and Harchaoui, Zaid},
  booktitle = {NeurIPS},
  year      = {2021}
}

"""

_DESCRIPTION = """\
MAUVE is a library built on PyTorch and HuggingFace Transformers to measure the gap between neural text and human text with the eponymous MAUVE measure.

MAUVE summarizes both Type I and Type II errors measured softly using Kullback–Leibler (KL) divergences.

For details, see the MAUVE paper: https://arxiv.org/abs/2102.01454 (Neurips, 2021).

This metrics is a wrapper around the official implementation of MAUVE:
https://github.com/krishnap25/mauve
"""

_KWARGS_DESCRIPTION = """
Calculates MAUVE scores between two lists of generated text and reference text.
Args:
    predictions: list of generated text to score. Each predictions
        should be a string with tokens separated by spaces.
    references: list of reference for each prediction. Each
        reference should be a string with tokens separated by spaces.
Optional Args:
    num_buckets: the size of the histogram to quantize P and Q. Options: 'auto' (default) or an integer
    pca_max_data: the number data points to use for PCA dimensionality reduction prior to clustering. If -1, use all the data. Default -1
    kmeans_explained_var: amount of variance of the data to keep in dimensionality reduction by PCA. Default 0.9
    kmeans_num_redo: number of times to redo k-means clustering (the best objective is kept). Default 5
    kmeans_max_iter: maximum number of k-means iterations. Default 500
    featurize_model_name: name of the model from which features are obtained. Default 'gpt2-large' Use one of ['gpt2', 'gpt2-medium', 'gpt2-large', 'gpt2-xl'].
    device_id: Device for featurization. Supply a GPU id (e.g. 0 or 3) to use GPU. If no GPU with this id is found, use CPU
    max_text_length: maximum number of tokens to consider. Default 1024
    divergence_curve_discretization_size: Number of points to consider on the divergence curve. Default 25
    mauve_scaling_factor: "c" from the paper. Default 5.
    verbose: If True (default), print running time updates
    seed: random seed to initialize k-means cluster assignments.
Returns:
    mauve: MAUVE score, a number between 0 and 1. Larger values indicate that P and Q are closer,
    frontier_integral: Frontier Integral, a number between 0 and 1. Smaller values indicate that P and Q are closer,
    divergence_curve: a numpy.ndarray of shape (m, 2); plot it with matplotlib to view the divergence curve,
    p_hist: a discrete distribution, which is a quantized version of the text distribution p_text,
    q_hist: same as above, but with q_text.
Examples:

    >>> # faiss segfaults in doctest for some reason, so the .compute call is not tested with doctest
    >>> import datasets
    >>> mauve = datasets.load_metric('mauve')
    >>> predictions = ["hello there", "general kenobi"]
    >>> references = ["hello there", "general kenobi"]
    >>> out = mauve.compute(predictions=predictions, references=references) # doctest: +SKIP
    >>> print(out.mauve) # doctest: +SKIP
    1.0
"""


@datasets.utils.file_utils.add_start_docstrings(_DESCRIPTION, _KWARGS_DESCRIPTION)
class Mauve(datasets.Metric):
    def _info(self):
        return datasets.MetricInfo(
            description=_DESCRIPTION,
            citation=_CITATION,
            homepage="https://github.com/krishnap25/mauve",
            inputs_description=_KWARGS_DESCRIPTION,
            features=datasets.Features(
                {
                    "predictions": datasets.Value("string", id="sequence"),
                    "references": datasets.Value("string", id="sequence"),
                }
            ),
            codebase_urls=["https://github.com/krishnap25/mauve"],
            reference_urls=[
                "https://arxiv.org/abs/2102.01454",
                "https://github.com/krishnap25/mauve",
            ],
        )

    def _compute(
        self,
        predictions,
        references,
        p_features=None,
        q_features=None,
        p_tokens=None,
        q_tokens=None,
        num_buckets="auto",
        pca_max_data=-1,
        kmeans_explained_var=0.9,
        kmeans_num_redo=5,
        kmeans_max_iter=500,
        featurize_model_name="gpt2-large",
        device_id=-1,
        max_text_length=1024,
        divergence_curve_discretization_size=25,
        mauve_scaling_factor=5,
        verbose=True,
        seed=25,
    ):
        out = compute_mauve(
            p_text=predictions,
            q_text=references,
            p_features=p_features,
            q_features=q_features,
            p_tokens=p_tokens,
            q_tokens=q_tokens,
            num_buckets=num_buckets,
            pca_max_data=pca_max_data,
            kmeans_explained_var=kmeans_explained_var,
            kmeans_num_redo=kmeans_num_redo,
            kmeans_max_iter=kmeans_max_iter,
            featurize_model_name=featurize_model_name,
            device_id=device_id,
            max_text_length=max_text_length,
            divergence_curve_discretization_size=divergence_curve_discretization_size,
            mauve_scaling_factor=mauve_scaling_factor,
            verbose=verbose,
            seed=seed,
        )
        return out
