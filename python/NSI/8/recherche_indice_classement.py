def recherche_indices_classement(elt, tab):
    inferieur = []
    egal = []
    superieur = []

    for i in range(len(tab)):
        if tab[i] < elt:
            inferieur.append(i)
        elif tab[i] == elt:
            egal.append(i)
        else:
            superieur.append(i)

    return inferieur, egal, superieur


print(recherche_indices_classement(3, [1, 3, 4, 2, 4, 6, 3, 0]))
print(recherche_indices_classement(3, [1, 4, 2, 6, 0]))
print(recherche_indices_classement(3, [1, 1, 1, 1]))
print(recherche_indices_classement(3, []))