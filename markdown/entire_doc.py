from inline import plain
import html
from paragraph import split_document

def trim_right(document):
    return reduce(lambda r, line: r + [line.rstrip()], document, [])

def generate_preview(document, size):
    content_length = 0
    result = []
    for para in split_document(trim_right(document)):
        content_length += para.length()
        if size < content_length:
            break
        result.append(para)
    return reduce(lambda r, para: r + para.build(), result, [])

def forge(document):
    return reduce(lambda r, para: r + para.build(),
                  split_document(trim_right(document)), [])

def plain_title(text):
    return plain(html.forge(text))
