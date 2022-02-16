import distutils.dir_util
import logging
import os
import re
import requests
import sys
from itertools import islice
from pathlib import Path
from typing import Dict, Optional, Set, Tuple

from dotenv import load_dotenv
from git import Repo
from tqdm.contrib.concurrent import thread_map


load_dotenv()
logger = logging.getLogger(__name__)
ROOT = Path()

# General environment variables accepted values for booleans
ENV_VARS_TRUE_VALUES = {"1", "ON", "YES", "TRUE"}
ENV_VARS_TRUE_AND_AUTO_VALUES = ENV_VARS_TRUE_VALUES.union({"AUTO"})

if os.environ.get("HF_USE_PROD", "AUTO") in ENV_VARS_TRUE_VALUES:
    HUB_ENDPOINT = "https://huggingface.co"
else:
    HUB_ENDPOINT = "https://moon-staging.huggingface.co"

HUB_CANONICAL_WHOAMI = HUB_ENDPOINT + "/api/whoami-v2"
HUB_CANONICAL_CREATE_URL = HUB_ENDPOINT + "/api/repos/create"
HUB_CANONICAL_INFO_URL = HUB_ENDPOINT + "/api/datasets/{dataset_name}"
HUB_CANONICAL_DATASET_GIT_URL = HUB_ENDPOINT.replace("https://", "https://user:{token}@") + "/datasets/{dataset_name}.git"
HUB_API_GH_TO_HF = HUB_ENDPOINT + "/api/gh-to-hf/{github_username}"
DATASETS_LIB_CATALOG_DIR_NAME = "datasets"
DATASETS_LIB_COMMIT_URL = "https://github.com/huggingface/datasets/commit/{hexsha}"
CANONICAL_DATASET_REPO_MAIN_BRANCH = "main"
HUB_DIR_NAME = "hub"


def hf_retrieve_author(author_name, author_email) -> Tuple[str, str]:
    # Some HF members have enabled email address privacy on GitHub
    # This is here just to be able to link the commits to their HF accounts
    if author_email.endswith("@users.noreply.github.com"):
        try:
            github_username = author_email[: -len("@users.noreply.github.com")].split("+", 1)[-1]
            response = requests.get(HUB_API_GH_TO_HF.format(github_username=github_username))
            author_email = response.json()["user"] + "@users.noreply.huggingface.co"
        except Exception:
            pass
    return author_name, author_email


class UnauthorizedError(ConnectionError):
    pass


class UpdateFailed(RuntimeError):
    pass


def src_canonical_dataset_path(datasets_lib_path: Path, dataset_name: str) -> Path:
    return datasets_lib_path / DATASETS_LIB_CATALOG_DIR_NAME / dataset_name


def canonical_dataset_path(dataset_name: str) -> Path:
    return ROOT / HUB_DIR_NAME / dataset_name


def canonical_dataset_git_url(dataset_name: str, token: str) -> str:
    return HUB_CANONICAL_DATASET_GIT_URL.format(dataset_name=dataset_name, token=token)


def canonical_dataset_info_url(dataset_name: str) -> str:
    return HUB_CANONICAL_INFO_URL.format(dataset_name=dataset_name)


def create_remote_repo(dataset_name: str, token: str):
    response = requests.post(
        HUB_CANONICAL_CREATE_URL,
        headers={"authorization": f"Bearer {token}"},
        json={
            "name": dataset_name,
            "canonical": True,
            "type": "dataset",
        },
    )
    response.raise_for_status()


def whoami(token: str) -> str:
    response = requests.get(HUB_CANONICAL_WHOAMI, headers={"authorization": f"Bearer {token}"})
    response.raise_for_status()
    user_info = response.json()
    return user_info


def check_authorizations(user_info: dict):
    if "trusted-committers" not in [org["name"] for org in user_info["orgs"] if org["type"] == "org"]:
        raise UnauthorizedError(
            f"User {user_info['name']} is not part of the 'trusted-committers' org: "
            "it can't push to canonical repositories"
        )


def apply_hacks_for_moon_landing(dataset_repo_path: Path):
    if (dataset_repo_path / "README.md").is_file():
        with (dataset_repo_path / "README.md").open("r") as f:
            readme_content = f.read()
        if readme_content.count("---\n") > 1:
            _, tags, content = readme_content.split("---\n", 2)
            tags = tags.replace("\nlicense:", "\nlicenses:").replace(".", "-").replace("$", "%")
            with (dataset_repo_path / "README.md").open("w") as f:
                f.write("---\n".join(["", tags, content]))


class update_main:
    def __init__(
        self,
        datasets_lib_path: str,
        commit_args: Tuple[str],
        token: str,
        deleted_files: Dict[str, Set[str]],
        tag_name: Optional[str] = None,
    ) -> None:
        self.datasets_lib_path = datasets_lib_path
        self.commit_args = commit_args
        self.token = token
        self.deleted_files = deleted_files  # dict dataset_name -> set of relative paths of the deleted files
        self.tag_name = tag_name

    def __call__(self, dataset_name: str) -> bool:
        try:
            create_remote_repo(dataset_name, self.token)
        except requests.exceptions.HTTPError as e:
            if "409 Client Error: Conflict for url:" not in repr(e):  # don't log if repo already exists
                logger.warning(f"[{dataset_name}] " + repr(e))
        if not canonical_dataset_path(dataset_name).is_dir():
            repo = Repo.clone_from(
                canonical_dataset_git_url(dataset_name, self.token), to_path=canonical_dataset_path(dataset_name)
            )
        else:
            repo = Repo(canonical_dataset_path(dataset_name))

        logs = []
        logs.append(repo.git.reset("--hard"))
        logs.append(repo.git.clean("-f", "-d"))
        logs.append(repo.git.checkout(CANONICAL_DATASET_REPO_MAIN_BRANCH))
        logs.append(repo.remote().pull())
        # Copy the changes and commit
        distutils.dir_util.copy_tree(
            str(src_canonical_dataset_path(datasets_lib_path, dataset_name)), str(canonical_dataset_path(dataset_name))
        )
        for filepath_to_delete in self.deleted_files.get(dataset_name, []):
            try:
                (canonical_dataset_path(dataset_name) / filepath_to_delete).unlink()
            except Exception as e:
                logger.warning(f"[{dataset_name}] Couldn't delete file at {filepath_to_delete}: {repr(e)}")
        apply_hacks_for_moon_landing(canonical_dataset_path(dataset_name))
        logs.append(repo.git.add("."))
        if "Changes to be committed:" in repo.git.status():
            logs.append(repo.git.commit(*self.commit_args))
        try:
            logs.append(repo.git.push())
            if self.tag_name:
                # If the dataset repository hasn't been tagged for this release yet,
                # it means that the new version of the datasets lib just got released.
                # In this case we have to tag the new commit with this release name
                logs.append(repo.git.tag(self.tag_name, f"-m Add tag from datasets {self.tag_name}"))
                logs.append(repo.git.push("--tags"))
        except Exception as e:
            logs.append(repr(e))
        if "Your branch is up to date with" not in repo.git.status():
            logs.append(repo.git.status())
            logs = "\n".join(str(log) for log in logs)
            logger.warning(f"[{dataset_name}] Push failed")
            logger.warning(f"[{dataset_name}] Git logs: \n{logs}")
            return False
        else:
            return True


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    token = os.environ["HF_TOKEN"]
    datasets_lib_path = Path(os.environ["DATASETS_LIB_PATH"]).expanduser().resolve()

    if Path(token).expanduser().is_file():
        with Path(token).expanduser().open("r") as f:
            token = f.read().strip()
    user_info = whoami(token)
    check_authorizations(user_info)

    datasets_lib_repo = Repo(datasets_lib_path)
    current_commit, prev_commit = list(islice(datasets_lib_repo.iter_commits(), 2))
    author_name, author_email = current_commit.author.name, current_commit.author.email
    author_name, author_email = hf_retrieve_author(author_name, author_email)
    commit_args = (f"-m {current_commit.message}",)
    commit_args += (f"-m Commit from {DATASETS_LIB_COMMIT_URL.format(hexsha=current_commit.hexsha)}",)
    commit_args += (f"--author={author_name} <{author_email}>",)

    for _tag in datasets_lib_repo.tags:
        # Add a new tag if this is a `datasets` release
        if _tag.commit == current_commit and re.match(r"^[0-9]+\.[0-9]+\.[0-9]+$", _tag.name):
            new_tag = _tag
            break
    else:
        new_tag = None

    changed_files_since_last_commit = [
        path
        for diff in datasets_lib_repo.index.diff(prev_commit)
        for path in [diff.a_path, diff.b_path]
        if path.startswith(DATASETS_LIB_CATALOG_DIR_NAME)
        and path.count("/") >= 2
    ]

    changed_datasets_names_since_last_commit = {path.split("/")[1] for path in changed_files_since_last_commit}
    # ignore json, csv etc.
    changed_datasets_names_since_last_commit = {
        dataset_name for dataset_name in changed_datasets_names_since_last_commit
        if (datasets_lib_path / DATASETS_LIB_CATALOG_DIR_NAME / dataset_name / (dataset_name + ".py")).is_file()
    }

    deleted_files = {dataset_name: set() for dataset_name in changed_datasets_names_since_last_commit}
    for path in changed_files_since_last_commit:
        _, dataset_name, rel_path = path.split("/", 2)
        if (
            dataset_name in changed_datasets_names_since_last_commit
            and not (datasets_lib_path / path).is_file()
        ):
            deleted_files[dataset_name].add(rel_path)

    dataset_names = sys.argv[1:]
    if dataset_names:
        if dataset_names[0] == "--all":
            dataset_names = sorted(
                d.name for d in (datasets_lib_path / DATASETS_LIB_CATALOG_DIR_NAME).glob("*")
                if d.is_dir() and (d / (d.name + ".py")).is_file()  # ignore json, csv etc.
            )
        if dataset_names[0] == "--auto":
            if new_tag:
                logger.info(
                    "All the datasets will be updated since --auto was used and "
                    f"this is a new release {new_tag.name} of the `datasets` library."
                )
                dataset_names = sorted(d.name for d in (ROOT / HUB_DIR_NAME).glob("*") if d.is_dir())
                dataset_names = sorted(
                    d.name for d in (datasets_lib_path / DATASETS_LIB_CATALOG_DIR_NAME).glob("*")
                    if d.is_dir() and (d / (d.name + ".py")).is_file()  # ignore json, csv etc.
                )
            else:
                logger.info(
                    "All the datasets that have been changed in the latest commit of `datasets` will be updated "
                    "since --auto was used."
                )
                dataset_names = sorted(changed_datasets_names_since_last_commit)
        if dataset_names:
            logger.info(
                f"Updating the '{CANONICAL_DATASET_REPO_MAIN_BRANCH}' branch of those datasets: {' '.join(dataset_names)}"
            )
            successes = thread_map(
                update_main(
                    datasets_lib_path=datasets_lib_path,
                    commit_args=commit_args,
                    token=token,
                    deleted_files=deleted_files,
                    tag_name=new_tag.name if new_tag else None,
                ),
                dataset_names,
            )
            datasets_with_errors = [dataset_name for success, dataset_name in zip(successes, dataset_names) if not success]
            if datasets_with_errors:
                raise UpdateFailed(
                    f"Those datasets couldn't be updated: {' '.join(datasets_with_errors)}\n"
                    "Please check the logs to see what went wrong.\n"
                    "Once you fixed the errors, you can re-run this script:\n\n"
                    f"\tpython update_main.py {' '.join(datasets_with_errors)}"
                )
        else:
            logger.info("No changes detected -- nothing to update !")
