from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

import persist
import admin.model as admin

def escape_content(content):
    from markdown import entire_doc
    return ''.join(entire_doc.forge(content.split('\n')))

def escape_title(title):
    from markdown import html
    return html.escape(title)

def escape_preview(content):
    from markdown.entire_doc import generate_preview
    return ''.join(generate_preview(content.split('\n')))

def post_for_client(post):
    post.title = escape_title(post.title)
    post.content = escape_content(post.content)
    from conf import build_post_link
    post.ident = build_post_link(post.pid)
    return post

def posts_for_client(origin_posts):
    return map(lambda p: post_for_client(p), origin_posts)

class BaseView(webapp.RequestHandler):
    def get(self):
        raise_not_found(self)

    def post(self):
        raise_not_found(self)

    def put_page(self, template_file, template_value=dict()):
        import os
        usr = admin.User.get_by_session(self.request)
        template_value['usr'] = usr
        template_value['style'] = 'midnight'
        path = os.path.join(os.path.dirname(__file__), template_file)
        self.response.out.write(template.render(path, template_value))

class NotFound(BaseView):
    pass

def raise_not_found(view):
    view.error(404)
    view.put_page('templates/notfound.html', {
            'posts': posts_for_client(persist.fetch_posts(0, 5)),
        })

def raise_forbidden(view):
    view.error(403)
    view.put_page('templates/forbidden.html', {
            'posts': posts_for_client(persist.fetch_posts(0, 5)),
        })
