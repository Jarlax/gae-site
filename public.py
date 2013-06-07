import webapp2
from model import Page


class PublicHandler(webapp2.RequestHandler):
    def get(self, page_id=''):
        self.response.write('PUB GET ' + page_id)

    def img(self, file_id):
        page = Page.get_by_id(file_id)
        if page and page.file_content:
            self.response.headers['Content-Type'] = str(page.file_type)
            self.response.write(page.file_content)
        else:
            self.error(404)
