from random import seed
from random import choice, randint, shuffle
import numpy
from time import time

import blocking_group as bg

# seed random number generator
# seed(1)

class Housing:
    def __init__(self):
        self.num_rooms = 160
        self.num_students = 280
        self.rooms = [[] for x in range(9)] # list of lists, where first index is room size
                                            # rooms are tuples: (room id, proximity, quality, size)
        self.blocking_groups = [] # list of blocking_group objects
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
        self.time_elapsed = None

    def randomly_generate_rooms(self):
        ''' generate random room proximities and qualities based on fixed room size distribution '''
        room_size_quantities = [32, 80, 13, 24, 5, 3, 1, 2]
        i = 0
        # unique id for each room
        counter = 0

        while i < len(room_size_quantities):
            for j in range(room_size_quantities[i]):
                room_id = counter
                counter += 1
                proximity = randint(1, 10)
                quality = randint(0, 10)
                self.rooms[i + 1].append((room_id, proximity, quality))
            i += 1

        # print(self.rooms)

    def randomly_generate_blocking_groups(self):
        ''' randomly generate blocking group sizes from blocking size distribution '''
        students_remaining = self.num_students
        curr_id = 0

        # distribution information from HODP: https://medium.com/harvard-open-data-project/harvard-housing-part-2-how-do-students-form-groups-a4c95cdf97a6
        blocking_size_dist = [1] * 9 + [2] * 6 + [3] * 7 + [4] * 12 + [5] * 13 + [6] * 19 + [7] * 16 + [8] * 18

        while students_remaining > 0:
            block_size = choice(blocking_size_dist) # randomly choose item from blocking_size_dist

            if block_size > students_remaining:
                block_size = students_remaining

            self.blocking_groups.append(bg.BlockingGroup(curr_id, block_size, self))
            students_remaining = students_remaining - block_size
            curr_id += 1

    def set_bg_room_prefs(self):
        for bg in self.blocking_groups:
            bg.set_preferences()

    def run_adams(self, is_random_rg_config = True):
        ''' run adams house style lottery, returns blocking group assignments.
            is_random_rg_config := true means randomly assigning committed rg configs
            return # of unallocated people '''

        #testing
        for bg in self.blocking_groups:
            bg.set_general_rg_preferences()

        if (is_random_rg_config):
            print("=== Running ADAMS with random RG configs ===")
        else:
            print("=== Running ADAMS with opt RG configs ===")

        start = time()

        # blocking groups choose rooming configurations according to room size distribution/randomly
        for bg in self.blocking_groups:
            rg_config = choice(self.rg_configs[bg.size])
            bg.set_rg_config(is_random_rg_config)

        # generate blocking group preferences
        print("setting ADAMS bg preferences")
        for bg in self.blocking_groups:
            bg.set_rg_config_preferences()
        print("done setting ADAMS preferences")

        # run RSD
        shuffle(self.blocking_groups)
        taken_rooms = []
        unallocated_ppl_count = 0

        for bg in self.blocking_groups:
            chosen_rooms = []
            room_prefs = bg.rg_preferences
            i = 0
            while chosen_rooms == []:
                try:
                    desired_rooms = room_prefs[i]
                    # check if each room in the combo has been taken
                    for room in desired_rooms[1]:
                        room_id = room[0]
                        if room_id not in taken_rooms:
                            chosen_rooms.append(room)
                        else:
                            chosen_rooms = []
                            # go to the next combination in the preference order
                            i += 1
                            break
                except IndexError: # unallocated by end of lottery
                    unallocated_ppl_count += bg.size
                    chosen_rooms = [(None, None, 3, bg.size)] # default quality 3 for whole bg

            # update chosen rooms
            bg.assigned_rooms = chosen_rooms
            if (chosen_rooms[0][0]): # if actual room allocated
                taken_rooms.extend([room_id for (room_id, _, _, _) in chosen_rooms])

        end = time()
        self.time_elapsed = end - start

        print("# of unallocated people: %i" % unallocated_ppl_count)

        return unallocated_ppl_count

    def run_currier(self):
        print("=== Running CURRIER ===")
        start = time()
        # generate blocking group preferences
        print("setting CURRIER bg preferences")
        for bg in self.blocking_groups:
            bg.set_full_rg_preferences()
        print("done setting CURRIER preferences")

        # run RSD
        shuffle(self.blocking_groups)
        taken_rooms = []
        for bg in self.blocking_groups:
            chosen_rooms = []
            room_prefs = bg.rg_preferences
            i = 0
            while chosen_rooms == []:
                desired_rooms = room_prefs[i]
                # check if each room in the combo has been taken
                for room in desired_rooms[1]:
                    room_id = room[0]
                    if room_id not in taken_rooms:
                        chosen_rooms.append(room)
                    else:
                        chosen_rooms = []
                        # go to the next combination in the preference order
                        i += 1
                        break
            # update chosen rooms
            bg.assigned_rooms = chosen_rooms
            taken_rooms.extend([room_id for (room_id, _, _, _) in chosen_rooms])

        end = time()
        self.time_elapsed = end - start
        return self.blocking_groups

    def run_dunster(self):
        print("=== Running DUNSTER ===")
        start = time()

        # decide who enters specialized housing lottery
        for bg in self.blocking_groups:
            best_size = (-1, -1)
            for room_size in bg.preferences[1:]:
                qualities = [quality for (_, _, quality, size) in room_size]
                avg_quality = float(sum(qualities)) / float(len(room_size))
                if avg_quality > best_size[1]:
                    best_size = (size, avg_quality)
            if best_size[0] >= 5 and best_size[0] == bg.size:
                bg.specialized = True

        # run specialized lottery
        print("running specialized lottery")
        shuffle(self.blocking_groups)
        taken_rooms = []
        for bg in self.blocking_groups:
            if bg.specialized:
                chosen_room = None
                for room in bg.preferences[bg.size]:
                    if room[0] not in taken_rooms:
                        chosen_room = room
                        bg.assigned_rooms = [chosen_room]
                        taken_rooms.append(room[0])
                        break
                if chosen_room is None:
                    # drop down to general lottery
                    bg.specialized = False

        # run general lottery
        print("running general lottery")
        for bg in self.blocking_groups:
            if not bg.specialized:
                bg.set_general_rg_preferences()
                chosen_rooms = []
                room_prefs = bg.rg_preferences
                i = 0
                while chosen_rooms == []:
                    desired_rooms = room_prefs[i]
                    # check if each room in the combo has been taken
                    for room in desired_rooms[1]:
                        room_id = room[0]
                        if room_id not in taken_rooms:
                            chosen_rooms.append(room)
                        else:
                            chosen_rooms = []
                            # go to the next combination in the preference order
                            i += 1
                            break
                # update chosen rooms
                bg.assigned_rooms = chosen_rooms
                taken_rooms.extend([room_id for (room_id, _, _, _) in chosen_rooms])

        end = time()
        self.time_elapsed = end - start
        return self.blocking_groups

    def print_lottery_statistics(self):
        # calculate average quality and standard deviation
        qualities = []

        for bg in self.blocking_groups:
            for (_, _, quality, size) in bg.assigned_rooms:
                addition = [quality for i in range(size)]
                qualities.extend(addition)

        avg_quality = float(sum(qualities)) / float(self.num_students)
        sd = numpy.array(qualities).std()
        print("average: {}".format(avg_quality))
        print("sd: {}".format(sd))
        print("time: {}".format(self.time_elapsed))
        return(avg_quality, sd, self.time_elapsed)
