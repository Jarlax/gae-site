from admin import AdminHandler
from public import PublicHandler, ImageHandler
import webapp2

name_pattern = '[_a-z0-9]+'  # Name pattern
image_pattern = '%s\.(jpe?g|png)' % name_pattern # Image name pattern

app = webapp2.WSGIApplication([
    webapp2.Route(r'/_s/pages', AdminHandler, handler_method='list',
                  methods=['GET']),
    webapp2.Route(r'/_s/page/<key:%s>' % name_pattern, AdminHandler,
                  methods=['GET', 'PUT', 'DELETE']),
    webapp2.Route(r'/_s/page', AdminHandler, methods=['POST']),
    webapp2.Route(r'/_s/img', AdminHandler, handler_method='img',
                  methods=['POST']),
    webapp2.Route(r'/<key:%s>' % image_pattern, ImageHandler, methods=['GET']),
    webapp2.Route(r'/<key:%s>' % name_pattern, PublicHandler, methods=['GET']),
    webapp2.Route(r'/', PublicHandler, methods=['GET'])
], debug=True)



