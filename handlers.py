import jinja2
import json
import webapp2
from google.appengine.api import users
from google.appengine.ext import ndb
from mimetypes import guess_type
from model import Page

JINJA_ENVIRONMENT = jinja2.Environment(loader=jinja2.FileSystemLoader('templates'))
JINJA_ENVIRONMENT.line_statement_prefix = '@'


class PublicHandler(webapp2.RequestHandler):
    master_id = 'master'
    master_key = ndb.Key(Page, master_id)

    def get(self, page_id=''):
        menu_pages = [(p.name, p.key.string_id())
                      for p in Page.query(ancestor=self.master_key).fetch(projection=[Page.name])]
        if not page_id and menu_pages:
            _, page_id = menu_pages[0]
        page = Page()  # Empty object
        if page_id:
            page = Page.get_by_id(page_id, parent=self.master_key)
        values = {
            'site_name': 'GAE Site',
            'menu': menu_pages,
            'page': page,
            'is_admin': users.is_current_user_admin(),
            'master_id': self.master_id
        }
        template = JINJA_ENVIRONMENT.get_template('page.html')
        self.response.write(template.render(values))

    def get_file(self, file_id):
        page = Page.get_by_id(file_id, parent=self.master_key)
        if page and page.file_content:
            self.response.headers['Content-Type'] = str(page.file_type)
            self.response.write(page.file_content)
        else:
            self.error(404)


class AdminHandler(webapp2.RequestHandler):
    master_page_key = ndb.Key(Page, 'master')

    def add_page(self, parent_id='', order_num=''):
        self.response.write(parent_id + ' ' + order_num)

    def get(self, page_id):
        page = Page.get_by_id(page_id, parent=self.master_page_key)
        if page:
            self.response.write(page.toJson())
        else:
            self.error(404)

    def list(self):
        query = Page.query(ancestor=self.master_page_key)\
            .order(-Page.created_on)\
            .fetch(projection=[Page.name, Page.created_on, Page.template])

        json_data = json.dumps([p.to_props() for p in query])
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
