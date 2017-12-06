import os
import jinja2
import urllib
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
templ_env.filters['urlencode'] = lambda s: urllib.quote(s.encode('utf8'))

def render(request, filename, kwargs):
    kwargs['usr'] = models.user.User.get_by_session(request)
    kwargs['conf'] = models.admin.SiteConfiguration.load()
    kwargs['global_tags'] = models.tag.sort_by_count()
    kwargs['recent_posts'] = [ utils.dumpjson.post_title(p) for p in
                            utils.escape.client_posts(models.post.fetch(0, 6)) ]
    return templ_env.get_template(filename).render(**kwargs)

def put_page(handler, templ_file, templ_data):
    handler.response.out.write(render(handler.request, templ_file, templ_data))
