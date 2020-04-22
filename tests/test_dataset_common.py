# coding=utf-8
# Copyright 2019 HuggingFace Inc.
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


class DatasetTesterMixin:

    Dataset = None
    Config = None

    # similar to model_classes in `transformers`
    config_names = ()
    mock_folder_structure_fn = None

    class MockDataLoaderManager(object):

        # this can actually be defined here and is the data_dir used to
        data_dir = None

        def __init__(self, mock_folder_structure_fn, config_name):
            self.config_name = config_name
            self.mock_folder_structure_fn = mock_folder_structure_fn
            # save the created mock data files
            # Here a check that the mock_folder_structure_fn has the wanted signutare,
            # which is def mock_folder_structure_fn(config) -> path_to_created_folder_structure

        def download_and_extract(self, *args):
            # this function has to be in the manager under this name to work
            return self.mock_folder_structure_fn(self.config_name, self.data_dir)

    def test_load_dataset(self):

        for config_name in self.config_names:
            # create config and dataset
            config = self.Config(config_name)
            dataset = self.Dataset(config=config)

            # create mock data loader manager with test specific mock_folder_strucutre_fn
            mock_dl_manager = DatasetTesterMixin.MockDataLoaderManager(self.mock_folder_structure_fn, config_name)

            # use the mock_dl_manager to create mock data and get split generators from there
            split_generators = dataset._split_generators(mock_dl_manager)

            # from here the rest is easy to test since we have working split generators
