# Fix convention cards to add the signal ranking commands.

from argparse import ArgumentParser
from pathlib import Path

from upgrade_tools import StandardUpgrader, AddInfo


TEXT_TO_CHECK = (  # lines to check against, if we find them, don't auto-fix.
    " {*rank} commands",
    "\\newcommand{\\deattrank}",
    "\\newcommand{\\decourank}",
    "\\newcommand{\\desuirank}",
    "\\newcommand{\\prattrank}",
    "\\newcommand{\\prcourank}",
    "\\newcommand{\\prsuirank}",
)
TEXT_TO_ADD = (  # lines to add.
    AddInfo(
        anchor="% Signals:",
        text="""% Two alternatives here:
%    1. uncomment the setboolean to check the box that is "primary signal", as the card suggests.
%    2. Do not uncomment any checkbox, but rank the entries by putting a single
%       character in each box with the {*rank} commands.""",
    ),
    AddInfo(
        anchor="\\setboolean{desui}{true}",
        text="\\newcommand{\\deattrank}{}\n"
        "\\newcommand{\\decourank}{}\n"
        "\\newcommand{\\desuirank}{}",
    ),
    AddInfo(
        anchor="\\setboolean{prsui}{true}",
        text="\\newcommand{\\prattrank}{}\n"
        "\\newcommand{\\prcourank}{}\n"
        "\\newcommand{\\prsuirank}{}",
    ),
)


if __name__ == "__main__":
    DESC = "Fix v0.9 convention cards to add signal ranking commands in v0.9.1."
    EPILOG = (
        "If directories are targeted, all .tex files that "
        "\\usepackage{acbl2022cc} under that directory will be modified."
    )
    parser = ArgumentParser(description=DESC, epilog=EPILOG)
    parser.add_argument("source", nargs="+", help="file(s) or directory(s) to convert.")
    args = parser.parse_args()

    upgrader = StandardUpgrader(
        check_tests=TEXT_TO_CHECK,
        add_lines=TEXT_TO_ADD,
    )
    for source in args.source:
        upgrader.process(Path(source))
