from src.calculs.modeles.enums import UniteAngleEnum

from src.calculs.modeles.entites_mathemathiques import \
    SpaceRechercheAnglesLimites,                       \
    IntervalleLineaire

from .setups import faux

''' ************************ Configs Simulation ************************ '''

# space de recherche
space_recherche = \
    SpaceRechercheAnglesLimites(
        intervalle_rho   = IntervalleLineaire(min= 1000, max= 1501, pas=  250),  # mm
        intervalle_phi   = IntervalleLineaire(min=    0, max=  180, pas=    6),  # degres
        intervalle_theta = IntervalleLineaire(min=    0, max=  180, pas=    6),  # degres
        unite = UniteAngleEnum.DEGRE
)

# diametre des câbles
diametre_cable = 10  # mm

# discretisation des câbles
n_discretisation_cables = 20  # point/câble

# discretisation des cubes
k_dicretisation_cubes = 3  # division/arête --> nb points/face = (k+1)^2

# verbose
verbose = True

# dictionnaire de configs
configs_simulation = {
    'space_recherche'         : space_recherche,
    'diametre_cable'          : diametre_cable,
    'n_discretisation_cables' : n_discretisation_cables,
    'k_dicretisation_cubes'   : k_dicretisation_cubes,
    'verbose'                 : verbose
}

''' ************************ Selection ************************ '''

selection = {
    'faux' : True
}

''' ************************ faux ************************ '''

if selection['faux']:
    faux.verificateur.trouver_angles_limites(
        sauvegarde_automatique = True,
        nom_fichier_sauvegarde = './resultats_limites/faux'
    )

    faux.verificateur.sauvegarder_graphe_limites_png(nom_fichier='./graphes/faux')
    faux.verificateur.afficher_graphe_limites()
