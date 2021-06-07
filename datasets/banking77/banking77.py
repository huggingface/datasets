# coding=utf-8
# Copyright 2020 The HuggingFace Datasets Authors and the current dataset script contributor.
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
"""BANKING77 dataset."""


import csv

import datasets
from datasets.tasks import TextClassification


_CITATION = """\
@inproceedings{Casanueva2020,
    author      = {I{\~{n}}igo Casanueva and Tadas Temcinas and Daniela Gerz and Matthew Henderson and Ivan Vulic},
    title       = {Efficient Intent Detection with Dual Sentence Encoders},
    year        = {2020},
    month       = {mar},
    note        = {Data available at https://github.com/PolyAI-LDN/task-specific-datasets},
    url         = {https://arxiv.org/abs/2003.04807},
    booktitle   = {Proceedings of the 2nd Workshop on NLP for ConvAI - ACL 2020}
}
"""  # noqa: W605

_DESCRIPTION = """\
BANKING77 dataset provides a very fine-grained set of intents in a banking domain.
It comprises 13,083 customer service queries labeled with 77 intents.
It focuses on fine-grained single-domain intent detection.
"""

_HOMEPAGE = "https://github.com/PolyAI-LDN/task-specific-datasets"

_LICENSE = "Creative Commons Attribution 4.0 International"

_TRAIN_DOWNLOAD_URL = (
    "https://raw.githubusercontent.com/PolyAI-LDN/task-specific-datasets/master/banking_data/train.csv"
)
_TEST_DOWNLOAD_URL = "https://raw.githubusercontent.com/PolyAI-LDN/task-specific-datasets/master/banking_data/test.csv"


class Banking77(datasets.GeneratorBasedBuilder):
    """BANKING77 dataset."""

    VERSION = datasets.Version("1.1.0")

    def _info(self):
        features = datasets.Features(
            {
                "text": datasets.Value("string"),
                "label": datasets.features.ClassLabel(
                    names=[
                        "activate_my_card",
                        "age_limit",
                        "apple_pay_or_google_pay",
                        "atm_support",
                        "automatic_top_up",
                        "balance_not_updated_after_bank_transfer",
                        "balance_not_updated_after_cheque_or_cash_deposit",
                        "beneficiary_not_allowed",
                        "cancel_transfer",
                        "card_about_to_expire",
                        "card_acceptance",
                        "card_arrival",
                        "card_delivery_estimate",
                        "card_linking",
                        "card_not_working",
                        "card_payment_fee_charged",
                        "card_payment_not_recognised",
                        "card_payment_wrong_exchange_rate",
                        "card_swallowed",
                        "cash_withdrawal_charge",
                        "cash_withdrawal_not_recognised",
                        "change_pin",
                        "compromised_card",
                        "contactless_not_working",
                        "country_support",
                        "declined_card_payment",
                        "declined_cash_withdrawal",
                        "declined_transfer",
                        "direct_debit_payment_not_recognised",
                        "disposable_card_limits",
                        "edit_personal_details",
                        "exchange_charge",
                        "exchange_rate",
                        "exchange_via_app",
                        "extra_charge_on_statement",
                        "failed_transfer",
                        "fiat_currency_support",
                        "get_disposable_virtual_card",
                        "get_physical_card",
                        "getting_spare_card",
                        "getting_virtual_card",
                        "lost_or_stolen_card",
                        "lost_or_stolen_phone",
                        "order_physical_card",
                        "passcode_forgotten",
                        "pending_card_payment",
                        "pending_cash_withdrawal",
                        "pending_top_up",
                        "pending_transfer",
                        "pin_blocked",
                        "receiving_money",
                        "Refund_not_showing_up",
                        "request_refund",
                        "reverted_card_payment?",
                        "supported_cards_and_currencies",
                        "terminate_account",
                        "top_up_by_bank_transfer_charge",
                        "top_up_by_card_charge",
                        "top_up_by_cash_or_cheque",
                        "top_up_failed",
                        "top_up_limits",
                        "top_up_reverted",
                        "topping_up_by_card",
                        "transaction_charged_twice",
                        "transfer_fee_charged",
                        "transfer_into_account",
                        "transfer_not_received_by_recipient",
                        "transfer_timing",
                        "unable_to_verify_identity",
                        "verify_my_identity",
                        "verify_source_of_funds",
                        "verify_top_up",
                        "virtual_card_not_working",
                        "visa_or_mastercard",
                        "why_verify_identity",
                        "wrong_amount_of_cash_received",
                        "wrong_exchange_rate_for_cash_withdrawal",
                    ]
                ),
            }
        )
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=features,
            supervised_keys=None,
            homepage=_HOMEPAGE,
            license=_LICENSE,
            citation=_CITATION,
            task_templates=[TextClassification(text_column="text", label_column="label")],
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        train_path = dl_manager.download_and_extract(_TRAIN_DOWNLOAD_URL)
        test_path = dl_manager.download_and_extract(_TEST_DOWNLOAD_URL)
        return [
            datasets.SplitGenerator(name=datasets.Split.TRAIN, gen_kwargs={"filepath": train_path}),
            datasets.SplitGenerator(name=datasets.Split.TEST, gen_kwargs={"filepath": test_path}),
        ]

    def _generate_examples(self, filepath):
        """Yields examples as (key, example) tuples."""
        with open(filepath, encoding="utf-8") as f:
            csv_reader = csv.reader(f, quotechar='"', delimiter=",", quoting=csv.QUOTE_ALL, skipinitialspace=True)
            # call next to skip header
            next(csv_reader)
            for id_, row in enumerate(csv_reader):
                text, label = row
                yield id_, {"text": text, "label": label}
