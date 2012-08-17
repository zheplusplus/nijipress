import os
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
import models.user
import models.admin

def render(request, template_file, template_values):
    template_values['usr'] = models.user.User.get_by_session(request)
    template_values['conf'] = models.admin.SiteConfiguration.load()
    path = os.path.join(os.path.dirname(__file__), template_file)
    return str(template.render(path, template_values).encode('utf-8'))

def page_renderer(template_file):
    class PageRender(webapp.RequestHandler):
        def get(self):
            self.response.out.write(render(self.request, template_file, dict()))
    return PageRender

def admin_page_renderer(template_file):
    base = page_renderer(template_file)
    class PageRender(base):
        @models.user.admin_only
        def get(self):
            return base.get(self)
    return PageRender

def put_page(handler, templ_file, templ_data):
    handler.response.out.write(render(handler.request, templ_file, templ_data))
