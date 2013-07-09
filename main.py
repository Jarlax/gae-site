from handlers import AdminHandler, PublicHandler
import webapp2

name_pattern = '[_a-z0-9]+'  # Name pattern

app = webapp2.WSGIApplication([
    webapp2.Route(r'/_add', AdminHandler, handler_method='add_page',
                  methods=['GET']),
    webapp2.Route(r'/_delete/<page_id:%s>' % name_pattern, AdminHandler,
                  handler_method='delete_page', methods=['POST']),
    webapp2.Route(r'/_save', AdminHandler, handler_method='save',
                  methods=['POST']),
    webapp2.Route(r'/_exchange', AdminHandler, handler_method='exchange',
                  methods=['GET']),
    webapp2.Route(r'/file/<file_id:%s>' % name_pattern, PublicHandler,
                  handler_method='get_file', methods=['GET']),
    webapp2.Route(r'/<page_id:%s>' % name_pattern, PublicHandler,
                  methods=['GET']),
    webapp2.Route(r'/', PublicHandler, methods=['GET'])
], debug=True)



