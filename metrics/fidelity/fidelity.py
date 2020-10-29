import logging

import numpy as np
import torch

import datasets
import metrics.fidelity.utility as utility


logger = logging.getLogger(__name__)

_CITATION = """
@inproceedings{carton+rathore+tan:20,
	 author = {Samuel Carton and Anirudh Rathore and Chenhao Tan},
	 title = {Evaluating and Characterizing Human Rationales},
	 year = {2020},
	 booktitle = {Proceedings of EMNLP}
}
"""

_DESCRIPTION = """
This metric computes fidelity (Yu et al. 2019, DeYoung et al. 2019) and normalized fidelity (Carton et al. 2020).

Fidelity is a measure of rationale faithfulness, measuring whether the information contained in an extractive rationale
is sufficient or necessary (aka comprehensive) for the model to make similar predictions as it does with full
information. A good rationale should be highly sufficient, and optionally highly comprehensive depending on the specific
use case.

Normalization is an optional addition which adjusts fidelity scores to account for baseline model behavior.
This is helpful when comparing scores across different models and datasets. See (Carton et al. 2020) for further
details.

sufficiency(x, y_hat, alpha) = 1 - max(0, P(y_hat/x) - P(y_hat/x, alpha))
comprehensiveness(x, y_hat, alpha) = max(0, P(y_hat/x) - P(y_hat/x, alpha))
null difference = max(0, P(y_hat/x) - P(y_hat/x, 0))
normalized_sufficiency(x, y_hat, alpha) = (sufficiency(x, y_hat, alpha) - sufficiency(x, y_hat, 0)) / null difference
normalized_comp(x, y_hat, alpha) = comprehensiveness(x, y_hat, alpha) / null difference 

References:
- Samuel Carton, Anirudh Rathore, and Chenhao Tan. 2020. Evaluating and Characterizing Human Rationales.
 In Proceedings of the 2020 Conference on Empirical Methods in Natural Language Processing.
- Jay DeYoung, Sarthak Jain, Nazneen Fatema Rajani, Eric Lehman, Caiming Xiong, Richard Socher, and Byron C. Wallace.
 2019. ERASER: A Benchmark to Evaluate Rationalized NLP Models.
 arXiv preprint, November. arXiv: 1911.03429.
- Mo Yu, Shiyu Chang, Yang Zhang, and Tommi S. Jaakkola. 2019. Rethinking Cooperative Rationalization:
 Introspective Extraction and Complement Control.
 In Proceedings of the 2019 Conference on Empirical Methods in Natural Language Processing.
"""

_KWARGS_DESCRIPTION = """
Under Construction
Args:
	`predictions`: (numpy array) y_hat
	`prob_y_hat`: (numpy array) P(y_hat/x)
	`prob_y_hat_alpha`: (numpy array) P(y_hat/x, alpha)
	`null_difference`: (numpy array) max(0, P(y_hat/x) - P(y_hat/x, 0))
	`model`: (pytorch nn Module) model to compute predictions
	`pad_token_id`: padding token id for the corresponding tokenizer
	`input_ids`: (torch.tensor) tensor of input ids
	`alpha`: (list) 0s and 1s corresponding to the presence of a token in the rationale
	`attention_masks`: [Optional] (torch.tensor) tensor of attention masks
	`fidelity_type`: [Default="sufficiency"] (str) sufficiency or comprehensiveness
	`clip`: [Default=True] (bool) true for clipping the fidelity values between 0 and 1
	`normalization`: [Default=True] (bool) true for adjusting fidelity scores to account for baseline model behavior
	`reduction`: [Default='mean'] (str) option for returning the entire array of fidelities or mean of that
	`binarization_threshold`: [Default=0.5] >= 0.5 corresponds to 1 and 0 otherwise when binarizing alpha values
Returns:
	`fidelity`: 
"""


class Fidelity(datasets.Metric):
    def _info(self):
        return datasets.MetricInfo(
            description=_DESCRIPTION,
            citation=_CITATION,
            inputs_description=_KWARGS_DESCRIPTION,
            features=datasets.Features(
                {
                    "predictions": datasets.Value("float", id="sequence"),
                    "prob_y_hat": datasets.Value("float", id="sequence"),
                    "prob_y_hat_alpha": datasets.Value("float", id="sequence"),
                    "null_difference": datasets.Value("float", id="sequence"),
                    "mode": datasets.Value("string", id="sequence"),
                    "normalization": datasets.Value("bool", id="sequence"),
                }
            ),
        )

    def _compute(
        self,
        predictions: np.ndarray = None,
        prob_y_hat: np.ndarray = None,
        prob_y_hat_alpha: np.ndarray = None,
        null_difference: np.ndarray = None,
        model: torch.nn.Module = None,
        pad_token_id: int = None,
        input_ids: torch.Tensor = None,
        alpha: list = None,
        attention_masks: torch.Tensor = None,
        fidelity_type: str = "sufficiency",
        clip: bool = True,
        normalization: bool = True,
        reduction: str = "mean",
        binarization_threshold: float = 0.5,
    ):

        if normalization:
            if (
                (predictions is None)
                and (prob_y_hat is None or prob_y_hat_alpha is None or null_difference is None)
                and (model is None or input_ids is None or alpha is None)
            ):
                return "Please provide either predictions or model and inputs to compute predictions"
        else:
            if (
                (predictions is None)
                and (prob_y_hat is None or prob_y_hat_alpha is None)
                and (model is None or input_ids is None or alpha is None)
            ):
                return "Please provide either predictions or model and inputs to compute predictions"

        if prob_y_hat is None:
            predictions, prob_y_hat = utility.compute_predictions(
                input_ids=input_ids, model=model, attention_masks=attention_masks
            )
            prob_y_hat = prob_y_hat[np.arange(len(prob_y_hat)), predictions]

        if prob_y_hat_alpha is None:
            input_ids_reduced, attention_masks_reduced = utility.reduce_input_with_rationale(
                input_ids=input_ids, alpha=alpha, pad_token_id=pad_token_id, fidelity_type=fidelity_type
            )

            predictions_alpha, prob_y_hat_alpha = utility.compute_predictions(
                input_ids=input_ids_reduced, model=model, attention_masks=attention_masks_reduced
            )
            prob_y_hat_alpha = prob_y_hat_alpha[np.arange(len(prob_y_hat_alpha)), predictions]

        # Calculating fidelity value
        fidelity = utility.compute_fidelity(
            prob_y_hat=prob_y_hat,
            prob_y_hat_alpha=prob_y_hat_alpha,
            fidelity_type=fidelity_type,
            dataset_level=False,
            clip=clip,
        )

        if normalization:
            if null_difference is None:
                null_difference = utility.compute_null_diff(
                    input_ids=input_ids,
                    model=model,
                    predictions=predictions,
                    prob_y_hat=prob_y_hat,
                    pad_token_id=pad_token_id,
                )

            # Normalizing fidelity value
            fidelity = utility.normalize_item_set_fidelity(
                fidelity=fidelity, null_difference=null_difference, fidelity_type=fidelity_type, clip=clip
            )

        if reduction == "mean":
            return np.mean(fidelity)
        elif reduction is None:
            return fidelity
