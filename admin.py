import json
from mimetypes import guess_type
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
        exclude = ['content', 'children']
        json_data = json.dumps([p.to_props(exclude) for p in Page.query().order(-Page.created_on)])
        self.response.write(json_data)

    def put(self, page_id):
        page = Page.get_by_id(page_id)
        if not page:
            page = Page(id=page_id)
        try:
            json_data = self.request.get('data')
            props = json.loads(json_data)
            page.mergeProps(props)
            self.__set_file(page)
            page.put()
        except ValueError:
            self.error(400)

    def delete(self, page_id):
        page = Page.get_by_id(page_id)
        page.key.delete()

    def __set_file(self, page):
        file_content = self.request.get('file')
        if file_content:
            file_param = self.request.params.get('file', None)
            if file_param:
                page.file_type, enc = guess_type(file_param.filename)
            page.file_content = file_content
