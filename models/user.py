from google.appengine.ext import ndb
import handlers.base

class User(ndb.Model):
    name = ndb.StringProperty()
    passwd = ndb.StringProperty()
    session_key = ndb.StringProperty()
    admin = ndb.BooleanProperty()

    @staticmethod
    def new(name):
        usr = User()
        usr.name = name
        usr.passwd = ''
        usr.admin = False
        return usr

    @staticmethod
    def get_by_name(name):
        return User.query(User.name == name).get()

    @staticmethod
    def get_admin():
        return User.query(User.admin == True).get()

    @staticmethod
    def get_by_session(request):
        key = request.cookies['skey'] if 'skey' in request.cookies else ''
        u = User.query(User.session_key == key).get()
        if u is None:
            return User.new('')
        return u

    @staticmethod
    def get_by_cookie_key(key):
        return User.query(User.session_key == key).get()

def admin_only(f):
    def wrapper(handler):
        if not User.get_by_session(handler.request).admin:
            return handlers.base.raise_forbidden(handler)
        return f(handler)
    return wrapper
