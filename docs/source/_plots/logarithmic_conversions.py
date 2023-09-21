import numpy as np
import itertools
import matplotlib.pyplot as plt

quant = ['Np','B','Bm/BmW/BW','BV/BuV','BuA','BOhm','BSPL','BSIL','BSWL','PR/AR','W','V','A','Ohm','Pa','W/m2']
nquant = len(quant)
idquant = list(range(nquant))

conv = [
    ['Np','B'],
    ['B','PR/AR'],
    ['Np','PR/AR'],
    ['Bm/BmW/BW','W'],
    ['BV/BuV','V'],
    ['BuA','A'],
    ['BOhm','Ohm'],
    ['BSPL','Pa'],
    ['BSIL','W/m2'],
    ['BSWL','W'],
]
for i in range(len(conv)):
    conv[i][0] = quant.index(conv[i][0])
    conv[i][1] = quant.index(conv[i][1])
conv = np.array(conv)

fig, axes = plt.subplots(1,1,figsize=(5,5),tight_layout=True)

ax = axes
ax.set_xticks(idquant)
ax.set_yticks(idquant)
ax.xaxis.set_major_locator(plt.MaxNLocator(nquant))
ax.yaxis.set_major_locator(plt.MaxNLocator(nquant))
#ax.set_xticklabels(quant, rotation='vertical', fontsize=8)
#ax.set_yticklabels(quant, rotation='horizontal', fontsize=8)
ax.set_axisbelow(True)
ax.grid()

ax.scatter(conv[:,0], conv[:,1])
#for q1, q2 in itertools.product(idquant,idquant):
#    where
#    print(q1, q2)

plt.savefig("logarithmic_conversions.png")