# Copyright 2023 The HuggingFace Team. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Extends `dill` to support pickling more types with more consistent pickle representation."""
import os
import sys
from importlib import import_module
from io import BytesIO
from types import CodeType

import dill
from packaging import version

from .. import config


class Pickler(dill.Pickler):
    dispatch = dill._dill.MetaCatchingDict(dill.Pickler.dispatch.copy())

    _delayed_module_dispatch = {}
    _reduce_subclasses_types = set()

    def save(self, obj, save_persistent_id=True):
        # Register delayed dispatchers when the base module has been imported
        modules = Pickler._delayed_module_dispatch & sys.modules.keys()
        for module in modules:
            attrs = Pickler._delayed_module_dispatch.pop(module)
            for attr, func, reduce_subclasses in attrs:
                *submodules, attr = attr.split(".")
                t = getattr(import_module(".".join(submodules)), attr)
                Pickler.dispatch[t] = func
                if reduce_subclasses:
                    Pickler._reduce_subclasses_types = (*Pickler._reduce_subclasses_types, t)

        # Check if the object is a subclass of a type that has a "reduce_subclasses=True" reducer
        obj_type = type(obj)
        # import pdb; pdb.set_trace()
        if (
            obj_type not in Pickler.dispatch
            and Pickler._reduce_subclasses_types
            and issubclass(obj_type, Pickler._reduce_subclasses_types)
        ):
            base_type = next(iter(t for t in obj_type.__mro__ if t in Pickler._reduce_subclasses_types))
            Pickler.dispatch[obj_type] = Pickler.dispatch[base_type]

        dill.Pickler.save(self, obj, save_persistent_id=save_persistent_id)

    # def _batch_setitems(self, items):
    #     # Ignore the order of keys in a dict
    #     try:
    #         # Faster, but fails for unorderable elements
    #         items = sorted(items)
    #     except Exception:  # TypeError, decimal.InvalidOperation, etc.
    #         from datasets.fingerprint import Hasher

    #         items = sorted(items, key=lambda x: Hasher.hash(x[0]))
    #     dill.Pickler._batch_setitems(self, items)

    def memoize(self, obj):
        # Don't memoize strings since two identical strings can have different Python ids
        if type(obj) != str:  # noqa: E721
            dill.Pickler.memoize(self, obj)


def pklregister(t, reduce_subclasses=False):
    """Register a custom reducer for a type."""

    def proxy(func):
        if isinstance(t, str):
            module = t.split(".", 1)[0]
            Pickler._delayed_module_dispatch.setdefault(module, []).append((t, func, reduce_subclasses))
        else:
            Pickler.dispatch[t] = func
            if reduce_subclasses:
                Pickler._reduce_subclasses_types = (*Pickler._reduce_subclasses_types, t)
        return func

    return proxy


def dump(obj, file):
    """Pickle an object to a file."""
    Pickler(file, recurse=True).dump(obj)


def dumps(obj):
    """Pickle an object to a string."""
    file = BytesIO()
    dump(obj, file)
    return file.getvalue()


if config.DILL_VERSION < version.parse("0.3.6"):

    def log(pickler, msg):
        dill._dill.log.info(msg)

elif config.DILL_VERSION.release[:3] in [version.parse("0.3.6").release, version.parse("0.3.7").release]:

    def log(pickler, msg):
        dill._dill.logger.trace(pickler, msg)


#####################
# Custom reducers
#####################


@pklregister("regex.Pattern")
def _save_regexPattern(pickler, obj):
    import regex  # type: ignore

    log(pickler, f"Re: {obj}")
    args = (obj.pattern, obj.flags)
    pickler.save_reduce(regex.compile, args, obj=obj)
    log(pickler, "# Re")


@pklregister("tiktoken.Encoding")
def _save_tiktokenEncoding(pickler, obj):
    import tiktoken  # type: ignore

    log(pickler, f"Enc: {obj}")
    args = (obj.name, obj._pat_str, obj._mergeable_ranks, obj._special_tokens)
    pickler.save_reduce(tiktoken.Encoding, args, obj=obj)
    log(pickler, "# Enc")


@pklregister("torch.Tensor")
def _save_torchTensor(pickler, obj):
    import torch  # type: ignore

    # `torch.from_numpy` is not picklable in `torch>=1.11.0`
    def create_torchTensor(np_array):
        return torch.from_numpy(np_array)

    log(pickler, f"To: {obj}")
    args = (obj.detach().cpu().numpy(),)
    pickler.save_reduce(create_torchTensor, args, obj=obj)
    log(pickler, "# To")


@pklregister("spacy.Language", reduce_subclasses=True)
def _save_spacyLanguage(pickler, obj):
    import spacy  # type: ignore

    def create_spacyLanguage(config, bytes):
        lang_cls = spacy.util.get_lang_class(config["nlp"]["lang"])
        lang_inst = lang_cls.from_config(config)
        return lang_inst.from_bytes(bytes)

    log(pickler, f"Sp: {obj}")
    args = (obj.config, obj.to_bytes())
    pickler.save_reduce(create_spacyLanguage, args, obj=obj)
    log(pickler, "# Sp")


@pklregister("transformers.PreTrainedTokenizerBase", reduce_subclasses=True)
def _save_transformersPreTrainedTokenizerBase(pickler, obj):
    log(pickler, f"Tok: {obj}")
    state = obj.__getstate__()
    if "cache" in state and isinstance(state["cache"], dict):
        state["cache"] = {}
    pickler.save_reduce(type(obj), (), state=state, obj=obj)
    log(pickler, "# Tok")


@pklregister(set)
def _save_set(pickler, obj):
    log(pickler, f"Se: {obj}")
    try:
        # Faster, but fails for unorderable elements
        args = (sorted(obj),)
    except Exception:  # TypeError, decimal.InvalidOperation, etc.
        from datasets.fingerprint import Hasher

        args = (sorted(obj, key=Hasher.hash),)

    pickler.save_reduce(set, args, obj=obj)
    log(pickler, "# Se")


#####################
# Code object reducer
#####################

if config.DILL_VERSION < version.parse("0.3.6"):

    @pklregister(CodeType)
    def _save_code(pickler, obj):
        """
        From dill._dill.save_code
        This is a modified version that removes the origin (filename + line no.)
        of functions created in notebooks or shells for example.
        """
        dill._dill.log.info(f"Co: {obj}")
        # The filename of a function is the .py file where it is defined.
        # Filenames of functions created in notebooks or shells start with '<'
        # ex: <ipython-input-13-9ed2afe61d25> for ipython, and <stdin> for shell
        # Filenames of functions created in ipykernel the filename
        # look like f"{tempdir}/ipykernel_{id1}/{id2}.py"
        # Moreover lambda functions have a special name: '<lambda>'
        # ex: (lambda x: x).__code__.co_name == "<lambda>"  # True
        #
        # For the hashing mechanism we ignore where the function has been defined
        # More specifically:
        # - we ignore the filename of special functions (filename starts with '<')
        # - we always ignore the line number
        # - we only use the base name of the file instead of the whole path,
        # to be robust in case a script is moved for example.
        #
        # Only those two lines are different from the original implementation:
        co_filename = (
            ""
            if obj.co_filename.startswith("<")
            or (
                len(obj.co_filename.split(os.path.sep)) > 1
                and obj.co_filename.split(os.path.sep)[-2].startswith("ipykernel_")
            )
            or obj.co_name == "<lambda>"
            else os.path.basename(obj.co_filename)
        )
        co_firstlineno = 1
        # The rest is the same as in the original dill implementation
        if dill._dill.PY3:
            if hasattr(obj, "co_posonlyargcount"):
                args = (
                    obj.co_argcount,
                    obj.co_posonlyargcount,
                    obj.co_kwonlyargcount,
                    obj.co_nlocals,
                    obj.co_stacksize,
                    obj.co_flags,
                    obj.co_code,
                    obj.co_consts,
                    obj.co_names,
                    obj.co_varnames,
                    co_filename,
                    obj.co_name,
                    co_firstlineno,
                    obj.co_lnotab,
                    obj.co_freevars,
                    obj.co_cellvars,
                )
            else:
                args = (
                    obj.co_argcount,
                    obj.co_kwonlyargcount,
                    obj.co_nlocals,
                    obj.co_stacksize,
                    obj.co_flags,
                    obj.co_code,
                    obj.co_consts,
                    obj.co_names,
                    obj.co_varnames,
                    co_filename,
                    obj.co_name,
                    co_firstlineno,
                    obj.co_lnotab,
                    obj.co_freevars,
                    obj.co_cellvars,
                )
        else:
            args = (
                obj.co_argcount,
                obj.co_nlocals,
                obj.co_stacksize,
                obj.co_flags,
                obj.co_code,
                obj.co_consts,
                obj.co_names,
                obj.co_varnames,
                co_filename,
                obj.co_name,
                co_firstlineno,
                obj.co_lnotab,
                obj.co_freevars,
                obj.co_cellvars,
            )
        pickler.save_reduce(CodeType, args, obj=obj)
        dill._dill.log.info("# Co")
        return

elif config.DILL_VERSION.release[:3] in [version.parse("0.3.6").release, version.parse("0.3.7").release]:
    # From: https://github.com/uqfoundation/dill/blob/dill-0.3.6/dill/_dill.py#L1104
    @pklregister(CodeType)
    def save_code(pickler, obj):
        dill._dill.logger.trace(pickler, "Co: %s", obj)

        ############################################################################################################
        # Modification here for huggingface/datasets
        # The filename of a function is the .py file where it is defined.
        # Filenames of functions created in notebooks or shells start with '<'
        # ex: <ipython-input-13-9ed2afe61d25> for ipython, and <stdin> for shell
        # Filenames of functions created in ipykernel the filename
        # look like f"{tempdir}/ipykernel_{id1}/{id2}.py"
        # Moreover lambda functions have a special name: '<lambda>'
        # ex: (lambda x: x).__code__.co_name == "<lambda>"  # True
        #
        # For the hashing mechanism we ignore where the function has been defined
        # More specifically:
        # - we ignore the filename of special functions (filename starts with '<')
        # - we always ignore the line number
        # - we only use the base name of the file instead of the whole path,
        # to be robust in case a script is moved for example.
        #
        # Only those two lines are different from the original implementation:
        co_filename = (
            ""
            if obj.co_filename.startswith("<")
            or (
                len(obj.co_filename.split(os.path.sep)) > 1
                and obj.co_filename.split(os.path.sep)[-2].startswith("ipykernel_")
            )
            or obj.co_name == "<lambda>"
            else os.path.basename(obj.co_filename)
        )
        co_firstlineno = 1
        # The rest is the same as in the original dill implementation, except for the replacements:
        # - obj.co_filename => co_filename
        # - obj.co_firstlineno => co_firstlineno
        ############################################################################################################

        if hasattr(obj, "co_endlinetable"):  # python 3.11a (20 args)
            args = (
                obj.co_lnotab,  # for < python 3.10 [not counted in args]
                obj.co_argcount,
                obj.co_posonlyargcount,
                obj.co_kwonlyargcount,
                obj.co_nlocals,
                obj.co_stacksize,
                obj.co_flags,
                obj.co_code,
                obj.co_consts,
                obj.co_names,
                obj.co_varnames,
                co_filename,  # Modification for huggingface/datasets ############################################
                obj.co_name,
                obj.co_qualname,
                co_firstlineno,  # Modification for huggingface/datasets #########################################
                obj.co_linetable,
                obj.co_endlinetable,
                obj.co_columntable,
                obj.co_exceptiontable,
                obj.co_freevars,
                obj.co_cellvars,
            )
        elif hasattr(obj, "co_exceptiontable"):  # python 3.11 (18 args)
            args = (
                obj.co_lnotab,  # for < python 3.10 [not counted in args]
                obj.co_argcount,
                obj.co_posonlyargcount,
                obj.co_kwonlyargcount,
                obj.co_nlocals,
                obj.co_stacksize,
                obj.co_flags,
                obj.co_code,
                obj.co_consts,
                obj.co_names,
                obj.co_varnames,
                co_filename,  # Modification for huggingface/datasets ############################################
                obj.co_name,
                obj.co_qualname,
                co_firstlineno,  # Modification for huggingface/datasets #########################################
                obj.co_linetable,
                obj.co_exceptiontable,
                obj.co_freevars,
                obj.co_cellvars,
            )
        elif hasattr(obj, "co_linetable"):  # python 3.10 (16 args)
            args = (
                obj.co_lnotab,  # for < python 3.10 [not counted in args]
                obj.co_argcount,
                obj.co_posonlyargcount,
                obj.co_kwonlyargcount,
                obj.co_nlocals,
                obj.co_stacksize,
                obj.co_flags,
                obj.co_code,
                obj.co_consts,
                obj.co_names,
                obj.co_varnames,
                co_filename,  # Modification for huggingface/datasets ############################################
                obj.co_name,
                co_firstlineno,  # Modification for huggingface/datasets #########################################
                obj.co_linetable,
                obj.co_freevars,
                obj.co_cellvars,
            )
        elif hasattr(obj, "co_posonlyargcount"):  # python 3.8 (16 args)
            args = (
                obj.co_argcount,
                obj.co_posonlyargcount,
                obj.co_kwonlyargcount,
                obj.co_nlocals,
                obj.co_stacksize,
                obj.co_flags,
                obj.co_code,
                obj.co_consts,
                obj.co_names,
                obj.co_varnames,
                co_filename,  # Modification for huggingface/datasets ############################################
                obj.co_name,
                co_firstlineno,  # Modification for huggingface/datasets #########################################
                obj.co_lnotab,
                obj.co_freevars,
                obj.co_cellvars,
            )
        else:  # python 3.7 (15 args)
            args = (
                obj.co_argcount,
                obj.co_kwonlyargcount,
                obj.co_nlocals,
                obj.co_stacksize,
                obj.co_flags,
                obj.co_code,
                obj.co_consts,
                obj.co_names,
                obj.co_varnames,
                co_filename,  # Modification for huggingface/datasets ############################################
                obj.co_name,
                co_firstlineno,  # Modification for huggingface/datasets #########################################
                obj.co_lnotab,
                obj.co_freevars,
                obj.co_cellvars,
            )

        pickler.save_reduce(dill._dill._create_code, args, obj=obj)
        dill._dill.logger.trace(pickler, "# Co")
        return
