# coding=utf-8
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
""" Perplexity Metric """


from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
from tqdm import tqdm
import datasets

_CITATION = """\

"""

_DESCRIPTION = """
Perplexity (PPL) is one of the most common metrics for evaluating language models.
It is defined as the exponentiated average negative log-likelihood of a sequence.

For more information, see https://huggingface.co/docs/transformers/perplexity
"""

_KWARGS_DESCRIPTION = """
Args:
    model_id (str): model used for calculating Perplexity
    input_text (list of str): input text, each separate text snippet
        is one list entry. Perplexity returned will be an average of
        the perplexity for each list entry.
    stride (int): stride size, defaults to 512
    device (str): device to run on, defaults to cuda
Returns:
    perplexity: average perplexity score for segment
Examples:
    Example 1:
        >>> perplexity = datsets.load_meric("perplexity")
        >>> input_text = ["lorem ipsum", "Happy Birthday!", "Bienvenue"]
        >>> results = perplexity.compute(model_id='gpt2',
                                        input_text=input_text,
                                        stride=1)
        {'perplexity': }

    Example 2:
        >>> perplexity = datasets.load_metric("perplexity")
        >>> input_text = datasets.load_dataset("wikitext", "wikitext-2-raw-v1", "test")
        >>> results = perplexity.compute(model_id='gpt2',
                                        input_text=input_text,
                                        stride=512)
        {'perplexity': }

    >>> perplexity = datasets.load_metric("perplexity")
    >>> results = perplexity.compute(model='gpt2-large', stride=1024)
    >>> print(results)
    {'perplexity': 19.64}
"""



@datasets.utils.file_utils.add_start_docstrings(_DESCRIPTION, _KWARGS_DESCRIPTION)
class Perplexity(datasets.Metric):
    def _info(self):
        return datasets.MetricInfo(
            description=_DESCRIPTION,
            citation=_CITATION,
            inputs_description=_KWARGS_DESCRIPTION,
            features=datasets.Features(
                {
                    "predictions": None,
                    "references": None
                }
            ),
            reference_urls=[
                "https://huggingface.co/docs/transformers/perplexity"
            ],
        )

    def compute(self, **kwargs):
        """ Compute perplexity. Overrides the metrics `compute` method.

        Args:
            **kwargs: Keyword arguments that will be forwarded
                        to the perplexity :meth:`_compute` method.

        Return:
            perplexity (float)
        """

        return self._compute(**kwargs)


    def _compute(
        self,
        model_id,
        input_text,
        stride=512,
        device=None):
        """ Compute Perplexity """

        model = AutoModelForCausalLM.from_pretrained(model_id)
        model = model.to(device)

        tokenizer = AutoTokenizer.from_pretrained(model_id, pad_token="<PAD>")

        encodings = tokenizer(input_text, padding=True, return_tensors='pt', return_special_tokens_mask=True)

        encoded_texts = encodings['input_ids']
        special_tokens_masks = encodings['special_tokens_mask']

        max_model_length = model.config.n_positions

        ppls = []
        
        for text_index in tqdm(range(0, len(encoded_texts))):
            encoded_text = encoded_texts[text_index]
            special_tokens_mask = special_tokens_masks[text_index]

            encoded_text_length = len(encoded_text) - special_tokens_mask.sum()

            nlls = []

            target_index = 1
            num_predictions = 0

            while target_index < encoded_text_length:
                start_index = max(0, target_index - (max_model_length - 1))

                input_ids = encoded_text[start_index:target_index+1]

                target_ids = input_ids.clone()
                target_ids[:-1] = -100

                with torch.no_grad():
                    outputs = model(input_ids, labels=target_ids)
                    neg_log_likelihood = outputs[0]

                nlls.append(neg_log_likelihood)

                target_index+=stride
                num_predictions+=1

            if len(nlls) > 0:
                ppls.append(torch.exp(torch.stack(nlls).sum() / num_predictions))

        print(ppls)
        ppl = torch.stack(ppls).sum() / len(encoded_texts)

        return {
            "perplexity": float(ppl),
        }

