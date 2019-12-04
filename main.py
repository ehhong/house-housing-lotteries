import housing

def main():
    house = housing.Housing()
    house.randomly_generate_rooms()
    house.randomly_generate_blocking_groups()

    house.run_adams()
    house.print_lottery_statistics()

    # house.run_currier()
    # house.print_lottery_statistics()

if __name__== "__main__":
    main()
