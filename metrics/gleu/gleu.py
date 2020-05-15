# coding=utf-8
# Copyright 2020 The HuggingFace NLP Authors.
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
""" GLEU metric. """

import random
import nlp
import scipy.stats
import numpy as np

from .gec_gleu import GLEU  # From: https://github.com/cnap/gec-ranking/blob/master/scripts/gleu.py

_CITATION = """\
@InProceedings{napoles-EtAl:2015:ACL-IJCNLP,
  author    = {Napoles, Courtney  and  Sakaguchi, Keisuke  and  Post, Matt  and  Tetreault, Joel},
  title     = {Ground Truth for Grammatical Error Correction Metrics},
  booktitle = {Proceedings of the 53rd Annual Meeting of the Association for Computational Linguistics and the 7th International Joint Conference on Natural Language Processing (Volume 2: Short Papers)},
  month     = {July},
  year      = {2015},
  address   = {Beijing, China},
  publisher = {Association for Computational Linguistics},
  pages     = {588--593},
  url       = {http://www.aclweb.org/anthology/P15-2097}
}
@Article{napoles2016gleu,
  author    = {Napoles, Courtney  and  Sakaguchi, Keisuke  and  Post, Matt  and  Tetreault, Joel},
  title     = {{GLEU} Without Tuning},
  journal   = {eprint arXiv:1605.02592 [cs.CL]},
  year      = {2016},
  url       = {http://arxiv.org/abs/1605.02592}
}
"""

_DESCRIPTION = """\
The GLEU metric is a variant of BLEU proposed for evaluating grammatical error corrections
using n-gram overlap with a set of reference sentences, as opposed to precision/recall of specific
annotated errors (Napoles et al., 2015). GLEU hews more closely to human judgments than the rankings produced by
metrics such as MaxMatch and I-measure. The present metric is the second version of GLEU (Napoles et al., 2016)
modified to address problems that arise when using an increasing number of reference sets.
The modified metric does not require tuning and is recommended to be used instead of the original version.
"""

_KWARGS_DESCRIPTION = """
Computes GLEU score.
Args:
    predictions: list of translations to score.
        Each translation should be tokenized into a list of tokens.
    references: list of lists of references for each translation.
        Each reference should be tokenized into a list of tokens.
    max_order: Maximum n-gram order to use when computing BLEU score.
    smooth: Whether or not to apply Lin et al. 2004 smoothing.
Returns:
    'bleu': bleu score,
    'precisions': geometric mean of n-gram precisions,
    'brevity_penalty': brevity penalty,
    'length_ratio': ratio of lengths,
    'translation_length': translation_length,
    'reference_length': reference_length
"""

def get_gleu_stats(scores) :
    mean = np.mean(scores)
    std = np.std(scores)
    ci = scipy.stats.norm.interval(0.95,loc=mean,scale=std)
    return {'mean': mean,
            'std': std,
            'ci': ci}

class Gleu(nlp.Metric):
    def __init__(self, **kwargs):
        raise NotImplementedError("Gleu is currently under construction.")

    def _info(self):
        return nlp.MetricInfo(
            description=_DESCRIPTION,
            citation=_CITATION,
            inputs_description=_KWARGS_DESCRIPTION,
            features=nlp.Features({
                'predictions': nlp.Sequence(nlp.Value('string', id='token'), id='sequence'),
                'references': nlp.Sequence(nlp.Sequence(nlp.Value('string', id='token'), id='sequence'), id='references'),
            }),
            codebase_urls=["https://github.com/cnap/gec-ranking"],
            reference_urls=["https://github.com/cnap/gec-ranking"]
        )

    def _compute(self, predictions, references, source, num_iterations=500, debug=False):
        raise NotImplementedError("To finish")
        gleu_calculator = GLEU()

        gleu_calculator.load_sources(source)
        gleu_calculator.load_references(references)

        # first generate a random list of indices, using a different seed
        # for each iteration
        indices = []
        for j in range(num_iterations) :
            random.seed(j*101)
            indices.append([random.randint(0,len(references)-1)
                            for i in range(len(predictions))])

        if debug :
            print('===== Sentence-level scores =====')
            print('SID Mean Stdev 95%CI GLEU')

        iter_stats = [ [0 for i in range(2*4+2)]
                        for j in range(num_iterations) ]

        for i,h in enumerate(predictions) :

            gleu_calculator.load_hypothesis_sentence(h)
            # we are going to store the score of this sentence for each ref
            # so we don't have to recalculate them 500 times

            stats_by_ref = [ None for r in range(len(references)) ]

            for j in range(num_iterations) :
                ref = indices[j][i]
                this_stats = stats_by_ref[ref]

                if this_stats is None :
                    this_stats = [ s for s in gleu_calculator.gleu_stats(
                        i,r_ind=ref) ]
                    stats_by_ref[ref] = this_stats

                iter_stats[j] = [ sum(scores)
                                    for scores in zip(iter_stats[j], this_stats)]

            if debug :
                # sentence-level GLEU is the mean GLEU of the hypothesis
                # compared to each reference
                for r in range(len(references)) :
                    if stats_by_ref[r] is None :
                        stats_by_ref[r] = [s for s in gleu_calculator.gleu_stats(
                            i,r_ind=r) ]

                print(i)
                print(' '.join(get_gleu_stats([gleu_calculator.gleu(stats,smooth=True)
                                                for stats in stats_by_ref])))

        if debug :
            print('\n==== Overall score =====')
            print('Mean Stdev 95%CI GLEU')
            print(' '.join(get_gleu_stats([gleu_calculator.gleu(stats)
                                            for stats in iter_stats ])))
        return get_gleu_stats([gleu_calculator.gleu(stats)
                                    for stats in iter_stats ])[0]
