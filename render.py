import os
import jinja2
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

import models.user
import models.admin
import models.tag
import models.post
import utils.dumpjson
import utils.escape

def strftime(dt, fmt):
    if not dt:
        return ''
    return dt.strftime(fmt.encode('utf-8')).decode('utf-8')

templ_env = jinja2.Environment(loader=jinja2.FileSystemLoader(
                        os.path.join(os.path.dirname(__file__), 'templates')))
templ_env.filters['strftime'] = strftime
templ_env.filters['urlencode'] = utils.escape.urlencode

def render(request, filename, kwargs):
    kwargs['usr'] = models.user.User.get_by_session(request)
    kwargs['conf'] = models.admin.SiteConfiguration.load()
    return templ_env.get_template(filename).render(**kwargs)

def put_page(handler, templ_file, templ_data):
    handler.response.out.write(render(handler.request, templ_file, templ_data))
