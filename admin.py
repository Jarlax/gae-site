import webapp2
from model import Page


class AdminHandler(webapp2.RequestHandler):
    def get(self, key):
        self.response.write('ADMIN GET ' + key)

    def list(self):
        self.response.write('ADMIN LIST')

    def put(self, key):
        self.response.write('ADMIN PUT ' + key)

    def post(self):
        self.response.write('ADMIN POST')

    def img(self):
        req = self.request
        filename = req.params['image'].filename
        page = Page(id=filename,
                    name=filename,
                    image=req.get('image'))
        page.put()
        self.response.status = 201

    def delete(self, key):
        self.response.write('ADMIN DELETE ' + key)
