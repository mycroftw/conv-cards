"""Fix convention cards to add the second "Other Carding" text line."""

from argparse import ArgumentParser
from pathlib import Path

from upgrade_tools import StandardUpgrader, AddInfo, ReplaceText

TEXT_TO_CHECK = (  # lines to check against, if we find them, don't auto-fix.
    "\\newcommand{\\othercardingtextone}",
    "\\newcommand{\\othercardingtexttwo}",
)
TEXT_TO_ADD = (  # lines to add.
    AddInfo(
        anchor="\\newcommand{\\othercardingtext}",
        text="\\newcommand{\\othercardingtextone}{}",
        before=True,
    ),
)
TEXT_TO_REPLACE = (  # text to replace.  Done *after* add
    ReplaceText(
        anchor="\\newcommand{\\othercardingtext}",
        text="\\newcommand{\\othercardingtexttwo}",
    ),
)


if __name__ == "__main__":
    DESC = (
        "Fix v0.9.3 convention cards to make available the text line after "
        "'Other Carding' as well as the text line below 'Smith Echo'."
    )
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
        repl_text=TEXT_TO_REPLACE,
    )
    for source in args.source:
        upgrader.process(Path(source))
