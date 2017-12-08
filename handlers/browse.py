import base
import rss
import utils.escape
import models.post

@base.get('/')
def index(request):
    if request.contains('feed'):
        return rss.make_rss(request)
    if request.contains('p'):
        return request.redirect('/p/%s' % request.get('p'))
    if request.contains('tag'):
        return request.redirect('/tag/%s' % request.get('tag'))

    p = request.get_of_type('page', int)
    request.put_page('index.html', {
        'posts': utils.escape.client_posts(models.post.fetch(p)),
        'tags': models.tag.sort_by_count(),
        'current_page': p,
        'page_count': xrange(models.post.count_pages()),
        'paging_on': models.post.count_pages() > 1,
    })

@base.get('/p/([0-9]+)')
def view_post(request, post_id):
    try:
        post = models.post.by_id(post_id)
        request.put_page('post.html', {
            'page_title': utils.escape.head_title(post),
            'post': utils.escape.client_post(post),
        })
    except ValueError:
        request.raise_not_found()

@base.get('/tag/(.+)')
def list_by_tag(request, tag):
    p = request.get_of_type('page', int)
    request.put_page('index.html', {
        'posts': utils.escape.client_posts(models.post.by_tag(tag, p)),
        'tags': models.tag.sort_by_count(),
        'current_page': p,
        'page_count': xrange(models.post.count_pages_by_tag(tag)),
        'query_tag': tag,
        'paging_on': models.post.count_pages_by_tag(tag) > 1,
    })

@base.get('/api/nav')
@base.return_json
def nav(request):
    return {
        'tags': models.tag.sort_by_count(),
        'new_posts': [{
            'id': p.pid,
            'title': p.title,
        } for p in utils.escape.client_posts(models.post.fetch(0, 6))],
    }
