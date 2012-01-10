from google.appengine.ext import db

class Post(db.Model):
    pid = db.IntegerProperty()
    date = db.DateTimeProperty(auto_now_add=True)
    title = db.StringProperty(multiline=False)
    content = db.TextProperty()
    preview = db.TextProperty()

    def init_tags(self, tags):
        self.tags = tags
        return self

    def init_id(self):
        posts = db.GqlQuery('SELECT * FROM Post ORDER BY pid DESC')
        if posts.count() == 0:
            self.pid = 0
        else:
            self.pid = posts[0].pid + 1
        return self

POSTS_PER_PAGE = 16

def page_count(count):
    return (count + POSTS_PER_PAGE - 1) / POSTS_PER_PAGE

def fetch_posts(page=0, count=POSTS_PER_PAGE):
    return [post.init_tags(tags_by_post_id(post.pid)) for post in
       db.GqlQuery('SELECT * FROM Post ORDER BY date DESC').fetch(count,
                                                                  count * page)]

def total_posts_page_count():
    return page_count(db.GqlQuery('SELECT __key__ FROM Post').count())

def post_by_id(ident):
    try:
        post_id = int(ident)
        posts = db.GqlQuery('SELECT * FROM Post WHERE pid = :1', post_id)
        if posts.count() == 0:
            raise ValueError('no such post')
    	return posts[0].init_tags(tags_by_post_id(post_id))
    except ValueError:
        return Post().init_tags([]).init_id()

def posts_by_tag(tag, page=0, count=POSTS_PER_PAGE):
    post_ids = [r.post_id for r in
                      db.GqlQuery('SELECT * FROM TagPostR WHERE tag = :1', tag)]
    return [post.init_tags(tags_by_post_id(post.pid)) for post in
                      db.Query(Post).filter('pid in', post_ids).order('-date')
                                    .fetch(count, count * page)]

def total_posts_page_count_by_tag(tag):
    return page_count(db.GqlQuery('SELECT __key__ FROM TagPostR WHERE tag = :1',
                                  tag).count())

def put_post(post, tags):
    post.put()
    update_relations(post.pid, tags)

class TagPostR(db.Model):
    tag = db.StringProperty(multiline=False)
    post_id = db.IntegerProperty()

def put_tag_post_relation(tag, post_id):
    if db.GqlQuery('SELECT * FROM TagPostR WHERE tag = :1 AND post_id = :2',
                   tag, post_id).count() == 0:
        r = TagPostR()
        r.tag = tag
        r.post_id = post_id
        r.put()

def relations_by_post_id(post_id):
    return db.GqlQuery('SELECT * FROM TagPostR WHERE post_id = :1', post_id)

def tags_by_post_id(post_id):
    return [r.tag for r in relations_by_post_id(post_id)]

def update_relations(post_id, tags):
    for r in relations_by_post_id(post_id):
        if not r.tag in tags:
            r.delete()
    for tag in tags:
        put_tag_post_relation(tag, post_id)

def all_tags():
    class Tag:
        def __init__(self, name, rate):
            self.name = name
            self.rate = rate
    tags = dict()
    max_tag_count = 1
    for r in db.GqlQuery('SELECT * FROM TagPostR'):
        tags[r.tag] = tags[r.tag] + 1 if r.tag in tags else 0
        if tags[r.tag] > max_tag_count:
            max_tag_count = tags[r.tag]
    return sorted([Tag(n, 0.8 + 1.2 * c / max_tag_count) for n, c in
                                 tags.iteritems()], key=lambda tag: tag.name)

class Comment(db.Model):
    author = db.StringProperty(multiline=False)
    email = db.StringProperty(multiline=False)
    url = db.StringProperty(multiline=False)
    content = db.StringProperty(multiline=True)
    date = db.DateTimeProperty(auto_now_add=True)
    ipaddr = db.StringProperty(multiline=False)
    post_id = db.IntegerProperty()

def recent_comments(page=0, count=16):
    return db.GqlQuery('SELECT * FROM Comment ORDER BY date DESC').fetch(
                                count, count * page)

def comments_for_post(post_id):
    return db.GqlQuery('SELECT * FROM Comment WHERE post_id = :1 ORDER BY date',
                       post_id)
