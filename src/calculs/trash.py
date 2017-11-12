def matrice_rotation(angle, vecteur):
    direction = vecteur / norme_vecteur(vecteur)
    x, y, z = get_coordonnees_vecteur_3d(direction)
    c = cos(angle)
    s = sin(angle)

    r11 = x ** 2 + (1 - x ** 2) * c
    r12 = x * y * (1 - c) - z * s
    r13 = x * z * (1 - c) + y * s

    r21 = x * y * (1 - c) + z * s
    r22 = y ** 2 + (1 - y ** 2) * c
    r23 = y * z * (1 - c) - x * s

    r31 = x * z * (1 - c) - y * s
    r32 = y * z * (1 - c) + x * s
    r33 = z ** 2 + (1 - z ** 2) * c

    return matrix([[r11, r12, r13],
                   [r21, r22, r23],
                   [r31, r32, r33]])


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





class Vecteur(numpy.matrix):
    def __new__(cls, x, y, z):
        # note that we have to send cls to super's __new__, even though we gave it to super already.
        # I think this is because __new__ is technically a staticmethod even though it should be a classmethod
        return super(Vecteur, cls).__new__(cls, "{}; {}; {}".format(x, y, z))




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






sommets = [Vecteur3D(sommet[0], sommet[1], sommet[2]) for sommet in product((1,-1), repeat=3)]

# !!!!!!!!!!!!!!! faire gaffe avec les arrondissement
def points_dans_meme_plane(p1, p2, p3, p4):
    vec1 = p2 - p1
    vec2 = p3 - p1

    # coordonnees du vec resultant du prod vect
    u, v, w = tuple(cross(vec1.T, vec2.T)[0].tolist())

    normal = Vecteur3D(u,v,w)

    k1 = normal.T.dot(p1)
    k4 = normal.T.dot(p4)
    diff = (k1 - k4)[0][0]
    return diff == 0

faces = []

for quartette in combinations(sommets, 4):
    if points_dans_meme_plane(quartette[0], quartette[1], quartette[2], quartette[3]):
        faces.append(quartette)