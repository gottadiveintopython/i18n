import pytest


@pytest.fixture(scope='module')
def extract():
    from kivy_garden.i18n.utils import extract_msgids_from_string_literals as f
    return f


@pytest.mark.parametrize('input', [
    r'_("msgid")',
    r"_('msgid')",
    r'100 + _("msgid")',
    r"100 + _('msgid')",
    r'_("msgid") + 100',
    r"_('msgid') + 100",
])
def test_not_in_string_literal(extract, input):
    assert [] == list(extract(input))


@pytest.mark.parametrize('input', [
    r'''"_('msgid')"''',
    r"""'_("msgid")'""",
    r'''"100 + _('msgid')"''',
    r"""'100 + _("msgid")'""",
    r'''"_('msgid') + 100"''',
    r"""'_("msgid") + 100'""",
])
def test_in_string_literal(extract, input):
    assert ["msgid", ] == list(extract(input))


def test_mixed(extract):
    from textwrap import dedent
    py_source = dedent('''
        PYTHON_CODE = _("This shouldn't be extracted.")
        KV_CODE = """
        Label:
            text: _("Hello") + _('World') + l._("!")
        """
        ''')
    assert ["Hello", "World", "!", ] == list(extract(py_source))
