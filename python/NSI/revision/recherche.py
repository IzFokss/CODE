def recherche(tab,n):
  indice = 0
  for i in range(len(tab)):
    if tab[i]==n:
      indice = i 
  
  if indice == 0:
    return None
  else:
    return indice
  
    

print(recherche([3,2,3,4,3,5,6],3))
print(recherche([3,2,3,4,3,5,6],7))