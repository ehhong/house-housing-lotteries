
class BlockingGroup:
    def __init__(self, bgid, size, house):
        self.id = bgid
        self.size = size
        self.house = house;
        self.preferences = [] # strict preferences for this blocking group

    def set_preferences(self):
        ''' semi-randomly set preferences for blocking group based on size '''
        # restrict number of rooms per blocking group? how do we wanna do this
