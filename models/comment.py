from google.appengine.ext import db

import util

class Comment(db.Model):
    author = db.StringProperty(multiline=False)
    email = db.StringProperty(multiline=False)
    url = db.StringProperty(multiline=False)
    content = db.StringProperty(multiline=True)
    date = db.DateTimeProperty(auto_now_add=True)
    ipaddr = db.StringProperty(multiline=False)
    post_id = db.IntegerProperty()

def count_pages():
    return util.count_pages(db.GqlQuery('SELECT __key__ FROM Comment').count())

def fetch(page=0, count=util.ITEMS_PER_PAGE):
    return db.GqlQuery('SELECT * FROM Comment ORDER BY date DESC').fetch(
                                count, count * page)

def by_post_id(post_id):
    return db.GqlQuery('SELECT * FROM Comment WHERE post_id = :1 ORDER BY date',
                       post_id)
