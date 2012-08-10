import os
import hashlib
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
import models
import admin.model as admin
import utils.escape

def comments_for_client(comments):
    def client_comment(c):
        c.email_md5 = hashlib.md5(c.email).hexdigest()
        c.esc_content = utils.escape.esc_content(c.content)
        return c
    return [client_comment(c) for c in comments]

class RootHandler(webapp.RequestHandler):
    def render(self, template_file, template_values):
        template_values['usr'] = admin.User.get_by_session(self.request)
        template_values['conf'] = admin.SiteConfiguration.load()
        path = os.path.join(os.path.dirname(__file__), template_file)
        return str(template.render(path, template_values).encode('utf-8'))

def page_renderer(template_file):
    class PageRender(RootHandler):
        def get(self):
            self.response.out.write(self.render(template_file, dict()))
    return PageRender

class BaseView(RootHandler):
    def get(self):
        raise_not_found(self)

    def post(self):
        raise_not_found(self)

    def request_value(self, key, wanted_type):
        try:
            return wanted_type(self.request.get(key))
        except ValueError:
            return wanted_type()

    def put_page(self, template_file, template_values):
        self.response.out.write(self.render(template_file, template_values))

class NotFound(BaseView):
    pass

def raise_not_found(view):
    view.error(404)
    view.put_page('templates/notfound.html', dict())

def raise_forbidden(view):
    view.error(403)
    view.put_page('templates/forbidden.html', dict())
