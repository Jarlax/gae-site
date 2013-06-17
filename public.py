from google.appengine.ext import ndb
import jinja2
import webapp2
from model import Page

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader('templates'),
    extensions=['jinja2.ext.autoescape'])


class PublicHandler(webapp2.RequestHandler):
    master_page_key = ndb.Key(Page, 'master')

    def get(self, page_id=''):
        menu_pages = [(p.name, p.key.string_id())
                      for p in Page.query(ancestor=self.master_page_key).fetch(projection=[Page.name])]
        if not page_id and menu_pages:
            _, page_id = menu_pages[0]
        page = Page()  # Empty object
        if page_id:
            page = Page.get_by_id(page_id, parent=self.master_page_key)
        values = {
            'name': 'GAE Site',
            'menu': menu_pages,
            'page': page
        }
        template = JINJA_ENVIRONMENT.get_template('page.html')
        self.response.write(template.render(values))

    def get_file(self, file_id):
        page = Page.get_by_id(file_id)
        if page and page.file_content:
            self.response.headers['Content-Type'] = str(page.file_type)
            self.response.write(page.file_content)
        else:
            self.error(404)
