import json
import webapp2
from model import Page
from util import get_id_by_name, get_img_type


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
        if not page:
            self.error(404)
        elif not self.__do_save(page):
            self.error(400)

    def post(self):
        if self.__do_save():
            self.response.status = 201
        else:
            self.error(400)

    def delete(self, page_id):
        page = Page.get_by_id(page_id)
        page.key.delete()

    def __do_save(self, page=None):
        try:
            json_data = self.request.get('data')
            props = json.loads(json_data)
            if not page:
                page = self.__create_model(props)
            page.mergeProps(props)
            image = self.request.get('image')
            if image:
                page.image = image
            page.put()
            return True
        except:  # TODO: Add nicer exception handling
            return False

    def __create_model(self, props):
        name = props['name']
        ext = self.__get_ext()
        page_id = get_id_by_name(name, ext)
        return Page(id=page_id)

    def __get_ext(self):
        image_file = self.request.params.get('image', None)
        if image_file is not None:
            return get_img_type(image_file.filename)
