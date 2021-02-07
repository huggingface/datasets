import os
import sys

from .utils.logging import get_logger


logger = get_logger(__name__)

_PY_VERSION: str = sys.version.split()[0]

if int(_PY_VERSION.split(".")[0]) == 3 and int(_PY_VERSION.split(".")[1]) < 8:
    import importlib_metadata
else:
    import importlib.metadata as importlib_metadata


USE_TF = os.environ.get("USE_TF", "AUTO").upper()
USE_TORCH = os.environ.get("USE_TORCH", "AUTO").upper()

_torch_version = "N/A"
_torch_available = False
if USE_TORCH in ("1", "ON", "YES", "AUTO") and USE_TF not in ("1", "ON", "YES"):
    try:
        _torch_version = importlib_metadata.version("torch")
        _torch_available = True
        logger.info("PyTorch version {} available.".format(_torch_version))
    except importlib_metadata.PackageNotFoundError:
        pass
else:
    logger.info("Disabling PyTorch because USE_TF is set")

_tf_version = "N/A"
_tf_available = False
if USE_TF in ("1", "ON", "YES", "AUTO") and USE_TORCH not in ("1", "ON", "YES"):
    try:
        _tf_version = importlib_metadata.version("tensorflow")
        _tf_available = True
        logger.info("TensorFlow version {} available.".format(_tf_version))
    except importlib_metadata.PackageNotFoundError:
        pass
else:
    logger.info("Disabling Tensorflow because USE_TORCH is set")

USE_BEAM = os.environ.get("USE_BEAM", "AUTO").upper()
_beam_version = "N/A"
_beam_available = False
if USE_BEAM in ("1", "ON", "YES", "AUTO"):
    try:
        _beam_version = importlib_metadata.version("apache_beam")
        _beam_available = True
        logger.info("Apache Beam version {} available.".format(_beam_version))
    except importlib_metadata.PackageNotFoundError:
        pass
else:
    logger.info("Disabling Apache Beam because USE_BEAM is set to False")


USE_RAR = os.environ.get("USE_RAR", "AUTO").upper()
_rarfile_version = "N/A"
_rarfile_available = False
if USE_RAR in ("1", "ON", "YES", "AUTO"):
    try:
        _rarfile_version = importlib_metadata.version("apache_beam")
        _rarfile_available = True
        logger.info("rarfile available.")
    except importlib_metadata.PackageNotFoundError:
        pass
else:
    logger.info("Disabling rarfile because USE_RAR is set to False")


def is_torch_available():
    return _torch_available


def is_tf_available():
    return _tf_available


def is_beam_available():
    return _beam_available


def is_rarfile_available():
    return _rarfile_available
