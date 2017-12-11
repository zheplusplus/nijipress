from urlparse import urlparse

import base
import utils.escape
import models.post
from models.caching import cache
from models.admin import SiteConfiguration

def rss_post(post, url):
    post.plain_title = utils.escape.head_title(post)
    post.ident = ''.join([url.scheme, '://', url.netloc, '/p/', str(post.pid)])
    post = utils.escape.client_post(post)
    return post

@cache('rss_posts')
def rss_posts(origin_posts, url):
    return map(lambda p: rss_post(p, url), origin_posts)

def make_rss(request):
    items_count = models.admin.SiteConfiguration.load().rss_items_count or 0
    url = urlparse(request.url())
    request.put_page('feed.xml', {
        'site_link': url.scheme + '://' + url.netloc,
        'posts': rss_posts(models.post.fetch(0, items_count), url),
    })

@base.get('/rss')
def rss(request):
    return make_rss(request)
