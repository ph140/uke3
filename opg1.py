# usr/bin/!
import numpy as np
from matplotlib import pyplot as plt


def datatrim(data):
    """
    Lager en liste med alle verdiene, fjerner ']' fra det siste elementet.
    Fjerner whitespace.
    Returnerer en liste med floats.
    """
    liste = data.split(',')
    liste[-1] = liste[-1].replace(']', '')

    for i, verdi in enumerate(liste):
        liste[i] = float(verdi.strip())
    return liste


# Integrasjon ved trapesmetoden
def trapes_metode(x, y, i):
    return (x[i+1] - x[i]) * ((y[i] + y[i+1])) / 2


class FallSkjerm():
    def __init__(self, navn, radius, color):
        self.navn = navn
        self.akselerasjon, self.tid = self.hentData()
        self.fart = self.integrasjon(self.akselerasjon)
        self.distanse = self.integrasjon(self.fart)
        self.k, self.v = self.finn_k()
        self.radius = radius
        self.areal = round(np.pi*self.radius**2, 5)
        self.forhold = round(self.areal/self.k, 5)
        self.color = color
        self.lagre()
        self.laggraf()
        self.skriv_svar()

    # Returnerer en liste med akselerasjon, og en med tid
    def hentData(cls):
        with open(cls.navn+'fallskjerm.txt', 'r') as file:
            data = file.read()
        data = data.replace('Verdiene for tid er gitt ved ', '')
        data = data.split('[')
        return datatrim(data[1]), datatrim(data[2])

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

    # Printer areal, k-verdi og forhold.
    def skriv_svar(cls):
        navn = cls.navn
        navn = navn.capitalize()
        print(f'{navn} fallskjerm:')
        print(f'Radius: {cls.radius}')
        print(f'Areal: {cls.areal}')
        print(f'K-verdi: {cls.k}')
        print(f'Forhold: {cls.forhold}\n')

    def finn_k(cls, k=0.01, avvik=9999):
        g = 9.81  # tyngdeakselerasjon
        m = 0.37  # vekten til ballen
        nytt_avvik = 0  # Lager ny avvik for ny k-verdi
        tslutt = cls.tid[-1]  # Slutt-tid er lik siste element i tidslisten
        N = 500  # 500 steg som i fartslisten
        h = (tslutt)/(N-1)  # Samme tidsintervalll som i tidslisten

        v = np.zeros(N)  # Liste der vi fyller inn verdier for fart
        t = np.zeros(N)  # Liste der vi fyller inn verdier for tid

        # Eulers metode
        for i in range(N-1):
            v[i+1] = v[i] + h * (g - k * v[i]**2 / m)
            t[i+1] = t[i] + h

        # Regner ut hvor mye prognosen avviker fra de målte dataene
        for i in range(500):
            nytt_avvik += abs(v[i]-cls.fart[i])

        # Om avviket er mindre enn det forrige fortsetter algoritmen med 0.01
        # større k-verdi, for å se om det kan bli enda mindre avvik.
        if nytt_avvik < avvik:
            k += 0.01
            k, v = cls.finn_k(k, nytt_avvik)

        # Returnerer det minste avviket, og fartslisten for den k-verdien
        return(round(k, 5), v)

    def integrasjon(cls, y_verdier):
        y = [0]
        for i, tid in enumerate(cls.tid[:-1]):
            y.append(y[i-1] + trapes_metode(cls.tid, y_verdier, i))
        return y


# Lager de tre instansene av fallskjermene
liten = FallSkjerm('liten', 0.11, 'r')
middels = FallSkjerm('middels', 0.17, 'g')
stor = FallSkjerm('stor', 0.26, 'b')

# Lager aksetitler, legend og viser grafen
plt.xlabel('Tid (s)')
plt.ylabel('Fart (m/s)')
plt.legend()
plt.show()
