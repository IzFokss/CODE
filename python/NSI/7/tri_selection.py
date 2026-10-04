def echange(x,y,tab):
  """Fonction permettant d'échanger deux valeurs d'une liste
  ::param (x) :: premier élément à échanger
  ::param (y) :: deuxième élément à échanger
  ::return tab"""
  temp = tab[x]
  tab[x] = tab[y]
  tab[y] = temp
  return tab

def tri_selection(tab):
  n = len(tab)
  for i in range(n):
    indice_min = i
    for j in range(i + 1, n):
      if tab[j] < tab[indice_min]:
        indice_min = j
    if indice_min != i:
      echange(i, indice_min, tab)
  return tab


print(tri_selection([9,4,5,6,1,3,2,8,7]))