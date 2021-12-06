__all__ =(
    'enum_all_fonts', 'get_all_fonts', 'enum_fonts_from_text', 'enum_fonts_from_lang',
)

from typing import Tuple, Iterator
from functools import lru_cache
from pathlib import Path

SUFFIXES = {'.ttf', '.otf', '.ttc', }
EXCLUDES = {
    # SDL2 text provider cannot render this font. Don't know about other providers.
    'NotoColorEmoji.ttf',

    # This doesn't contain English letters.
    'DroidSansFallbackFull.ttf',
}
DISCRIMINANT = {
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

def enum_all_fonts() -> Iterator[Path]:
    '''Enumerates pre-installed fonts'''
    from kivy.core.text import LabelBase
    suffixes = SUFFIXES
    excludes = EXCLUDES
    for dir in LabelBase.get_system_fonts_dir():
        for child in Path(dir).iterdir():
            if child.suffix in suffixes and child.name not in excludes:
                yield child


@lru_cache(maxsize=1)
def get_all_fonts() -> Tuple[Path]:
    '''Returns a tuple of pre-installed fonts. Caches the return-value.'''
    return tuple(enum_all_fonts())


def enum_fonts_from_text(text: str) -> Iterator[Path]:
    '''Enumerates pre-installed fonts that are capable of rendering the given
    ``text``. The ``text`` must contain more than two characters without
    duplication.

    .. note::

        The longer the ``text`` is, the more accurate the result would be,
        but the more time it'll take.
    '''
    from kivy.core.text import Label as CoreLabel
    if len(text) < 3:
        raise ValueError(f"'text' must contain more than two characters")
    if len(set(text)) < len(text):
        raise ValueError(f"'text' should not contain duplicated characters")
    label = CoreLabel()
    label._size = (16, 16)
    for path in get_all_fonts():
        label.options['font_name'] = str(path)
        label.resolve_font_name()
        pixels_set = set()
        for i, c in enumerate(text, start=1):
            label.text = c
            label._render_begin()
            label._render_text(c, 0, 0)
            pixels_set.add(label._render_end().data)
            if len(pixels_set) != i:
                break
        else:
            yield path


def enum_fonts_from_lang(lang: str) -> Iterator[Path]:
    '''Enumerates pre-installed fonts supporting the given language. '''
    try:
        text = DISCRIMINANT[lang]
    except KeyError:
        return iter('')
    return enum_fonts_from_text(text)
