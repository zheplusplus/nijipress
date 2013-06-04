import os
import jinja2
import urllib
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
import models.user
import models.admin

def strftime(dt, fmt):
    if not dt:
        return ''
    return dt.strftime(fmt.encode('utf-8')).decode('utf-8')

templ_env = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), 'templates')))
templ_env.filters['strftime'] = strftime
templ_env.filters['urlencode'] = urllib.quote

def render(request, filename, kwargs):
    kwargs['usr'] = models.user.User.get_by_session(request)
    kwargs['conf'] = models.admin.SiteConfiguration.load()
    return templ_env.get_template(filename).render(**kwargs)

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
