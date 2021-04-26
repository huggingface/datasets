#!/usr/bin/env python

""" This script will run in CI and make sure all new changes to datasets readme files have valid content present.
"""

from pathlib import Path
from subprocess import check_output
from typing import List

from datasets.utils.readme import validate_readme


def get_changed_files(repo_path: Path) -> List[Path]:
    diff_output = check_output(["git", "diff", "--name-only", "HEAD..origin/master"], cwd=repo_path)
    changed_files = [Path(repo_path, f) for f in diff_output.decode().splitlines()]
    return changed_files


if __name__ == "__main__":
    import logging
    from argparse import ArgumentParser

    logging.basicConfig(level=logging.DEBUG)

    ap = ArgumentParser()
    ap.add_argument("--repo_path", type=Path, default=Path.cwd())
    ap.add_argument("--check_all", action="store_true")
    args = ap.parse_args()

    repo_path: Path = args.repo_path
    if args.check_all:
        readmes = [dd / "README.md" for dd in (repo_path / "datasets").iterdir()]
    else:
        changed_files = get_changed_files(repo_path)
        readmes = [
            f
            for f in changed_files
            if f.exists() and f.name.lower() == "readme.md" and f.parent.parent.name == "datasets"
        ]

    failed: List[Path] = []
    for readme in sorted(readmes):
        try:
            DatasetMetadata.from_readme(readme)
            logging.debug(f"✅️ Validated '{readme.relative_to(repo_path)}'")
        except TypeError as e:
            failed.append(readme)
            logging.warning(f"❌ Failed to validate '{readme.relative_to(repo_path)}':\n{e}")
        except Exception as e:
            failed.append(readme)
            logging.warning(f"⁉️ Something unexpected happened on '{readme.relative_to(repo_path)}':\n{e}")

    if len(failed) > 0:
        logging.info(f"❌ Failed on {len(failed)} files.")
        exit(1)
    else:
        logging.info("All is well, keep up the good work 🤗!")
        exit(0)
