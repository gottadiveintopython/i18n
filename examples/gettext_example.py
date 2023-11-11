from kivy.app import App
from kivy.lang import Builder

KV_CODE = r'''
BoxLayout:
    orientation: 'vertical'
    AnchorLayout:
        Spinner:
            values: ['en', 'ar', 'zh', 'ja', 'ko', 'ru', 'fr', 'hi', ]
            font_size: sp(20)
            size_hint: .5, .3
            on_kv_post:
                self.bind(text=l.setter("lang"))
                self.text = 'ko'
    Label:
        font_name: l.font_name
        font_size: sp(40)
        text: l._("greeting")
'''


class SampleApp(App):
    def build(self):
        self.title = 'Greeting in various languages'
        self.setup_localizer()
        return Builder.load_string(KV_CODE)

    @staticmethod
    def setup_localizer():
        from pathlib import PurePath
        from kivy_garden.i18n.localizer import Localizer, GettextBasedTranslatorFactory
        factory = GettextBasedTranslatorFactory(
            domain='gettext_example',
            localedir=PurePath(__file__).parent / 'locales',
        )
        Localizer(translator_factory=factory).install(name='l')


if __name__ == '__main__':
    SampleApp().run()
