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