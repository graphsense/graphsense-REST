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
    def from_address_row(row, currency):
        return Tag(row.address, row.label, row.category, row.abuse,
                   row.tagpack_uri, row.source, row.lastmod, currency)

    @staticmethod
    def from_entity_row(row, address, currency):
        return Tag(address, row.label, row.category, row.abuse,
                   row.tagpack_uri, row.source, row.lastmod, currency)

    def to_dict(self):
        return self.__dict__


class Label(object):
    """ Model representing a Label """

    def __init__(self, label, label_norm, address_count):
        self.label = label
        self.label_norm = label_norm
        self.address_count = address_count

    @staticmethod
    def from_row(row):
        return Label(row.label, row.label_norm, row.address_count)

    def to_dict(self):
        return self.__dict__

