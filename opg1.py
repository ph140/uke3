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


# Integrasjon ved trapesmetoden
def trapes_metode(x, y, indeks):
    return (x[indeks+1]-x[indeks])*((y[indeks]+y[indeks+1]))/2


# Returnerer en liste med integrete verdier av argument-listen
def integrasjon(tid, y_verdier0):
    y_verdier1 = [0]
    for indeks, j in enumerate(tid[:-1]):
        y_verdier1.append(y_verdier1[indeks-1] +
                          trapes_metode(tid, y_verdier0, indeks))
    return y_verdier1


def finn_k(tid, fart, avvik=99999, k=0.01):
    g = 9.81  # tyngdeakselerasjon
    m = 0.37  # vekten til ballen
    nytt_avvik = 0

    t0 = 0  # Starttid er 0
    tslutt = tid[-1]  # Slutt-tid er samme som siste element i fartslisten
    N = 500  # 500 steg som i fartslisten
    h = (tslutt-t0)/(N-1)  # Samme tidsintervalll som i tidslisten

    v = np.zeros(N)  # Liste der vi fyller inn verdier for fart
    t = np.zeros(N)  # Liste der vi fyller inn verdier for tid

    for i in range(N-1):
        v[i+1] = v[i] + h * (g - k * v[i]**2 / m)
        t[i+1] = t[i] + h

    # Regner ut hvor mye prognosen avviker fra de målte dataene
    for i in range(500):
        nytt_avvik += abs(v[i]-fart[i])

    # Dersom avviket er mindre enn det forrige fortsetter algoritmen med 0.01
    # større k-verdi, for å se om det kan bli enda mindre avvik.
    if nytt_avvik < avvik:
        k += 0.01
        k, v = finn_k(tid, fart, nytt_avvik, k)

    # Returnerer det minste avviket
    return(k, v)


class FallSkjerm():
    def __init__(self, navn, radius, color):
        self.navn = navn
        self.data = self.getData()
        self.akselerasjon, self.tid = til_liste(self.data)
        self.fart = integrasjon(self.tid, self.akselerasjon)
        self.distanse = integrasjon(self.tid, self.fart)
        self.k, self.v = finn_k(self.tid, self.fart)
        self.radius = radius
        self.areal = round(np.pi*self.radius**2, 5)
        self.forhold = round(self.areal/self.k, 5)
        self.color = color
        self.lagre()
        self.laggraf()

    def getData(cls):
        with open(cls.navn+'fallskjerm.txt', 'r') as file:
            return file.read()

    # Lagrer akselersajonsverdiene i kolonneform i nye filer.
    def lagre(cls):
        filnavn = cls.navn+'_akselerasjon.txt'
        with open(filnavn, 'w') as file:
            for i, j in enumerate(cls.akselerasjon):
                akstxt = str(j)
                for _ in range(24-len(akstxt)):
                    akstxt += ' '
                file.write(akstxt+str(cls.tid[i])+'\n')

    # Plotter grafer for fart, prognose-fart og distanse
    def laggraf(cls):
        plt.plot(cls.tid, cls.v, cls.color+'--', label='Prognose')
        plt.plot(cls.tid, cls.fart, cls.color, label='Målte data')
        plt.plot(cls.tid, cls.distanse, cls.color+':', label='Distanse')


# Lager de tre instansene av fallskjermene
liten = FallSkjerm('liten', 0.11, 'r')
middels = FallSkjerm('middels', 0.17, 'g')
stor = FallSkjerm('stor', 0.26, 'b')

# Lager aksetitler og viser grafen
plt.xlabel('Tid (s)')
plt.ylabel('Fart (m/s)')
plt.legend()
plt.show()
