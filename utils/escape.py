import hashlib
import markdown
import markdown.inline
import markdown.html
import markdown.entire_doc

def esc_content(content):
    return ''.join(markdown.entire_doc.forge(content.split('\n')))

def esc_title_plain(title):
    return markdown.entire_doc.plain_title(title)

def esc_preview(content):
    return ''.join(markdown.entire_doc.generate_preview(content.split('\n'),
                                                        1729))

def client_post(post):
    post.title = esc_content(post.title)
    post.preview = esc_preview(post.content)
    post.content = esc_content(post.content)
    return post

def client_posts(origin_posts):
    return map(lambda p: client_post(p), origin_posts)

def client_comment(c):
    c.email_md5 = hashlib.md5(c.email).hexdigest()
    c.esc_content = esc_content(c.content)
    return c

def client_comments(comments):
    return [client_comment(c) for c in comments]
