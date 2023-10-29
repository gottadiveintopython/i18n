__all__ = ('extract_msgids_from_string_literals', )

'''xgettextは文字列literalからは抽出してくれないのでこのscriptを使って抽出する'''

import re
from typing import Iterator


def extract_string_literals(python_code: str) -> Iterator[str]:
    from ast import parse, walk, Constant
    str_ = str
    isinstance_ = isinstance
    for node in walk(parse(python_code)):
        if isinstance_(node, Constant) and isinstance_(node.value, str_):
            yield node.value


PATTERN = re.compile(r"""
    (^|\W)(_\(".*?"\))  # _("")で括られた文字列
    |                   # もしくは
    (^|\W)(_\('.*?'\))  # _('')で括られた文字列
""", re.VERBOSE | re.MULTILINE)


def extract_msgid(s:str) -> Iterator[str]:
    for m in PATTERN.finditer(s):
        yield (m.group(2) or m.group(4))


def extract_msgids_from_string_literals(python_code: str) -> Iterator[str]:
    return (
        ls
        for s in extract_string_literals(python_code)
        for ls in extract_msgid(s)
    )


def main():
    import sys
    from pathlib import Path
    from io import StringIO
    output = StringIO()
    write = output.write
    for file in sys.argv[1:]:
        for ls in extract_msgids_from_string_literals(Path(file).read_text(encoding='utf-8')):
            print(ls, file=output)
    print(output.getvalue())
    output.close()


if __name__ == "__main__":
    main()
