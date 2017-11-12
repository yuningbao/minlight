import pickle
import matplotlib.pyplot as plt

pickle_in = open("limites_faux_banc_test.pickle", "rb")
print(pickle_in)
limites = pickle.load(pickle_in)

print(limites)

fig = plt.figure()
ax  = fig.gca()


lines = {}

for rho, couples in limites.items():
    phi   = [couple[0] for couple in couples]
    theta = [couple[1] for couple in couples]

    line, = ax.plot(phi, theta)

    lines[rho] = line

plt.show()
