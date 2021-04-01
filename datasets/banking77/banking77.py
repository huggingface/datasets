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

from __future__ import absolute_import, division, print_function

import csv

import datasets


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
                        "card_arrival",
                        "card_linking",
                        "exchange_rate",
                        "card_payment_wrong_exchange_rate",
                        "extra_charge_on_statement",
                        "pending_cash_withdrawal",
                        "fiat_currency_support",
                        "card_delivery_estimate",
                        "automatic_top_up",
                        "card_not_working",
                        "exchange_via_app",
                        "lost_or_stolen_card",
                        "age_limit",
                        "pin_blocked",
                        "contactless_not_working",
                        "top_up_by_bank_transfer_charge",
                        "pending_top_up",
                        "cancel_transfer",
                        "top_up_limits",
                        "wrong_amount_of_cash_received",
                        "card_payment_fee_charged",
                        "transfer_not_received_by_recipient",
                        "supported_cards_and_currencies",
                        "getting_virtual_card",
                        "card_acceptance",
                        "top_up_reverted",
                        "balance_not_updated_after_cheque_or_cash_deposit",
                        "card_payment_not_recognised",
                        "edit_personal_details",
                        "why_verify_identity",
                        "unable_to_verify_identity",
                        "get_physical_card",
                        "visa_or_mastercard",
                        "topping_up_by_card",
                        "disposable_card_limits",
                        "compromised_card",
                        "atm_support",
                        "direct_debit_payment_not_recognised",
                        "passcode_forgotten",
                        "declined_cash_withdrawal",
                        "pending_card_payment",
                        "lost_or_stolen_phone",
                        "request_refund",
                        "declined_transfer",
                        "Refund_not_showing_up",
                        "declined_card_payment",
                        "pending_transfer",
                        "terminate_account",
                        "card_swallowed",
                        "transaction_charged_twice",
                        "verify_source_of_funds",
                        "transfer_timing",
                        "reverted_card_payment?",
                        "change_pin",
                        "beneficiary_not_allowed",
                        "transfer_fee_charged",
                        "receiving_money",
                        "failed_transfer",
                        "transfer_into_account",
                        "verify_top_up",
                        "getting_spare_card",
                        "top_up_by_cash_or_cheque",
                        "order_physical_card",
                        "virtual_card_not_working",
                        "wrong_exchange_rate_for_cash_withdrawal",
                        "get_disposable_virtual_card",
                        "top_up_failed",
                        "balance_not_updated_after_bank_transfer",
                        "cash_withdrawal_not_recognised",
                        "exchange_charge",
                        "top_up_by_card_charge",
                        "activate_my_card",
                        "cash_withdrawal_charge",
                        "card_about_to_expire",
                        "apple_pay_or_google_pay",
                        "verify_my_identity",
                        "country_support",
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
        """ Yields examples as (key, example) tuples. """
        with open(filepath, encoding="utf-8") as f:
            csv_reader = csv.reader(f, quotechar='"', delimiter=",", quoting=csv.QUOTE_ALL, skipinitialspace=True)
            # call next to skip header
            next(csv_reader)
            for id_, row in enumerate(csv_reader):
                text, label = row
                yield id_, {"text": text, "label": label}
