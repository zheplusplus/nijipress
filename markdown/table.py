import re

_CELL_RE = re.compile('^(?P<cell_attr>((;[^;]+);)|())(?P<cell_content>.*$)')
_ROW_RE = re.compile('[|][|](?P<cell>([^|]|[|][^|])*)')

def attr_format(attr):
    if 0 == len(attr):
        return ''

    if not len(attr) % 2 == 0:
        return ''

    attrs = ''
    try:
        from nijiconf import CELL_ATTR_MAP
        for i in range(0, len(attr) / 2 - 1):
            attrs += CELL_ATTR_MAP[attr[i * 2 + 1]](attr[i * 2 + 2])
        return attrs
    except KeyError:
        from nijierr import ParseError, MSG_CELL_ATTR_ERROR
        raise ParseError(MSG_CELL_ATTR_ERROR + attr[1: -1])

def attr_content_extract(cell):
    from nijiconf import CELL_BEGIN
    return _CELL_RE.sub(
            lambda m: CELL_BEGIN % (attr_format(m.group('cell_attr')),
                                    m.group('cell_content')), cell)

def row_extract(line):
    from nijiconf import CELL_END
    return _ROW_RE.sub(
            lambda m: attr_content_extract(m.group('cell')) + CELL_END, line)
