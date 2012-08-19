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

def comment_view(c):
    return {
        'email_md5': c.email_md5,
        'author': c.author,
        'url': c.url,
        'date': str(c.date),
        'content': c.esc_content,
    }

def comment_admin(c):
    return {
        'id': c.key().id(),
        'author': c.author,
        'email': c.email,
        'email_md5': c.email_md5,
        'url': c.url,
        'date': str(c.date),
        'content': c.esc_content,
        'ipaddr': c.ipaddr,
        'post_id': c.post_id,
    }
