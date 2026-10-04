'''Implémentation du type abstrait Liste en utilisant des tableaux statiques '''
def nouvelleListe():
    '''Renvoie une liste vide
    :: return (Liste) :: renvoie une liste vide sous forme d'un tableau vide ()
    '''
    return []

def estVide(lst):
    '''Renvoie True si la liste est vide
    :: param lst(Liste) :: une liste à tester
    :: return (bool) :: True si la liste est vide ()
    '''
    if lst == []:
        return True
    return False

def insererTete(x, lst):
    '''Renvoie une nouvelle liste où x est la tête et liste la queue
    :: param x(Elt) :: un élément compatible avec votre liste qui devient la tête
    :: param lst(Liste) :: la liste qui va devenir la queue de la nouvelle
    :: return (Liste) :: la nouvelle liste
    '''
    list2 = [0 for x in range(len(lst) + 1)]    # On crée une liste plus longue de 1
    for index in range(len(lst)):
        list2[index + 1] = lst[index]           # Décalage vers la droite
    list2[0] = x                                # On place la tête
    return list2                                # On renvoie la nouvelle liste

def lireTete(lst):
    '''Renvoie la tête de la liste, sans toucher à la liste elle-même
    :: param lst(Liste) :: la liste dont on désire lire la tête
    :: return (Elt) :: la tête voulue, None si la tête est vide
    '''
    if not estVide(lst):
        return lst[0] # la valeur envoyée est la première valeur de la liste

def supprimerTete(lst):
    '''Renvoie une nouvelle liste où on a supprimé la tête de l'ancienne
    :: param lst(Liste) :: la liste dont on supprime la tête
    :: return (Liste) :: la nouvelle liste
    '''
    if estVide(lst):
        return nouvelleListe() # la liste envoyée est ()
    else:
      list2 = [0 for x in range(len(lst) - 1)]    # On crée une liste moins longue de 1
      for index in range(1, len(lst)):
          list2[index - 1] = lst[index]           # Décalage vers la gauche
      return list2                                # On renvoie la nouvelle liste


liste1 = []
liste2 = None
liste3 = "c"

print("La liste 1 contient : ",liste1)
print("La liste 1 est vide : ",estVide(liste1))
print("La liste 2 contient : ",liste2)
print("La liste 2 est vide : ",estVide(liste2))
print("La liste 3 contient : ",liste3)
print("La liste 3 est vide : ",estVide(liste3))
print()
print("ATTENTION")
print("Seule la liste 4 respecte l'interface TAD : ")
print("Les listes 1 à 3 sont crées sans passer par la fonction d'interface nouvelleListe.")
print()

print("Nouvelle liste")
liste4 = nouvelleListe()
print("La liste 4 contient : ",liste4)
print("La liste 4 est vide : ",estVide(liste4))
print("La tête de la liste est : ", lireTete(liste4))
print()
print("Supprimer tête")
liste4 = supprimerTete(liste4)
print("La liste 4 sans la tête est : ", liste4)
print("La liste 4 contient : ",liste4)
print()
print("Inserer tête")
liste4 = insererTete(5, liste4)
print("La liste 4 contient : ",liste4)
print("La liste 4 est vide : ",estVide(liste4))
print("La tête de la liste est : ", lireTete(liste4))
print("La liste 4 contient : ",liste4)
print()
print("Inserer tête")
liste4 = insererTete(2, liste4)
print("La liste 4 contient : ",liste4)
print("La liste 4 est vide : ",estVide(liste4))
print("La tête de la liste est : ", lireTete(liste4))
print("La liste 4 contient : ",liste4)
print()
print("Inserer tête")
liste4 = insererTete(8, liste4)
print("La liste 4 contient : ",liste4)
print("La liste 4 est vide : ",estVide(liste4))
print("La tête de la liste est : ", lireTete(liste4))
print("La liste 4 contient : ",liste4)
print()
print("Inserer tête")
liste4 = insererTete(15, liste4)
print("La liste 4 contient : ",liste4)
print("La liste 4 est vide : ",estVide(liste4))
print("La tête de la liste est : ", lireTete(liste4))
print("La liste 4 contient : ",liste4)
print()
print("Inserer tête")
liste4 = insererTete(3, liste4)
print("La liste 4 contient : ",liste4)
print("La liste 4 est vide : ",estVide(liste4))
print("La tête de la liste est : ", lireTete(liste4))
print("La liste 4 contient : ",liste4)
print()
print("Supprimer tête")
liste4 = supprimerTete(liste4)
print("La liste 4 sans la tête est : ", liste4)
print("La liste 4 est vide : ",estVide(liste4))
print("La tête de la liste est : ", lireTete(liste4))
print("La liste 4 contient : ",liste4)
print()
print("Supprimer tête")
liste4 = supprimerTete(liste4)
print("La liste 4 sans la tête est : ", liste4)
print("La liste 4 est vide : ",estVide(liste4))
print("La tête de la liste est : ", lireTete(liste4))
print("La liste 4 contient : ",liste4)
print()
print("Supprimer tête")
liste4 = supprimerTete(liste4)
print("La liste 4 sans la tête est : ", liste4)
print("La liste 4 est vide : ",estVide(liste4))
print("La tête de la liste est : ", lireTete(liste4))
print("La liste 4 contient : ",liste4)
print()
print("Supprimer tête")
liste4 = supprimerTete(liste4)
print("La liste 4 sans la tête est : ", liste4)
print("La liste 4 est vide : ",estVide(liste4))
print("La tête de la liste est : ", lireTete(liste4))
print("La liste 4 contient : ",liste4)
print()
print("Supprimer tête")
liste4 = supprimerTete(liste4)
print("La liste 4 sans la tête est : ", liste4)
print("La liste 4 est vide : ",estVide(liste4))
print("La tête de la liste est : ", lireTete(liste4))
print("La liste 4 contient : ",liste4)
print()
print("Supprimer tête")
liste4 = supprimerTete(liste4)
print("La liste 4 sans la tête est : ", liste4)
print("La liste 4 est vide : ",estVide(liste4))
print("La tête de la liste est : ", lireTete(liste4))
print("La liste 4 contient : ",liste4)


