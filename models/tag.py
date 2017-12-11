from collections import defaultdict
from google.appengine.ext import db

from caching import cache

class TagPostR(db.Model):
    tag = db.StringProperty(multiline=False)
    post_id = db.IntegerProperty()

    @classmethod
    @cache('tagcount')
    def count_tags_by_name(cls):
        result = defaultdict(int)
        for r in cls.all():
            result[r.tag] += 1
        return result

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
