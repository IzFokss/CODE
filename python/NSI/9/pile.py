def pile():
    # retourne une liste vide
    return []

def vide(p):
    """Renvoie True si la pile est vide et False sinon"""
    return True if p == [] else False

def empiler(p, x):
    """Ajoute l'élément x au début de la pile p"""
    p.insert(0, x)
    return p

def depiler(p):
    """Si la pile n'est pas vide, dépile l'élément du sommet de la pile p sinon
    avertit l'utilisateur que la pile est vide."""
    try:
        x = p.pop(0)
        return x
    except IndexError:
        print("Attention, votre pile est vide !!!")
        return None

def taille(p):
    """Retourne la taille de la pile"""
    if vide(p):
        return 0
    else:
        return len(p)




print(depiler([1,2,3,4,5,6,7,8,9,10]))
