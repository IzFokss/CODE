def recherche(tab,n):
    for i in range(len(tab)):
        if tab[i] == n :
            return i
    return None

print(recherche([2, 3, 4, 5, 6], 5))

print( recherche([2, 3, 4, 6, 7], 5) )