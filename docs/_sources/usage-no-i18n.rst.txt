===============
Usage (No i18n)
===============

If all you want is to use pre-installed fonts to save space, this is the guide for you.

Step 1: Locate pre-installed fonts
==================================

Enumerate the pre-installed fonts and check whether they support the language you need.

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


Step 2: Set the font as default before creating any widgets
===========================================================

.. code-block::

    from kivy.core.text import LabelBase, DEFAULT_FONT

    LabelBase.register(DEFAULT_FONT, font.name)

That's it.


However, not all languages are supported by default
===================================================

:func:`~kivy_garden.i18n.fontfinder.font_supports_lang` does not support all languages out of the box.
If a language is not supported, you need to register it first:

.. code-block::

    from kivy_garden.i18n.fontfinder import register_lang

    register_lang("th", "ราชอAB")  # Thai language

    for font in enum_pre_installed_fonts():
        if font_supports_lang(font, "th"):
            print("Found a Thai font:", font.name)

Alternatively, you can use :func:`~kivy_garden.i18n.fontfinder.font_provides_glyphs` directly:

.. code-block::

    from kivy_garden.i18n.fontfinder import font_provides_glyphs

    for font in enum_pre_installed_fonts():
        if font_provides_glyphs(font, "ราชอAB"):
            print("Found a Thai font:", font.name)

You may have noticed the ``AB`` in the example above.
If you don't include ASCII characters, you might end up selecting a font that cannot render them,
such as a fallback font, which is probably not what you want.
