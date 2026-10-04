def convertir(T):
    puissance = 0
    total = 0
    for i in range(len(T)-1, -1, -1):
        total += T[i]*(2**puissance)
        print(total)
        puissance += 1
    return total

# autre solution :
##def convertir(T):
##    n = len(T)
##    s  =  0
##    for i in range(n):
##        s = s + T[i]*2**(n-1-i)
##    return s

assert convertir([1, 0, 1, 0, 0, 1, 1]) == 83
assert convertir([1, 0, 0, 0, 0, 0, 1, 0]) == 130

## Exercice 2

liste = [9, 5, 8, 4, 0, 2, 7, 1, 10, 3, 6]

def tri_insertion(tab):
    n = len(tab)
    for i in range(1, n):
        valeur_insertion = tab[i]
        # la variable j sert à déterminer où placer la valeur à ranger
        j = i
        # tant qu'on a pas trouvé la place de l'élément à insérer
        # on décale les valeurs du tableau vers la droite
        while j > 0 and valeur_insertion < tab[j-1]:
            tab[j] = tab[j-1]
            j = j-1
        tab[j] = valeur_insertion

liste = [9, 5, 8, 4, 0, 2, 7, 1, 10, 3, 6]
tri_insertion(liste)
assert liste == [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]