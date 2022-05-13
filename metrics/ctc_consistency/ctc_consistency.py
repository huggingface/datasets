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
""" CTC-Consistency metric. """

import datasets
import ctc_score
from ctc_score import SummarizationScorer


_CITATION = """\
@article{deng2021compression,
  title={Compression, Transduction, and Creation: A Unified Framework for Evaluating Natural Language Generation},
  author={Deng, Mingkai and Tan, Bowen and Liu, Zhengzhong and Xing, Eric P and Hu, Zhiting},
  journal={arXiv preprint arXiv:2109.06379},
  year={2021}
}
"""

_DESCRIPTION = """\
    We adopt the prevailing definition of consistency (Cao et al., 2018; Kryscinski et al., 2019), which dictates that the summary y should only contain information from x (instead of other sources or hallucinations). The aspect is also referred to as “factual correctness” or “faithfulness” in previous work2. For y to be fully consistent, all tokens in y should align with x. Therefore, we can straightforwardly devise the consistency metric based on the information alignment defined above:
    CONSISTENCY(y, x) = mean (align(y → x)), which is the average alignment scores of tokens in y w.r.t. x. Our metric offers a simpler solution than the recent QA-based metrics (Scialom et al., 2019; Durmus et al., 2020; Wang et al., 2020) that compare the answers extracted from y and x by a Question-Answering system, and is more interpretable than the black-box consistency classification models (Falke et al., 2019; Krys ́cin ́ski et al., 2019; Maynez et al., 2020).

"""

_KWARGS_DESCRIPTION = """
Computes CTC consistency score of translated segments against one or more references.
Args:
    sources: list of all document texts (line-by-line)
    hypothesis: list of all hypothesized texts to evaluate (line-by-line)
Returns:
    'scores: ctc-consistency score,
Examples:
    >>> sources = [
    ...     "(CNN)Donald Sterling's racist remarks cost him an NBA team last year. But now it's his former female companion who has lost big. A Los Angeles judge has ordered V. Stiviano to pay back more than $2.6 million in gifts after Sterling's wife sued her. In the lawsuit, Rochelle \"Shelly\" Sterling accused Stiviano of targeting extremely wealthy older men. She claimed Donald Sterling used the couple's money to buy Stiviano a Ferrari, two Bentleys and a Range Rover, and that he helped her get a $1.8 million duplex. Who is V. Stiviano? Stiviano countered that there was nothing wrong with Donald Sterling giving her gifts and that she never took advantage of the former Los Angeles Clippers owner, who made much of his fortune in real estate. Shelly Sterling was thrilled with the court decision Tuesday, her lawyer told CNN affiliate KABC. \"This is a victory for the Sterling family in recovering the $2,630,000 that Donald lavished on a conniving mistress,\" attorney Pierce O'Donnell said in a statement. \"It also sets a precedent that the injured spouse can recover damages from the recipient of these ill-begotten gifts.\" Stiviano's gifts from Donald Sterling didn't just include uber-expensive items like luxury cars. According to the Los Angeles Times, the list also includes a $391 Easter bunny costume, a $299 two-speed blender and a $12 lace thong. Donald Sterling's downfall came after an audio recording surfaced of the octogenarian arguing with Stiviano. In the tape, Sterling chastises Stiviano for posting pictures on social media of her posing with African-Americans, including basketball legend Magic Johnson. \"In your lousy f**ing Instagrams, you don't have to have yourself with -- walking with black people,\" Sterling said in the audio first posted by TMZ. He also tells Stiviano not to bring Johnson to Clippers games and not to post photos with the Hall of Famer so Sterling's friends can see. \"Admire him, bring him here, feed him, f**k him, but don't put (Magic) on an Instagram for the world to have to see so they have to call me,\" Sterling said. NBA Commissioner Adam Silver banned Sterling from the league, fined him $2.5 million and pushed through a charge to terminate all of his ownership rights in the franchise. Fact check: Donald Sterling's claims vs. reality CNN's Dottie Evans contributed to this report."            # tokenized prediction of the sample
    ... ]
    >>> hypothesis = [
    ...     "-lrb- cnn -rrb- donald sterling 's racist remarks cost him an nba team last year . but now it 's his former female companion who has lost big . a los angeles judge has ordered v. stiviano to pay back more than $ 2.6 million in gifts after sterling 's wife sued her ."  # tokenized references for the sample
    ... ]
    >>> ctc_consistency = datasets.load_metric("CTC_Consistency")
    >>> results = ctc_consistency.compute(sources=sources, hypothesis=hypothesis)
    >>> print(results["scores"])
    0.9349850675401589
"""


@datasets.utils.file_utils.add_start_docstrings(_DESCRIPTION, _KWARGS_DESCRIPTION)
class CTC_Consistency(datasets.Metric):
    def _info(self):
        return datasets.MetricInfo(
            description=_DESCRIPTION,
            citation=_CITATION,
            inputs_description=_KWARGS_DESCRIPTION,
            features=datasets.Features(
                {
                    "sources": datasets.Value("string", id="sequence"),
                    "hypothesis": datasets.Value("string", id="sequence"),
                }
            ),
            codebase_urls=["https://github.com/tanyuqian/ctc-gen-eval/blob/master/ctc_score/summarization_scorer.py"],
            reference_urls=[
                "https://github.com/tanyuqian/ctc-gen-eval",
            ],
        )

    def _compute(self, sources, hypothesis):
        scorer = SummarizationScorer(align='D-cnndm')
        scores = []
        for src_s, hyp_s in zip(sources, hypothesis):
            scores.append(scorer.score(doc=src_s, refs=[], hypo=hyp_s, aspect='consistency'))
        return {"scores": scores}
