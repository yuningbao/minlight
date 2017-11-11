from outils2 import *
from entites import *

maisonette = Pave(
      centre = Vecteur3D(
                  x = 3500 + 5000/2,
                  y = 5000/2,
                  z = 2900/2
      ),
      ypr_angles = TupleAnglesRotation(0,0,0),
      dimensions = DimensionsPave(
            longueur = 5000,
            largeur  = 2500,
            hauteur  = 2900
      )
)

dimensions_source = DimensionsPave(
      longueur = 600,
      largeur  = 1600,
      hauteur  = 1600
)

chambre = Pave(
      centre = Vecteur3D(0,0,0),
      ypr_angles = TupleAnglesRotation(0,0,0),
      dimensions = DimensionsPave(
            longueur = 8500,
            largeur  = 5000,
            hauteur  = 4000
      )
)

ancrage_x = 3500
ancrage_y = 5000
ancrage_z = 4000

configs_ancrage = {
      'S000' : Vecteur3D(        0,         0,         0),
      'S100' : Vecteur3D(ancrage_x,         0,         0),
      'S010' : Vecteur3D(        0, ancrage_y,         0),
      'S110' : Vecteur3D(ancrage_x, ancrage_y,         0),
      'S001' : Vecteur3D(        0,         0, ancrage_z),
      'S101' : Vecteur3D(ancrage_x,         0, ancrage_z),
      'S011' : Vecteur3D(        0, ancrage_y, ancrage_z),
      'S111' : Vecteur3D(ancrage_x, ancrage_y, ancrage_z)
}

space_recherche = SpaceRechercheAnglesLimites(
      intervalle_rho   = IntervalleLineaire(min= 0, max= 3501, pas=  250),
      intervalle_phi   = IntervalleLineaire(min= 0, max= 90, pas= pi/60),
      intervalle_theta = IntervalleLineaire(min= 0, max= pi,   pas= pi/30)
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
