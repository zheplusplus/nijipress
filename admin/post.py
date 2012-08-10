import base
import utils.escape
import models.post
import admin.model as admin

class NewPost(base.BaseView):
    def get(self):
        self.put_page('templates/new.html', {
                'is_new': True,
                'title': '',
                'content': '',
                'tags': '',
            })

class Preview(base.BaseView):
    def post(self):
        ident = self.request.get('id')
        title = self.request.get('title')
        content = self.request.get('content')
        tags = self.request.get('tags')
        usr = admin.User.get_by_session(self.request)
        self.put_page('templates/preview.html', {
                'id': ident,
                'title': title,
                'content': content,
                'tags': tags,
                'prepared_title': utils.escape.esc_content(title),
                'prepared_content': utils.escape.esc_content(content),
                'prepared_tags': [s.strip() for s in tags.split(',')],
                'usr': usr,
            })

class Add(base.BaseView):
    def post(self):
        if not admin.User.get_by_session(self.request).admin:
            return base.raise_forbidden(self)
        post_id = self.request.get('id')
        p = None
        try:
            p = models.post.by_id(post_id)
        except ValueError:
            p = models.post.new()
            post_id = str(p.pid)
        p.title = self.request.get('title')
        p.content = self.request.get('content')
        tags = self.request.get('tags')
        models.post.put(p, [s.strip() for s in tags.split(',')])
        self.redirect('/?p=' + post_id)

class List(base.BaseView):
    def get(self):
        p = self.request_value('page', int)
        self.put_page('templates/list_posts.html', {
                'posts': utils.escape.client_posts(models.post.fetch(p)),
                'current_page': p,
                'page_count': xrange(models.post.count_pages()),
            })

class Edit(base.BaseView):
    def get(self):
        post = models.post.by_id(self.request.get('id'))
        self.put_page('templates/new.html', {
                'is_new': False,
                'id': post.pid,
                'title': post.title,
                'content': post.content,
                'tags': ', '.join(post.tags),
            })
