# coding=utf-8
# Copyright 2020 The HuggingFace NLP Authors and the TensorFlow Datasets Authors.
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

# Lint as: python3
r"""Script to call download_and_prepare on DatasetBuilder.

Standalone script to generate specific dataset(s). This can be
used if you want to separate download/generation of dataset from actual usage.

By default, the dataset is generated in the default location
(~/nlp), which the same as when calling `nlp.load()`.

Instructions:
```
python -m nlp.scripts.download_and_prepare \
    --datasets=cifar10
```

If you have your dataset defined outside of `nlp`, use
`--module_import="path.to.my.dataset_module"` to have your Python module
containing your `DatasetBuilder` definition imported.


"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import importlib
import os
import pdb
import time

from absl import app
from absl import flags
import logging
import tensorflow.compat.v2 as tf
import nlp

logger = logging.getLogger(__name__)

FLAGS = flags.FLAGS

DEFAULT_DATA_DIR = os.path.expanduser(os.path.join("~", "nlp"))

flags.DEFINE_string("datasets", "",
                                        "Comma separated list of datasets to build, defaults to all"
                                        "builders.")
flags.DEFINE_string("exclude_datasets", "",
                                        "Comma separated list of datasets to exclude,"
                                        "(no download, no prepare).")
flags.DEFINE_multi_string(
        "module_import", None,
        "Modules to import. Use this when your DatasetBuilder is defined outside "
        "of nlp.")
flags.DEFINE_integer(
        "builder_config_id", None,
        "If given 1 dataset with BUILDER_CONFIGS, id of config to build.")
flags.DEFINE_boolean(
        "experimental_latest_version", False,
        "Set to true to builder the latest version available, even if not default.")

flags.DEFINE_string("data_dir", DEFAULT_DATA_DIR, "Where to place the data.")
flags.DEFINE_string("download_dir", None, "Where to place downloads.")
flags.DEFINE_string("extract_dir", None, "Where to extract files.")
flags.DEFINE_string(
        "manual_dir", None,
        "Directory where dataset have manually been downloaded / extracted.")
flags.DEFINE_string("checksums_dir", None,
                                        "For external datasets, specify the location of the "
                                        "dataset checksums.")
default_compute_stats = nlp.download.ComputeStatsMode.AUTO
flags.DEFINE_enum(
        "compute_stats",
        default_compute_stats.value,
        [e.value for e in nlp.download.ComputeStatsMode],
        "Whether to compute or not the dynamic statistics.")
flags.DEFINE_integer(
        "max_examples_per_split", None,
        "optional max number of examples to write into each split (for testing).")

# Beam flags
flags.DEFINE_list(
        "beam_pipeline_options", [],
        "A (comma-separated) list of flags to pass to `PipelineOptions` when "
        "preparing with Apache Beam. Example: "
        "`--beam_pipeline_options=job_name=my-job,project=my-project`")


# Development flags
flags.DEFINE_boolean("register_checksums", False,
                                         "If True, store size and checksum of downloaded files.")

# Debug flags
flags.DEFINE_boolean("debug", False,
                                         "If True, will drop into debugger after data generation")
flags.DEFINE_boolean("debug_start", False,
                                         "If True, will drop into debugger on startup")
flags.DEFINE_boolean("sleep_start", False,
                                         "If True, will sleep on startup; useful for ssh")
flags.DEFINE_boolean("disable_tqdm", False, "If True, disable tqdm.")


def download_config():
    return nlp.download.DownloadConfig(
            extract_dir=FLAGS.extract_dir,
            manual_dir=FLAGS.manual_dir,
            compute_stats=FLAGS.compute_stats,
            # TODO(b/116270825): Add flag to force extraction / preparation.
            download_mode=nlp.download.GenerateMode.REUSE_DATASET_IF_EXISTS,
            max_examples_per_split=FLAGS.max_examples_per_split,
            register_checksums=FLAGS.register_checksums,
    )


def download_and_prepare(builder):
    """Generate data for a given dataset."""
    logger.info("download_and_prepare for dataset %s...", builder.info.full_name)

    dl_config = download_config()

    if isinstance(builder, nlp.BeamBasedBuilder):
        beam = nlp.lazy_imports.apache_beam
        # TODO(b/129149715): Restore compute stats. Currently skipped because not
        # beam supported.
        dl_config.compute_stats = nlp.download.ComputeStatsMode.SKIP
        dl_config.beam_options = beam.options.pipeline_options.PipelineOptions(
                flags=["--%s" % opt for opt in FLAGS.beam_pipeline_options])

    builder.download_and_prepare(
            download_dir=FLAGS.download_dir,
            download_config=dl_config,
    )
    print(str(builder.info.data))

    if FLAGS.debug:
        dataset = builder.as_dataset(split=nlp.Split.TRAIN)
        pdb.set_trace()
        del dataset


def import_modules(modules):
    for module in modules:
        importlib.import_module(module)


def main(_):
    if FLAGS.module_import:
        import_modules(FLAGS.module_import)

    if FLAGS.debug_start:
        pdb.set_trace()
    if FLAGS.sleep_start:
        time.sleep(60*60*3)

    if FLAGS.disable_tqdm:
        logger.info("Disabling tqdm.")
        nlp.disable_progress_bar()

    if FLAGS.checksums_dir:
        nlp.download.add_checksums_dir(FLAGS.checksums_dir)

    datasets_to_build = set(FLAGS.datasets and FLAGS.datasets.split(","))
    datasets_to_build -= set(FLAGS.exclude_datasets.split(","))
    version = "experimental_latest" if FLAGS.experimental_latest_version else None
    logger.info("Running download_and_prepare for datasets:\n%s",
                             "\n".join(datasets_to_build))
    logger.info('Version: "%s"', version)
    builders = {
            name: nlp.builder(name, data_dir=FLAGS.data_dir, version=version)
            for name in datasets_to_build
    }

    if FLAGS.builder_config_id is not None:
        # Requesting a single config of a single dataset
        if len(builders) > 1:
            raise ValueError(
                    "--builder_config_id can only be used when building a single dataset")
        builder = builders[list(builders.keys())[0]]
        if not builder.BUILDER_CONFIGS:
            raise ValueError(
                    "--builder_config_id can only be used with datasets with configs")
        config = builder.BUILDER_CONFIGS[FLAGS.builder_config_id]
        logger.info("Running download_and_prepare for config: %s", config.name)
        builder_for_config = nlp.builder(
                builder.name, data_dir=FLAGS.data_dir, config=config, version=version)
        download_and_prepare(builder_for_config)
    else:
        for name, builder in builders.items():
            if builder.BUILDER_CONFIGS and "/" not in name:
                # If builder has multiple configs, and no particular config was
                # requested, then compute all.
                for config in builder.BUILDER_CONFIGS:
                    builder_for_config = nlp.builder(
                            builder.name, data_dir=FLAGS.data_dir, config=config,
                            version=version)
                    download_and_prepare(builder_for_config)
            else:
                # If there is a slash in the name, then user requested a specific
                # dataset configuration.
                download_and_prepare(builder)


if __name__ == "__main__":
    tf.enable_v2_behavior()
    app.run(main)
