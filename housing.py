from random import seed
from random import choice, randint

import blocking_group

# seed random number generator
seed(1)

class Housing:
    def __init__(self):
        self.num_rooms = 160
        self.num_students = 280
        self.rooms = [] # rooms are tuples: (size, proximity, quality)
        self.blocking_groups = [] # list of blocking_group objects

    def randomly_generate_rooms(self):
        ''' generate random room proximities and qualities based on fixed room size distribution '''
        room_size_quantities = [32, 80, 13, 24, 5, 3, 1, 2]
        i = 0

        while i < len(room_size_quantities):
            for j in range(room_size_quantities[i]):
                room_size = i + 1
                proximity = randint(1, 10)
                quality = randint(0, 10)
                self.rooms.append((room_size, proximity, quality))
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

            self.blocking_groups.append(blocking_group.BlockingGroup(curr_id, block_size))
            students_remaining = students_remaining - block_size
            curr_id += 1
