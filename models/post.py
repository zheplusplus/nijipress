from google.appengine.ext import db
from google.appengine.api import memcache

import util
import tag
import caching

class Post(db.Model):
    pid = db.IntegerProperty(indexed=True)
    date = db.DateTimeProperty(auto_now_add=True)
    date_update = db.DateTimeProperty(auto_now=True)
    title = db.StringProperty(multiline=False)
    content = db.TextProperty()
    markdown = db.StringProperty(multiline=False)

    def init_tags(self, tags):
        self.tags = tags
        return self

    def fix_fields(self):
        # Since v1.1.0
        if self.date_update is None:
            self.date_update = self.date
        # Since v1.1.0
        if self.markdown is None:
            self.markdown = 'nijitext'
        return self

    @classmethod
    @caching.cache('post_id_time')
    def post_id_time(cls):
        return [{
            'pid': p.pid,
            'date_update': p.fix_fields().date_update,
        } for p in cls.all()]

def new():
    p = Post()
    p.title = ''
    p.tags = []
    p.content = ''
    posts = db.Query(Post).order('-pid').fetch(limit=1)
    if len(posts) == 0:
        p.pid = 0
    else:
        p.pid = posts[0].pid + 1
    return p

def fetch(page, count=util.ITEMS_PER_PAGE):
    start = util.ITEMS_PER_PAGE * page
    CACHE_SIZE = util.ITEMS_PER_PAGE * 2

    def fetch_posts(start_index, count):
        if count <= 0:
            return []
        return [p.init_tags(tag.tags_by_post_id(p.pid)) for p in
                      db.Query(Post).order('-date')
                                    .fetch(count, offset=start_index)]

    def cache_posts(start_index, count):
        if count <= 0:
            return []
        cache = memcache.get('posts')
        if cache == None:
            cache = fetch_posts(0, CACHE_SIZE)
            memcache.set('posts', cache)
        return cache[start_index: count + start_index]

    cache_count = CACHE_SIZE - start
    if count < cache_count:
        cache_count = count
    fetch_start = CACHE_SIZE if start < CACHE_SIZE else start
    result = (cache_posts(start, cache_count) +
              fetch_posts(fetch_start, count - cache_count))
    return [p.fix_fields() for p in result]

def count_pages():
    return util.count_pages(db.Query(Post).count())

def count_pages_by_tag(t):
    return util.count_pages(db.Query(tag.TagPostR).filter('tag =', t).count())

def by_id(ident):
    post_id = int(ident)
    posts = db.Query(Post).filter('pid =', post_id)
    if posts.count() == 0:
        raise ValueError('no such post')
    return posts[0].init_tags(tag.tags_by_post_id(post_id)).fix_fields()

def by_tag(t, page=0, count=util.ITEMS_PER_PAGE):
    post_ids = [r.post_id for r in db.Query(tag.TagPostR).filter('tag =', t)]
    post_ids = sorted(post_ids, reverse=True)[count * page: count * (page + 1)]
    return [post.init_tags(tag.tags_by_post_id(post.pid)).fix_fields()
            for post in db.Query(Post).filter('pid in', post_ids).order('-date')]

def put(post, tags):
    tags = filter(lambda t: len(t) > 0, map(lambda t: t.strip(), tags))
    post.put()
    tag.update_relations(post.pid, tags)
    _invalidate_cache()

def posts_ids():
    return _load_posts_ids()

def _invalidate_cache():
    memcache.delete('posts')
    caching.flush_all()

@caching.cache('posts_ids')
def _load_posts_ids():
    return [p.pid for p in Post.all()]
