import housing

def main():
    house = housing.Housing()
    house.randomly_generate_rooms()
    house.randomly_generate_blocking_groups()
    
    print("Hello World!")

if __name__== "__main__":
    main()
