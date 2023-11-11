===========
Font Finder
===========

This module assists you in locating a font for languages that cannot be displayed using Kivy's default font, Roboto, from the system.
You no longer need to include fonts in your app, saving valuable space.

Usage
=====

Usage is pretty straightforward.
Enumerate pre-installed fonts, then check if they are capable of rendering these languages one by one.

.. code-block::

    from kivy_garden.i18n.fontfinder import enum_pre_installed_fonts, can_render_lang

    for font in enum_pre_installed_fonts():
        if can_render_lang(font, 'ja'):
            print("Found a Japanese font:", font.name)
        if can_render_lang(font, 'ko'):
            print("Found a Korean font:", font.name)

The ``can_render_lang()`` API does not offer support for all languages by default.
If a language is not supported, you will need to register it first:

.. code-block::

    from kivy_garden.i18n.fontfinder import register_lang

    register_lang('th', "ราชอAB")  # Thai language

    for font in enum_pre_installed_fonts():
        if can_render_lang(font, 'th'):
            print("Found a Thai font:", font.name)

You may have noticed the ``AB`` in the code above.
If you exclude ASCII characters, you might choose a font that cannot render them, such as a fallback font, which is probably not what you want.


API Reference
=============

.. automodule:: kivy_garden.i18n.fontfinder
    :members:
    :undoc-members:
