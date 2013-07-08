from google.appengine.ext import ndb


class Page(ndb.Model):
    name = ndb.StringProperty()
    content = ndb.StringProperty(indexed=False)
    content_html = ndb.StringProperty(indexed=False)
    description = ndb.StringProperty(indexed=False)
    keywords = ndb.StringProperty(indexed=False)
    order = ndb.IntegerProperty()
    page_type = ndb.StringProperty()
    file_content = ndb.BlobProperty()
    file_type = ndb.StringProperty()
    created_on = ndb.DateTimeProperty(auto_now=True)

    def mergeProps(self, props):
        for v in props:
            if v == 'order':
                setattr(self, v, int(props[v]))
            else:
                setattr(self, v, props[v])

    @staticmethod
    def get_or_create(page_id, parent_key):
        page = Page.get_by_id(page_id, parent=parent_key)
        if not page:
            page = Page(id=page_id, parent=parent_key)
        return page

    @staticmethod
    def get_children_names(parent_key, by_date=True):
        query = Page.query(ancestor=parent_key)
        if by_date:
            query = query.order(-Page.created_on)
        else:
            query = query.order(Page.order)
        query = query.fetch(projection=[Page.name])
        return [(p.name, p.key.string_id()) for p in query]

    @staticmethod
    def get_children_count(parent_key):
        return Page.query(ancestor=parent_key).count()

    @staticmethod
    def get_first_child(parent_key, by_date=True):
        query = Page.query(ancestor=parent_key)
        if by_date:
            query = query.order(-Page.created_on)
        else:
            query = query.order(Page.order)
        res = query.fetch(1)
        return res[0] if res else None

    @staticmethod
    def inc_order_number(parent_key, start):
        pages = Page.query(Page.order >= start, ancestor=parent_key)
        for page in pages:
            page.order += 1
            page.put()

    @staticmethod
    def dec_order_number(parent_key, start):
        pages = Page.query(Page.order >= start, ancestor=parent_key)
        for page in pages:
            page.order -= 1
            page.put()