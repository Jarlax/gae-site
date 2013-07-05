from handlers import AdminHandler, AdminHandler1, PublicHandler
import webapp2

name_pattern = '[_a-z0-9]+'  # Name pattern

app = webapp2.WSGIApplication([
    webapp2.Route(r'/_s/pages', AdminHandler, handler_method='list',
                  methods=['GET']),
    webapp2.Route(r'/_s/page/<page_id:%s>' % name_pattern, AdminHandler,
                  methods=['GET', 'PUT', 'DELETE']),
    webapp2.Route(r'/_s/page', AdminHandler, methods=['POST']),
    webapp2.Route(r'/_s/logout-url', AdminHandler, handler_method='log_out_url',
                  methods=['GET']),
    webapp2.Route(r'/_add', AdminHandler1, handler_method='add_page',
                  methods=['GET']),
    webapp2.Route(r'/_delete/<page_id:%s>' % name_pattern, AdminHandler1,
                  handler_method='delete_page', methods=['POST']),
    webapp2.Route(r'/_save', AdminHandler1, handler_method='save',
                  methods=['POST']),
    webapp2.Route(r'/file/<file_id:%s>' % name_pattern, PublicHandler,
                  handler_method='get_file', methods=['GET']),
    webapp2.Route(r'/<page_id:%s>' % name_pattern, PublicHandler,
                  methods=['GET']),
    webapp2.Route(r'/', PublicHandler, methods=['GET'])
], debug=True)



