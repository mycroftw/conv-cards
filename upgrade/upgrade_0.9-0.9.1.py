# Fix convention cards to add the signal ranking commands.

from argparse import ArgumentParser
from fileinput import FileInput
from pathlib import Path

TEXT_TO_CHECK = (  # lines to check against, if we find them, don't auto-fix.
    ' {*rank} commands',
    '\\newcommand{\\deattrank}',
    '\\newcommand{\\decourank}',
    '\\newcommand{\\desuirank}',
    '\\newcommand{\\prattrank}',
    '\\newcommand{\\prcourank}',
    '\\newcommand{\\prsuirank}',
)
TEXT_TO_ADD = (  # lines to add.
    '''% Two alternatives here:
%    1. uncomment the setboolean to check the box that is "primary signal", as the card suggests.
%    2. Do not uncomment any checkbox, but rank the entries by putting a single
%       character in each box with the {*rank} commands.
''',
    '\\newcommand{\\deattrank}{}\n',
    '\\newcommand{\\decourank}{}\n',
    '\\newcommand{\\desuirank}{}\n',
    '\\newcommand{\\prattrank}{}\n',
    '\\newcommand{\\prcourank}{}\n',
    '\\newcommand{\\prsuirank}{}\n',
)


def _process_file(file: Path):
    """process a tex file.  Check first to ensure it hasn't already been done."""

    text = Path(file).read_text()
    if '\\usepackage{acbl2022cc}' not in text:
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
            if '% Signals' in line:
                line = ''.join([line, TEXT_TO_ADD[0]])
            elif '\\setboolean{desui}{true}' in line:
                line = ''.join([line] + list(TEXT_TO_ADD[1:4]))
            elif '\\setboolean{prsui}{true}' in line:
                line = ''.join([line] + list(TEXT_TO_ADD[4:]))
            print(line, end='')

    return 0


def do_fix(source: list):
    """for each entry in source, fix files or files in directories."""

    for filename in source:
        file = Path(filename)
        if not file.exists():
            print(f'Error: file {filename} does not exist, skipping.')
        elif file.is_file():
            _process_file(file)
        elif file.is_dir():
            for name in file.glob('**/*.tex'):
                _process_file(name)


if __name__ == "__main__":
    desc = 'Fix v0.9 convention cards to add signal ranking commands in v0.9.1.'
    epilog = ('If directories are targeted, all .tex files that '
              '\\usepackage{acbl2022cc} under that directory will be modified.')
    parser = ArgumentParser(description=desc, epilog=epilog)
    parser.add_argument('source', nargs='+',
                        help='file(s) or directory(s) to convert.')
    args = parser.parse_args()

    do_fix(args.source)
