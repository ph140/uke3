import numpy as np
from matplotlib import pyplot as plt

with open('litenfallskjerm.txt', 'r') as file:
    data = file.read()


data = data.strip('Akselerasjonsverdiene er gitt ved ')
data = data.replace('Verdiene for tid er gitt ved ', '')
data = data.split('[')


def fiksdata(minliste):
    print(minliste)
    minliste.split(',')
    minliste[-1] = minliste[-1].replace(']', '')

    for index, item in enumerate(minliste):
        minliste[index] = float(item.strip())

    return minliste


aksel = fiksdata(data[1])
print(aksel)

#
# aks = data[1].split(',')
# tid = data[2].split(',')
#
# aks[-1] = aks[-1].replace(']', '')
# tid[-1] = tid[-1].replace(']', '')
#
#
# for index, item in enumerate(aks):
#     aks[index] = float(item.strip())
#
# for index, item in enumerate(tid):
#     tid[index] = float(item.strip())
#
# plt.plot(tid, aks, 'r--')
# plt.show()
