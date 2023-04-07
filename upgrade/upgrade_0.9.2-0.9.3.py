# Fix convention cards to add the signal ranking commands.

from argparse import ArgumentParser
from fileinput import FileInput
from pathlib import Path

TEXT_TO_CHECK = (  # lines to check against, if we find them, don't auto-fix.
    '\\pagestyle{empty}',
    '\\usepackage[left=0mm, right=4mm, top=20mm]{geometry};',
)
TEXT_TO_ADD = (  # lines to add
    '\\pagestyle{empty}',
)
TEXT_TO_CHANGE = {
    '\\usepackage[left=0mm, right=5mm, top=20mm]{geometry};':
        '\\usepackage[left=0mm, right=4mm, top=20mm]{geometry};'
}


def _process_file(file: Path):
    """process a tex file.  Check first to ensure it hasn't already been done."""

    text = Path(file).read_text()
    if '\\usepackage{acbl2022cc' not in text:
        print(f'Error: {file} is not a ACBL 2022 template, skipping.')
        return 1

    # confirm that the changes haven't already been made
    for line in TEXT_TO_CHECK:
        if line in text:
            print(f'Warning: {file} contains text to be added: \n{line}\n.'
                  f'Skipping this file, please fix manually.')
            return 2

    # do the changes.
    print(f'fixing {file}...')
    with FileInput(files=[file], inplace=True, backup='.bak') as f:
        for line in f:
            if '\\documentclass[12 pt, draft]{article}' in line:
                line = ''.join([line, TEXT_TO_ADD[0]])
            for find_, replace_ in TEXT_TO_CHANGE.items():
                if find_ in line:
                    line = replace_
            print(line, end='')

    return 0


def do_fix(source: list):
    """for each entry in source, fix files or files in directories."""

    for filename in source:
        f = Path(filename)
        if not f.exists():
            print(f'Error: file {filename} does not exist, skipping.')
        elif f.is_file():
            _process_file(f)
        elif f.is_dir():
            for name in f.glob('**/*.tex'):
                _process_file(name)


if __name__ == "__main__":
    desc = (
        'Fix v0.9.1 convention cards to add '
        'usertextsize change option in v0.9.1.'
    )
    epilog = (
        'If directories are targeted, all .tex files that '
        '`\\usepackage{acbl2022cc` under that directory will be modified.'
    )
    parser = ArgumentParser(description=desc, epilog=epilog)
    parser.add_argument('source', nargs='+',
                        help='file(s) or directory(s) to convert.')
    args = parser.parse_args()

    do_fix(args.source)
