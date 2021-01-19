# import numpy as np
from matplotlib import pyplot as plt

# Lager lister for farten
liten_fart = [0]
middels_fart = [0]
stor_fart = [0]


# Åpner og leser av filene
with open('litenfallskjerm.txt', 'r') as file:
    liten_data = file.read()
with open('middelsfallskjerm.txt', 'r') as file:
    middels_data = file.read()
with open('storfallskjerm.txt', 'r') as file:
    stor_data = file.read()


def til_liste(data):
    """
    Fjerner uønsket tekst fra datasettet, og splitter opp i lister for å
    skille akselerasjon og tid.
    Returnerer en liste for tid, og en for akselerasjon.
    """
    data = data.replace('Verdiene for tid er gitt ved ', '')
    data = data.split('[')
    return datatrim(data[1]), datatrim(data[2])


def datatrim(data):
    """
    Lager en liste med alle verdiene, fjerner ']' fra det siste elementet.
    Fjerner whitespace.
    Returnerer en liste med floats.
    """
    liste = data.split(',')
    liste[-1] = liste[-1].replace(']', '')

    for index, item in enumerate(liste):
        liste[index] = float(item.strip())
    return liste


def integral(datatid, datasett, x):
    return (datatid[x+1]-datatid[x])*((datasett[x]+datasett[x+1]))/2


def lagfart(tid, fart, akselerasjon):
    for i, j in enumerate(tid[:-1]):
        fart.append(fart[i-1]+integral(tid, akselerasjon, i))


def skrivfil(fil, aks, tid):
    with open(fil+'.txt', 'w') as file:
        for i, j in enumerate(aks):
            akstxt = str(j)
            for _ in range(24-len(akstxt)):
                akstxt += ' '
            file.write(akstxt)
            file.write(str(tid[i])+'\n')


# Lager listene som trengs
liten_akselerasjon, liten_tid = til_liste(liten_data)
middels_akselerasjon, middels_tid = til_liste(middels_data)
stor_akselerasjon, stor_tid = til_liste(stor_data)


lagfart(liten_tid, liten_fart, liten_akselerasjon)
lagfart(middels_tid, middels_fart, middels_akselerasjon)
lagfart(stor_tid, stor_fart, stor_akselerasjon)

skrivfil('liten_aks', liten_akselerasjon, liten_tid)
skrivfil('middels_aks', middels_akselerasjon, middels_tid)
skrivfil('stor_aks', stor_akselerasjon, stor_tid)

plt.plot(liten_tid, liten_fart, 'r-')
plt.plot(middels_tid, middels_fart, 'b-')
plt.plot(stor_tid, stor_fart, 'g-')
plt.show()
