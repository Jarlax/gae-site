import webapp2
from model import Page
from util import get_img_type


class PublicHandler(webapp2.RequestHandler):
    def get(self, page_id=''):
        self.response.write('PUB GET ' + page_id)


class ImageHandler(webapp2.RequestHandler):
    def get(self, page_id):
        page = Page.get_by_id(page_id)
        if page and page.image:
            img_type = get_img_type(page_id)
            self.response.headers['Content-Type'] = str('image/' + img_type)
            self.response.write(page.image)
        else:
            self.error(404)
