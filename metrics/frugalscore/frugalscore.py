# Copyright 2022 The HuggingFace Datasets Authors and the current metric script contributor.
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
"""FrugalScore metric."""

import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer, Trainer, TrainingArguments

import datasets


_CITATION = """\
@article{eddine2021frugalscore,
  title={FrugalScore: Learning Cheaper, Lighter and Faster Evaluation Metrics for Automatic Text Generation},
  author={Eddine, Moussa Kamal and Shang, Guokan and Tixier, Antoine J-P and Vazirgiannis, Michalis},
  journal={arXiv preprint arXiv:2110.08559},
  year={2021}
}
"""

_DESCRIPTION = """\
FrugalScore is a reference-based metric for NLG models evaluation. It is based on a distillation approach that allows to learn a fixed, low cost version of any expensive NLG metric, while retaining most of its original performance.
"""


_KWARGS_DESCRIPTION = """
Calculates how good are predictions given some references, using certain scores.
Args:
    predictions (list of str): list of predictions to score. Each predictions
        should be a string.
    references (list of str): list of reference for each prediction. Each
        reference should be a string.
    batch_size (int): the batch size for predictions.
    max_length (int): maximum sequence length.
    device (str): either gpu or cpu
Returns:
    scores (list of int): list of scores.
Examples:
    >>> frugalscore = datasets.load_metric("frugalscore")
    >>> results = frugalscore.compute(predictions=['hello there', 'huggingface'], references=['hello world', 'hugging face'])
    >>> print([round(s, 3) for s in results["scores"]])
    [0.631, 0.645]
"""


@datasets.utils.file_utils.add_start_docstrings(_DESCRIPTION, _KWARGS_DESCRIPTION)
class FRUGALSCORE(datasets.Metric):
    def _info(self):
        return datasets.MetricInfo(
            description=_DESCRIPTION,
            citation=_CITATION,
            inputs_description=_KWARGS_DESCRIPTION,
            features=datasets.Features(
                {
                    "predictions": datasets.Value("string"),
                    "references": datasets.Value("string"),
                }
            ),
            homepage="https://github.com/moussaKam/FrugalScore",
        )

    def _download_and_prepare(self, dl_manager):
        if self.config_name == "default":
            checkpoint = "moussaKam/frugalscore_tiny_bert-base_bert-score"
        else:
            checkpoint = self.config_name
        self.model = AutoModelForSequenceClassification.from_pretrained(checkpoint)
        self.tokenizer = AutoTokenizer.from_pretrained(checkpoint)

    def _compute(
        self,
        predictions,
        references,
        batch_size=32,
        max_length=128,
        device=None,
    ):
        """Returns the scores"""
        assert len(predictions) == len(
            references
        ), "predictions and references should have the same number of sentences."
        if device is not None:
            assert device in ["gpu", "cpu"], "device should be either gpu or cpu."
        else:
            device = "gpu" if torch.cuda.is_available() else "cpu"
        training_args = TrainingArguments(
            "trainer",
            fp16=(device == "gpu"),
            per_device_eval_batch_size=batch_size,
            report_to=None,
            no_cuda=(device == "cpu"),
        )
        dataset = {"sentence1": predictions, "sentence2": references}
        raw_datasets = datasets.Dataset.from_dict(dataset)

        def tokenize_function(data):
            return self.tokenizer(
                data["sentence1"], data["sentence2"], max_length=max_length, truncation=True, padding=True
            )

        tokenized_datasets = raw_datasets.map(tokenize_function, batched=True)
        tokenized_datasets.remove_columns(["sentence1", "sentence2"])
        trainer = Trainer(self.model, training_args, tokenizer=self.tokenizer)
        predictions = trainer.predict(tokenized_datasets)
        return {"scores": list(predictions.predictions.squeeze(-1))}
