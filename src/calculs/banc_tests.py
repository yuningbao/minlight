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

config_ancrage = ConfigurationAncrage(
    configs_cables = [
        ConfigurationCable(
            point_ancrage     = Vecteur3D(        0,         0,         0),
            nom_sommet_source = 'S000'
        ),
        ConfigurationCable(
            point_ancrage     = Vecteur3D(ancrage_x,         0,         0),
            nom_sommet_source = 'S100'
        ),
        ConfigurationCable(
            point_ancrage     = Vecteur3D(        0, ancrage_y,         0),
            nom_sommet_source = 'S010'
        ),
        ConfigurationCable(
            point_ancrage     = Vecteur3D(ancrage_x, ancrage_y,         0),
            nom_sommet_source = 'S110'
        ),
        ConfigurationCable(
            point_ancrage     = Vecteur3D(        0,         0, ancrage_z),
            nom_sommet_source = 'S001'
        ),
        ConfigurationCable(
            point_ancrage     = Vecteur3D(ancrage_x,         0, ancrage_z),
            nom_sommet_source = 'S101'
        ),
        ConfigurationCable(
            point_ancrage     = Vecteur3D(        0, ancrage_y, ancrage_z),
            nom_sommet_source = 'S011'
        ),
        ConfigurationCable(
            point_ancrage     = Vecteur3D(ancrage_x, ancrage_y, ancrage_z),
            nom_sommet_source = 'S111'
        )
    ]
)

space_recherche = SpaceRechercheAnglesLimites(
      intervalle_rho   = IntervalleLineaire(min= 1000, max= 3501, pas=  250),
      intervalle_phi   = IntervalleLineaire(min=    0, max=   90, pas=    3),
      intervalle_theta = IntervalleLineaire(min=    0, max=  180, pas=    3)
)

systeme_spherique_baie_vitree = SystemeRepereSpherique(
    centre = Vecteur3D(
                  x = 3500,
                  y = 5000/2,
                  z = 2900/2
    ),
    ypr_angles = TupleAnglesRotation(
                  yaw   = 180,
                  pitch = 0,
                  row   = 0,
                  unite = UniteAngleEnum.DEGRE,
    )
)

limites = trouver_angles_limites(
      space_recherche,
      maisonette,
      dimensions_source,
      chambre,
      config_ancrage,
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
