#!/usr/bin/env python

""" This script will run in CI and make sure all new changes to datasets readme files have valid metadata yaml headers.

"""

from pathlib import Path
from subprocess import check_call, check_output
from typing import List

from pydantic import ValidationError

from datasets.utils.metadata_validator import DatasetMetadata


def get_changed_files(repo_path: Path) -> List[Path]:
    # check_call(["git", "fetch"], cwd=repo_path)
    diff_output = check_output(["git", "diff", "--name-only", "HEAD..origin/master"], cwd=repo_path)
    changed_files = [Path(repo_path, f) for f in diff_output.decode().splitlines()]
    return changed_files


if __name__ == "__main__":
    import logging
    from argparse import ArgumentParser

    logging.basicConfig(level=logging.DEBUG)

    ap = ArgumentParser()
    ap.add_argument("--repo_path", type=Path, default=Path.cwd())
    args = ap.parse_args()

    cwd = args.repo_path
    changed_files = get_changed_files(cwd)
    changed_readmes = [
        f for f in changed_files if f.exists() and f.name.lower() == "readme.md" and f.parent.parent.name == "datasets"
    ]

    failed: List[Path] = []
    for readme in changed_readmes:
        try:
            DatasetMetadata.from_readme(readme)
            logging.debug(f"✔️ Validated '{readme.absolute()}'")
        except ValidationError as e:
            failed.append(readme)
            logging.warning(f"❌ Failed to validate '{readme.absolute()}':\n{e}")

    if len(failed) > 0:
        logging.info(f"❌ Failed on {len(failed)} files.")
        exit(1)
    else:
        logging.info("All is well, keep up the good work 🤗!")
        exit(0)
