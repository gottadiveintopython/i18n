dummy_fontfinder = {'zh': 'zh font', 'en': 'en font', }.__getitem__


def test_install():
    from kivy.lang import global_idmap
    from kivy_garden.i18n.localizer import KXLocalizer
    loc = KXLocalizer()
    loc.install()
    assert global_idmap['l'] is loc
    loc.install(name='l2')
    assert global_idmap['l2'] is loc


def test_DictBasedTranslator():
    from kivy_garden.i18n.localizer import KXLocalizer, DictBasedTranslator
    translator = DictBasedTranslator({
        'greeting': {
            'zh': '早安',
            'en': 'morning',
        },
        'tiger': {
            'zh': '老虎',
            'en': 'Tiger',
        },
    })
    loc = KXLocalizer(translator=translator)
    loc.lang = 'zh'
    assert loc._("greeting") == '早安'
    assert loc._("tiger") == '老虎'
    assert loc._("unknown msgid") == 'unknown msgid'
    loc.lang = 'en'
    assert loc._("greeting") == 'morning'
    assert loc._("tiger") == 'Tiger'
    assert loc._("unknown msgid") == 'unknown msgid'
    loc.lang = 'unknown lang'
    assert loc._("greeting") == 'greeting'
    assert loc._("tiger") == 'tiger'
    assert loc._("unknown msgid") == 'unknown msgid'
    assert loc.font_name == 'Roboto'


def test_GettextTranslator():
    from pathlib import PurePath
    from kivy_garden.i18n.localizer import KXLocalizer, GettextTranslator
    translator = GettextTranslator(
        'test_localizer',
        PurePath(__file__).parent / 'locales',
    )
    loc = KXLocalizer(translator=translator)
    loc.lang = 'zh'
    assert loc._("greeting") == '早安'
    assert loc._("tiger") == '老虎'
    assert loc._("unknown msgid") == 'unknown msgid'
    loc.lang = 'en'
    assert loc._("greeting") == 'morning'
    assert loc._("tiger") == 'Tiger'
    assert loc._("unknown msgid") == 'unknown msgid'


def test_binding():
    from textwrap import dedent
    from kivy.lang import Builder
    from kivy_garden.i18n.localizer import KXLocalizer, DictBasedTranslator

    translator = DictBasedTranslator({
        'greeting': {
            'zh': '早安',
            'en': 'morning',
        },
    })
    loc = KXLocalizer(fontfinder=dummy_fontfinder, translator=translator)
    loc.install()
    label = Builder.load_string(dedent("""
        Label:
            font_name: l.font_name
            text: l._("greeting")
        """))
    loc.lang = 'zh'
    assert label.text == '早安'
    assert label.font_name == 'zh font'
    loc.lang = 'en'
    assert label.text == 'morning'
    assert label.font_name == 'en font'
