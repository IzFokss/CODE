'''Implémentation de type abstrait Liste en utilisant le type natif list de Python

Liste désigne la structure de données que nous utilisons pour gérer les listes.
Elt désigne la structure de données pouvant être un élément de nos listes.

Description rapide de l'interface :
-----------------------------------
1 ::: nouvelleListe() -> Liste
2 ::: estVide(liste:Liste) -> bool
3 ::: compteListe((liste:Liste) -> int
4 ::: afficherListe(liste:Liste) -> str
5 ::: lireElement(liste:Liste, index:int) -> Elt
6 ::: insererElement(x:Elt, liste:Liste, position:int) -> Liste
7 ::: supprimerElement(liste:Liste, position:int)  -> Liste
'''

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
      print("Attention la liste est vide")
      return True
    return False

def compteListe(lst):
  """Renvoie la taille de la liste
  :: param lst(Liste) :: une liste
  """
  return len(lst)

def afficherListe(lst):
  '''Renvoie une représentation de la Liste sous forme d'une séquence commençant par la tête
  :: param lst(Liste) :: une liste
  :: return (str) :: un string représentant notre liste
  '''
  return str(lst)

def lireElement(lst, position):
  '''Renvoie la valeur stockée à la position voulue
  :: param lst(Liste) :: une liste
  :: param position(int) :: une valeur d'index valide pour cette liste
  :: return (Elt) :: la valeur voulue
  '''
  if estVide(lst)==True:
    return None
  else:
    return lst[position]

def insererElement(x, lst, position):
  '''Renvoie une Liste en insérant x à la position position.
  :: param x(Elt) :: l'élément à insérer, compatible avec la liste
  :: param lst(Liste) :: une liste
  :: param position(int) :: une valeur d'index valide pour cette liste
  :: return (Liste) :: la nouvelle liste
  '''
  list2 = [element for element in lst] # copie à l'identique de la liste
  list2.insert(position, x)            # insertion de l'élément à la position voulue
  return list2                         # On renvoie la nouvelle liste

def supprimerElement(lst, position):
  '''Renvoie une nouvelle liste où on a supprimé l'élément situé à la position fournie
  :: param lst(Liste) :: une liste
  :: param position(int) :: une valeur d'index valide pour cette liste
  :: return (Liste) :: la nouvelle liste
  '''
  if estVide(lst) == True:
    return []
  else:
    list2 = [element for element in lst] # copie à l'identique de la liste
    list2.pop(position)                   # suppression de l'élément à la position voulue
    return list2                          # On renvoie la nouvelle liste

print("Nouvelle liste")
liste4 = nouvelleListe()
print("La liste 4 contient : ",liste4)
print("La liste 4 est vide : ",estVide(liste4))
print("La tête de la liste est : ", lireElement(liste4,1))
print()
print("Supprimer tête")
print("La liste 4 contient : ",liste4)
liste4 = supprimerElement(liste4,0)
print("La liste 4 sans la tête est : ", liste4)
print()
print("Inserer tête")
liste4 = insererElement(5, liste4,0)
print("La liste 4 contient : ",liste4)
print("La liste 4 est vide : ",estVide(liste4))
print("La tête de la liste est : ", lireElement(liste4,0))
print()
print("Inserer tête")
liste4 = insererElement(2, liste4,0)
print("La liste 4 contient : ",liste4)
print("La liste 4 est vide : ",estVide(liste4))
print("La tête de la liste est : ", lireElement(liste4,0))
print()
print("Inserer tête")
liste4 = insererElement(8, liste4,0)
print("La liste 4 contient : ",liste4)
print("La liste 4 est vide : ",estVide(liste4))
print("La tête de la liste est : ", lireElement(liste4,0))
print()
print("Inserer tête")
liste4 = insererElement(15, liste4,0)
print("La liste 4 contient : ",liste4)
print("La liste 4 est vide : ",estVide(liste4))
print("La tête de la liste est : ", lireElement(liste4,0))
print()
print("Inserer tête")
liste4 = insererElement(3, liste4,0)
print("La liste 4 contient : ",liste4)
print("La liste 4 est vide : ",estVide(liste4))
print("La tête de la liste est : ", lireElement(liste4,0))
print()
print("Supprimer tête")
liste4 = supprimerElement(liste4,0)
print("La liste 4 sans la tête est : ", liste4)
print("La liste 4 est vide : ",estVide(liste4))
print("La tête de la liste est : ", lireElement(liste4,0))
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
print(afficherListe(liste4))
