def post_title(p):
    return {
        'id': p.pid,
        'title': p.title,
    }

def post_preview(p):
    return dict({
        'preview': p.preview,
    }.items() + post_title(p).items())

def post_full(p):
    return dict({
        'content': p.content,
    }.items() + post_title(p).items())
