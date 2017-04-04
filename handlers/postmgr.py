import base
import async
import utils.escape
import models.post
import models.admin

@base.get('/c/post')
def get(request):
    request.put_page('new.html', {
        'is_new': True,
        'title': '',
        'content': '',
        'tags': '',
    })

class Preview(async.AsyncHandler):
    def serve(self):
        title = self.args['title']
        content = self.args['content']
        tags = self.args['tags']
        return {
            'title': utils.escape.esc_content(title),
            'content': utils.escape.esc_content(content),
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
        models.post.put(p, [s.strip() for s in self.args['tags'].split(',')])
        return { 'id': post_id }

@base.get('/c/posts')
def get(request):
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
        'tags': ', '.join(post.tags),
    })
