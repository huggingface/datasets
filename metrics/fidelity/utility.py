import logging

import numpy as np
import torch


logger = logging.getLogger(__name__)


def compute_fidelity(prob_y_hat, prob_y_hat_alpha, fidelity_type="sufficiency", clip=True, dataset_level=False):
    """
    clip=False ERASER's definition of sufficiency and comprehensiveness Cite?? ask chenhao
    Calculating the fidelity value given probabilities
    :param prob_y_hat: P(y_hat/x)
    :param prob_y_hat_alpha: P(y_hat/x,alpha) where text is reduced by alpha
    :param fidelity_type: sufficiency or comprehensiveness
    :param clip: true for clipping the fidelity values between 0 and 1
    :param dataset_level: dataset level fidelity else instance level
    :return: fidelity
    """
    if clip:
        mean_difference = np.clip(np.array(prob_y_hat) - np.array(prob_y_hat_alpha), 0, 1)
    else:
        mean_difference = prob_y_hat - prob_y_hat_alpha
    if dataset_level:
        mean_difference = np.mean(mean_difference)
    if fidelity_type == "sufficiency":
        return 1 - mean_difference
    else:
        return mean_difference


def itemwize_normalization(fidelity, null_difference, fidelity_type, clip, eps):
    """
    Normalize a fidelity value given the null difference value
    :param fidelity: sufficiency or comprehensiveness metric
    :param null_difference: max(0, P(y_hat/x) - P(y_hat/x, 0)); alpha = 0
    :param fidelity_type: sufficiency or comprehensiveness
    :param clip: true for clipping the fidelity values between 0 and 1
    :param eps: denominator threshold when it tends to 0
    :return: normalized fidelity
    """
    try:
        if fidelity_type == "sufficiency":
            numerator = fidelity - (1 - null_difference)
            denominator = 1 - (1 - null_difference)
        else:
            numerator = fidelity
            denominator = null_difference

        if np.abs(denominator) < eps:
            result = 0
        else:
            result = numerator / denominator
    except Exception as e:
        logger.info(e)
        return 0

    if clip:
        return np.clip(result, 0, 1)
    else:
        return result


def normalization(fidelity, null_difference, fidelity_type="sufficiency", clip=True, eps=1e-5):
    """
    Normalize a list of fidelity values given the null difference values
    :param fidelity: sufficiency or comprehensiveness metric
    :param null_difference: max(0, P(y_hat/x) - P(y_hat/x, 0)); alpha = 0
    :param fidelity_type: sufficiency or comprehensiveness
    :param clip: true for clipping the fidelity values between 0 and 1
    :param eps: denominator threshold when it tends to 0
    :return: normalized fidelity
    """
    normalized_fidelity = []
    for idx, itemwize_fidelity in enumerate(fidelity):
        normalized_fidelity.append(
            itemwize_normalization(
                fidelity=itemwize_fidelity,
                null_difference=null_difference[idx],
                fidelity_type=fidelity_type,
                clip=clip,
                eps=eps,
            )
        )

    return normalized_fidelity


def compute_predictions(input_ids, model, attention_masks=None):
    """
    Compute the prediction for given input_ids, model and attention masks
    This function returns numpy arrays of labels and probabilities associated with that label
    :param input_ids: tensor of input ids
    :param model: pytorch nn Module
    :param attention_masks: tensor of attention masks
    :return: numpy array of labels and probabilities associated with that label
    """
    if attention_masks is not None:
        result = model.forward(input_ids=input_ids.to(model.device), attention_mask=attention_masks.to(model.device))
    else:
        result = model.forward(input_ids=input_ids.to(model.device))

    if model.device == "cuda":
        result["py_index"] = result["py_index"].detach().cpu()
        result["probs"] = result["probs"].detach().cpu()

    return result["py_index"].numpy(), result["probs"].numpy()


def compute_null_diff(input_ids, model, predictions, prob_y_hat, tokenizer):
    """
    Calculate the null difference which helps in accounting for model-dependent baseline performance
    null difference = max(0, p(y_hat/x) - p(y_hat/x, 0))
    returns the label and prediction probability
    :param prob_y_hat: P(y_hat/x)
    :param predictions: y_hat
    :param input_ids: tensor of input ids
    :param model: pytorch nn Module
    :param tokenizer: data tokenizer
    :return: null difference
    """
    input_ids_reduced, attention_mask_reduced = reduce(input_ids=input_ids, rationale=None, tokenizer=tokenizer)

    predictions_0, prob_y_hat_0 = compute_predictions(
        input_ids=input_ids_reduced, model=model, attention_masks=attention_mask_reduced
    )
    prob_y_hat_0_predicted_class = prob_y_hat_0[np.arange(len(prob_y_hat_0)), predictions]

    null_difference = 1 - compute_fidelity(
        prob_y_hat=prob_y_hat, prob_y_hat_alpha=prob_y_hat_0_predicted_class, fidelity_type="sufficiency"
    )

    return null_difference


def reduce(input_ids, rationale=None, tokenizer=None, fidelity_type="sufficiency"):
    """
    Reduce the input_ids based on the alpha values or the rationale values
    sufficiency - reduce by keeping only the tokens which are in the rationale
    comprehensiveness - reduce by keeping all the tokens which are not in the rationale
    :param input_ids: tensor of input ids
    :param rationale: a list of 0s or 1s corresponding to a token's presence in the rationale
    :param tokenizer: data tokenizer
    :param fidelity_type: sufficiency or comprehensiveness
    :return: tensor of reduced input ids and reduced attention masks
    """
    input_ids_reduced = []
    attention_mask_reduced = []
    for idx in range(len(input_ids)):
        if rationale is None:
            rationale_i = [0] * len(input_ids[idx])
        else:
            rationale_i = rationale[idx]
        input_ids_reduced_i = []
        attention_mask_reduced_i = []
        for j in range(len(input_ids[idx])):
            if input_ids[idx][j] in [0, 2]:
                input_ids_reduced_i.append(input_ids[idx][j].item())
                attention_mask_reduced_i.append(1)
            else:
                if fidelity_type == "sufficiency" and rationale_i[j] >= 0.5:
                    input_ids_reduced_i.append(input_ids[idx][j].item())
                    attention_mask_reduced_i.append(1)
                elif fidelity_type == "comprehensiveness" and rationale_i[j] < 0.5:
                    input_ids_reduced_i.append(input_ids[idx][j].item())
                    attention_mask_reduced_i.append(1)

        num_padding_tokens = len(input_ids[idx]) - len(input_ids_reduced_i)
        input_ids_reduced_i = input_ids_reduced_i + [tokenizer.pad_token_id] * num_padding_tokens
        attention_mask_reduced_i = attention_mask_reduced_i + [0] * num_padding_tokens
        input_ids_reduced.append(input_ids_reduced_i)
        attention_mask_reduced.append(attention_mask_reduced_i)
    return torch.tensor(input_ids_reduced), torch.tensor(attention_mask_reduced)
