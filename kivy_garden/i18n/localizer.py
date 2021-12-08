__all__ = ('KXLocalizer', 'GettextTranslator', 'DictBasedTranslator', )
from typing import Callable, Dict

from kivy.properties import StringProperty, ObjectProperty
from kivy.event import EventDispatcher
from kivy.uix.label import Label

# type hints
Lang = str
Msgid = str
Fontname = str
FuncTranslate = Callable[[Msgid], str]


class KXLocalizer(EventDispatcher):
    lang = StringProperty()

    _ = ObjectProperty(lambda v: v)
    '''(read-only) translator'''

    font_name = StringProperty(Label.font_name.defaultvalue)
    '''(read-only)'''

    def __init__(
        self, *,
        lang: Lang='en',
        translator: Callable[[Lang], FuncTranslate]=None,
        fontfinder: Callable[[Lang], Fontname]=None,
    ):
        if translator is None:
            translator = lambda lang: lambda msgid: msgid
        if fontfinder is None:
            fontfinder = DefaultFontFinder()
        self._translator = translator
        self._fontfinder = fontfinder
        super().__init__(lang=lang)

    def install(self, *, name):
        from kivy.lang import global_idmap
        global_idmap[name] = self

    def on_lang(self, __, lang):
        self.font_name = self._fontfinder(lang)
        self._ = self._translator(lang)


class DefaultFontFinder:
    PRESET = {
        'en': (v := 'Roboto'),
        'fr': v,
        'ru': v,
    }
    def __init__(self):
        self._font_names = self.PRESET.copy()

    def __call__(self, lang: Lang) -> Fontname:
        try:
            return self._font_names[lang]
        except KeyError:
            pass
        from .fontfinder import enum_fonts_from_lang
        try:
            font_name = next(enum_fonts_from_lang(lang)).name
        except StopIteration:
            from kivy.logger import Logger
            Logger.warning(
                f"kivy_garden.i18n: Couldn't find a font for lang'{lang}'. "
                "Use Roboto as a fallback.")
            font_name = 'Roboto'
        self._font_names[lang] = font_name
        return font_name


class GettextTranslator:
    def __init__(self, domain, localedir):
        self.domain = domain
        self.localedir = localedir

    def __call__(self, lang: Lang) -> FuncTranslate:
        from gettext import translation
        return translation(domain=self.domain, localedir=self.localedir, languages=(lang, )).gettext


class DictBasedTranslator:
    def __init__(self, table: Dict[Msgid, Dict[Lang, str]]):
        self._table = table

    def __call__(self, lang: Lang) -> FuncTranslate:
        def func(msgid):
            try:
                return self._table[msgid][lang]
            except KeyError:
                return msgid
        return func
