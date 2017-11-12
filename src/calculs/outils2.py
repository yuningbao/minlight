from numpy import cos, sin, pi, matrix, sqrt
from numpy.linalg import pinv
import numpy as np
from pprint import pprint

from entites import *

import shapely.geometry as geom

def verifier_cables(cables, maisonette, source, chambre, N_discretisation=300, bilan_incomplet_si_touche=False):

    generators_points = {}

    bilan = {}
    for cable in cables:
        message = \
            {
                'maisonette': 'ok',
                'source': 'ok',
                'chambre': 'ok',
                'croisement': '?'
            }

        for point in cable.get_generator_points_discretisation(N_discretisation):
            # maisonette
            if maisonette.point_appartient_pave(point):
                message['maisonette'] = '!'
                if bilan_incomplet_si_touche:
                    break

            # source
            if source.point_appartient_pave(point):
                message['source'] = '!'
                if bilan_incomplet_si_touche:
                    break

            # chambre
            if not chambre.point_appartient_pave(point):
                message['chambre'] = '!'
                if bilan_incomplet_si_touche:
                    break

            # ajouter les croisements

        bilan[cable.nom_sommet_source] = message
        any_touch = any(str == '!' for str in list(message.values()))

        if bilan_incomplet_si_touche and any_touch:
            break

    return bilan


def verifier_position(maisonette, source, chambre, config_ancrage, diametre_cable, N_discretisations_cables, print_results=False):
    sommets_source = source.get_dictionnaire_sommets()

    cables = config_ancrage.get_cables(sommets_source, diametre_cable=diametre_cable)

    bilan_cables = verifier_cables(cables, maisonette, source, chambre,
                                   N_discretisations_cables, bilan_incomplet_si_touche=True)

    # verifier si source touche murs
    # verifier si source touche maisonette
    # verifier si source touche evap

    if print_results:
        print('Bilan des résultats des cãbles')
        pprint(bilan_cables)

    any_touch = any(str == '!' for resume_cable in list(bilan_cables.values()) for str in list(resume_cable.values()))

    return not any_touch


def trouver_angles_limites(dimensions_source, maisonette, chambre, systeme_spherique_baie_vitree, configs_simulation):
    diametre_cable = configs_simulation['diametre_cable']

    N_discretisations_cables = configs_simulation['N_discretisations_cables']

    K_dicretisation_cubes = configs_simulation['K_dicretisation_cubes']

    space_recherche = configs_simulation['space_recherche']

    config_ancrage = configs_simulation['config_ancrage']

    verbose = configs_simulation['verbose']

    intervalle_rho, intervalle_phi, intervalle_theta = space_recherche.get_intervalles()

    unite_angles = space_recherche.unite

    source = Pave(
        centre     = Vecteur3D(0,0,0),
        ypr_angles = TupleAnglesRotation(0,0,0),
        dimensions = dimensions_source
    )

    limites = {}

    for rho in intervalle_rho:

        if verbose:
            print('rho =', rho)

        couples_angles = []

        limites[rho] = couples_angles

        for phi in intervalle_phi:

            premier_theta_ok = False

            for theta in intervalle_theta:

                theta_max = theta

                changer_source_a_partir_des_coordonnes_spheriques(
                    source                 = source,
                    coordonnees_spheriques = CoordonnesSpherique(rho, theta, phi, unite=unite_angles),
                    systeme_spherique      = systeme_spherique_baie_vitree
                )

                if verifier_position(maisonette, source, chambre, config_ancrage, diametre_cable, N_discretisations_cables=N_discretisations_cables):
                    premier_theta_ok = True
                else:
                    break

            couples_angles.append((phi, theta_max))

            print(couple)

            if not premier_theta_ok:
                break
        print()

    return limites


def solutions_formule_quadratique(a, b, c):
    return ((-b - sqrt(b*b - 4*a*c))/(2*a),(-b + sqrt(b*b - 4*a*c))/(2*a))

