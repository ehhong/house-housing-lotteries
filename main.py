import housing

def main():
    adams_1_score, adams_2_score, currier_score, dunster_score = 0, 0, 0, 0
    adams_1_sd_total, adams_2_sd_total, currier_sd_total, dunster_sd_total = 0, 0, 0, 0
    adams_1_time_total, adams_2_time_total, currier_time_total, dunster_time_total = 0, 0, 0, 0

    for i in range(10):
        print("ITERATION {}".format(i))
        house = housing.Housing()
        house.randomly_generate_rooms()
        house.randomly_generate_blocking_groups()
        house.set_bg_room_prefs()

        house.run_adams(is_random_rg_config = False)
        adams_1_avg, adams_1_sd, adams_1_time = house.print_lottery_statistics()
        adams_1_score += adams_1_avg
        adams_1_sd_total += adams_1_sd
        adams_1_time_total += adams_1_time

        house.run_adams(is_random_rg_config = True)
        adams_2_avg, adams_2_sd, adams_2_time = house.print_lottery_statistics()
        adams_2_score += adams_2_avg
        adams_2_sd_total += adams_2_sd
        adams_2_time_total += adams_2_time

        house.run_currier()
        currier_avg, currier_sd, currier_time = house.print_lottery_statistics()
        currier_score += currier_avg
        currier_sd_total += currier_sd
        currier_time_total += currier_time

        house.run_dunster()
        dunster_avg, dunster_sd, dunster_time = house.print_lottery_statistics()
        dunster_score += dunster_avg
        dunster_sd_total += dunster_sd
        dunster_time_total += dunster_time

if __name__== "__main__":
    main()
