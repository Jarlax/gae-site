import json
from google.appengine.ext import ndb


class Page(ndb.Model):
    name = ndb.StringProperty()
    content = ndb.StringProperty()
    template = ndb.StringProperty()
    file_content = ndb.BlobProperty()
    file_type = ndb.StringProperty()
    children = ndb.StringProperty(repeated=True)

    def to_props(self, exclude=None):
        exclude_props = ['file_content', 'file_type']
        if exclude:
            exclude_props += exclude
        props = self.to_dict(exclude=exclude_props)
        if self.key:
            props['id'] = self.key.string_id()
        return props

    def toJson(self):
        return json.dumps(self.to_props())

    def mergeProps(self, props):
        for v in props:
            setattr(self, v, props[v])

