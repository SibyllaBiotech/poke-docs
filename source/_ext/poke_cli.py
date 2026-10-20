"""Sphinx directive that documents the poke command line from its real argument parser.

``.. poke-cli-tables::`` renders the usage line, a table of the positional arguments, one
table per option group (flag, default, description) and the closing note of the help text,
all taken from ``poke.main.build_parser()`` of the installed package. The page therefore
always matches ``poke -h`` and never has to be edited by hand.
"""
import argparse

from docutils import nodes
from docutils.parsers.rst import Directive
from docutils.statemachine import StringList


def _flag_text(action):
    """`-o, --output PATH`: the flags of the option followed by its placeholder."""
    text = ", ".join(action.option_strings) if action.option_strings else action.dest
    metavar = action.metavar
    if isinstance(metavar, tuple):
        metavar = " ".join(metavar)
    if metavar:
        text += " " + metavar
    return text


def _default_text(action):
    """The default as the user would type it; "off" for a switch, a dash when there is none."""
    default = action.default
    if isinstance(action, argparse._StoreTrueAction):
        return "off"
    if default is None or default is argparse.SUPPRESS or default == []:
        return "—"
    if str(default) == ".":
        return "current directory"
    if isinstance(default, (list, tuple)):
        return " ".join(map(str, default))
    return str(default)


def _help_text(parser, action):
    """The help string with argparse placeholders such as %(default)s filled in."""
    text = action.help or ""
    if "%" in text:
        try:
            text = parser._get_formatter()._expand_help(action)
        except AttributeError:
            text = text % dict(vars(action), prog=parser.prog)
    text = " ".join(text.split())
    if text and not text.endswith("."):
        text += "."
    return text[:1].upper() + text[1:]


def _table(headers, rows):
    table = nodes.table(classes=["cli-table"])
    tgroup = nodes.tgroup(cols=len(headers))
    table += tgroup
    for _ in headers:
        tgroup += nodes.colspec(colwidth=1)
    thead = nodes.thead()
    tgroup += thead
    head_row = nodes.row()
    thead += head_row
    for header in headers:
        head_row += nodes.entry("", nodes.paragraph(text=header))
    tbody = nodes.tbody()
    tgroup += tbody
    for cells in rows:
        row = nodes.row()
        tbody += row
        for cell in cells:
            row += nodes.entry("", nodes.paragraph("", "", cell))
    return table


class PokeCliTables(Directive):
    """Usage line, positional arguments, one table per option group, closing note."""

    def run(self):
        import poke.main

        parser = poke.main.build_parser()
        # Rebuild the page when the parser's source changes (editable installs).
        self.state.document.settings.env.note_dependency(poke.main.__file__)

        out = [nodes.literal_block(text=parser.format_usage().strip(), language="text")]
        for group in parser._action_groups:
            actions = [a for a in group._group_actions if a.help is not argparse.SUPPRESS]
            if not actions:
                continue
            title = group.title[:1].upper() + group.title[1:]
            section = nodes.section(ids=[nodes.make_id(title)], names=[nodes.fully_normalize_name(title)])
            section += nodes.title(text=title)
            if group is parser._positionals:
                rows = [(nodes.literal(text=a.dest), nodes.Text(_help_text(parser, a))) for a in actions]
                section += _table(("Argument", "Description"), rows)
            else:
                rows = [(nodes.literal(text=_flag_text(a)), nodes.Text(_default_text(a)), nodes.Text(_help_text(parser, a)))
                        for a in actions]
                section += _table(("Flag", "Default", "Description"), rows)
            out.append(section)

        if parser.epilog:
            container = nodes.container()
            self.state.nested_parse(StringList([parser.epilog], source="poke --help epilog"), 0, container)
            out.extend(container.children)
        return out


def setup(app):
    app.add_directive("poke-cli-tables", PokeCliTables)
    return {"parallel_read_safe": True, "parallel_write_safe": True}
