import base
import persist

class Build(base.BaseView):
    def get(self):
        from conf import SITE_LINK, TITLE, DESCRIPTION
        self.put_page('templates/feed.xml', {
                'title': TITLE,
                'description': DESCRIPTION,
                'site_link': SITE_LINK,
                'posts': base.posts_for_client(persist.fetch_posts()),
            })
