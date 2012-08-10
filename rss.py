import base
import utils.escape
import models
from urlparse import urlparse

def post_for_client(post, url):
    post = utils.escape.client_post(post)
    post.ident = ''.join([url.scheme, '://', url.netloc, '/?p=', str(post.pid)])
    return post

def posts_for_client(origin_posts, url):
    return map(lambda p: post_for_client(p, url), origin_posts)

class Build(base.BaseView):
    def get(self):
        url = urlparse(self.request.url)
        self.put_page('templates/feed.xml', {
                'site_link': url.scheme + '://' + url.netloc,
                'posts': posts_for_client(models.post.fetch(), url),
            })
