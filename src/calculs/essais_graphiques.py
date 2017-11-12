
'''
fig = plt.figure()
ax = fig.gca(projection='3d')
ax.set_aspect("equal")

# draw cube
r = [-1, 1]
for s, e in combinations(np.array(list(product(r, r, r))), 2):
    if np.sum(np.abs(s-e)) == r[1]-r[0]:
        ax.plot3D(*zip(s, e), color="b")

# draw sphere
u, v = np.mgrid[0:2*np.pi:20j, 0:np.pi:10j]
x = np.cos(u)*np.sin(v)
y = np.sin(u)*np.sin(v)
z = np.cos(v)
ax.plot_wireframe(x, y, z, color="r")

# draw a point
ax.scatter([0], [0], [0], color="g", s=100)

# draw a vector
from matplotlib.patches import FancyArrowPatch
from mpl_toolkits.mplot3d import proj3d


class Arrow3D(FancyArrowPatch):

    def __init__(self, xs, ys, zs, *args, **kwargs):
        FancyArrowPatch.__init__(self, (0, 0), (0, 0), *args, **kwargs)
        self._verts3d = xs, ys, zs

    def draw(self, renderer):
        xs3d, ys3d, zs3d = self._verts3d
        xs, ys, zs = proj3d.proj_transform(xs3d, ys3d, zs3d, renderer.M)
        self.set_positions((xs[0], ys[0]), (xs[1], ys[1]))
        FancyArrowPatch.draw(self, renderer)

a = Arrow3D([0, 1], [0, 1], [0, 1], mutation_scale=20,
            lw=1, arrowstyle="-|>", color="k")
ax.add_artist(a)
plt.show()

from time import sleep
sleep(3)

import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, 6*np.pi, 100)
y = np.sin(x)

# You probably won't need this if you're embedding things in a tkinter plot...
plt.ion()

fig = plt.figure()
ax = fig.add_subplot(111)
line1, = ax.plot(x, y, 'r-') # Returns a tuple of line objects, thus the comma

for phase in np.linspace(0, 10*np.pi, 500):
    line1.set_ydata(np.sin(x + phase))
    fig.canvas.draw()


'''




from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
from itertools import product, combinations
from numpy import cross
from entites import *
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.art3d as art3d
from time import sleep

def face_carre(s1, s2, s3, s4):
    p1 = s1.T.tolist()[0]
    p2 = s2.T.tolist()[0]
    p3 = s3.T.tolist()[0]
    p4 = s4.T.tolist()[0]
    return np.array([p1, p2, p3, p4])

def faces_cube(sommets):
    faces = {}
    faces['xy0'] = face_carre(s1= sommets['S000'], s2= sommets['S100'], s3= sommets['S110'], s4= sommets['S010'])
    faces['xy1'] = face_carre(s1= sommets['S001'], s2= sommets['S101'], s3= sommets['S111'], s4= sommets['S011'])
    faces['x0z'] = face_carre(s1= sommets['S000'], s2= sommets['S100'], s3= sommets['S101'], s4= sommets['S001'])
    faces['x1z'] = face_carre(s1= sommets['S010'], s2= sommets['S110'], s3= sommets['S111'], s4= sommets['S011'])
    faces['0yz'] = face_carre(s1= sommets['S000'], s2= sommets['S010'], s3= sommets['S011'], s4= sommets['S001'])
    faces['1yz'] = face_carre(s1= sommets['S100'], s2= sommets['S110'], s3= sommets['S111'], s4= sommets['S101'])
    return faces

def arete_cube(s1, s2):
    return tuple([coord1, coord2] for coord1, coord2 in zip(s1.get_coordonnees(), s2.get_coordonnees()))

def aretes_cube(sommets):
    aretes = {}
    aretes['x00'] = arete_cube(sommets['S000'], sommets['S100'])
    aretes['x01'] = arete_cube(sommets['S001'], sommets['S101'])
    aretes['x10'] = arete_cube(sommets['S010'], sommets['S110'])
    aretes['x11'] = arete_cube(sommets['S011'], sommets['S111'])
    aretes['0y0'] = arete_cube(sommets['S000'], sommets['S010'])
    aretes['0y1'] = arete_cube(sommets['S001'], sommets['S011'])
    aretes['1y0'] = arete_cube(sommets['S100'], sommets['S110'])
    aretes['1y1'] = arete_cube(sommets['S101'], sommets['S111'])
    aretes['00z'] = arete_cube(sommets['S000'], sommets['S001'])
    aretes['01z'] = arete_cube(sommets['S010'], sommets['S011'])
    aretes['10z'] = arete_cube(sommets['S100'], sommets['S101'])
    aretes['11z'] = arete_cube(sommets['S110'], sommets['S111'])
    return aretes

pave = Pave(centre = Vecteur3D(0,0,0),
            ypr_angles = TupleAnglesRotation(0,0,0),
            dimensions = DimensionsPave(2,2,2))

sommets = pave.get_dictionnaire_sommets()

plt.ion()
fig = plt.figure()
ax = fig.gca(projection='3d')

aretes = {}

for arete, sommets_arete in aretes_cube(sommets).items():
    line, = ax.plot(*sommets_arete, color='k', linewidth=3)
    aretes[arete] = line

fig.show()
ax.imshow()
print('!!!!!!!!!!!!!!!!!!!!11')

faces = {}
for face, sommets_face in faces_cube(sommets).items():
    poly = art3d.Poly3DCollection([sommets_face])
    ax.add_collection3d(poly)
    faces[face] = poly
    poly.set_3d_properties()


for face in faces.values():
    ax.collections.remove(face)


'''
from entites import *

class PaveDraw(Pave):

    def draw(self, axe):
        xs = []
        ys = []
        zs = []

        for sommet in self.sommets_pave():
            x, y, z = sommet.get_coordonnees()
            xs.append(x)
            ys.append(y)
            zs.append(z)

        axe.plot_trisurf(X=xs, Y=ys, Z=zs, color='b')


pave = PaveDraw(centre=Vecteur3D(x=0,y=0,z=0), ypr_angles=TupleAnglesRotation(0,0,0), dimensions=DimensionsPave(1,1,1))

fig = plt.figure()
ax = fig.gca(projection='3d')

#pave.draw(ax)

'''

