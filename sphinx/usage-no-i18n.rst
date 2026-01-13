===============
Usage (No i18n)
===============

If all you want is to use pre-installed fonts to save space, this is the guide for you.

Step 1: Locate pre-installed fonts
==================================

Enumerate pre-installed fonts and check whether they provide the characters you need.

.. code-block::

    from kivy_garden.i18n.fontfinder import (
        enum_pre_installed_fonts,
        font_provides_glyphs,
    )

    for font in enum_pre_installed_fonts():
        if font_provides_glyphs(font, "哪經傳說経伝説经传说한글ひらABC"):
            print("Found a font that likely provides CJK glyphs:", font.name)
            break
    else:
        raise Exception("Couldn't find a font that provides CJK glyphs")


Step 1: Locate pre-installed fonts
==================================

Enumerate pre-installed fonts and check whether they are capable of rendering the languages you need.

.. code-block::

    from kivy_garden.i18n.fontfinder import (
        enum_pre_installed_fonts,
        font_supports_lang,
    )

    for font in enum_pre_installed_fonts():
        if font_supports_lang(font, "ja"):
            print("Found a Japanese font:", font.name)
            break
    else:
        raise Exception("Couldn't find a Japanese font")


Step 2: Apply the font before creating any widgets
==================================================

.. code-block::

    from kivy.core.text import LabelBase, DEFAULT_FONT

    LabelBase.register(DEFAULT_FONT, font.name)

That's it.


However, not all languages are supported by default
===================================================

The ``font_supports_lang()`` API does not offer support for all languages by default.
If a language is not supported, you will need to register it first:

.. code-block::

    from kivy_garden.i18n.fontfinder import register_lang

    register_lang('th', "ราชอAB")  # Thai language

    for font in enum_pre_installed_fonts():
        if font_supports_lang(font, 'th'):
            print("Found a Thai font:", font.name)

You may have noticed the ``AB`` in the code above.
If you exclude ASCII characters, you might choose a font that cannot render them, such as a fallback font, which is probably not what you want.


API Reference
=============

.. automodule:: kivy_garden.i18n.fontfinder
    :members:
    :undoc-members:
