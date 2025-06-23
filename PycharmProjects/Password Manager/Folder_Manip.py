"""
for i in range(0, 11):
    fichier = open("C:\\Users\\Benjamin\\Desktop\\python.txt", "a")
    fichier.write(f"Test{i}\n")
"""


def read_folder():
    fichier = open("C:\\Users\\Raphaël\\PycharmProjects\\Password Manager\\mdp.txt", "r")

    lists = []
    listclear = []
    lists += fichier.readlines()
    for i in lists:
        listclear.append(i.rstrip())
    dico = {}

    for i in range(0, len(listclear), 2):
        dico[listclear[i]] = listclear[i + 1]
    fichier.close()
    return dico
