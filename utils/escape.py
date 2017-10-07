import hashlib
import md
import md.nijitext.entire_doc as comment_md

def esc_content(content):
    return ''.join(comment_md.forge(content.split('\n')))

def head_title(post):
    markdown = md.get(post.markdown)
    return markdown.head_title(post.title)

def client_post(post):
    markdown = md.get(post.markdown)
    return markdown.process_post(post)

def client_posts(posts):
    return [client_post(p) for p in posts]

def client_comment(c):
    c.email_md5 = hashlib.md5(c.email).hexdigest()
    c.esc_content = esc_content(c.content)
    return c

def client_comments(comments):
    return [client_comment(c) for c in comments]
