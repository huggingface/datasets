# Copyright 2022 The HuggingFace Datasets Authors and the current dataset script contributor.
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
"""Perplexity Metric."""

import torch
from torch.nn import CrossEntropyLoss
from transformers import AutoModelForCausalLM, AutoTokenizer

import datasets
from datasets import logging


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
            NOTE: Perplexity can only be calculated for causal language models.
                    This includes models such as gpt2, causal variations of bert,
                    causal versions of t5, and more (the full list can be found
                    in the AutoModelForCausalLM documentation here:
                    https://huggingface.co/docs/transformers/master/en/model_doc/auto#transformers.AutoModelForCausalLM )

    input_texts (list of str): input text, each separate text snippet
        is one list entry. Perplexity returned will be an average of
        the perplexity for each list entry.
    stride (int): stride size, defaults to 512
    device (str): device to run on, defaults to 'cuda' when available
Returns:
    perplexity: dictionary containing the average perplexity score for the text
        in the input list.
Examples:
    Example 1:
        >>> perplexity = datasets.load_metric("perplexity")
        >>> input_texts = ["lorem ipsum", "Happy Birthday!", "Bienvenue"]
        >>> results = perplexity.compute(model_id='gpt2',
        ...                              input_texts=input_texts,
        ...                              stride=1)
        >>> round(results["perplexity"], 1)
        78.2

    Example 2:
        >>> perplexity = datasets.load_metric("perplexity")
        >>> input_texts = datasets.load_dataset("wikitext",
        ...                                     "wikitext-2-raw-v1",
        ...                                     split="test")["text"][:10] # doctest:+ELLIPSIS
        [...]
        >>> results = perplexity.compute(model_id='gpt2',
        ...                              input_texts=input_texts,
        ...                              stride=256)
        >>> round(results["perplexity"], 1)
        117.9

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
                    "input_texts": datasets.Value("string"),
                }
            ),
            reference_urls=["https://huggingface.co/docs/transformers/perplexity"],
        )

    def _compute(self,
                input_texts,
                model_id,
                batch_size: int = 16,
                add_start_token: bool = True,
                stride: int = 512,
                tensory_type: str = "pt",
                device=None):

        if device is not None:
            assert device in ["gpu", "cpu", "cuda"], "device should be either gpu or cpu."
            if device == "gpu":
                device = "cuda"
        else:
            device = "cuda" if torch.cuda.is_available() else "cpu"

        print("cuda avail?", torch.cuda.is_available())
        print(device)

        model = AutoModelForCausalLM.from_pretrained(model_id)
        model = model.to(device)

        if add_start_token:
            tokenizer = AutoTokenizer.from_pretrained(model_id, pad_token="<PAD>")
            max_tokenized_len = model.config.n_positions - 1
            if tokenizer.bos_token is None:
                tokenizer.add_special_tokens({'bos_token':'<BOS>'})
        else:
            tokenizer = AutoTokenizer.from_pretrained(model_id, pad_token="<PAD>")
            max_tokenized_len = model.config.n_positions

        model.resize_token_embeddings(len(tokenizer))

        

        encodings = tokenizer(input_texts, add_special_tokens=False, padding=True, truncation=True, max_length=max_tokenized_len, return_tensors="pt", return_attention_mask=True, return_special_tokens_mask=True).to(
            device
        )

        encoded_texts = encodings["input_ids"]
        attn_masks = encodings["attention_mask"]
        special_tokens_masks = encodings["special_tokens_mask"]

        max_model_length = model.config.n_positions

        ppls = []

        loss_fct = CrossEntropyLoss(reduction="none")

        for text_index in logging.tqdm(range(0, len(encoded_texts), batch_size)):
            encoded_batch = encoded_texts[text_index:min(text_index+batch_size, len(encoded_texts))]
            attn_mask = attn_masks[text_index:min(text_index+batch_size, len(attn_masks))]
           
            special_tokens_mask = special_tokens_masks[text_index:min(text_index+batch_size, len(attn_masks))] 

            if add_start_token:
                bos_tokens_tensor = torch.tensor([[tokenizer.bos_token_id]]*encoded_batch.size(dim=0)).to(device)
                encoded_batch = torch.cat([bos_tokens_tensor, encoded_batch], dim=1)
                attn_mask = torch.cat([torch.zeros(bos_tokens_tensor.size(), dtype=torch.int64).to(device), attn_mask], dim=1)
                print("encoded_batch:", encoded_batch)
                # pred_mask = torch.tensor([[-100]]*encoded_batch.size(dim=0)).to(device)

                # print("pred_mask size:", pred_mask.size(), "|| encoded_batch size:", encoded_batch.size())

                #labels = torch.cat([pred_mask, encoded_batch[:, 1:]], dim=1)
            #else:
            labels = encoded_batch

            #encoded_text_length = len(encoded_text) - special_tokens_mask.sum()

            nlls = []

            #target_index = max(1, min(stride - 1, encoded_text_length - 1))

            while False: #target_index < encoded_text_length:
                start_index = max(0, target_index - (max_model_length - 1))

                input_ids = encoded_text[start_index : target_index + 1]

                target_ids = input_ids.clone()
                target_ids[:-1] = -100

                attn_mask = torch.ones(len(input_ids)).to(device)
                attn_mask[-1] = 0

                with torch.no_grad():
                    outputs = model(input_ids, labels=target_ids, attention_mask=attn_mask)
                    neg_log_likelihood = outputs[0]

                nlls.append(neg_log_likelihood)

                target_index += stride

            # print("max model length:", max_model_length, "|| embedding length:", encoded_batch.size())
            # print("encoded text:", encoded_batch)
            # print("special token mask:", special_tokens_mask)
            # print("attn mask:", attn_mask)
            # print("bos_token:", tokenizer.bos_token, tokenizer.bos_token_id)

            # break

            with torch.no_grad():
                mod = model(encoded_batch, attention_mask=attn_mask)
            out_logits = mod.logits

            print("out_logits:", out_logits)

            loss_fct = CrossEntropyLoss(reduction="none")


            attn_labels = labels.clone()
            attn_labels[labels == 0] = -100
            loss_num = loss_fct(out_logits.transpose(1,2), attn_labels)
            print("loss_num:", loss_num)
            exponent = (loss_num*attn_mask).sum(1) / attn_mask.sum(1)
            print("exponent:", exponent)
            perp_batch = torch.exp2(exponent).tolist()
            print("perp_batch:", perp_batch)

            shift_logits = out_logits[..., :-1, :].contiguous()
            shift_labels = labels[..., 1:].contiguous()
            shift_attention_mask_batch = attn_mask[..., 1:].contiguous()

            perplexity_batch = torch.exp((loss_fct(shift_logits.transpose(1,2), shift_labels)*shift_attention_mask_batch).sum(1) / shift_attention_mask_batch.sum(1)).tolist()


            ppls += perplexity_batch


            #if len(nlls) > 0:
            #ppls.append(torch.exp2(torch.mean(torch.stack(nlls))))

        #ppl = torch.mean(torch.stack(ppls))

        return {"perplexity": ppls}
