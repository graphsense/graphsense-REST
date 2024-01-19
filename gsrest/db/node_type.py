from enum import Enum


class NodeType(Enum):
    ADDRESS = 'address'
    CLUSTER = 'cluster'

    def __str__(self):
        return self.value
