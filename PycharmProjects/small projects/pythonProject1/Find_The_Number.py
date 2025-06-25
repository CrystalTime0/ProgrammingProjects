import random


def test_number(random_nb,i):
    user_number = int(input("Quel est votre proposition?\n"))

    if random_nb > user_number:
        print("Most\n")

    elif random_nb < user_number:
        print("Less\n")

    elif random_nb == user_number and i == 0:
        print('You Win In One Try !')
        exit()

    elif random_nb == user_number:
        print("You Win")
        exit()




if __name__ == '__main__':
    random_number = random.randint(0, 1)

    for i in range(10):
        test_number(random_number,i)

    print(random_number)
