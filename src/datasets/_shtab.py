"""Fake shtab."""
from argparse import Action, ArgumentParser


FILE = None
DIRECTORY = DIR = None


class PrintCompletionAction(Action):
    """Print completion action."""

    def __call__(self, parser, namespace, values, option_string=None):
        """Warn when shtab is not installed.

        :param parser:
        :param namespace:
        :param values:
        :param option_string:
        """
        print("Please install shtab firstly!")
        parser.exit(0)


def add_argument_to(parser: ArgumentParser, *args, **kwargs):
    """Add completion argument to parser.

    :param parser:
    :type parser: ArgumentParser
    :param args:
    :param kwargs:
    """
    Action.complete = None  # type: ignore
    parser.add_argument(
        "--print-completion",
        choices=["bash", "zsh", "tcsh"],
        action=PrintCompletionAction,
        help="print shell completion script",
    )
    return parser
