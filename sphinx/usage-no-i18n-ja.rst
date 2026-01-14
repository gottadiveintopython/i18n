====================
Usage (No i18n) |ja|
====================

国際化は不要だがインストール済みのフォントを使ってアプリの容量を減らしたいという人はここの手順に従ってください。

まずはインストール済みのフォントを列挙して、それがアプリで用いる言語に対応しているか確かめます。

.. code-block::

    from kivy_garden.i18n.fontfinder import (
        enum_pre_installed_fonts,
        font_supports_lang,
    )

    for font in enum_pre_installed_fonts():
        if font_supports_lang(font, "ja"):
            print("日本語フォントが見つかりました:", font.name)
            break
    else:
        raise Exception("日本語フォントが見つかりませんでした")

見つかったらそれを既定のフォントとして登録します。
この作業はいかなるウィジェットを作るより前に行った方が良いでしょう。

.. code-block::

    from kivy.core.text import LabelBase, DEFAULT_FONT

    LabelBase.register(DEFAULT_FONT, font.name)

以上で終わりです。

ただし初期状態では全ての言語には対応していないので
未対応の言語を使いたい場合は先に :func:`~kivy_garden.i18n.fontfinder.register_lang` で登録してください。

.. code-block::

    from kivy_garden.i18n.fontfinder import register_lang

    register_lang("th", "ราชอAB")  # タイ語

    for font in enum_pre_installed_fonts():
        if font_supports_lang(font, "th"):
            print("タイ語フォントが見つかりました:", font.name)

または :func:`~kivy_garden.i18n.fontfinder.font_provides_glyphs` を使うこともできます:

.. code-block::

    from kivy_garden.i18n.fontfinder import font_provides_glyphs

    for font in enum_pre_installed_fonts():
        if font_provides_glyphs(font, "ราชอAB"):
            print("タイ語フォントが見つかりました:", font.name)

(上記の例においてタイ語の文字以外に ``AB`` を含めているのを不思議に思うかもしれません。
これはASCII文字を含めないとそれが含まれないフォント(例: フォールバックフォント)が選ばれる可能性があるからです。)
