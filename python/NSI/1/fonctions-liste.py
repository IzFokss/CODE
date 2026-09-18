def nouvelleListe():
    return []
    
def estVide(L):
    if len(L) == 0:
        return True
    return False
        
def insererTete(x,L):
    L.insert(0,x)
    return L

def lireTete(L):
    if estVide(L) ==False:
        return (L[0],L)

def supprimerTete(L):
    if estVide(L) == False:
        x = L[0]
        L = L[1:]
        return (x,L)
    else:
        return []
        
def afficherListe(L):
    liste = []
    while not estVide(L):
        tete, L = lireTete(L)
        liste.append(tete)
        L = supprimerTete(L)[1]  
    return liste
    
liste1 = []
liste2 = []
liste3 = ["c"]

print("La liste 1 contient: ",liste1)
print("La liste 1 est vide : ", estVide(liste1))
print("La liste 2 contient : ",liste2)
print("La liste 2 est vide : ",estVide(liste2))
print("La liste 3 contient: ",liste3)
print("La liste 3 est vide : ", estVide(liste3))
print()
print('ATTENTION!')
print("Seule la liste 4 respecte l'interface TAD")
print("Les listes 1 à 3 sont crées sans passer par la fonction d'interface nouvelleListe")
print()
print("Nouvelle Liste")
liste4 = nouvelleListe()
print("la liste 4 contient : ",liste4)
print("La liste 4 est vide : ",estVide(liste4))
print("la tete de la liste 4 est :",lireTete(liste4))
print()
print("Supprimer Tete")
liste4 = supprimerTete(liste4)
print("la liste 4 sans la tete est: ",liste4)
print("la liste 4 contient : ",liste4)
print()
print("Inserer Tete")
liste4 = insererTete(5,liste4)
print("la liste 4 contient : ",liste4)
print("La liste 4 est vide : ",estVide(liste4))
print("La tete de la liste est : ",lireTete(liste4))
print("la liste 4 contient : ",liste4)
print()
print("Inserer Tete")
liste4 = insererTete(2,liste4)
print("la liste 4 contient : ",liste4)
print("La liste 4 est vide : ",estVide(liste4))
print("La tete de la liste est : ",lireTete(liste4))
print("la liste 4 contient : ",liste4)
print()
print("Inserer Tete")
liste4 = insererTete(8,liste4)
print("la liste 4 contient : ",liste4)
print("La liste 4 est vide : ",estVide(liste4))
print("La tete de la liste est : ",lireTete(liste4))
print("la liste 4 contient : ",liste4)
print()
print("Inserer Tete")
liste4 = insererTete(15,liste4)
print("la liste 4 contient : ",liste4)
print("La liste 4 est vide : ",estVide(liste4))
print("La tete de la liste est : ",lireTete(liste4))
print("la liste 4 contient : ",liste4)
print("Inserer Tete")
liste4 = insererTete(3,liste4)
print("la liste 4 contient : ",liste4)
print("La liste 4 est vide : ",estVide(liste4))
print("La tete de la liste est : ",lireTete(liste4))
print("la liste 4 contient : ",liste4)
print()
print("Supprimer Tete")
liste4= supprimerTete(liste4)
print("La liste 4 sans la tete est : ",liste4)
print("La liste 4 est vide : ",estVide(liste4))
print("La tete de la liste est : ",lireTete(liste4))
print("la liste 4 contient : ",liste4)