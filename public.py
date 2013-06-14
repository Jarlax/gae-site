import jinja2
import webapp2
from model import Page

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader('templates'),
    extensions=['jinja2.ext.autoescape'])


class PublicHandler(webapp2.RequestHandler):
    def get(self, page_id=''):
        values = {
            'model': page_id
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
