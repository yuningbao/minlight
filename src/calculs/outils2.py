from numpy import cos, sin, pi, matrix, sqrt
from numpy.linalg import pinv
import numpy as np
from pprint import pprint

from entites import *

import shapely.geometry as geom


def ypr_angles(yaw, pitch, row):
    return {'yaw': yaw, 'pitch': pitch, 'row': row}


def get_ypr_angles(angles):
    return angles['yaw'], angles['pitch'], angles['row']


def get_rpy_angles(angles):
    return angles['row'], angles['pitch'], angles['yaw']


def dimensions_pave(longueur, largeur, hauteur):
    return {'longueur': longueur, 'largeur': largeur, 'hauteur': hauteur}


def get_dimensions_pave(dimensions):
    return dimensions['longueur'], dimensions['largeur'], dimensions['hauteur']


def matrice_rotation_xyz_pour_inverser_zyx(ypr_angles):
    yaw, pitch, row = ypr_angles.get_angles()

    angles_opposes = TupleAnglesRotation(
        row=-row, pitch=-pitch, yaw=-yaw,
        sequence=SequenceAnglesRotationEnum.RPY
    )

    return angles_opposes.get_matrice_rotation()


# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!
ordre_sommets = ['S000', 'S100', 'S010', 'S110', 'S001', 'S101', 'S011', 'S111']


def dictionnaire_sommets(sommets_ordones):
    return {nom: sommet for nom, sommet in zip(ordre_sommets, sommets_ordones)}


def sommets_ordonnes(dictionnaire_sommets):
    return [dictionnaire_sommets[nom] for nom in ordre_sommets]


def sommets_pave_origine(dimensions):
    # dimensions
    long, larg, haut = get_dimensions_pave(dimensions)

    # sommets (coins) du pavé centré dans l'origine
    S000 = Vecteur3D(- long / 2, - larg / 2, - haut / 2)
    S100 = Vecteur3D(+ long / 2, - larg / 2, - haut / 2)
    S010 = Vecteur3D(- long / 2, + larg / 2, - haut / 2)
    S110 = Vecteur3D(+ long / 2, + larg / 2, - haut / 2)
    S001 = Vecteur3D(- long / 2, - larg / 2, + haut / 2)
    S101 = Vecteur3D(+ long / 2, - larg / 2, + haut / 2)
    S011 = Vecteur3D(- long / 2, + larg / 2, + haut / 2)
    S111 = Vecteur3D(+ long / 2, + larg / 2, + haut / 2)

    # sommets (coins) de la source repérés par rapport à son centre
    return [S000, S100, S010, S110, S001, S101, S011, S111]


def sommets_pave(centre, ypr_angles, dimensions):
    '''
    convention utilisé pour les rotations : z-y’-x″ (intrinsic rotations) = Yaw, pitch, and roll rotations
    http://planning.cs.uiuc.edu/node102.html
    http://planning.cs.uiuc.edu/node104.html
    https://en.wikipedia.org/wiki/Euler_angles#Tait.E2.80.93Bryan_angles
    https://en.wikipedia.org/wiki/Euler_angles#Rotation_matrix

    *** ancien 'anglesToPos' ***

    On suppose qu'on veut orienter le centre de la source par des angles 
    et la position du centre, on calcule les positios des sommets (les coins de la source).
    :param centreSoleil: centre de la source dans le système de repère de la chambre
    :param theta: remplir...
    :param phi: remplir...
    :param dimensionsSource: (dictionnaire) longueur, largeur, hauteur du pave de la source
    :return: liste des sommets de la source par rapport au système de repère de la chambre
    '''

    # Sommets
    # sommets (coins) de la source repérés par rapport à son centre
    S_origine = sommets_pave_origine(dimensions)

    # matrice de rotation
    Rot = ypr_angles.get_matrice_rotatio()
    # Rot = matrice_rotation_z1_y2_x3(ypr_angles)

    # rotation
    S_origine_rot = [Rot * s for s in S_origine]

    # translation
    S = [s + centre for s in S_origine_rot]

    return S


def sommets_pave_nomes(centre, ypr_angles, dimensions):
    S = sommets_pave(centre, ypr_angles, dimensions)
    dic = dictionnaire_sommets(S)
    return dic


def point_appartient_pave_origine(point, dimensions):
    '''
    Fonction qui teste si un point est dans le volume d'un pavé localisé à l'origine.
    :param dimensions: (dictionnaire) longueur, largeur, hauteur du pave de la source
    :return: False/True
    '''
    long, larg, haut = get_dimensions_pave(dimensions)

    demi_long, demi_larg, demi_haut = long / 2, larg / 2, haut / 2

    x, y, z = point.get_coordonnes()

    return -demi_long <= x <= demi_long and \
           -demi_larg <= y <= demi_larg and \
           -demi_haut <= z <= demi_haut


def point_appartient_pave(point, centre, ypr_angles, dimensions):
    '''
    Fonction qui teste si un point est dans le volume d'un pavé localisé à l'origine.
    :param dimensions: (dictionnaire) longueur, largeur, hauteur du pave de la source
    :param centre: centre du pavé repéré dans le sys de coordonnées globale
    :return: False/True
    '''
    point_repere_translate = point - centre

    rot = matrice_rotation_xyz_pour_inverser_zyx(ypr_angles)

    point_repere_pave = rot * point_repere_translate

    return point_appartient_pave_origine(point_repere_pave, dimensions)


def point_appartient_pave_droit(point, centre, dimensions):
    '''
    Fonction qui teste si un point est dans le volume d'un pavé dont le point Mini est donné.
    :param dimensions: (dictionnaire) longueur, largeur, hauteur du pave de la source
    :param centre: centre du pavé repéré dans le sys de coordonnées globale
    :return: False/True
    '''
    return point_appartient_pave_origine(point - centre, dimensions)


def creer_vecteurs_cables(configs_ancrage, sommets_source):
    return {nom: Vecteur3D(
        vecteur_depart=configs_ancrage[nom],
        vecteur_arrivee=sommets_source[nom]
    )
        for nom in ordre_sommets}


def longueurs_utiles_cables(les_vecteurs_cable):
    return [vc.norme() for vc in les_vecteurs_cable]


def generator_points_discretisation_cable(point_ancrage, vecteur_cable, N):
    return (point_ancrage + (i / N) * vecteur_cable
            for i in range(1, N))


# pas encore utilisé
def tester_interdictions_points(generator_points, tests_interdictions):
    resultats = {t['nom']: t['message_ok'] for t in tests_interdictions}
    for p in generator_points:
        for t in tests_interdictions:
            fonction = t['fonction']
            args = t['args']
            if fonction.__call__(p, **args):
                resultats[t['nom']] = t['message_probleme']
    return resultats


def verifier_cables(cables, maisonette, source, chambre, N_discretisation=300):
    centre_maisonette, dimensions_maisonette = maisonette['centre'], maisonette['dimensions']

    centre_source, ypr_angles_source, dimensions_source = source['centre'], source['ypr_angles'], source['dimensions']

    dimensions_chambre = chambre['dimensions']

    generators_points = {}
    for cable in cables:
        nom, point_ancrage, vecteur = cable['nom'], cable['point_ancrage'], cable['vecteur']

        generators_points[nom] = generator_points_discretisation_cable(point_ancrage, vecteur, N_discretisation)

    bilan = {}
    for nom, gen in generators_points.items():
        message = \
            {
                'maisonette': 'ok',
                'source': 'ok',
                'chambre': 'ok',
                'croisement': '?'
            }

        for point in gen:
            # maisonette
            if point_appartient_pave_droit(point, centre_maisonette, dimensions_maisonette):
                message['maisonette'] = '!'

            # source
            if point_appartient_pave(point, centre_source, ypr_angles_source, dimensions_source):
                message['source'] = '!'

            # chambre
            if not point_appartient_pave_droit(point, Vecteur3D(0, 0, 0), dimensions_chambre):
                message['chambre'] = '!'

                # ajouter les croisements

        bilan[nom] = message

    return bilan


def creer_cables(configs_ancrage, sommets_source):
    vecteurs_cables = creer_vecteurs_cables(configs_ancrage, sommets_source)

    cables = [{
        'nom': nom,
        'point_ancrage': configs_ancrage[nom],
        'vecteur': vecteurs_cables[nom]
    }
        for nom in ordre_sommets]

    return cables


def verifier_position(maisonette, source, chambre, configs_ancrage, print_results=False):
    sommets_source = sommets_pave_nomes(centre=source['centre'],
                                        ypr_angles=source['ypr_angles'],
                                        dimensions=source['dimensions'])

    cables = creer_cables(configs_ancrage, sommets_source)

    bilan_cables = verifier_cables(cables, maisonette, source, chambre)

    # verifier si source touche murs
    # verifier si source touche maisonette
    # verifier si source touche evap

    if print_results:
        print('Bilan des résultats des cãbles')
        pprint(bilan_cables)

    return any(str == '!' for str in list(bilan_cables.values()))


def coordonnees_spheriques(roh, theta, phi):
    return {'roh': roh, 'theta': theta, 'phi': phi}


def get_coordonnees_spheriques(coordonnees_spheriques):
    return coordonnees_spheriques['roh'], coordonnees_spheriques['theta'], coordonnees_spheriques['phi']


def systeme_spherique(centre, ypr_angles):
    return {'centre': centre, 'ypr_angles': ypr_angles}


def get_systeme_spherique(systeme_spherique):
    return systeme_spherique['centre'], systeme_spherique['ypr_angles']


def source_spherique_to_source_cartesian_global(coordonnees_spheriques, systeme_spherique):
    roh, theta, phi = get_coordonnees_spheriques(coordonnees_spheriques)

    # p = centre de la source pour le systeme cartesien à partir du quel le spherique est defini
    p = Vecteur3D(roh * cos(phi) * cos(theta),
                  roh * cos(phi) * sin(theta),
                  roh * sin(phi))

    centre_systeme, ypr_angles = get_systeme_spherique(systeme_spherique)

    rot = matrice_rotation_xyz_pour_inverser_zyx(ypr_angles)

    centre_source = rot * p + centre_systeme

    ypr_angles_source = \
        TupleAnglesRotation(
            row=0, pitch=phi, yaw=theta,
            sequence=SequenceAnglesRotationEnum.YPR,
            unite=UniteAngleEnum.DEGRE  # !!!!!!!!!!!!!!!!!!!!!!!!1
        )

    source = {'centre': centre_source, 'ypr_angles': ypr_angles_source}

    return source


def intervalle_lineaire_pas(min, max, pas):
    return np.arange(start=min, stop=max, step=pas)


def intervalle_lineaire_nombre_pas(min, max, nombre_pas):
    return np.linspace(start=min, stop=max, num=nombre_pas)


def space_recherche(space_rho, space_phi, space_theta):
    return {'space_rho': space_rho, 'space_phi': space_phi, 'space_theta': space_theta}


def get_space_recherche(space_recherche):
    return space_recherche['space_rho'], space_recherche['space_phi'], space_recherche['space_theta']


def trouver_angles_limites(space_recherche, maisonette, dimensions_source, chambre, configs_ancrage,
                           systeme_spherique_baie_vitree):
    space_rho, space_phi, space_theta = get_space_recherche(space_recherche)

    resultats = {}
    for rho in space_rho:
        couples = []
        resultats[rho] = couples

        premier_phi_ok = False

        for phi in space_phi:

            theta_max = np.nan

            for theta in space_theta:

                source_spherique = coordonnees_spheriques(rho, theta, phi)

                source = source_spherique_to_source_cartesian_global(
                    coordonnees_spheriques=source_spherique,
                    systeme_spherique=systeme_spherique_baie_vitree
                )

                source['dimensions'] = dimensions_source

                if verifier_position(maisonette, source, chambre, configs_ancrage):
                    premier_phi_ok = True
                    pass

                else:
                    theta_max = theta
                    break

            couples.append((phi, theta_max))

            if not premier_phi_ok:
                break


'''
def maxTheta(r, phi, maisonette,source,chambre,configs_ancrag)
#r : distance entre centre de la face de la maisonette et le centre de la source, r des coordonnes spheriques
#phi : angle verticale , coordonnes spheriques
#centreRotation:
#maisonette
#source
#chambre


    wallCentre = creerPoint(LargCC/2,LongM,HautM/2) # milieu du mur d'interet

    sourceCentreReference = creerPoint(LargCC/2 + r,LongM,HautM/2) - wallCentre

    maxTheta = [][] #stores a max theta for each phi
    for i in range(90):
        for j in range(90):
            maxTheta[i][j] = 90

    for phiDegrees in range(90):
        for thetaDegrees in range(90):
                phi = math.radians(phiDegrees)
                theta = math.radians(thetaDegrees)
                rotationMatrixTheta = np.matrix([[1,0,0],[0,cos(theta),-sin(theta)],[0,sin(theta),cos(theta)]])
                rotationMatrixPhi = np.matrix([[cos(phi),-sin(phi),0],[sin(phi),cos(phi),0],[0,0,1]])
                sourceRotated = rotationMatrixTheta*rotationMatrixPhi*sourceCentreReference
                directionNormale = sourceRotated - wallCentres
                directionNormale = directionNormale/norme_vecteur(directionNormale)
                roll = arctan(directionNormale[1]/directionNormale[0])
                pitch = arctan(sqrt(directionNormale[0]**2  + directionNormale[1]**2 )/directionNormale[2])
                if(verifySource(sourceCentre,roll,pitch))#a faire
                    continue
                maxTheta[phiDegrees] = thetaDegrees
                break

'''



