def trim_right(document):
    return reduce(lambda r, line: r + [line.rstrip()], document, [])

def generate_preview(document, size):
    content_length = 0
    result = []
    from paragraph import split_document
    for para in split_document(trim_right(document)):
        content_length += para.length()
        if size < content_length:
            break
        result.append(para)
    return reduce(lambda r, para: r + para.build(), result, [])

def forge(document):
    from paragraph import split_document
    return reduce(lambda r, para: r + para.build(),
                  split_document(trim_right(document)), [])
