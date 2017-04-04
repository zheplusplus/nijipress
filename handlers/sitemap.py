from urlparse import urlparse

import base
import models

@base.get('/sitemap.*')
def get(request):
    url = urlparse(request.url())
    request.put_page('sitemap.xml', {
        'site_link': url.scheme + '://' + url.netloc,
        'tags': models.tag.sort_by_count(),
        'posts_ids': models.post.posts_ids(),
    })
