# kivy_garden.i18n

Internationalization support for Kivy applications.

```python
from kivy_garden.i18n.localizer import MappingBasedTranslatorFactory, Localizer

translations = {
    "greeting": {
        "ja": "おはよう",
        "en": "morning",
    },
    "app title": {
        "ja": "初めてのKivyプログラム",
        "en": "My First Kivy App",
    },
}
localizer = Localizer(MappingBasedTranslatorFactory(translations))

l = localizer
l.lang = "en"  # Set the "current language" to "en"
assert l.font_name == "Roboto"
assert l._("greeting") == "morning"
assert l._("app title") == "My First Kivy App"

l.lang = "ja"
assert l.font_name == "<a pre-installed Japanese font>"
assert l._("greeting") == "おはよう"
assert l._("app title") == "初めてのKivyプログラム"
```

Bindings:

```python
from kivy.lang import Builder

localizer.install(name="l")
label = Builder.load_string("""
Label:
    font_name: l.font_name
    text: l._("greeting")
""")
localizer.lang = "en"
assert label.font_name == "Roboto"
assert label.text == "morning"
localizer.lang = "ja"
assert label.font_name == "<a pre-installed Japanese font>"
assert label.text == "おはよう"
```

# Installation

Pin the minor version.

```
pip install "kivy-garden-i18n>=0.2,<0.3"
```

# Tested on

- CPython 3.10 + Kivy 2.3
- CPython 3.11 + Kivy 2.3
- CPython 3.12 + Kivy 2.3
- CPython 3.13 + Kivy 2.3
