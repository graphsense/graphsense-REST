class Tag(object):
    """ Model representing a tag """

    def __init__(self, address, label, category, abuse, tagpack_uri, source,
                 lastmod, active, currency):
        self.address = address
        self.label = label
        self.category = category
        self.abuse = abuse
        self.tagpack_uri = tagpack_uri
        self.source = source
        self.lastmod = lastmod
        self.active = active
        self.currency = currency

    @staticmethod
    def from_address_row(row, currency, active=False):
        if not active:
            # from address_tags table
            active = row.active_address
        return Tag(row.address, row.label, row.category, row.abuse,
                   row.tagpack_uri, row.source, row.lastmod, active, currency)

    @staticmethod
    def from_entity_row(row, address, currency):
        return Tag(address, row.label, row.category, row.abuse,
                   row.tagpack_uri, row.source, row.lastmod, True, currency)

    def to_dict(self):
        return self.__dict__
