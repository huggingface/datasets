# Copyright 2021 The HuggingFace Datasets Authors and the current dataset script contributor.
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
"""Pearson correlation coefficient metric."""

from scipy.stats import pearsonr

import datasets


_DESCRIPTION = """
Pearson correlation coefficient and p-value for testing non-correlation.
The Pearson correlation coefficient measures the linear relationship between two datasets. The calculation of the p-value relies on the assumption that each dataset is normally distributed. Like other correlation coefficients, this one varies between -1 and +1 with 0 implying no correlation. Correlations of -1 or +1 imply an exact linear relationship. Positive correlations imply that as x increases, so does y. Negative correlations imply that as x increases, y decreases.
The p-value roughly indicates the probability of an uncorrelated system producing datasets that have a Pearson correlation at least as extreme as the one computed from these datasets.
"""


_KWARGS_DESCRIPTION = """
Args:
    predictions (`list` of `int`): Predicted class labels, as returned by a model.
    references (`list` of `int`): Ground truth labels.
    return_pvalue (`boolean`): If `True`, returns the p-value, along with the correlation coefficient. If `False`, returns only the correlation coefficient. Defaults to `False`.

Returns:
    pearsonr (`float`): Pearson correlation coefficient. Minimum possible value is -1. Maximum possible value is 1. Values of 1 and -1 indicate exact linear positive and negative relationships, respectively. A value of 0 implies no correlation.
    p-value (`float`): P-value, which roughly indicates the probability of an The p-value roughly indicates the probability of an uncorrelated system producing datasets that have a Pearson correlation at least as extreme as the one computed from these datasets. Minimum possible value is 0. Maximum possible value is 1. Higher values indicate higher probabilities.

Examples:

    Example 1-A simple example using only predictions and references.
        >>> pearsonr_metric = datasets.load_metric("pearsonr")
        >>> results = pearsonr_metric.compute(predictions=[10, 9, 2.5, 6, 4], references=[1, 2, 3, 4, 5])
        >>> print(round(results['pearsonr'], 2))
        -0.74

    Example 2-The same as Example 1, but that also returns the `p-value`.
        >>> pearsonr_metric = datasets.load_metric("pearsonr")
        >>> results = pearsonr_metric.compute(predictions=[10, 9, 2.5, 6, 4], references=[1, 2, 3, 4, 5], return_pvalue=True)
        >>> print(sorted(list(results.keys())))
        ['p-value', 'pearsonr']
        >>> print(round(results['pearsonr'], 2))
        -0.74
        >>> print(round(results['p-value'], 2))
        0.15
"""


_CITATION = """
@article{2020SciPy-NMeth,
author  = {Virtanen, Pauli and Gommers, Ralf and Oliphant, Travis E. and
      Haberland, Matt and Reddy, Tyler and Cournapeau, David and
      Burovski, Evgeni and Peterson, Pearu and Weckesser, Warren and
      Bright, Jonathan and {van der Walt}, St{\'e}fan J. and
      Brett, Matthew and Wilson, Joshua and Millman, K. Jarrod and
      Mayorov, Nikolay and Nelson, Andrew R. J. and Jones, Eric and
      Kern, Robert and Larson, Eric and Carey, C J and
      Polat, Ilhan and Feng, Yu and Moore, Eric W. and
      {VanderPlas}, Jake and Laxalde, Denis and Perktold, Josef and
      Cimrman, Robert and Henriksen, Ian and Quintero, E. A. and
      Harris, Charles R. and Archibald, Anne M. and
      Ribeiro, Antonio H. and Pedregosa, Fabian and
      {van Mulbregt}, Paul and {SciPy 1.0 Contributors}},
title   = {{{SciPy} 1.0: Fundamental Algorithms for Scientific
      Computing in Python}},
journal = {Nature Methods},
year    = {2020},
volume  = {17},
pages   = {261--272},
adsurl  = {https://rdcu.be/b08Wh},
doi = {10.1038/s41592-019-0686-2},
}
"""


@datasets.utils.file_utils.add_start_docstrings(_DESCRIPTION, _KWARGS_DESCRIPTION)
class Pearsonr(datasets.Metric):
    def _info(self):
        return datasets.MetricInfo(
            description=_DESCRIPTION,
            citation=_CITATION,
            inputs_description=_KWARGS_DESCRIPTION,
            features=datasets.Features(
                {
                    "predictions": datasets.Value("float"),
                    "references": datasets.Value("float"),
                }
            ),
            reference_urls=["https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.pearsonr.html"],
        )

    def _compute(self, predictions, references, return_pvalue=False):
        if return_pvalue:
            results = pearsonr(references, predictions)
            return {"pearsonr": results[0], "p-value": results[1]}
        else:
            return {"pearsonr": float(pearsonr(references, predictions)[0])}
