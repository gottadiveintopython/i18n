==========
Usage |ja|
==========


1: 翻訳データを用意する
===========================

初期状態では二種類の形式の翻訳データが使えます。
一つは gettext_ で作った ``.mo`` ファイルで、もう一つは以下のような :class:`collections.abc.Mapping` です。

.. code-block::

    翻訳表 = {
        "greeting": {
            "ja": "おはよう",
            "en": "morning",
        },
        "app title": {
            "ja": "初めてのKivyプログラム",
            "en": "My First Kivy App",
        },
    }


2: TranslatorFactory を作る
==================================

翻訳データから ``TranslatorFactory`` を作ります。

.. code-block::

    from kivy_garden.i18n.localizer import (
        GettextBasedTranslatorFactory,
        MappingBasedTranslatorFactory,
    )

    # gettextの場合
    factory = GettextBasedTranslatorFactory(domain, localedir)

    # mappingの場合
    factory = MappingBasedTranslatorFactory(翻訳表)

(``domain`` と ``localedir`` は :func:`gettext.translation` に渡されます)。


3: Localizer を作る
==========================

``TranslatorFactory`` から :class:`~kivy_garden.i18n.localizer.Localizer` を作ります。

.. code-block::

    from kivy_garden.i18n.localizer import Localizer

    localizer = Localizer(factory)


完了
====

これで準備完了です。
後はこの ``localizer`` に対して「このメッセージの訳は何ですか？」や「現在の言語に適したフォントは何ですか？」と尋ねるだけです。

.. code-block::

    l = localizer
    l.lang = "en"  # "現在の言語" を "en" に設定
    print(l.font_name)  # => Roboto
    print(l._("greeting"))  # => morning
    print(l._("app title"))  # => My First Kivy App

    l.lang = "ja"
    print(l.font_name)  # => <インストール済みの日本語フォントの名前>
    print(l._("greeting"))  # => おはよう
    print(l._("app title"))  # => 初めてのKivyプログラム


また ``Localizer`` は :class:`kivy.event.EventDispatcher` の派生クラスであり
``Localizer.font_name`` と ``Localizer._`` はKivyのプロパティであるためKivyの自動バインディング機能も利用できます。

.. code-block::

    # Kv言語のコードからimport文無しで"l"という名前でlocalizerへ触れるようにする。
    localizer.install(name="l")

.. code-block:: yaml

    # in .kv files
    Label:
        font_name: l.font_name
        text: l._("greeting")

``localizer.lang`` (現在の言語)が変わると ``localizer._`` と ``localizer.font_name`` の値も自動で変わるため、
それが上記コード内の式 ``l.font_name`` と ``l._("greeting")`` の再評価を引き起こします。
これで現在の言語が変わるたびに文字列とフォントが自動で切り替わるラベルができました。
