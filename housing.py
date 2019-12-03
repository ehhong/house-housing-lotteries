from random import seed
from random import choice, randint

import blocking_group as bg

# seed random number generator
seed(1)

class Housing:
    def __init__(self):
        self.num_rooms = 160
        self.num_students = 280
        self.rooms = [[] for x in range(9)] # list of lists, where first index is room size
                                            # rooms are tuples: (size, proximity, quality)
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

    def run_adams(self):
        ''' run adams house style lottery '''
        num_eight_suites = 2

        # blocking groups choose rooming configurations according to room size distribution/randomly
        for bg in self.blocking_groups:
            rg_config = choice(self.rg_configs[bg.size])

            # ensure that all 8-man suites are requested
            if bg.size == 8 and num_eight_suites > 0:
                rg_config = self.rg_configs[bg.size][0]
                num_eight_suites = num_eight_suites - 1

            print(rg_config)
            bg.set_rg_config(rg_config)

        # blocking groups rank preferences under committed rooming configurations
        

        # run RSD for all blocking groups
            # if no rooms left, drop to bottom of lottery and choose randomly at end
