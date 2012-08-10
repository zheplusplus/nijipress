from google.appengine.ext import db
from google.appengine.api import memcache

class TagPostR(db.Model):
    tag = db.StringProperty(multiline=False)
    post_id = db.IntegerProperty()

def _put_relation(tag, post_id):
    if db.Query(TagPostR).filter('tag =', tag
                        ).filter('post_id =', post_id).count() == 0:
        r = TagPostR()
        r.tag = tag
        r.post_id = post_id
        r.put()

def _relations_by_post_id(post_id):
    return db.Query(TagPostR).filter('post_id =', post_id)

def tags_by_post_id(post_id):
    return [r.tag for r in _relations_by_post_id(post_id)]

def update_relations(post_id, tags):
    for r in _relations_by_post_id(post_id):
        if not r.tag in tags:
            r.delete()
    for tag in tags:
        _put_relation(tag, post_id)

def sort_by_count():
    cache = memcache.get('tags')
    if cache == None:
        cache = _load_cache()
        memcache.set('tags', cache)
    return cache

def _load_cache():
    tags = dict()
    max_tag_count = 1
    for r in TagPostR.all():
        tags[r.tag] = tags[r.tag] + 1 if r.tag in tags else 0
        if tags[r.tag] > max_tag_count:
            max_tag_count = tags[r.tag]
    return sorted([{
        'name': n,
        'rate': (0.0 + c) / max_tag_count,
    } for n, c in tags.iteritems()], key=lambda tag: tag['name'])
