from urlparse import urlparse
from datetime import datetime

import base
import models
from models.post import Post

base.page_render('/about', 'about.html')

@base.get('/sitemap.*')
def get(request):
    url = urlparse(request.url())
    Post.post_id_time()
    request.put_page('sitemap.xml', {
        'site_link': url.scheme + '://' + url.netloc,
        'tags': models.tag.sort_by_count(),
        'posts_id_time': Post.post_id_time(),
        'last_modified': datetime.now(),
    })
