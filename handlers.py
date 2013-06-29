import jinja2
import json
import webapp2
from google.appengine.api import users
from google.appengine.ext import ndb
from mimetypes import guess_type
from model import Page

site_name = 'GAE Site'
master_id = 'master'

JINJA_ENV = jinja2.Environment(loader=jinja2.FileSystemLoader('templates'))
JINJA_ENV.line_statement_prefix = '@'
JINJA_ENV.globals['logout_url'] = lambda: users.create_logout_url('/')
JINJA_ENV.globals['master_id'] = master_id


class PublicHandler(webapp2.RequestHandler):
    master_key = ndb.Key(Page, master_id)

    def get(self, page_id=''):
        if page_id:
            page = Page.get_by_id(page_id, parent=self.master_key)
        else:
            page = Page.get_first_child(self.master_key)
        if page:
            return self._get_page(page)
        else:
            self.error(404)

    def get_file(self, file_id):
        page = Page.get_by_id(file_id, parent=self.master_key)
        if page and page.file_content:
            self.response.headers['Content-Type'] = str(page.file_type)
            self.response.write(page.file_content)
        else:
            self.error(404)

    def _get_page(self, page):
        master = 'admin' if users.is_current_user_admin() else 'public'
        menu_pages = Page.get_children_names(self.master_key)
        values = {
            'master': master + '.html',
            'menu': menu_pages,
            'page': page,
            'site_name': site_name
        }
        template = JINJA_ENV.get_template(page.page_type + '.html')
        self.response.write(template.render(values))


class AdminHandler1(PublicHandler):
    def add_page(self):
        params = self.request.params
        order = params.get('order', Page.get_children_count(self.master_key))
        parent = params.get('parent', master_id)
        type = params.get('type', None)
        if type:
            parent_key = ndb.Key(Page, parent)
            page = Page(parent=parent_key, type=type, order=int(order))
            self._get_page(page)
        else:
            self.error(400)


class AdminHandler(webapp2.RequestHandler):
    master_page_key = ndb.Key(Page, 'master')

    def get(self, page_id):
        page = Page.get_by_id(page_id, parent=self.master_page_key)
        if page:
            self.response.write(page.toJson())
        else:
            self.error(404)

    def list(self):
        query = Page.query(ancestor=self.master_page_key)\
            .order(-Page.created_on)\
            .fetch(projection=[Page.name, Page.created_on, Page.page_type])

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
