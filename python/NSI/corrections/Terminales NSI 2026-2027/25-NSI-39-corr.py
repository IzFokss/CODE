def moyenne(tab):
    if tab == []:
        print('erreur')
        return None
    somme = 0
    for elt in tab:
        somme += elt
    return somme / len(tab)

assert moyenne([5, 3, 8]) == 5.333333333333333
assert moyenne([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]) == 5.5
print(moyenne([]))
# Comportement différent suivant le traitement proposé.

def tri(tab):
    #i est le premier indice de la zone non triee, j le dernier indice.
    #Au debut, la zone non triee est le tableau entier.
    i = 0
    j = len(tab) - 1
    while i != j :
        if tab[i]== 0:
            i = i + 1
        else :
            valeur = tab[j]
            tab[j] = tab[i]
            tab[i] = valeur
            j = j - 1
    return tab

assert tri([0, 1, 0, 1, 0, 1, 0, 1, 0])==[0, 0, 0, 0, 0, 1, 1, 1, 1]