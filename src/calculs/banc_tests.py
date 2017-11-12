from simulation import *

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
      # Cest le centre !!!!!!!!!!!!!!!!!!11
      centre = Vecteur3D(8500/2,5000/2,4000/2),
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
      intervalle_theta = IntervalleLineaire(min=    0, max=  180, pas=    3),
      unite = UniteAngleEnum.DEGRE
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

diametre_cable = 10

limites = trouver_angles_limites(
      space_recherche,
      maisonette,
      dimensions_source,
      chambre,
      config_ancrage,
      systeme_spherique_baie_vitree,
      diametre_cable
)

pprint(limites)
