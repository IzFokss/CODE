def parcours_largeur(arbre):
    resultat = []
    file = [arbre]

    while file:
        noeud = file.pop(0)

        if noeud is not None:
            gauche, etiquette, droite = noeud
            resultat.append(etiquette)

            file.append(gauche)
            file.append(droite)

    return resultat
    