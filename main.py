from admin import AdminHandler
from public import PublicHandler, ImageHandler
import webapp2

np = '[_a-z0-9]+'  # Name pattern

app = webapp2.WSGIApplication([
    webapp2.Route(r'/_s/pages', AdminHandler, handler_method='list',
                  methods=['GET']),
    webapp2.Route(r'/_s/page/<key:%s>' % np, AdminHandler,
                  methods=['GET', 'PUT', 'DELETE']),
    webapp2.Route(r'/<key:%s\.(jpg|png)>' % np, ImageHandler, methods=['GET']),
    webapp2.Route(r'/<key:%s>' % np, PublicHandler, methods=['GET']),
    webapp2.Route(r'/', PublicHandler, methods=['GET'])
], debug=True)



