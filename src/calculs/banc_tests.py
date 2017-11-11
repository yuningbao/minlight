from parametres import *
from outils import *
from numpy import pi

maisonette = {
      'centre' :
            point_3d(
                  x = 3500 + 5000/2,
                  y = 2500,
                  z = 2000
            ),
      'dimensions' :
            dimensions_pave(
                  longueur = 5000,
                  largeur  = 2500,
                  hauteur  = 2900
            )
}

dimensions_source = dimensions_pave(
      longueur = 600,
      largeur  = 1600,
      hauteur  = 1600
)

chambre = {
      'dimensions' :
            dimensions_pave(
                  longueur = 8500,
                  largeur  = 5000,
                  hauteur  = 4000
            )
}

ancrage_x = 3500
ancrage_y = 5000
ancrage_z = 4000

configs_ancrage = {
      'S000' : point_3d(        0,         0,         0),
      'S100' : point_3d(ancrage_x,         0,         0),
      'S010' : point_3d(        0, ancrage_y,         0),
      'S110' : point_3d(ancrage_x, ancrage_y,         0),
      'S001' : point_3d(        0,         0, ancrage_z),
      'S101' : point_3d(ancrage_x,         0, ancrage_z),
      'S011' : point_3d(        0, ancrage_y, ancrage_z),
      'S111' : point_3d(ancrage_x, ancrage_y, ancrage_z)
}

space_recherche = space_recherche(
      space_rho   = intervalle_lineaire_pas(min= 0, max= 3750, pas=  250),
      space_phi   = intervalle_lineaire_pas(min= 0, max= pi/2, pas= pi/60),
      space_theta = intervalle_lineaire_pas(min= 0, max= pi,   pas= pi/30)
)

systeme_spherique_baie_vitree = \
      systeme_spherique(
            centre     = point_3d(
                  x = 3500,
                  y = 5000/2,
                  z = 2900/2
            ),
            ypr_angles = ypr_angles(
                  yaw   = pi,
                  pitch = 0,
                  row   = 0
            )
      )

limites = trouver_angles_limites(
      space_recherche,
      maisonette,
      dimensions_source,
      chambre,
      configs_ancrage,
      systeme_spherique_baie_vitree
)

pprint(limites)

# ConflitDePosition(100,100,300,0.52,0.24,Pa,1000)

"""
ConflitDePosition(creerPoint(100,100,300),0,0,Pa,1000)
ConflitDePosition(creerPoint(600,250,200),0,0,Pa,1000)
ConflitDePosition(creerPoint(100,50,100),0,0,Pa,1000)
ConflitDePosition(creerPoint(100,200,40),0,0,Pa,1000)
"""

# print(appartientVolumeSoleil(creerPoint(0,0,0), creerPoint(0,0,0), 0, 0))
# print(appartientVolumeSoleil(creerPoint(40,40,40), creerPoint(200,200,200), 0, 0))
# print(appartientVolumeSoleil(creerPoint(200,200,200), creerPoint(200,200,200), 0, 0))
# print(appartientVolumeSoleil(creerPoint(200,200,200), creerPoint(200,200,200), math.pi/4, math.pi/4))
# print(appartientVolumeSoleil(creerPoint(205,205,205), creerPoint(200,200,200), math.pi/4, math.pi/4))
