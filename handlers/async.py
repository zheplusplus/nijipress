import json
import base
import models.tag
import models.post
import utils.dumpjson
import utils.escape

class AsyncHandler(base.BaseView):
    def post(self):
        self.args = json.loads(self.request.body)
        self.response.out.write(json.dumps(self.serve()))

class Tags(AsyncHandler):
    def serve(self):
        return models.tag.sort_by_count()

class RecentPosts(AsyncHandler):
    def serve(self):
        return [ utils.dumpjson.post_title(p) for p in
                utils.escape.client_posts(models.post.fetch(0, 6)) ]

class LoadPostById(AsyncHandler):
    def serve(self):
        return utils.dumpjson.post_full(utils.escape.client_post(
            models.post.by_id(self.args['id'])))
