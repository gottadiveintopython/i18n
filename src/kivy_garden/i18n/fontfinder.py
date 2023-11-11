__all__ =(
    'enum_pre_installed_fonts', 'can_render_text', 'can_render_lang', 'default_filter', 'enum_langs', 'register_lang',
)

from typing import Union
from collections.abc import Callable, Iterator
from pathlib import Path, PurePath
from kivy.core.text import LabelBase, Label as CoreLabel

from ._exceptions import UnsupportedLanguageError


def default_filter(font: PurePath, suffixes=('.ttf', '.otf', '.ttc', )) -> bool:
    '''
    The default *filter* of :func:`enum_pre_installed_fonts`.
    If the suffix of the ``font`` is one of ``.ttf``, ``.otf`` and ``.ttc`` as well as its filename doesn't contain
    ``'fallback'``, this function returns True.
    '''
    return font.suffix in suffixes and 'fallback' not in font.name.lower()


def enum_pre_installed_fonts(*, filter: Callable[[Path], bool]=default_filter) -> Iterator[Path]:
    for dir in LabelBase.get_system_fonts_dir():
        for child in Path(dir).iterdir():
            if filter(child):
                yield child


def can_render_text(font: Union[str, Path], text: str) -> bool:
    '''
    Whether a specified ``font`` is capable of rendering a specified ``text``.

    :param text: must consist of more than two characters without repetition.

    .. code-block::

        from kivy_garden.i18n.fontfinder import can_render_text as f

        # Roboto, the default font, lacks CJK characters.
        assert f("Roboto", "ABC")
        assert not f("Roboto", "漢字한글ひら")
        assert not f("Roboto", "漢字한글ひらABC")

        assert f("NotoSerifCJK-Regular.ttc", "ABC")
        assert f("NotoSerifCJK-Regular.ttc", "漢字한글ひら")
        assert f("NotoSerifCJK-Regular.ttc", "漢字한글ひらABC")

        # Fallback-fonts may lack ASCII characters.
        assert not f("DroidSansFallbackFull.ttf", "ABC")
        assert f("DroidSansFallbackFull.ttf", "漢字한글ひら")
        assert not f("DroidSansFallbackFull.ttf", "漢字한글ひらABC")

    .. note::

        The longer the ``text`` is, the more accurate the result will be, but the more time it would take.
    '''
    if not _validate_discriminant(text):
        raise ValueError(f"'text' must consist of more than two characters without repetition (was {text!r})")
    label = CoreLabel()
    label._size = (16, 16, )
    label.options['font_name'] = str(font)
    label.resolve_font_name()
    rendered_text = set()
    for i, c in enumerate(text, start=1):
        label.text = c
        label._render_begin()
        label._render_text(c, 0, 0)
        data = label._render_end().data
        if data in rendered_text:
            return False
        rendered_text.add(data)
    return True


DISCRIMINANTS = {
    'ar': 'الجزيرةAB',
    'hi': 'भारतAB',
    'ja': (v := '経伝説あAB'),
    'ja-JP': v,
    'ja_JP': v,
    'ko': (v := '안녕조AB'),
    'ko-KR': v,
    'ko_KR': v,
    'zh-Hans': (v := '哪经传说AB'),
    'zh_Hans': v,
    'zh-CN': v,
    'zh_CN': v,
    'zh-SG': v,
    'zh_SG': v,
    'zh-Hant': (v := '哪經傳說AB'),
    'zh_Hant': v,
    'zh-TW': v,
    'zh_TW': v,
    'zh-HK': v,
    'zh_HK': v,
    'zh-MO': v,
    'zh_MO': v,
    'zh': '哪經傳說经传说AB',
}


def can_render_lang(font: Union[str, Path], lang: str) -> bool:
    '''
    Whether a specified ``font`` is capable of rendering a specified ``lang``.

    .. code-block::

        from kivy_garden.i18n.fontfinder import can_render_lang as f

        assert not f("Roboto", "zh")
        assert not f("Roboto", "ko")
        assert not f("Roboto", "ja")

        assert f("NotoSerifCJK-Regular.ttc", "zh")
        assert f("NotoSerifCJK-Regular.ttc", "ko")
        assert f("NotoSerifCJK-Regular.ttc", "ja")

        # Font that lacks ASCII characters is considered unable to render any language.
        assert not f("DroidSansFallbackFull.ttf", "zh")
        assert not f("DroidSansFallbackFull.ttf", "ko")
        assert not f("DroidSansFallbackFull.ttf", "ja")

    :raise UnsupportedLanguageError: if the given ``lang`` is not supported.
    '''
    try:
        text = DISCRIMINANTS[lang]
    except KeyError:
        raise UnsupportedLanguageError(lang)
    return can_render_text(font, text)


def enum_langs() -> Iterator[str]:
    '''
    Available languages for :func:`can_render_lang`.
    '''
    return DISCRIMINANTS.keys()


def register_lang(lang: str, discriminant: str):
    '''
    Enable a language in the :func:`can_render_lang`.

    .. code-block::

        register_lang('th', "ราชอAB")  # Thai language
    '''
    if not _validate_discriminant(discriminant):
        raise ValueError(f"'discriminant' must consist of more than two characters without repetition (was {discriminant!r})")
    DISCRIMINANTS[lang] = discriminant


def _validate_discriminant(discriminant: str, len=len, set=set) -> bool:
    l = len(discriminant)
    return l >= 3 and len(set(discriminant)) == l
