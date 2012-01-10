import base
import persist

def page(request):
    try:
        return int(request.get('page'))
    except ValueError:
        return 0

def index_page(view):
    p = page(view.request)
    view.put_page('templates/index.html', {
            'posts': base.posts_for_client(persist.fetch_posts(p)),
            'tags': persist.all_tags(),
            'current_page': p,
            'page_count': xrange(persist.total_posts_page_count()),
            'paging_on': persist.total_posts_page_count() > 1,
        })

def by_tag(view):
    p = page(view.request)
    tag = view.request.get('tag')
    view.put_page('templates/index.html', {
            'posts': base.posts_for_client(persist.posts_by_tag(tag, p)),
            'tags': persist.all_tags(),
            'current_page': p,
            'page_count': xrange(persist.total_posts_page_count_by_tag(tag)),
            'query_tag': tag,
            'paging_on': persist.total_posts_page_count_by_tag(tag) > 1,
        })

def single_post(view):
    post = persist.post_by_id(view.request.get('p'))
    if post.title:
        view.put_page('templates/post.html', {
                'post': base.post_for_client(post),
                'comments': persist.comments_for_post(post.pid),
            })
    else:
        base.raise_not_found(view)

class Index(base.BaseView):
    def get(self):
        if 'p' in self.request.arguments():
            return single_post(self)
        if 'tag' in self.request.arguments():
            return by_tag(self)
        return index_page(self)

class PostComment(base.BaseView):
    def post(self):
        try:
            post_id = int(self.request.get('post_id'))
            if len(persist.post_by_id(post_id).title) == 0:
                raise ValueError('no such post')
        except ValueError:
            return base.raise_not_found(self)
        comment = persist.Comment()
        comment.author = self.request.get('author')
        comment.content = self.request.get('content')
        if len(comment.content) > 0:
            comment.email = self.request.get('email')
            url = self.request.get('url')
            if len(url) > 0 and not url.startswith('http'):
                url = 'http://' + url
            comment.url = url
            comment.ipaddr = self.request.remote_addr
            comment.post_id = post_id
            comment.put()
        self.redirect('/?p=' + str(post_id))
