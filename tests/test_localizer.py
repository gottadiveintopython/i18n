import pytest


def test_install():
    from kivy.lang import global_idmap
    from kivy_garden.i18n.localizer import Localizer
    loc = Localizer()
    loc.install(name='l')
    assert global_idmap['l'] is loc

    # name confliction
    with pytest.raises(ValueError):
        loc.install(name='l')

    loc.uninstall(name='l')


def test_MappingBasedTranslatorFactory():
    from kivy_garden.i18n.localizer import Localizer, MappingBasedTranslatorFactory
    factory = MappingBasedTranslatorFactory({
        'morning': {
            'ko': '안녕',
            'zh': '早安',
        },
        'tiger': {
            'zh': '老虎',
            'en': 'Tiger',
        },
    })
    loc = Localizer(translator_factory=factory)
    loc.lang = 'zh'
    assert loc._("morning") == '早安'
    assert loc._("tiger") == '老虎'
    loc.lang = 'ko'
    assert loc._("morning") == '안녕'
    assert loc._("tiger") == 'tiger'
    loc.lang = 'en'
    assert loc._("morning") == 'morning'
    assert loc._("tiger") == 'Tiger'


def test_GettextBasedTranslatorFactory():
    from pathlib import PurePath
    from kivy_garden.i18n.localizer import Localizer, GettextBasedTranslatorFactory
    factory = GettextBasedTranslatorFactory(
        'test_localizer',
        PurePath(__file__).parent / 'locales',
    )
    loc = Localizer(translator_factory=factory)
    loc.lang = 'zh'
    assert loc._("greeting") == '早安'
    assert loc._("tiger") == '老虎'
    assert loc._("unknown msgid") == 'unknown msgid'
    loc.lang = 'en'
    assert loc._("greeting") == 'morning'
    assert loc._("tiger") == 'Tiger'
    assert loc._("unknown msgid") == 'unknown msgid'


def test_kv_binding():
    from textwrap import dedent
    from kivy.lang import Builder
    from kivy_garden.i18n.localizer import Localizer, MappingBasedTranslatorFactory

    factory = MappingBasedTranslatorFactory({
        'greeting': {
            'zh': '早安',
            'en': 'morning',
        },
    })
    dummy_font_picker = {'zh': 'zh font', 'en': 'en font', }.__getitem__

    loc = Localizer(font_picker=dummy_font_picker, translator_factory=factory)
    loc.install(name='l')
    label = Builder.load_string(dedent("""
        Label:
            font_name: l.font_name
            text: l._("greeting")
        """))
    loc.uninstall(name='l')
    loc.lang = 'zh'
    assert label.text == '早安'
    assert label.font_name == 'zh font'
    loc.lang = 'en'
    assert label.text == 'morning'
    assert label.font_name == 'en font'
    label.font_name = 'Roboto'


@pytest.mark.parametrize("strict", [True, False])
def test_compile_translations(strict):
    import types
    from kivy_garden.i18n.localizer import MappingBasedTranslatorFactory
    _compile_translations = MappingBasedTranslatorFactory._compile_translations

    source = types.MappingProxyType({
        'greeting': {"ko": "안녕", "zh": "安安", },
        "apple": {"ko": "사과", "zh": "蘋果", },
    })
    assert _compile_translations(source, strict=strict) == {
        "ko": {"greeting": "안녕", "apple": "사과", },
        'zh': {"greeting": "安安", "apple": "蘋果", },
    }


@pytest.mark.parametrize("strict", [True, False])
def test_compile_incomplete_translations(strict):
    import types
    from contextlib import nullcontext
    from kivy_garden.i18n.localizer import MappingBasedTranslatorFactory
    _compile_translations = MappingBasedTranslatorFactory._compile_translations

    # The "apple" msgid is missing a "ko" translation.
    source = types.MappingProxyType({
        'greeting': {"ko": "안녕", "zh": "安安", },
        "apple": {"zh": "蘋果", },
    })
    with pytest.raises(ValueError) if strict else nullcontext():
        assert _compile_translations(source, strict=strict) == {
            "ko": {"greeting": "안녕", "apple": "apple", },
            'zh': {"greeting": "安安", "apple": "蘋果", },
        }
