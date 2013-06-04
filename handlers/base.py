from google.appengine.ext import webapp
import render

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
    render.put_page(handler, 'notfound.html', dict())

def raise_forbidden(handler):
    handler.error(403)
    render.put_page(handler, 'forbidden.html', dict())
