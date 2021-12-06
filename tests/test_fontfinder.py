import pytest

@pytest.mark.parametrize('text', ('', 'A', 'AB'))
def test_too_short_text(text):
    from kivy_garden.i18n.fontfinder import enum_fonts_from_text
    with pytest.raises(ValueError):
        next(enum_fonts_from_text(text))


def test_duplicated_character():
    from kivy_garden.i18n.fontfinder import enum_fonts_from_text
    with pytest.raises(ValueError):
        next(enum_fonts_from_text('Guido van Rossum'))


def test_the_faster_version_produces_the_same_result_as_the_safer_version():
    from kivy_garden.i18n.fontfinder import enum_fonts_from_text, DISCRIMINANT
    for text in {text for text in DISCRIMINANT.values()}:
        assert tuple(enum_fonts_from_text(text)) == tuple(enum_fonts_from_text_another_ver(text))


def enum_fonts_from_text_another_ver(text):
    '''Another version of ``enum_fonts_from_text()``. This exists only for tests.'''
    from kivy.uix.label import Label
    from kivy_garden.i18n.fontfinder import get_all_fonts
    if len(text) < 3:
        raise ValueError(f"'text' must contain more than two characters")
    if len(set(text)) < len(text):
        raise ValueError(f"'text' should not contain duplicated characters")
    label = Label(font_size=15)
    for path in get_all_fonts():
        label.font_name = str(path)
        pixels_set = set()
        for i, c in enumerate(text, start=1):
            label.text = c
            label.texture_update()
            pixels_set.add(label.texture.pixels)
            if len(pixels_set) != i:
                break
        else:
            yield path
