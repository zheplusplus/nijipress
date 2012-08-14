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
        self.response.out.write(render.render(self.request, template_file,
                                              template_values))

def raise_not_found(view):
    view.error(404)
    view.put_page('templates/notfound.html', dict())

def raise_forbidden(view):
    view.error(403)
    view.put_page('templates/forbidden.html', dict())
