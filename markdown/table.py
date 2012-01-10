import re

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
    return re.sub('^(?P<cell_attr>((;[^;]+);)|())(?P<cell_content>.*$)'
                , lambda m: CELL_BEGIN % (attr_format(m.group('cell_attr'))
                                        , m.group('cell_content'))
                , cell)

def row_extract(line):
    from nijiconf import CELL_END
    return re.sub('[|][|](?P<cell>([^|]|[|][^|])*)'
                , lambda m: attr_content_extract(m.group('cell')) + CELL_END
                , line)
