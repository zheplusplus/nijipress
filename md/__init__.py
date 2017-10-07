import nijitext.inline
import nijitext.html
import nijitext.entire_doc

class MarkdownConvert(object):
    def __init__(self, head_title, content, preview):
        """
        head_title: escape the title for <head><title>
        content: escape the title and the content which will be shown in the page
        preview: text preview
        """
        self.head_title = head_title
        self.content = content
        self.preview = preview

    def process_multilines(self, content):
        return ''.join(self.content(content.split('\n')))

    def generate_preview(self, content):
        return ''.join(self.preview(content.split('\n'), 1729))

    def process_post(self, post):
        post.title = self.process_multilines(post.title)
        content = post.content
        post.content = self.process_multilines(content)
        post.preview = self.generate_preview(content)
        return post

__nijitext = MarkdownConvert(
    nijitext.entire_doc.plain_title,
    nijitext.entire_doc.forge,
    nijitext.entire_doc.generate_preview,
)

__markmap = {
    None: __nijitext,
    'nijitext': __nijitext,
}

def get(t):
    return __markmap[t]
