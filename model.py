import json
from google.appengine.ext import ndb


class Page(ndb.Model):
    name = ndb.StringProperty()
    content = ndb.StringProperty()
    template = ndb.StringProperty()
    image = ndb.BlobProperty()
    children = ndb.StringProperty(repeated=True)

    def toJson(self):
        props = self.to_dict(exclude=['image'])
        if self.key:
            props['id'] = self.key.string_id()
        return json.dumps(props)

    def mergeProps(self, props):
        for v in props:
            setattr(self, v, props[v])

