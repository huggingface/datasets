import csv
import os
import textwrap

import datasets
from datasets import TextClassification


logger = datasets.logging.get_logger(__name__)


_DESCRIPTION = textwrap.dedent(
    """\
The Consumer Complaint Database is a collection of complaints about consumer financial products and services that we sent to companies for response. Complaints are published after the company responds, confirming a commercial relationship with the consumer, or after 15 days, whichever comes first. Complaints referred to other regulators, such as complaints about depository institutions with less than $10 billion in assets, are not published in the Consumer Complaint Database. The database generally updates daily.
There are multiple Text Classification problems that can be solved with this dataset:
- Complaint Type Identification
- Complaint Sub-Product Identification
- Complaint from vulnerable or Service-person
"""
)

_CITATION = """\
"""

_BASE_DOWNLOAD_URL = "https://files.consumerfinance.gov/ccdb/complaints.csv.zip"

_HOMEPAGE = "https://www.consumerfinance.gov/data-research/consumer-complaints/"

_LICENSE = "https://cfpb.github.io/source-code-policy/"

_SUPPORTED_VERSIONS = [
    datasets.Version("1.0.0", "Initial Version"),
]


_DEFAULT_VERSION = datasets.Version("1.0.0", "Initial Version")

_url = _BASE_DOWNLOAD_URL

_TAGS = ["Servicemember", "Older American", "Older American, Servicemember", ""]

_SUB_PRODUCT_CATEGORIES = [
    "Credit reporting",
    "General-purpose credit card or charge card",
    "Checking account",
    "Other debt",
    "Second mortgage",
    "Conventional home mortgage",
    "I do not know",
    "Credit card debt",
    "Medical debt",
    "Federal student loan servicing",
    "FHA mortgage",
    "Conventional fixed mortgage",
    "Loan",
    "Other (i.e. phone, health club, etc.)",
    "Store credit card",
    "Installment loan",
    "Credit card",
    "Medical",
    "Mobile or digital wallet",
    "Private student loan",
    "Non-federal student loan",
    "Domestic (US) money transfer",
    "VA mortgage",
    "Vehicle loan",
    "Auto debt",
    "Payday loan",
    "Conventional adjustable mortgage (ARM)",
    "Other personal consumer report",
    "Payday loan debt",
    "Savings account",
    "Virtual currency",
    "Other bank product/service",
    "Other type of mortgage",
    "Other banking product or service",
    "Other mortgage",
    "International money transfer",
    "Lease",
    "General-purpose prepaid card",
    "Home equity loan or line of credit (HELOC)",
    "Government benefit card",
    "Mortgage debt",
    "Personal line of credit",
    "Home equity loan or line of credit",
    "Federal student loan debt",
    "Private student loan debt",
    "Credit repair services",
    "Title loan",
    "Auto",
    "Vehicle lease",
    "Mortgage",
    "Reverse mortgage",
    "General purpose card",
    "CD (Certificate of Deposit)",
    "Federal student loan",
    "Payroll card",
    "Debt settlement",
    "Check cashing service",
    "Traveler's check or cashier's check",
    "Gift card",
    "(CD) Certificate of deposit",
    "Money order",
    "Foreign currency exchange",
    "Refund anticipation check",
    "Gift or merchant card",
    "Cashing a check without an account",
    "ID prepaid card",
    "Mobile wallet",
    "Government benefit payment card",
    "Pawn loan",
    "Other special purpose card",
    "Check cashing",
    "Credit repair",
    "Traveler’s/Cashier’s checks",
    "Transit card",
    "Student prepaid card",
    "Electronic Benefit Transfer / EBT card",
    "",
]

_PRODUCT_CATEGORIES = [
    "Credit reporting, credit repair services, or other personal consumer reports",
    "Debt collection",
    "Mortgage",
    "Credit card or prepaid card",
    "Checking or savings account",
    "Credit reporting",
    "Student loan",
    "Money transfer, virtual currency, or money service",
    "Credit card",
    "Vehicle loan or lease",
    "Bank account or service",
    "Payday loan, title loan, or personal loan",
    "Consumer Loan",
    "Payday loan",
    "Money transfers",
    "Prepaid card",
    "Other financial service",
    "Virtual currency",
]


class ConsumerComplaints(datasets.GeneratorBasedBuilder):
    """Consumer Complaints dataset."""

    def _info(self):
        features = datasets.Features(
            {
                "Date Received": datasets.Value("timestamp[s]"),
                "Product": datasets.features.ClassLabel(names=_PRODUCT_CATEGORIES),
                "Sub Product": datasets.features.ClassLabel(names=_SUB_PRODUCT_CATEGORIES),
                "Issue": datasets.Value("string"),
                "Sub Issue": datasets.Value("string"),
                "Complaint Text": datasets.Value("string"),
                "Company Public Response": datasets.Value("string"),
                "Company": datasets.Value("string"),
                "State": datasets.Value("string"),
                "Zip Code": datasets.Value("string"),
                "Tags": datasets.features.ClassLabel(names=_TAGS),
                "Consumer Consent Provided": datasets.Value("string"),
                "Submitted via": datasets.Value("string"),
                "Date Sent To Company": datasets.Value("string"),
                "Company Response To Consumer": datasets.Value("string"),
                "Timely Response": datasets.Value("string"),
                "Consumer Disputed": datasets.Value("string"),
                "Complaint ID": datasets.Value("string"),
            }
        )
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=features,
            homepage=_HOMEPAGE,
            license=_LICENSE,
            citation=_CITATION,
            task_templates=[
                TextClassification(text_column="Complaint Text", label_column="Product"),
                TextClassification(text_column="Complaint Text", label_column="Sub Product"),
                TextClassification(text_column="Complaint Text", label_column="Tags"),
            ],
        )

    def _split_generators(self, dl_manager):
        path = dl_manager.download_and_extract(_url)
        path = os.path.join(path, "complaints.csv")
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={"filepath": path},
            )
        ]

    def _generate_examples(self, filepath):
        """Generate consumer complaints examples."""
        with open(filepath, encoding="utf-8") as csv_file:
            csv_reader = csv.reader(
                csv_file, quotechar='"', delimiter=",", quoting=csv.QUOTE_ALL, skipinitialspace=True
            )
            next(csv_reader)  # skip header row
            for id_, row in enumerate(csv_reader):
                (
                    date_received,
                    product,
                    sub_product,
                    issue,
                    sub_issue,
                    complaint_text,
                    company_public_response,
                    company,
                    state,
                    zip_code,
                    tags,
                    consumer_consent_provided,
                    submitted_via,
                    date_sent_to_company,
                    company_response_to_consumer,
                    timely_response,
                    consumer_disputed,
                    complaint_id,
                ) = row
                yield id_, {
                    "Date Received": date_received,
                    "Product": product,
                    "Sub Product": sub_product,
                    "Issue": issue,
                    "Sub Issue": sub_issue,
                    "Complaint Text": complaint_text,
                    "Company Public Response": company_public_response,
                    "Company": company,
                    "State": state,
                    "Zip Code": zip_code,
                    "Tags": tags,
                    "Consumer Consent Provided": consumer_consent_provided,
                    "Submitted via": submitted_via,
                    "Date Sent To Company": date_sent_to_company,
                    "Company Response To Consumer": company_response_to_consumer,
                    "Timely Response": timely_response,
                    "Consumer Disputed": consumer_disputed,
                    "Complaint ID": complaint_id,
                }
