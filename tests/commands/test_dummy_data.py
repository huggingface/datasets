import os
from collections import namedtuple

from datasets.commands.dummy_data import DummyDataCommand


DummyDataCommandArgs = namedtuple(
    "DummyDataCommandArgs",
    [
        "path_to_dataset",
        "auto_generate",
        "n_lines",
        "json_field",
        "xml_tag",
        "match_text_files",
        "keep_uncompressed",
        "cache_dir",
        "encoding",
    ],
    defaults=[False, 5, None, None, None, False, None, None],
)


class MockDummyDataCommand(DummyDataCommand):
    def _autogenerate_dummy_data(self, dataset_builder, mock_dl_manager, keep_uncompressed):
        mock_dl_manager.datasets_scripts_dir = os.path.abspath(os.path.join(self._path_to_dataset, os.pardir))
        return super()._autogenerate_dummy_data(dataset_builder, mock_dl_manager, keep_uncompressed)


def test_dummy_data_command(dataset_loading_script_dir, capfd):
    args = DummyDataCommandArgs(path_to_dataset=dataset_loading_script_dir, auto_generate=True)
    dummy_data_command = MockDummyDataCommand(*args)
    _ = capfd.readouterr()
    dummy_data_command.run()
    assert os.path.exists(os.path.join(dataset_loading_script_dir, "dummy", "0.0.0", "dummy_data.zip"))
    captured = capfd.readouterr()
    assert captured.out.startswith("Automatic dummy data generation succeeded for all configs of")
