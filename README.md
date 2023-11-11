# kivy_garden.i18n

A library that assists in creating a Kivy app with internationalization support.

It's composed of the following two primary components:

- The **Font Finder** helps you find fonts.
  If your app doesn't need i18n support, and you just want to use pre-installed fonts to saving space, you probably only need this.
- The **Localizer** helps you switch texts and fonts according to "current language".

## Installation

```
pip install "kivy-garden-i18n>=0.2<0.3"
poetry add kivy-garden-i18n@~0.2
```

# Tested on

- CPython 3.10 + Kivy 2.2.1
- CPython 3.11 + Kivy 2.2.1
