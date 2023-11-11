import pytest
p = pytest.mark.parametrize
from pathlib import Path


@p("arg, outcome", [
    ("hoge.ttf", True),
    ("hoge.otf", True),
    ("hoge.ttc", True),
    ("hoge.jpg.ttf", True),
    ("hoge.jpg", False),
    ("hoge.ttf.jpg", False),
    ("fallback.ttf", False),
    ("fallback.jpg", False),
    ("hoge", False),
    ("", False),
])
def test_default_filter(arg, outcome):
    from kivy_garden.i18n.fontfinder import default_filter
    assert default_filter(Path(arg)) is outcome


def test_enum_pre_installed_fonts():
    from kivy_garden.i18n.fontfinder import enum_pre_installed_fonts
    font = next(enum_pre_installed_fonts(), None)
    if font is None:
        pytest.skip("No font was found on this system")
    else:
        assert isinstance(font, Path)


@pytest.fixture(scope='module')
def cjk_font():
    from kivy_garden.i18n.fontfinder import enum_pre_installed_fonts
    for font in enum_pre_installed_fonts():
        if 'CJK' in font.name:
            return font


class Test_can_render_text:
    @p("text", ["", "A", "AB", "AAB", ])
    def test_invalid_arg(self, text):
        from kivy_garden.i18n.fontfinder import can_render_text
        with pytest.raises(ValueError):
            can_render_text("Roboto", text)

    @p("text, outcome", [
        ("ABC", True),
        ("@ /", True),
        ("漢字한글そは", False),
        ("漢字한글そはABC", False),
    ])
    def test_roboto(self, text, outcome):
        from kivy_garden.i18n.fontfinder import can_render_text
        assert can_render_text("Roboto", text) is outcome

    @p("text, outcome", [
        ("ABC", True),
        ("@ /", True),
        ("漢字한글そは", True),
        ("漢字한글そはABC", True),
    ])
    def test_cjk(self, cjk_font, text, outcome):
        from kivy_garden.i18n.fontfinder import can_render_text
        if cjk_font is None:
            pytest.skip("No CJK font was found on this system.")
        else:
            assert can_render_text(cjk_font, text) is outcome


class Test_can_render_lang:
    @p("lang", "zh ko ja".split())
    def test_cjk(self, cjk_font, lang):
        from kivy_garden.i18n.fontfinder import can_render_lang
        if cjk_font is None:
            pytest.skip("No CJK font was found on this system.")
        assert can_render_lang(cjk_font, lang)
        assert not can_render_lang("Roboto", lang)


class Test_register_lang:
    @p("text", ["", "A", "AB", "AAB", ])
    def test_invalid_arg(self, text):
        from kivy_garden.i18n.fontfinder import register_lang
        with pytest.raises(ValueError):
            register_lang("xxx", text)

    def test_valid_arg(self):
        from kivy_garden.i18n.fontfinder import register_lang, DISCRIMINANTS
        register_lang("xxx", "ABCD")
        assert DISCRIMINANTS["xxx"] == "ABCD"
