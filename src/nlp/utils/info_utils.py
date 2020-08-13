import logging
import os
from hashlib import sha256
from typing import Optional


logger = logging.getLogger(__name__)


class ChecksumVerificationException(Exception):
    """Exceptions during checksums verifications of downloaded files."""


class UnexpectedDownloadedFile(ChecksumVerificationException):
    """Some downloaded files were not expected."""


class ExpectedMoreDownloadedFiles(ChecksumVerificationException):
    """Some files were supposed to be downloaded but were not."""


class NonMatchingChecksumError(ChecksumVerificationException):
    """The downloaded file checksum don't match the expected checksum."""


def verify_checksums(expected_checksums: Optional[dict], recorded_checksums: dict, verification_name=None):
    if expected_checksums is None:
        logger.info("Unable to verify checksums.")
        return
    if len(set(expected_checksums) - set(recorded_checksums)) > 0:
        raise ExpectedMoreDownloadedFiles(str(set(expected_checksums) - set(recorded_checksums)))
    if len(set(recorded_checksums) - set(expected_checksums)) > 0:
        raise UnexpectedDownloadedFile(str(set(recorded_checksums) - set(expected_checksums)))
    bad_urls = [url for url in expected_checksums if expected_checksums[url] != recorded_checksums[url]]
    for_verification_name = " for " + verification_name if verification_name is not None else ""
    if len(bad_urls) > 0:
        error_msg = "Checksums didn't match" + for_verification_name + ":\n"
        raise NonMatchingChecksumError(error_msg + str(bad_urls))
    logger.info("All the checksums matched successfully" + for_verification_name)


class SplitsVerificationException(Exception):
    """Exceptions during splis verifications"""


class UnexpectedSplits(SplitsVerificationException):
    """The expected splits of the downloaded file is missing."""


class ExpectedMoreSplits(SplitsVerificationException):
    """Some recorded splits are missing."""


class NonMatchingSplitsSizesError(SplitsVerificationException):
    """The splits sizes don't match the expected splits sizes."""


def verify_splits(expected_splits: Optional[dict], recorded_splits: dict):
    if expected_splits is None:
        logger.info("Unable to verify splits sizes.")
        return
    if len(set(expected_splits) - set(recorded_splits)) > 0:
        raise ExpectedMoreSplits(str(set(expected_splits) - set(recorded_splits)))
    if len(set(recorded_splits) - set(expected_splits)) > 0:
        raise UnexpectedSplits(str(set(recorded_splits) - set(expected_splits)))
    bad_splits = [
        {"expected": expected_splits[name], "recorded": recorded_splits[name]}
        for name in expected_splits
        if expected_splits[name].num_examples != recorded_splits[name].num_examples
    ]
    if len(bad_splits) > 0:
        raise NonMatchingSplitsSizesError(str(bad_splits))
    logger.info("All the splits matched successfully.")


def get_size_checksum_dict(path: str) -> dict:
    """Compute the file size and the sha256 checksum of a file"""
    m = sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            m.update(chunk)
    return {"num_bytes": os.path.getsize(path), "checksum": m.hexdigest()}
