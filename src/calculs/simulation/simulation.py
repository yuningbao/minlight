from entites_mathemathiques import *
from entites_systeme_minlight import *
import pickle
from datetime import datetime
import matplotlib.pyplot as plt


class VerificateurAnglesLimites():

    def __init__(self,
                 dimensions_source,
                 maisonette,
                 chambre,
                 config_ancrage,
                 systeme_spherique_baie_vitree,
                 configs_simulation):

        self.dimensions_source = dimensions_source
        self.maisonette        = maisonette
        self.chambre           = chambre

        self.config_ancrage  = config_ancrage

        self.systeme_spherique_baie_vitree = systeme_spherique_baie_vitree

        self.diametre_cable  = configs_simulation['diametre_cable']
        self.space_recherche = configs_simulation['space_recherche']

        self.n_discretisations_cables = configs_simulation['n_discretisations_cables']
        self.k_dicretisation_cubes    = configs_simulation['k_dicretisation_cubes']

        self.verbose                  = configs_simulation['verbose']

        self.source = Pave(
            centre     = Vecteur3D(0,0,0),
            ypr_angles = TupleAnglesRotation(0,0,0),
            dimensions = dimensions_source
        )

        self.limites = {}

    def trouver_angles_limites(self, sauvegarde_automatique=True, nom_fichier_sauvegarde='auto'):

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

        if sauvegarde_automatique:
            self.sauvegarder_limites(nom_fichier_sauvegarde)

    def position_ok(self):
        sommets_source = self.source.get_dictionnaire_sommets()

        cables = self.config_ancrage.get_cables(sommets_source, diametre_cable=self.diametre_cable)

        if not self.cables_ok(cables):
            return False

        if self.source.intersection_avec_pave(self.maisonette,
                                              nombre_points_discretisation = self.k_dicretisation_cubes):
            return False

        if not self.source.entierement_dans_pave(self.chambre,
                                                 nombre_points_discretisation = self.k_dicretisation_cubes):
            return False

        return True

    def cables_ok(self, cables):

        for cable in cables:

            # maisonette
            if cable.intersection_avec_pave(self.maisonette, self.n_discretisation_cables):
                return False

            # source
            if cable.intersection_avec_pave(self.source, self.n_discretisation_cables):
                return False

            # chambre
            if not cable.entierement_dans_pave(self.chambre, self.n_discretisation_cables):
                return False

            # croisements
            for autre_cable in cables:
                if autre_cable == cable:
                    pass
                else:
                    if cable.intersects_cable(autre_cable):
                        return False

        return True

    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!! creer une verification auto pour noms des fichier pour ne pas écrire dessus
    def sauvegarder_limites(self, nom_fichier='auto'):
        if nom_fichier == 'auto':
            format = '_%y_%m_%d_%H_%M_%S'
            nom_fichier = 'angles_limites' + datetime.now().strftime(format)

        pickle_out = open(nom_fichier + '.pickle', "wb")
        pickle.dump(self.limites, pickle_out)
        pickle_out.close()

    def charger_fichier_limites(self, nom_fichier):
        pickle_in = open(nom_fichier + '.pickle', "rb")
        self.limites = pickle.load(pickle_in)
        pickle_in.close()

    def _generer_graphe(self, xlim=[0, 90], ylim=[0, 90] ):
        fig = plt.figure()
        ax = fig.gca()

        for rho, couples in self.limites.items():
            phi, theta = zip(*couples)

            line, = ax.plot(phi, theta)

            line.set_label('Rho = ' + "{r:0.2f}".format(r=rho/1000) + ' m')

        ax.set_title('Angles Limites')
        ax.set_xlabel('Theta [º]')
        ax.set_ylabel('Phi [º]')

        ax.set_xlim(xlim)
        ax.set_ylim(ylim)

        ax.legend()

    def afficher_graphe_limites(self, xlim=[0, 90], ylim=[0, 90]):
        self._generer_graphe(xlim, ylim)
        plt.show()

    def sauvegarder_graphe_limites_png(self, xlim=[0, 90], ylim=[0, 90], nom_fichier='auto'):

        self._generer_graphe(xlim, ylim)

        if nom_fichier == 'auto':
            format = '_%y_%m_%d_%H_%M_%S'
            nom_fichier = 'angles_limites' + datetime.now().strftime(format)

        plt.savefig(nom_fichier + '.png', bbox_inches='tight')