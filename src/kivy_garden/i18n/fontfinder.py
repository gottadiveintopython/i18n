__all__ =(
    "enum_pre_installed_fonts", "default_filter", "enum_langs", "register_lang",
    "font_provides_glyphs", "is_lang_supported",
)

from typing import Union
from collections.abc import Callable, Iterator
from pathlib import Path, PurePath
from kivy.core.text import LabelBase, Label as CoreLabel


def default_filter(font: PurePath, suffixes={".ttf", ".otf", ".ttc", ".woff", ".woff2"}) -> bool:
    '''
    The default *filter* for :func:`enum_pre_installed_fonts`.

    Returns True if ``font`` has one of the specified suffixes and its filename
    does not contain ``"fallback"``.
    '''
    return font.suffix in suffixes and "fallback" not in font.name.lower()


def enum_pre_installed_fonts(*, filter: Callable[[PurePath], bool]=default_filter) -> Iterator[Path]:
    for dir in LabelBase.get_system_fonts_dir():
        for child in Path(dir).iterdir():
            if filter(child):
                yield child


def font_provides_glyphs(font: str | Path, glyphs: str) -> bool:
    '''
    Whether a specified ``font`` supports all of the given ``glyphs``.

    :param glyphs: A string consisting of three or more unique characters.

    .. code-block::

        from kivy_garden.i18n.fontfinder import font_provides_glyphs as f

        # Roboto, Kivy's default font, lacks CJK glyphs.
        assert f("Roboto", "ABC")
        assert not f("Roboto", "漢字한글ひら")
        assert not f("Roboto", "漢字한글ひらABC")

        # NotoSerifCJK supports CJK and ASCII glyphs.
        assert f("NotoSerifCJK-Regular.ttc", "ABC")
        assert f("NotoSerifCJK-Regular.ttc", "漢字한글ひら")
        assert f("NotoSerifCJK-Regular.ttc", "漢字한글ひらABC")

        # Fallback fonts may lack ASCII glyphs.
        assert not f("DroidSansFallbackFull.ttf", "ABC")
        assert f("DroidSansFallbackFull.ttf", "漢字한글ひら")
        assert not f("DroidSansFallbackFull.ttf", "漢字한글ひらABC")

    .. note::

        Providing more glyphs improves accuracy, but increases the execution time.
    '''
    if not _validate_discriminant(glyphs):
        raise ValueError(f"'glyphs' must consist of three or more unique characters (was {glyphs!r})")
    label = CoreLabel()
    label._size = (16, 16, )
    label.options['font_name'] = str(font)
    label.resolve_font_name()
    rendered_results = set()
    for c in glyphs:
        label.text = c
        label._render_begin()
        label._render_text(c, 0, 0)
        pixels = label._render_end().data
        if pixels in rendered_results:
            return False
        rendered_results.add(pixels)
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
'''
あるフォントがある言語に対応しているか否かを判定するために使われる辞書。
辞書の値に含まれている文字全てがフォントに含まれている時のみ、そのフォントは対応する鍵の言語に対応していると見做される。
'''


def font_supports_lang(font: Union[str, Path], lang: str) -> bool:
    '''
    Whether a specified ``font`` is capable of rendering a specified ``lang``.

    .. code-block::

        from kivy_garden.i18n.fontfinder import font_supports_lang as f

        assert not f("Roboto", "zh")
        assert not f("Roboto", "ko")
        assert not f("Roboto", "ja")

        assert f("NotoSerifCJK-Regular.ttc", "zh")
        assert f("NotoSerifCJK-Regular.ttc", "ko")
        assert f("NotoSerifCJK-Regular.ttc", "ja")

        # A font that lacks ASCII characters is considered unable to support any language.
        assert not f("DroidSansFallbackFull.ttf", "zh")
        assert not f("DroidSansFallbackFull.ttf", "ko")
        assert not f("DroidSansFallbackFull.ttf", "ja")
    '''
    try:
        glyphs = DISCRIMINANTS[lang]
    except KeyError:
        raise ValueError(f"Unable to check language support: {lang = }.\n" "Register the language first using 'register_lang' function.")                         )
    return font_provides_glyphs(font, glyphs)


def enum_langs() -> Iterator[str]:
    '''
    Available languages for :func:`font_supports_lang`.
    '''
    return DISCRIMINANTS.keys()


def register_lang(lang: str, discriminant: str):
    '''
    Enable a language in the :func:`font_supports_lang`.

    .. code-block::

        register_lang('th', "ราชอAB")  # Thai language
    '''
    if not _validate_discriminant(discriminant):
        raise ValueError(f"'discriminant' must consist of three or more unique characters (was {discriminant!r})")
    DISCRIMINANTS[lang] = discriminant


def _validate_discriminant(discriminant: str, len=len, set=set) -> bool:
    l = len(discriminant)
    return l >= 3 and len(set(discriminant)) == l


# Aliases for backward compatibility
can_render_text = font_provides_glyphs
can_render_lang = font_supports_lang
