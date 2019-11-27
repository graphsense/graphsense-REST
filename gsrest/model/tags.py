class Tag(object):
    """ Model representing a tag """

    def __init__(self, address, label, category, abuse, tagpack_uri, source,
                 lastmod, currency):
        self.address = address
        self.label = label
        self.category = category
        self.abuse = abuse
        self.tagpack_uri = tagpack_uri
        self.source = source
        self.lastmod = lastmod
        self.currency = currency


    @staticmethod
    def from_row(row, currency):
        return Tag(row.address, row.label, row.category, row.abuse,
                   row.tagpack_uri, row.source, row.lastmod, currency)

    def to_dict(self):
        return self.__dict__


