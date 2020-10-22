import logging

import numpy as np

import metrics.fidelity.utility as utility
import datasets


logger = logging.getLogger(__name__)

_CITATION = """
citation is under construction 
@misc{carton2020evaluating,
      title={Evaluating and Characterizing Human Rationales}, 
      author={Samuel Carton and Anirudh Rathore and Chenhao Tan},
      year={2020},
      eprint={2010.04736},
      archivePrefix={arXiv},
      primaryClass={cs.CL}
}
"""

_DESCRIPTION = """
description is under construction
sufficiency(x, y_hat, alpha) = 1 - max(0, P(y_hat/x) - P(y_hat/x, alpha))
comprehensiveness(x, y_hat, alpha) = max(0, P(y_hat/x) - P(y_hat/x, alpha))
null difference = max(0, P(y_hat/x) - P(y_hat/x, 0))
"""

_KWARGS_DESCRIPTION = """
Args:
	`predictions`: (numpy array) y_hat
	`prob_y_hat`: (numpy array) P(y_hat/x)
	`prob_y_hat_alpha`: (numpy array) P(y_hat/x, alpha)
	`null_difference`: (numpy array) max(0, P(y_hat/x) - P(y_hat/x, 0))
	`model`: (pytorch nn Module) model to compute predictions
	`tokenizer`: data tokenizer
	`input_ids`: (torch.tensor) tensor of input ids
	`alpha`: (list) 0s and 1s corresponding to the presence of a token in the rationale
	`attention_masks`: [Optional] (torch.tensor) tensor of attention masks
	`fidelity_type`: [Default="sufficiency"] (str) sufficiency or comprehensiveness
	`clip`: [Default=True] (bool) true for clipping the fidelity values between 0 and 1
	`normalization`: [Default=True] (bool) true for calibrating 
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
                    "model": datasets.Value("float", id="sequence"),
                    "tokenizer": datasets.Value("float", id="sequence"),
                    "mode": datasets.Value("string", id="sequence"),
                    "normalization": datasets.Value("bool", id="sequence"),
                }
            ),
        )

    def _compute(
        self,
        predictions=None,
        prob_y_hat=None,
        prob_y_hat_alpha=None,
        null_difference=None,
        model=None,
        tokenizer=None,
        input_ids=None,
        alpha=None,
        attention_masks=None,
        fidelity_type="sufficiency",
        clip=True,
        normalization=True,
        # reduction='mean' # discuss with sam
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
            input_ids_reduced, attention_masks_reduced = utility.reduce(
                input_ids=input_ids, rationale=alpha, tokenizer=tokenizer, fidelity_type=fidelity_type
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
                    tokenizer=tokenizer,
                )

            # Normalizing fidelity value
            fidelity = utility.normalization(
                fidelity=fidelity, null_difference=null_difference, fidelity_type=fidelity_type, clip=clip
            )

        # if reduction == 'mean':
        # 	return np.mean(fidelity)
        # elif reduction is None:
        # Ask about reduction from Sam
        return fidelity
