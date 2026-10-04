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


def lireElement(lst, position):
  '''Renvoie la valeur stockée à la position voulue
  :: param lst(Liste) :: une liste
  :: param position(int) :: une valeur d'index valide pour cette liste
  :: return (Elt) :: la valeur voulue
  '''
  return lst[position]

def insererElement(x, lst, position):
  '''Renvoie une Liste en insérant x à la position position.
  :: param x(Elt) :: l'élément à insérer, compatible avec la liste
  :: param lst(Liste) :: une liste
  :: param position(int) :: une valeur d'index valide pour cette liste
  :: return (Liste) :: la nouvelle liste
  '''
  list2 = [0 for x in range(len(lst) + 1)]  # On crée une liste plus longue de 1
  for index in range(position):
    list2[index] = lst[index]  # copie à l'identique jusqu'à la position
  list2[position] = x  # On place l'élément à sa position
  for index in range(position, len(lst)):
    list2[index + 1] = lst[index]  # Décalage vers la droite jusqu'à la fin
  return list2  # On renvoie la nouvelle liste

def supprimerElement(lst, position):
  '''Renvoie une nouvelle liste où on a supprimé l'élément situé à la position fournie
  :: param lst(Liste) :: une liste
  :: param position(int) :: une valeur d'index valide pour cette liste
  :: return (Liste) :: la nouvelle liste
  '''
  list2 = [0 for x in range(len(lst) - 1)]  # On crée une liste plus courte de 1
  for index in range(position):
    list2[index] = lst[index]  # copie à l'identique jusqu'à la position
  for index in range(position, len(list2)):
      list2[index] = lst[index + 1]  # Décalage vers la gauche jusqu'à la fin
  return list2  # On renvoie la nouvelle liste

def compteListe(lst):
  """Renvoie la taille de la liste
  :: param lst(Liste) :: une liste
  """
  return len(lst)

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
print("Ajouter un élément à une certaine position")
print("La liste 4 contient : ", liste4)
liste4=insererElement(88,liste4,2)
print("Après insertion la liste 4 contient : ", liste4)
print()
print("Supprimer un élément à une certaine position")
print("La liste 4 contient : ", liste4)
liste4=supprimerElement(liste4,3)
print("Après suppression la liste 4 contient : ", liste4)
print()
print("Le nombre d'éléments dans la liste 4 est : ",compteListe(liste4))
