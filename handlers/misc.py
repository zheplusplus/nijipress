from urlparse import urlparse
from datetime import datetime

import base
from models.post import Post
from models.tag import TagPostR

base.page_render('/about', 'about.html')

@base.get('/sitemap.*')
def get(request):
    url = urlparse(request.url())
    request.put_page('sitemap.xml', {
        'site_link': url.scheme + '://' + url.netloc,
        'tags': TagPostR.count_tags_by_name().iterkeys(),
        'posts_id_time': Post.post_id_time(),
        'last_modified': datetime.now(),
    })
