from google.appengine.ext import db

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
        u = db.GqlQuery('SELECT * FROM User WHERE name = :1', name)
        if u.count() == 0:
            return User.new(name)
        return u[0]

    @staticmethod
    def get_by_session(request):
        key = request.cookies['skey'] if 'skey' in request.cookies else ''
        u = db.GqlQuery('SELECT * FROM User WHERE session_key = :1', key)
        if u.count() == 0:
            return User.new('')
        return u[0]
