import numpy as np
from matplotlib import pyplot as plt


with open('litenfallskjerm.txt', 'r') as file:
    liten_data = file.read()
with open('middelsfallskjerm.txt', 'r') as file:
    middels_data = file.read()
with open('storfallskjerm.txt', 'r') as file:
    stor_data = file.read()


def til_liste(data):
    data = data.strip('Akselerasjonsverdiene er gitt ved ')
    data = data.replace('Verdiene for tid er gitt ved ', '')
    data = data.split('[')
    return fiksdata(data[1]), fiksdata(data[2])


def fiksdata(liste):
    liste = liste.split(',')
    liste[-1] = liste[-1].replace(']', '')

    for index, item in enumerate(liste):
        liste[index] = float(item.strip())
    return liste


liten_akselerasjon, liten_tid = til_liste(liten_data)
middels_akselerasjon, middels_tid = til_liste(middels_data)
stor_akselerasjon, stor_tid = til_liste(stor_data)


plt.plot(liten_tid, liten_akselerasjon, 'r-')
plt.plot(middels_tid, middels_akselerasjon, 'b-')
plt.plot(stor_tid, stor_akselerasjon, 'g-')
plt.show()
