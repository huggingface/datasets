# ruff: noqa: F401
# This is the module that test_patching.py uses to test patch_submodule()
import os
import os as renamed_os
from os import path
from os import path as renamed_path
from os.path import join
from os.path import join as renamed_join


open = open  # we just need to have a builtin inside this module to test it properly
