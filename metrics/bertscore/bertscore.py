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
""" BERTScore metric. """

import nlp
import bert_score

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
BERTScore leverages the pre-trained contextual embeddings from BERT and matches words in candidate and reference sentences by cosine similarity.
It has been shown to correlate with human judgment on sentence-level and system-level evaluation. 
Moreover, BERTScore computes precision, recall, and F1 measure, which can be useful for evaluating different language generation tasks.

See the [README.md] file at https://github.com/Tiiiger/bert_score for more information.
"""

_KWARGS_DESCRIPTION = """
BERTScore Metrics with the hashcode from a source against one or more references.

Args:
    `predictions` (list of str): prediction/candidate sentences
    `refereces` (list of str or list of list of str): reference sentences
    `lang` (str): language of the sentences; required (e.g. 'en')
    `model_type` (str): bert specification, default using the suggested
    model for the target langauge; has to specify at least one of
    `model_type` or `lang`
    `num_layers` (int): the layer of representation to use.
    default using the number of layer tuned on WMT16 correlation data
    `verbose` (bool): turn on intermediate status update
    `idf` (bool or dict): use idf weighting, can also be a precomputed idf_dict
    `device` (str): on which the contextual embedding model will be allocated on.
    If this argument is None, the model lives on cuda:0 if cuda is available.
    `nthreads` (int): number of threads
    `batch_size` (int): bert score processing batch size
    at least one of `model_type` or `lang`. `lang` needs to be
    specified when `rescale_with_baseline` is True.
    `rescale_with_baseline` (bool): rescale bertscore with pre-computed baseline
Returns:
    'precision': Precision,
    'recall': Recall,
    'f1', F1 score,
    'hashcode': Hashcode of the library,
"""

class BERTScore(nlp.Metric):
    def _info(self):
        return nlp.MetricInfo(
            description=_DESCRIPTION,
            citation=_CITATION,
            homepage="https://github.com/Tiiiger/bert_score",
            inputs_description=_KWARGS_DESCRIPTION,
            features=nlp.Features({
                'predictions': nlp.Value('string', id='sequence'),
                'references': nlp.Sequence(nlp.Value('string', id='sequence'), id='references'),
            }),
            codebase_urls=["https://github.com/Tiiiger/bert_score"],
            reference_urls=["https://github.com/Tiiiger/bert_score",
                            "https://arxiv.org/abs/1904.09675"]
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
    ):
        if model_type is None:
            assert lang is not None, "either lang or model_type should be specified"
            model_type = bert_score.utils.lang2model[lang.lower()]

        if num_layers is None:
            num_layers = bert_score.utils.model2layers[model_type]

        hashcode = bert_score.utils.get_hash(model_type, num_layers, idf, rescale_with_baseline)
        if not hasattr(self, 'cached_bertscorer') or self.cached_bertscorer.hash != hashcode:
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
            )

        (P, R, F) = self.cached_bertscorer.score(
            cands=predictions, refs=references, verbose=verbose, batch_size=batch_size,
        )
        output_dict = {
            'precision': P,
            'recall': R,
            'f1': F,
            'hashcode': hashcode,
        }
        return output_dict
