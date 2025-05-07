from argparse import ArgumentParser
from typing import Optional

from huggingface_hub import HfApi

import datasets.config
from datasets.commands import BaseDatasetsCLICommand
from datasets.hub import convert_to_parquet


def _command_factory(args):
    return ConvertToParquetCommand(
        args.dataset_id,
        args.token,
        args.revision,
        args.trust_remote_code,
    )


class ConvertToParquetCommand(BaseDatasetsCLICommand):
    @staticmethod
    def register_subcommand(parser):
        parser: ArgumentParser = parser.add_parser("convert_to_parquet", help="Convert dataset to Parquet")
        parser.add_argument(
            "dataset_id", help="source dataset ID, e.g. USERNAME/DATASET_NAME or ORGANIZATION/DATASET_NAME"
        )
        parser.add_argument("--token", help="access token to the Hugging Face Hub (defaults to logged-in user's one)")
        parser.add_argument("--revision", help="source revision")
        parser.add_argument(
            "--trust_remote_code", action="store_true", help="whether to trust the code execution of the load script"
        )
        parser.add_argument(
            "--merge-pull-request",
            action="store_true",
            help="whether to automatically merge the pull request after conversion",
        )
        parser.set_defaults(func=_command_factory)

    def __init__(
        self,
        dataset_id: str,
        token: Optional[str],
        revision: Optional[str],
        trust_remote_code: bool,
    ):
        self._dataset_id = dataset_id
        self._token = token
        self._revision = revision
        self._trust_remote_code = trust_remote_code
        self._merge_pull_request = False

    def run(self) -> None:
        commit_info = convert_to_parquet(
            self._dataset_id, revision=self._revision, token=self._token, trust_remote_code=self._trust_remote_code
        )

        if self._merge_pull_request:
            api = HfApi(endpoint=datasets.config.HF_ENDPOINT, token=self._token)
            api.merge_pull_request(
                repo_id=self._dataset_id,
                discussion_num=int(commit_info.pr_num),
                token=self._token,
                repo_type="dataset",
            )
