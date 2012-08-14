import base
import models.post
import models.admin

class Save(base.BaseView):
    def post(self):
        if not models.admin.User.get_by_session(self.request).admin:
            return base.raise_forbidden(self)
        conf = models.admin.SiteConfiguration.load_persist()
        conf.title = self.request.get('title').strip()
        conf.style = self.request.get('style').strip()
        conf.rss_uri = self.request.get('rss_uri').strip()
        conf.rss_description = self.request.get('rss_description').strip()
        conf.analytics_code = self.request.get('analytics_code').strip()
        conf.analytics_domain = self.request.get('analytics_domain').strip()
        conf.post_html = self.request.get('post_html').strip()
        models.admin.SiteConfiguration.save(conf)
        models.admin.Blogroll.add_by_text(self.request.get('blogrolls').strip())
        self.redirect('/c/siteconf')
