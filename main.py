import housing

def main():
    house = housing.Housing()
    house.randomly_generate_rooms()
    house.randomly_generate_blocking_groups()

    house.run_adams()
    # house.print_lottery_statistics()

    # testing currier
    house.blocking_groups[0].set_rg_preferences()

if __name__== "__main__":
    main()
