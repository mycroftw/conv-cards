"""Add section labels."""

from argparse import ArgumentParser
from pathlib import Path

from upgrade_tools import StandardUpgrader, AddInfo, ReplaceLine


check_tests = [
    "\\label{sec:Names}",
    "\\label{subsec:1NT_left}",
    "\\label{sec:Signals}",
]
add_lines = [
    AddInfo(
        anchor="% And now the card itself",
        text="\\label{sec:Names}",
        before=True,
    )
]
replace_lines = [
    ReplaceLine(text="\\label{subsec:Leads_NT}", anchor="% Leads vs. NT"),
    ReplaceLine(text="\\label{subsec:Leads_Suit}", anchor="% Leads vs suit"),
    ReplaceLine(text="\\label{sec:Leads_Suit}", anchor="% Leads"),
    ReplaceLine(text="\\label{sec:Signals}", anchor="% Signals"),
    ReplaceLine(text="\\label{sec:Carding}", anchor="% Carding"),
    ReplaceLine(text="\\label{sec:Slams}", anchor="% Slam conventions"),
    ReplaceLine(text="\\label{sec:vs_Preempts}", anchor="% vs. opening preempts"),
    ReplaceLine(text="\\label{sec:Preempts}", anchor="% Opening preempts"),
    ReplaceLine(text="\\label{sec:vs_TOX}", anchor="% vs. takeout double"),
    ReplaceLine(text="\\label{sec:Cuebid}", anchor="% Direct cuebid"),
    ReplaceLine(text="\\label{sec:NT_Defence}", anchor="% Defense vs. NT"),
    ReplaceLine(text="\\label{sec:Overcalls}", anchor="% Overcalls"),
    ReplaceLine(text="\\label{sec:NT_Overcall}", anchor="% NT overcalls"),
    ReplaceLine(text="\\label{sec:X}", anchor="% Doubles"),
    ReplaceLine(text="\\label{sec:misc}", anchor="% Bottom of card"),
    ReplaceLine(text="\\label{sec:2S}", anchor="% 2 Spades"),
    ReplaceLine(text="\\label{sec:2H}", anchor="% 2 Hearts"),
    ReplaceLine(text="\\label{sec:2D}", anchor="% 2 Diamonds\n"),
    ReplaceLine(text="\\label{sec:2C}", anchor="% 2 Clubs\n"),
    ReplaceLine(text="\\label{sec:3NT}", anchor="% 3NT"),
    ReplaceLine(text="\\label{sec:2NT}", anchor="% 2NT"),
    ReplaceLine(text="\\label{subsec:1NT_bottom}", anchor="% 1NT: Bottom"),
    ReplaceLine(text="\\label{subsec:1NT_right}", anchor="% 1NT: Second column"),
    ReplaceLine(text="\\label{subsec:1NT_left}", anchor="% 1NT: First column"),
    ReplaceLine(text="\\label{sec:1NT}", anchor="% 1NT: Top"),
    ReplaceLine(text="\\label{sec:1M}", anchor="% 1 Major"),
    ReplaceLine(text="\\label{sec:1D}", anchor="% 1 Diamond"),
    ReplaceLine(text="\\label{sec:1C}", anchor="% 1 Club"),
    ReplaceLine(text="\\label{sec:General_Approach}", anchor="% General approach"),
]


if __name__ == "__main__":
    DESC = "Fix v0.9.2 convention cards, change section head comments to \\labels"
    EPILOG = (
        "If directories are targeted, all .tex files that "
        "\\usepackage{acbl2022cc} under that directory will be modified."
    )
    parser = ArgumentParser(description=DESC, epilog=EPILOG)
    parser.add_argument("source", nargs="+", help="file(s) or directory(s) to convert.")
    args = parser.parse_args()

    upgrader = StandardUpgrader(
        check_tests=check_tests,
        add_lines=add_lines,
        replace_lines=replace_lines,
    )
    for source in args.source:
        upgrader.process(Path(source))
