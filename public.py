import webapp2


class PublicHandler(webapp2.RequestHandler):
    def get(self, key=''):
        self.response.write('PUB GET ' + key)


class ImageHandler(webapp2.RequestHandler):
    def get(self, key):
        self.response.write('IMG GET ' + key)
