==============
Advanced Usage
==============

If you want to use other types of text sources, you'll need to create your own ``TranslatorFactory``.
And if you want to customize the way the ``Localizer`` picks fonts, you'll need to create your own ``FontPicker``.

.. automethod:: kivy_garden.i18n.localizer.Localizer.__init__

* ``TranslatorFactory`` must be a callable that takes a string representing a language, and returns a ``Translator``.
* ``Translator`` must be a callable that takes a ``msgid``, and returns a ``msgstr``.
  If you've ever used gettext_, you may already know what ``msgid`` and ``msgstr`` are.
* ``FontPicker`` must be a callable that takes a string representing a language, and returns a ``Font``.
* ``Font`` must be either a path to a font file or a name registered using :meth:`kivy.core.text.LabelBase.register` e.g. ``Roboto``.

They are defined as follows:

.. code-block::

    Msgid: TypeAlias = str
    Msgstr: TypeAlias = str
    Lang: TypeAlias = str
    Translator: TypeAlias = Callable[[Msgid], Msgstr]
    TranslatorFactory : TypeAlias = Callable[[Lang], Translator]
    Font: TypeAlias = str
    FontPicker: TypeAlias = Callable[[Lang], Font]

You can use any object as long as it satisfies the above constraints.
