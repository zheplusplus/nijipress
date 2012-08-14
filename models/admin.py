from google.appengine.ext import db
from google.appengine.api import memcache

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
            return User.new(name)
        return u[0]

    @staticmethod
    def get_by_session(request):
        key = request.cookies['skey'] if 'skey' in request.cookies else ''
        u = db.Query(User).filter('session_key =', key)
        if u.count() == 0:
            return User.new('')
        return u[0]

class SiteConfiguration(db.Model):
    title = db.StringProperty(multiline=False)
    style = db.StringProperty(multiline=False)
    rss_uri = db.StringProperty(multiline=False)
    rss_description = db.StringProperty(multiline=False)
    analytics_code = db.StringProperty(multiline=False)
    analytics_domain = db.StringProperty(multiline=False)
    post_html = db.TextProperty()

    @staticmethod
    def load_persist():
        conf = SiteConfiguration.all()
        if conf.count() == 0:
            conf = SiteConfiguration()
            conf.title = 'A NijiPress Site'
            conf.style = 'midnight'
            conf.rss_uri = '/rss'
            conf.rss_description = ''
            conf.analytics_code = ''
            conf.post_html = ''
            return conf
        return conf[0]

    @staticmethod
    def load():
        cache = memcache.get('psiteconf')
        if cache == None:
            cache = SiteConfiguration.load_persist()
            memcache.set('psiteconf', cache)
        return cache

    @staticmethod
    def save(conf):
        memcache.set('psiteconf', conf)
        conf.put()

    def blogrolls(self):
        return Blogroll.load()

class Blogroll(db.Model):
    uri = db.StringProperty(multiline=False)
    text = db.StringProperty(multiline=False)

    @staticmethod
    def add_by_text(text):
        for line in text.split('\n'):
            line = line.strip()
            if len(line) == 0:
                continue
            r = line.partition('<')
            blogroll = Blogroll()
            blogroll.uri = r[0].strip()
            blogroll.text = r[2].strip()
            blogroll.put()
        memcache.delete('pblogrolls')

    @staticmethod
    def load():
        cache = memcache.get('pblogrolls')
        if cache == None:
            cache = Blogroll.all()
            memcache.set('pblogrolls', cache)
        return cache
