from typing import List, Optional, Union

from ..utils.file_utils import is_tf_available, is_torch_available
from ..utils.logging import get_logger
from .formatting import CustomFormatter, Formatter, NumpyFormatter, PandasFormatter, PythonFormatter, format, query


logger = get_logger(__name__)

_FORMAT_TYPES = {}
_FORMAT_TYPES_ALIASES = {}
_FORMAT_TYPES_ALIASES_UNAVAILABLE = {}


def register_formatter(format_type: Union[None, str], aliases: Optional[List[str]] = None):
    aliases = aliases if aliases is not None else []

    def wrapper(formatter_cls: type) -> type:
        if format_type in _FORMAT_TYPES:
            logger.warning(
                f"Overwriting format type '{format_type}' ({_FORMAT_TYPES[format_type].__name__} -> {formatter_cls.__name__})"
            )
        _FORMAT_TYPES[format_type] = formatter_cls
        for alias in set(aliases + [format_type]):
            if alias in _FORMAT_TYPES_ALIASES:
                logger.warning(
                    f"Overwriting format type alias '{alias}' ({_FORMAT_TYPES_ALIASES[alias]} -> {format_type})"
                )
            _FORMAT_TYPES_ALIASES[alias] = format_type
        return formatter_cls

    return wrapper


def _register_unavailable_formatter(format_type: Union[None, str], aliases: Optional[List[str]] = None):
    aliases = aliases if aliases is not None else []

    def wrapper(unavailable_error: type) -> type:
        for alias in set(aliases + [format_type]):
            _FORMAT_TYPES_ALIASES_UNAVAILABLE[alias] = unavailable_error
        return unavailable_error

    return wrapper


register_formatter(None, aliases=["python"])(PythonFormatter)
register_formatter("numpy", aliases=["np"])(NumpyFormatter)
register_formatter("pandas", aliases=["pd"])(PandasFormatter)
register_formatter("custom")(CustomFormatter)

if is_torch_available():
    from .torch_formatter import TorchFormatter

    register_formatter("torch", aliases=["pt", "pytorch"])(TorchFormatter)
else:
    _torch_error = ValueError("PyTorch needs to be installed to be able to return PyTorch tensors.")
    _register_unavailable_formatter("torch", aliases=["pt", "pytorch"])(_torch_error)

if is_tf_available():
    from .tf_formatter import TFFormatter

    register_formatter("tensorflow", aliases=["tf"])(TFFormatter)
else:
    _tf_error = ValueError("Tensorflow needs to be installed to be able to return Tensorflow tensors.")
    _register_unavailable_formatter("tensorflow", aliases=["tf"])(_tf_error)


def get_formatter(format_type: Union[None, str], **format_kwargs) -> Formatter:
    if format_type in _FORMAT_TYPES_ALIASES:
        format_type = _FORMAT_TYPES_ALIASES[format_type]
    if format_type in _FORMAT_TYPES:
        return _FORMAT_TYPES[format_type](**format_kwargs)
    if format_type in _FORMAT_TYPES_ALIASES_UNAVAILABLE:
        raise _FORMAT_TYPES_ALIASES_UNAVAILABLE[format_type]
    else:
        raise ValueError(
            "Return type should be None or selected in ['numpy', 'torch', 'tensorflow', 'pandas'], but got '{}'".format(
                format_type
            )
        )
