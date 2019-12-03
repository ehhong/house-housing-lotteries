from random import seed, randint
seed(1)

class BlockingGroup:
    def __init__(self, bgid, size, house):
        self.id = bgid
        self.size = size
        self.house = house;
        self.preferences = [] # strict preferences for this blocking group
        self.rg_config = None # used for Adams
        self.assigned_rooms = []

    def set_preferences(self):
        ''' semi-randomly set preferences for blocking group based on size '''
        randomized_prefs = [[] for x in range(9)]

        for room_size, room_list in enumerate(self.house.rooms):
            for index, (room_id, proximity, quality) in enumerate(room_list):
              new_quality = randint(max(0, quality - 2), min(10, quality + 2))
              randomized_prefs[room_size].append((room_id, proximity, new_quality))

        self.preferences = randomized_prefs

        # sort by quality within each room size
        for i, v in enumerate(self.preferences):
            v.sort(key = lambda x: (x[2], x[1]), reverse = True)

        # print(self.preferences)

        # restrict number of rooms per blocking group? how do we wanna do this

    def set_rg_config(self, rg_config):
        ''' rg_config should be a tuple '''
        self.rg_config = rg_config
