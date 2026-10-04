def ecriture_binaire_entier_positif(n):
    if n == 0:
        return "0"

    resultat = ""

    while n > 0:
        resultat = str(n % 2) + resultat #convertis n%2 en chaine de caractère et l'ajoute à resultat
        n = n // 2 #mets à jour n 

    return resultat


print(ecriture_binaire_entier_positif(0))    
print(ecriture_binaire_entier_positif(2))    
print(ecriture_binaire_entier_positif(25))   
print(ecriture_binaire_entier_positif(105))
