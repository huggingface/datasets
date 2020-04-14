import os
import re
import shutil
from argparse import ArgumentParser, Namespace
from logging import getLogger

from nlp.commands import BaseTransformersCLICommand


def convert_command_factory(args: Namespace):
    """
    Factory function used to convert a model TF 1.0 checkpoint in a PyTorch checkpoint.
    :return: ServeCommand
    """
    return ConvertCommand(
        args.tfds_directory, args.nlp_directory
    )


class ConvertCommand(BaseTransformersCLICommand):
    @staticmethod
    def register_subcommand(parser: ArgumentParser):
        """
        Register this command to argparse so it's available for the transformer-cli
        :param parser: Root parser to register command-specific arguments
        :return:
        """
        train_parser = parser.add_parser(
            "convert",
            help="CLI tool to convert a (nlp) TensorFlow-Dataset in a HuggingFace-NLP dataset.",
        )
        train_parser.add_argument(
            "--tfds_directory", type=str, required=True, help="Path to the TensorFlow Datasets folder."
        )
        train_parser.add_argument(
            "--nlp_directory", type=str, required=True, help="Path to the HuggingFace NLP folder."
        )
        train_parser.set_defaults(func=convert_command_factory)

    def __init__(
        self,
        tfds_directory: str,
        nlp_directory: str,
        *args
    ):
        self._logger = getLogger("nlp-cli/converting")

        self._tfds_directory = tfds_directory
        self._nlp_directory = nlp_directory

    def run(self):
        abs_tfds_path = os.path.abspath(self._tfds_directory)
        abs_nlp_path = os.path.abspath(self._nlp_directory)
        self._logger.info("Converting datasets from %s to %s", abs_tfds_path, abs_nlp_path)

        utils_files = []
        imports_to_builder_map = {}
        for f_name in os.listdir(abs_tfds_path):
            self._logger.info("Looking at file %s", f_name)
            input_file = os.path.join(abs_tfds_path, f_name)
            output_file = os.path.join(abs_nlp_path, f_name)

            if not os.path.isfile(input_file) or '__init__' in f_name or '_test' in f_name or not '.py' in f_name:
                self._logger.info("Skipping file")
                continue

            with open(input_file, "r") as f:
                lines = f.readlines()

            out_lines = []
            is_builder = False
            tfds_imports = []
            for line in lines:
                out_line = line

                # Convert imports
                if 'import tensorflow.compat.v2 as tf' in out_line:
                    continue
                elif '@tfds.core' in out_line:
                    continue
                elif 'import tensorflow_datasets.public_api as tfds' in out_line:
                    out_line = 'import nlp\n'
                elif 'from absl import logging' in out_line:
                    out_line = 'import logging\n'
                else:
                    out_line = out_line.replace('tfds.core', 'nlp')
                    out_line = out_line.replace('tf.io.gfile.GFile', 'open')
                    out_line = out_line.replace('tf.', 'nlp.')
                    out_line = out_line.replace('tfds.features.Text()', 'nlp.string')
                    out_line = out_line.replace('The TensorFlow Datasets Authors',
                                                'The TensorFlow Datasets Authors and the HuggingFace NLP Authors')
                    out_line = out_line.replace('tfds.', 'nlp.')

                # Take care of saving utilities (to later move them together with main script)
                if 'tensorflow_datasets' in out_line:
                    match = re.match(r"from\stensorflow_datasets.*import\s([^\.\r\n]+)", out_line)
                    tfds_imports.extend(imp.strip() for imp in match.group(1).split(','))
                    out_line = 'from . import ' + match.group(1)

                # Check we have not forget anything
                assert not 'tf.' in out_line and not 'tfds.' in out_line and not 'tensorflow_datasets' in out_line, f"Error converting {out_line.strip()}"

                if "GeneratorBasedBuilder" in out_line or "BeamBasedBuilder" in out_line:
                    is_builder = True
                out_lines.append(out_line)

            if is_builder:
                # We create a new directory for each dataset
                dir_name = f_name.replace('.py', '')
                output_dir = os.path.join(abs_nlp_path, dir_name)
                output_file = os.path.join(output_dir, f_name)
                os.makedirs(output_dir, exist_ok=True)
                self._logger.info("Adding directory %s", output_dir)
                imports_to_builder_map.update(dict((imp, output_dir) for imp in tfds_imports))
            else:
                # Utilities will be moved at the end
                utils_files.append(output_file)

            with open(output_file, "w") as f:
                f.writelines(out_lines)
            self._logger.info("Converted in %s", output_file)

        for utils_file in utils_files:
            try:
                f_name = os.path.basename(utils_file)
                dest_folder = imports_to_builder_map[f_name.replace('.py', '')]
                self._logger.info("Moving %s to %s", utils_file, dest_folder)
                shutil.copy(utils_file, dest_folder)
            except KeyError:
                self._logger.error(f"Cannot find destination folder for {utils_file}. Please copy manually.")
