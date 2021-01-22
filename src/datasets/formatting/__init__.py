from typing import Union

from ..utils.file_utils import is_tf_available, is_torch_available
from .formatting import Formatter, NumpyFormatter, PandasFormatter, PythonFormatter, format, query


if is_torch_available():
    from .torch_formatter import TorchFormatter

if is_tf_available():
    from .tf_formatter import TFFormatter


def get_formatter(format_type: Union[None, str], **format_kwargs) -> Formatter:
    if format_type in [None, "python"]:
        return PythonFormatter(**format_kwargs)
    elif format_type in ["numpy", "np"]:
        return NumpyFormatter(**format_kwargs)
    elif format_type in ["pandas", "pd"]:
        return PandasFormatter(**format_kwargs)
    elif format_type in ["torch", "pytorch", "pt"]:
        if is_torch_available():
            return TorchFormatter(**format_kwargs)
        else:
            raise ValueError("PyTorch needs to be installed to be able to return PyTorch tensors.")
    elif format_type in ["tensorflow", "tf"]:
        if is_tf_available():
            return TFFormatter(**format_kwargs)
        else:
            raise ValueError("Tensorflow needs to be installed to be able to return Tensorflow tensors.")
    else:
        raise ValueError(
            "Return type should be None or selected in ['numpy', 'torch', 'tensorflow', 'pandas'], but got '{}'".format(
                format_type
            )
        )
