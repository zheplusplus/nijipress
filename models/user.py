from google.appengine.ext import db
import handlers.base

class User(db.Model):
    name = db.StringProperty(multiline=False)
    passwd = db.StringProperty(multiline=False)
    session_key = db.StringProperty(multiline=False)
    admin = db.BooleanProperty()

    @staticmethod
    def new(name):
        usr = User()
        usr.name = name
        usr.passwd = ''
        usr.admin = False
        return usr

    @staticmethod
    def get_by_name(name):
        u = db.Query(User).filter('name =', name)
        if u.count() == 0:
            return None
        return u[0]

    @staticmethod
    def get_admin():
        u = db.Query(User).filter('admin =', True)
        if u.count() == 0:
            return None
        return u[0]

    @staticmethod
    def get_by_session(request):
        key = request.cookies['skey'] if 'skey' in request.cookies else ''
        u = db.Query(User).filter('session_key =', key)
        if u.count() == 0:
            return User.new('')
        return u[0]

def admin_only(f):
    def wrapper(handler):
        if not User.get_by_session(handler.request).admin:
            return handlers.base.raise_forbidden(handler)
        return f(handler)
    return wrapper
