import base
import utils.escape
import models.post
import models.comment

def index_page(view):
    p = view.request_value('page', int)
    view.put_page('index.html', {
        'posts': utils.escape.client_posts(models.post.fetch(p)),
        'tags': models.tag.sort_by_count(),
        'current_page': p,
        'page_count': xrange(models.post.count_pages()),
        'paging_on': models.post.count_pages() > 1,
    })

def by_tag(view):
    p = view.request_value('page', int)
    tag = view.request.get('tag')
    view.put_page('index.html', {
        'posts': utils.escape.client_posts(models.post.by_tag(tag, p)),
        'tags': models.tag.sort_by_count(),
        'current_page': p,
        'page_count': xrange(models.post.count_pages_by_tag(tag)),
        'query_tag': tag,
        'paging_on': models.post.count_pages_by_tag(tag) > 1,
    })

def single_post(view):
    try:
        post = models.post.by_id(view.request.get('p'))
        view.put_page('post.html', {
            'page_title': utils.escape.esc_title_plain(post.title),
            'post': utils.escape.client_post(post),
        })
    except ValueError:
        base.raise_not_found(view)

class Index(base.BaseView):
    def get(self):
        if 'feed' in self.request.arguments():
            return self.redirect('http://rss.bitfoc.us/')
        if 'p' in self.request.arguments():
            return single_post(self)
        if 'tag' in self.request.arguments():
            return by_tag(self)
        return index_page(self)
