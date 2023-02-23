from datasets.utils.patching import _PatchedModuleObj, patch_submodule

from . import _test_patching


def test_patch_submodule():
    import os as original_os
    from os import path as original_path
    from os import rename as original_rename
    from os.path import dirname as original_dirname
    from os.path import join as original_join

    assert _test_patching.os is original_os
    assert _test_patching.path is original_path
    assert _test_patching.join is original_join

    assert _test_patching.renamed_os is original_os
    assert _test_patching.renamed_path is original_path
    assert _test_patching.renamed_join is original_join

    mock = "__test_patch_submodule_mock__"
    with patch_submodule(_test_patching, "os.path.join", mock):
        # Every way to access os.path.join must be patched, and the rest must stay untouched

        # check os.path.join
        assert isinstance(_test_patching.os, _PatchedModuleObj)
        assert isinstance(_test_patching.os.path, _PatchedModuleObj)
        assert _test_patching.os.path.join is mock

        # check path.join
        assert isinstance(_test_patching.path, _PatchedModuleObj)
        assert _test_patching.path.join is mock

        # check join
        assert _test_patching.join is mock

        # check that the other attributes are untouched
        assert _test_patching.os.rename is original_rename
        assert _test_patching.path.dirname is original_dirname
        assert _test_patching.os.path.dirname is original_dirname

        # Even renamed modules or objects must be patched

        # check renamed_os.path.join
        assert isinstance(_test_patching.renamed_os, _PatchedModuleObj)
        assert isinstance(_test_patching.renamed_os.path, _PatchedModuleObj)
        assert _test_patching.renamed_os.path.join is mock

        # check renamed_path.join
        assert isinstance(_test_patching.renamed_path, _PatchedModuleObj)
        assert _test_patching.renamed_path.join is mock

        # check renamed_join
        assert _test_patching.renamed_join is mock

        # check that the other attributes are untouched
        assert _test_patching.renamed_os.rename is original_rename
        assert _test_patching.renamed_path.dirname is original_dirname
        assert _test_patching.renamed_os.path.dirname is original_dirname

    # check that everthing is back to normal when the patch is over

    assert _test_patching.os is original_os
    assert _test_patching.path is original_path
    assert _test_patching.join is original_join

    assert _test_patching.renamed_os is original_os
    assert _test_patching.renamed_path is original_path
    assert _test_patching.renamed_join is original_join


def test_patch_submodule_builtin():
    assert _test_patching.open is open

    mock = "__test_patch_submodule_builtin_mock__"
    # _test_patching has "open" in its globals
    assert _test_patching.open is open
    with patch_submodule(_test_patching, "open", mock):
        assert _test_patching.open is mock

    # check that everthing is back to normal when the patch is over

    assert _test_patching.open is open


def test_patch_submodule_missing():
    # pandas.read_csv is not present in _test_patching
    mock = "__test_patch_submodule_missing_mock__"
    with patch_submodule(_test_patching, "pandas.read_csv", mock):
        pass


def test_patch_submodule_missing_builtin():
    # builtin should always be mocked even if they're not in the globals
    # in case they're loaded at one point
    mock = "__test_patch_submodule_missing_builtin_mock__"
    # _test_patching doesn't have "len" in its globals
    assert getattr(_test_patching, "len", None) is None
    with patch_submodule(_test_patching, "len", mock):
        assert _test_patching.len is mock
    assert _test_patching.len is len


def test_patch_submodule_start_and_stop():
    mock = "__test_patch_submodule_start_and_stop_mock__"
    patch = patch_submodule(_test_patching, "open", mock)
    assert _test_patching.open is open
    patch.start()
    assert _test_patching.open is mock
    patch.stop()
    assert _test_patching.open is open


def test_patch_submodule_successive():
    from os import rename as original_rename
    from os.path import dirname as original_dirname
    from os.path import join as original_join

    mock_join = "__test_patch_submodule_successive_join__"
    mock_dirname = "__test_patch_submodule_successive_dirname__"
    mock_rename = "__test_patch_submodule_successive_rename__"
    assert _test_patching.os.path.join is original_join
    assert _test_patching.os.path.dirname is original_dirname
    assert _test_patching.os.rename is original_rename

    with patch_submodule(_test_patching, "os.path.join", mock_join):
        with patch_submodule(_test_patching, "os.rename", mock_rename):
            with patch_submodule(_test_patching, "os.path.dirname", mock_dirname):
                assert _test_patching.os.path.join is mock_join
                assert _test_patching.os.path.dirname is mock_dirname
                assert _test_patching.os.rename is mock_rename

    # try another order
    with patch_submodule(_test_patching, "os.rename", mock_rename):
        with patch_submodule(_test_patching, "os.path.join", mock_join):
            with patch_submodule(_test_patching, "os.path.dirname", mock_dirname):
                assert _test_patching.os.path.join is mock_join
                assert _test_patching.os.path.dirname is mock_dirname
                assert _test_patching.os.rename is mock_rename

    assert _test_patching.os.path.join is original_join
    assert _test_patching.os.path.dirname is original_dirname
    assert _test_patching.os.rename is original_rename


def test_patch_submodule_doesnt_exist():
    mock = "__test_patch_submodule_doesnt_exist_mock__"
    with patch_submodule(_test_patching, "__module_that_doesn_exist__.__attribute_that_doesn_exist__", mock):
        pass
    with patch_submodule(_test_patching, "os.__attribute_that_doesn_exist__", mock):
        pass
