__all__ = (
    # type hints
    "Translator", "TranslatorFactory", "FontPicker",

    # exceptions
    "FontNotFoundError",

    # concrete TranslatorFactory
    "GettextBasedTranslatorFactory", "MappingBasedTranslatorFactory",

    # concrete FontPicker
    "DefaultFontPicker",

    #
    "Localizer",
)

from collections.abc import Callable, Mapping
from typing import TypeAlias, Union
import itertools
from functools import cached_property

from kivy.properties import StringProperty, ObjectProperty
from kivy.event import EventDispatcher
from kivy.logger import Logger
from kivy.uix.label import Label

from .fontfinder import enum_pre_installed_fonts, font_supports_lang

Msgid: TypeAlias = str
Msgstr: TypeAlias = str
Lang: TypeAlias = str
Translator: TypeAlias = Callable[[Msgid], Msgstr]
TranslatorFactory : TypeAlias = Callable[[Lang], Translator]
Font: TypeAlias = str
FontPicker: TypeAlias = Callable[[Lang], Font]


class FontNotFoundError(Exception):
    @cached_property
    def lang(self) -> Lang:
        '''The language for which a localizer couldn't find a suitable font.'''
        return self.args[0]


class Localizer(EventDispatcher):
    lang: Lang = StringProperty()
    '''
    The "current language" of this localizer.
    '''

    _: Translator = ObjectProperty(lambda msgid: msgid)
    '''
    (read-only)
    A callable object that takes a ``msgid``, and returns the corresponging ``msgstr`` according to the "current language".

    .. code-block::

        loc = Localizer(...)
        loc.lang = "en"
        print(loc._("app title"))  # => "My First Kivy Program"
        loc.lang = "ja"
        print(loc._("app title"))  # => "初めてのKivyプログラム"

    :meta public:
    '''

    font_name: Font = StringProperty(Label.font_name.defaultvalue)
    '''
    (read-only)
    A font that is capable of rendering the "current language".

    .. code-block::

        loc = Localizer(...)
        loc.lang = "en"
        print(loc.font_name)  # => "Roboto"
        loc.lang = "ko"
        print(loc.font_name)  # => "/../NotoSerifCJK-Regular.ttc"
    '''

    def __init__(self, translator_factory: TranslatorFactory=None, *, lang: Lang='en', font_picker: FontPicker=None):
        if translator_factory is None:
            Logger.warning(f"kivy_garden.i18n: No translator_factory was provided. Msgid's themselves will be displayed.")
            translator_factory = lambda lang: lambda msgid: msgid
        if font_picker is None:
            font_picker = DefaultFontPicker()
        self.translator_factory = translator_factory
        self.font_picker = font_picker
        super().__init__(lang=lang)

    def install(self, *, name):
        '''
        Makes the localizer accessble from kv without any import-statements.

        .. code-block::

            loc = Localizer(...)
            loc.install(name='l')

        .. code-block:: yaml

            Label:
                font_name: l.font_name
                text: l._("msgid")

        :raises ValueError: if the ``name`` has already been used.
        '''
        from kivy.lang import global_idmap
        if name in global_idmap:
            raise ValueError(f"The name {name!r} has already been used.")
        global_idmap[name] = self

    def uninstall(self, *, name):
        from kivy.lang import global_idmap
        if name not in global_idmap:
            raise ValueError(f"The name {name!r} not found.")
        if global_idmap[name] is not self:
            raise ValueError(f"The object referenced by {name!r} is not me.")
        del global_idmap[name]

    @staticmethod
    def on_lang(self, lang):
        ''':meta private:'''
        self._ = self.translator_factory(lang)
        self.font_name = self.font_picker(lang)


class DefaultFontPicker:
    PRESET = {
        "en": (v := "Roboto"),
        "fr": v,
        "it": v,
        "pt": v,
        "ru": v,
    }
    ''':meta private:'''

    del v

    def __init__(self, *, fallback: Union[Lang, None]="Roboto"):
        self._lang2font = self.PRESET.copy()
        self._fallback = fallback

    def __call__(self, lang: Lang) -> Font:
        try:
            return self._lang2font[lang]
        except KeyError:
            pass

        name = None
        for font in enum_pre_installed_fonts():
            if font_supports_lang(font, lang):
                name = font.name
                break
        if name is None:
            fallback = self._fallback
            if fallback is None:
                raise FontNotFoundError(lang)
            Logger.warning(f"kivy_garden.i18n: Couldn't find a font for lang '{lang}'. Use {fallback} as a fallback.")
            name = fallback
        self._lang2font[lang] = name
        return name


class GettextBasedTranslatorFactory:
    def __init__(self, domain, localedir):
        self.domain = domain
        self.localedir = localedir

    def __call__(self, lang: Lang) -> Translator:
        from gettext import translation
        return translation(domain=self.domain, localedir=self.localedir, languages=(lang, )).gettext


class MappingBasedTranslatorFactory:
    def __init__(self, translations: Mapping[Msgid, Mapping[Lang, Msgstr]], /, strict=False):
        '''
        :param strict:
            If False (default), a missing translation falls back to the ``msgid`` itself.
            If True, a missing translation raises ``ValueError``.
        '''
        self._compiled_translations = self._compile_translations(translations, strict=strict)

    def __call__(self, lang: Lang) -> Translator:
        return self._compiled_translations[lang].__getitem__

    @staticmethod
    def _compile_translations(d: Mapping[Msgid, Mapping[Lang, Msgstr]], *, strict) -> dict[Lang, dict[Msgid, Msgstr]]:
        '''
        アプリ開発者側にとって嬉しいのは次のような形式の翻訳表だと思うが

        .. code-block::

            翻訳表 = {
                "greeting": {
                    "ja": "おはよう",
                    "en": "morning",
                },
                "app title": {
                    "ja": "初めてのKivyプログラム",
                    "en": "My First Kivy App",
                },
            }

        ライブラリが内部で持ちたいのは次の形式の翻訳表である。

        .. code-block::

            翻訳表 = {
                "ja": {
                    "greeting": "おはよう",
                    "app title": "初めてのKivyプログラム",
                },
                "en": {
                    "greeting": "morning",
                    "app title": "My First Kivy App",
                },
            }

        この関数は前者を後者に変換する。
        '''
        msgids = tuple(d.keys())
        langs = set(itertools.chain.from_iterable(d.values()))
        if strict:
            try:
                return {
                    lang: {msgid: d[msgid][lang] for msgid in msgids}
                    for lang in langs
                }
            except KeyError as e:
                raise ValueError(f"Msgid '{e.args[0]}' is missing one or more translations") from e
        else:
            return {
                lang: {msgid: d[msgid].get(lang, msgid) for msgid in msgids}
                for lang in langs
            }
