__all__ = (
    'I18nError', 'UnsupportedLanguageError',
)
from functools import cached_property


class I18nError(Exception):
    '''Base class of all the module-specific exceptions'''


class UnsupportedLanguageError(I18nError):
    @cached_property
    def lang(self):
        return self.args[0]
