from google.appengine.ext import ndb


class Page(ndb.Model):
    name = ndb.StringProperty()
    content = ndb.StringProperty()
    template = ndb.StringProperty()
    image = ndb.BlobProperty()
    children = ndb.StringProperty(repeated=True)
