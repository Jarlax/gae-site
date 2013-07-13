import jinja2
import webapp2
from google.appengine.api import users
from google.appengine.ext import ndb
from model import Page

site_name = 'GAE Site'
master_id = 'master'

JINJA_ENV = jinja2.Environment(loader=jinja2.FileSystemLoader('templates'),
                               extensions=['jinja2.ext.autoescape'])
JINJA_ENV.line_statement_prefix = '@'
JINJA_ENV.filters['q'] = lambda(value): value.replace('\'', '\\\'')
JINJA_ENV.globals['logout_url'] = lambda: users.create_logout_url('/')
JINJA_ENV.globals['master_id'] = master_id


class PublicHandler(webapp2.RequestHandler):
    master_key = ndb.Key(Page, master_id)

    def get(self, page_id=''):
        if page_id:
            page = Page.get_by_id(page_id, parent=self.master_key)
        else:
            page = Page.get_first_child(self.master_key, False)
        if page:
            return self._get_page(page)
        else:
            self.redirect('/_add?type=post')

    def get_file(self, file_id):
        page = Page.get_by_id(file_id, parent=self.master_key)
        if page and page.file_content:
            self.response.headers['Content-Type'] = str(page.file_type)
            self.response.write(page.file_content)
        else:
            self.error(404)

    def _get_page(self, page):
        master = 'admin' if users.is_current_user_admin() else 'public'
        menu_pages = Page.get_children_names(self.master_key, False)
        values = {
            'id': page.key.string_id(),
            'master': master + '.html',
            'menu': menu_pages,
            'page': page,
            'site_name': site_name
        }
        template = JINJA_ENV.get_template(page.page_type + '.html')
        self.response.write(template.render(values))

    def _redirect_url(self, page=None):
        return '/'  # TODO implement


class AdminHandler(PublicHandler):
    def add_page(self):
        params = self.request.params
        order = params.get('order', Page.get_children_count(self.master_key))
        parent = self._get_parent_key()
        page_type = params.get('type', None)
        if page_type:
            page = Page(parent=parent, page_type=page_type, order=int(order))
            self._get_page(page)
        else:
            self.error(400)

    def delete_page(self, page_id):
        page = Page.get_by_id(page_id, parent=self.master_key)
        if page:
            Page.dec_order_number(self.master_key, page.order)
            page.key.delete()
            self.redirect(self._redirect_url())
        else:
            self.error(404)

    def save(self):
        params = self.request.params
        page = Page.get_or_create(params.get('id'), self._get_parent_key())
        page.mergeProps(params)
        if page.order is None:
            page.order = Page.get_children_count(self.master_key)
        page.put()
        self.redirect(self._redirect_url(page))

    def exchange(self):
        params = self.request.params
        page1 = Page.get_by_id(params.get('page1'), parent=self.master_key)
        page2 = Page.get_by_id(params.get('page2'), parent=self.master_key)
        page1.order, page2.order = page2.order, page1.order
        page1.put()
        page2.put()

    def _get_parent_key(self):
        return ndb.Key(Page, self.request.params.get('parent', master_id))