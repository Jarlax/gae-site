from admin import AdminHandler
from public import PublicHandler
from util import name_pattern
import webapp2

app = webapp2.WSGIApplication([
    webapp2.Route(r'/_s/pages', AdminHandler, handler_method='list',
                  methods=['GET']),
    webapp2.Route(r'/_s/page/<page_id:%s>' % name_pattern, AdminHandler,
                  methods=['GET', 'PUT', 'DELETE']),
    webapp2.Route(r'/_s/page', AdminHandler, methods=['POST']),
    webapp2.Route(r'/file/<file_id:%s>' % name_pattern, PublicHandler,
                  handler_method='get_file', methods=['GET']),
    webapp2.Route(r'/<page_id:%s>' % name_pattern, PublicHandler,
                  methods=['GET']),
    webapp2.Route(r'/', PublicHandler, methods=['GET'])
], debug=True)



