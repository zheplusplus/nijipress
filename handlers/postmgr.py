import base
import async
import utils.escape
import models.post
import md

@base.get('/c/newpost')
def get(request):
    request.put_page('new.html', {
        'is_new': True,
        'title': '',
        'content': '',
        'tags': '',
        'markdown': 'nijipress',
    })

class Preview(async.AsyncHandler):
    def serve(self):
        title = self.args['title']
        content = self.args['content']
        tags = self.args['tags']
        markdown = self.args['md']
        return {
            'title': md.process(title, markdown),
            'content': md.process(content, markdown),
            'tags': [s.strip() for s in tags.split(',')],
        }

class Receiver(async.AsyncHandler):
    @models.user.admin_only
    def serve(self):
        if 'id' in self.args:
            post_id = self.args['id']
            p = models.post.by_id(post_id)
        else:
            p = models.post.new()
            post_id = p.pid
        p.title = self.args['title']
        p.content = self.args['content']
        p.markdown = self.args['md']
        models.post.put(p, [s.strip() for s in self.args['tags'].split(',')])
        return { 'id': post_id }

@base.get('/c/posts')
def list_posts(request):
    p = request.get_of_type('page', int)
    request.put_page('list_posts.html', {
        'posts': utils.escape.client_posts(models.post.fetch(p)),
        'current_page': p,
        'page_count': xrange(models.post.count_pages()),
    })

@base.get('/c/edit')
def get(request):
    post = models.post.by_id(request.get('id'))
    request.put_page('new.html', {
        'is_new': False,
        'id': post.pid,
        'title': post.title,
        'content': post.content,
        'markdown': post.markdown or 'nijitext',
        'tags': ', '.join(post.tags),
    })
