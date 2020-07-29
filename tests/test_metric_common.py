# coding=utf-8
# Copyright 2020 HuggingFace Inc.
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

import logging
import tempfile

from absl.testing import parameterized

from nlp import DownloadConfig, GenerateMode, hf_api, load_metric

from .utils import aws, slow


logging.basicConfig(level=logging.INFO)


def get_aws_metric_names():
    api = hf_api.HfApi()
    # fetch all metric names
    metrics = [x.id for x in api.metric_list()]
    return [{"testcase_name": x, "metric_name": x} for x in metrics]


@parameterized.named_parameters(get_aws_metric_names())
@aws
class AWSMetricTest(parameterized.TestCase):
    metric_name = None

    @slow
    def test_load_real_metric(self, metric_name):
        with tempfile.TemporaryDirectory() as temp_data_dir:
            download_config = DownloadConfig()
            download_config.download_mode = GenerateMode.FORCE_REDOWNLOAD
            load_metric(metric_name, data_dir=temp_data_dir, download_config=download_config)
