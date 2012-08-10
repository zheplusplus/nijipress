import base
import models
from urlparse import urlparse

class Build(base.BaseView):
    def get(self):
        url = urlparse(self.request.url)
        self.put_page('templates/sitemap.xml', {
                'site_link': url.scheme + '://' + url.netloc,
                'tags': models.tag.sort_by_count(),
                'posts_ids': models.post.posts_ids(),
            })
