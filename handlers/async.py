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

@base.get('/api/loadpostbyid/([0-9]+)')
@base.return_json
def load_post_by_id(request, post_id):
    post = models.post.by_id(post_id)
    if post is None:
        return {}
    return utils.dumpjson.post_full(utils.escape.client_post(post))

class LoadPostById(AsyncHandler):
    def serve(self):
        return utils.dumpjson.post_full(utils.escape.client_post(
                                    models.post.by_id(self.args['id'])))
