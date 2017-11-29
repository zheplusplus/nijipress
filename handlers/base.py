import functools
import json
from werkzeug.utils import cached_property
from google.appengine.ext import webapp

import render
from models.user import User

class BaseView(webapp.RequestHandler):
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
        render.put_page(self, template_file, template_values)

def raise_not_found(handler):
    handler.error(404)
    render.put_page(handler, 'errors/not-found.html', {})

def raise_forbidden(handler):
    handler.error(403)
    render.put_page(handler, 'errors/forbidden.html', {})

all_routes = []

class Request(object):
    def __init__(self, handler):
        self._handler = handler
        self._req = handler.request

    def get(self, key, value=None):
        return self._req.get(key, value)

    def contains(self, key):
        return key in self._req.arguments()

    def get_of_type(self, key, tp):
        try:
            return tp(self._req.get(key))
        except ValueError:
            return tp()

    def url(self):
        return self._req.url

    def cookie(self, key):
        return self._req.cookies.get(key, '')

    def put_json(self, json_obj):
        self._handler.response.out.write(json.dumps(json_obj))
        
    def put_page(self, template_file, template_values):
        render.put_page(self._handler, template_file, template_values)

    def error_page(self, status_code, template_file):
        self._handler.error(status_code)
        render.put_page(self._handler, 'errors/' + template_file, {})

    def raise_not_found(self):
        self.error_page(404, 'not-found.html')

    def raise_method_not_allowed(self):
        self.error_page(405, 'method-not-allowed.html')

    def raise_no_auth(self):
        self.error_page(401, 'no-auth.html')

    def raise_forbidden(self):
        self.error_page(403, 'forbidden.html')

    @cached_property
    def user(self):
        return User.get_by_cookie_key(request.cookie('skey'))

def get(url):
    def wrapper(f):
        class GetHandler(webapp.RequestHandler):
            def get(self, *args):
                return f(Request(self), *args)

            def post(self):
                self.error(405)
                render.put_page(self, 'errors/method-not-allowed.html', {})

        all_routes.append((url, GetHandler))
        return GetHandler
    return wrapper

def return_json(f):
    @functools.wraps(f)
    def w(request, *arg, **kwargs):
        j = f(request, *arg, **kwargs)
        request.put_json(j)
    return w

def admin_only(f):
    @functools.wraps(f)
    def w(request, *arg, **kwargs):
        if request.user is None:
            return request.raise_no_auth()
        if not request.user.admin:
            return request.raise_forbidden()
        return f(request, *arg, **kwargs)
    return w
