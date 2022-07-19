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
"""Spearman correlation coefficient metric."""

from scipy.stats import spearmanr

import datasets


_DESCRIPTION = """
The Spearman rank-order correlation coefficient is a measure of the
relationship between two datasets. Like other correlation coefficients,
this one varies between -1 and +1 with 0 implying no correlation.
Positive correlations imply that as data in dataset x increases, so
does data in dataset y. Negative correlations imply that as x increases,
y decreases. Correlations of -1 or +1 imply an exact monotonic relationship.

Unlike the Pearson correlation, the Spearman correlation does not
assume that both datasets are normally distributed.

The p-value roughly indicates the probability of an uncorrelated system
producing datasets that have a Spearman correlation at least as extreme
as the one computed from these datasets. The p-values are not entirely
reliable but are probably reasonable for datasets larger than 500 or so.
"""

_KWARGS_DESCRIPTION = """
Args:
    predictions (`List[float]`): Predicted labels, as returned by a model.
    references (`List[float]`): Ground truth labels.
    return_pvalue (`bool`): If `True`, returns the p-value. If `False`, returns
            only the spearmanr score. Defaults to `False`.
Returns:
    spearmanr (`float`): Spearman correlation coefficient.
    p-value (`float`): p-value. **Note**: is only returned if `return_pvalue=True` is input.
Examples:
    Example 1:
        >>> spearmanr_metric = datasets.load_metric("spearmanr")
        >>> results = spearmanr_metric.compute(references=[1, 2, 3, 4, 5], predictions=[10, 9, 2.5, 6, 4])
        >>> print(results)
        {'spearmanr': -0.7}

    Example 2:
        >>> spearmanr_metric = datasets.load_metric("spearmanr")
        >>> results = spearmanr_metric.compute(references=[1, 2, 3, 4, 5],
        ...                                     predictions=[10, 9, 2.5, 6, 4],
        ...                                     return_pvalue=True)
        >>> print(results['spearmanr'])
        -0.7
        >>> print(round(results['spearmanr_pvalue'], 2))
        0.19
"""

_CITATION = r"""\
@book{kokoska2000crc,
  title={CRC standard probability and statistics tables and formulae},
  author={Kokoska, Stephen and Zwillinger, Daniel},
  year={2000},
  publisher={Crc Press}
}
@article{2020SciPy-NMeth,
  author  = {Virtanen, Pauli and Gommers, Ralf and Oliphant, Travis E. and
            Haberland, Matt and Reddy, Tyler and Cournapeau, David and
            Burovski, Evgeni and Peterson, Pearu and Weckesser, Warren and
            Bright, Jonathan and {van der Walt}, St{\'e}fan J. and
            Brett, Matthew and Wilson, Joshua and Millman, K. Jarrod and
            Mayorov, Nikolay and Nelson, Andrew R. J. and Jones, Eric and
            Kern, Robert and Larson, Eric and Carey, C J and
            Polat, {\.I}lhan and Feng, Yu and Moore, Eric W. and
            {VanderPlas}, Jake and Laxalde, Denis and Perktold, Josef and
            Cimrman, Robert and Henriksen, Ian and Quintero, E. A. and
            Harris, Charles R. and Archibald, Anne M. and
            Ribeiro, Ant{\^o}nio H. and Pedregosa, Fabian and
            {van Mulbregt}, Paul and {SciPy 1.0 Contributors}},
  title   = {{{SciPy} 1.0: Fundamental Algorithms for Scientific
            Computing in Python}},
  journal = {Nature Methods},
  year    = {2020},
  volume  = {17},
  pages   = {261--272},
  adsurl  = {https://rdcu.be/b08Wh},
  doi     = {10.1038/s41592-019-0686-2},
}
"""


@datasets.utils.file_utils.add_start_docstrings(_DESCRIPTION, _KWARGS_DESCRIPTION)
class Spearmanr(datasets.Metric):
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
            reference_urls=["https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.spearmanr.html"],
        )

    def _compute(self, predictions, references, return_pvalue=False):
        results = spearmanr(references, predictions)
        if return_pvalue:
            return {"spearmanr": results[0], "spearmanr_pvalue": results[1]}
        else:
            return {"spearmanr": results[0]}
