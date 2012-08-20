from google.appengine.ext import db
from google.appengine.api import memcache

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
            conf.analytics_domain = ''
            conf.post_html = ''
            return conf
        return conf[0]

    @staticmethod
    def load():
        cache = memcache.get('siteconf-ura')
        if cache == None:
            cache = SiteConfiguration.load_persist()
            memcache.set('siteconf-ura', cache)
        return cache

    @staticmethod
    def save(conf):
        memcache.set('siteconf-ura', conf)
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
        memcache.delete('blogrolls-ura')

    @staticmethod
    def load():
        cache = memcache.get('blogrolls-ura')
        if cache == None:
            cache = Blogroll.all()
            memcache.set('blogrolls-ura', cache)
        return cache
