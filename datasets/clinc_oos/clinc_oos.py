"""An Evaluation Dataset for Intent Classification and Out-of-Scope Prediction"""

from __future__ import absolute_import, division, print_function

import json
import textwrap

import datasets


_CITATION = """\
    @inproceedings{larson-etal-2019-evaluation,
    title = "An Evaluation Dataset for Intent Classification and Out-of-Scope Prediction",
    author = "Larson, Stefan  and
      Mahendran, Anish  and
      Peper, Joseph J.  and
      Clarke, Christopher  and
      Lee, Andrew  and
      Hill, Parker  and
      Kummerfeld, Jonathan K.  and
      Leach, Kevin  and
      Laurenzano, Michael A.  and
      Tang, Lingjia  and
      Mars, Jason",
    booktitle = "Proceedings of the 2019 Conference on Empirical Methods in Natural Language Processing and the 9th International Joint Conference on Natural Language Processing (EMNLP-IJCNLP)",
    year = "2019",
    url = "https://www.aclweb.org/anthology/D19-1131"
}
"""

_DESCRIPTION = """\
    This dataset is for evaluating the performance of intent classification systems in the
    presence of "out-of-scope" queries. By "out-of-scope", we mean queries that do not fall
    into any of the system-supported intent classes. Most datasets include only data that is
    "in-scope". Our dataset includes both in-scope and out-of-scope data. You might also know
    the term "out-of-scope" by other terms, including "out-of-domain" or "out-of-distribution".
"""

_DESCRIPTIONS = {
    "small": textwrap.dedent(
        """\
        Small, in which there are only 50 training queries per each in-scope intent
        """
    ),
    "imbalanced": textwrap.dedent(
        """\
        Imbalanced, in which intents have either 25, 50, 75, or 100 training queries.
        """
    ),
    "plus": textwrap.dedent(
        """\
        OOS+, in which there are 250 out-of-scope training examples, rather than 100.
        """
    ),
}

_URL = "https://github.com/clinc/oos-eval/"

_DATA_URLS = {
    "small": "https://raw.githubusercontent.com/clinc/oos-eval/master/data/data_small.json",
    "imbalanced": "https://raw.githubusercontent.com/clinc/oos-eval/master/data/data_imbalanced.json",
    "plus": "https://raw.githubusercontent.com/clinc/oos-eval/master/data/data_oos_plus.json",
}


class ClincConfig(datasets.BuilderConfig):

    """BuilderConfig for CLINC150"""

    def __init__(self, description, data_url, citation, url, **kwrags):
        """
        Args:
            description: `string`, brief description of the dataset
            data_url: `dictionary`, dict with url for each split of data.
            citation: `string`, citation for the dataset.
            url: `string`, url for information about the dataset.
            **kwrags: keyword arguments frowarded to super
        """
        super(ClincConfig, self).__init__(version=datasets.Version("1.0.0", ""), **kwrags)
        self.description = description
        self.data_url = data_url
        self.citation = citation
        self.url = url


class ClincOos(datasets.GeneratorBasedBuilder):
    BUILDER_CONFIGS = [
        ClincConfig(
            name=name, description=_DESCRIPTIONS[name], data_url=_DATA_URLS[name], citation=_CITATION, url=_URL
        )
        for name in ["small", "imbalanced", "plus"]
    ]

    def _info(self):
        features = {}
        features["text"] = datasets.Value("string")
        labels_list = [
            "restaurant_reviews",
            "nutrition_info",
            "account_blocked",
            "oil_change_how",
            "time",
            "weather",
            "redeem_rewards",
            "interest_rate",
            "gas_type",
            "accept_reservations",
            "smart_home",
            "user_name",
            "report_lost_card",
            "repeat",
            "whisper_mode",
            "what_are_your_hobbies",
            "order",
            "jump_start",
            "schedule_meeting",
            "meeting_schedule",
            "freeze_account",
            "what_song",
            "meaning_of_life",
            "restaurant_reservation",
            "traffic",
            "make_call",
            "text",
            "bill_balance",
            "improve_credit_score",
            "change_language",
            "no",
            "measurement_conversion",
            "timer",
            "flip_coin",
            "do_you_have_pets",
            "balance",
            "tell_joke",
            "last_maintenance",
            "exchange_rate",
            "uber",
            "car_rental",
            "credit_limit",
            "oos",
            "shopping_list",
            "expiration_date",
            "routing",
            "meal_suggestion",
            "tire_change",
            "todo_list",
            "card_declined",
            "rewards_balance",
            "change_accent",
            "vaccines",
            "reminder_update",
            "food_last",
            "change_ai_name",
            "bill_due",
            "who_do_you_work_for",
            "share_location",
            "international_visa",
            "calendar",
            "translate",
            "carry_on",
            "book_flight",
            "insurance_change",
            "todo_list_update",
            "timezone",
            "cancel_reservation",
            "transactions",
            "credit_score",
            "report_fraud",
            "spending_history",
            "directions",
            "spelling",
            "insurance",
            "what_is_your_name",
            "reminder",
            "where_are_you_from",
            "distance",
            "payday",
            "flight_status",
            "find_phone",
            "greeting",
            "alarm",
            "order_status",
            "confirm_reservation",
            "cook_time",
            "damaged_card",
            "reset_settings",
            "pin_change",
            "replacement_card_duration",
            "new_card",
            "roll_dice",
            "income",
            "taxes",
            "date",
            "who_made_you",
            "pto_request",
            "tire_pressure",
            "how_old_are_you",
            "rollover_401k",
            "pto_request_status",
            "how_busy",
            "application_status",
            "recipe",
            "calendar_update",
            "play_music",
            "yes",
            "direct_deposit",
            "credit_limit_change",
            "gas",
            "pay_bill",
            "ingredients_list",
            "lost_luggage",
            "goodbye",
            "what_can_i_ask_you",
            "book_hotel",
            "are_you_a_bot",
            "next_song",
            "change_speed",
            "plug_type",
            "maybe",
            "w2",
            "oil_change_when",
            "thank_you",
            "shopping_list_update",
            "pto_balance",
            "order_checks",
            "travel_alert",
            "fun_fact",
            "sync_device",
            "schedule_maintenance",
            "apr",
            "transfer",
            "ingredient_substitution",
            "calories",
            "current_location",
            "international_fees",
            "calculator",
            "definition",
            "next_holiday",
            "update_playlist",
            "mpg",
            "min_payment",
            "change_user_name",
            "restaurant_suggestion",
            "travel_notification",
            "cancel",
            "pto_used",
            "travel_suggestion",
            "change_volume",
        ]
        features["intent"] = datasets.ClassLabel(names=labels_list)

        return datasets.DatasetInfo(
            description=_DESCRIPTION + "\n" + self.config.description,
            features=datasets.Features(features),
            homepage=self.config.url,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        file_ = dl_manager.download_and_extract(self.config.data_url)

        return [
            datasets.SplitGenerator(name=datasets.Split.TRAIN, gen_kwargs={"filepath": file_, "split": "train"}),
            datasets.SplitGenerator(name=datasets.Split.VALIDATION, gen_kwargs={"filepath": file_, "split": "val"}),
            datasets.SplitGenerator(name=datasets.Split.TEST, gen_kwargs={"filepath": file_, "split": "test"}),
        ]

    def _generate_examples(self, filepath, split):
        with open(filepath, encoding="utf-8") as f:
            j = json.load(f)
            for id_, row in enumerate(j[split] + j["oos_" + split]):
                yield id_, {"text": row[0], "intent": row[1]}
