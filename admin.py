import webapp2
from model import Page


class AdminHandler(webapp2.RequestHandler):
    def get(self, page_id):
        page = Page.get_by_id(page_id)
        if page:
            self.response.write(page.toJson())
        else:
            self.error(404)

    def list(self):
        self.response.write('ADMIN LIST')

    def put(self, page_id):
        page = Page.get_by_id(page_id)
        json_str = self.request.body
        page.mergeJson(json_str)
        page.put()

    def post(self):
        page = Page(id='test')  # TODO: fix issue with assigning ID
        json_str = self.request.body
        page.mergeJson(json_str)
        page.put()
        self.response.status = 201

    def img(self):
        req = self.request
        filename = req.params['image'].filename
        page = Page(id=filename,
                    name=filename,
                    image=req.get('image'))
        page.put()
        self.response.status = 201

    def delete(self, page_id):
        page = Page.get_by_id(page_id)
        page.key.delete()
