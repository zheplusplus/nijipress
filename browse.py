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
        if 'p' in self.request.arguments():
            return single_post(self)
        if 'tag' in self.request.arguments():
            return by_tag(self)
        return index_page(self)

class PostComment(base.BaseView):
    def post(self):
        try:
            post_id = int(self.request.get('post_id'))
            models.post.by_id(post_id)
        except ValueError:
            return base.raise_not_found(self)
        comment = models.comment.Comment()
        comment.author = self.request.get('author').strip()
        comment.content = self.request.get('content').strip()
        if len(comment.content) > 0:
            comment.email = self.request.get('email').strip()
            url = self.request.get('url').strip()
            if len(url) > 0 and not url.startswith('http'):
                url = 'http://' + url
            comment.url = url.strip()
            comment.ipaddr = self.request.remote_addr
            comment.post_id = post_id
            comment.put()
        self.redirect('/?p=' + str(post_id))
