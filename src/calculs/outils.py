from numpy import cos, sin, pi, matrix, sqrt
from numpy.linalg import pinv
import numpy as np
from pprint import pprint

import shapely.geometry as geom


def point_3d(x, y, z):
    '''
    Retourne une matrice colonne 3x1 (numpy.matrix).
    [x, y, z]^T
    :return: matrice (numpy.matrix) colonne 3x1
    '''
    return matrix([[x], [y], [z]])


def get_coordonnees_point_3d(point):
    '''
    Prend un point_3d et retourne une tuple (x,y,z).
    :param point: matrice (numpy.matrix) colonne 3x1
    '''
    return point.item(0), point.item(1), point.item(2)


def vecteur_3d(x, y, z):
    '''
    Retourne une matrice colonne 3x1 (numpy.matrix).
    [x, y, z]^T
    :return: matrice (numpy.matrix) colonne 3x1
    '''
    return matrix([[x], [y], [z]])


def get_coordonnees_vecteur_3d(vecteur):
    '''
    Prend un point_3d et retourne une tuple (x,y,z).
    :param point: matrice (numpy.matrix) colonne 3x1
    '''
    return vecteur.item(0), vecteur.item(1), vecteur.item(2)


def rpy_angles(row, pitch, yaw):
    return {'yaw' : yaw, 'pitch' : pitch, 'row' : row}


def get_ypr_angles(angles):
    return angles['yaw'], angles['pitch'], angles['row']


def get_rpy_angles(angles):
    return angles['row'], angles['pitch'], angles['yaw']


def dimensions_pave(longueur, largeur, hauteur):
    return {'longueur' : longueur, 'largeur' : largeur, 'hauteur' : hauteur}


def get_dimensions_pave(dimensions):
    return dimensions['longueur'], dimensions['largeur'], dimensions['hauteur']


def distance_2_points(A, B):
    '''
    Distance euclidiainne en 3D entre 2 points.
    :param A: matrice (numpy.matrix) colonne 3x1
    :param B: matrice (numpy.matrix) colonne 3x1
    '''
    ax, ay, az = get_coordonnees_point_3d(A)
    bx, by, bz = get_coordonnees_point_3d(B)

    ecart_x = ax - bx
    ecart_y = ay - by
    ecart_z = az - bz

    return sqrt(ecart_x ** 2 + ecart_y ** 2 + ecart_z ** 2);


def matrice_rotation_x(angle):
    s, c = sin(angle), cos(angle)
    return matrix([
        [1, 0,  0],
        [0, c, -s],
        [0, s,  c]
    ])


def matrice_rotation_y(angle):
    s, c = sin(angle), cos(angle)
    return matrix([
        [ c, 0, s],
        [ 0, 1, 0],
        [-s, 0, c]
    ])


def matrice_rotation_z(angle):
    s, c = sin(angle), cos(angle)
    return matrix([
        [c, -s, 0],
        [s,  c, 0],
        [0,  0, 1]
    ])


def matrice_rotation_z1_y2_x3(angles):
    yaw, pitch, row = get_ypr_angles(angles)
    return matrice_rotation_z(yaw) * matrice_rotation_y(pitch) * matrice_rotation_x(row)


def matrice_rotation_x1_y2_z3(angles):
    row, pitch, yaw = get_rpy_angles(angles)
    return matrice_rotation_x(row) * matrice_rotation_y(pitch) * matrice_rotation_z(yaw)


def generer_noms_sommets_pave():
    return ['S000', 'S100', 'S010', 'S110', 'S001', 'S101', 'S011', 'S111']


def generer_dictionnaire_sommets(sommets):
    return {nom : sommet for nom, sommet in zip(generer_noms_sommets_pave(), sommets)}


def get_points_ancrage_ordones(configs_ancrage):
    return [configs_ancrage[nom] for nom in generer_noms_sommets_pave()]


def sommets_pave_origine(dimensions):
    # dimensions
    long, larg, haut = get_dimensions_pave(dimensions)

    # sommets (coins) du pavé centré dans l'origine
    S000 = point_3d(+ long/2, - larg/2, - haut/2)
    S100 = point_3d(- long/2, - larg/2, - haut/2)
    S010 = point_3d(+ long/2, + larg/2, - haut/2)
    S110 = point_3d(- long/2, + larg/2, - haut/2)
    S001 = point_3d(+ long/2, - larg/2, + haut/2)
    S101 = point_3d(- long/2, - larg/2, + haut/2)
    S011 = point_3d(+ long/2, + larg/2, + haut/2)
    S111 = point_3d(- long/2, + larg/2, + haut/2)

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
    Rot = matrice_rotation_z1_y2_x3(ypr_angles)

    # rotation
    S_origine_rot = [Rot * s for s in S_origine]

    # translation
    S = [s + centre for s in S_origine_rot]

    return S


def point_appartient_pave_origine(point, dimensions):
    '''
    Fonction qui teste si un point est dans le volume d'un pavé localisé à l'origine.
    :param dimensions: (dictionnaire) longueur, largeur, hauteur du pave de la source
    :return: False/True
    '''
    long, larg, haut = get_dimensions_pave(dimensions)

    demi_long, demi_larg, demi_haut = long/2, larg/2, haut/2

    x, y, z = get_coordonnees_point_3d(point)

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

    yaw, pitch, row = get_ypr_angles(ypr_angles)

    angles_opposes = rpy_angles(row = -row, pitch = -pitch, yaw = -yaw)

    rot = matrice_rotation_x1_y2_z3(angles_opposes)

    point_repere_pave = rot * point_repere_translate

    return point_appartient_pave_origine(point_repere_pave, dimensions)


def point_appartient_pave_droit_S000(point, S000, dimensions):
    '''
    Fonction qui teste si un point est dans le volume d'un pavé dont le point Mini est donné.
    :param dimensions: (dictionnaire) longueur, largeur, hauteur du pave de la source
    :param pointMini: sommet le plus proche de l'origine dans le sys de coordonnées globale
    :return: False/True
    '''
    long, larg, haut = get_dimensions_pave(dimensions)

    x, y, z = get_coordonnees_point_3d(point - S000)

    return 0 <= x <= long and 0 <= y <= larg and 0 <= z <= haut


def vecteur_difference_2_points(depart, arrive):
    return arrive - depart


def norme_vecteur(vecteur):
    x, y, z = get_coordonnees_vecteur_3d(vecteur)
    return sqrt(x**2 + y**2 + z**2)


def direction_difference_2_points(depart, arrive):
    vec = vecteur_difference_2_points(depart, arrive)

    x, y, z = get_coordonnees_vecteur_3d(vec)

    norme = norme_vecteur(vec)

    xn, yn, zn = x/norme, y/norme, z/norme

    return vecteur_3d(xn, yn, zn)




def creer_vecteurs_cables(points_ancrage, sommets_source):

    return [vecteur_difference_2_points(pa, ss)
            for pa, ss
            in zip(points_ancrage, sommets_source)]


def longueurs_utiles_cables(les_vecteurs_cable):
    return [norme_vecteur(vc) for vc in les_vecteurs_cable]


def generator_points_discretisation_cable(point_ancrage, vecteur_cable, N):
    return (point_ancrage + (i/N)*vecteur_cable
            for i in range(1, N))


# pas encore utilisé
def tester_interdictions_points(generator_points, tests_interdictions):
    resultats = {t['nom'] : t['message_ok'] for t in tests_interdictions}
    for p in generator_points:
        for t in tests_interdictions:
            fonction = t['fonction']
            args     = t['args']
            if fonction.__call__(p, **args):
                resultats[t['nom']] = t['message_probleme']
    return resultats


def verifier_cables(cables, maisonette, source, chambre, N_discretisation = 300):
    S000_maisonette, dimensions_maisonette = maisonette['S000'], maisonette['dimensions']

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
                'maisonette' : 'ok',
                'source'     : 'ok',
                'chambre'    : 'ok',
                'croisement' : '?'
            }

        for point in gen:
            # maisonette
            if point_appartient_pave_droit_S000(point, S000_maisonette, dimensions_maisonette):
                message['maisonette'] = '!'

            # source
            if point_appartient_pave(point, centre_source, ypr_angles_source, dimensions_source):
                message['source'] = '!'

            #chambre
            if not point_appartient_pave_droit_S000(p, point_3d(0,0,0), dimensions_chambre):
                message['chambre'] = '!'

            # ajouter les croisements

        bilan[nom] = message

    return bilan


def verifier_position(maisonette, source, chambre, configs_ancrage, print_results=False):
    sommets_source = sommets_pave(centre     = source['centre'    ],
                                  ypr_angles = source['ypr_angles'],
                                  dimensions = source['dimensions'])

    points_ancrage = get_points_ancrage_ordones(configs_ancrage)

    vecteurs_cables = creer_vecteurs_cables(points_ancrage, sommets_source)

    cables = [{'nom' : nom, 'point_ancrage' : pa, 'vecteur' : vec}
              for nom, pa, vec
              in zip(generer_noms_sommets_pave(), points_ancrage, vecteurs_cables)]

    bilan_cables = verifier_cables(cables, maisonette, source, chambre)

    # verifier si source touche murs
    # verifier si source touche maisonette
    # verifier si source touche evap

    if print_results:
        print('Bilan des résultats des cãbles')
        pprint(bilan_cables)








### Calcul des tensions dans les câbles :

# Matrices pour le produit vectoriel ;
Ex = matrix([[0, 1, 0],
             [0, 0, 1]])

Ey = matrix([[1, 0, 0],
             [0, 0, 1]])

Ez = matrix([[1, 0, 0],
             [0, 1, 0]])

E  = matrix([[0, -1],
             [1, 0]])

Hx = ( Ex.T * E.T) * Ex
Hy = (-Ey.T * E.T) * Ey
Hz = ( Ez.T * E.T) * Ez

def matrice_torsion(source, configs_ancrage):

    # comment ça marche
    # point d'application des tensions ?
    # momments ?
    # centre de gravité

    sommets_source = sommets_pave(centre     = source['centre'    ],
                                  ypr_angles = source['ypr_angles'],
                                  dimensions = source['dimensions'])

    points_ancrage = get_points_ancrage_ordones(configs_ancrage)

    vecteurs_cables = creer_vecteurs_cables(points_ancrage, sommets_source)

    Mx = [ss.T * (Hx * vc) for vc, ss in zip(vecteurs_cables, sommets_source)]
    My = [ss.T * (Hy * vc) for vc, ss in zip(vecteurs_cables, sommets_source)]
    Mz = [ss.T * (Hz * vc) for vc, ss in zip(vecteurs_cables, sommets_source)]

    # à quoi ça sert ?
    Fx = [v[0][0] for v in zip(vecteurs_cables)]
    Fy = [v[0][1] for v in zip(vecteurs_cables)]
    Fz = [v[0][2] for v in zip(vecteurs_cables)]

    # ça devrait pas etre pour chaque cable ?
    W = matrix([Fx, Fy, Fz, Mx, My, Mz])

    return W


print(matrice_torsion(source, configs_ancrage))

masse = 50  # en kg

S = sommets_pave(source['centre'], source['ypr_angles'], source['dimensions'])

g = 9.81

fx = 0
fy = 0
fz = masse * g

Force = vecteur_3d(fx, fy, fz)
MomentPoids_P = vecteur_3d(0, 0, 0)  # ça suppose un bilan fait à partir du centre de masse

"""
Si d'autre actions extérieur il faudra mettre des moments qui s'appliquent en P
mx = [(MCentre.T * (Hx * F))]
my = [(MCentre.T * (Hy * F))]
mz = [(MCentre.T * (Hz * F))]
"""

forceExt = np.concatenate((Force, MomentPoids_P), axis=0)


def vecteurTension(centreSoleil, theta, phi, Pa):
    W = matrice_torsion(centreSoleil, theta, phi, Pa)
    T = - pinv(W) * forceExt
    # il y a une infinité de solutions utiliser la pseudo inverse permet d'avoir les tensions minimales
    return T





