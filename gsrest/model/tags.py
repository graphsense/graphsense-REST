class Tag:
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


class Concept:
    """Concept Definition.
    This class serves as a proxy for a concept that is defined
    in some remote taxonomy. It just provides the most essential properties.
    A concept can be viewed as an idea or notion; a unit of thought.
    See: https://www.w3.org/TR/skos-reference/#concepts
    """

    def __init__(self, taxonomy, id_, uri, label, description):
        self.taxonomy = taxonomy
        self.id = id_
        self.uri = uri
        self.label = label
        self.description = description

    @staticmethod
    def from_row(row):
        return Concept(row.taxonomy, row.id, row.uri, row.label,
                       row.description)

    def to_dict(self):
        return self.__dict__


class Taxonomy:
    """ Model representing a taxonomy """

    def __init__(self, taxonomy, uri):
        self.taxonomy = taxonomy
        self.uri = uri

    @staticmethod
    def from_row(row):
        return Taxonomy(row.key, row.uri)

    def to_dict(self):
        return self.__dict__
