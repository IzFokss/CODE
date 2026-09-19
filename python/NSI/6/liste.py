'''Implémentation du type abstrait Liste en utilisant des tuples (tete, queue)'''
def nouvelleListe():
    '''Renvoie une liste vide
    :: return (Liste) :: renvoie une liste vide sous forme d'un tuple vide ()
    '''
    return ()

def estVide(lst):
    '''Renvoie True si la liste est vide
    :: param lst(Liste) :: une liste à tester
    :: return (bool) :: True si la liste est un tuple vide ()
    '''
    if lst == ():
        return True
    return False

def insererTete(x, lst):
    '''Renvoie une nouvelle liste où x est la tête et liste la queue
    :: param x(Elt) :: un élément compatible avec votre liste qui devient la tête
    :: param lst(Liste) :: la liste qui va devenir la queue de la nouvelle
    :: return (Liste) :: la nouvelle liste
    '''
    return (x, lst)

def lireTete(lst):
    '''Renvoie la tête de la liste, sans toucher à la liste elle-même
    :: param lst(Liste) :: la liste dont on désire lire la tête
    :: return (Elt) :: la tête voulue, None si la tête est vide
    '''
    if not estVide(lst):
        return lst[0] # la valeur envoyée est la première partie du tuple

def supprimerTete(lst):
    '''Renvoie une nouvelle liste où on a supprimé la tête de l'ancienne
    :: param lst(Liste) :: la liste dont on supprime la tête
    :: return (Liste) :: la nouvelle liste
    '''
    if estVide(lst):
        return nouvelleListe() # la liste envoyée est ()
    else:
        return lst[1] # la liste envoyée est est la deuxième partie du tuple

def afficherListe(lst):
    '''Renvoie une représentation de la Liste sous forme d'une séquence commençant par la tête
    :: param lst(Liste) :: une liste
    :: return liste(Liste) :: la liste
    '''
    liste = []
    while not (estVide(lst)) and lireTete(lst) != None:
        tete = lireTete(lst)
        liste.append(tete)
        lst = supprimerTete(lst)
    return liste

def compteListe (lst):
    return len(afficherListe(lst))




def lireElement(lst,position):
    """Renvoie la valeur d'un élément à une certaine position de la liste
    ::param lst(Liste) :: une liste
    ::param position(int) :: une valeur de position valide pour cette liste
    ::return  (Elt)  :: la valeur située à cette position"""
    for i in range(position):
        lst = supprimerTete(lst)
    return lireTete(lst)

def insererElement(x, lst, position):
    """ Renvoie une représentation de la Liste contenant le nouvel élément
    ::param x(Elt) :: l'élément à insérer, compatible avec la liste
    ::param lst(Liste) :: une liste
    ::param position(int) :: une valeur d'index valide pour cette liste
    ::return(Liste) :: la nouvelle liste
    """
    lesTetes = []
    for i in range(position):
        lesTetes.append(lireTete(lst))
        lst = supprimerTete(lst)
    lst = insererTete(x, lst)
    for j in range(len(lesTetes) - 1, -1, -1): 
        lst = insererTete(lesTetes[j], lst)
    return lst

def supprimerElement(lst,position):
    """Renvoie une représentation de la Liste ne contenant plus l'élément
    supprimer sous forme d'une séquence commençant par la tête
    ::param lst(Liste) ::une Liste
    ::param position(int) :: une valeur d'index valide pour cette liste
    ::return (Liste) :: la nouvelle liste"""
    lesTetes = []
    for i in range(position):
        lesTetes.append(lireTete(lst))
        lst = supprimerTete(lst)
    lst = supprimerTete(lst)
    for j in range(len(lesTetes) -1,-1,-1):
        lst = insererTete(lesTetes[j],lst)
    return lst


        



liste1 = ()
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
print("La liste 4 convertie en type list est : ",afficherListe(liste4))
print()
print("Le nombre d'éléments dans la liste 4 est : ",compteListe(liste4))


for i in range(len(afficherListe(liste4))):
    print("La valeur en position", i,"est:",lireElement(liste4,i))
print()
print("Ajouter un élément à une certaine position")
print("la liste 4 contient : ", liste4)
liste4 = insererElement(88,liste4,2)
print("après insertion, la liste 4 contient : ",liste4)
print()
print("supprimer un élément à une certaine position")
print("la liste 4 contient : ", liste4)
liste4 = supprimerElement(liste4,3)
print("après supression, la liste 4 contient : ",liste4)
print()
print("La liste 4 convertie en type list est : ",afficherListe(liste4))
print()
print("Le nombre d'éléments dans la liste 4 est : ",compteListe(liste4))