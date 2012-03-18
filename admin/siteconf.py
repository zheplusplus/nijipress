import base
import models.post
import admin.model as model

class ConfigureSite(base.BaseView):
    def get(self):
        if not model.User.get_by_session(self.request).admin:
            return base.raise_forbidden(self)
        self.put_page('templates/siteconf.html')

class Save(base.BaseView):
    def post(self):
        if not model.User.get_by_session(self.request).admin:
            return base.raise_forbidden(self)
        conf = model.SiteConfiguration.load()
        conf.title = self.request.get('title').strip()
        conf.style = self.request.get('style').strip()
        conf.rss_uri = self.request.get('rss_uri').strip()
        conf.rss_description = self.request.get('rss_description').strip()
        conf.analytics_code = self.request.get('analytics_code').strip()
        conf.analytics_domain = self.request.get('analytics_domain').strip()
        model.SiteConfiguration.save(conf)
        self.redirect('/c/siteconf')
