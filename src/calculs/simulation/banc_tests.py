from setups import faux


''' ************************ Selection ************************ '''

selection = {
    'faux' : True
}

''' ************************ faux ************************ '''

if selection['faux']:
    faux.verificateur.trouver_angles_limites(
        sauvegarde_automatique = True,
        nom_fichier_sauvegarde = 'faux'
    )

    faux.verificateur.sauvegarder_graphe_limites_png(nom_fichier='faux')
    faux.verificateur.afficher_graphe_limites()
