import re

import tags
import inline
import paragraph

SECTION_SPLIT_PAT = re.compile('\n\n+')
CODE_BLOCK_BEGIN_PAT = re.compile('\n{{{[ ]*[a-zA-Z0-9]*\n')
CODE_BLOCK_END_PAT = '\n}}}'
CODE_LINE_LEADING_SPACE_PAT = re.compile('(?P<s>(^[ ]+))')


class CodeBlock(paragraph.Section):
    def __init__(self, part):
        lines = part.split('\n')
        paragraph.Section.__init__(self, lines[1:])
        self.lang = lines[0][3:].strip()

    def head(self):
        return (tags.CODE_BLOCK_BEGIN % self.lang if self.lang
                else tags.CODE_BLOCK_BEGIN_MONOCHR)

    def tail(self):
        return tags.CODE_BLOCK_END

    def body(self):
        return tags.BR.join([CODE_LINE_LEADING_SPACE_PAT.sub(
            lambda m: tags.SPACE * len(m.group('s')), inline.forge(line)
        ) for line in self.lines])


def partition(doc):
    begin = 0
    for cb_match in CODE_BLOCK_BEGIN_PAT.finditer(doc):
        start = cb_match.start()
        before, after = doc[begin: start].strip(), doc[start:]
        if before:
            for sec in filter(None, SECTION_SPLIT_PAT.split(before)):
                for para in paragraph.find_paras(sec.split('\n')):
                    yield para
        cb_end = after.find(CODE_BLOCK_END_PAT)
        if -1 == cb_end:
            cb_end = len(after)
        yield CodeBlock(after[: cb_end].strip())

        begin = cb_end + len(CODE_BLOCK_END_PAT) + start

    for sec in filter(None, SECTION_SPLIT_PAT.split(doc[begin:])):
        for para in paragraph.find_paras(sec.split('\n')):
            yield para


def compile_entire(doc):
    return ''.join([p.build() for p in partition(doc)])


def compile_partial(doc, limit):
    def truncate(limit):
        result = []
        for para in partition(doc):
            limit = para.truncate_to(limit)
            if limit < 0 and result:
                return result, False
            result.append(para)
        return result, True
    paras, complete = truncate(limit)
    return ''.join([p.build() for p in paras]), complete
