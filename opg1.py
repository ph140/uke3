import numpy as np
from matplotlib import pyplot as plt


def trapes_metode(x, y, i):
    return (x[i+1] - x[i]) * ((y[i] + y[i+1]))


class fallSkjerm():
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

    def hentData(cls):
        with open(cls.navn+'fallskjerm.txt', 'r') as file:
            data = file.read()

        aks = list(map(float, data.split("[")[1].split("]")[0].split(", ")))
        tid = list(map(float, data.split("[")[2].split("]")[0].split(", ")))
        return aks, tid

    # Lagrer akselersajonsverdiene i kolonneform i nye filer.
    def lagre(cls):
        with open(cls.navn+'_akselerasjon.txt', 'w') as file:
            for i, j in enumerate(cls.akselerasjon):
                akstxt = str(j) + (24-len(str(j)))*' '
                file.write(akstxt + str(cls.tid[i]) + '\n')

    # Plotter grafer for fart, prognose-fart og distanse
    def laggraf(cls):
        plt.plot(cls.tid, cls.v, cls.color+'--', label='Prognose')
        plt.plot(cls.tid, cls.fart, cls.color, label='Målte data')
        plt.plot(cls.tid, cls.distanse, cls.color+':', label='Distanse')

    # Printer areal, k-verdi og forhold.
    def skriv_svar(cls):
        print(f'{cls.navn.capitalize()} fallskjerm:')
        print(f'Forhold: {cls.forhold}')
        print(f'Distanse: {cls.distanse[-1]}\n')

    def finn_k(cls, k=0.01, avvik=9999):
        g = 9.81  # tyngdeakselerasjon
        m = 0.37  # vekten til ballen
        nytt_avvik = 0  # Lager ny avvik for ny k-verdi
        # Slutt-tid er lik siste element i tidslisten
        tslutt = cls.tid[-1]
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
        if abs(nytt_avvik) < abs(avvik):
            k += 0.001
            k, v = cls.finn_k(k, nytt_avvik)

        # Returnerer det minste avviket, og fartslisten for den k-verdien
        return(round(k, 5), v)

    def integrasjon(cls, y_verdier):
        y = [0]
        for i, tid in enumerate(cls.tid[:-1]):
            y.append(y[i-1] + trapes_metode(cls.tid, y_verdier, i))
        return y


# Lager de tre instansene av fallskjermene
liten = fallSkjerm('liten', 0.11, 'r')
middels = fallSkjerm('middels', 0.17, 'g')
stor = fallSkjerm('stor', 0.26, 'b')

# Lager aksetitler, legend og viser grafen
plt.xlabel('Tid (s)')
plt.ylabel('Fart (m/s)')
plt.legend()
plt.show()
