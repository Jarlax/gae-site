import webapp2


class AdminHandler(webapp2.RequestHandler):
    def get(self, key):
        self.response.write('ADMIN GET ' + key)

    def list(self):
        self.response.write('ADMIN LIST')

    def put(self, key):
        self.response.write('ADMIN PUT ' + key)

    def post(self):
        self.response.write('ADMIN POST')

    def delete(self, key):
        self.response.write('ADMIN DELETE ' + key)
