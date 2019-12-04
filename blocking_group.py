from random import seed, randint
from itertools import combinations

seed(1)

class BlockingGroup:
    def __init__(self, bgid, size, house):
        self.id = bgid
        self.size = size
        self.house = house;
        self.preferences = [] # list of lists, indexed by room size -- custom preferences for this blocking group
                              # rooms are tuples: (room id, proximity, quality, size)
        self.rg_config = None # used for Adams
        self.assigned_rooms = []

        self.rg_preferences = [] # (avg quality, list of assigned rooms)
        self.rg_configs = { # maximally 3 rooming groups per blocking group
            1: [[1]],
            2: [[2], [1,1]],
            3: [[3], [2,1], [1,1,1]],
            4: [[4], [3,1], [2,2], [2,1,1]],
            5: [[5], [4,1], [3,2], [3,1,1], [2,2,1]],
            6: [[6], [5,1], [4,2], [4,1,1], [3,3], [3,2,1], [2,2,2]],
            7: [[7], [6,1], [5,2], [5,1,1], [4,3], [4,2,1], [3,3,1], [3,2,2]],
            8: [[8], [7,1], [6,2], [6,1,1], [5,3], [5,2,1], [4,4], [4,3,1], [4,2,2], [3,3,2]]
        }

    def set_preferences(self):
        ''' semi-randomly set individual room preferences for blocking group based on size '''
        randomized_prefs = [[] for x in range(9)]

        for room_size, room_list in enumerate(self.house.rooms):
            for index, (room_id, proximity, quality) in enumerate(room_list):
              new_quality = randint(max(0, quality - 2), min(10, quality + 2))
              randomized_prefs[room_size].append((room_id, proximity, new_quality, room_size))

        self.preferences = randomized_prefs

        # sort by quality within each room size
        for i, v in enumerate(self.preferences):
            v.sort(key = lambda x: (x[2], x[1]), reverse = True)

    def set_rg_config_preferences(self):
        ''' create preference listing for the bg's current rg config '''
        if (not self.rg_config):
            print("No RG config set")

        rg_config_combos = []

        # set up rg config in a better form
        room_size_quantities = dict() # key: size; value: quantity of rooms of that size
        for rs in self.rg_config:
            if rs in room_size_quantities:
                room_size_quantities[rs] += 1
            else:
                room_size_quantities[rs] = 1

        # find each combination, and quality score
        combo_list = [] # list of lists of each combination of rooms
        for sz, q in room_size_quantities.items():
            c = map(lambda x: list(x), combinations(self.preferences[sz], q))
            combo_list.append(c)

        # get all room combinations for this rg config
        rg_config_combos.extend(get_room_combos(combo_list))

        # get avg quality of rg_config
        q_rg_config_combos = map(lambda rooms: (get_avg_quality(rooms), rooms), rg_config_combos)

        # sort by quality
        q_rg_config_combos.sort(key = lambda (q, _): q, reverse=True)
        self.rg_preferences = q_rg_config_combos

    def set_full_rg_preferences(self):
        ''' create full listing of preferences for full blocking group '''
        all_rg_configs = []

        # for each rg configuration
        rg_configs = self.rg_configs[self.size]
        for rg_config in rg_configs:

            # set up rg config in a better form
            room_size_quantities = dict() # key: size; value: quantity of rooms of that size
            for rs in rg_config:
                if rs in room_size_quantities:
                    room_size_quantities[rs] += 1
                else:
                    room_size_quantities[rs] = 1

            # find each combination, and quality score
            combo_list = [] # list of lists of each combination of rooms
            for sz, q in room_size_quantities.items():
                c = map(lambda x: list(x), combinations(self.preferences[sz], q))
                combo_list.append(c)

            # get all room combinations for this rg config
            all_rg_configs.extend(get_room_combos(combo_list))

        # get avg quality of rg_config
        q_all_rg_configs = map(lambda rooms: (get_avg_quality(rooms), rooms), all_rg_configs)

        # sort by quality
        q_all_rg_configs.sort(key = lambda (q, _): q, reverse=True)
        self.rg_preferences = q_all_rg_configs

    def set_rg_config(self, rg_config):
        ''' rg_config should be a tuple '''
        self.rg_config = rg_config

# helper function
def get_room_combos(combo_list):
    ''' given a list of combos for each size of room, return the full set of room combinations for the rg config '''

    # prefs is a list of lists (room combinations) of currently generated preferences
    def get_room_combos_rec(prefs, idx):

        # base case
        if idx >= len(combo_list):
            return prefs
        else:
            if idx == 0:
                return get_room_combos_rec(combo_list[idx], idx + 1)
            else:
                updated_prefs = []
                for p in prefs:
                    for r in combo_list[idx]:

                        rc = p + r
                        updated_prefs.append(rc)

                return get_room_combos_rec(updated_prefs, idx + 1)

    return get_room_combos_rec([], 0)

def get_avg_quality(rooms):
    ''' given a list of rooms, return avg quality per person '''
    qualities = []
    num_students = 0

    for (_, _, quality, size) in rooms:
        num_students += size
        addition = [quality for i in range(size)]
        qualities.extend(addition)

    avg_quality = float(sum(qualities)) / float(num_students)
    return avg_quality
