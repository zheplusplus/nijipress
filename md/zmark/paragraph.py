import re
import cgi
import bisect

import inline
import tags
import mathcom.api
import template


def forge_line(modifiers, line):
    for modifier in modifiers:
        line = modifier(line)
    return line


class Block(object):
    def build(self):
        return ''

    def truncate_to(self, limit):
        return 0


class Section(Block):
    def __init__(self, lines):
        self.lines = lines

    def build(self):
        return ''.join([self.head(), self.body(), self.tail()])

    def body(self):
        return ''

    def head(self):
        return ''

    def tail(self):
        return ''

    def truncate_to(self, limit):
        i = 0
        for i, ln in enumerate(self.lines):
            limit -= len(ln)
            if limit <= 0:
                self.lines = self.lines[:i + 1]
                return limit
        return limit


class Paragraph(Section):
    def __init__(self, lines):
        Section.__init__(self, filter(None, lines))

    def body(self):
        r = []
        for line in self.lines:
            r.extend([tags.PLINE_BEGIN, inline.forge(line), tags.PLINE_END])
        return ''.join(r)

    def head(self):
        return tags.PARA_BEGIN

    def tail(self):
        return tags.PARA_END


class Bullets(Section):
    def __init__(self, lines):
        Section.__init__(self, filter(None, [ln[2:] for ln in lines]))

    def body(self):
        return ''.join(sum([[tags.LI_BEGIN, inline.forge(line), tags.LI_END]
                            for line in self.lines], []))

    def head(self):
        return tags.UL_BEGIN

    def tail(self):
        return tags.UL_END


class SortedList(Bullets):
    def __init__(self, lines):
        Bullets.__init__(self, lines)

    def head(self):
        return tags.OL_BEGIN

    def tail(self):
        return tags.OL_END


class Table(Block):
    CELL_SPLIT = re.compile(r'(?<![\\])[\|]')

    class Cell(object):
        def __init__(self, content):
            self.content = content

    class Row(list):
        def __init__(self):
            list.__init__(self, [])

    def __init__(self, lines):
        self.head_rows, self.body_rows = self._parse_rows(lines)
        self.caption = ''

    def build(self):
        return template.render(
            'markdown/table.html', head_rows=self.head_rows,
            body_rows=self.body_rows, caption=self.caption)

    def _parse_rows(self, lines):
        head_rows = []
        for line in lines:
            if line[:2] != '|!':
                break
            head_rows.append(self._parse_row(line[2:]))
        return head_rows, [self._parse_row(line[1:])
                           for line in lines[len(head_rows):]]

    def _parse_row(self, line):
        spans = sorted([m.span() for m in inline.LINK_RE.finditer(line)] +
                       [m.span() for m in inline.PAGE_RE.finditer(line)])
        row = Table.Row()
        begin = 0
        for c in Table.CELL_SPLIT.finditer(line):
            c_span = c.span()
            span_i = bisect.bisect_left(spans, c_span)
            if span_i == 0:
                row.append(Table.Cell(inline.forge(
                    line[begin: c_span[0]].strip())))
                begin = c_span[1]
                continue
            span = spans[span_i - 1]
            if span[1] < c_span[1]:
                row.append(Table.Cell(inline.forge(
                    line[begin: c_span[0]].strip())))
                begin = c_span[1]
        row.append(Table.Cell(inline.forge(line[begin:].strip())))
        return row

    @staticmethod
    def _truncate_at(rows, limit):
        for i, row in enumerate(rows):
            for c in row.cells:
                limit -= len(c.content)
            if limit <= 0:
                return rows[:i + 1], limit
        return rows, limit

    def truncate_to(self, limit):
        limit -= len(self.caption)
        if limit <= 0:
            self.caption = ''
            del self.head_rows[:]
            del self.body_rows[:]
            return limit

        rows, limit = Table._truncate_at(self.head_rows, limit)
        if limit <= 0:
            self.head_rows = rows
            del self.body_rows[:]
            return limit

        rows, limit = Table._truncate_at(self.body_rows, limit)
        self.body_rows = rows
        return limit


class TableWithCaption(Table):
    def __init__(self, lines):
        Table.__init__(self, lines[1:])
        self.caption = lines[0][2:].strip()


class AsciiArt(Section):
    def __init__(self, lines):
        Section.__init__(self, [ln[2:] for ln in lines])

    def head(self):
        return tags.AA_BEGIN

    def tail(self):
        return tags.AA_END

    def body(self):
        return tags.BR.join([
            cgi.escape(line, quote=True).replace(' ', tags.SPACE)
            for line in self.lines])


class OneLineBlock(Block):
    def __init__(self, text):
        self.text = text

    def truncate_to(self, limit):
        return limit - len(self.text)


class Heading(OneLineBlock):
    def __init__(self, lines):
        line = lines[0]
        OneLineBlock.__init__(self, line[3:].strip())
        self.level = int(line[1: 2])

    def build(self):
        return tags.HEADING.format(
            lvl=self.level, text=inline.forge(self.text),
            anchor=template.f_encode_anchor(self.text))


class Expression(OneLineBlock):
    def __init__(self, lines):
        OneLineBlock.__init__(
            self, ''.join(filter(None, [ln[2:] for ln in lines])))

    def build(self):
        expr = mathcom.api.parse(self.text)
        return tags.EXPRESSION % (template.f_render_mathcom(expr),
                                  template.f_tojson(expr))


class LinePattern(object):
    def __init__(self, pattern_begin, pattern_end, ctor, start_exc, end_exc):
        self.begin = re.compile(pattern_begin)
        self.end = re.compile(pattern_end)
        self.ctor = ctor
        self.start_excluded = start_exc
        self.end_excluded = end_exc

LINE_PATTERNS = (
    LinePattern('[*][ ]', '(?![*][ ])', Bullets, False, False),
    LinePattern('[#][ ]', '(?![#][ ])', SortedList, False, False),
    LinePattern(r'^\|\|', r'(?![\|])', TableWithCaption, False, False),
    LinePattern(r'[\|]', r'(?![\|])', Table, False, False),
    LinePattern(r'(h|H)[1-6]\.', '', Heading, False, False),
    LinePattern(r'[$][ ][^$]+$', r'(?![$][ ])', Expression, False, False),
    LinePattern('(: |:$)', '(?!(: |:$))', AsciiArt, False, False),
    # CodeBlock is parsed when partition
)


def get_para(pattern, lines, begin):
    begin += 1 if pattern.start_excluded else 0
    end = begin + 1
    while end < len(lines) and not pattern.end.match(lines[end]):
        end += 1
    return (end + (1 if pattern.end_excluded else 0),
            pattern.ctor(lines[begin: end]))


def normal_text_from(document, begin):
    begin_pattern = match_pattern_begin(document[begin])
    if begin_pattern is not None:
        return begin_pattern, begin, None
    end = begin
    while end < len(document):
        begin_pattern = match_pattern_begin(document[end])
        if begin_pattern is not None:
            return begin_pattern, end, Paragraph(document[begin: end])
        end += 1
    return None, end, Paragraph(document[begin: end])


def match_pattern_begin(line):
    for pattern in LINE_PATTERNS:
        if pattern.begin.match(line):
            return pattern
    return None


def find_paras(document):
    cursor = 0
    while cursor < len(document):
        pattern, cursor, section = normal_text_from(document, cursor)
        if section is not None:
            yield section
        if cursor < len(document):
            cursor, section = get_para(pattern, document, cursor)
            yield section
