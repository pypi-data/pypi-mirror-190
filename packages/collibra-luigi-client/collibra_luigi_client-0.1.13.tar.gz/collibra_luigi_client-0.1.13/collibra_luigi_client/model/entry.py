import json

from collibra_luigi_client.model.community import Community
from collibra_luigi_client.model.domain import Domain
from collibra_luigi_client.model.identifier import Identifier
from collibra_luigi_client.model.type import Type


def default(o):
    if type(o) in [Entry, Identifier, Type, Domain, Community]:
        return dict((key, value) for key, value in o.__dict__.items() if value)
    else:
        return None


class Entry:
    def __init__(self, resourceType: str = None, identifier: Identifier = None, type: Type = None, displayName: str = None, attributes: list = None, relations: list = None, tags: list = None, status: str = None):
        self.resourceType: str = resourceType
        self.identifier: Identifier = identifier
        self.type: Type = type
        self.displayName: str = displayName
        self.attributes: list = attributes
        self.relations: list = relations
        self.tags: list = tags
        self.status: str = status

    def __str__(self):
        return json.dumps(self, default=default)
