def ligne_suivante(ligne):
    '''Renvoie la ligne suivant ligne du triangle de Pascal'''
    ligne_suiv = [1] 
    for i in range(1,len(ligne)): 
        ligne_suiv.append(ligne[i-1]+ligne[i]) 
    ligne_suiv.append(1) 
    return ligne_suiv

def pascal(n):
    '''Renvoie le triangle de Pascal de hauteur n'''
    triangle = [ [1] ]
    for k in range(n): 
        ligne_k = ligne_suivante(triangle[-1])
        triangle.append(ligne_k)
    return triangle
    
    
    
    
print(pascal(4))


