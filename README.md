# i18n

Kivyアプリの多言語化は面倒くさいです。
というのも只表示する文字列を切り替えればいいわけではないからです。
**Kivyは文字列の描画に必要なフォントを自動で選んでくれはしないので、アプリ側がKivyに教えてあげなければいけません。**
それを怠れば画面には文字に代わって豆腐が表示されてしまいます。

また多くのKivyアプリはフォントをアプリに詰め込むという方法を採っていますが、これも多言語化の際には問題となります。
フォントを幾つもアプリに詰め込めんでアプリのサイズが数十MB膨れ上がればアプリの利用者は喜ばないでしょう。

そこでこのmoduleの出番です。
このmoduleは文字列を切り替える機能に加えて、**OSにinstall済のフォントの中から各言語用の物を自動で選んでくれます。**
なのでアプリにフォントを詰め込む必要はもうありません。

## install方法

```
pip install --pre kivy_garden.i18n
```

## 使い方

### フォントの検索

表示する文字列の切り替えとフォントの切り替えは別々の機能であり、どちらか片方だけ使うこともできます。
また多言語化には興味はないけどOSにinstall済のフォントを利用して少しでもアプリの容量を減らしたいという人も居るでしょう。
そういった人には以下のような使い方がおすすめです。


```python
# OSにinstall済の日本語フォントの内 最初に見つけた物を利用する例

from kivy_garden.i18n.fontfinder import enum_fonts_from_lang

font = next(enum_fonts_from_lang('ja'), None)
if font is None:
    print(f"日本語フォントが見つかりませんでした")
else:
    label.font_name = font.name
```

### フォントの切り替え

そして多言語化させたい場合は以下のようにします。

```python
from kivy_garden.i18n.localizer import KXLocalizer

loc = KXLocalizer()
loc.lang = 'ja'
print(loc.font_name)  # => 何かの日本語フォント名が出力される
loc.lang = 'zh'
print(loc.font_name)  # => 何かの中文フォント名が出力される
```

重要なのが`KXLocalizer`が`EventDispatcher`な事で

```python
class KXLocalizer(EventDispatcher):
    lang = StringProperty(...)
    font_name = StringProperty(...)
    _ = ObjectProperty(...)
```

bindingを利かせれば`lang`を切り替えた時に`Label`の`font_name`も自動で切り替わるようにできます。

```python
from kivy.app import App
from kivy.lang import Builder
from kivy_garden.i18n.localizer import KXLocalizer


KV_CODE = '''
Label:
    font_name: app.loc.font_name
'''


class SampleApp(App):
    def build(self):
        self.loc = KXLocalizer()
        return Builder.load_string(KV_CODE)

    def on_start(self):
        self.loc.lang = 'ja'  # bindingによりLabelには自動で日本語フォントが適用される
```

また`KXLocalizer.install()`を用いる事で`#:import`無しで`KXLocalizer`をKv言語内で直接参照できるようにもできます。
ただしglobal変数を書き換える行為なので使用は自己責任で。

```python
# 上のcodeど同等のcode
from kivy.app import App
from kivy.lang import Builder
from kivy_garden.i18n.localizer import KXLocalizer


KV_CODE = '''
Label:
    font_name: l.font_name  # import無しで参照 !!
'''

class SampleApp(App):
    def build(self):
        self.loc = KXLocalizer()
        self.loc.install(name='l')  # install !!
        return Builder.load_string(KV_CODE)

    def on_start(self):
        self.loc.lang = 'ja'
```

### 翻訳(文字列の切り替え)

そして肝心の翻訳ですが、これは`KXLocalizer`に翻訳者(Translator)を与える事で実現できます。
現在ある翻訳者は

- `gettext`を利用する`GettextTranslator`と
- 辞書を用いた単純な仕組みの`DictBasedTranslator`

の二種で、ここでは`DictBasedTranslator`を用いた方法を解説します。
`GettextTranslator`に関しては[gettext_example](https://github.com/gottadiveintopython/i18n/blob/main/examples/gettext_example.py)を参照して下さい。

まず必要となるのは以下のような辞書型の翻訳表です。

```python
翻訳表 = {
    'tiger': {
        'zh': '老虎',
        'ja': '虎',
        'en': 'tiger',
    },
    'apple': {
        'zh': '蘋果',
        'ja': 'りんご',
        'en': 'apple',
    },
}
```

pythonの辞書literalは書きづらいので実際にはYAML形式で翻訳表を作り、それをpythonの辞書に変換した方が良いかもしれません。

```yaml
tiger:
  zh: 老虎
  ja: 虎
  en: tiger
apple:
  zh: 蘋果
  ja: りんご
  en: apple
```

```python
import yaml
翻訳表 = yaml.safe_load(YAML文字列)
```

翻訳表ができたら後は以下のようにして`KXLocalizer`に与えるだけです。

```python
from kivy_garden.i18n.localizer import KXLocalizer, DictBasedTranslator
loc = KXLocalizer(translator=DictBasedTranslator(翻訳表))
```

すると既に`loc.lang`(現在の言語)に基づいて適切な翻訳結果が得られるようになっています。

```python
loc.lang = 'ja'
print(loc._("tiger"))  # => 虎
print(loc._("apple"))  # => りんご
print(loc.font_name)   # => 何かの日本語フォント名
loc.lang = 'zh'
print(loc._("tiger"))  # => 老虎
print(loc._("apple"))  # => 蘋果
print(loc.font_name)   # => 何かの中文フォント名
```

そしてこれもなのですがbindingを利かせてあげれば`loc.lang`(現在の言語)に連動して`Label`の`text`と`font_name`が自動で更新されます。

```python
from kivy.app import App
from kivy.lang import Builder
from kivy_garden.i18n.localizer import KXLocalizer, DictBasedTranslator


KV_CODE = '''
Label:
    font_name: l.font_name
    text: l._("apple")
'''


class SampleApp(App):
    def build(self):
        self.loc = KXLocalizer(translator=DictBasedTranslator(翻訳表))
        self.loc.install(name='l')
        return Builder.load_string(KV_CODE)

    def on_start(self):
        # Labelのfont_nameに日本語フォントが、textには りんご が入る
        self.loc.lang = 'ja'

        # Labelのfont_nameに英文フォントが、textには apple が入る
        self.loc.lang = 'en'
```

このように`EventDispacther`のbindingの仕組みを利用すると**アプリの実行中に表示言語を自由に切り替えられるのがこのmoduleの強みとなります**。
もちろん言語切替時にアプリの再起動を求めるつもりなのであれば無理にbindingを利かせる必要はありません。

以上がこのmoduleの基本的な使い方となります。

## 小道具

`xgettext`は翻訳の必要性のある文字列をpythonソース中から抜き出してくれる素晴らしい道具ですが、
文字列literalの中までは見てくれないという欠点があります。
すなわち以下のcodeにおいて

```python
KV_CODE = '''
BoxLayout:
    Label:
        text: _("ABC")
    Label:
        text: _("DEF")
'''

_("123")
```

`123`は抜き出してくれても`ABC`と`DEF`は抜き出してくれません。
というわけでそういったことをしてくれる道具を作りました。

```
python -m kivy_gardem.i18n.extract_msgids_from_string_literals 上記のpythonファイル > ./output.py
```

```python
# output.pyの中身
_("ABC")
_("DEF")
```

このように文字列literal内の翻訳対象文字列をその外に抜き出してくれるので、
それを`xgettext`に喰わせてあげれば取りこぼしをせずに済みます。
