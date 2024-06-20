# Fix convention cards to add the signal ranking commands.

from argparse import ArgumentParser
from pathlib import Path

from upgrade_tools import StandardUpgrader, AddInfo

TEXT_TO_CHECK = (  # lines to check against, if we find them, don't auto-fix.
    "renewcommand{\\usertextsize}",
)
TEXT_TO_ADD = (  # lines to add
    AddInfo(
        anchor="\\setboolean{serif}{false}",
        text="""
% it is sometimes very hard to read the small text on printed page.
% Uncomment one of these commands if you want to override the default
% (bigger if serif, normal size if not)
%\\renewcommand{\\usertextsize}{\\footnotesize}  % larger answer size
%\\renewcommand{\\usertextsize}{\\scriptsize}    % smaller answer size""",
    ),
)


if __name__ == "__main__":
    DESC = "Fix v0.9.1 convention cards to add usertextsize change option in v0.9.1."
    EPILOG = (
        "If directories are targeted, all .tex files that "
        "`\\usepackage{acbl2022cc` under that directory will be modified."
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
