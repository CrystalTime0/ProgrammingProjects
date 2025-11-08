import random


def verify_number(random_nb,nb_try):
    user_number = int(input("Quel est votre proposition?\n"))

    if random_nb > user_number:
        print("Most\n")

    elif random_nb < user_number:
        print("Less\n")

    elif random_nb == user_number and nb_try == 0:
        print('You Win In One Try !')
        exit()

    elif random_nb == user_number:
        print(f"You Win in {nb_try} tries")
        exit()




if __name__ == '__main__':
    random_number = random.randint(0, 1000)

    for i in range(10):
        verify_number(random_number,i)

    print(random_number)
