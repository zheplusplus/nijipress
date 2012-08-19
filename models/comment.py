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
    return util.count_pages(db.Query(Comment).count())

def fetch(start):
    return db.Query(Comment).order('-date').fetch(util.ITEMS_PER_PAGE, start)

def by_post_id(post_id):
    return db.Query(Comment).filter('post_id =', post_id).order('date')

def _copy_comment(dest, src):
    dest.author = src.author
    dest.email = src.email
    dest.url = src.url
    dest.content = src.content
    dest.date = src.date
    dest.ipaddr = src.ipaddr
    dest.post_id = src.post_id

def put(comment):
    tokens = db.Query(AllowedToken).filter('token =', comment.ctoken)
    if tokens.count() > 0:
        comment.approve(tokens[0])
        return True
    comment.put()
    return False

class AllowedToken(db.Model):
    token = db.StringProperty(multiline=False)
    last_update = db.DateTimeProperty(auto_now_add=True)

class PendingComment(db.Model):
    author = db.StringProperty(multiline=False)
    email = db.StringProperty(multiline=False)
    url = db.StringProperty(multiline=False)
    content = db.StringProperty(multiline=True)
    date = db.DateTimeProperty(auto_now_add=True)
    ipaddr = db.StringProperty(multiline=False)
    post_id = db.IntegerProperty()
    ctoken = db.StringProperty(multiline=False)

    def approve(self, token=None):
        if token == None:
            token = AllowedToken()
            token.token = self.ctoken
        token.last_update = self.date
        token.put()
        comment = Comment()
        _copy_comment(comment, self)
        comment.put()
        if self.is_saved(): self.delete()
