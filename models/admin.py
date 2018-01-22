from google.appengine.ext import ndb
from google.appengine.api import memcache

SITECONF_CACHE_KEY = 'siteconf_v110'
BLOGROLL_CACHE_KEY = 'blogrool_v110'

class SiteConfiguration(ndb.Model):
    title = ndb.StringProperty()
    style = ndb.StringProperty()
    rss_uri = ndb.StringProperty()
    rss_description = ndb.StringProperty()
    rss_items_count = ndb.IntegerProperty()
    analytics_code = ndb.StringProperty()
    analytics_domain = ndb.StringProperty()
    post_html = ndb.TextProperty()

    def fix_fields(self):
        # Since v1.1.0
        if self.rss_items_count is None:
            self.rss_items_count = 0
        return self

    @staticmethod
    def load_persist():
        conf = SiteConfiguration.query().get()
        if conf is None:
            conf = SiteConfiguration()
            conf.title = 'A NijiPress Site'
            conf.style = 'midnight'
            conf.rss_uri = '/rss'
            conf.rss_items_count = 0
            conf.rss_description = ''
            conf.analytics_code = ''
            conf.analytics_domain = ''
            conf.post_html = ''
        return conf

    @staticmethod
    def load():
        cache = memcache.get(SITECONF_CACHE_KEY)
        if cache == None:
            cache = SiteConfiguration.load_persist()
            memcache.set(SITECONF_CACHE_KEY, cache)
        return cache.fix_fields()

    @staticmethod
    def save(conf):
        memcache.set(SITECONF_CACHE_KEY, conf)
        conf.put()

    def blogrolls(self):
        return Blogroll.load()

class Blogroll(ndb.Model):
    uri = ndb.StringProperty()
    text = ndb.StringProperty()

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
        memcache.delete(BLOGROLL_CACHE_KEY)

    @staticmethod
    def load():
        cache = memcache.get(BLOGROLL_CACHE_KEY)
        if cache == None:
            cache = list(Blogroll.query())
            memcache.set(BLOGROLL_CACHE_KEY, cache)
        return cache
