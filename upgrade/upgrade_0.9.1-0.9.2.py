# Fix convention cards to add the signal ranking commands.

from argparse import ArgumentParser
from fileinput import FileInput
from pathlib import Path

TEXT_TO_CHECK = (  # lines to check against, if we find them, don't auto-fix.
    'renewcommand{\\usertextsize}',
)
TEXT_TO_ADD = (  # lines to add
    '''
% it is sometimes very hard to read the small text on printed page.
% Uncomment one of these commands if you want to override the default
% (bigger if serif, normal size if not)
%\\renewcommand{\\usertextsize}{\\footnotesize}  % larger answer size
%\\renewcommand{\\usertextsize}{\\scriptsize}    % smaller answer size
''',
)


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
            if '\\setboolean{serif}{false}' in line:
                line = ''.join([line, TEXT_TO_ADD[0]])
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
