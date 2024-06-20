"""Tools to upgrade completed templates to fixes of original template."""

import shutil
from abc import abstractmethod, ABC
from operator import attrgetter
from pathlib import Path
from typing import Optional, NamedTuple, Callable, List, Iterator


# Utility functions
def template_files(directory: Path = Path.cwd()) -> Iterator[Path]:
    """Returns each template in turn.  Convenience function."""

    templates = []
    if not directory.exists():
        print(f"{directory.name} could not be found, ignoring.")
    if directory.is_file():
        if ".tex" in directory.suffixes:
            templates.append(directory)
        else:
            print(f"{directory.name} is not a LaTeX file, ignoring.")
    else:
        templates.extend(directory.glob("*.tex"))

    for template in templates:
        if "\\usepackage{acbl2022cc}" in template.read_text():
            yield template
        else:
            print(f"{template.name} is not an ACBL 2022 style template, ignoring.")


def read_template(template: Path, backup: bool = True) -> list:
    """Read a template.  Back it up to dir/backup first if requested."""
    if backup:
        template.parent.joinpath("backup").mkdir(exist_ok=True)
        shutil.copy2(template, template.parent.joinpath("backup"))
    with template.open(encoding="utf-8") as f:
        return f.readlines()


def write_template(template: Path, text: list) -> None:
    """Write a list of lines as a template file."""
    with template.open("w", encoding="utf=8") as f:
        f.writelines(text)


def find_in_file(template: list, match_text: str) -> Optional[int]:
    """Return the line number of first match, or None if not found.

    This is not a complete line match.
    """
    return next(
        (count for count, value in enumerate(template) if match_text in value), None
    )


class FoundInTemplateError(Exception):
    """Error because text was unexpectedly found/not found in the template."""


#  Add/delete/replace functions.  They all rely on a file opened by
# "read_template" as a (mutable) list of lines.
def add_text_before_line(template: list, text: str, line_no: int) -> None:
    """Add text to a template read as a list of lines before line X."""
    template.insert(line_no, text + "\n")


def add_text_after_line(template: list, text: str, line_no: int) -> None:
    """Add text to a template, after line X."""
    add_text_before_line(template, text, line_no + 1)


def add_text_before_text(template: list, text: str, match_text: str) -> bool:
    """Add text to a template, before the first line containing match_text.

    Does nothing if no match.
    """
    number = find_in_file(template, match_text)
    if number is not None:
        add_text_before_line(template, text, number)
    return number is not None


def add_text_after_text(template: list, text: str, match_text: str) -> bool:
    """Add text to a template, after the first line containing match_text."""
    number = find_in_file(template, match_text)
    if number is not None:
        add_text_after_line(template, text, number)
    return number is not None


def delete_lines_before_line(template: list, line_no: int, count: int = 1) -> None:
    """Delete count lines before line number in template."""
    del template[line_no - count : line_no]


def delete_lines(template: list, line_no: int, count: int = 1) -> None:
    """Delete count lines, starting with specified line number in template."""
    del template[line_no : line_no + count]


def delete_lines_before_text(template: list, match_text: str, count: int = 1) -> bool:
    """Delete lines before first match of text in template.

    Does nothing if no match.
    """
    number = find_in_file(template, match_text)
    if number is not None:
        delete_lines_before_line(template, number, count)
    return number is not None


def delete_lines_from_text(template: list, match_text: str, count: int = 1) -> bool:
    """Delete lines starting with line with first text match."""
    number = find_in_file(template, match_text)
    if number is not None:
        delete_lines(template, number, count)
    return number is not None


def replace_line(template: list, repl_text: str, line_no: int) -> None:
    """Replace a line in a file by line number."""
    template[line_no] = repl_text + "\n"


def replace_line_by_match(template: list, repl_text: str, match_text: str) -> bool:
    """Replace a line by text match.

    Replaces entire line - not just the matched text.  See "replace_text".
    """
    number = find_in_file(template, match_text)
    if number is not None:
        replace_line(template, repl_text, number)
    return number is not None


def replace_text(template, repl_text: str, match_text: str, replace_all: False) -> bool:
    """Replace text in file (first match or all).

    Note: if multiple matches on one line, "replace_all" will do all on that
    line (and all matches); first match will replace the first match on that
    line only.
    """
    number = find_in_file(template, match_text)
    count = 0
    while number is not None:
        if replace_all:
            template[number] = template[number].replace(match_text, repl_text)
            count = 1
        else:
            template[number] = template[number].replace(match_text, repl_text, 1)
            count += 1
            break
        number = find_in_file(template, match_text)
    return bool(count)


class AddInfo(NamedTuple):
    """Instructions for adding line(s) to a template.
    anchor: line_no or match_text
    before: bool
    text: to add
    """

    anchor: int | str
    before: bool = False
    text: str = ""


class DeleteInfo(NamedTuple):
    """Instructions for deleting lines from a template.
    anchor: line_no or match_text
    before: bool
    count: number of lines
    """

    anchor: int | str
    before: bool = False
    count: int = 1


class ReplaceLine(NamedTuple):
    """Information for replacing a line in a template.
    anchor: line_no or match_text (note - will replace entire line)
    text: to replace
    """

    anchor: int | str
    text: str = ""


class ReplaceText(NamedTuple):
    """Information for replacing text in a template.
    anchor: match_text
    text: to add
    all: for match_text, replace all matches
    """

    anchor: str
    text: str
    all: bool = False


class Upgrader(ABC):
    """Base class for upgrade scripts.  Many just stubs to fill out."""

    @abstractmethod
    def check_template(self, template: list) -> bool:
        """Check against "already done".  To be implemented by inheritor."""
        raise NotImplementedError

    @abstractmethod
    def add_lines(self, template: list) -> int:
        """Add the lines set up in the class to the template."""
        raise NotImplementedError

    @abstractmethod
    def remove_lines(self, template: list) -> int:
        """remove lines set up in class from the template."""
        raise NotImplementedError

    @abstractmethod
    def replace_lines(self, template: list) -> int:
        """replace lines."""
        raise NotImplementedError

    @abstractmethod
    def rewrite_text(self, template: list) -> int:
        """change text."""
        raise NotImplementedError

    @abstractmethod
    def process(self) -> int:
        """Process files."""
        raise NotImplementedError


class StandardUpgrader(Upgrader):
    """Do the "normal" thing for each function."""

    def __init__(
        self,
        check_tests: Optional[list[str]] = None,
        add_lines: Optional[list[AddInfo]] = None,
        delete_info: Optional[list[DeleteInfo]] = None,
        replace_lines: Optional[list[ReplaceLine]] = None,
        repl_text: Optional[list[ReplaceText]] = None,
    ):
        self.check_tests = check_tests or []
        self.add_instructions = add_lines or []
        self.delete_instructions = delete_info or []
        self.replace_instructions = replace_lines or []
        self.replace_text_instructions = repl_text or []

    def check_template(self, template: list) -> None:
        """Check against "already done".  Raises exception if found."""
        for test in self.check_tests:
            number = find_in_file(template, test)
            if number is not None:
                raise FoundInTemplateError(
                    f"WARNING: test text [{test}] found in template at line {number}."
                )

    def add_lines(self, template: list) -> int:
        """Add the lines set up in the class to the template."""
        count = 0

        # divide instructions into "int" type and "match" type.
        int_add_instructions = sorted(
            [x for x in self.add_instructions if isinstance(x.anchor, int)],
            key=attrgetter("anchor"),
            reverse=True,
        )
        text_add_instructions = [
            x for x in self.add_instructions if isinstance(x.anchor, str)
        ]

        for item in int_add_instructions:
            if item.before:
                add_text_before_line(template, item.text, item.anchor)
            else:
                add_text_after_line(template, item.text, item.anchor)
            count += 1

        for item in text_add_instructions:
            if item.before:
                count += add_text_before_text(template, item.text, item.anchor)
            else:
                count += add_text_after_text(template, item.text, item.anchor)

        return count

    def remove_lines(self, template: list) -> int:
        """remove lines set up in class from the template."""
        count = 0

        # divide instructions into "int" type and "match" type.
        int_instructions = sorted(
            [x for x in self.delete_instructions if isinstance(x.anchor, int)],
            key=attrgetter("anchor"),
            reverse=True,
        )
        text_instructions = [
            x for x in self.delete_instructions if isinstance(x.anchor, str)
        ]

        for item in int_instructions:
            if item.before:
                delete_lines_before_line(template, item.anchor, item.count)
            else:
                delete_lines(template, item.anchor, item.count)
            count += 1

        for item in text_instructions:
            if item.before:
                count += delete_lines_before_text(template, item.anchor, item.count)
            else:
                count += delete_lines_from_text(template, item.anchor, item.count)

        return count

    def replace_lines(self, template: list) -> int:
        """Replace entire lines in text."""

        count = 0

        # divide instructions into "int" type and "match" type.
        int_instructions = sorted(
            [x for x in self.replace_instructions if isinstance(x.anchor, int)],
            key=attrgetter("anchor"),
            reverse=True,
        )
        text_instructions = [
            x for x in self.replace_instructions if isinstance(x.anchor, str)
        ]

        for item in int_instructions:
            replace_line(template, item.text, item.anchor)
            count += 1

        for item in text_instructions:
            count += replace_line_by_match(template, item.text, item.anchor)

        return count

    def rewrite_text(self, template: list) -> int:
        """change text, or change lines."""
        count = 0

        for item in self.replace_text_instructions:
            count += replace_text(template, item.text, item.anchor, item.all)

        return count

    def process(self, templates: Path = Path.cwd(), fail_on_miss: bool = True) -> int:
        """Do the needful."""

        def _safe_run_function(
            fn: Callable[[List], int], text_: list, expected: int
        ) -> int:
            """Run a function, report/quit on failure to do everything asked."""
            count = fn(text_)
            if count != expected:
                warning = (
                    f"Function {fn.__name__} expected to do {expected} "
                    f"operations, actually did {count}."
                )
                print(warning)
                if fail_on_miss:
                    raise FoundInTemplateError(warning)
            return count

        ops_performed = 0
        for template in template_files(templates):
            print(f"Updating {template.name}")
            text = read_template(template)
            self.check_template(text)

            ops_performed += _safe_run_function(
                self.add_lines, text, len(self.add_instructions)
            )
            ops_performed += _safe_run_function(
                self.remove_lines, text, len(self.delete_instructions)
            )
            ops_performed += _safe_run_function(
                self.replace_lines, text, len(self.replace_instructions)
            )
            ops_performed += _safe_run_function(
                self.rewrite_text, text, len(self.replace_text_instructions)
            )
            write_template(template, text)

        return ops_performed
