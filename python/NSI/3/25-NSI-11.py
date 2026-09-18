def somme_max(tab):
    n = len(tab)
    sommes_max = [0]*n
    sommes_max[0] = tab[0]
    # on calcule la plus grande somme se terminant en i
    for i in range(1,n):
        if sommes_max[i-1] + tab[i] > tab[i]: 
            sommes_max[i] = sommes_max[i-1] + tab[i]
        else:
            sommes_max[i] = tab[i]
    # on en déduit la plus grande somme de celles-ci
    maximum = 0
    for i in range(1, n):
        if sommes_max[i] > sommes_max[maximum]: 
            maximum = i
    return sommes_max[maximum]



# Test 1 : tous les nombres sont positifs
assert somme_max([1, 2, 3, 4, 5]) == 15

# Test 2 : avec des nombres négatifs
assert somme_max([1, 2, -3, 4, 5]) == 9

# Test 3 : exemple de l'énoncé
assert somme_max([1, -2, 3, 10, -4, 7, 2, -5]) == 18

# Test 4 : tous les nombres sont négatifs
assert somme_max([-5, -2, -8]) == -2

# Test 5 : un seul élément
assert somme_max([7]) == 7

# Test 6 : le maximum est au début
assert somme_max([10, -5, -6, -2]) == 10

# Test 7 : le maximum est à la fin
assert somme_max([-5, -2, 1, 10]) == 11

print("Tous les tests sont réussis !")