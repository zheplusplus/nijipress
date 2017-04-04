from md.html import escape
from paragraph import split_document
import inline

def trim_right(document):
    return reduce(lambda r, line: r + [line.rstrip()], document, [])

def generate_preview(document, size):
    content_length = 0
    result = []
    for para in split_document(trim_right(document.split('\n'))):
        content_length += para.length()
        if size < content_length:
            break
        result.append(para)
    return reduce(lambda r, para: r + para.build(), result, [])

def forge(document):
    return reduce(lambda r, para: r + para.build(),
                  split_document(trim_right(document.split('\n'))), [])

def plain_title(text):
    return inline.plain(escape(text))

display_title = inline.forge
