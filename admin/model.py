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

class SiteConfiguration(db.Model):
    title = db.StringProperty(multiline=False)
    style = db.StringProperty(multiline=False)
    rss_uri = db.StringProperty(multiline=False)
    rss_description = db.StringProperty(multiline=False)
    analytics_code = db.StringProperty(multiline=False)
    analytics_domain = db.StringProperty(multiline=False)
    post_html = db.StringProperty(multiline=True)

    @staticmethod
    def _load_cache():
        conf = SiteConfiguration.all()
        if conf.count() == 0:
            conf = SiteConfiguration()
            conf.title = 'A NijiPress Site'
            conf.style = 'midnight'
            conf.rss_uri = '/rss'
            conf.rss_description = ''
            conf.analytics_code = ''
            cont.post_html = ''
            return conf
        return conf[0]

    @staticmethod
    def load():
        cache = memcache.get('siteconf')
        if cache == None:
            cache = SiteConfiguration._load_cache()
            memcache.set('siteconf', cache)
        return cache

    @staticmethod
    def save(conf):
        memcache.set('siteconf', conf)
        conf.put()
