import webapp2
from model import Page
from util import get_img_type


class PublicHandler(webapp2.RequestHandler):
    def get(self, key=''):
        self.response.write('PUB GET ' + key)


class ImageHandler(webapp2.RequestHandler):
    def get(self, key):
        page = Page.get_by_id(key)
        if page and page.image:
            type = get_img_type(page.name)
            self.response.headers['Content-Type'] = str('image/' + type)
            self.response.write(page.image)
        else:
            self.error(404)
