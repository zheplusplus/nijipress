import base
import models.post
import models.comment

def index_page(view):
    p = view.request_value('page', int)
    view.put_page('templates/index.html', {
            'posts': base.posts_for_client(models.post.fetch(p)),
            'tags': models.tag.sort_by_count(),
            'current_page': p,
            'page_count': xrange(models.post.count_pages()),
            'paging_on': models.post.count_pages() > 1,
        })

def by_tag(view):
    p = view.request_value('page', int)
    tag = view.request.get('tag')
    view.put_page('templates/index.html', {
            'posts': base.posts_for_client(models.post.by_tag(tag, p)),
            'tags': models.tag.sort_by_count(),
            'current_page': p,
            'page_count': xrange(models.post.count_pages_by_tag(tag)),
            'query_tag': tag,
            'paging_on': models.post.count_pages_by_tag(tag) > 1,
        })

def single_post(view):
    def title_text(title):
        def flat_nodes(nodes):
            r = []
            for n in nodes:
                if n.nodeType == n.TEXT_NODE:
                    r.append(n.data)
                else:
                    r.extend(flat_nodes(n.childNodes))
            return r
        import xml.dom.minidom as dom
        return ''.join(flat_nodes(dom.parseString((
                '<title>' + title + '</title>').encode('utf-8')).childNodes))
    try:
        post = base.post_for_client(models.post.by_id(view.request.get('p')))
        view.put_page('templates/post.html', {
                'post': post,
                'title': title_text(post.title),
                'comments': base.comments_for_client(
                                models.comment.by_post_id(post.pid)),
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

def _comment_token(request):
    import time
    from hashlib import sha256
    return request.cookies['ctkn'] if 'ctkn' in request.cookies else sha256(
                                                 str(time.time())).hexdigest()

class PostComment(base.BaseView):
    def post(self):
        try:
            post_id = int(self.request.get('post_id'))
            models.post.by_id(post_id)
        except ValueError:
            return base.raise_not_found(self)
        comment = models.comment.PendingComment()
        comment.content = self.request.get('content').strip()
        if 0 < len(comment.content) <= 500:
            comment.author = self.request.get('author').strip()
            comment.email = self.request.get('email').strip()
            comment.ctoken = _comment_token(self.request)
            url = self.request.get('url').strip()
            if len(url) > 0 and not url.startswith('http'):
                url = 'http://' + url
            comment.url = url
            comment.ipaddr = self.request.remote_addr
            comment.post_id = post_id
            if models.comment.put(comment):
                update_cookie(self.response, comment.ctoken)
                self.error(404)
                self.put_page('templates/message.html', {
                        'id': post_id,
                        'message': 'Your comment is awaiting moderation',
                        'posts': base.posts_for_client(models.post.fetch(0, 5)),
                    })
                return
        self.redirect('/?p=' + str(post_id))

def update_cookie(response, token):
    from Cookie import BaseCookie
    cookie = BaseCookie()
    cookie['ctkn'] = token
    cookie['ctkn']['path'] = '/'
    cookie['ctkn']['max-age'] = 17299119
    response.headers.add('Set-Cookie', cookie['ctkn'].output(header='').strip())
