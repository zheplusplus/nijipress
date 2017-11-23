import base
import rss
import utils.escape
import models.post

def index_page(request):
    p = request.get_of_type('page', int)
    request.put_page('index.html', {
        'posts': utils.escape.client_posts(models.post.fetch(p)),
        'tags': models.tag.sort_by_count(),
        'current_page': p,
        'page_count': xrange(models.post.count_pages()),
        'paging_on': models.post.count_pages() > 1,
    })

def by_tag(request):
    p = request.get_of_type('page', int)
    tag = request.get('tag')
    request.put_page('index.html', {
        'posts': utils.escape.client_posts(models.post.by_tag(tag, p)),
        'tags': models.tag.sort_by_count(),
        'current_page': p,
        'page_count': xrange(models.post.count_pages_by_tag(tag)),
        'query_tag': tag,
        'paging_on': models.post.count_pages_by_tag(tag) > 1,
    })

def single_post(request, post_id):
    try:
        post = models.post.by_id(post_id)
        request.put_page('post.html', {
            'page_title': utils.escape.head_title(post),
            'post': utils.escape.client_post(post),
        })
    except ValueError:
        request.raise_not_found()

@base.get('/')
def index(request):
    if request.contains('feed'):
        return rss.make_rss(request)
    if request.contains('p'):
        return single_post(request, request.get('p'))
    if request.contains('tag'):
        return by_tag(request)
    return index_page(request)

@base.get('/p/([0-9]+)')
def view_post(request, post_id):
    return single_post(request, post_id)
