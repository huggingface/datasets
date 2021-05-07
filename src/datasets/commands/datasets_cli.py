#!/usr/bin/env python
from argparse import ArgumentParser

from datasets.commands.convert import ConvertCommand
from datasets.commands.dummy_data import DummyDataCommand
from datasets.commands.env import EnvironmentCommand
from datasets.commands.run_beam import RunBeamCommand
from datasets.commands.test import TestCommand
from datasets.utils.logging import set_verbosity_info


def main():
    parser = ArgumentParser("HuggingFace Datasets CLI tool", usage="datasets-cli <command> [<args>]")
    commands_parser = parser.add_subparsers(help="datasets-cli command helpers")
    set_verbosity_info()

    # Register commands
    ConvertCommand.register_subcommand(commands_parser)
    EnvironmentCommand.register_subcommand(commands_parser)
    TestCommand.register_subcommand(commands_parser)
    RunBeamCommand.register_subcommand(commands_parser)
    DummyDataCommand.register_subcommand(commands_parser)

    # Let's go
    args = parser.parse_args()

    if not hasattr(args, "func"):
        parser.print_help()
        exit(1)

    # Run
    service = args.func(args)
    service.run()


if __name__ == "__main__":
    main()
