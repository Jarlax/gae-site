import webapp2
from model import Page


class PublicHandler(webapp2.RequestHandler):
    def get(self, page_id=''):
        self.response.write('PUB GET ' + page_id)

    def img(self, image_id):
        page = Page.get_by_id(image_id)
        if page and page.image:
            img_type = page.image_type
            self.response.headers['Content-Type'] = str('image/' + img_type)
            self.response.write(page.image)
        else:
            self.error(404)
