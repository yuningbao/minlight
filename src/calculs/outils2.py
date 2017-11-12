from numpy import cos, sin, pi, matrix, sqrt
from numpy.linalg import pinv
import numpy as np
from pprint import pprint

from entites_mathemathiques import *

import shapely.geometry as geom

class VerificateurAnglesLimites():

    def __init__(self, dimensions_source, maisonette, chambre, config_ancrage, systeme_spherique_baie_vitree, configs_simulation):
        self.dimensions_source = dimensions_source
        self.maisonette        = maisonette
        self.chambre           = chambre

        self.config_ancrage  = config_ancrage

        self.systeme_spherique_baie_vitree = systeme_spherique_baie_vitree

        self.diametre_cable  = configs_simulation['diametre_cable']
        self.space_recherche = configs_simulation['space_recherche']

        self.n_discretisations_cables = configs_simulation['N_discretisations_cables']
        self.n_dicretisation_cubes    = configs_simulation['K_dicretisation_cubes']

        self.verbose                  = configs_simulation['verbose']

        self.source = Pave(
            centre     = Vecteur3D(0,0,0),
            ypr_angles = TupleAnglesRotation(0,0,0),
            dimensions = dimensions_source
        )

        self.limites = {}


    def trouver_angles_limites(self):

        intervalle_rho, intervalle_phi, intervalle_theta = self.space_recherche.get_intervalles()

        unite_angles = self.space_recherche.unite

        for rho in intervalle_rho:

            if self.verbose:
                print('rho =', rho)

            couples_angles = []

            self.limites[rho] = couples_angles

            for phi in intervalle_phi:

                premier_theta_ok = False

                for theta in intervalle_theta:

                    theta_max = theta

                    self.source.changer_a_partir_de_coordonnes_spheriques(
                        coordonnees_spheriques = CoordonnesSpherique(rho, theta, phi, unite=unite_angles),
                        systeme_spherique      = self.systeme_spherique_baie_vitree
                    )

                    if self.position_ok():
                        premier_theta_ok = True
                    else:
                        break

                couples_angles.append((phi, theta_max))

                if self.verbose:
                    print((phi, theta_max))

                if not premier_theta_ok:
                    break

            if self.verbose:
                print()

        return self.limites

    def position_ok(self):
        sommets_source = self.source.get_dictionnaire_sommets()

        cables = self.config_ancrage.get_cables(sommets_source, diametre_cable=self.diametre_cable)

        cables_ok = self.cables_ok(cables)

        # verifier si source touche murs
        # verifier si source touche maisonette

        return cables_ok


    def cables_ok(self, cables):

        for cable in cables:

            # maisonette
            if cable.intersection_avec_pave(self.maisonette, self.n_discretisation_cables):
                bilan[cable.nom_sommet_source]['maisonette'] = '!'

                if bilan_incomplet:
                    break

            # source
            if cable.intersection_avec_pave(source, n_discretisation_cables):
                bilan[cable.nom_sommet_source]['source'] = '!'

                if bilan_incomplet:
                    break

            # chambre
            if not cable.entierement_dans_pave(chambre):
                bilan[cable.nom_sommet_source]['chambre'] = '!'

                if bilan_incomplet:
                    break

            # croisements
            for autre_cable in cables:
                if autre_cable == cable:
                    pass
                else:
                    if cable.intersects_cable(autre_cable):
                        bilan[cable.nom_sommet_source]['croisement'] = '!'

                        if bilan_incomplet:
                            break

        return bilan


def verifier_cables(cables, maisonette, source, chambre, n_discretisation_cables, bilan_incomplet=False):

    bilan = {}
    message_standard = \
        {
            'maisonette' : 'ok',
            'source'     : 'ok',
            'chambre'    : 'ok',
            'croisement' : 'ok'
        }

    for cable in cables:
        bilan[cable.nom_sommet_source] = message_standard

    for cable in cables:

        # maisonette
        if cable.intersection_avec_pave(maisonette, n_discretisation_cables):
            bilan[cable.nom_sommet_source]['maisonette'] = '!'

            if bilan_incomplet:
                break

        # source
        if cable.intersection_avec_pave(source, n_discretisation_cables):
            bilan[cable.nom_sommet_source]['source'] = '!'

            if bilan_incomplet:
                break

        # chambre
        if not cable.entierement_dans_pave(chambre):
            bilan[cable.nom_sommet_source]['chambre'] = '!'

            if bilan_incomplet:
                break

        # croisements
        for autre_cable in cables:
            if autre_cable == cable:
                pass
            else:
                if cable.intersects_cable(autre_cable):
                    bilan[cable.nom_sommet_source]['croisement'] = '!'

                    if bilan_incomplet:
                        break

    return bilan


def bilan_cables_tout_ok(bilan_cables):
    resumes_cables = list(bilan_cables.values())
    return all(message == 'ok' for resume in resumes_cables for message in list(resume.values()))






def solutions_formule_quadratique(a, b, c):
    return ((-b - sqrt(b*b - 4*a*c))/(2*a),(-b + sqrt(b*b - 4*a*c))/(2*a))

