import json
from google.appengine.ext import ndb


class Page(ndb.Model):
    name = ndb.StringProperty()
    content = ndb.StringProperty(indexed=False)
    content_html = ndb.StringProperty(indexed=False)
    description = ndb.StringProperty(indexed=False)
    keywords = ndb.StringProperty(indexed=False)
    template = ndb.StringProperty()
    file_content = ndb.BlobProperty()
    file_type = ndb.StringProperty()
    created_on = ndb.DateTimeProperty(auto_now=True)

    def to_props(self):
        exclude_props = ['file_content', 'file_type', 'created_on']
        props = self.to_dict(exclude=exclude_props)
        props['created_date'] = str(self.created_on.date())
        if self.key:
            props['id'] = self.key.string_id()
        return props

    def toJson(self):
        return json.dumps(self.to_props())

    def mergeProps(self, props):
        for v in props:
            setattr(self, v, props[v])

    @staticmethod
    def get_children_names(parent_key):
        query = Page.query(ancestor=parent_key).fetch(projection=[Page.name])
        return [(p.name, p.key.string_id()) for p in query]

    @staticmethod
    def get_children_count(parent_key):
        return Page.query(ancestor=parent_key).count()

    @staticmethod
    def get_first_child(parent_key):
        return Page.query(ancestor=parent_key).fetch(1)[0]



