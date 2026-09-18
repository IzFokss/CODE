def recherche (liste,nombre):
    occurence = 0
    for i in liste:
        if i == nombre :
            occurence += 1
    if occurence == 0:
        return None
    return (f"Il y a {occurence} fois la valeur {nombre} dans la liste {liste}")


print(recherche([5, 3],1))
print(recherche([2,4],2))
print(recherche([2,3,5,2,4],2))