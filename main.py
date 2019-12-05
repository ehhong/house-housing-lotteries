import housing

def main():
    house = housing.Housing()
    house.randomly_generate_rooms()
    house.randomly_generate_blocking_groups()
    house.set_bg_room_prefs()

    house.run_adams(False)
    house.print_lottery_statistics()

    house.run_adams(True)
    house.print_lottery_statistics()

    house.run_currier()
    house.print_lottery_statistics()

if __name__== "__main__":
    main()
