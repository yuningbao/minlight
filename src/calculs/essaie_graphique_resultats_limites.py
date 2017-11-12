import pickle
import matplotlib.pyplot as plt

pickle_in = open("limites_faux_banc_test.pickle", "rb")
print(pickle_in)
limites = pickle.load(pickle_in)

fig = plt.figure()
ax  = fig.gca()

for rho, couples in limites.items():
    phi   = [couple[0] for couple in couples]
    theta = [couple[1] for couple in couples]

    line, = ax.plot(phi, theta)

    line.set_label('Rho = ' + "{r:0.2f}".format(r=rho/1000) + ' m')

ax.set_title('Angles Limites')
ax.set_xlabel('Theta [º]')
ax.set_ylabel('Phi [º]')

ax.set_xlim([0, 90])
ax.set_ylim([0, 90])

ax.legend()
plt.show()
