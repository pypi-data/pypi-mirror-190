from collibra_luigi_client.model.community import Community


class Domain:
    def __init__(self, name: str = None, community: Community = None):
        self.name = name
        self.community = community
