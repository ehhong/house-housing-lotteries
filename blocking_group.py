
class BlockingGroup:
    def __init__(self, bgid, size):
        self.id = bgid
        self.size = size
        self.preferences = [] # strict preferences for this blocking group

    def set_preferences(self):
        ''' semi-randomly set preferences for blocking group based on size '''
