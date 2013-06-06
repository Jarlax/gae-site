from admin import AdminHandler
from public import PublicHandler, ImageHandler
from util import image_pattern, name_pattern
import webapp2

app = webapp2.WSGIApplication([
    webapp2.Route(r'/_s/pages', AdminHandler, handler_method='list',
                  methods=['GET']),
    webapp2.Route(r'/_s/page/<page_id:%s>' % name_pattern, AdminHandler,
                  methods=['GET', 'PUT', 'DELETE']),
    webapp2.Route(r'/_s/page/<page_id:%s>' % image_pattern, AdminHandler,
                  methods=['GET', 'PUT', 'DELETE']),  # TODO: fix more elegant
    webapp2.Route(r'/_s/page', AdminHandler, methods=['POST']),
    webapp2.Route(r'/<page_id:%s>' % image_pattern, ImageHandler, methods=['GET']),
    webapp2.Route(r'/<page_id:%s>' % name_pattern, PublicHandler, methods=['GET']),
    webapp2.Route(r'/', PublicHandler, methods=['GET'])
], debug=True)



