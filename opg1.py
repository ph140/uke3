import numpy as np
from matplotlib import pyplot as plt


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


def lagfart(tid, akselerasjon):
    fart = [0]
    for i, j in enumerate(tid[:-1]):
        fart.append(fart[i-1]+integral(tid, akselerasjon, i))
    return fart


def skrivfil(fil, aks, tid):
    with open('aksfiler/'+fil+'.txt', 'w') as file:
        for i, j in enumerate(aks):
            akstxt = str(j)
            for _ in range(24-len(akstxt)):
                akstxt += ' '
            file.write(akstxt)
            file.write(str(tid[i])+'\n')


def find_k(tid, fart, avvik=99999, k=0.01):
    g = 9.81  # tyngdeakselerasjon
    m = 0.37  # vekten til ballen
    ny_avvik = 0

    t0 = 0  # Starttid er 0
    tslutt = tid[-1]  # Slutt-tid er samme som siste element i fartslisten
    N = 500  # 500 steg som i fartslisten
    h = (tslutt-t0)/(N-1)  # Samme tidsintervalll som i tidslisten

    v = np.zeros(N)  # Liste der vi fyller inn verdier for fart
    t = np.zeros(N)  # Liste der vi fyller inn verdier for tid

    for i in range(N-1):
        v[i+1] = v[i] + h * (g - k * v[i]**2 / m)
        t[i+1] = t[i] + h

    for i in range(500):
        ny_avvik += abs(v[i]-fart[i])

    if ny_avvik < avvik:
        k += 0.01
        k, v = find_k(tid, fart, ny_avvik, k)
    return(k, v)


# Åpner og leser av filene
with open('litenfallskjerm.txt', 'r') as file:
    liten_data = file.read()
with open('middelsfallskjerm.txt', 'r') as file:
    middels_data = file.read()
with open('storfallskjerm.txt', 'r') as file:
    stor_data = file.read()

# Lager listene som trengs
liten_akselerasjon, liten_tid = til_liste(liten_data)
middels_akselerasjon, middels_tid = til_liste(middels_data)
stor_akselerasjon, stor_tid = til_liste(stor_data)

# Beregner fart
liten_fart = lagfart(liten_tid, liten_akselerasjon)
middels_fart = lagfart(middels_tid, middels_akselerasjon)
stor_fart = lagfart(stor_tid, stor_akselerasjon)

# Beregner distanse
liten_distanse = lagfart(liten_tid, liten_fart)
middels_distanse = lagfart(middels_tid, middels_fart)
stor_distanse = lagfart(stor_tid, stor_fart)

# Lagrer akselerasjon og tid i filer
skrivfil('liten_aks', liten_akselerasjon, liten_tid)
skrivfil('middels_aks', middels_akselerasjon, middels_tid)
skrivfil('stor_aks', stor_akselerasjon, stor_tid)

# Beregner k-verdier, og farts-prognoser basert på eulers metode
liten_k, v1 = find_k(liten_tid, liten_fart)
middels_k, v2 = find_k(middels_tid, middels_fart)
stor_k, v3 = find_k(stor_tid, stor_fart)

# Radius-verdier oppgitt i oppgaven
liten_radius = 0.11
middels_radius = 0.17
stor_radius = 0.33

liten_areal = round(np.pi*liten_radius**2, 5)
middels_areal = round(np.pi*middels_radius**2, 5)
stor_areal = round(np.pi*stor_radius**2, 5)

liten_ratio = round(liten_areal/liten_k, 5)
middels_ratio = round(middels_areal/middels_k, 5)
stor_ratio = round(stor_areal/stor_k, 5)


print(f'Liten_k: {liten_k}\nMiddels k: {middels_k}\nStor_k: {stor_k}\n\n\n')
print(f'Liten: {liten_areal}\nMiddels: {middels_areal}\nStor: {stor_areal}\n')
print(f'Liten: {liten_ratio}\nMiddels: {middels_ratio}\nStor: {stor_ratio}\n')
print(f'{liten_distanse[-1]}\n {middels_distanse[-1]}\n {stor_distanse[-1]}')

plt.plot(liten_tid, v1, 'r--', label='fart av prognose')
plt.plot(liten_tid, liten_fart, 'r-', label='fart av data')
plt.plot(liten_tid, liten_distanse, 'r:', label='distanse')
plt.plot(middels_tid, v2, 'b--')
plt.plot(middels_tid, middels_fart, 'b-')
plt.plot(middels_tid, middels_distanse, 'b:')
plt.plot(stor_tid, v3, 'g-')
plt.plot(stor_tid, stor_fart, 'g-')
plt.plot(stor_tid, stor_distanse, 'g:')
plt.xlabel('Tid (s)')
plt.ylabel('Fart (m/s)')
plt.legend()
plt.show()
