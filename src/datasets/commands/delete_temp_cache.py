import os
import shutil
import tempfile
from argparse import ArgumentParser

from datasets import config
from datasets.commands import BaseDatasetsCLICommand


def delete_temp_cache_command_factory(_):
    return DeleteTempCacheCommand()


class DeleteTempCacheCommand(BaseDatasetsCLICommand):
    @staticmethod
    def register_subcommand(parser: ArgumentParser):
        download_parser = parser.add_parser("delete-temp-cache", help="Print relevant system environment info.")
        download_parser.set_defaults(func=delete_temp_cache_command_factory)

    def run(self):
        num_deleted = 0
        for name in os.listdir(tempfile.gettempdir()):
            path = os.path.join(tempfile.gettempdir(), name)
            if name.startswith(config.TEMP_CACHE_DIR_PREFIX) and os.path.isdir(path):
                shutil.rmtree(path)
                num_deleted += 1
        if num_deleted == 0:
            print("No temporary cache directories to delete.")
        else:
            print(f"Deleted {num_deleted} temporary cache" + "directories" if num_deleted > 1 else "directory" + ".")
