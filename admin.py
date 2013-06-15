import json
from mimetypes import guess_type
from google.appengine.api import users
from google.appengine.ext import ndb
import webapp2
from model import Page


class AdminHandler(webapp2.RequestHandler):
    master_page_key = ndb.Key(Page, 'master')

    def get(self, page_id):
        page = Page.get_by_id(page_id, parent=self.master_page_key)
        if page:
            self.response.write(page.toJson())
        else:
            self.error(404)

    def list(self):
        exclude = ['content', 'children']
        query = Page.query(ancestor=self.master_page_key)\
            .order(-Page.created_on)\
            .fetch(projection=[Page.name, Page.created_on, Page.template])

        json_data = json.dumps([p.to_props(exclude) for p in query])
        self.response.write(json_data)

    def put(self, page_id):
        page = Page.get_by_id(page_id)
        if not page:
            page = Page(id=page_id, parent=self.master_page_key)
        try:
            json_data = self.request.get('data')
            props = json.loads(json_data)
            page.mergeProps(props)
            self.__set_file(page)
            page.put()
        except ValueError:
            self.error(400)

    def delete(self, page_id):
        page = Page.get_by_id(page_id, parent=self.master_page_key)
        if page:
            page.key.delete()
        else:
            self.error(404)

    def log_out_url(self):
        self.response.write(users.create_logout_url('/'))

    def __set_file(self, page):
        file_content = self.request.get('file')
        if file_content:
            page.file_content = file_content
            file_param = self.request.params.get('file', None)
            if file_param:
                page.file_type, enc = guess_type(file_param.filename)
