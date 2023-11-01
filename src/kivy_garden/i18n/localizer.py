from __future__ import annotations

__all__ = (
    # type hints
    'Translator', 'TranslatorFactory', 'FontPicker',

    # exceptions
    'I18nError', 'FontNotFoundError',

    # concrete TranslatorFactory
    'GettextBasedTranslatorFactory', 'MappingBasedTranslatorFactory',

    # concrete FontPicker
    'DefaultFontPicker',

    #
    'Localizer',
)

from collections.abc import Callable, Mapping
from typing import TypeAlias, Union
import itertools
from functools import cached_property

from kivy.properties import StringProperty, ObjectProperty
from kivy.event import EventDispatcher
from kivy.logger import Logger
from kivy.uix.label import Label

Msgid: TypeAlias = str
Msgstr: TypeAlias = str
Lang: TypeAlias = str
Translator: TypeAlias = Callable[[Msgid], Msgstr]
TranslatorFactory : TypeAlias = Callable[[Lang], Translator]
Font: TypeAlias = str
FontPicker: TypeAlias = Callable[[Lang], Font]


class I18nError(Exception):
    '''Base class of all the module-specific exceptions'''


class FontNotFoundError(I18nError):
    '''Failed to find a font.'''

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

    def __init__(self, *, lang: Lang='en', translator_factory: TranslatorFactory=None, font_picker: FontPicker=None):
        if translator_factory is None:
            Logger.warning(
                f"kivy_garden.i18n: No translator_factory was provided. ``msgid``s themselves will be displaed.")
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

        :raises I18nError: if the ``name`` has already been used.
        '''
        from kivy.lang import global_idmap
        if name in global_idmap:
            raise I18nError(f"The name {name!r} has already been used.")
        global_idmap[name] = self

    def uninstall(self, *, name):
        from kivy.lang import global_idmap
        if name not in global_idmap:
            raise I18nError(f"The name {name!r} not found.")
        if global_idmap[name] is not self:
            raise I18nError(f"The object referenced by {name!r} is not me.")
        del global_idmap[name]

    @staticmethod
    def on_lang(self, lang):
        ''':meta private:'''
        self._ = self.translator_factory(lang)
        self.font_name = self.font_picker(lang)


class DefaultFontPicker:
    PRESET = {
        'en': (v := 'Roboto'),
        'fr': v,
        'it': v,
        'pt': v,
        'ru': v,
    }
    ''':meta private:'''

    del v

    def __init__(self, *, fallback: Union[Lang, None]='Roboto'):
        self._lang2font = self.PRESET.copy()
        self._fallback = fallback

    def __call__(self, lang: Lang) -> Font:
        try:
            return self._lang2font[lang]
        except KeyError:
            pass

        from .fontfinder import enum_pre_installed_fonts, can_render_lang
        name = None
        for font in enum_pre_installed_fonts():
            if can_render_lang(font, lang):
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
    def __init__(self, table: Mapping[Msgid, Mapping[Lang, Msgstr]], /):
        self._table = _reverse_mapping(table, nullable=False)

    def __call__(self, lang: Lang) -> Translator:
        return self._table[lang].__getitem__


def _reverse_mapping(d: Mapping[Msgid, Mapping[Lang, Msgstr]], *, nullable=True) -> dict[Lang, dict[Msgid, Msgstr]]:
    msgids = tuple(d.keys())
    langs = set(itertools.chain.from_iterable(d.values()))
    if nullable:
        return {
            lang: {msgid: d[msgid].get(lang, None) for msgid in msgids}
            for lang in langs
        }
    else:
        return {
            lang: {msgid: d[msgid].get(lang, msgid) for msgid in msgids}
            for lang in langs
        }
