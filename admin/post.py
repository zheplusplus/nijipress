import base
import persist
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
                'prepared_title': base.escape_title(title),
                'prepared_content': base.escape_content(content),
                'prepared_tags': [s.strip() for s in tags.split(',')],
                'usr': usr,
            })

class Add(base.BaseView):
    def post(self):
        post = persist.post_by_id(self.request.get('id'))
        usr = admin.User.get_by_session(self.request)
        if usr.admin:
            post.title = self.request.get('title')
            post.content = self.request.get('content')
            post.preview = base.escape_preview(post.content)
            tags = self.request.get('tags')
            persist.put_post(post, [s.strip() for s in tags.split(',')])
            self.redirect('/c/posts')
        else:
            base.raise_forbidden(self)

class List(base.BaseView):
    def get(self):
        p = self.request_value('page', int)
        self.put_page('templates/list_posts.html', {
                'posts': base.posts_for_client(persist.fetch_posts(p)),
                'current_page': p,
                'page_count': xrange(persist.total_posts_page_count()),
            })

class Edit(base.BaseView):
    def get(self):
        post = persist.post_by_id(self.request.get('id'))
        self.put_page('templates/new.html', {
                'is_new': False,
                'id': post.pid,
                'title': post.title,
                'content': post.content,
                'tags': ', '.join(post.tags),
            })
