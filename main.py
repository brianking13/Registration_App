import api

def next(choice):
    if choice == '1':
        api.add()
    elif choice == '2':
        api.remove()
    elif choice ==  '3':
        api.charge()
    else:
        choice = input('Please select a valid number: ')
        next(choice)


def main():
    api.initial_setup()
    choice = input('What would you like to do? \nChoose a number: \n[1] Add a Patient \n[2] Remove a Patient \n[3] Charge a Patient \nChoice: ')
    next(choice)





if __name__ == '__main__':
    main()
